from typing import Optional

from .base_model import BaseModel


class InstitutionAddress(BaseModel):
    org_units: "InstitutionAddressOrgUnits"


class InstitutionAddressOrgUnits(BaseModel):
    objects: list["InstitutionAddressOrgUnitsObjects"]


class InstitutionAddressOrgUnitsObjects(BaseModel):
    current: Optional["InstitutionAddressOrgUnitsObjectsCurrent"]


class InstitutionAddressOrgUnitsObjectsCurrent(BaseModel):
    addresses: list["InstitutionAddressOrgUnitsObjectsCurrentAddresses"]


class InstitutionAddressOrgUnitsObjectsCurrentAddresses(BaseModel):
    value: str


InstitutionAddress.update_forward_refs()
InstitutionAddressOrgUnits.update_forward_refs()
InstitutionAddressOrgUnitsObjects.update_forward_refs()
InstitutionAddressOrgUnitsObjectsCurrent.update_forward_refs()
InstitutionAddressOrgUnitsObjectsCurrentAddresses.update_forward_refs()
