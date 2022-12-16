from digitalpy.core.parsing.abstract_format import AbstractFormat
from digitalpy.core.domain.object_id import ObjectId
from digitalpy.core.domain.node import Node
from digitalpy.core.zmanager.request import Request

class HirearchicalFormat(AbstractFormat):
    
    def deserialize_values(self, request: Request):
        return self.deserialize_hirearchy(request)
    
    def deserialize_hirearchy(self, values):
        if self.is_serialized_node(values):
            result = self.deserialize_node(values)
            node = result['node']
            values = result['data']
            values[str(node.get_oid())] = node
        
        else:
            for key, value in values.items():
                if isinstance(value, dict) or isinstance(value, object):
                    result = self.deserialize_hirearchy(value)
                    values[key] = result
                else:
                    values[key] = value
        return values
                        
    def serialize_hierarchy(self, values):
        if self.is_deserialized_node(values):
            values = self.serialize_node(values)
        else:
            if hasattr(values, 'items'):
                for key, value in values.items():
                    if value != None and not (isinstance(value, int) or isinstance(value,str) or isinstance(value, float) or isinstance(value, bool)):
                        result = self.serialize_hierarchy(value)
                        if ObjectId.is_valid(key):
                            values = result
                        else:
                            values[key] = result
                    else:
                        values[key] = value
        return values
    
    def is_serialized_node(self, value):
        return False
    
    def is_deserialized_node(self, value):
        return isinstance(value, Node)
    
    