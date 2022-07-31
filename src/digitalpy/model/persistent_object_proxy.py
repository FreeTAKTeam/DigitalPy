from digitalpy.model.persistent_object import PersistentObject


class PersistentObjectProxy(PersistentObject):
    _id = None
    _realSubject = None

    def __init__(self, id):
        self._id = id