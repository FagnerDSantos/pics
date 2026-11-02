import asyncio
from typing import Any

from app.core.errors import register_exception_handlers
from app.middleware.body_limit import RequestBodyLimitMiddleware
from app.middleware.security_headers import SecurityHeadersMiddleware
from fastapi import FastAPI
from fastapi.testclient import TestClient

SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "geolocation=(), camera=(), microphone=()",
}


def test_validation_error_does_not_echo_submitted_values() -> None:
    test_api = FastAPI()
    register_exception_handlers(test_api)

    @test_api.get("/validation")
    def validation_endpoint(value: int) -> dict[str, int]:
        return {"value": value}

    client = TestClient(SecurityHeadersMiddleware(test_api))
    submitted_value = "private-input-123"
    response = client.get("/validation", params={"value": submitted_value})

    assert response.status_code == 422
    assert response.json() == {"detail": "Request validation failed"}
    assert submitted_value not in response.text
    assert "input" not in response.text
    for header, value in SECURITY_HEADERS.items():
        assert response.headers[header] == value


def test_unexpected_error_is_generic_and_keeps_security_headers() -> None:
    test_api = FastAPI()
    register_exception_handlers(test_api)

    @test_api.get("/failure")
    def failure_endpoint() -> None:
        raise RuntimeError("private exception details")

    client = TestClient(
        SecurityHeadersMiddleware(test_api), raise_server_exceptions=False
    )
    response = client.get("/failure")

    assert response.status_code == 500
    assert response.json() == {"detail": "Internal server error"}
    assert "private exception details" not in response.text
    assert "Traceback" not in response.text
    for header, value in SECURITY_HEADERS.items():
        assert response.headers[header] == value


def test_body_limit_ignores_content_length_when_counting_chunks() -> None:
    calls: list[bool] = []
    sent: list[dict[str, Any]] = []
    request_messages = [
        {
            "type": "http.request",
            "body": b"x" * (1024 * 1024 + 1),
            "more_body": False,
        }
    ]

    async def downstream(
        scope: dict[str, Any], receive: Any, send: Any
    ) -> None:
        calls.append(True)

    async def receive() -> dict[str, Any]:
        return request_messages.pop(0)

    async def send(message: dict[str, Any]) -> None:
        sent.append(message)

    scope: dict[str, Any] = {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": "POST",
        "scheme": "http",
        "path": "/",
        "raw_path": b"/",
        "query_string": b"",
        "root_path": "",
        "headers": [(b"content-length", b"1")],
        "client": ("127.0.0.1", 12345),
        "server": ("testserver", 80),
    }

    asyncio.run(RequestBodyLimitMiddleware(downstream)(scope, receive, send))

    assert calls == []
    assert sent[0]["status"] == 413
    assert sent[1]["body"] == b'{"detail":"Request body too large"}'
