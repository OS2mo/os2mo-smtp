# Generated by ariadne-codegen on 2025-02-20 12:55
# Source: queries.graphql

from typing import List, Optional, Union
from uuid import UUID

from .async_base_client import AsyncBaseClient
from .base_model import UNSET, UnsetType
from .get_address_data import GetAddressData, GetAddressDataAddresses
from .get_institution_address import (
    GetInstitutionAddress,
    GetInstitutionAddressOrgUnits,
)
from .get_manager_data import GetManagerData, GetManagerDataManagers
from .get_org_unit_data import GetOrgUnitData, GetOrgUnitDataOrgUnits
from .get_org_unit_relations import GetOrgUnitRelations, GetOrgUnitRelationsOrgUnits
from .get_root_org import GetRootOrg, GetRootOrgOrg
from .get_user_data import GetUserData, GetUserDataEmployees


def gql(q: str) -> str:
    return q


class GraphQLClient(AsyncBaseClient):
    async def get_manager_data(
        self, uuids: Union[Optional[List[UUID]], UnsetType] = UNSET
    ) -> GetManagerDataManagers:
        query = gql(
            """
            query getManagerData($uuids: [UUID!]) {
              managers(filter: {uuids: $uuids, from_date: null, to_date: null}) {
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
            """
        )
        variables: dict[str, object] = {"uuids": uuids}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetManagerData.parse_obj(data).managers

    async def get_user_data(
        self, uuids: Union[Optional[List[UUID]], UnsetType] = UNSET
    ) -> GetUserDataEmployees:
        query = gql(
            """
            query getUserData($uuids: [UUID!]) {
              employees(filter: {uuids: $uuids}) {
                objects {
                  validities {
                    name
                    addresses {
                      value
                      address_type {
                        scope
                      }
                    }
                    engagements {
                      org_unit_uuid
                    }
                  }
                }
              }
            }
            """
        )
        variables: dict[str, object] = {"uuids": uuids}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetUserData.parse_obj(data).employees

    async def get_root_org(self) -> GetRootOrgOrg:
        query = gql(
            """
            query getRootOrg {
              org {
                uuid
              }
            }
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetRootOrg.parse_obj(data).org

    async def get_org_unit_data(
        self, uuids: Union[Optional[List[UUID]], UnsetType] = UNSET
    ) -> GetOrgUnitDataOrgUnits:
        query = gql(
            """
            query getOrgUnitData($uuids: [UUID!]) {
              org_units(filter: {uuids: $uuids}) {
                objects {
                  validities {
                    name
                    user_key
                    parent_uuid
                    managers {
                      employee_uuid
                    }
                  }
                }
              }
            }
            """
        )
        variables: dict[str, object] = {"uuids": uuids}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetOrgUnitData.parse_obj(data).org_units

    async def get_address_data(
        self, uuids: Union[Optional[List[UUID]], UnsetType] = UNSET
    ) -> GetAddressDataAddresses:
        query = gql(
            """
            query getAddressData($uuids: [UUID!]) {
              addresses(filter: {uuids: $uuids}) {
                objects {
                  current {
                    name
                    employee_uuid
                    address_type {
                      scope
                    }
                  }
                }
              }
            }
            """
        )
        variables: dict[str, object] = {"uuids": uuids}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetAddressData.parse_obj(data).addresses

    async def get_org_unit_relations(
        self, uuids: Union[Optional[List[UUID]], UnsetType] = UNSET
    ) -> GetOrgUnitRelationsOrgUnits:
        query = gql(
            """
            query getOrgUnitRelations($uuids: [UUID!]) {
              org_units(filter: {uuids: $uuids}) {
                objects {
                  current {
                    name
                    root {
                      uuid
                    }
                    engagements {
                      uuid
                    }
                    related_units(exclude_self: true) {
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
            """
        )
        variables: dict[str, object] = {"uuids": uuids}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetOrgUnitRelations.parse_obj(data).org_units

    async def get_institution_address(
        self,
        uuids: Union[Optional[List[UUID]], UnsetType] = UNSET,
        root: Union[Optional[List[UUID]], UnsetType] = UNSET,
    ) -> GetInstitutionAddressOrgUnits:
        query = gql(
            """
            query getInstitutionAddress($uuids: [UUID!], $root: [UUID!]) {
              org_units(filter: {parent: {uuids: $root}, descendant: {uuids: $uuids}}) {
                objects {
                  current {
                    addresses(filter: {address_type: {scope: "EMAIL"}}) {
                      value
                    }
                  }
                }
              }
            }
            """
        )
        variables: dict[str, object] = {"uuids": uuids, "root": root}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetInstitutionAddress.parse_obj(data).org_units
