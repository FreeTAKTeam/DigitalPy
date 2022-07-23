import uuid
import re
from default_persistent_object import DefaultPersistentObject
from load_configuration import Configuration

from persistent_object import PersistentObject
from persistent_object_proxy import PersistentObjectProxy

class Node(DefaultPersistentObject):
    def __init__(self, node_type, configuration: Configuration, model) -> None:
        #super(Node, self).__init__(node_type)
        self._type = ''
        self._id = str(uuid.uuid4())
        self._children: dict[str, Node] = {}
        self._parents: dict[str, Node] = {}
        self._depth = -1
        self._path = ''
        self._relationship_definition = configuration.elements[self.__class__.__name__]
        self._add_relationships(configuration, model)

    def _add_relationships(self, configuration: Configuration, model) -> None:
        for relationship_name, relationship_def in self._relationship_definition.relationships.items():
            child_class = getattr(model, relationship_name)
            child_instance = child_class(configuration, model)
            self.add_child(child_instance)

    def get_first_child(self, child_type, values, properties, use_regex=True):
        children = self.get_children_ex(None, children_type=child_type, values=values, properties=properties, use_regex=use_regex)
        if len(children) > 0:
            return children[0]
        else:
            return None

    def get_children(self):
        return self._children
        # return self.get_relatives('child')

    def get_relations(self, hirearchy_type='all'):
        return self.get_mapper().get_relations(hirearchy_type)

    def get_relatives(self, hirearchy_type):
        relatives = []
        relations = self.get_relations(hirearchy_type)
        for relation in relations:
            cur_relatives = self.parent.get_value(relation.get_other_role())
            if cur_relatives is None:
                continue
            if not isinstance(cur_relatives, list):
                cur_relatives = [cur_relatives]
            for cur_relative in cur_relatives:
                if isinstance(cur_relatives, PersistentObjectProxy):
                    continue
                else:
                    relatives.append(cur_relative) 
                    
    def get_children_ex(self, oid=None, role=None, children_type=None, values=None, properties=None, use_regex=True):
        if role is not None:
            child_roles = self.get_possible_children()
            if self.child_roles[role]:
                raise Exception("No child role defined with name %s" % role)
            nodes = self.parent.get_value(role)
            if not isinstance(nodes,list):
                nodes = [nodes]
            children = []
            for cur_node in nodes:
                if isinstance(cur_node, PersistentObject):
                    children = cur_node
            return self.filter(children, oid, children_type, values, properties, use_regex)
        else:
            return self.filter(self.get_children(), oid, children_type, values, properties, use_regex)

    def get_num_children(self, children_type=None):
        count = 0
        if children_type:
            for child in self._children.values():
                if child.get_type() == children_type:
                    count += 1
            return count
        else:
            return len(self._children)
    
    def add_child(self, child):
        if self.validate_child_addition(child):
            self._children[child.get_id()]=child
            setattr(self, child.__class__.__name__, child)
            child.set_parent(self)
        else:
            raise TypeError('child must be an instance of Node')
    
    def validate_child_addition(self, child):
        if isinstance(child, Node):
            child_type = child.get_type()
            if child_type in self._relationship_definition.relationships:
                relationship_requirements = self._relationship_definition.relationships[child_type]
                children = self.get_children_ex(children_type=child_type)
                if relationship_requirements["max_occurs"] == len(children):
                    return False
            return True
        raise TypeError("children must inherit from type Node")

    def delete_child(self, child_id):
        del self._children[child_id]

    def validate_child_removal(self, child):
        if isinstance(child, Node):
            child_type = child.get_type()
            if child_type in self._relationship_definition:
                relationship_requirements = self._relationship_definition[child_type]
                if relationship_requirements["aggregation"] == "composite":
                    return False
                children = self.get_children_ex(children_type=child_type)
                if relationship_requirements["min_occurs"] == len(children):
                    return False
            return True
        raise TypeError("children must inherit from type Node")

    def update_parent(self, parent, recursive=True):
        if parent in self._parents:
            return None
        else:
            self._parents[parent.get_id()] = parent

    def filter(self, node_list, oid, node_type, values, properties, use_regex):
        return_array = []
        for key, node in node_list.items():
            if isinstance(node, PersistentObject):
                match = True
                # check id
                if oid != None and node.get_oid() != oid:
                    match = False
                # check type
                if node_type != None and node.get_type() != node_type:
                    match = False
                # check properties
                if properties != None and isinstance(properties, dict):
                    for key, value in properties.items():
                        node_property = node.get_property(key)
                        if use_regex and not re.match("/"+value+"/m", node_property):
                            match = False
                            break

                        elif not hasattr(node, key) and not use_regex:
                            match = False
                            break

                # check values
                if values != None and isinstance(values, dict):
                    for key, value in properties.items():
                        node_value = self.get_value(key)
                        if use_regex and not re.match("/"+value+"/m", node_value):
                            match = False
                            break
                if match:
                    return_array.append(node)
        return return_array

    def get_next_sibling(self):
        parent = self.get_parent()
        if parent is not None:
            parent_children = parent.get_children()
            next_sibling = None
            
            for index, child in enumerate(parent_children):
                if child.get_oid() == self._oid and index<len(parent_children)-1:
                    next_sibling = parent_children[index + 1]
                    break

            if next_sibling is not None:
                return next_sibling
            
            return None
    
    def get_previous_sibling(self):
        parent = self.get_parent()
        if parent is not None:
            parent_children = parent.get_children()
            previous_sibling = None
            for index, child in enumerate(parent_children):
                if parent.get_oid() == self._oid and index>0:
                    previous_sibling = parent_children[index-1]
                    break
            if previous_sibling is not None:
                return previous_sibling
            return None

    def get_num_parents(self, parent_type=None):
        count = 0
        
        if parent_type is not None:
            for index, parent in enumerate(self._parents):
                if parent.get_type() == parent_type:
                    count +=1
        
        else:
            count = len(self._parents)
        
        return count
    
    def set_parent(self, parent):
        if isinstance(parent, Node):
            self._parents[parent.get_id()] = parent

    def get_parent(self):
        if len(self._parents) > 0:
            return list(self._parents.values())[0]
        else:
            return None

    def get_first_parent(self, parent_type, values, properties, use_regex=True):
        parents = self.get_parents_ex(None, parent_type, values, properties, use_regex)
        if len(parents) > 0:
            return parents[0]
        else:
            return None

    def get_parents(self):
        return self._parents

    def get_parents_ex(self, oid, type, values, properties, use_regex=True):
        return self.filter(self._parents, oid, type, values, properties, use_regex)

    def get_depth(self):
        self._depth = 0
        parent = self.get_parent()
        while parent is not None and isinstance(parent, Node):
            self._depth += 1
            parent = parent.get_parent()
        return self._depth