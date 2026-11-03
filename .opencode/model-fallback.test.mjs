import assert from "node:assert/strict"
import test from "node:test"
import ModelFallbackPlugin from "./plugins/model-fallback.js"
import {
  hasPartialAssistantOutput,
  isRetryableProviderError,
  nextFallbackModel,
} from "./model-fallback-core.mjs"

const chain = [
  "opencode-go/gpt-6-luna",
  "opencode-go/kimi-k3",
  "opencode-go/deepseek-v4-pro",
  "opencode-go/glm-5.3",
  "opencode/deepseek-v4.1-flash-free",
]

test("classifies rate limit, quota and unavailable-service errors", () => {
  assert.equal(isRetryableProviderError({ data: { statusCode: 429, message: "Too many requests" } }), true)
  assert.equal(isRetryableProviderError({ data: { statusCode: 402, message: "Usage limit reached" } }), true)
  assert.equal(isRetryableProviderError({ data: { statusCode: 503, message: "Unavailable" } }), true)
  assert.equal(isRetryableProviderError({ data: { statusCode: 400, message: "This Go model requires Global regions" } }), true)
  assert.equal(isRetryableProviderError({ data: { statusCode: 400, message: "Bad request" } }), false)
})

test("walks fallback models in the configured priority order", () => {
  assert.equal(nextFallbackModel(chain, chain[0]), chain[1])
  assert.equal(nextFallbackModel(chain, chain[1]), chain[2])
  assert.equal(nextFallbackModel(chain, chain[2]), chain[3])
  assert.equal(nextFallbackModel(chain, chain[3]), chain[4])
  assert.equal(nextFallbackModel(chain, chain[4]), undefined)
})

test("does not replay a turn after assistant output or any tool call", () => {
  const userID = "user-1"
  assert.equal(
    hasPartialAssistantOutput([
      { info: { role: "user", id: userID }, parts: [{ type: "text", text: "Change a file" }] },
      { info: { role: "assistant", id: "assistant-1" }, parts: [{ type: "tool", tool: "edit" }] },
    ], userID),
    true,
  )
  assert.equal(
    hasPartialAssistantOutput([
      { info: { role: "user", id: userID }, parts: [{ type: "text", text: "Answer" }] },
      { info: { role: "assistant", id: "assistant-1" }, parts: [{ type: "text", text: "Partial" }] },
    ], userID),
    true,
  )
  assert.equal(
    hasPartialAssistantOutput([
      { info: { role: "user", id: userID }, parts: [{ type: "text", text: "Answer" }] },
      {
        info: { role: "assistant", id: "assistant-1", error: { name: "APIError" } },
        parts: [{ type: "step-start" }, { type: "error" }],
      },
    ], userID),
    false,
  )
})

test("submits one automatic fallback after a safe 429 error", async () => {
  const userID = "user-original"
  const assistantID = "assistant-failed"
  const submitted = []
  const client = {
    session: {
      messages: async () => ({
        data: [
          {
            info: {
              id: userID,
              role: "user",
              agent: "build",
              model: { providerID: "opencode-go", modelID: "gpt-6-luna" },
              time: { created: 1 },
            },
            parts: [{ type: "text", text: "Return only OK" }],
          },
          {
            info: {
              id: assistantID,
              role: "assistant",
              sessionID: "session-1",
              providerID: "opencode-go",
              modelID: "gpt-6-luna",
              error: { name: "APIError", data: { statusCode: 429, message: "Rate limit" } },
              time: { created: 2 },
            },
            parts: [{ type: "error", text: "Rate limit" }],
          },
        ],
      }),
      promptAsync: async (request) => submitted.push(request),
    },
    app: { log: async () => ({}) },
  }
  const plugin = await ModelFallbackPlugin({ client, directory: process.cwd() })
  const event = {
    type: "session.error",
    properties: {
      sessionID: "session-1",
      error: { name: "APIError", data: { statusCode: 429, message: "Rate limit" } },
    },
  }

  await plugin.event({ event })
  await plugin.event({ event })

  assert.equal(submitted.length, 1)
  assert.deepEqual(submitted[0].body.model, { providerID: "opencode-go", modelID: "kimi-k3" })
  assert.equal(submitted[0].body.parts[0].text, "Return only OK")
})
