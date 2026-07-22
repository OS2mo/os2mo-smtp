# SPDX-FileCopyrightText: Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0

from datetime import UTC
from datetime import datetime
from typing import Protocol
from typing import TypeVar

from more_itertools import only


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
