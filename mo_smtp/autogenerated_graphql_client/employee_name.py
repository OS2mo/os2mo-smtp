# Generated by ariadne-codegen on 2025-02-28 13:18
# Source: queries.graphql


from .base_model import BaseModel


class EmployeeName(BaseModel):
    employees: "EmployeeNameEmployees"


class EmployeeNameEmployees(BaseModel):
    objects: list["EmployeeNameEmployeesObjects"]


class EmployeeNameEmployeesObjects(BaseModel):
    validities: list["EmployeeNameEmployeesObjectsValidities"]


class EmployeeNameEmployeesObjectsValidities(BaseModel):
    name: str


EmployeeName.update_forward_refs()
EmployeeNameEmployees.update_forward_refs()
EmployeeNameEmployeesObjects.update_forward_refs()
EmployeeNameEmployeesObjectsValidities.update_forward_refs()
