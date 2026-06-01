from collections.abc import Awaitable
from collections.abc import Callable
from typing import Any

import pytest
from more_itertools import one


@pytest.mark.integration_test
async def test_mailcatcher_roundtrip(
    email_client: Any,
    get_sent_mails: Callable[[], Awaitable[list[dict]]],
) -> None:
    email_client.send_email(
        receiver={"someone@example.com"},
        subject="ping",
        body="pong",
        texttype="plain",
    )

    msg = one(await get_sent_mails())
    assert msg["subject"] == "ping"
    assert msg["recipients"] == ["<someone@example.com>"]
