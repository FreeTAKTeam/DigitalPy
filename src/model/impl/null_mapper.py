from model.persistence_mapper import PersistenceMapper


class NullMapper(PersistenceMapper):
    def get_type(self):
        return 'NULLType'