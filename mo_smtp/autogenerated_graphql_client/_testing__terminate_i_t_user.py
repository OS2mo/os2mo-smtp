from uuid import UUID

from .base_model import BaseModel


class TestingTerminateITUser(BaseModel):
    ituser_terminate: "TestingTerminateITUserItuserTerminate"


class TestingTerminateITUserItuserTerminate(BaseModel):
    uuid: UUID


TestingTerminateITUser.update_forward_refs()
TestingTerminateITUserItuserTerminate.update_forward_refs()
