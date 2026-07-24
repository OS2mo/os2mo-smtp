from datetime import datetime

from pydantic import Field

from .base_model import BaseModel


class OrgUnitValidities(BaseModel):
    org_units: "OrgUnitValiditiesOrgUnits"


class OrgUnitValiditiesOrgUnits(BaseModel):
    objects: list["OrgUnitValiditiesOrgUnitsObjects"]


class OrgUnitValiditiesOrgUnitsObjects(BaseModel):
    validities: list["OrgUnitValiditiesOrgUnitsObjectsValidities"]


class OrgUnitValiditiesOrgUnitsObjectsValidities(BaseModel):
    validity: "OrgUnitValiditiesOrgUnitsObjectsValiditiesValidity"


class OrgUnitValiditiesOrgUnitsObjectsValiditiesValidity(BaseModel):
    from_: datetime = Field(alias="from")
    to: datetime | None


OrgUnitValidities.update_forward_refs()
OrgUnitValiditiesOrgUnits.update_forward_refs()
OrgUnitValiditiesOrgUnitsObjects.update_forward_refs()
OrgUnitValiditiesOrgUnitsObjectsValidities.update_forward_refs()
OrgUnitValiditiesOrgUnitsObjectsValiditiesValidity.update_forward_refs()
