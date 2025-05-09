from datetime import datetime
from uuid import UUID

from pydantic import Field

from .base_model import BaseModel


class ManagerData(BaseModel):
    managers: "ManagerDataManagers"


class ManagerDataManagers(BaseModel):
    objects: list["ManagerDataManagersObjects"]


class ManagerDataManagersObjects(BaseModel):
    validities: list["ManagerDataManagersObjectsValidities"]


class ManagerDataManagersObjectsValidities(BaseModel):
    employee_uuid: UUID | None
    org_unit_uuid: UUID
    validity: "ManagerDataManagersObjectsValiditiesValidity"


class ManagerDataManagersObjectsValiditiesValidity(BaseModel):
    to: datetime | None
    from_: datetime = Field(alias="from")


ManagerData.update_forward_refs()
ManagerDataManagers.update_forward_refs()
ManagerDataManagersObjects.update_forward_refs()
ManagerDataManagersObjectsValidities.update_forward_refs()
ManagerDataManagersObjectsValiditiesValidity.update_forward_refs()
