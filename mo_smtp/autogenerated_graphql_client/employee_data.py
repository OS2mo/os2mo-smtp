# Generated by ariadne-codegen on 2025-02-28 13:18
# Source: queries.graphql


from .base_model import BaseModel


class EmployeeData(BaseModel):
    employees: "EmployeeDataEmployees"


class EmployeeDataEmployees(BaseModel):
    objects: list["EmployeeDataEmployeesObjects"]


class EmployeeDataEmployeesObjects(BaseModel):
    validities: list["EmployeeDataEmployeesObjectsValidities"]


class EmployeeDataEmployeesObjectsValidities(BaseModel):
    name: str
    addresses: list["EmployeeDataEmployeesObjectsValiditiesAddresses"]
    engagements: list["EmployeeDataEmployeesObjectsValiditiesEngagements"]


class EmployeeDataEmployeesObjectsValiditiesAddresses(BaseModel):
    value: str


class EmployeeDataEmployeesObjectsValiditiesEngagements(BaseModel):
    org_unit: list["EmployeeDataEmployeesObjectsValiditiesEngagementsOrgUnit"]
    managers: list["EmployeeDataEmployeesObjectsValiditiesEngagementsManagers"]


class EmployeeDataEmployeesObjectsValiditiesEngagementsOrgUnit(BaseModel):
    name: str


class EmployeeDataEmployeesObjectsValiditiesEngagementsManagers(BaseModel):
    person: (
        None | (list["EmployeeDataEmployeesObjectsValiditiesEngagementsManagersPerson"])
    )


class EmployeeDataEmployeesObjectsValiditiesEngagementsManagersPerson(BaseModel):
    addresses: list[
        "EmployeeDataEmployeesObjectsValiditiesEngagementsManagersPersonAddresses"
    ]


class EmployeeDataEmployeesObjectsValiditiesEngagementsManagersPersonAddresses(
    BaseModel
):
    value: str


EmployeeData.update_forward_refs()
EmployeeDataEmployees.update_forward_refs()
EmployeeDataEmployeesObjects.update_forward_refs()
EmployeeDataEmployeesObjectsValidities.update_forward_refs()
EmployeeDataEmployeesObjectsValiditiesAddresses.update_forward_refs()
EmployeeDataEmployeesObjectsValiditiesEngagements.update_forward_refs()
EmployeeDataEmployeesObjectsValiditiesEngagementsOrgUnit.update_forward_refs()
EmployeeDataEmployeesObjectsValiditiesEngagementsManagers.update_forward_refs()
EmployeeDataEmployeesObjectsValiditiesEngagementsManagersPerson.update_forward_refs()
EmployeeDataEmployeesObjectsValiditiesEngagementsManagersPersonAddresses.update_forward_refs()
