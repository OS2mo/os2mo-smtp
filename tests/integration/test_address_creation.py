from collections.abc import Awaitable
from collections.abc import Callable
from uuid import UUID
from uuid import uuid4

import pytest
from fastramqpi.pytest_util import retrying
from more_itertools import one
from structlog.testing import capture_logs

CreateEmployee = Callable[[str, str], Awaitable[UUID]]
CreateAddress = Callable[..., Awaitable[UUID]]


@pytest.mark.integration_test
@pytest.mark.envvar({"ENABLE_ADDRESS_EVENTS": "True"})
@pytest.mark.usefixtures("test_client")  # run the app so its listener polls MO
async def test_address_event_is_delivered_end_to_end(
    create_employee: CreateEmployee,
    create_address: CreateAddress,
    email_employee: UUID,
    get_sent_mails: Callable[[], Awaitable[list[dict]]],
) -> None:
    """End-to-end: a real address event flows MO → listener → handler → mail.

    Unlike the other tests, this one enables the address listener and does NOT
    trigger the endpoint manually — it relies on the running app's GraphQL
    event listener to fetch the event MO emits and POST it to the handler. This
    is the one test that proves the listener wiring (routing key + path), at the
    cost of polling for delivery.
    """
    employee = await create_employee("Mick", "Jagger")
    await create_address(
        value="mick@example.com", address_type=email_employee, person=employee
    )

    async for attempt in retrying():
        with attempt:
            msg = one(await get_sent_mails())
            assert msg["recipients"] == ["<mick@example.com>"]


@pytest.mark.integration_test
async def test_address_not_found(
    trigger_event: Callable[[str, UUID], Awaitable[None]],
    get_sent_mails: Callable[[], Awaitable[list[dict]]],
) -> None:
    """A non-existent address UUID sends no email."""
    with capture_logs() as cap_logs:
        await trigger_event("address", uuid4())

    assert "Address not found" in str(cap_logs)
    assert await get_sent_mails() == []


@pytest.mark.integration_test
async def test_org_unit_address_is_ignored(
    create_address: CreateAddress,
    email_unit: UUID,
    create_org_unit: Callable[[str], Awaitable[UUID]],
    trigger_event: Callable[[str, UUID], Awaitable[None]],
    get_sent_mails: Callable[[], Awaitable[list[dict]]],
) -> None:
    """An address belonging to an org unit (not an employee) sends no email."""
    org_unit = await create_org_unit("Stones")
    address = await create_address(
        value="unit@example.com", address_type=email_unit, org_unit=org_unit
    )

    with capture_logs() as cap_logs:
        await trigger_event("address", address)

    assert "The address does not belong to an employee" in str(cap_logs)
    assert await get_sent_mails() == []


@pytest.mark.integration_test
async def test_phone_address_is_ignored(
    create_employee: CreateEmployee,
    create_address: CreateAddress,
    phone_employee: UUID,
    trigger_event: Callable[[str, UUID], Awaitable[None]],
    get_sent_mails: Callable[[], Awaitable[list[dict]]],
) -> None:
    """A non-EMAIL (PHONE) address on an employee sends no email."""
    employee = await create_employee("Mick", "Jagger")
    address = await create_address(
        value="+4512345678", address_type=phone_employee, person=employee
    )

    with capture_logs() as cap_logs:
        await trigger_event("address", address)

    assert "The address type is not EMAIL" in str(cap_logs)
    assert await get_sent_mails() == []


@pytest.mark.integration_test
async def test_existing_email_is_skipped(
    create_employee: CreateEmployee,
    create_address: CreateAddress,
    email_employee: UUID,
    trigger_event: Callable[[str, UUID], Awaitable[None]],
    get_sent_mails: Callable[[], Awaitable[list[dict]]],
) -> None:
    """An employee who already has another email gets no notification."""
    employee = await create_employee("Mick", "Jagger")
    address = await create_address(
        value="first@example.com", address_type=email_employee, person=employee
    )
    await create_address(
        value="second@example.com", address_type=email_employee, person=employee
    )

    with capture_logs() as cap_logs:
        await trigger_event("address", address)

    assert "A previous email address exists" in str(cap_logs)
    assert await get_sent_mails() == []


@pytest.mark.integration_test
async def test_sends_email_no_engagements(
    create_employee: CreateEmployee,
    create_address: CreateAddress,
    email_employee: UUID,
    trigger_event: Callable[[str, UUID], Awaitable[None]],
    get_sent_mails: Callable[[], Awaitable[list[dict]]],
) -> None:
    """An employee with a single email and no engagements gets a basic notice."""
    employee = await create_employee("Mick", "Jagger")
    address = await create_address(
        value="mick@example.com", address_type=email_employee, person=employee
    )

    await trigger_event("address", address)

    msg = one(await get_sent_mails())
    assert msg["subject"] == "Registrering i MO"
    assert msg["recipients"] == ["<mick@example.com>"]
    assert (
        "Denne besked er sendt som bekræftelse på at Mick Jagger er registreret i OS2MO."
        in msg["body"]
    )


@pytest.mark.integration_test
async def test_sends_email_with_engagement_and_manager_cc(
    create_employee: CreateEmployee,
    create_address: CreateAddress,
    email_employee: UUID,
    create_org_unit: Callable[[str], Awaitable[UUID]],
    create_engagement: Callable[[UUID, UUID], Awaitable[UUID]],
    create_manager: Callable[[UUID, UUID], Awaitable[UUID]],
    trigger_event: Callable[[str, UUID], Awaitable[None]],
    get_sent_mails: Callable[[], Awaitable[list[dict]]],
) -> None:
    """An engaged employee gets a notice naming the unit, with the manager CC'd."""
    employee = await create_employee("Mick", "Jagger")
    address = await create_address(
        value="mick@example.com", address_type=email_employee, person=employee
    )
    org_unit = await create_org_unit("Stones")
    await create_engagement(employee, org_unit)

    manager = await create_employee("Keith", "Richards")
    await create_address(
        value="manager@example.com", address_type=email_employee, person=manager
    )
    await create_manager(manager, org_unit)

    await trigger_event("address", address)

    msg = one(await get_sent_mails())
    assert msg["subject"] == "Registrering i MO"
    assert set(msg["recipients"]) == {"<mick@example.com>", "<manager@example.com>"}
    assert (
        "Denne besked er sendt som bekræftelse på at Mick Jagger er registreret i Stones"
        in msg["body"]
    )


@pytest.mark.integration_test
async def test_sends_email_with_multiple_engagements(
    create_employee: CreateEmployee,
    create_address: CreateAddress,
    email_employee: UUID,
    create_org_unit: Callable[[str], Awaitable[UUID]],
    create_engagement: Callable[[UUID, UUID], Awaitable[UUID]],
    create_manager: Callable[[UUID, UUID], Awaitable[UUID]],
    trigger_event: Callable[[str, UUID], Awaitable[None]],
    get_sent_mails: Callable[[], Awaitable[list[dict]]],
) -> None:
    """An employee engaged in multiple units gets all units named, all managers CC'd."""
    employee = await create_employee("Mick", "Jagger")
    address = await create_address(
        value="mick@example.com", address_type=email_employee, person=employee
    )

    for unit_name, manager_email in [
        ("Stones", "stones_manager@example.com"),
        ("Rolling", "rolling_manager@example.com"),
    ]:
        org_unit = await create_org_unit(unit_name)
        await create_engagement(employee, org_unit)
        manager = await create_employee("Manager", unit_name)
        await create_address(
            value=manager_email, address_type=email_employee, person=manager
        )
        await create_manager(manager, org_unit)

    await trigger_event("address", address)

    msg = one(await get_sent_mails())
    assert msg["subject"] == "Registrering i MO"
    assert set(msg["recipients"]) == {
        "<mick@example.com>",
        "<stones_manager@example.com>",
        "<rolling_manager@example.com>",
    }
    # Units appear in non-deterministic order, so assert both are present.
    assert "Stones" in msg["body"]
    assert "Rolling" in msg["body"]
