# SPDX-FileCopyrightText: Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0

from typing import Any

import pytest
from more_itertools import one


@pytest.mark.integration_test
async def test_mailcatcher_roundtrip(email_client: Any, get_sent_mails) -> None:
    email_client.send_email(
        receiver={"someone@example.com"},
        subject="ping",
        body="pong",
        texttype="plain",
    )

    mail = one(await get_sent_mails())
    assert mail.subject == "ping"
    assert mail.recipients == ["<someone@example.com>"]
    assert mail.plain.strip() == "pong"
