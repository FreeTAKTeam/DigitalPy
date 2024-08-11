# pylint: disable=invalid-name
from digitalpy.core.digipy_configuration.action_key import ActionKey
from digitalpy.core.domain.node import Node

# iterating associations


class ActionFlow(Node):
    """An ActionFlow is a sequence of actions that are executed in a specific order.
    
    An action flow is distinguished by a section with the following structure:
    [ConfigIni]
    Sender?Ctx@Decorator?Action
    
    """

    def __init__(
        self, model_configuration, model, oid=None, node_type="ActionKey"
    ) -> None:
        super().__init__(
            node_type, model_configuration=model_configuration, model=model, oid=oid
        )
        self._actions: list[ActionKey] = []
        self._config_id: str = ""

    @property
    def actions(self) -> list[ActionKey]:
        """The actions that are executed in a specific order."""
        return self._actions
    
    @actions.setter
    def actions(self, actions: list[ActionKey]):
        actions = list(actions)
        if not isinstance(actions, list):
            raise TypeError("'actions' must be of type list")
        self._actions = actions

    @property
    def config_id(self) -> str:
        """The configuration id of the action flow."""
        return self._config_id
    
    @config_id.setter
    def config_id(self, config_id: str):
        if not isinstance(config_id, str):
            raise TypeError("'config_id' must be of type str")
        self._config_id = config_id
