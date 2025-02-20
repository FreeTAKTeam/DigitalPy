from .controllers.FilmologyManagement_persistence_controller import FilmologyManagementPersistenceController
from digitalpy.core.component_management.impl.default_facade import DefaultFacade
from digitalpy.core.zmanager.impl.async_action_mapper import AsyncActionMapper
from digitalpy.core.zmanager.impl.default_action_mapper import DefaultActionMapper
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from .controllers.FilmologyManagement_controller import FilmologyManagementController
from .configuration.FilmologyManagement_constants import (
    ACTION_MAPPING_PATH,
    LOGGING_CONFIGURATION_PATH,
    INTERNAL_ACTION_MAPPING_PATH,
    MANIFEST_PATH,
    CONFIGURATION_PATH_TEMPLATE,
    LOG_FILE_PATH,
    ACTION_FLOW_PATH,
)

from . import base


class FilmologyManagement(DefaultFacade):
    """
    """

    def __init__(self, sync_action_mapper: DefaultActionMapper, request: Request,
                 response: Response, configuration,
                 action_mapper: AsyncActionMapper = None,  # type: ignore
                 tracing_provider_instance=None):  # type: ignore
        super().__init__(
            # the path to the external action mapping
            action_mapping_path=str(ACTION_MAPPING_PATH),
            # the path to the internal action mapping
            internal_action_mapping_path=str(INTERNAL_ACTION_MAPPING_PATH),
            # the path to the logger configuration
            logger_configuration=str(LOGGING_CONFIGURATION_PATH),
            # the package containing the base classes
            base=base,  # type: ignore
            # the general action mapper (passed by constructor)
            action_mapper=sync_action_mapper,
            # the request object (passed by constructor)
            request=request,
            # the response object (passed by constructor)
            response=response,
            # the configuration object (passed by constructor)
            configuration=configuration,
            # log file path
            log_file_path=LOG_FILE_PATH,
            # the tracing provider used
            tracing_provider_instance=tracing_provider_instance,
            # the template for the absolute path to the model object definitions
            configuration_path_template=CONFIGURATION_PATH_TEMPLATE,
            # the path to the manifest file
            manifest_path=str(MANIFEST_PATH),
            # the general action mapper (passed by constructor)
            action_flow_path=str(ACTION_FLOW_PATH),
        )
        self.persistence_controller = FilmologyManagementPersistenceController(
            request, response, sync_action_mapper, configuration)
        self.FilmologyManagement_controller = FilmologyManagementController(
            request, response, sync_action_mapper, configuration)

    def initialize(self, request: Request, response: Response):
        self.FilmologyManagement_controller.initialize(request, response)
        self.persistence_controller.initialize(request, response)

        return super().initialize(request, response)

    def execute(self, method=None):
        try:
            if hasattr(self, method):  # type: ignore
                print("executing method "+str(method))  # type: ignore
                getattr(self, method)(**self.request.get_values())  # type: ignore
            else:
                self.request.set_value("logger", self.logger)
                self.request.set_value("config_loader", self.config_loader)
                self.request.set_value("tracer", self.tracer)
                response = self.execute_sub_action(self.request.get_action())
                self.response.set_values(response.get_values())
        except Exception as e:
            self.logger.fatal(str(e))
    @DefaultFacade.public
    def POSTMovie(self, *args, **kwargs):
        """Creates a new Movie record.
        """
        self.FilmologyManagement_controller.POSTMovie(*args, **kwargs)
    @DefaultFacade.public
    def DELETEMovie(self, *args, **kwargs):
        """Deletes an existing Movie record based on the provided ID.
        """
        self.FilmologyManagement_controller.DELETEMovie(*args, **kwargs)
    @DefaultFacade.public
    def GETMovie(self, *args, **kwargs):
        """Retrieves a list of all Movie
        """
        self.FilmologyManagement_controller.GETMovie(*args, **kwargs)
    @DefaultFacade.public
    def PATCHMovie(self, *args, **kwargs):
        """Updates an existing Movie record.
        """
        self.FilmologyManagement_controller.PATCHMovie(*args, **kwargs)
    @DefaultFacade.public
    def GETDirectorId(self, *args, **kwargs):
        """retrieve an existing Director record based on the provided ID.
        """
        self.FilmologyManagement_controller.GETDirectorId(*args, **kwargs)
    @DefaultFacade.public
    def POSTPoster(self, *args, **kwargs):
        """Creates a new Poster record.
        """
        self.FilmologyManagement_controller.POSTPoster(*args, **kwargs)
    @DefaultFacade.public
    def DELETEPoster(self, *args, **kwargs):
        """Deletes an existing Poster record based on the provided ID.
        """
        self.FilmologyManagement_controller.DELETEPoster(*args, **kwargs)
    @DefaultFacade.public
    def GETPoster(self, *args, **kwargs):
        """Retrieves a list of all Poster
        """
        self.FilmologyManagement_controller.GETPoster(*args, **kwargs)
    @DefaultFacade.public
    def PATCHPoster(self, *args, **kwargs):
        """Updates an existing Poster record.
        """
        self.FilmologyManagement_controller.PATCHPoster(*args, **kwargs)
    @DefaultFacade.public
    def GETGenreId(self, *args, **kwargs):
        """retrieve an existing Genre record based on the provided ID.
        """
        self.FilmologyManagement_controller.GETGenreId(*args, **kwargs)
    @DefaultFacade.public
    def POSTDate(self, *args, **kwargs):
        """Creates a new Date record.
        """
        self.FilmologyManagement_controller.POSTDate(*args, **kwargs)
    @DefaultFacade.public
    def DELETEDate(self, *args, **kwargs):
        """Deletes an existing Date record based on the provided ID.
        """
        self.FilmologyManagement_controller.DELETEDate(*args, **kwargs)
    @DefaultFacade.public
    def GETDate(self, *args, **kwargs):
        """Retrieves a list of all Date
        """
        self.FilmologyManagement_controller.GETDate(*args, **kwargs)
    @DefaultFacade.public
    def PATCHDate(self, *args, **kwargs):
        """Updates an existing Date record.
        """
        self.FilmologyManagement_controller.PATCHDate(*args, **kwargs)
    @DefaultFacade.public
    def GETLanguageId(self, *args, **kwargs):
        """retrieve an existing Language record based on the provided ID.
        """
        self.FilmologyManagement_controller.GETLanguageId(*args, **kwargs)
    @DefaultFacade.public
    def POSTDirector(self, *args, **kwargs):
        """Creates a new Director record.
        """
        self.FilmologyManagement_controller.POSTDirector(*args, **kwargs)
    @DefaultFacade.public
    def DELETEDirector(self, *args, **kwargs):
        """Deletes an existing Director record based on the provided ID.
        """
        self.FilmologyManagement_controller.DELETEDirector(*args, **kwargs)
    @DefaultFacade.public
    def GETDirector(self, *args, **kwargs):
        """Retrieves a list of all Director
        """
        self.FilmologyManagement_controller.GETDirector(*args, **kwargs)
    @DefaultFacade.public
    def PATCHDirector(self, *args, **kwargs):
        """Updates an existing Director record.
        """
        self.FilmologyManagement_controller.PATCHDirector(*args, **kwargs)
    @DefaultFacade.public
    def GETDateId(self, *args, **kwargs):
        """retrieve an existing Date record based on the provided ID.
        """
        self.FilmologyManagement_controller.GETDateId(*args, **kwargs)
    @DefaultFacade.public
    def POSTActor(self, *args, **kwargs):
        """Creates a new Actor record.
        """
        self.FilmologyManagement_controller.POSTActor(*args, **kwargs)
    @DefaultFacade.public
    def DELETEActor(self, *args, **kwargs):
        """Deletes an existing Actor record based on the provided ID.
        """
        self.FilmologyManagement_controller.DELETEActor(*args, **kwargs)
    @DefaultFacade.public
    def GETActor(self, *args, **kwargs):
        """Retrieves a list of all Actor
        """
        self.FilmologyManagement_controller.GETActor(*args, **kwargs)
    @DefaultFacade.public
    def PATCHActor(self, *args, **kwargs):
        """Updates an existing Actor record.
        """
        self.FilmologyManagement_controller.PATCHActor(*args, **kwargs)
    @DefaultFacade.public
    def GETMovieId(self, *args, **kwargs):
        """retrieve an existing Movie record based on the provided ID.
        """
        self.FilmologyManagement_controller.GETMovieId(*args, **kwargs)
    @DefaultFacade.public
    def POSTLanguage(self, *args, **kwargs):
        """Creates a new Language record.
        """
        self.FilmologyManagement_controller.POSTLanguage(*args, **kwargs)
    @DefaultFacade.public
    def DELETELanguage(self, *args, **kwargs):
        """Deletes an existing Language record based on the provided ID.
        """
        self.FilmologyManagement_controller.DELETELanguage(*args, **kwargs)
    @DefaultFacade.public
    def GETLanguage(self, *args, **kwargs):
        """Retrieves a list of all Language
        """
        self.FilmologyManagement_controller.GETLanguage(*args, **kwargs)
    @DefaultFacade.public
    def PATCHLanguage(self, *args, **kwargs):
        """Updates an existing Language record.
        """
        self.FilmologyManagement_controller.PATCHLanguage(*args, **kwargs)
    @DefaultFacade.public
    def GETPosterId(self, *args, **kwargs):
        """retrieve an existing Poster record based on the provided ID.
        """
        self.FilmologyManagement_controller.GETPosterId(*args, **kwargs)
    @DefaultFacade.public
    def GETActorId(self, *args, **kwargs):
        """retrieve an existing Actor record based on the provided ID.
        """
        self.FilmologyManagement_controller.GETActorId(*args, **kwargs)
    @DefaultFacade.public
    def POSTGenre(self, *args, **kwargs):
        """Creates a new Genre record.
        """
        self.FilmologyManagement_controller.POSTGenre(*args, **kwargs)
    @DefaultFacade.public
    def DELETEGenre(self, *args, **kwargs):
        """Deletes an existing Genre record based on the provided ID.
        """
        self.FilmologyManagement_controller.DELETEGenre(*args, **kwargs)
    @DefaultFacade.public
    def GETGenre(self, *args, **kwargs):
        """Retrieves a list of all Genre
        """
        self.FilmologyManagement_controller.GETGenre(*args, **kwargs)
    @DefaultFacade.public
    def PATCHGenre(self, *args, **kwargs):
        """Updates an existing Genre record.
        """
        self.FilmologyManagement_controller.PATCHGenre(*args, **kwargs)
