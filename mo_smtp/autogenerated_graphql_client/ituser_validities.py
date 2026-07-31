from datetime import datetime
from uuid import UUID

from pydantic import Field

from .base_model import BaseModel


class ItuserValidities(BaseModel):
    itusers: "ItuserValiditiesItusers"


class ItuserValiditiesItusers(BaseModel):
    objects: list["ItuserValiditiesItusersObjects"]


class ItuserValiditiesItusersObjects(BaseModel):
    validities: list["ItuserValiditiesItusersObjectsValidities"]


class ItuserValiditiesItusersObjectsValidities(BaseModel):
    user_key: str
    rolebindings: list["ItuserValiditiesItusersObjectsValiditiesRolebindings"]
    person: list["ItuserValiditiesItusersObjectsValiditiesPerson"] | None
    itsystem_response: "ItuserValiditiesItusersObjectsValiditiesItsystemResponse"
    validity: "ItuserValiditiesItusersObjectsValiditiesValidity"


class ItuserValiditiesItusersObjectsValiditiesRolebindings(BaseModel):
    role: list["ItuserValiditiesItusersObjectsValiditiesRolebindingsRole"]


class ItuserValiditiesItusersObjectsValiditiesRolebindingsRole(BaseModel):
    name: str
    uuid: UUID


class ItuserValiditiesItusersObjectsValiditiesPerson(BaseModel):
    name: str
    uuid: UUID


class ItuserValiditiesItusersObjectsValiditiesItsystemResponse(BaseModel):
    uuid: UUID
    validities: list[
        "ItuserValiditiesItusersObjectsValiditiesItsystemResponseValidities"
    ]


class ItuserValiditiesItusersObjectsValiditiesItsystemResponseValidities(BaseModel):
    name: str
    validity: (
        "ItuserValiditiesItusersObjectsValiditiesItsystemResponseValiditiesValidity"
    )


class ItuserValiditiesItusersObjectsValiditiesItsystemResponseValiditiesValidity(
    BaseModel
):
    from_: datetime | None = Field(alias="from")
    to: datetime | None


class ItuserValiditiesItusersObjectsValiditiesValidity(BaseModel):
    from_: datetime = Field(alias="from")
    to: datetime | None


ItuserValidities.update_forward_refs()
ItuserValiditiesItusers.update_forward_refs()
ItuserValiditiesItusersObjects.update_forward_refs()
ItuserValiditiesItusersObjectsValidities.update_forward_refs()
ItuserValiditiesItusersObjectsValiditiesRolebindings.update_forward_refs()
ItuserValiditiesItusersObjectsValiditiesRolebindingsRole.update_forward_refs()
ItuserValiditiesItusersObjectsValiditiesPerson.update_forward_refs()
ItuserValiditiesItusersObjectsValiditiesItsystemResponse.update_forward_refs()
ItuserValiditiesItusersObjectsValiditiesItsystemResponseValidities.update_forward_refs()
ItuserValiditiesItusersObjectsValiditiesItsystemResponseValiditiesValidity.update_forward_refs()
ItuserValiditiesItusersObjectsValiditiesValidity.update_forward_refs()
