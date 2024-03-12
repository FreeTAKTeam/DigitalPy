from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from digitalpy.core.zmanager.request import Request

if TYPE_CHECKING:
    from digitalpy.core.IAM.persistence.user import User

class IAMRecipientFilterStrategy(ABC):

    @abstractmethod
    def apply_filter(self, request: Request, user: 'User') -> bool:
        """ apply filter to request and user to check if the user can access the resource

        Args:
            request (Request): the request to be checked
            user (User): the user to be checked

        Returns:
            bool: True if the user can access the resource or if the filter is inapplicable to the request, 
            False otherwise
        """