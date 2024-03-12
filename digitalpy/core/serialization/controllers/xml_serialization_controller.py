from typing import Union
from digitalpy.core.main.controller import (
    Controller,
)
from copy import deepcopy
from lxml.etree import Element  # pylint: disable=no-name-in-module
from lxml import etree
import xmltodict
import uuid

from digitalpy.core.domain.node import Node
from digitalpy.core.parsing.load_configuration import ModelConfiguration as LoadConf
from digitalpy.core.main.object_factory import ObjectFactory

class XMLDeserializer:
    """this class exposes the basic lxml target interface for parsing COTs to Node objects"""
    def __init__(self, node: Node) -> None:
        if node is None:
            raise ValueError("node cannot be None")
        if not isinstance(node, Node):
            raise ValueError("node must be an instance of Node")
        self.root_node: Node = node
        self.curr_object: Node = None
        self.prev_object: Node = None
        self.siblings = []
        self.stack = []
        
        self.xml_obj: etree.ElementBase = None
        self.xml_root: etree.ElementBase = None

    def start(self, tag: str, attrib: dict):
        """this method is called when the parser encounters a start tag

        Args:
            tag (str): the tag name
            attrib (dict): the attributes of the tag
        """
        # check that the tag matches the current node
        if self.curr_object is None:
            self.curr_object = self.root_node
        else:
            children = self._get_child_node(tag)

            # if the tag is a sibling of the current node, set the current node to the sibling
            if len(children)>1:
                self.siblings = children
                self.curr_object = self.siblings.pop()

            # if the tag is a child of the current node, set the current node to the child
            elif len(children)==1:
                self.curr_object = children.pop()
            
            # if the tag is not a child of the current node, create a new xml element and add it to the current node
            else:
                if self.xml_obj is None:
                    self.xml_root = etree.Element(tag, attrib)
                    self.xml_obj = self.xml_root
                else:
                    self.xml_obj = etree.SubElement(self.xml_obj, tag, attrib)
                return
        
        # if the current node is the same type as the previous node, create a new instance of the current node
        if type(self.curr_object) == type(self.prev_object):
            id = str(uuid.uuid1())
            oid = ObjectFactory.get_instance(
                "ObjectId", {"id": id, "type": str(type(self.curr_object))}
            )

            new_inst = type(self.curr_object)(LoadConf(), None, oid)
            self.prev_object.get_parent().add_child(new_inst)
            self.curr_object = new_inst

        # set the attributes of the current node
        for key, value in attrib.items():
            if key in self.curr_object.cot_attributes:
                setattr(self.curr_object, key, value)
            else:
                self.curr_object.xml.set(key, value)

    def _get_child_node(self, tag: str) -> list[Node]:
        """gets the child node of the current node with the given tag name

        Args:
            tag (str): the tag name of the child node

        Returns:
            Node: the child node
        """
        children = self.curr_object.get_children_ex(children_type=tag)
        return children
        
    def end(self, tag):
        """this method is called when the parser encounters an end tag

        Args:
            tag (str): the tag name, required by the lxml target interface
        """
        if self.xml_root is not None and tag == self.xml_root.tag:
            self.xml_obj = None
        elif self.xml_obj is not None:
            self.xml_obj = self.xml_obj.getparent()
        else:
            self.prev_object = self.curr_object
            self.curr_object = self.curr_object.get_parent()
        
    def data(self, data: str):
        """this method is called when the parser encounters data

        Args:
            data (str): the data
        """

        # if the current node has an xml object, set the text of the xml object
        if self.xml_obj is not None:
            self.xml_obj.text = data
        # otherwise, set the text of the current node
        else:
            self.curr_object.text = data

    def comment(self, text):
        pass

    def close(self):
        return self.root_node

class XMLSerializationController(Controller):
    def __init__(self, request, response, action_mapper, configuration) -> None:
        super().__init__(request, response, action_mapper, configuration)

    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
        return self.response

    def serialize_node(self, node, **kwargs):
        """converts the provided node to an xml string

        Args:
            node (Node): the node to be serialized to xml
        """
        # TODO this should not be a direct return and should be fixed ASAP
        return self._serialize_node(node, node.__class__.__name__.lower())

    def deserialize(self, message: bytes, model_object: Node, *args, **kwargs):
        """converts the provided xml string to a node

        Args:
            message (bytes): the xml string to be converted to a node
        """
        return self._deserialize(message, model_object)
    
    def _deserialize(self, message: bytes, model_object: Node) -> Node:
        target = XMLDeserializer(model_object)
        parser = etree.XMLParser(target=target)
        result = etree.XML(message, parser)
        self.response.set_value("model_object", result)
        return result
    
    def _serialize_node(
        self, node: Node, tag_name: str, level=0
    ) -> Union[str, Element]:
        """the body of the serialization function recursively serializes each node class

        Args:
            node (Node): the root node class to be serialized
            tag_name (str): the name of the root node class to be serialized
            level (int, optional): _description_. Defaults to 0.

        Returns:
            Union[str, Element]: the original call to this method returns a string representing the xml
                the Element is only returned in the case of recursive calls
        """
        if node.extended:
            xml = etree.fromstring(xmltodict.unparse(node.extended))
        else:
            xml = etree.Element(tag_name)

        # handles text data within tag
        if hasattr(node, "text"):
            xml.text = str(node.text)

        for attribName in node.get_properties():
            # below line is required because get_all_properties function returns only cot property names
            value = getattr(node, attribName)
            if hasattr(value, "__dict__"):
                tagElement = self._serialize_node(
                    value, attribName, level=level + 1)
                # TODO: modify so double underscores are handled differently
                try:
                    if attribName[0] == "_":
                        tagElement.tag = "_" + tagElement.tag
                        xml.append(tagElement)
                except:
                    pass
                else:
                    xml.append(tagElement)

            elif value == None:
                continue

            elif isinstance(value, list):
                for element in value:
                    tagElement = self._serialize_node(
                        element, attribName, level=level + 1
                    )
                    # TODO: modify so double underscores are handled differently
                    try:
                        if attribName[0] == "_":
                            tagElement.tag = "_" + tagElement.tag
                            xml.append(tagElement)
                    except:
                        pass
                    else:
                        xml.append(tagElement)

            else:
                # TODO: modify so double underscores are handled differently
                # handles instances in which attribute name begins with double underscore
                try:
                    if attribName[0] == "_":
                        xml.attrib["_" + attribName] = value
                except:
                    pass
                else:
                    xml.attrib[attribName] = str(value)
        if hasattr(node, "xml_string"):
            # this method combines the xml object parsed from
            # the model object with the xml_string found in the node
            # directly, giving priority to the xml object parsed from the model object
            xml = self._xml_merge(node.xml_string, xml)
        if level == 0:
            return etree.tostring(xml)
        else:
            return xml

    def _xml_merge(self, a, b):
        """credits: https://gist.github.com/dirkjot/bd25b037b33bba6187e99d76792ceb90
        this function merges two xml etree elements

        Args:
            a (_type_): _description_
            b (_type_): _description_
        """

        def inner(a_parent, b_parent):
            for bchild in b_parent:
                achild = a_parent.xpath("./" + bchild.tag)
                if not achild:
                    a_parent.append(bchild)
                elif bchild.getchildren():
                    inner(achild[0], bchild)

        res = deepcopy(a)
        inner(res, b)
        return res
