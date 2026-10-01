"""Shared pytest fixtures."""

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app


@pytest.fixture
def client() -> Iterator[TestClient]:
    """A test client for an app built with test settings, ignoring any local .env."""
    settings = Settings(_env_file=None, env="test")
    with TestClient(create_app(settings)) as test_client:
        yield test_client
