from uuid import UUID

from ._testing__create_address import (
    TestingCreateAddress,
    TestingCreateAddressAddressCreate,
)
from ._testing__create_class import TestingCreateClass, TestingCreateClassClassCreate
from ._testing__create_employee import (
    TestingCreateEmployee,
    TestingCreateEmployeeEmployeeCreate,
)
from ._testing__create_engagement import (
    TestingCreateEngagement,
    TestingCreateEngagementEngagementCreate,
)
from ._testing__create_facet import TestingCreateFacet, TestingCreateFacetFacetCreate
from ._testing__create_manager import (
    TestingCreateManager,
    TestingCreateManagerManagerCreate,
)
from ._testing__create_org_root import (
    TestingCreateOrgRoot,
    TestingCreateOrgRootOrgCreate,
)
from ._testing__create_org_unit import (
    TestingCreateOrgUnit,
    TestingCreateOrgUnitOrgUnitCreate,
)
from ._testing__terminate_manager import (
    TestingTerminateManager,
    TestingTerminateManagerManagerTerminate,
)
from ._testing__terminate_org_unit import (
    TestingTerminateOrgUnit,
    TestingTerminateOrgUnitOrgUnitTerminate,
)
from .async_base_client import AsyncBaseClient
from .employee_name import EmployeeName, EmployeeNameEmployees
from .input_types import (
    AddressCreateInput,
    ClassCreateInput,
    EmployeeCreateInput,
    EngagementCreateInput,
    FacetCreateInput,
    ManagerCreateInput,
    ManagerTerminateInput,
    OrganisationCreate,
    OrganisationUnitCreateInput,
    OrganisationUnitTerminateInput,
)
from .institution_address import InstitutionAddress, InstitutionAddressOrgUnits
from .ituser import Ituser, ItuserItusers
from .manager_data import ManagerData, ManagerDataManagers
from .org_unit_address import OrgUnitAddress, OrgUnitAddressOrgUnits
from .org_unit_ancestors import OrgUnitAncestors, OrgUnitAncestorsOrgUnits
from .org_unit_data import OrgUnitData, OrgUnitDataOrgUnits
from .org_unit_relations import OrgUnitRelations, OrgUnitRelationsOrgUnits
from .related_unit_registrations import (
    RelatedUnitRegistrations,
    RelatedUnitRegistrationsRelatedUnits,
)
from .rolebinding import Rolebinding, RolebindingRolebindings


def gql(q: str) -> str:
    return q


class GraphQLClient(AsyncBaseClient):
    async def manager_data(self, uuid: UUID) -> ManagerDataManagers:
        query = gql("""
            query managerData($uuid: UUID!) {
              managers(filter: {uuids: [$uuid], from_date: null, to_date: null}) {
                objects {
                  validities {
                    employee_uuid
                    org_unit_uuid
                    validity {
                      to
                      from
                    }
                  }
                }
              }
            }
            """)
        variables: dict[str, object] = {"uuid": uuid}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return ManagerData.parse_obj(data).managers

    async def employee_name(self, uuid: UUID) -> EmployeeNameEmployees:
        query = gql("""
            query employeeName($uuid: UUID!) {
              employees(filter: {uuids: [$uuid]}) {
                objects {
                  current {
                    name
                  }
                }
              }
            }
            """)
        variables: dict[str, object] = {"uuid": uuid}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return EmployeeName.parse_obj(data).employees

    async def org_unit_ancestors(self, uuid: UUID) -> OrgUnitAncestorsOrgUnits:
        query = gql("""
            query orgUnitAncestors($uuid: UUID!) {
              org_units(filter: {uuids: [$uuid]}) {
                objects {
                  current {
                    ancestors {
                      uuid
                      name
                    }
                    name
                  }
                }
              }
            }
            """)
        variables: dict[str, object] = {"uuid": uuid}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return OrgUnitAncestors.parse_obj(data).org_units

    async def org_unit_data(self, uuid: UUID) -> OrgUnitDataOrgUnits:
        query = gql("""
            query orgUnitData($uuid: UUID!) {
              org_units(filter: {uuids: [$uuid]}) {
                objects {
                  current {
                    name
                    user_key
                  }
                }
              }
            }
            """)
        variables: dict[str, object] = {"uuid": uuid}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return OrgUnitData.parse_obj(data).org_units

    async def org_unit_relations(self, uuid: UUID) -> OrgUnitRelationsOrgUnits:
        query = gql("""
            query orgUnitRelations($uuid: UUID!) {
              org_units(filter: {uuids: [$uuid]}) {
                objects {
                  current {
                    name
                    root {
                      uuid
                    }
                    engagements {
                      uuid
                    }
                    related_units {
                      org_units {
                        uuid
                        root {
                          uuid
                        }
                      }
                    }
                  }
                }
              }
            }
            """)
        variables: dict[str, object] = {"uuid": uuid}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return OrgUnitRelations.parse_obj(data).org_units

    async def institution_address(
        self, uuid: UUID, root: UUID
    ) -> InstitutionAddressOrgUnits:
        query = gql("""
            query institutionAddress($uuid: UUID!, $root: UUID!) {
              org_units(filter: {parent: {uuids: [$root]}, descendant: {uuids: [$uuid]}}) {
                objects {
                  current {
                    addresses(filter: {address_type: {scope: "EMAIL"}}) {
                      value
                    }
                  }
                }
              }
            }
            """)
        variables: dict[str, object] = {"uuid": uuid, "root": root}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return InstitutionAddress.parse_obj(data).org_units

    async def org_unit_address(self, uuid: UUID) -> OrgUnitAddressOrgUnits:
        query = gql("""
            query orgUnitAddress($uuid: UUID!) {
              org_units(filter: {uuids: [$uuid]}) {
                objects {
                  current {
                    addresses(filter: {address_type: {scope: "EMAIL"}}) {
                      value
                    }
                  }
                }
              }
            }
            """)
        variables: dict[str, object] = {"uuid": uuid}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return OrgUnitAddress.parse_obj(data).org_units

    async def related_unit_registrations(
        self, uuid: UUID
    ) -> RelatedUnitRegistrationsRelatedUnits:
        query = gql("""
            query relatedUnitRegistrations($uuid: UUID!) {
              related_units(filter: {uuids: [$uuid], from_date: null, to_date: null}) {
                objects {
                  registrations {
                    validities {
                      org_units_response {
                        objects {
                          uuid
                          current {
                            root {
                              uuid
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
            """)
        variables: dict[str, object] = {"uuid": uuid}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return RelatedUnitRegistrations.parse_obj(data).related_units

    async def rolebinding(self, uuid: UUID) -> RolebindingRolebindings:
        query = gql("""
            query rolebinding($uuid: UUID!) {
              rolebindings(filter: {uuids: [$uuid]}) {
                objects {
                  current {
                    ituser {
                      uuid
                    }
                  }
                }
              }
            }
            """)
        variables: dict[str, object] = {"uuid": uuid}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return Rolebinding.parse_obj(data).rolebindings

    async def ituser(self, uuid: UUID) -> ItuserItusers:
        query = gql("""
            query ituser($uuid: UUID!) {
              itusers(filter: {uuids: [$uuid]}) {
                objects {
                  current {
                    user_key
                    rolebindings {
                      role {
                        name
                        uuid
                      }
                    }
                    person {
                      name
                      uuid
                    }
                    itsystem {
                      name
                      uuid
                    }
                  }
                }
              }
            }
            """)
        variables: dict[str, object] = {"uuid": uuid}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return Ituser.parse_obj(data).itusers

    async def _testing__create_org_root(
        self, input: OrganisationCreate
    ) -> TestingCreateOrgRootOrgCreate:
        query = gql("""
            mutation _Testing_CreateOrgRoot($input: OrganisationCreate!) {
              org_create(input: $input) {
                uuid
              }
            }
            """)
        variables: dict[str, object] = {"input": input}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return TestingCreateOrgRoot.parse_obj(data).org_create

    async def _testing__create_facet(
        self, input: FacetCreateInput
    ) -> TestingCreateFacetFacetCreate:
        query = gql("""
            mutation _Testing_CreateFacet($input: FacetCreateInput!) {
              facet_create(input: $input) {
                uuid
              }
            }
            """)
        variables: dict[str, object] = {"input": input}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return TestingCreateFacet.parse_obj(data).facet_create

    async def _testing__create_class(
        self, input: ClassCreateInput
    ) -> TestingCreateClassClassCreate:
        query = gql("""
            mutation _Testing_CreateClass($input: ClassCreateInput!) {
              class_create(input: $input) {
                uuid
              }
            }
            """)
        variables: dict[str, object] = {"input": input}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return TestingCreateClass.parse_obj(data).class_create

    async def _testing__create_employee(
        self, input: EmployeeCreateInput
    ) -> TestingCreateEmployeeEmployeeCreate:
        query = gql("""
            mutation _Testing_CreateEmployee($input: EmployeeCreateInput!) {
              employee_create(input: $input) {
                uuid
              }
            }
            """)
        variables: dict[str, object] = {"input": input}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return TestingCreateEmployee.parse_obj(data).employee_create

    async def _testing__create_address(
        self, input: AddressCreateInput
    ) -> TestingCreateAddressAddressCreate:
        query = gql("""
            mutation _Testing_CreateAddress($input: AddressCreateInput!) {
              address_create(input: $input) {
                uuid
              }
            }
            """)
        variables: dict[str, object] = {"input": input}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return TestingCreateAddress.parse_obj(data).address_create

    async def _testing__create_org_unit(
        self, input: OrganisationUnitCreateInput
    ) -> TestingCreateOrgUnitOrgUnitCreate:
        query = gql("""
            mutation _Testing_CreateOrgUnit($input: OrganisationUnitCreateInput!) {
              org_unit_create(input: $input) {
                uuid
              }
            }
            """)
        variables: dict[str, object] = {"input": input}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return TestingCreateOrgUnit.parse_obj(data).org_unit_create

    async def _testing__create_manager(
        self, input: ManagerCreateInput
    ) -> TestingCreateManagerManagerCreate:
        query = gql("""
            mutation _Testing_CreateManager($input: ManagerCreateInput!) {
              manager_create(input: $input) {
                uuid
              }
            }
            """)
        variables: dict[str, object] = {"input": input}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return TestingCreateManager.parse_obj(data).manager_create

    async def _testing__terminate_manager(
        self, input: ManagerTerminateInput
    ) -> TestingTerminateManagerManagerTerminate:
        query = gql("""
            mutation _Testing_TerminateManager($input: ManagerTerminateInput!) {
              manager_terminate(input: $input) {
                uuid
              }
            }
            """)
        variables: dict[str, object] = {"input": input}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return TestingTerminateManager.parse_obj(data).manager_terminate

    async def _testing__create_engagement(
        self, input: EngagementCreateInput
    ) -> TestingCreateEngagementEngagementCreate:
        query = gql("""
            mutation _Testing_CreateEngagement($input: EngagementCreateInput!) {
              engagement_create(input: $input) {
                uuid
              }
            }
            """)
        variables: dict[str, object] = {"input": input}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return TestingCreateEngagement.parse_obj(data).engagement_create

    async def _testing__terminate_org_unit(
        self, input: OrganisationUnitTerminateInput
    ) -> TestingTerminateOrgUnitOrgUnitTerminate:
        query = gql("""
            mutation _Testing_TerminateOrgUnit($input: OrganisationUnitTerminateInput!) {
              org_unit_terminate(input: $input) {
                uuid
              }
            }
            """)
        variables: dict[str, object] = {"input": input}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return TestingTerminateOrgUnit.parse_obj(data).org_unit_terminate
