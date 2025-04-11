from typing import Any
from uuid import UUID
import structlog

from more_itertools import one

from .helpers import extract_current_or_latest_validity

from .autogenerated_graphql_client.client import GraphQLClient
from .autogenerated_graphql_client.ituser import ItuserItusersObjectsCurrent

logger = structlog.get_logger()


async def get_address_data(mo: GraphQLClient, uuid: UUID) -> Any:
    """
    Loads information concerning an employee's address

    Args:
        key: User UUID
        graphql_session: The GraphQL session to run queries on

    Return:
        Dictionary with queried address data
    """
    gql_response = await mo.address_data(uuid)
    if gql_response.objects:
        return one(gql_response.objects).current
    return


async def get_manager_data(mo: GraphQLClient, uuid: UUID) -> Any:
    gql_response = await mo.manager_data(uuid)
    if gql_response.objects:
        return extract_current_or_latest_validity(one(gql_response.objects).validities)


async def get_employee_data(mo: GraphQLClient, uuid: UUID) -> Any:
    """
    Loads a user's data

    Args:
        uuid: List of user UUIDs to query
        graphql_session: The GraphQL session to run queries on

    Return:
        Dictionary with queried user data
    """
    gql_response = await mo.employee_data(uuid)
    return one(gql_response.objects).current


async def get_employee_name(mo: GraphQLClient, uuid: UUID) -> Any:
    """
    Loads a user's name

    Args:
        uuid: List of user UUIDs to query
        graphql_session: The GraphQL session to run queries on

    Return:
        Dictionary with queried user data
    """
    gql_response = await mo.employee_name(uuid)
    return one(gql_response.objects).current


async def get_org_unit_data(mo: GraphQLClient, uuid: UUID) -> Any:
    """
    Loads a user's data

    Args:
        key: User UUID
        graphql_session: The GraphQL session to run queries on

    Return:
        Dictionary with queried org unit data
    """
    gql_response = await mo.org_unit_data(uuid)
    return one(gql_response.objects).current


async def get_org_unit_location(mo: GraphQLClient, uuid: UUID):
    """
    Constructs and org-unit location string, where different org-units in the
    hierarchy are separated by forward slashes.
    """
    gql_response = await mo.org_unit_ancestors(uuid)
    org_units = gql_response.objects
    current = one(org_units).current

    org_unit_location = ""
    if current:
        ancestors = [ancestor.name for ancestor in reversed(current.ancestors)]
        org_unit_location = " / ".join(ancestors + [current.name])

    return org_unit_location


async def get_org_unit_relations(mo: GraphQLClient, org_unit_uuid: UUID):
    gql_response = await mo.org_unit_relations(org_unit_uuid)
    return gql_response.objects


async def get_institution_address(mo: GraphQLClient, uuid: UUID, root: UUID):
    gql_response = await mo.institution_address(uuid, root)
    current = one(gql_response.objects).current
    addresses = {address.value for address in current.addresses} if current else set()

    return addresses


async def get_ituser_uuid_by_rolebinding(mo: GraphQLClient, uuid: UUID) -> UUID | None:
    try:
        gql_response = await mo.rolebinding(uuid)
        current = one(gql_response.objects).current
        if current is None:
            return None
        ituser_uuid = one(current.ituser).uuid
        return ituser_uuid
    except Exception:  # pragma: no cover
        logger.warning(
            "Failed to fetch ituser from rolebinding UUID."
            "This is usually caused by rolebinding events being fired, when it should've only been an ituser event"
        )
        return None


async def get_ituser(
    mo: GraphQLClient, uuid: UUID
) -> ItuserItusersObjectsCurrent | None:
    gql_response = await mo.ituser(uuid)
    ituser_data = one(gql_response.objects).current
    return ituser_data
