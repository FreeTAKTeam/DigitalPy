# pylint: disable=invalid-name

from digitalpy.core.zmanager.configuration.zmanager_constants import TopicCategory
from digitalpy.core.domain.node import Node

from digitalpy.core.zmanager.configuration.zmanager_constants import ZMANAGER_MESSAGE_DELIMITER
# iterating associations

class Topic(Node):
    def __init__(self, model_configuration, model, oid=None, node_type="Topic") -> None:
        super().__init__(node_type, model_configuration=model_configuration, model=model, oid=oid)
        self._category: TopicCategory = None
        self._protocol: str = None
        self._extension: list[str] = None

    @property
    def category(self) -> 'TopicCategory':
        """The category of the topic."""
        return self._category
    
    @category.setter
    def category(self, category: 'TopicCategory'):
        category = TopicCategory(category)
        if not isinstance(category, TopicCategory):
            raise TypeError("'category' must be of type str")
        self._category = category

    @property
    def protocol(self) -> 'str':
        """The protocol of the topic."""
        return self._protocol
    
    @protocol.setter
    def protocol(self, protocol: 'str'):
        protocol = str(protocol)
        if not isinstance(protocol, str):
            raise TypeError("'protocol' must be of type str")
        self._protocol = protocol

    @property
    def extension(self) -> list[str]:
        """The extension of the topic."""
        return self._extension
    
    @extension.setter
    def extension(self, extension: list[str]):
        self._extension = extension

    def build_topic_string(self) -> str:
        """Builds a list of strings that represent every level of the topic extensions."""
        return ZMANAGER_MESSAGE_DELIMITER.join([self.category, self.protocol, *self.extension])
