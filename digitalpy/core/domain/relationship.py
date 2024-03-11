"""this module defines a decorator to create a relationship between two entities, this will act similarly to the property decorator in python except
that it will allow the definition of uml properties in the relationship such as multiplicity and type, these properties will be used to define runtime
validation of the relationship
"""
from enum import Enum
import functools

class RelationshipType(Enum):
    """this class is used to define the type of a relationship, it is an enumeration of the possible relationship
    types
    """
    AGGREGATION = "aggregation"
    COMPOSITION = "composition"
    ASSOCIATION = "association"

class Relationship:
    """
    A decorator class that represents a relationship between two entities. This class is used as a 
    decorator to define the getter, setter, and deleter for the relationship.
    """
    def __init__(self, fget=None, fset=None, fdel=None, multiplicity_upper: int=1, multiplicity_lower: int=0, reltype: str = RelationshipType.ASSOCIATION):
        if type not in RelationshipType:
            raise ValueError("invalid relationship type")
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.multiplicity_lower = multiplicity_lower
        self.multiplicity_upper = multiplicity_upper
        self.type = reltype
        if fget is not None:
            functools.update_wrapper(self, fget)

    def __get__(self, obj, objtype=None):
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        return self.fget(obj)
    
    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        
        obj_more_than_one = isinstance(obj, str) or not hasattr(obj, '__len__')

        if self.multiplicity_lower>1 and obj_more_than_one:
            raise ValueError(f"This property has a lower multiplicity of {self.multiplicity_lower}")
        
        if obj_more_than_one and len(obj)<self.multiplicity_upper:
            raise ValueError(f"This property has an upper multiplicity of {self.multiplicity_upper}")

        self.fset(obj, value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(obj)

    def getter(self, fget=None):
        return type(self)(fget=fget, fset=self.fset, fdel=self.fdel, multiplicity_upper=self.multiplicity_upper, multiplicity_lower=self.multiplicity_lower, reltype=self.type)

    def setter(self, fset=None):
        return type(self)(fget=self.fget, fset=fset, fdel=self.fdel, multiplicity_upper=self.multiplicity_upper, multiplicity_lower=self.multiplicity_lower, reltype=self.type)

    def deleter(self, fdel=None):
        return type(self)(fget=self.fget, fset=self.fset, fdel=fdel, multiplicity_upper=self.multiplicity_upper, multiplicity_lower=self.multiplicity_lower, reltype=self.type)
    
    def __call__(self, func):
        if not self.fget:
            self.fget = func
        elif not self.fset:
            self.fset = func
        elif not self.fdel:
            self.fdel = func
        return self
