from email import message

from attr import has
from emergency_RI.controller.domain.main import Domain
from node import Node

def test_create_node():
    node = Domain().create_node(message_type='emergency', object_class_name='Event')
    assert isinstance(node, Node)
    assert node.__class__.__name__ == 'Event'
    assert hasattr(node, 'Detail') == True
    assert hasattr(node, 'Point') == True
    assert hasattr(node.Detail, 'Emergency') == True