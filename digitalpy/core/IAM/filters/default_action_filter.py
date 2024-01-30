from digitalpy.core.zmanager.request import Request
from digitalpy.core.IAM.IAM_action_filter_strategy import IAMActionFilterStrategy
from digitalpy.core.IAM.persistence.user import User


class DefaultActionFilter(IAMActionFilterStrategy):
    """ default filter strategy for IAM"""
    def apply_filter(self, request: 'Request', user: 'User', action_key: 'str')-> bool:
        """ default strategy is to always allow users to access resources

        Args:
            request (Request): request to be checked
            user (User): user to be checked

        Returns:
            bool: whether the user can access the resource
        """
        return True
