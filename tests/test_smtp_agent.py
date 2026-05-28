# SPDX-FileCopyrightText: 2019-2020 Magenta ApS
#
# SPDX-License-Identifier: MPL-2.0
from collections.abc import Iterator
from typing import Any
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from mo_smtp.config import Settings
from mo_smtp.smtp_agent import _configure_listeners
from mo_smtp.smtp_agent import create_app


@pytest.fixture(scope="module")
def app(
    load_settings_overrides_module_scope: dict[str, Any],
) -> Iterator[FastAPI]:
    """Test that we can construct our FastAPI application."""

    with patch("mo_smtp.smtp_agent.EmailClient", MagicMock()):
        yield create_app()


@pytest.fixture(scope="module")
def test_client(app: FastAPI) -> Iterator[TestClient]:
    """Fixture to construct a FastAPI test-client.

    Note:
        The app does not do lifecycle management.

    Yields:
        TestClient for the FastAPI application.
    """
    yield TestClient(app)


def test_create_app(
    app: Iterator[FastAPI],
) -> None:
    """Test that we can construct our FastAPI application."""

    assert isinstance(app, FastAPI)


def test_send_test_mail(test_client: TestClient):
    params = {"receiver": "nj@magenta-aps.dk"}
    response = test_client.post("/send_test_email", params=params)
    assert response.status_code == 202


@pytest.mark.parametrize(
    "enabled_env,expected_paths",
    [
        # Opt-in default: nothing fires unless explicitly enabled.
        ({}, set()),
        # A subset enables exactly those listeners.
        (
            {"ENABLE_ADDRESS_EVENTS": "True", "ENABLE_ITUSER_EVENTS": "True"},
            {"/address", "/ituser"},
        ),
        # All six flags wire through to all six listeners.
        (
            {
                "ENABLE_ADDRESS_EVENTS": "True",
                "ENABLE_MANAGER_EVENTS": "True",
                "ENABLE_ROLEBINDING_EVENTS": "True",
                "ENABLE_ITUSER_EVENTS": "True",
                "ENABLE_ORG_UNIT_EVENTS": "True",
                "ENABLE_RELATED_UNIT_EVENTS": "True",
            },
            {
                "/address",
                "/manager",
                "/rolebinding",
                "/ituser",
                "/org_unit",
                "/related_unit",
            },
        ),
    ],
)
def test_configure_listeners(
    load_settings_overrides: dict[str, str],
    monkeypatch: pytest.MonkeyPatch,
    enabled_env: dict[str, str],
    expected_paths: set[str],
) -> None:
    """Each enable_*_events flag declares exactly one matching listener."""
    for key, value in enabled_env.items():
        monkeypatch.setenv(key, value)

    paths = {listener.path for listener in _configure_listeners(Settings())}

    assert paths == expected_paths
