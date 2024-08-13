#######################################################
#
# DigitalPy.py
# Python implementation of the Class DigitalPy
# Generated by Enterprise Architect
# Created on:      28-Dec-2022 1:18:23 PM
# Original author: FreeTAKTeam
#
#######################################################
import multiprocessing
import os
import pathlib
import threading
from time import sleep
from typing import TYPE_CHECKING

from digitalpy.core.digipy_configuration.controllers.action_flow_controller import ActionFlowController
from digitalpy.core.service_management.service_management_core import ServiceManagementCore
from digitalpy.core.telemetry.singleton_status_factory import SingletonStatusFactory
from digitalpy.core.telemetry.domain.status_factory import StatusFactory
from digitalpy.core.main.impl.configuration_factory import ConfigurationFactory
from digitalpy.core.zmanager.integration_manager import IntegrationManager
from digitalpy.core.digipy_configuration.domain.model.configuration import Configuration
from digitalpy.core.digipy_configuration.impl.inifile_configuration import (
    InifileConfiguration,
)
from digitalpy.core.component_management.impl.default_facade import DefaultFacade

from digitalpy.core.telemetry.tracer import Tracer
from digitalpy.core.telemetry.tracing_provider import TracingProvider
from digitalpy.core.zmanager.response import Response
from digitalpy.core.component_management.component_management_facade import (
    ComponentManagement,
)

from digitalpy.core.zmanager.subject import Subject
from digitalpy.core.main.factory import Factory
from digitalpy.core.main.impl.default_factory import DefaultFactory
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.main.singleton_configuration_factory import (
    SingletonConfigurationFactory,
)


from digitalpy.core.domain.domain_facade import Domain
from digitalpy.core.IAM.IAM_facade import IAM
from digitalpy.core.serialization.serialization_facade import Serialization
from digitalpy.core.service_management.service_management_facade import (
    ServiceManagement,
)
from digitalpy.core.files.files_facade import Files
from digitalpy.core.zmanager.domain.model.zmanager_configuration import (
    ZManagerConfiguration,
)

if TYPE_CHECKING:
    from digitalpy.core.digipy_configuration.action_key_controller import (
        ActionKeyController,
    )


class DigitalPy:
    """this is the executable of the digitalPy framework, providing the starting point
    for a bare bone application.
    """

    def __init__(self):
        # Set up necessary resources and configurations for the application to run
        self.resources = []
        self.configuration: Configuration = InifileConfiguration("")

        self.subject: Subject
        self.subject_thread: threading.Thread

        self.service_manager: ServiceManagementCore
        self.service_manager_thread: threading.Thread

        self.integration_manager: IntegrationManager
        self.integration_manager_process: multiprocessing.Process

        # register the digitalpy action mapping under ../digitalpy/core_config.ini
        self.configuration.add_configuration(
            str(
                pathlib.PurePath(
                    pathlib.PurePath(os.path.abspath(__file__)).parent.parent,
                    "core_config.ini",
                )
            ),
        )
        # the central digitalpy configuration used throughout the application
        self.factory: Factory = DefaultFactory(self.configuration)

        # register the factory and configuration to the object factory singleton
        ObjectFactory.configure(self.factory)

        # register the configuration factory to the config factory singleton
        self._initialize_configuration_factory()

        self._initialize_status_factory()

        self.initialize_tracing()

        self.responses: dict[str, Response] = {}

        self.action_key_controller: "ActionKeyController" = ObjectFactory.get_instance(
            "ActionKeyController"
        )

        self.service_id = self.configuration.get_value("service_id", "DigitalPy")

        self.zmanager_conf: ZManagerConfiguration = (
            SingletonConfigurationFactory.get_configuration_object(
                "ZManagerConfiguration"
            )
        )

    def _initialize_status_factory(self):
        self.status_factory = StatusFactory()

        SingletonStatusFactory.configure(self.status_factory)

        status_conf = InifileConfiguration("")
        status_conf.add_configuration(
            str(
                pathlib.PurePath(
                    pathlib.PurePath(os.path.abspath(__file__)).parent.parent,
                    "core_status.ini",
                )
            ),
        )

        self.status_factory.add_configuration(status_conf)

    def _initialize_configuration_factory(self):
        self.configuration_factory = ConfigurationFactory()
        SingletonConfigurationFactory.configure(self.configuration_factory)

        base_conf: Configuration = InifileConfiguration("")
        base_conf.add_configuration(
            str(
                pathlib.PurePath(
                    pathlib.PurePath(os.path.abspath(__file__)).parent.parent,
                    "configuration_management.ini",
                )
            ),
        )

        SingletonConfigurationFactory.add_configuration(base_conf)

    def initialize_tracing(self):
        """initialize the tracing provider for the application"""
        # the central tracing provider
        self._tracing_provider: TracingProvider = self.factory.get_instance(
            "tracingprovider"
        )

        self._tracing_provider.initialize_tracing()

        self.tracer: Tracer = self._tracing_provider.create_tracer("DigitalPy.Main")

    def register_flows(self):
        action_flow_controller = ActionFlowController()
        action_flow_file = str(
            pathlib.PurePath(__file__).parent.parent / "core_flows.ini"
        )
        file_facades: Files = ObjectFactory.get_instance("Files")
        file = file_facades.get_or_create_file(path=action_flow_file)

        action_flow_controller.create_action_flow(file)

    def register_components(self):
        """register digitalpy core components, these must be registered before any other components
        furthermore, these are registered without the use of component management to avoid circular
        dependencies. This method of registration also assumes that the components are defined in
        the digitalpy/core/action_mapping.ini file and are located in the digitalpy/core folder.
        Any inheriting classes should override this method to register their own components using
        the component management facade. and should call super().register_components() to ensure
        that the core components are registered.

        Inheriting classes should also set the following configuration values in their configuration
        file:
        [ComponentManagement]
        component_import_root=<path to the root of the component folder as a python import>
        component_installation_path=<path to the root of the component folder as a file system path>
        component_blueprint_path=<path to the blueprint file for the component>
        """

        config: Configuration = ObjectFactory.get_instance("Configuration")

        def register_component(facade: DefaultFacade, config: Configuration):
            config.add_configuration(facade.get_configuration_path())

            ObjectFactory.register_instance(
                facade.__class__.__name__.lower() + "actionmapper",
                facade.get_action_mapper(),
            )

            facade.setup()

        register_component(ComponentManagement(None, None, None, None), config)

        register_component(Domain(None, None, None, None), config)

        register_component(IAM(None, None, None, None), config)

        register_component(Serialization(None, None, None, None), config)

        register_component(ServiceManagement(None, None, None, None), config)

        register_component(Files(None, None, None, None), config)

    def test_event_loop(self):
        """the main event loop of the application should be called within a continuous while loop"""
        sleep(1)

    def event_loop(self):
        """the main event loop of the application should be called within a continuous while loop"""
        # TODO: what should this be in the default case
        sleep(1)

    def start(self):  # type: ignore
        """Begin the execution of the application, this should be overriden
        by any inheriting classes"""

        self.register_components()
        self.register_flows()
        self.configure()

        self.start_zmanager()
        self.start_core_services()
        while True:
            try:
                self.event_loop()
            except Exception as ex:  # pylint: disable=broad-except
                self.handle_exception(ex)

    def handle_exception(self, error: Exception):
        """Deal with errors that occur during the execution of the application"""
        print("error thrown :" + str(error))

    def start_core_services(self):
        """Start the core services of the application"""
        self.start_service_manager()

    def start_zmanager(self):
        """Start the zmanager services of the application"""
        self.start_integration_manager_service()
        self.start_subject_service()

    def start_subject_service(self):
        """this function is responsible for starting the subject service"""
        try:
            self.subject: Subject = ObjectFactory.get_instance("Subject")
            self.subject_thread = threading.Thread(target=self.subject.begin_routing)
            self.subject_thread.start()
        except Exception as ex:
            raise RuntimeError("Failed to start the subject service") from ex

    def stop_subject_service(self):
        """this function is responsible for stopping the subject service"""
        try:
            self.subject.running.clear()
            # wait for the subject to clean up its resources
            self.subject_thread.join(self.zmanager_conf.subject_pull_timeout / 1000 + 3)
        except Exception as e:
            raise RuntimeError("Failed to stop the subject service") from e

    def start_integration_manager_service(self) -> bool:
        """Starts the integration manager service.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:

            # begin the integration_manager_service
            self.integration_manager: IntegrationManager = ObjectFactory.get_instance(
                "IntegrationManager"
            )
            self.integration_manager_process = multiprocessing.Process(
                target=self.integration_manager.start
            )
            self.integration_manager_process.start()

            return True
        except Exception as ex:
            raise ex

    def stop_integration_manager_service(self) -> bool:
        """Stops the integration manager service.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            self.integration_manager.running.clear()
            # wait for the integration manager to clean up its resources
            self.integration_manager_process.join(
                self.zmanager_conf.integration_manager_pull_timeout / 1000 + 2
            )
            if self.integration_manager_process.is_alive():
                self.integration_manager_process.terminate()
                self.integration_manager_process.join()
            else:
                self.integration_manager_process.join()
            return True
        except Exception as ex:
            raise ex

    def start_service_manager(self) -> bool:
        """Starts the service manager.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:

            # begin the service_manager
            self.service_manager: ServiceManagementCore = ObjectFactory.get_instance(
                "ServiceManager"
            )

            self.service_manager.start()

            return True
        except Exception as ex:
            raise ex

    def stop_service_manager(self) -> bool:
        """Stops the service manager.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:

            self.service_manager.stop()
            self.service_manager.join()
            return True
        except Exception as ex:
            raise ex

    def stop(self):
        """End the execution of the application"""
        self.stop_core_services()
        self.stop_zmanager()

        exit(0)

    def stop_core_services(self):
        """Stop the core services of the application"""
        self.stop_service_manager()

    def stop_zmanager(self):
        """Stop the zmanager services of the application"""
        self.stop_integration_manager_service()
        self.stop_subject_service()

    def restart(self):
        """End and then restart the execution of the application"""
        self.stop()
        self.start()

    def save_state(self):
        """Persist the current state of the application to allow for future restoration"""

    def load_state(self):
        """Restore the application to a previously saved state"""

    def configure(self):
        """Set or modify the configuration of the application"""

    def get_status(self):
        """Retrieve the current status of the application (e.g. running, stopped, etc.)"""

    def get_logs(self):
        """Retrieve the log records generated by the application"""

    def shutdown(self):
        """Close all resources and terminate the applications"""
        self.resources = []
        self.configurations = {}


if __name__ == "__main__":
    DigitalPy().start()
