from typing import Any, List
from digitalpy.core.persistence.persistence_mapper import PersistenceMapper
from digitalpy.core.persistence.build_depth import BuildDepth
from digitalpy.core.persistence.persistent_object import PersistentObject
from digitalpy.core.translation.message import Message
from digitalpy.core.persistence.persistence_operation import PersistenceOperation
from digitalpy.core.persistence.paging_info import PagingInfo
from digitalpy.core.domain.object_id import ObjectId


class NullMapper(PersistenceMapper):
    """NullMapper acts as there is no mapper."""

    def get_type(self):
        return "NULL_type"

    def begin_transaction(self) -> Any:
        """@see _persistence_mapper.begin_transaction()"""
        pass

    def commit_transaction(self) -> Any:
        """@see _persistence_mapper.commit_transaction()"""
        pass

    def create(self, type: Any, build_depth: Any = BuildDepth.SINGLE) -> Any:
        """@see _persistence_mapper.create()"""
        return PersistentObject(type, build_depth)

    def delete(self, object: PersistentObject) -> Any:
        """@see _persistence_mapper.delete()"""
        pass

    def execute_operation(self, operation: PersistenceOperation) -> Any:
        """@see _persistence_mapper.execute_operation()"""
        return 0

    def get_attribute(self, name: Any) -> Any:
        """@see _persistence_mapper.get_attribute()"""
        pass

    def get_attribute_description(self, name: Any, message: Message) -> Any:
        """@see _persistence_mapper.get_attribute_description()"""
        pass

    def get_attribute_display_name(self, name: Any, message: Message) -> Any:
        """@see _persistence_mapper.get_attribute_display_name()"""
        pass

    def get_attributes(self, tags: List = [], match_mode: Any = "all") -> Any:
        """@see _persistence_mapper.get_attributes()"""
        return []

    def get_default_order(self, role_name: Any = None) -> Any:
        """@see _persistence_mapper.get_default_order()"""
        pass

    def get_OIDs(
        self,
        type: Any,
        criteria: Any = None,
        orderby: Any = None,
        paging_info: PagingInfo = None,
    ) -> Any:
        """@see _persistence_facade.get_oI_ds()"""
        return []

    def get_pk_names(self) -> Any:
        """@see _persistence_mapper.get_pk_names()"""
        return []

    def get_properties(self) -> Any:
        """@see _persistence_mapper.get_properties()"""
        pass

    def get_references(self) -> Any:
        """@see _persistence_mapper.get_references()"""
        pass

    def get_relation(self, role_name: Any) -> Any:
        """@see _persistence_mapper.get_relation()"""
        pass

    def get_relations(self, hierarchy_type: Any = "all") -> Any:
        """@see _persistence_mapper.get_relations()"""
        return []

    def get_relations_by_type(self, type: Any) -> Any:
        """@see _persistence_mapper.get_relations_by_type()"""
        pass

    def get_sortkey(self, role_name: Any = None) -> Any:
        """@see _persistence_mapper.get_sortkey()"""
        pass

    def get_statements(self) -> Any:
        """@see _persistence_mapper.get_statements()"""
        pass

    def get_type_description(self, message: Message) -> Any:
        """@see _persistence_mapper.get_type_description()"""
        pass

    def get_type_display_name(self, message: Message) -> Any:
        """@see _persistence_mapper.get_type_display_name()"""
        pass

    def has_attribute(self, name: Any) -> Any:
        """@see _persistence_mapper.has_attribute()"""
        return False

    def has_relation(self, role_name: Any) -> Any:
        """@see _persistence_mapper.has_relation()"""
        pass

    def is_sortable(self, role_name: Any = None) -> Any:
        """@see _persistence_mapper.is_sortable()"""
        pass

    def load(self, oid: ObjectId, build_depth: Any = BuildDepth.SINGLE) -> Any:
        """@see _persistence_mapper.load()"""
        pass

    def load_objects(
        self,
        type: Any,
        build_depth: Any = BuildDepth.SINGLE,
        criteria: Any = None,
        orderby: Any = None,
        paging_info: PagingInfo = None,
    ) -> Any:
        """@see _persistence_facade.load_objects()"""
        pass

    def load_relation(
        self,
        objects: List,
        role: Any,
        build_depth: Any = BuildDepth.SINGLE,
        criteria: Any = None,
        orderby: Any = None,
        paging_info: PagingInfo = None,
    ) -> Any:
        """@see _persistence_mapper.load_relation()"""
        pass

    def rollback_transaction(self) -> Any:
        """@see _persistence_mapper.rollback_transaction()"""
        pass

    def save(self, object: PersistentObject) -> Any:
        """@see _persistence_mapper.save()"""
        pass
