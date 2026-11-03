import { randomUUID } from "node:crypto"
import { readFileSync } from "node:fs"
import { join } from "node:path"
import {
  hasPartialAssistantOutput,
  isRetryableProviderError,
  nextFallbackModel,
} from "../model-fallback-core.mjs"

const DEFAULT_CONFIG = {
  models: [
    "opencode-go/gpt-6-luna",
    "opencode-go/kimi-k3",
    "opencode-go/deepseek-v4-pro",
    "opencode-go/glm-5.3",
    "opencode/deepseek-v4.1-flash-free",
  ],
  cooldownSeconds: 300,
  retryableStatusCodes: [408, 425, 429, 500, 502, 503, 504, 529],
  retryableErrorPatterns: [
    "rate limit",
    "too many requests",
    "quota exceeded",
    "usage limit",
    "limit reached",
    "temporarily unavailable",
    "service unavailable",
    "overloaded",
    "gateway timeout",
    "connection reset",
    "connection refused",
    "socket hang up",
    "network error",
    "fetch failed",
    "requires global regions",
    "not available in your region",
    "region is not available",
    "model is unavailable",
  ],
}

function readConfig(directory) {
  try {
    const config = JSON.parse(
      readFileSync(join(directory, ".opencode", "model-fallback.json"), "utf8"),
    )
    return { ...DEFAULT_CONFIG, ...config }
  } catch {
    return DEFAULT_CONFIG
  }
}

function unwrap(result) {
  return result?.data ?? result
}

function messageModel(info) {
  if (info?.providerID && info?.modelID) {
    return `${info.providerID}/${info.modelID}`
  }
  if (info?.model?.providerID && info?.model?.modelID) {
    return `${info.model.providerID}/${info.model.modelID}`
  }
  return undefined
}

function replayPart(part) {
  if (part.type === "text") {
    return { type: "text", text: part.text, ...(part.synthetic ? { synthetic: true } : {}) }
  }
  if (part.type === "file") {
    return {
      type: "file",
      mime: part.mime,
      ...(part.filename ? { filename: part.filename } : {}),
      url: part.url,
      ...(part.source ? { source: part.source } : {}),
    }
  }
  if (part.type === "agent") return { type: "agent", name: part.name }
  if (part.type === "subtask") {
    return {
      type: "subtask",
      prompt: part.prompt,
      description: part.description,
      agent: part.agent,
    }
  }
  return undefined
}

function latestTurn(messages) {
  let userIndex = -1
  for (let index = 0; index < messages.length; index += 1) {
    if (messages[index]?.info?.role === "user") userIndex = index
  }
  if (userIndex < 0) return undefined
  const user = messages[userIndex]
  const assistant = messages
    .slice(userIndex + 1)
    .findLast(({ info }) => info?.role === "assistant")
  return { user, assistant }
}

async function log(client, level, message, extra = {}) {
  try {
    await client.app.log({
      body: { service: "model-fallback", level, message, extra },
    })
  } catch {
    // Logging must not interfere with a session or a fallback attempt.
  }
}

export default async function ModelFallbackPlugin({ client, directory }) {
  const config = readConfig(directory)
  const sessions = new Map()
  const cooldowns = new Map()
  const inFlight = new Set()

  async function handleFailure(sessionID, error, failedInfo) {
    if (!sessionID || !isRetryableProviderError(error, config) || inFlight.has(sessionID)) return

    const response = await client.session.messages({
      path: { id: sessionID },
      query: { directory },
    })
    const rawMessages = unwrap(response)
    if (!Array.isArray(rawMessages)) return
    const messages = [...rawMessages].sort(
      (left, right) => (left.info?.time?.created ?? 0) - (right.info?.time?.created ?? 0),
    )
    const turn = latestTurn(messages)
    if (!turn?.user?.info?.id || !turn.assistant) return
    if (!turn.assistant.info?.error && !failedInfo?.error) return
    if (hasPartialAssistantOutput(messages, turn.user.info.id)) {
      await log(client, "warn", "Fallback skipped: failed turn already produced output or tool activity", {
        sessionID,
      })
      return
    }

    let state = sessions.get(sessionID)
    const knownUser = state &&
      (state.rootUserID === turn.user.info.id || state.replayUserIDs.has(turn.user.info.id))
    if (!knownUser) {
      state = {
        rootUserID: turn.user.info.id,
        replayUserIDs: new Set(),
        attempted: new Set(),
        handledFailures: new Set(),
      }
      sessions.set(sessionID, state)
    }

    const currentModel = messageModel(turn.assistant.info) ?? messageModel(turn.user.info)
    if (!currentModel) return
    const failureID = turn.assistant.info?.id ?? `${turn.user.info.id}:${currentModel}`
    if (state.handledFailures.has(failureID)) return
    state.handledFailures.add(failureID)
    state.attempted.add(currentModel)
    cooldowns.set(currentModel, Date.now() + config.cooldownSeconds * 1000)

    const chain = config.models.filter((model) => {
      const unavailableUntil = cooldowns.get(model) ?? 0
      return unavailableUntil <= Date.now() || model === currentModel
    })
    const next = nextFallbackModel(chain, currentModel, state.attempted)
    if (!next) {
      await log(client, "error", "Fallback chain exhausted", { sessionID, failedModel: currentModel })
      return
    }

    const slash = next.indexOf("/")
    const parts = (turn.user.parts ?? []).map(replayPart).filter(Boolean)
    if (slash < 1 || parts.length === 0) return

    const retryMessageID = randomUUID()
    state.replayUserIDs.add(retryMessageID)
    inFlight.add(sessionID)
    try {
      await client.session.promptAsync({
        path: { id: sessionID },
        query: { directory },
        body: {
          messageID: retryMessageID,
          model: {
            providerID: next.slice(0, slash),
            modelID: next.slice(slash + 1),
          },
          agent: turn.user.info.agent,
          ...(turn.user.info.tools ? { tools: turn.user.info.tools } : {}),
          parts,
        },
      })
      await log(client, "warn", "Retrying failed turn with fallback model", {
        sessionID,
        failedModel: currentModel,
        fallbackModel: next,
      })
    } catch {
      await log(client, "error", "Fallback request could not be submitted", {
        sessionID,
        fallbackModel: next,
      })
    } finally {
      inFlight.delete(sessionID)
    }
  }

  return {
    event: async ({ event }) => {
      if (event?.type === "session.error") {
        const properties = event.properties ?? {}
        await handleFailure(properties.sessionID, properties.error)
      }
      if (event?.type === "message.updated") {
        const info = event.properties?.info
        if (info?.role === "assistant" && info.error) {
          await handleFailure(info.sessionID, info.error, info)
        }
      }
    },
  }
}
