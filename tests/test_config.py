# SPDX-FileCopyrightText: Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0

from typing import Any

import pytest
from pydantic import ValidationError

from mo_smtp.config import Settings


def test_invalid_notification_send_schedule_is_rejected(
    load_settings_overrides: dict[str, Any],
) -> None:
    """A malformed cron expression fails at startup instead of silently never
    firing the notification queue."""
    with pytest.raises(ValidationError):
        Settings(notification_send_schedule="not a cron expression")
