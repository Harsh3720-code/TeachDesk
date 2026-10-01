"""Application settings, read from TEACHDESK_* environment variables."""

from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed configuration. Values come from the environment or a local .env file.

    Model names are configuration, not code (CLAUDE.md): the defaults below are
    the models named in SPEC.md §4 and are the only place they appear.
    """

    model_config = SettingsConfigDict(
        env_prefix="TEACHDESK_", env_file=".env", extra="ignore"
    )

    env: Literal["local", "test", "production"] = "local"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    router_model: str = "claude-haiku-4-5-20251001"
    drafting_model: str = "claude-sonnet-5-5"
