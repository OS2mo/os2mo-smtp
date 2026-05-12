from uuid import UUID

from .base_model import BaseModel


class TestingCreateOrgUnitItUser(BaseModel):
    ituser_create: "TestingCreateOrgUnitItUserItuserCreate"


class TestingCreateOrgUnitItUserItuserCreate(BaseModel):
    uuid: UUID


TestingCreateOrgUnitItUser.update_forward_refs()
TestingCreateOrgUnitItUserItuserCreate.update_forward_refs()
