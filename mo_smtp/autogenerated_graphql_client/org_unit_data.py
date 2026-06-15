from typing import Optional

from .base_model import BaseModel


class OrgUnitData(BaseModel):
    org_units: "OrgUnitDataOrgUnits"


class OrgUnitDataOrgUnits(BaseModel):
    objects: list["OrgUnitDataOrgUnitsObjects"]


class OrgUnitDataOrgUnitsObjects(BaseModel):
    current: Optional["OrgUnitDataOrgUnitsObjectsCurrent"]


class OrgUnitDataOrgUnitsObjectsCurrent(BaseModel):
    name: str
    user_key: str


OrgUnitData.update_forward_refs()
OrgUnitDataOrgUnits.update_forward_refs()
OrgUnitDataOrgUnitsObjects.update_forward_refs()
OrgUnitDataOrgUnitsObjectsCurrent.update_forward_refs()
