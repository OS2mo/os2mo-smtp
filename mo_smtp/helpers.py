# SPDX-FileCopyrightText: Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0

from datetime import UTC
from datetime import datetime
from datetime import timedelta
from typing import Protocol
from typing import TypeVar

import structlog
from cronsim import CronSim
from fastapi import Header
from fastapi import HTTPException
from more_itertools import only

from . import depends

logger = structlog.get_logger()


class EventDeferred(HTTPException):
    """Ask the event system to redeliver the event at `not_before`."""

    def __init__(self, not_before: datetime, detail: str) -> None:
        logger.info(
            "Deferring the event", reason=detail, not_before=not_before.isoformat()
        )
        super().__init__(
            status_code=425,  # Too Early
            detail=detail,
            headers={"X-Not-Before": not_before.isoformat()},
        )


def defer_until_advance_notice(
    effective: datetime | None, settings: depends.Settings
) -> None:
    """Defer the event when a change takes effect further ahead than
    advance_notice_days — its alert should arrive with that much notice."""
    if effective is None:
        return
    not_before = effective - timedelta(days=settings.advance_notice_days)
    if datetime.now(UTC) < not_before:
        raise EventDeferred(not_before, "Change takes effect in the future")


async def enforce_send_schedule(
    settings: depends.Settings,
    x_not_before: str | None = Header(default=None),
) -> None:
    """Batch alerts to the send schedule, e.g. nightly.

    Off-schedule events are deferred until the schedule's next tick, so they
    wait in the event system and are processed together once it arrives. A
    redelivered event carries the X-Not-Before it was deferred to, which keeps
    the whole batch due while it drains.
    """
    if settings.notification_send_schedule is None:
        return
    send_time = next_send_time(
        settings.notification_send_schedule,
        datetime.now().astimezone(),
        datetime.fromisoformat(x_not_before) if x_not_before else None,
    )
    if send_time is not None:
        raise EventDeferred(send_time, "Outside the notification send schedule")


def next_send_time(
    schedule: str, now: datetime, not_before: datetime | None = None
) -> datetime | None:
    """The schedule's next tick to defer to, or None if it is send time.

    It is send time when `now` falls within a tick's minute (a cron tick lasts
    its whole minute, as in cron itself), or when the event was delivered with
    the not-before it was previously deferred to and that target falls within
    the current send cycle — at or after the schedule's most recent tick. The
    latter lets a batch keep draining past its tick's minute: every event
    deferred to that tick stays due until the next one.
    """
    minute = now.replace(second=0, microsecond=0)
    tick = next(CronSim(schedule, minute - timedelta(minutes=1)))
    if tick == minute:
        return None
    if not_before is not None:
        previous_tick = next(CronSim(schedule, now, reverse=True))
        if previous_tick <= not_before <= now:
            return None
    return tick


class Validity(Protocol):
    @property
    def from_(self) -> datetime | None:  # pragma: no cover
        ...

    @property
    def to(self) -> datetime | None:  # pragma: no cover
        ...


class ValidityModel(Protocol):
    @property
    def validity(self) -> Validity:  # pragma: no cover
        ...


T = TypeVar("T", bound=ValidityModel)


def extract_current_or_latest_validity(validities: list[T]) -> T | None:
    """
    Check each validity in a list of validities and return the one which is either
    valid today, or has the latest end-date
    """
    if len(validities) <= 1:
        return only(validities)

    def is_current(val: T) -> bool:
        # Cannot use datetime.utcnow as it is not timezone aware
        now_utc = datetime.now(UTC)

        match (val.validity.from_, val.validity.to):
            case (start, None):
                assert start is not None
                return start < now_utc
            case (start, end):
                assert start is not None
                assert end is not None
                return start < now_utc < end
            case _:  # pragma: no cover
                raise AssertionError()

    # If any of the validities is valid today, return it
    current_validity = only(filter(is_current, validities))
    if current_validity:
        return current_validity
    # Otherwise return the latest
    # TODO: Does this actually make sense? - Should we not return the one which is the
    #       closest to now, rather than the one that is the furthest into the future?
    # Cannot use datetime.max directly as it is not timezone aware
    datetime_max_utc = datetime.max.replace(tzinfo=UTC)
    latest_validity = max(
        validities, key=lambda val: val.validity.to or datetime_max_utc
    )
    return latest_validity
