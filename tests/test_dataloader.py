# SPDX-FileCopyrightText: 2019-2020 Magenta ApS
#
# SPDX-License-Identifier: MPL-2.0
import datetime
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch
from uuid import uuid4

import pytest
import pytz  # type: ignore

from mo_smtp.autogenerated_graphql_client.get_manager_data import (
    GetManagerDataManagersObjectsValidities,
)
from mo_smtp.autogenerated_graphql_client.institution_address import (
    InstitutionAddressOrgUnits,
)
from mo_smtp.autogenerated_graphql_client.org_unit_relations import (
    OrgUnitRelationsOrgUnits,
    OrgUnitRelationsOrgUnitsObjects,
)
from mo_smtp.dataloaders import DataLoader, get_institution_address
from mo_smtp.dataloaders import get_org_unit_relations
from mo_smtp.dataloaders import mo_datestring_to_utc


@pytest.fixture
async def graphql_session() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
async def dataloader(graphql_session: AsyncMock) -> DataLoader:
    mo = AsyncMock()
    dataloader = DataLoader(mo)
    return dataloader


async def test_load_mo_user_data(dataloader: DataLoader) -> None:
    result = await dataloader.load_mo_user_data(uuid4())
    assert result is not None
    dataloader.mo.get_user_data.assert_awaited_once()


async def test_load_mo_org_unit_data(dataloader: DataLoader) -> None:
    result = await dataloader.load_mo_org_unit_data(uuid4())
    assert result is not None
    dataloader.mo.get_org_unit_data.assert_awaited_once()


async def test_load_mo_address_data(dataloader: DataLoader) -> None:
    result = await dataloader.load_mo_address_data(uuid4())
    assert result is not None
    dataloader.mo.get_address_data.assert_awaited_once()

    emtpy_mock = MagicMock()
    emtpy_mock.objects = []
    dataloader.mo.get_address_data.return_value = emtpy_mock
    result = await dataloader.load_mo_address_data(uuid4())
    assert result is None


async def test_load_mo_manager_data(dataloader: DataLoader):
    result_mock = MagicMock()
    object_mock = MagicMock()

    validities_list = [MagicMock()]

    object_mock.validities = (
        validities_list  # Mock the 'validities' attribute as a list
    )
    result_mock.objects = [object_mock]
    dataloader.mo.get_manager_data.return_value = result_mock

    result = await dataloader.load_mo_manager_data(uuid4())
    assert result is not None
    dataloader.mo.get_manager_data.assert_awaited_once()


async def test_load_mo_root_org_uuid(dataloader: DataLoader):
    root_org_uuid = uuid4()

    root_org_mock = AsyncMock()
    root_org_mock.uuid = root_org_uuid
    dataloader.mo.get_root_org.return_value = root_org_mock

    result = await dataloader.load_mo_root_org_uuid()
    assert result == root_org_uuid


async def test_get_org_unit_location(dataloader: DataLoader):
    root_org_uuid = str(uuid4())
    dataloader.load_mo_root_org_uuid = AsyncMock()  # type: ignore
    dataloader.load_mo_root_org_uuid.return_value = root_org_uuid

    root_org = {"uuid": root_org_uuid}

    org_unit_1 = {
        "parent_uuid": root_org_uuid,
        "name": "org1",
        "uuid": str(uuid4()),
    }
    org_unit_2 = {
        "parent_uuid": org_unit_1["uuid"],
        "name": "org2",
        "uuid": str(uuid4()),
    }

    org_unit_dict = {
        root_org["uuid"]: root_org,
        org_unit_1["uuid"]: org_unit_1,
        org_unit_2["uuid"]: org_unit_2,
    }

    async def load_org_unit_data(uuid):
        return org_unit_dict[uuid]

    dataloader.load_mo_org_unit_data = AsyncMock()  # type: ignore
    dataloader.load_mo_org_unit_data.side_effect = load_org_unit_data

    assert await dataloader.get_org_unit_location(org_unit_1) == "org1"
    assert await dataloader.get_org_unit_location(org_unit_2) == "org1 / org2"


async def test_get_org_unit_relations():
    root_org = uuid4()
    org_unit_uuid = uuid4()
    test_data = [
        OrgUnitRelationsOrgUnitsObjects.parse_obj(
            {
                "current": {
                    "name": "org-unit-name",
                    "root": [{"uuid": root_org}],
                    "engagements": [
                        {"uuid": uuid4()},
                    ],
                    "related_units": [
                        {
                            "org_units": [
                                {
                                    "uuid": uuid4(),
                                    "root": [{"uuid": root_org}],
                                }
                            ]
                        }
                    ],
                }
            }
        )
    ]

    mocked_mo_client = AsyncMock()
    # mock org_unit_relations, which returns `data.org_units`
    mocked_mo_client.org_unit_relations.return_value = (
        OrgUnitRelationsOrgUnits.parse_obj({"objects": test_data})
    )

    # test that `get_org_unit_relations` returns the response from `org_unit_relations`.objects (which is what the test_data is)
    org_unit_relations_response = await get_org_unit_relations(
        mo=mocked_mo_client, org_unit_uuid=[org_unit_uuid]
    )

    assert org_unit_relations_response == test_data
    mocked_mo_client.org_unit_relations.assert_awaited_once_with([org_unit_uuid])


async def test_get_institution_address():
    root_org = uuid4()
    org_unit_uuid = uuid4()
    test_data = InstitutionAddressOrgUnits.parse_obj(
        {"objects": [{"current": {"addresses": [{"value": "test@test.dk"}]}}]}
    )

    mocked_mo_client = AsyncMock()

    mocked_mo_client.institution_address.return_value = test_data

    institution_address_response = await get_institution_address(
        mo=mocked_mo_client, root=[root_org], uuids=[org_unit_uuid]
    )
    # expect a set of the email(s) in response
    expected_response = set(["test@test.dk"])

    assert institution_address_response == expected_response
    mocked_mo_client.institution_address.assert_awaited_once_with(
        [org_unit_uuid], [root_org]
    )


def test_extract_latest_object(dataloader: DataLoader):
    uuid_obj1 = uuid4()
    uuid_obj2 = uuid4()
    uuid_obj3 = uuid4()

    datetime_mock = MagicMock(datetime)
    datetime_mock.datetime.utcnow.return_value = datetime.datetime(2022, 8, 10)
    datetime_mock.datetime.fromisoformat = datetime.datetime.fromisoformat

    with patch(
        "mo_smtp.dataloaders.datetime",
        datetime_mock,
    ):
        # One of the objects is valid today - return it
        obj1: GetManagerDataManagersObjectsValidities = MagicMock()
        obj1.validity.from_ = datetime.datetime(2022, 8, 1)
        obj1.validity.to = datetime.datetime(2022, 8, 1)
        obj1.employee_uuid = uuid_obj1

        obj2: GetManagerDataManagersObjectsValidities = MagicMock()
        obj2.validity.from_ = datetime.datetime(2022, 8, 2)
        obj2.validity.to = datetime.datetime(2022, 8, 15)
        obj2.employee_uuid = uuid_obj2

        obj3: GetManagerDataManagersObjectsValidities = MagicMock()
        obj3.validity.from_ = datetime.datetime(2022, 8, 15)
        obj3.validity.to = None
        obj3.employee_uuid = uuid_obj3

        objects = [obj1, obj2, obj3]

        assert (
            dataloader.extract_current_or_latest_object(objects).employee_uuid
            == uuid_obj2
        )

        # One of the objects is valid today (without to-date) - return it
        obj1 = MagicMock()
        obj1.validity.from_ = datetime.datetime(2022, 8, 1)
        obj1.validity.to = datetime.datetime(2022, 8, 2)
        obj1.employee_uuid = uuid_obj1

        obj2 = MagicMock()
        obj2.validity.from_ = datetime.datetime(2022, 8, 2)
        obj2.validity.to = None
        obj2.employee_uuid = uuid_obj2

        objects = [obj1, obj2]
        assert (
            dataloader.extract_current_or_latest_object(objects).employee_uuid
            == uuid_obj2
        )

        # One of the objects is valid today (without from-date)- return it
        obj1 = MagicMock()
        obj1.validity.from_ = None
        obj1.validity.to = datetime.datetime(2022, 8, 15)
        obj1.employee_uuid = uuid_obj2

        obj2 = MagicMock()
        obj2.validity.from_ = datetime.datetime(2022, 8, 15)
        obj2.validity.to = None
        obj2.employee_uuid = uuid_obj3

        objects = [obj1, obj2]
        assert (
            dataloader.extract_current_or_latest_object(objects).employee_uuid
            == uuid_obj2
        )

        # No object is valid today - return the latest
        obj1 = MagicMock()
        obj1.validity.from_ = datetime.datetime(2022, 8, 1)
        obj1.validity.to = datetime.datetime(2022, 8, 2)
        obj1.employee_uuid = uuid_obj1

        obj2 = MagicMock()
        obj2.validity.from_ = datetime.datetime(2022, 8, 15)
        obj2.validity.to = None
        obj2.employee_uuid = uuid_obj3

        objects = [obj1, obj2]
        assert (
            dataloader.extract_current_or_latest_object(objects).employee_uuid
            == uuid_obj3
        )

        # No object is valid today - return the latest
        obj1 = MagicMock()
        obj1.validity.from_ = datetime.datetime(2022, 8, 1)
        obj1.validity.to = datetime.datetime(2022, 8, 2)
        obj1.employee_uuid = uuid_obj1

        obj2 = MagicMock()
        obj2.validity.from_ = datetime.datetime(2022, 8, 15)
        obj2.validity.to = datetime.datetime(2022, 8, 20)
        obj2.employee_uuid = uuid_obj2

        objects = [obj1, obj2]
        assert (
            dataloader.extract_current_or_latest_object(objects).employee_uuid
            == uuid_obj2
        )

        with pytest.raises(Exception):
            objects = []
            dataloader.extract_current_or_latest_object(objects)


def test_mo_datestring_to_utc():
    datetime_obj = datetime.datetime(
        2022, 8, 15, tzinfo=pytz.timezone("Europe/Copenhagen")
    )

    assert mo_datestring_to_utc(datetime_obj) == datetime.datetime(2022, 8, 15)
    assert mo_datestring_to_utc(None) is None
