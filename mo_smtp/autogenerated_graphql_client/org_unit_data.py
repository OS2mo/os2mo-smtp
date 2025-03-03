# Generated by ariadne-codegen on 2025-03-03 14:01
# Source: queries.graphql

from uuid import UUID

from .base_model import BaseModel


class OrgUnitData(BaseModel):
    org_units: "OrgUnitDataOrgUnits"


class OrgUnitDataOrgUnits(BaseModel):
    objects: list["OrgUnitDataOrgUnitsObjects"]


class OrgUnitDataOrgUnitsObjects(BaseModel):
    validities: list["OrgUnitDataOrgUnitsObjectsValidities"]


class OrgUnitDataOrgUnitsObjectsValidities(BaseModel):
    name: str
    user_key: str
    root: list["OrgUnitDataOrgUnitsObjectsValiditiesRoot"] | None


class OrgUnitDataOrgUnitsObjectsValiditiesRoot(BaseModel):
    uuid: UUID


OrgUnitData.update_forward_refs()
OrgUnitDataOrgUnits.update_forward_refs()
OrgUnitDataOrgUnitsObjects.update_forward_refs()
OrgUnitDataOrgUnitsObjectsValidities.update_forward_refs()
OrgUnitDataOrgUnitsObjectsValiditiesRoot.update_forward_refs()
