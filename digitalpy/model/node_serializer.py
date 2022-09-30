from abc import ABC, abstractmethod

class NodeSerializer(ABC):
    
    @abstractmethod
    def is_serialized_node(self, data):
        """check if the given data represents a serialized node"""
        
    @abstractmethod
    def deserialize_node(data, parent: Node = None, role=None):
        """Deserialize a Node from serialized data. Only values given in data are being set."""
        
    @abstractmethod
    def serialize_node(self, node):
        """serialize a node into an array"""
        
    