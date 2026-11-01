from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.main import app

client = TestClient(app)

SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "geolocation=(), camera=(), microphone=()",
}


def test_root() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Pics API"}


def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["service"] == "pics-api"
    assert body["version"] == get_settings().app_version


def test_security_headers() -> None:
    response = client.get("/health")

    for header, value in SECURITY_HEADERS.items():
        assert response.headers[header] == value
