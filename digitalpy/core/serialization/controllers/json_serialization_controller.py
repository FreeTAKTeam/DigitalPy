from typing import Any, Dict, Union
from digitalpy.core.main.controller import (
    Controller,
)
from digitalpy.core.domain.relationship import Relationship
from digitalpy.core.domain.node import Node
from digitalpy.core.parsing.load_configuration import ModelConfiguration as LoadConf
from digitalpy.core.domain.domain_facade import Domain
from copy import deepcopy
import json


class JSONSerializationController(Controller):
    """The JSONSerializationController class is responsible for serializing and deserializing nodes to and from JSON strings"""

    # this is a class variable that is used to keep track of the nodes that are being serialized to prevent infinite recursion
    serializing = []

    def __init__(self, request, response, sync_action_mapper, configuration) -> None:
        JSONSerializationController.serializing = []
        super().__init__(sync_action_mapper, request, response, configuration)
        self.domain_controller = Domain(
            sync_action_mapper, request, response, configuration
        )

    def deserialize(
        self, message: Union[str, bytes, dict], model_object: Node, *args, **kwargs
    ):
        """converts the provided xml string to a node

        Args:
            message (bytes): the xml string to be converted to a node
        """
        if isinstance(message, bytes):
            dictionary = json.loads(message)
        elif isinstance(message, str):
            dictionary = json.loads(message)
        else:
            dictionary = message
        deserialized_model_obj = self._deserialize(
            dictionary=dictionary, node=model_object
        )
        self.response.set_value("model_object", deserialized_model_obj)
        return deserialized_model_obj

    def _deserialize(self, dictionary: dict, node: Node):
        """recursively serialize a single layer of the given dictionary
        to a node object until a nested dictionary is found"""
        try:
            # if the dictionary is a nested dictionary, the first key is the root node class name
            if list(dictionary.keys())[0].lower() == node.__class__.__name__.lower():
                dictionary = dictionary[list(dictionary.keys())[0]]

            for key, value in dictionary.items():
                self.add_value_to_node(key, value, node)
            return node
        except Exception as ex:
            print(ex)

    def add_value_to_node(self, key, value, node: Node):
        """add a value to a node object"""

        # handles the case in which the value is a dictionary and the node attribute is a node
        if isinstance(value, dict) and (
            isinstance(getattr(node, key, None), Node)
            or isinstance(getattr(node, key, None), list)
        ):
            self._deserialize(value, getattr(node, key))

        # handles the case in which the value is a dictionary and the node attribute is not yet initialized such as in the case of an optional
        # attribute
        elif isinstance(value, dict):
            new_node = self.domain_controller.create_node(
                node._model_configuration,
                node._model_configuration.elements[node.__class__.__name__]
                .relationships[key]
                .target_class,
                extended_domain=node._model,
            )
            self._deserialize(value, new_node)
            setattr(node, key, new_node)

        # handles the case in which the value is a list and the node attribute is a list
        elif (
            isinstance(value, list)
            and isinstance(getattr(node, key, None), list)
            and isinstance(type(node).__dict__[key], Relationship)
        ):
            # add all mandatory nodes
            for i in range(len(getattr(node, key))):
                self._deserialize(value[i], getattr(node, key)[i])

            # add all optional nodes
            for i in range(len(getattr(node, key)), len(value)):
                new_node = self.domain_controller.create_node(
                    node._model_configuration,
                    node._model_configuration.elements[node.__class__.__name__]
                    .relationships[key]
                    .target_class,
                    extended_domain=node._model,
                )
                self._deserialize(value[i], new_node)
                setattr(node, key, new_node)

        # handles the generic case in which the value is not a dictionary or a list
        else:
            setattr(node, key, value)

    def serialize_node(self, message, **kwargs):
        """converts the provided node to an json string

        Args:
            node (Node): the node to be serialized to xml
        """
        messages = []
        if isinstance(message, list):
            messages = [
                self._serialize_node(node, node.__class__.__name__.lower())
                for node in message
            ]
        else:
            messages = [
                self._serialize_node(message, message.__class__.__name__.lower())
            ]
        self.response.set_value("message", messages)
        return messages

    def _serialize_node(self, node: Node, tag_name: str, level=0) -> Union[str, Dict]:
        """the body of the serialization function recursively serializes each node class

        Args:
            node (Node): the root node class to be serialized
            tag_name (str): the name of the root node class to be serialized
            level (int, optional): _description_. Defaults to 0.

        Returns:
            Union[str, Dict]: the original call to this method returns a string representing the xml
                the Element is only returned in the case of recursive calls
        """
        if node.oid in JSONSerializationController.serializing:
            return None
        JSONSerializationController.serializing.append(node.oid)
        json_data = {}

        for attrib_name in node.get_properties():
            # below line is required because get_all_properties function returns only cot property names
            value = getattr(node, attrib_name)
            if hasattr(value, "__dict__"):
                attrib_name, json_sub_element = self.handle_nested_object(
                    level, attrib_name, value
                )
                json_data[attrib_name] = json_sub_element

            elif value == None:
                continue

            elif isinstance(value, list):
                json_data[attrib_name] = []
                for element in value:
                    if not hasattr(element, "__dict__"):
                        self.handle_attribute(json_data, attrib_name, value)
                        break
                    else:
                        attrib_name, json_sub_element = self.handle_nested_object(
                            level, attrib_name, element
                        )
                        json_data[attrib_name].append(json_sub_element)

            else:
                # TODO: modify so double underscores are handled differently
                # handles instances in which attribute name begins with double underscore
                self.handle_attribute(json_data, attrib_name, value)
        for child in list(node.get_children().values()):
            self.handle_child(json_data, child, level)
        if level == 0:
            JSONSerializationController.serializing.remove(node.oid)
            return json_data
        else:
            JSONSerializationController.serializing.remove(node.oid)
            return json_data

    def handle_child(self, json_data, child, level):
        """
        Handles the serialization of a child node.

        Args:
            json_data (dict): The JSON data being serialized.
            child (Node): The child node to be serialized.
            level (int): The current level of serialization.

        Returns:
            None
        """
        child_class_name = child.__class__.__name__.lower()
        if isinstance(json_data.get(child_class_name, None), dict):
            json_data[child_class_name] = [
                json_data[child_class_name],
                self._serialize_node(child, child_class_name, level=level + 1),
            ]
        elif isinstance(json_data.get(child_class_name, None), list):
            json_data[child_class_name].append(
                self._serialize_node(child, child_class_name, level=level + 1)
            )
        else:
            resp = self._serialize_node(child, child_class_name, level=level + 1)
            if resp:
                json_data[child_class_name] = resp

    def handle_nested_object(self, level, attrib_name, value):
        json_sub_element = self._serialize_node(value, attrib_name, level=level + 1)
        # TODO: modify so double underscores are handled differently
        try:
            if attrib_name[0] == "_":
                attrib_name = "_" + attrib_name
        except:
            pass
        return attrib_name, json_sub_element

    def handle_attribute(self, json_data, attrib_name, value):
        try:
            if attrib_name[0] == "_":
                attrib_name = "_" + attrib_name
                json_data[attrib_name] = value
        except:
            pass
        else:
            json_data[attrib_name] = value
