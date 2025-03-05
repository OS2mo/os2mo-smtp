# Generated by ariadne-codegen on 2025-03-05 13:32
# Source: queries.graphql

from datetime import datetime
from uuid import UUID

from pydantic import Field

from .base_model import BaseModel


class GetManagerData(BaseModel):
    managers: "GetManagerDataManagers"


class GetManagerDataManagers(BaseModel):
    objects: list["GetManagerDataManagersObjects"]


class GetManagerDataManagersObjects(BaseModel):
    validities: list["GetManagerDataManagersObjectsValidities"]


class GetManagerDataManagersObjectsValidities(BaseModel):
    employee_uuid: UUID | None
    org_unit_uuid: UUID
    validity: "GetManagerDataManagersObjectsValiditiesValidity"


class GetManagerDataManagersObjectsValiditiesValidity(BaseModel):
    to: datetime | None
    from_: datetime = Field(alias="from")


GetManagerData.update_forward_refs()
GetManagerDataManagers.update_forward_refs()
GetManagerDataManagersObjects.update_forward_refs()
GetManagerDataManagersObjectsValidities.update_forward_refs()
GetManagerDataManagersObjectsValiditiesValidity.update_forward_refs()
