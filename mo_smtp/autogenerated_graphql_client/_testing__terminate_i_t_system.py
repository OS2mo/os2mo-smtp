from uuid import UUID

from .base_model import BaseModel


class TestingTerminateITSystem(BaseModel):
    itsystem_terminate: "TestingTerminateITSystemItsystemTerminate"


class TestingTerminateITSystemItsystemTerminate(BaseModel):
    uuid: UUID


TestingTerminateITSystem.update_forward_refs()
TestingTerminateITSystemItsystemTerminate.update_forward_refs()
