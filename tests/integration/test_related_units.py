# SPDX-FileCopyrightText: Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0

from datetime import datetime
from datetime import timezone
from uuid import UUID
from uuid import uuid4

import pytest
from more_itertools import one
from structlog.testing import capture_logs


@pytest.mark.integration_test
async def test_related_units_not_found(trigger_event, get_sent_mails) -> None:
    """A non-existent related-units UUID sends no email."""
    with capture_logs() as cap_logs:
        await trigger_event("related_unit", uuid4())

    assert "Related units not found" in str(cap_logs)
    assert await get_sent_mails() == []


@pytest.mark.integration_test
async def test_related_units_outside_loenorg_is_ignored(
    create_org_unit,
    create_related_units,
    trigger_event,
    get_sent_mails,
) -> None:
    """A relation between units outside the Lønorganisation sends no email."""
    adm_org = await create_org_unit(name="Administration")
    unit_a = await create_org_unit(name="Adm-enhed-1", parent=adm_org)
    unit_b = await create_org_unit(name="Adm-enhed-2", parent=adm_org)
    relation = await create_related_units(origin=unit_a, destination=[unit_b])

    with capture_logs() as cap_logs:
        await trigger_event("related_unit", relation)

    assert "Org unit is not in the Lønorganisation" in str(cap_logs)
    assert await get_sent_mails() == []


@pytest.mark.integration_test
async def test_related_units_deleted_relation_sends_email(
    root_loen_org: UUID,
    create_org_unit,
    create_related_units,
    trigger_event,
    get_sent_mails,
    missing_relation_body,
) -> None:
    """Removing a lønorg unit's only administration relation sends email."""
    loen_root = await create_org_unit(name="Lønorganisation", uuid=root_loen_org)
    loen_unit = await create_org_unit(name="Løn-enhed", parent=loen_root)
    adm_org = await create_org_unit(name="Administration")
    adm_unit = await create_org_unit(name="Adm-enhed", parent=adm_org)
    relation = await create_related_units(origin=loen_unit, destination=[adm_unit])
    await create_related_units(
        origin=loen_unit,
        destination=[],
        from_=datetime(2020, 1, 1, tzinfo=timezone.utc),
    )

    await trigger_event("related_unit", relation)

    mail = one(await get_sent_mails())
    assert mail.subject == "Manglende relation i Lønorganisation"
    assert mail.recipients == ["<datagruppen@silkeborg.dk>"]
    assert mail.plain.strip() == missing_relation_body("Løn-enhed")


@pytest.mark.integration_test
async def test_related_units_existing_relation_sends_no_email(
    root_loen_org: UUID,
    create_org_unit,
    create_related_units,
    trigger_event,
    get_sent_mails,
) -> None:
    """A lønorg unit that still relates to an administration unit sends no email."""
    loen_root = await create_org_unit(name="Lønorganisation", uuid=root_loen_org)
    loen_unit = await create_org_unit(name="Løn-enhed", parent=loen_root)
    adm_org = await create_org_unit(name="Administration")
    adm_unit = await create_org_unit(name="Adm-enhed", parent=adm_org)
    relation = await create_related_units(origin=loen_unit, destination=[adm_unit])

    with capture_logs() as cap_logs:
        await trigger_event("related_unit", relation)

    assert "Org unit has a relation outside of the Lønorganisation" in str(cap_logs)
    assert await get_sent_mails() == []
