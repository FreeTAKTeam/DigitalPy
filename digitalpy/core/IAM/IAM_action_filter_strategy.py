from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from digitalpy.core.IAM.persistence.user import User
    from digitalpy.core.zmanager.request import Request


class IAMActionFilterStrategy(ABC):

    @abstractmethod
    def apply_filter(self, request: 'Request', user: 'User', action_key: 'str') -> 'bool':
        """ apply filter to request and user to check if the user can access the resource

        Args:
            request (Request): the request to be checked
            user (User): the user to be checked
            action_key (str): the action key to be checked

        Returns:
            bool: True if the user can access the resource or if the filter is inapplicable to the request, 
            False otherwise
        """

    def _user_has_permission(self, user: 'User', permission_id: 'str') -> 'bool':
        """ check if the user has the permission
        
        Args:
            user (User): the user to be checked
            permission (str): the permission to be checked
        
        Returns:
            bool: True if the user has the permission, False otherwise
        """
        user_has_permissions = user is not None and user.system_user is not None and len(user.system_user.system_user_groups) > 0
        if user_has_permissions:
            for group in user.system_user.system_user_groups:
                for group_permission in group.system_group.system_group_permissions:
                    if group_permission.permission.PermissionID == permission_id:
                        return True        
        else:
            return False