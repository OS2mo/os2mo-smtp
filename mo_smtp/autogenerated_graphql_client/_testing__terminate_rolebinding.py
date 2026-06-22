from uuid import UUID

from .base_model import BaseModel


class TestingTerminateRolebinding(BaseModel):
    rolebinding_terminate: "TestingTerminateRolebindingRolebindingTerminate"


class TestingTerminateRolebindingRolebindingTerminate(BaseModel):
    uuid: UUID


TestingTerminateRolebinding.update_forward_refs()
TestingTerminateRolebindingRolebindingTerminate.update_forward_refs()
