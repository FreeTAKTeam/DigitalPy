from abc import abstractmethod, ABC


class Factory(ABC):
    
    @abstractmethod
    def get_instance(self, name, dynamic_configuration={}) -> object:
        raise NotImplementedError