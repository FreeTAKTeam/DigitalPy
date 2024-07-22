# pylint: disable=invalid-name
from digitalpy.core.domain.node import Node
from digitalpy.core.domain.relationship import Relationship, RelationshipType

from typing import TYPE_CHECKING
# iterating associations

class Component(Node):
    """"""
    def __init__(self, model_configuration, model, oid=None, node_type="Component") -> None:
        super().__init__(node_type, model_configuration=model_configuration, model=model, oid=oid)
        self._author: 'str' = None
        self._author_email: 'str' = None
        self._description: 'str' = None
        self._License: 'str' = None
        self._repo: 'str' = None
        self._requiredAlfaVersion: 'str' = None
        self._URL: 'str' = None
        self._Version: 'str' = None
        self._UUID: 'str' = None
        self._isActive: 'str' = None
        self._isInstalled: 'str' = None
        self._installationPath: 'str' = None
        self._name: 'str' = None

    @property
    def author(self) -> 'str':
        """The name of the author of this component."""
        return self._author

    @author.setter
    def author(self, author: 'str'):
        author = str(author)
        if not isinstance(author, str):
            raise TypeError("'author' must be of type str")
        self._author= author

    @property
    def author_email(self) -> 'str':
        """The email address of the author."""
        return self._author_email

    @author_email.setter
    def author_email(self, author_email: 'str'):
        author_email = str(author_email)
        if not isinstance(author_email, str):
            raise TypeError("'author_email' must be of type str")
        self._author_email= author_email

    @property
    def description(self) -> 'str':
        """A detailed description of the component."""
        return self._description

    @description.setter
    def description(self, description: 'str'):
        description = str(description)
        if not isinstance(description, str):
            raise TypeError("'description' must be of type str")
        self._description= description

    @property
    def License(self) -> 'str':
        """the type of license for this component"""
        return self._License

    @License.setter
    def License(self, License: 'str'):
        License = str(License)
        if not isinstance(License, str):
            raise TypeError("'License' must be of type str")
        self._License= License

    @property
    def repo(self) -> 'str':
        """the location of the repository for the component"""
        return self._repo

    @repo.setter
    def repo(self, repo: 'str'):
        repo = str(repo)
        if not isinstance(repo, str):
            raise TypeError("'repo' must be of type str")
        self._repo= repo

    @property
    def requiredAlfaVersion(self) -> 'str':
        """the required minimal version of the {Aphrodites Framework (e.g. DigitalPy) that is need to support the component"""
        return self._requiredAlfaVersion

    @requiredAlfaVersion.setter
    def requiredAlfaVersion(self, requiredAlfaVersion: 'str'):
        requiredAlfaVersion = str(requiredAlfaVersion)
        if not isinstance(requiredAlfaVersion, str):
            raise TypeError("'requiredAlfaVersion' must be of type str")
        self._requiredAlfaVersion= requiredAlfaVersion

    @property
    def URL(self) -> 'str':
        """universal Location where the component need to be installed. If empty will be installed inside the current system"""
        return self._URL

    @URL.setter
    def URL(self, URL: 'str'):
        URL = str(URL)
        if not isinstance(URL, str):
            raise TypeError("'URL' must be of type str")
        self._URL= URL

    @property
    def Version(self) -> 'str':
        """The version of the component, following semantic versioning"""
        return self._Version

    @Version.setter
    def Version(self, Version: 'str'):
        Version = str(Version)
        if not isinstance(Version, str):
            raise TypeError("'Version' must be of type str")
        self._Version= Version

    @property
    def UUID(self) -> 'str':
        """A unique identifier for the component e.g. D3BCB981-6D28-4664-905E-AF1C7B871A6D"""
        return self._UUID

    @UUID.setter
    def UUID(self, UUID: 'str'):
        UUID = str(UUID)
        if not isinstance(UUID, str):
            raise TypeError("'UUID' must be of type str")
        self._UUID= UUID

    @property
    def isActive(self) -> 'str':
        """true if the component's is currently running"""
        return self._isActive

    @isActive.setter
    def isActive(self, isActive: 'str'):
        isActive = str(isActive)
        if not isinstance(isActive, str):
            raise TypeError("'isActive' must be of type str")
        self._isActive= isActive

    @property
    def isInstalled(self) -> 'str':
        """true if the component's physical code has been deployed"""
        return self._isInstalled

    @isInstalled.setter
    def isInstalled(self, isInstalled: 'str'):
        isInstalled = str(isInstalled)
        if not isinstance(isInstalled, str):
            raise TypeError("'isInstalled' must be of type str")
        self._isInstalled= isInstalled

    @property
    def installationPath(self) -> 'str':
        """the location of the component on the disk"""
        return self._installationPath

    @installationPath.setter
    def installationPath(self, installationPath: 'str'):
        installationPath = str(installationPath)
        if not isinstance(installationPath, str):
            raise TypeError("'installationPath' must be of type str")
        self._installationPath= installationPath

    @property
    def name(self) -> 'str':
        """"""
        return self._name

    @name.setter
    def name(self, name: 'str'):
        name = str(name)
        if not isinstance(name, str):
            raise TypeError("'name' must be of type str")
        self._name= name
