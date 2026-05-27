from uuid import UUID

from .base_model import BaseModel


class TestingCreateOrgRoot(BaseModel):
    org_create: "TestingCreateOrgRootOrgCreate"


class TestingCreateOrgRootOrgCreate(BaseModel):
    uuid: UUID


TestingCreateOrgRoot.update_forward_refs()
TestingCreateOrgRootOrgCreate.update_forward_refs()
