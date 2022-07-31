from model.node import Node
import load_configuration
from emergency_RI.constants import CONFIGURATION_PATH_TEMPLATE
from emergency_RI import model
class Domain:
    def __init__(self):
        self.config_loader = load_configuration.LoadConfiguration(CONFIGURATION_PATH_TEMPLATE)

    def create_child(self, child_type: str):
        return FACTORY_MAPPING[child_type]().build()

    def accept_visitor(self, node: Node, visitor):
        return node.accept_visitor(visitor)
    
    def add_child(self, node: Node, child):
        return node.add_child(child)

    def create_node(self, message_type, object_class_name):
        configuration = self.config_loader.find_configuration(message_type)
        object_class = getattr(model, object_class_name)
        object_class_instance = object_class(configuration, model)
        return object_class_instance
        
    def delete_child(self, node: Node, child_id):
        return node.delete_child(child_id)

    def get_children_ex(id, node: Node, children_type, values, properties, use_regex=True):
        return node.get_children_ex(id, node, children_type, values, properties, use_regex)
        
    def get_first_child(self, node: Node, child_type, values, properties, use_regex=True):
        return node.get_first_child(child_type, values, properties, use_regex)
    
    def get_next_sibling(self, node):
        return node.get_next_sibling()

    def get_num_children(self, node: Node, children_type = None):
        return node.get_num_children(children_type)
    
    def get_num_parents(self, node: Node, parent_types = None):
        return node.get_num_parents(parent_types)
    
    def get_previous_sibling(self, node: Node):
        return node.get_previous_sibling()
    
    def get_parent(self, node: Node):
        return node.get_parent()