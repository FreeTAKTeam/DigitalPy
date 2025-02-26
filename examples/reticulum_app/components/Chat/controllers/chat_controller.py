"""
This is the main controller class of the application. Every operation of the controller is realized by this file
OOTB. It is recommended that you (the developper) avoid adding further methods to the file and instead add supporting
controllers with these methods should you need them. This controller is called directly by the facade in order to
fulfil any requests made to the component by default.
"""

from typing import TYPE_CHECKING

from digitalpy.core.main.controller import Controller

if TYPE_CHECKING:
    from digitalpy.core.digipy_configuration.domain.model.configuration import Configuration
    from digitalpy.core.zmanager.impl.default_action_mapper import DefaultActionMapper
    from digitalpy.core.zmanager.request import Request
    from digitalpy.core.zmanager.response import Response
    from digitalpy.core.domain.domain.network_client import NetworkClient

class ChatController(Controller):

    def __init__(self, request: 'Request',
                 response: 'Response',
                 sync_action_mapper: 'DefaultActionMapper',
                 configuration: 'Configuration'):
        super().__init__(request, response, sync_action_mapper, configuration)

    def initialize(self, request: 'Request', response: 'Response'):
        """This function is used to initialize the controller. 
        It is intiated by the service manager."""
        return super().initialize(request, response)
    
    def Chat(self, body: str, client: 'NetworkClient', *args, **kwargs):
        """This function is used to handle the Chat action."""
        self.response.set_value("client", None) # ensure the client is set to None so broadcast can be used
        self.response.set_value("message", body)
        return self.response