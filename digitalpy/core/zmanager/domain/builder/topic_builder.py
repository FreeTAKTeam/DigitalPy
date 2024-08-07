from typing import List, Union, TYPE_CHECKING
from functools import singledispatchmethod
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.request import Request
from digitalpy.core.domain.builder import Builder

from digitalpy.core.zmanager.configuration.zmanager_constants import (
    TOPIC,
    TopicCategory,
)
from digitalpy.core.zmanager.domain.model.topic import Topic

class TopicBuilder(Builder):
    """Builds a topic object"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result: Topic = None  # type: ignore

    def build_empty_object(
        self, config_loader=None, *args, **kwargs
    ):  # pylint: disable=unused-argument
        """Builds a topic object, config_loader is None because it is not used"""
        #TODO: disucs with team how to use config_loader in a consistent way
        self.request.set_value("object_class_name", "topic")
        if config_loader is None:
            configuration = None
        else:    
            configuration = config_loader.find_configuration(TOPIC)
        
        self.result = super()._create_model_object(
            configuration=configuration,
            extended_domain={
                "topic": Topic,
            },
        )

    @singledispatchmethod
    def add_object_data(self, mapped_object):
        """adds the data from the mapped object to the topic object"""
        raise TypeError(f"Unsupported object type: {type(mapped_object)}")

    @add_object_data.register
    def _(self, mapped_object: Request):
        """adds the data from the service object to the topic object, typically used for the topics to which a service will subscribe"""
        self.result.category = TopicCategory.REQUEST
        self.result.protocol = mapped_object.get_format()
        self.result.extension.extend(
            [
                mapped_object.get_sender(),
                mapped_object.get_context(),
                mapped_object.get_action(),
                mapped_object.get_id(),
            ]
        )

    @add_object_data.register
    def _(self, mapped_object: Response):
        self.result.category = TopicCategory.RESPONSE
        self.result.protocol = mapped_object.get_format()
        self.result.extension.extend(
            [mapped_object.get_sender(), mapped_object.get_id()]
        )

    def get_result(self):
        """gets the result of the builder"""
        return self.result
