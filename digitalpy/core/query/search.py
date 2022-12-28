import typing

class Search:
    def check(self, word: str) -> Union[bool, str]:
        pass

    def find(self, searchTerm: str, pagingInfo: Optional[PagingInfo]=None, createSummary: bool=True) -> Dict[int, Dict[str, Union[int, str]]]:
        pass

    def isSearchable(self, obj: PersistentObject) -> bool:
        pass
