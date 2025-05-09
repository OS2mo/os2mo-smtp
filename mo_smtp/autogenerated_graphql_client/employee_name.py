from typing import Optional

from .base_model import BaseModel


class EmployeeName(BaseModel):
    employees: "EmployeeNameEmployees"


class EmployeeNameEmployees(BaseModel):
    objects: list["EmployeeNameEmployeesObjects"]


class EmployeeNameEmployeesObjects(BaseModel):
    current: Optional["EmployeeNameEmployeesObjectsCurrent"]


class EmployeeNameEmployeesObjectsCurrent(BaseModel):
    name: str


EmployeeName.update_forward_refs()
EmployeeNameEmployees.update_forward_refs()
EmployeeNameEmployeesObjects.update_forward_refs()
EmployeeNameEmployeesObjectsCurrent.update_forward_refs()
