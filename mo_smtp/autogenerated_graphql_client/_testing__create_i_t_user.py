from uuid import UUID

from .base_model import BaseModel


class TestingCreateITUser(BaseModel):
    ituser_create: "TestingCreateITUserItuserCreate"


class TestingCreateITUserItuserCreate(BaseModel):
    uuid: UUID


TestingCreateITUser.update_forward_refs()
TestingCreateITUserItuserCreate.update_forward_refs()
