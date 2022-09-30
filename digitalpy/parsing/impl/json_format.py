from digitalpy.parsing.impl.hierarchical_format import HirearchicalFormat


class JsonFormat(HirearchicalFormat):
    
    def __init__(self, serializer: NodeSerializer):
        self.serializer = serializer
        
    def after_serialize(self, response: Response):
        return super().after_serialize(response)
    
    def is_serialized_node(self, value):
        return self.serializer.is_serialized_node(value)
        
    def serialize_node(self, value):
        node = self.serializer.serialize_node(value)
        return node
    
    def deserialize_node(self, value):
        result = self.serializer.deserialize_node(value)
        return result