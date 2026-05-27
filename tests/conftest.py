import os
from collections.abc import AsyncIterator
from collections.abc import Iterator
from typing import Any

import pytest
from httpx import AsyncClient
from pytest import Item

from mo_smtp.config import Settings


@pytest.hookimpl(trylast=True)
def pytest_collection_modifyitems(items: list[Item]) -> None:
    """Fake `autouse` fixtures for tests marked with integration_test.

    Uses trylast=True so it runs after the fastramqpi plugin's hook, ensuring
    prepended fixtures (like empty_db) end up before the plugin's fixtures.
    """
    for item in items:
        if item.get_closest_marker("integration_test"):
            # MUST prepend to replicate auto-use fixtures coming first
            item.fixturenames[:0] = [  # type: ignore[attr-defined]
                "empty_db",  # Ensure MO database is clean before snapshot
            ]


@pytest.fixture
async def empty_db(
    unauthenticated_mo_client: AsyncClient,
) -> AsyncIterator[None]:
    """Ensure tests are running on an empty database."""
    r = await unauthenticated_mo_client.post("/testing/database/purge")
    r.raise_for_status()
    yield


@pytest.fixture(scope="module")
def settings_overrides_module_scope() -> Iterator[dict[str, Any]]:
    """Fixture to construct dictionary of minimal overrides for valid settings."""
    overrides = {
        "CLIENT_ID": "Foo",
        "CLIENT_SECRET": "bar",
        "DRY_RUN": "True",
        "SMTP_PORT": "25",
        "SMTP_HOST": "smtp.host.com",
        "SMTP_SECURITY": "none",
        "FASTRAMQPI__AMQP__URL": "amqp://guest:guest@msg_broker:5672/",
        "FASTRAMQPI__DATABASE__USER": "fastramqpi",
        "FASTRAMQPI__DATABASE__PASSWORD": "fastramqpi",
        "FASTRAMQPI__DATABASE__HOST": "db",
        "FASTRAMQPI__DATABASE__NAME": "fastramqpi",
    }
    yield overrides


@pytest.fixture(scope="module")
def load_settings_overrides_module_scope(
    settings_overrides_module_scope: dict[str, Any],
) -> Iterator[dict[str, Any]]:
    """Fixture to set happy-path settings overrides as environmental variables."""
    monkeypatch = pytest.MonkeyPatch()
    for key, value in settings_overrides_module_scope.items():
        if os.environ.get(key) is None:
            monkeypatch.setenv(key, value)
        # Debugging line
        print(f"Set {key}={os.environ.get(key)}")
    yield settings_overrides_module_scope


@pytest.fixture
def settings_overrides() -> Iterator[dict[str, str]]:
    """Fixture to construct dictionary of minimal overrides for valid settings.

    Yields:
        Minimal set of overrides.
    """
    overrides = {
        "CLIENT_ID": "Foo",
        "CLIENT_SECRET": "bar",
        "DRY_RUN": "True",
        "SMTP_PORT": "25",
        "SMTP_HOST": "smtp.host.com",
        "SMTP_SECURITY": "none",
        "FASTRAMQPI__AMQP__URL": "amqp://guest:guest@msg_broker:5672/",
        "FASTRAMQPI__DATABASE__USER": "fastramqpi",
        "FASTRAMQPI__DATABASE__PASSWORD": "fastramqpi",
        "FASTRAMQPI__DATABASE__HOST": "db",
        "FASTRAMQPI__DATABASE__NAME": "fastramqpi",
    }
    yield overrides


@pytest.fixture
def load_settings_overrides(
    monkeypatch: pytest.MonkeyPatch,
    settings_overrides: dict[str, str],
) -> Iterator[dict[str, Any]]:
    """Fixture to set happy-path settings overrides as environmental variables."""
    for key, value in settings_overrides.items():
        if os.environ.get(key) is None:
            monkeypatch.setenv(key, value)
    yield settings_overrides


@pytest.fixture
def minimal_valid_settings(load_settings_overrides: None) -> Settings:
    return Settings()
