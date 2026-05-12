from datetime import datetime
from uuid import UUID

from pydantic import Field

from .base_model import BaseModel


class Rolebinding(BaseModel):
    rolebindings: "RolebindingRolebindings"


class RolebindingRolebindings(BaseModel):
    objects: list["RolebindingRolebindingsObjects"]


class RolebindingRolebindingsObjects(BaseModel):
    validities: list["RolebindingRolebindingsObjectsValidities"]


class RolebindingRolebindingsObjectsValidities(BaseModel):
    ituser: list["RolebindingRolebindingsObjectsValiditiesItuser"]
    validity: "RolebindingRolebindingsObjectsValiditiesValidity"


class RolebindingRolebindingsObjectsValiditiesItuser(BaseModel):
    uuid: UUID


class RolebindingRolebindingsObjectsValiditiesValidity(BaseModel):
    from_: datetime = Field(alias="from")
    to: datetime | None


Rolebinding.update_forward_refs()
RolebindingRolebindings.update_forward_refs()
RolebindingRolebindingsObjects.update_forward_refs()
RolebindingRolebindingsObjectsValidities.update_forward_refs()
RolebindingRolebindingsObjectsValiditiesItuser.update_forward_refs()
RolebindingRolebindingsObjectsValiditiesValidity.update_forward_refs()
