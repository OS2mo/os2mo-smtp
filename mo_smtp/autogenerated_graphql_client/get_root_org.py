# Generated by ariadne-codegen on 2025-02-24 10:19
# Source: queries.graphql

from uuid import UUID

from .base_model import BaseModel


class GetRootOrg(BaseModel):
    org: "GetRootOrgOrg"


class GetRootOrgOrg(BaseModel):
    uuid: UUID


GetRootOrg.update_forward_refs()
GetRootOrgOrg.update_forward_refs()
