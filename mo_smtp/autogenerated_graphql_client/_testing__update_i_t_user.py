from uuid import UUID

from .base_model import BaseModel


class TestingUpdateITUser(BaseModel):
    ituser_update: "TestingUpdateITUserItuserUpdate"


class TestingUpdateITUserItuserUpdate(BaseModel):
    uuid: UUID


TestingUpdateITUser.update_forward_refs()
TestingUpdateITUserItuserUpdate.update_forward_refs()
