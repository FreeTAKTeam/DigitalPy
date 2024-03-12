from typing import TYPE_CHECKING

from digitalpy.core.main.controller import Controller

if TYPE_CHECKING:
    from digitalpy.core.IAM.persistence.user import User
    from digitalpy.core.zmanager.request import Request
    from digitalpy.core.zmanager.response import Response
    from digitalpy.core.digipy_configuration.configuration import Configuration
    from digitalpy.core.zmanager.action_mapper import ActionMapper
    from digitalpy.core.IAM.IAM_recipient_filter_strategy import IAMRecipientFilterStrategy
    from digitalpy.core.IAM.IAM_action_filter_strategy import IAMActionFilterStrategy


class IAMFilterController(Controller):

    def __init__(
        self,
        request: 'Request',
        response: 'Response',
        sync_action_mapper: 'ActionMapper',
        configuration: 'Configuration',
        iam_recipient_filter_strategy: 'IAMRecipientFilterStrategy',
        iam_action_filter_strategy: 'IAMActionFilterStrategy'
    ):
        super().__init__(request, response, sync_action_mapper, configuration)
        self.iam_recipient_filter_strategy = iam_recipient_filter_strategy
        self.iam_action_filter_strategy = iam_action_filter_strategy

    def initialize(self, request: 'Request', response: 'Response'):
        super().initialize(request, response)

    def filter_recipients(self, recipients: list['User'], *args, **kwargs) -> list['User']:
        """ filter the recipients based on the request and the filter strategy

        Args:
            recipients (list[User]): the list of recipients to be filtered

        Returns:
            list[User]: the list of recipients after the filtering
        """
        filtered_recipients = [
                                recipients[i]
                                for i in range(len(recipients))
                                if self.iam_recipient_filter_strategy.apply_filter(self.request, recipients[i])
                               ]
        self.response.set_value("connections", filtered_recipients)
        return filtered_recipients

    def filter_action(self, user: 'User', request: 'Request', action_key: str, *args, **kwargs) -> bool:
        """filter the actions based on the request and the filter strategy

        Args:
            user (User): the user to be filtered
            request (Request): the request to be filtered
            action_key (str): the action key to be filtered

        Returns:
            bool: True if the action is allowed, False otherwise
        """
        return self.iam_action_filter_strategy.apply_filter(request, user, action_key)