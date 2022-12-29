from abc import ABC, abstractmethod
from digitalpy.core.persistence.ObjectId import ObjectId

class IndexedSearch(ABC):
    @abstractmethod
    def check(self, word: str) -> bool:
        pass
    
    @abstractmethod
    def find(self, searchTerm: str, pagingInfo: 'PagingInfo'=None, createSummary: bool=True) -> dict:
        pass
    
    @abstractmethod
    def isSearchable(self, obj: 'PersistentObject') -> bool:
        pass
    
    @abstractmethod
    def resetIndex(self):
        pass
    
    @abstractmethod
    def addToIndex(self, obj: 'PersistentObject'):
        pass
    
    @abstractmethod
    def deleteFromIndex(self, oid: ObjectId):
        pass
    
    @abstractmethod
    def commitIndex(self, optimize: bool=True):
        pass
    
    @abstractmethod
    def optimizeIndex(self):
        pass

