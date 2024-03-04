"""this module defines a decorator to create a relationship between two entities, this will act similarly to the property decorator in python except
that it will allow the definition of uml properties in the relationship such as multiplicity and type, these properties will be used to define runtime
validation of the relationship
"""
from enum import Enum
import functools

class Multiplicity(Enum):
    """this class is used to define the multiplicity of a relationship, it is an enumeration of the possible multiplicity values
    """
    ONE = "1"
    ZERO_TO_ONE = "0..1"
    ZERO_TO_MANY = "0..*"
    ONE_TO_MANY = "1..*"

class RelationshipType(Enum):
    """this class is used to define the type of a relationship, it is an enumeration of the possible relationship
    types
    """
    AGGREGATION = "aggregation"
    COMPOSITION = "composition"
    ASSOCIATION = "association"

class Relationship:
    """this class is used to define a relationship between two entities, this will act similarly to the property decorator in python except
    that it will allow the definition of uml properties in the relationship such as multiplicity and type, these properties will be used to define runtime
    validation of the relationship
    """
    def __init__(self, f, multiplicity: str = Multiplicity.ZERO_TO_ONE, type: str = RelationshipType.ASSOCIATION):
        if multiplicity not in Multiplicity:
            raise ValueError("invalid multiplicity")
        if type not in RelationshipType:
            raise ValueError("invalid relationship type")
        functools.update_wrapper(self, f)
        self.multiplicity = multiplicity
        self.type = type
        
    def __call__(self, f, *args, **kwargs):
        