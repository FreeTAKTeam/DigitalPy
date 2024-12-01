import uuid

import digitalpy.testing.facade_utilities as facade_utilities
from digitalpy.core.domain.domain.network_client import NetworkClient
from digitalpy.core.domain.domain_facade import Domain
from digitalpy.core.domain.object_id import ObjectId
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.parsing.load_configuration import (ConfigurationEntry,
                                                       ModelConfiguration,
                                                       Relationship)
from digitalpy.core.service_management.domain.model.service_description import \
    ServiceDescription
from digitalpy.core.service_management.domain.model.service_status_enum import \
    ServiceStatusEnum
from digitalpy.testing import domain_objects
from digitalpy.testing.domain_objects.enum_object import EnumObject
from digitalpy.testing.domain_objects.list_object import ListObject
from digitalpy.testing.domain_objects.simple_object import SimpleObject


def initialize_simple_object(request, response) -> SimpleObject:
    """initialize a simple domain object"""
    domain: Domain = facade_utilities.initialize_facade(
        "digitalpy.core.domain.domain_facade.Domain", request=request, response=response
    )
    simple_object = domain.create_node(
        ModelConfiguration(),
        "SimpleObject",
        extended_domain={"SimpleObject": domain_objects.SimpleObject},
    )
    return simple_object

def initialize_enum_object(request, response) -> EnumObject:
    """initialize an enum domain object"""
    domain: Domain = facade_utilities.initialize_facade(
        "digitalpy.core.domain.domain_facade.Domain", request=request, response=response
    )
    enum_object: EnumObject = domain.create_node(
        ModelConfiguration(),
        "EnumObject",
        extended_domain={"EnumObject": EnumObject},
    )
    return enum_object

def initialize_simple_list(request, response) -> SimpleObject:
    """initialize a simple domain object with a list of strings"""
    domain: Domain = facade_utilities.initialize_facade(
        "digitalpy.core.domain.domain_facade.Domain", request=request, response=response
    )
    simple_object = domain.create_node(
        ModelConfiguration(),
        "SimpleList",
        extended_domain={"SimpleList": domain_objects.SimpleList},
    )
    return simple_object


def initialize_list_object(request, response) -> ListObject:
    """initialize a list domain object"""
    domain: Domain = facade_utilities.initialize_facade(
        "digitalpy.core.domain.domain_facade.Domain", request=request, response=response
    )
    model_def = ModelConfiguration(
        elements={
            "ListObject": ConfigurationEntry(
                relationships={"list_data": Relationship(0, -1, "SimpleObject")}
            ),
            "SimpleObject": ConfigurationEntry(),
        }
    )
    simple_object = domain.create_node(
        model_def,
        "ListObject",
        extended_domain={
            "ListObject": domain_objects.ListObject,
            "SimpleObject": domain_objects.SimpleObject,
        },
    )
    return simple_object


def initialize_list_object_with_min(request, response) -> ListObject:
    """initialize a list domain object"""
    domain: Domain = facade_utilities.initialize_facade(
        "digitalpy.core.domain.domain_facade.Domain", request=request, response=response
    )
    model_def = ModelConfiguration(
        elements={
            "ListObject": ConfigurationEntry(
                relationships={"list_data": Relationship(2, 4, "SimpleObject")}
            ),
            "SimpleObject": ConfigurationEntry(),
        }
    )
    simple_object = domain.create_node(
        model_def,
        "ListObject",
        extended_domain={
            "ListObject": domain_objects.ListObject,
            "SimpleObject": domain_objects.SimpleObject,
        },
    )
    return simple_object


def initialize_nested_object(request, response) -> ListObject:
    """initialize a nested domain object"""
    domain: Domain = facade_utilities.initialize_facade(
        "digitalpy.core.domain.domain_facade.Domain", request=request, response=response
    )
    model_def = ModelConfiguration(
        elements={
            "NestedObject": ConfigurationEntry(
                relationships={"nested": Relationship(0, 1, "SimpleObject")}
            ),
            "SimpleObject": ConfigurationEntry(),
        }
    )
    simple_object = domain.create_node(
        model_def,
        "NestedObject",
        extended_domain={
            "NestedObject": domain_objects.NestedObject,
            "SimpleObject": domain_objects.SimpleObject,
        },
    )
    return simple_object


def initialize_nested_object_required(request, response) -> ListObject:
    """initialize a nested domain object"""
    domain: Domain = facade_utilities.initialize_facade(
        "digitalpy.core.domain.domain_facade.Domain", request=request, response=response
    )
    model_def = ModelConfiguration(
        elements={
            "NestedObject": ConfigurationEntry(
                relationships={"nested": Relationship(1, 1, "SimpleObject")}
            ),
            "SimpleObject": ConfigurationEntry(),
        }
    )
    simple_object = domain.create_node(
        model_def,
        "NestedObject",
        extended_domain={
            "NestedObject": domain_objects.NestedObject,
            "SimpleObject": domain_objects.SimpleObject,
        },
    )
    return simple_object

def initialize_test_service_description(request, response):
    """create a test service description"""
    domain: Domain = facade_utilities.initialize_facade(
        "digitalpy.core.domain.domain_facade.Domain", request=request, response=response
    )
    model_def = ModelConfiguration()
    service_description: ServiceDescription = domain.create_node(
        model_def,
        "ServiceDescription",
        extended_domain={"ServiceDescription": ServiceDescription},
    )
    service_description.name = "TestService"
    service_description.protocol = "json"
    service_description.status = ServiceStatusEnum.RUNNING
    service_description.description = "Test Service"
    service_description.id = "TestService"
    return service_description


def initialize_test_network_client():
    """create a test network client"""
    # create a new client object
    oid = ObjectId("network_client", id=str(uuid.uuid4()))
    client: NetworkClient = ObjectFactory.get_new_instance(
        "DefaultClient", dynamic_configuration={"oid": oid}
    )
    client.protocol = "json"
    client.service_id = "TestService"
    return client
