import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BACKEND_DIR / ".env")

DEFAULT_CORS_ORIGINS = "http://localhost:3000"
DEFAULT_APP_VERSION = "0.1.0"


@dataclass(frozen=True)
class Settings:
    cors_origins: list[str]
    app_version: str


def _parse_cors_origins(raw: str) -> list[str]:
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings(
        cors_origins=_parse_cors_origins(
            os.getenv("CORS_ORIGINS", DEFAULT_CORS_ORIGINS)
        ),
        app_version=os.getenv("APP_VERSION", DEFAULT_APP_VERSION),
    )
