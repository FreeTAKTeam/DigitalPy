# pylint: disable=invalid-name
from digitalpy.core.domain.node import Node

# iterating associations

class ActionKey(Node):
    """An ActionKey is a key that is used to trigger an action. It is a part of the system that can be"""
    def __init__(self, model_configuration, model, oid=None, node_type="ActionKey") -> None:
        super().__init__(node_type, model_configuration=model_configuration, model=model, oid=oid)
        self._action: 'str' = None
        self._context: 'str' = None
        self._decorator: 'str' = None
        self._config: 'str' = None
        self._target: 'str' = None
        self._source: 'str' = None
        self._referencedBehaviour: 'str' = None
        self._name: 'str' = None

    @property
    def action(self) -> 'str':
        """The action, which is triggered. If empty, any action is valid"""
        return self._action

    @action.setter
    def action(self, action: 'str'):
        action = str(action)
        if not isinstance(action, str):
            raise TypeError("'action' must be of type str")
        self._action= action

    @property
    def context(self) -> 'str':
        """The context, in which this association is valid. If empty, any context is valid. """
        return self._context

    @context.setter
    def context(self, context: 'str'):
        context = str(context)
        if not isinstance(context, str):
            raise TypeError("'context' must be of type str")
        self._context= context

    @property
    def decorator(self) -> 'str':
        """Optional, Allows to dynamically attach special behaviors to the result operation without changing his implementation
        . e.g. a decorator REST, will expose this action as a REST service. (e.g. REST, Pub, Sub, All, etc)"""
        return self._decorator

    @decorator.setter
    def decorator(self, decorator: 'str'):
        decorator = str(decorator)
        if not isinstance(decorator, str):
            raise TypeError("'decorator' must be of type str")
        self._decorator= decorator

    @property
    def config(self) -> 'str':
        """The configuration, or configuration section in which this Action is defined"""
        return self._config

    @config.setter
    def config(self, config: 'str'):
        config = str(config)
        if not isinstance(config, str):
            raise TypeError("'config' must be of type str")
        self._config= config

    @property
    def target(self) -> 'str':
        """the qualified name of the target of the action, this can also include the method name"""
        return self._target

    @target.setter
    def target(self, target: 'str'):
        target = str(target)
        if not isinstance(target, str):
            raise TypeError("'target' must be of type str")
        self._target= target

    @property
    def source(self) -> 'str':
        """the qualified name of the originator of the action"""
        return self._source

    @source.setter
    def source(self, source: 'str'):
        source = str(source)
        if not isinstance(source, str):
            raise TypeError("'source' must be of type str")
        self._source= source

    @property
    def referencedBehaviour(self) -> 'str':
        """optional, the name of the target function, to be attached to the qualified 
        name of the target."""
        return self._referencedBehaviour

    @referencedBehaviour.setter
    def referencedBehaviour(self, referencedBehaviour: 'str'):
        referencedBehaviour = str(referencedBehaviour)
        if not isinstance(referencedBehaviour, str):
            raise TypeError("'referencedBehaviour' must be of type str")
        self._referencedBehaviour= referencedBehaviour

    @property
    def name(self) -> 'str':
        """the name of the action key"""
        return self._name

    @name.setter
    def name(self, name: 'str'):
        name = str(name)
        if not isinstance(name, str):
            raise TypeError("'name' must be of type str")
        self._name= name
