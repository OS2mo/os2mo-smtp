from typing import Optional

from .base_model import BaseModel


class OrgUnitAncestors(BaseModel):
    org_units: "OrgUnitAncestorsOrgUnits"


class OrgUnitAncestorsOrgUnits(BaseModel):
    objects: list["OrgUnitAncestorsOrgUnitsObjects"]


class OrgUnitAncestorsOrgUnitsObjects(BaseModel):
    current: Optional["OrgUnitAncestorsOrgUnitsObjectsCurrent"]


class OrgUnitAncestorsOrgUnitsObjectsCurrent(BaseModel):
    ancestors: list["OrgUnitAncestorsOrgUnitsObjectsCurrentAncestors"]
    name: str


class OrgUnitAncestorsOrgUnitsObjectsCurrentAncestors(BaseModel):
    name: str


OrgUnitAncestors.update_forward_refs()
OrgUnitAncestorsOrgUnits.update_forward_refs()
OrgUnitAncestorsOrgUnitsObjects.update_forward_refs()
OrgUnitAncestorsOrgUnitsObjectsCurrent.update_forward_refs()
OrgUnitAncestorsOrgUnitsObjectsCurrentAncestors.update_forward_refs()
