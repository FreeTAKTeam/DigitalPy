from typing import TYPE_CHECKING
from digitalpy.core.IAM.IAM_filter_strategy import IAMFilterStrategy
from digitalpy.core.IAM.persistence.user import User

from digitalpy.core.main.controller import Controller

if TYPE_CHECKING:
    from digitalpy.core.zmanager.request import Request
    from digitalpy.core.zmanager.response import Response
    from digitalpy.core.digipy_configuration.configuration import Configuration
    from digitalpy.core.zmanager.action_mapper import ActionMapper


class IAMFilterController(Controller):

    def __init__(
        self,
        request: 'Request',
        response: 'Response',
        sync_action_mapper: 'ActionMapper',
        configuration: 'Configuration',
        iam_filter_strategy: 'IAMFilterStrategy',
    ):
        super().__init__(request, response, sync_action_mapper, configuration)
        self.iam_filter_strategy = iam_filter_strategy

    def initialize(self, request: 'Request', response: 'Response'):
        super().initialize(request, response)

    def filter_recipients(self, recipients: list[User], *args, **kwargs) -> list[User]:
        """ filter the recipients based on the request and the filter strategy

        Args:
            recipients (list[User]): the list of recipients to be filtered

        Returns:
            list[User]: the list of recipients after the filtering
        """
        filtered_recipients = []
        for recipient in recipients:
            if self.iam_filter_strategy.apply_filter(self.request, recipient):
                filtered_recipients.append(recipient)
        self.response.set_value("connections", filtered_recipients)
        return filtered_recipients
