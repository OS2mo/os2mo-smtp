from uuid import UUID

from .base_model import BaseModel


class TestingUpdateITSystem(BaseModel):
    itsystem_update: "TestingUpdateITSystemItsystemUpdate"


class TestingUpdateITSystemItsystemUpdate(BaseModel):
    uuid: UUID


TestingUpdateITSystem.update_forward_refs()
TestingUpdateITSystemItsystemUpdate.update_forward_refs()
