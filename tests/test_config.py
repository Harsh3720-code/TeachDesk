import pytest
from pydantic import ValidationError

from app.config import Settings


def test_defaults_match_spec(monkeypatch: pytest.MonkeyPatch) -> None:
    # Stop the developer's shell environment leaking into the defaults.
    for name in (
        "TEACHDESK_ENV",
        "TEACHDESK_LOG_LEVEL",
        "TEACHDESK_ROUTER_MODEL",
        "TEACHDESK_DRAFTING_MODEL",
    ):
        monkeypatch.delenv(name, raising=False)

    settings = Settings(_env_file=None)

    assert settings.env == "local"
    assert settings.log_level == "INFO"
    assert settings.router_model == "claude-haiku-4-5-20251001"
    assert settings.drafting_model == "claude-sonnet-5-5"


def test_env_vars_override_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TEACHDESK_ENV", "production")
    monkeypatch.setenv("TEACHDESK_LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("TEACHDESK_ROUTER_MODEL", "router-model-x")
    monkeypatch.setenv("TEACHDESK_DRAFTING_MODEL", "drafting-model-y")

    settings = Settings(_env_file=None)

    assert settings.env == "production"
    assert settings.log_level == "DEBUG"
    assert settings.router_model == "router-model-x"
    assert settings.drafting_model == "drafting-model-y"


def test_invalid_env_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TEACHDESK_ENV", "staging")

    with pytest.raises(ValidationError):
        Settings(_env_file=None)


def test_invalid_log_level_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TEACHDESK_LOG_LEVEL", "LOUD")

    with pytest.raises(ValidationError):
        Settings(_env_file=None)
