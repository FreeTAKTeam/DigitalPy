from digitalpy.core.zmanager.request import Request
from digitalpy.core.IAM.IAM_filter_strategy import IAMFilterStrategy
from digitalpy.core.IAM.persistence.user import User


class DefaultFilter(IAMFilterStrategy):
    """ default filter strategy for IAM"""
    def apply_filter(self, request: Request, user: User)-> bool:
        """ default strategy is to always allow users to access resources

        Args:
            request (Request): request to be checked
            user (User): user to be checked

        Returns:
            bool: whether the user can access the resource
        """
        return True
