# pylint: disable=invalid-name
from digitalpy.core.domain.node import Node

# iterating associations


class ActionKey(Node):
    """An ActionKey is a key that is used to trigger an action. It is a part of the
    system that can be"""

    def __init__(
        self, model_configuration, model, oid=None, node_type="ActionKey"
    ) -> None:
        super().__init__(
            node_type, model_configuration=model_configuration, model=model, oid=oid
        )
        self._action: "str" = ""
        self._context: "str" = ""
        self._decorator: "str" = ""
        self._config: "str" = ""
        self._target: "str" = ""
        self._source: "str" = ""
        self._referencedBehaviour: "str" = ""
        self._name: "str" = ""

    @property
    def action(self) -> "str":
        """The action, which is triggered. If empty, any action is valid"""
        return self._action

    @action.setter
    def action(self, action: "str"):
        action = str(action)
        if not isinstance(action, str):
            raise TypeError("'action' must be of type str")
        self._action = action

    @property
    def context(self) -> "str":
        """The context, in which this association is valid. If empty, any context is valid."""
        return self._context

    @context.setter
    def context(self, context: "str"):
        context = str(context)
        if not isinstance(context, str):
            raise TypeError("'context' must be of type str")
        self._context = context

    @property
    def decorator(self) -> "str":
        """Optional, Allows to dynamically attach special behaviors to the result operation without changing his implementation
        . e.g. a decorator REST, will expose this action as a REST service. (e.g. REST, Pub, Sub, All, etc)
        """
        return self._decorator

    @decorator.setter
    def decorator(self, decorator: "str"):
        decorator = str(decorator)
        if not isinstance(decorator, str):
            raise TypeError("'decorator' must be of type str")
        self._decorator = decorator

    @property
    def config(self) -> "str":
        """The configuration, or configuration section in which this Action is defined"""
        return self._config

    @config.setter
    def config(self, config: "str"):
        config = str(config)
        if not isinstance(config, str):
            raise TypeError("'config' must be of type str")
        self._config = config

    @property
    def target(self) -> "str":
        """the qualified name of the target of the action, this can also include the method name"""
        return self._target

    @target.setter
    def target(self, target: "str"):
        target = str(target)
        if not isinstance(target, str):
            raise TypeError("'target' must be of type str")
        self._target = target

    @property
    def source(self) -> "str":
        """the qualified name of the originator of the action"""
        return self._source

    @source.setter
    def source(self, source: "str"):
        source = str(source)
        if not isinstance(source, str):
            raise TypeError("'source' must be of type str")
        self._source = source

    @property
    def referencedBehaviour(self) -> "str":
        """optional, the name of the target function, to be attached to the qualified
        name of the target."""
        return self._referencedBehaviour

    @referencedBehaviour.setter
    def referencedBehaviour(self, referencedBehaviour: "str"):
        referencedBehaviour = str(referencedBehaviour)
        if not isinstance(referencedBehaviour, str):
            raise TypeError("'referencedBehaviour' must be of type str")
        self._referencedBehaviour = referencedBehaviour

    @property
    def name(self) -> "str":
        """the name of the action key"""
        return self._name

    @name.setter
    def name(self, name: "str"):
        name = str(name)
        if not isinstance(name, str):
            raise TypeError("'name' must be of type str")
        self._name = name

    def __eq__(self, value: object) -> bool:
        """Check if the given value is equal to this ActionKey, by comparing the action, context, decorator, and source.
        The target and referencedBehaviour are not considered in the comparison. The matching only fails if
        two set values are not equal. If the value is not an ActionKey, the default equality check is used.
        Example:
        ActionKey:
            action: "action"
            context: "context"
            decorator: "decorator"
            source: "source"
        ActionKey2:
            action: "action2"
            context: "context"
            decorator: "decorator"
            source: "source"
        ActionKey == ActionKey2 -> False

        ActionKey:
            action: "action"
            context: "context"
            decorator: "decorator"
            source: "source"
        ActionKey2:
            action: NULL
            context: "context"
            decorator: "decorator"
            source: "source"
        ActionKey == ActionKey2 -> True
        """
        if isinstance(value, ActionKey):
            return (
                (value.action == self.action or not value.action or not self.action)
                and (
                    value.context == self.context
                    or not value.context
                    or not self.context
                )
                and (
                    value.decorator == self.decorator
                    or not value.decorator
                    or not self.decorator
                )
                and (value.source == self.source or not value.source or not self.source)
            )
        else:
            return super().__eq__(value)

    def __str__(self) -> str:
        return f"ActionKey(name={self._name}, action={self._action}, context={self._context}, decorator={self._decorator}, config={self._config}, target={self._target}, source={self._source}, referencedBehaviour={self._referencedBehaviour})"
