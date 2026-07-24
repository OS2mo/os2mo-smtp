# SPDX-FileCopyrightText: Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0

from datetime import datetime
from uuid import UUID
from enum import Enum

from cronsim import CronSim
from cronsim import CronSimError
from fastramqpi.config import Settings as FastRAMQPISettings
from fastramqpi.ramqp.config import AMQPConnectionSettings
from pydantic import BaseSettings
from pydantic import Field
from pydantic import PositiveInt
from pydantic import validator


class SmtpAMQPConnectionSettings(AMQPConnectionSettings):
    queue_prefix = "smtp"
    prefetch_count = 1  # MO cannot handle too many requests


class SmtpFastRAMQPISettings(FastRAMQPISettings):
    amqp: SmtpAMQPConnectionSettings
    mo_graphql_version: PositiveInt = 22


class SMTPSecurity(Enum):
    NONE = "none"
    STARTTLS = "starttls"
    TLS = "tls"


class Settings(BaseSettings):
    class Config:
        frozen = True
        env_nested_delimiter = "__"

    fastramqpi: SmtpFastRAMQPISettings

    application_name: str = "os2mo_email_listener"

    root_loen_org: UUID | None = None
    alert_manager_removal_use_org_unit_emails: bool = False
    alert_manager_removal_exclude_org_units: list[UUID] = Field(
        [],
        description=(
            "Org unit UUIDs to exclude from manager removal alerts. Events for "
            "these org units and their descendants are ignored."
        ),
    )

    # Listeners
    enable_manager_events: bool = False
    enable_rolebinding_events: bool = False
    enable_ituser_events: bool = False
    enable_org_unit_events: bool = False
    enable_related_unit_events: bool = False

    advance_notice_days: int = Field(
        7,
        description=(
            "How many days before a future-dated change takes effect its alert "
            "is sent. Events earlier than that are deferred back to the event "
            "system with an X-Not-Before header. Applies to every alert type."
        ),
    )

    notification_send_schedule: str | None = Field(
        None,
        description=(
            "Cron expression restricting when alerts are sent, e.g. '0 0 * * *' "
            "to batch all mails at midnight. At any other time, events are "
            "deferred with an X-Not-Before header and wait in the event system "
            "until the next scheduled time. Unset means alerts are sent "
            "immediately. Evaluated in the container's local time."
        ),
    )

    @validator("notification_send_schedule")
    def validate_cron_expression(cls, value: str | None) -> str | None:
        if value is not None:
            try:
                CronSim(value, datetime.now())
            except CronSimError as e:
                raise ValueError(f"Invalid cron expression {value!r}: {e}") from e
        return value


class EmailSettings(BaseSettings):
    class Config:
        frozen = True
        env_nested_delimiter = "__"

    smtp_user: str | None = Field(None, description="SMTP user")
    smtp_password: str | None = Field(None, description="SMTP password")
    sender: str = "os2mo@magenta.dk"
    smtp_port: int = Field(..., description="SMTP port")
    smtp_host: str = Field(..., description="SMTP host. For example 'smtp.gmail.com' ")
    smtp_security: SMTPSecurity
    dry_run: bool = Field(
        False,
        description="When True, will print mails to the console but not send anything",
    )
    receiver_override: str = Field(
        "",
        description=(
            "Set to an email address to always send mails to this address. "
            "Useful for testing purposes."
        ),
    )
    receivers: list[str] = Field([], description="Email addresses to send mail to")
    smtp_timeout: int = Field(
        30,
        description="Timeout in seconds for SMTP connectivity check at startup",
    )
