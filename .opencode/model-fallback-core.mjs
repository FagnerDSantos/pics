const DEFAULT_CONFIG = {
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

function errorText(error) {
  if (!error || typeof error !== "object") return ""
  const data = error.data && typeof error.data === "object" ? error.data : {}
  const nested = data.error && typeof data.error === "object" ? data.error : {}
  return [error.message, data.message, nested.message]
    .filter((item) => typeof item === "string")
    .join(" ")
    .toLowerCase()
}

export function isRetryableProviderError(error, config = DEFAULT_CONFIG) {
  if (!error || typeof error !== "object") return false
  const data = error.data && typeof error.data === "object" ? error.data : {}
  const status = Number(error.statusCode ?? error.status ?? data.statusCode)
  const message = errorText(error)
  if (status === 402) return true
  if (config.retryableStatusCodes.includes(status)) return true
  if (status === 403 && /quota|usage limit|rate limit|too many requests/i.test(message)) return true
  return config.retryableErrorPatterns.some((pattern) =>
    message.includes(String(pattern).toLowerCase()),
  )
}

export function hasPartialAssistantOutput(messages, userMessageID) {
  if (!Array.isArray(messages)) return true
  const start = messages.findIndex(
    ({ info }) => info?.role === "user" && info.id === userMessageID,
  )
  if (start < 0) return true
  return messages.slice(start + 1).some(({ info, parts = [] }) => {
    if (info?.role !== "assistant") return false
    return parts.some(
      (part) => !["error", "retry", "step-start"].includes(part.type),
    )
  })
}

export function nextFallbackModel(chain, failedModel, attempted = new Set()) {
  const failedIndex = chain.indexOf(failedModel)
  const candidates = failedIndex >= 0 ? chain.slice(failedIndex + 1) : chain
  return candidates.find((model) => !attempted.has(model))
}
