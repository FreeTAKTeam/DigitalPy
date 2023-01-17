from typing import List, Dict
import inspect
from sqlalchemy.orm import registry, relationship, mapper
from sqlalchemy import Column, Integer, String, DateTime, Table, ForeignKey

from digitalpy.core.persistence.impl.null_mapper import NullMapper
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.domain.object_id import ObjectId
from digitalpy.core.persistence.persistent_object import PersistentObject
from digitalpy.core.persistence.property_change_event import PropertyChangeEvent
from digitalpy.core.persistence.value_change_event import ValueChangeEvent

#// 
#// DefaultPersistentObject is the base class of all persistent objects.
#// It mainly implements an unique identifier for each instance (ObjectId),
#// tracking of the persistent state, methods for setting and getting values
#// as well as callback methods for lifecycle events.
#// 
#// @author ingo herwig <ingo@wemove.com>
#//
class SQLAlchemyPersistentObject(PersistentObject):
    __mapped = False

    def __new__(cls, *args, **kwargs):
        reg = None
        for arg in args:
            if isinstance(arg, registry):
                reg = arg

        if reg == None:
            reg = kwargs.get("registry", None)
        if reg != None:
            if cls.__mapped == False and cls.__name__ not in reg.metadata.tables:

            
                columns = []
                properties: Dict[str, property] = {name: value.fset for name, value in vars(cls).items() if isinstance(value, property)}

                # create a default primary key as the OID to adhere to the principle of convention
                # instead of configuration
                columns.append(Column("oid", String(100), primary_key=True))
                relations = {}
                
                # TODO expand types and change the 100 default to a more sustainable configurable system
                type_column_mapping = {
                    "str": String(100),
                    "int": Integer,
                    "datetime.datetime": DateTime,
                    None: String(100)
                }

                for attr, attr_setter in properties.items():
                    # retrieve the attribute type from the type hint of the property setter
                    # NOTE: this assumes that all attributes to be turned into columns in the
                    # DB are defined as type hinted property's
                    attr_type = str(inspect.signature(attr_setter)).split(":", 1)
                    # handle case where no second attribute is present
                    if len(attr_type)>=2:
                        attr_type = attr_type[-1]
                    else:
                        continue
                    # remove potential leading 0s
                    attr_type = attr_type.strip()
                    attr_type = attr_type.split(" ")[0]
                    attr_type = attr_type.split("=")[0]
                    attr_type = attr_type.strip(")")
                    
                    columns.append(Column("__"+attr, type_column_mapping[attr_type]))

                #for child in children.values():
                #    relations[child.get_type()] = relationship(child.__class__.__name__, back_populates=self.__type)
                #for parent in parents:
                #    attributes.append(Column(String, ForeignKey(parent.get_type()+".oid")))
                persistency_table = Table(cls.__name__, reg.metadata, *columns)
                reg.map_imperatively(cls, persistency_table, properties=relations)
                cls.__mapped = True
        return super().__new__(cls)

    def __init__(self, oid: ObjectId = None, registry: registry = None, attributes: dict =None) -> None:
        if oid is None or not ObjectId.is_valid(oid):
            oid = ObjectId.NULL_OID()
        self.__type = oid.get_type()
        self._oid = oid
        if oid.contains_dummy_ids():
            self.state = SQLAlchemyPersistentObject.STATE_NEW
        else:
            self.state = SQLAlchemyPersistentObject.STATE_CLEAN
        self.attributes = attributes

    def set_value_internal(self, name, value):
        """Internal (fast) version to set a value without any validation, state change,
        listener notification etc."""
        self.attributes[name] = value

    def set_oid(self, oid):
        self._oid = oid

    def get_oid(self):
        return self._oid

    def __getstate__(self):
        d = self.__dict__.copy()
        d.pop('_parents', None)
        return d