import tests.testing_utilities.facade_utilities as facade_utilities
from tests.testing_utilities.domain_objects.simple_object import SimpleObject
from tests.testing_utilities.domain_objects.list_object import ListObject
from tests.testing_utilities import domain_objects

from digitalpy.core.domain.domain_facade import Domain
from digitalpy.core.parsing.load_configuration import ModelConfiguration, ConfigurationEntry, Relationship


def initialize_simple_object(request, response) -> SimpleObject:
    """initialize a simple domain object"""
    domain = facade_utilities.initialize_facade(
        "digitalpy.core.domain.domain_facade.Domain", request=request, response=response)
    simple_object = domain.create_node(ModelConfiguration(), "SimpleObject", extended_domain={
                                       "SimpleObject": domain_objects.SimpleObject})
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