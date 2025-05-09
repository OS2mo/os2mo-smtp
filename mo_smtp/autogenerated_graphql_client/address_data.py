from typing import Optional
from uuid import UUID

from .base_model import BaseModel


class AddressData(BaseModel):
    addresses: "AddressDataAddresses"


class AddressDataAddresses(BaseModel):
    objects: list["AddressDataAddressesObjects"]


class AddressDataAddressesObjects(BaseModel):
    current: Optional["AddressDataAddressesObjectsCurrent"]


class AddressDataAddressesObjectsCurrent(BaseModel):
    value: str
    employee_uuid: UUID | None
    address_type: "AddressDataAddressesObjectsCurrentAddressType"


class AddressDataAddressesObjectsCurrentAddressType(BaseModel):
    scope: str | None


AddressData.update_forward_refs()
AddressDataAddresses.update_forward_refs()
AddressDataAddressesObjects.update_forward_refs()
AddressDataAddressesObjectsCurrent.update_forward_refs()
AddressDataAddressesObjectsCurrentAddressType.update_forward_refs()
