from uuid import UUID

from .base_model import BaseModel


class TestingCreateITSystem(BaseModel):
    itsystem_create: "TestingCreateITSystemItsystemCreate"


class TestingCreateITSystemItsystemCreate(BaseModel):
    uuid: UUID


TestingCreateITSystem.update_forward_refs()
TestingCreateITSystemItsystemCreate.update_forward_refs()
