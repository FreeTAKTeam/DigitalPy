from email import message

from attr import has
from emergency_RI.controller.domain.main import Domain
from emergency_RI.controller.parser import parse_xml_to_model
from node import Node

def test_create_node():
    node = Domain().create_node(message_type='emergency', object_class_name='Event')
    assert isinstance(node, Node)
    assert node.__class__.__name__ == 'Event'
    assert hasattr(node, 'detail') == True
    assert hasattr(node, 'point') == True
    assert hasattr(node.detail, 'emergency') == True

def test_parse_xml_to_node():
    xml_string = '<event version="2.0" uid="test-emergency" type="b-a-o-tbl" how="h-e" start="2021-06-22T16:21:21.51Z" time="2021-07-25T20:23:20.294008Z" stale="2021-07-25T20:24:20.294025Z"><detail><link uid="SERVER" relation="p-p" production_time="2021-07-25T20:24:20Z" type="a-f-G-U-C" /><contact /><emergency /></detail><point le="9999999" ce="9999999" hae="9999999" lon="-107.725503268152" lat="42.324772908865" /></event>'
    node = parse_xml_to_model(xml_string)
    assert isinstance(node, Node)
    assert node.__class__.__name__ == 'Event'
    assert hasattr(node, 'detail') == True
    assert hasattr(node, 'point') == True
    assert hasattr(node.detail, 'emergency') == True