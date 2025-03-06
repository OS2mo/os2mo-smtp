# Generated by ariadne-codegen on 2025-03-06 12:48

from .address_data import (
    AddressData,
    AddressDataAddresses,
    AddressDataAddressesObjects,
    AddressDataAddressesObjectsCurrent,
    AddressDataAddressesObjectsCurrentAddressType,
)
from .async_base_client import AsyncBaseClient
from .base_model import BaseModel
from .client import GraphQLClient
from .employee_data import (
    EmployeeData,
    EmployeeDataEmployees,
    EmployeeDataEmployeesObjects,
    EmployeeDataEmployeesObjectsCurrent,
    EmployeeDataEmployeesObjectsCurrentAddresses,
    EmployeeDataEmployeesObjectsCurrentEngagements,
    EmployeeDataEmployeesObjectsCurrentEngagementsManagers,
    EmployeeDataEmployeesObjectsCurrentEngagementsManagersPerson,
    EmployeeDataEmployeesObjectsCurrentEngagementsManagersPersonAddresses,
    EmployeeDataEmployeesObjectsCurrentEngagementsOrgUnit,
)
from .employee_name import (
    EmployeeName,
    EmployeeNameEmployees,
    EmployeeNameEmployeesObjects,
    EmployeeNameEmployeesObjectsCurrent,
)
from .enums import AuditLogModel, FileStore, OwnerInferencePriority
from .exceptions import (
    GraphQLClientError,
    GraphQLClientGraphQLError,
    GraphQLClientGraphQLMultiError,
    GraphQLClientHttpError,
    GraphQlClientInvalidResponseError,
)
from .input_types import (
    AddressCreateInput,
    AddressFilter,
    AddressRegistrationFilter,
    AddressTerminateInput,
    AddressUpdateInput,
    AssociationCreateInput,
    AssociationFilter,
    AssociationRegistrationFilter,
    AssociationTerminateInput,
    AssociationUpdateInput,
    AuditLogFilter,
    ClassCreateInput,
    ClassFilter,
    ClassOwnerFilter,
    ClassRegistrationFilter,
    ClassTerminateInput,
    ClassUpdateInput,
    ConfigurationFilter,
    DescendantParentBoundOrganisationUnitFilter,
    EmployeeCreateInput,
    EmployeeFilter,
    EmployeeRegistrationFilter,
    EmployeesBoundAddressFilter,
    EmployeesBoundAssociationFilter,
    EmployeesBoundEngagementFilter,
    EmployeesBoundITUserFilter,
    EmployeesBoundLeaveFilter,
    EmployeesBoundManagerFilter,
    EmployeeTerminateInput,
    EmployeeUpdateInput,
    EngagementCreateInput,
    EngagementFilter,
    EngagementRegistrationFilter,
    EngagementTerminateInput,
    EngagementUpdateInput,
    FacetCreateInput,
    FacetFilter,
    FacetRegistrationFilter,
    FacetsBoundClassFilter,
    FacetTerminateInput,
    FacetUpdateInput,
    FileFilter,
    HealthFilter,
    ITAssociationCreateInput,
    ITAssociationTerminateInput,
    ITAssociationUpdateInput,
    ITSystemCreateInput,
    ITSystemFilter,
    ITSystemRegistrationFilter,
    ITSystemTerminateInput,
    ITSystemUpdateInput,
    ItuserBoundAddressFilter,
    ItuserBoundRoleBindingFilter,
    ITUserCreateInput,
    ITUserFilter,
    ITUserRegistrationFilter,
    ITUserTerminateInput,
    ITUserUpdateInput,
    KLECreateInput,
    KLEFilter,
    KLERegistrationFilter,
    KLETerminateInput,
    KLEUpdateInput,
    LeaveCreateInput,
    LeaveFilter,
    LeaveRegistrationFilter,
    LeaveTerminateInput,
    LeaveUpdateInput,
    ManagerCreateInput,
    ManagerFilter,
    ManagerRegistrationFilter,
    ManagerTerminateInput,
    ManagerUpdateInput,
    ModelsUuidsBoundRegistrationFilter,
    OrganisationCreate,
    OrganisationUnitCreateInput,
    OrganisationUnitFilter,
    OrganisationUnitRegistrationFilter,
    OrganisationUnitTerminateInput,
    OrganisationUnitUpdateInput,
    OrgUnitsboundaddressfilter,
    OrgUnitsboundassociationfilter,
    OrgUnitsboundengagementfilter,
    OrgUnitsboundituserfilter,
    OrgUnitsboundklefilter,
    OrgUnitsboundleavefilter,
    OrgUnitsboundmanagerfilter,
    OrgUnitsboundrelatedunitfilter,
    OwnerCreateInput,
    OwnerFilter,
    OwnerTerminateInput,
    OwnerUpdateInput,
    ParentsBoundClassFilter,
    ParentsBoundFacetFilter,
    ParentsBoundOrganisationUnitFilter,
    RAOpenValidityInput,
    RAValidityInput,
    RegistrationFilter,
    RelatedUnitFilter,
    RelatedUnitRegistrationFilter,
    RelatedUnitsUpdateInput,
    RoleBindingCreateInput,
    RoleBindingFilter,
    RoleBindingTerminateInput,
    RoleBindingUpdateInput,
    RoleRegistrationFilter,
    UuidsBoundClassFilter,
    UuidsBoundEmployeeFilter,
    UuidsBoundEngagementFilter,
    UuidsBoundFacetFilter,
    UuidsBoundITSystemFilter,
    UuidsBoundITUserFilter,
    UuidsBoundLeaveFilter,
    UuidsBoundOrganisationUnitFilter,
    ValidityInput,
)
from .institution_address import (
    InstitutionAddress,
    InstitutionAddressOrgUnits,
    InstitutionAddressOrgUnitsObjects,
    InstitutionAddressOrgUnitsObjectsCurrent,
    InstitutionAddressOrgUnitsObjectsCurrentAddresses,
)
from .manager_data import (
    ManagerData,
    ManagerDataManagers,
    ManagerDataManagersObjects,
    ManagerDataManagersObjectsValidities,
    ManagerDataManagersObjectsValiditiesValidity,
)
from .org_unit_data import (
    OrgUnitData,
    OrgUnitDataOrgUnits,
    OrgUnitDataOrgUnitsObjects,
    OrgUnitDataOrgUnitsObjectsCurrent,
    OrgUnitDataOrgUnitsObjectsCurrentRoot,
)
from .org_unit_descendants import (
    OrgUnitDescendants,
    OrgUnitDescendantsOrgUnits,
    OrgUnitDescendantsOrgUnitsObjects,
    OrgUnitDescendantsOrgUnitsObjectsCurrent,
)
from .org_unit_relations import (
    OrgUnitRelations,
    OrgUnitRelationsOrgUnits,
    OrgUnitRelationsOrgUnitsObjects,
    OrgUnitRelationsOrgUnitsObjectsCurrent,
    OrgUnitRelationsOrgUnitsObjectsCurrentEngagements,
    OrgUnitRelationsOrgUnitsObjectsCurrentRelatedUnits,
    OrgUnitRelationsOrgUnitsObjectsCurrentRelatedUnitsOrgUnits,
    OrgUnitRelationsOrgUnitsObjectsCurrentRelatedUnitsOrgUnitsRoot,
    OrgUnitRelationsOrgUnitsObjectsCurrentRoot,
)

__all__ = [
    "AddressCreateInput",
    "AddressData",
    "AddressDataAddresses",
    "AddressDataAddressesObjects",
    "AddressDataAddressesObjectsCurrent",
    "AddressDataAddressesObjectsCurrentAddressType",
    "AddressFilter",
    "AddressRegistrationFilter",
    "AddressTerminateInput",
    "AddressUpdateInput",
    "AssociationCreateInput",
    "AssociationFilter",
    "AssociationRegistrationFilter",
    "AssociationTerminateInput",
    "AssociationUpdateInput",
    "AsyncBaseClient",
    "AuditLogFilter",
    "AuditLogModel",
    "BaseModel",
    "ClassCreateInput",
    "ClassFilter",
    "ClassOwnerFilter",
    "ClassRegistrationFilter",
    "ClassTerminateInput",
    "ClassUpdateInput",
    "ConfigurationFilter",
    "DescendantParentBoundOrganisationUnitFilter",
    "EmployeeCreateInput",
    "EmployeeData",
    "EmployeeDataEmployees",
    "EmployeeDataEmployeesObjects",
    "EmployeeDataEmployeesObjectsCurrent",
    "EmployeeDataEmployeesObjectsCurrentAddresses",
    "EmployeeDataEmployeesObjectsCurrentEngagements",
    "EmployeeDataEmployeesObjectsCurrentEngagementsManagers",
    "EmployeeDataEmployeesObjectsCurrentEngagementsManagersPerson",
    "EmployeeDataEmployeesObjectsCurrentEngagementsManagersPersonAddresses",
    "EmployeeDataEmployeesObjectsCurrentEngagementsOrgUnit",
    "EmployeeFilter",
    "EmployeeName",
    "EmployeeNameEmployees",
    "EmployeeNameEmployeesObjects",
    "EmployeeNameEmployeesObjectsCurrent",
    "EmployeeRegistrationFilter",
    "EmployeeTerminateInput",
    "EmployeeUpdateInput",
    "EmployeesBoundAddressFilter",
    "EmployeesBoundAssociationFilter",
    "EmployeesBoundEngagementFilter",
    "EmployeesBoundITUserFilter",
    "EmployeesBoundLeaveFilter",
    "EmployeesBoundManagerFilter",
    "EngagementCreateInput",
    "EngagementFilter",
    "EngagementRegistrationFilter",
    "EngagementTerminateInput",
    "EngagementUpdateInput",
    "FacetCreateInput",
    "FacetFilter",
    "FacetRegistrationFilter",
    "FacetTerminateInput",
    "FacetUpdateInput",
    "FacetsBoundClassFilter",
    "FileFilter",
    "FileStore",
    "GraphQLClient",
    "GraphQLClientError",
    "GraphQLClientGraphQLError",
    "GraphQLClientGraphQLMultiError",
    "GraphQLClientHttpError",
    "GraphQlClientInvalidResponseError",
    "HealthFilter",
    "ITAssociationCreateInput",
    "ITAssociationTerminateInput",
    "ITAssociationUpdateInput",
    "ITSystemCreateInput",
    "ITSystemFilter",
    "ITSystemRegistrationFilter",
    "ITSystemTerminateInput",
    "ITSystemUpdateInput",
    "ITUserCreateInput",
    "ITUserFilter",
    "ITUserRegistrationFilter",
    "ITUserTerminateInput",
    "ITUserUpdateInput",
    "InstitutionAddress",
    "InstitutionAddressOrgUnits",
    "InstitutionAddressOrgUnitsObjects",
    "InstitutionAddressOrgUnitsObjectsCurrent",
    "InstitutionAddressOrgUnitsObjectsCurrentAddresses",
    "ItuserBoundAddressFilter",
    "ItuserBoundRoleBindingFilter",
    "KLECreateInput",
    "KLEFilter",
    "KLERegistrationFilter",
    "KLETerminateInput",
    "KLEUpdateInput",
    "LeaveCreateInput",
    "LeaveFilter",
    "LeaveRegistrationFilter",
    "LeaveTerminateInput",
    "LeaveUpdateInput",
    "ManagerCreateInput",
    "ManagerData",
    "ManagerDataManagers",
    "ManagerDataManagersObjects",
    "ManagerDataManagersObjectsValidities",
    "ManagerDataManagersObjectsValiditiesValidity",
    "ManagerFilter",
    "ManagerRegistrationFilter",
    "ManagerTerminateInput",
    "ManagerUpdateInput",
    "ModelsUuidsBoundRegistrationFilter",
    "OrgUnitData",
    "OrgUnitDataOrgUnits",
    "OrgUnitDataOrgUnitsObjects",
    "OrgUnitDataOrgUnitsObjectsCurrent",
    "OrgUnitDataOrgUnitsObjectsCurrentRoot",
    "OrgUnitDescendants",
    "OrgUnitDescendantsOrgUnits",
    "OrgUnitDescendantsOrgUnitsObjects",
    "OrgUnitDescendantsOrgUnitsObjectsCurrent",
    "OrgUnitRelations",
    "OrgUnitRelationsOrgUnits",
    "OrgUnitRelationsOrgUnitsObjects",
    "OrgUnitRelationsOrgUnitsObjectsCurrent",
    "OrgUnitRelationsOrgUnitsObjectsCurrentEngagements",
    "OrgUnitRelationsOrgUnitsObjectsCurrentRelatedUnits",
    "OrgUnitRelationsOrgUnitsObjectsCurrentRelatedUnitsOrgUnits",
    "OrgUnitRelationsOrgUnitsObjectsCurrentRelatedUnitsOrgUnitsRoot",
    "OrgUnitRelationsOrgUnitsObjectsCurrentRoot",
    "OrgUnitsboundaddressfilter",
    "OrgUnitsboundassociationfilter",
    "OrgUnitsboundengagementfilter",
    "OrgUnitsboundituserfilter",
    "OrgUnitsboundklefilter",
    "OrgUnitsboundleavefilter",
    "OrgUnitsboundmanagerfilter",
    "OrgUnitsboundrelatedunitfilter",
    "OrganisationCreate",
    "OrganisationUnitCreateInput",
    "OrganisationUnitFilter",
    "OrganisationUnitRegistrationFilter",
    "OrganisationUnitTerminateInput",
    "OrganisationUnitUpdateInput",
    "OwnerCreateInput",
    "OwnerFilter",
    "OwnerInferencePriority",
    "OwnerTerminateInput",
    "OwnerUpdateInput",
    "ParentsBoundClassFilter",
    "ParentsBoundFacetFilter",
    "ParentsBoundOrganisationUnitFilter",
    "RAOpenValidityInput",
    "RAValidityInput",
    "RegistrationFilter",
    "RelatedUnitFilter",
    "RelatedUnitRegistrationFilter",
    "RelatedUnitsUpdateInput",
    "RoleBindingCreateInput",
    "RoleBindingFilter",
    "RoleBindingTerminateInput",
    "RoleBindingUpdateInput",
    "RoleRegistrationFilter",
    "UuidsBoundClassFilter",
    "UuidsBoundEmployeeFilter",
    "UuidsBoundEngagementFilter",
    "UuidsBoundFacetFilter",
    "UuidsBoundITSystemFilter",
    "UuidsBoundITUserFilter",
    "UuidsBoundLeaveFilter",
    "UuidsBoundOrganisationUnitFilter",
    "ValidityInput",
]
