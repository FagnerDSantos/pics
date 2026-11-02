from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Message, Receive, Scope, Send

MAX_REQUEST_BODY_SIZE = 1024 * 1024


class RequestBodyLimitMiddleware:
    """Buffer request bodies only up to the configured maximum size."""

    def __init__(
        self,
        app: ASGIApp,
        max_body_size: int = MAX_REQUEST_BODY_SIZE,
    ) -> None:
        self.app = app
        self.max_body_size = max_body_size

    async def __call__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send,
    ) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        messages: list[Message] = []
        body_size = 0

        while True:
            message = await receive()
            if message["type"] == "http.disconnect":
                messages.append(message)
                break

            chunk = message.get("body", b"")
            body_size += len(chunk)
            if body_size > self.max_body_size:
                response = JSONResponse(
                    status_code=413,
                    content={"detail": "Request body too large"},
                )
                await response(scope, receive, send)
                return

            messages.append(message)
            if not message.get("more_body", False):
                break

        message_index = 0

        async def replay_receive() -> Message:
            nonlocal message_index
            if message_index < len(messages):
                message = messages[message_index]
                message_index += 1
                return message
            return {"type": "http.disconnect"}

        await self.app(scope, replay_receive, send)
