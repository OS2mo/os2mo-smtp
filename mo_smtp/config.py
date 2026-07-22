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

    enable_notification_queue: bool = Field(
        False,
        description=(
            "When True, events queue their alerts instead of emailing "
            "immediately; the queue is processed on notification_send_schedule. "
            "Repeated events for the same object coalesce into one email."
        ),
    )
    notification_send_schedule: str = Field(
        "0 1 * * *",
        description=(
            "Cron expression for when the notification queue is processed, "
            "evaluated in the container's local time."
        ),
    )

    @validator("notification_send_schedule")
    def validate_cron_expression(cls, value: str) -> str:
        try:
            CronSim(value, datetime.now())
        except CronSimError as e:
            # Re-raise as ValueError so pydantic reports it as a validation error.
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
