import uuid
from digitalpy.core.domain.object_id import ObjectId
from digitalpy.core.main.object_factory import ObjectFactory
import tests.testing_utilities.facade_utilities as facade_utilities
from tests.testing_utilities.domain_objects.simple_object import SimpleObject
from tests.testing_utilities.domain_objects.list_object import ListObject
from tests.testing_utilities.domain_objects.simple_list import SimpleList
from tests.testing_utilities import domain_objects

from digitalpy.core.domain.domain_facade import Domain
from digitalpy.core.service_management.domain.service_description import ServiceDescription
from digitalpy.core.service_management.domain.service_status import ServiceStatus
from digitalpy.core.parsing.load_configuration import ModelConfiguration, ConfigurationEntry, Relationship
from digitalpy.core.domain.domain.network_client import NetworkClient


def initialize_simple_object(request, response) -> SimpleObject:
    """initialize a simple domain object"""
    domain = facade_utilities.initialize_facade(
        "digitalpy.core.domain.domain_facade.Domain", request=request, response=response)
    simple_object = domain.create_node(ModelConfiguration(), "SimpleObject", extended_domain={
                                       "SimpleObject": domain_objects.SimpleObject})
    return simple_object

def initialize_simple_list(request, response) -> SimpleObject:
    """initialize a simple domain object with a list of strings"""
    domain = facade_utilities.initialize_facade(
        "digitalpy.core.domain.domain_facade.Domain", request=request, response=response)
    simple_object = domain.create_node(ModelConfiguration(), "SimpleList", extended_domain={
                                       "SimpleList": domain_objects.SimpleList})
    return simple_object

def initialize_list_object(request, response) -> ListObject:
    """initialize a list domain object"""
    domain = facade_utilities.initialize_facade(
        "digitalpy.core.domain.domain_facade.Domain", request=request, response=response)
    model_def = ModelConfiguration(
        elements={"ListObject":
                  ConfigurationEntry(
                      relationships={"list_data": Relationship(0, -1, "SimpleObject")}),
                  "SimpleObject":
                  ConfigurationEntry()
                  }
    )
    simple_object = domain.create_node(model_def, "ListObject", extended_domain={
                                       "ListObject": domain_objects.ListObject,
                                       "SimpleObject": domain_objects.SimpleObject
                                    })
    return simple_object

def initialize_list_object_with_min(request, response) -> ListObject:
    """initialize a list domain object"""
    domain = facade_utilities.initialize_facade(
        "digitalpy.core.domain.domain_facade.Domain", request=request, response=response)
    model_def = ModelConfiguration(
        elements={"ListObject":
                  ConfigurationEntry(
                      relationships={"list_data": Relationship(2, 4, "SimpleObject")}),
                  "SimpleObject":
                  ConfigurationEntry()
                  }
    )
    simple_object = domain.create_node(model_def, "ListObject", extended_domain={
                                       "ListObject": domain_objects.ListObject,
                                       "SimpleObject": domain_objects.SimpleObject
                                    })
    return simple_object

def initialize_nested_object(request, response) -> ListObject:
    """initialize a nested domain object"""
    domain = facade_utilities.initialize_facade(
        "digitalpy.core.domain.domain_facade.Domain", request=request, response=response)
    model_def = ModelConfiguration(
        elements={"NestedObject":
                  ConfigurationEntry(
                      relationships={"nested": Relationship(0, 1, "SimpleObject")}),
                  "SimpleObject": ConfigurationEntry()
                  }
    )
    simple_object = domain.create_node(model_def, "NestedObject",
                                       extended_domain={
                                           "NestedObject": domain_objects.NestedObject,
                                           "SimpleObject": domain_objects.SimpleObject
                                        })
    return simple_object

def initialize_nested_object_required(request, response) -> ListObject:
    """initialize a nested domain object"""
    domain = facade_utilities.initialize_facade(
        "digitalpy.core.domain.domain_facade.Domain", request=request, response=response)
    model_def = ModelConfiguration(
        elements={"NestedObject":
                    ConfigurationEntry(
                        relationships={"nested": Relationship(1, 1, "SimpleObject")}),
                  "SimpleObject": ConfigurationEntry()
                  }
    )
    simple_object = domain.create_node(model_def, "NestedObject",
                                       extended_domain={
                                           "NestedObject": domain_objects.NestedObject,
                                           "SimpleObject": domain_objects.SimpleObject
                                        })
    return simple_object

def initialize_test_service_description(request, response):
    """create a test service description"""
    domain = facade_utilities.initialize_facade(
        "digitalpy.core.domain.domain_facade.Domain", request=request, response=response)
    model_def = ModelConfiguration()
    service_description:ServiceDescription = domain.create_node(model_def, "ServiceDescription", extended_domain={"ServiceDescription": ServiceDescription})
    service_description.name = "TestService"
    service_description.protocol = "json"
    service_description.status = ServiceStatus.RUNNING
    service_description.description = "Test Service"
    service_description.id = "TestService"
    return service_description

def initialize_test_network_client():
    """create a test network client"""
    # create a new client object
    oid = ObjectId("network_client", id=str(uuid.uuid4()))
    client: NetworkClient = ObjectFactory.get_new_instance(
        "DefaultClient", dynamic_configuration={"oid": oid})
    client.protocol = "json"
    client.service_id = "TestService"
    return client
