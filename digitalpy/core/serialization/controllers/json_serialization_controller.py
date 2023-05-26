from typing import Dict, Union
from digitalpy.core.main.controller import (
    Controller,
)
from digitalpy.core.domain.node import Node
from copy import deepcopy
import json

class JSONSerializationController(Controller):
    def __init__(self, request, response, action_mapper, configuration) -> None:
        super().__init__(request, response, action_mapper, configuration)

    def serialize_node(self, node, **kwargs):
        """converts the provided node to an xml string

        Args:
            node (Node): the node to be serialized to xml
        """
        # TODO this should not be a direct return and should be fixed ASAP
        return self._serialize_node(node, node.__class__.__name__.lower())

    def _serialize_node(
        self, node: Node, tag_name: str, level=0
    ) -> Union[str, Dict]:
        """the body of the serialization function recursively serializes each node class

        Args:
            node (Node): the root node class to be serialized
            tag_name (str): the name of the root node class to be serialized
            level (int, optional): _description_. Defaults to 0.

        Returns:
            Union[str, Dict]: the original call to this method returns a string representing the xml
                the Element is only returned in the case of recursive calls
        """
        json_data = {}
        
        for attrib_name in node.get_properties():
            # below line is required because get_all_properties function returns only cot property names
            value = getattr(node, attrib_name)
            if hasattr(value, "__dict__"):
                attrib_name, json_sub_element = self.handle_nested_object(level, attrib_name, value)
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
                        attrib_name, json_sub_element = self.handle_nested_object(level, attrib_name, element)
                        json_data[attrib_name].append(json_sub_element)

            else:
                # TODO: modify so double underscores are handled differently
                # handles instances in which attribute name begins with double underscore
                self.handle_attribute(json_data, attrib_name, value)
                
        
        if level == 0:
            return json.dumps(json_data)
        else:
            return json_data

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