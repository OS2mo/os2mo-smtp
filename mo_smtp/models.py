# SPDX-FileCopyrightText: Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0

from datetime import datetime
from uuid import UUID

from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class SentAlert(Base):
    """A sent alert, recorded so we don't send duplicate emails.

    `relation` alerts dedup on object_uuid (alert once per entry into the
    bad state); `ituser` and `manager` alerts dedup on content_hash (re-alert
    only when the rendered content changes). At most one row per object per
    alert type.
    """

    __tablename__ = "sent_alert"
    __table_args__ = (UniqueConstraint("alert_type", "object_uuid"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    alert_type: Mapped[str] = mapped_column(String(50))
    object_uuid: Mapped[UUID]
    content_hash: Mapped[str | None] = mapped_column(String(64))
    sent_at: Mapped[datetime] = mapped_column(server_default=func.now())
