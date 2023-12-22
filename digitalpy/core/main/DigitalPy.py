#######################################################
#
# DigitalPy.py
# Python implementation of the Class DigitalPy
# Generated by Enterprise Architect
# Created on:      28-Dec-2022 1:18:23 PM
# Original author: FreeTAKTeam
#
#######################################################
from io import StringIO
import multiprocessing
import os
import pathlib
import sys
from threading import Event
from time import sleep
from typing import Callable
import signal

from digitalpy.core.digipy_configuration.configuration import Configuration
from digitalpy.core.digipy_configuration.impl.inifile_configuration import InifileConfiguration
from digitalpy.core.component_management.impl.component_registration_handler import ComponentRegistrationHandler
from digitalpy.core.telemetry.tracer import Tracer
from digitalpy.core.telemetry.tracing_provider import TracingProvider

from digitalpy.core.zmanager.subject import Subject
from digitalpy.core.zmanager.impl.zmq_pusher import ZMQPusher
from digitalpy.core.zmanager.impl.zmq_subscriber import ZmqSubscriber
from digitalpy.core.zmanager.request import Request
from digitalpy.core.main.factory import Factory
from digitalpy.core.main.impl.default_factory import DefaultFactory
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.service_management.controllers.service_management_main import ServiceManagementMain
from digitalpy.core.service_management.digitalpy_service import COMMAND_PROTOCOL, COMMAND_ACTION


class DigitalPy(ZmqSubscriber, ZMQPusher):
    """this is the executable of the digitalPy framework, providing the starting point
    for a bare bone application.
    """

    def __init__(self):
        # Set up necessary resources and configurations for the application to run
        self.resources = []
        self.configuration: Configuration = InifileConfiguration("")

        self.routing_proxy_service: Subject

        # register the digitalpy action mapping under ../digitalpy/action_mapping.ini
        self.configuration.add_configuration(
            str(
                pathlib.PurePath(
                    pathlib.PurePath(os.path.abspath(__file__)).parent.parent,
                    "action_mapping.ini",
                )
            ),
        )
        # the central digitalpy configuration used throughout the application
        self.factory: Factory = DefaultFactory(self.configuration)

        # register the factory and configuration to the object factory singleton
        ObjectFactory.configure(self.factory)
        ObjectFactory.register_instance("configuration", self.configuration)

        # factory instance is registered for use by the routing worker so that
        # the instances in the instance dictionary can be preserved when the
        # new object factory is instantiated in the sub-process
        ObjectFactory.register_instance("factory", self.factory)

        self.initialize_tracing()

        ZmqSubscriber.__init__(self, ObjectFactory.get_instance("formatter"))
        ZMQPusher.__init__(self, ObjectFactory.get_instance("formatter"))

    def set_zmanager_address(self):
        self.subject_address: str = self.configuration.get_value("subject_address", "Service")
        self.subject_port: int = int(self.configuration.get_value( "subject_port", "Service"))
        self.subject_protocol: str = self.configuration.get_value("subject_protocol", "Service")
        self.integration_manager_address: str = self.configuration.get_value("integration_manager_address", "Service")
        self.integration_manager_port: int = int(self.configuration.get_value("integration_manager_port", "Service"))
        self.integration_manager_protocol: str = self.configuration.get_value("integration_manager_protocol", "Service")
        self.service_id = "DigitalPy"

    def initialize_tracing(self):
        # the central tracing provider
        self._tracing_provider: TracingProvider = self.factory.get_instance(
            "tracingprovider")

        self._tracing_provider.initialize_tracing()

        self.tracer: Tracer = self._tracing_provider.create_tracer(
            "DigitalPy.Main")

    def register_components(self):
        """register all components of the application
        """
        # register base digitalpy components
        digipy_components = ComponentRegistrationHandler.discover_components(
            component_folder_path=pathlib.PurePath(
                str(
                    pathlib.PurePath(
                        os.path.abspath(__file__)
                    ).parent.parent
                ),
            )
        )

        for digipy_component in digipy_components:
            ComponentRegistrationHandler.register_component(
                digipy_component,  # type: ignore
                "digitalpy.core",
                self.configuration,  # type: ignore
            )

    def test_event_loop(self):
        """ the main event loop of the application should be called within a continuous while loop
        """
        sleep(1)

    def event_loop(self):
        """ the main event loop of the application should be called within a continuous while loop
        """
        # TODO: what should this be in the default case
        sleep(1)

    def start(self, testing: bool = False):  # type: ignore
        """Begin the execution of the application, this should be overriden
        by any inheriting classes"""

        self.register_components()
        self.configure()
        self.start_services()
        if not testing:
            while True:
                try:
                    self.event_loop()
                except Exception as ex:  # pylint: disable=broad-except
                    self.handle_exception(ex)
        # TODO: add a testing flag to the configuration
        elif testing:
            while True:
                try:
                    self.teardown_connections()
                except Exception as ex:  # pylint: disable=broad-except
                    self.handle_exception(ex)

    def handle_exception(self, error: Exception):
        """Deal with errors that occur during the execution of the application
        """
        print("error thrown :" + str(error))

    def start_services(self):
        self.set_zmanager_address()
        self.start_integration_manager_service()
        self.start_routing_proxy_service()
        self.start_service_manager()
        self.initialize_connections()

    def initialize_connections(self):
        ZMQPusher.initiate_connections(
            self, self.subject_port, self.subject_address, self.service_id)
        self.broker_connect(self.integration_manager_address, self.integration_manager_port,
                            self.integration_manager_protocol, self.service_id, COMMAND_PROTOCOL)

    def start_routing_proxy_service(self):
        """this function is responsible for starting the routing proxy service"""
        try:
            # begin the routing proxy
            self.routing_proxy_service: Subject = ObjectFactory.get_instance(
                "Subject")
            self.routing_proxy_process = multiprocessing.Process(
                target=self.routing_proxy_service.begin_routing
            )
            self.routing_proxy_process.start()

            return 1

        except Exception as ex:
            return -1

    def stop_routing_proxy_service(self):
        """this function is responsible for stopping the routing proxy service"""
        try:
            # TODO: add a pre termination call to shutdown workers and sockets before a
            # termination to prevent hanging resources
            if self.routing_proxy_process.is_alive():
                self.routing_proxy_process.terminate()
                self.routing_proxy_process.join()
            else:
                self.routing_proxy_process.join()
            return 1
        except Exception as e:
            return -1

    def start_integration_manager_service(self) -> bool:
        """Starts the integration manager service.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:

            # begin the integration_manager_service
            self.integration_manager_service = ObjectFactory.get_instance(
                "IntegrationManager")
            self.integration_manager_process = multiprocessing.Process(
                target=self.integration_manager_service.start)
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
            self.service_manager: ServiceManagementMain = ObjectFactory.get_instance(
                "ServiceManager")
            self.service_manager_process = multiprocessing.Process(target=self.service_manager.start, args=(ObjectFactory.get_instance(
                "factory"), ObjectFactory.get_instance("tracingprovider"), ComponentRegistrationHandler.component_index))
            self.service_manager_process.start()
            return True
        except Exception as ex:
            raise ex

    def stop_service_manager(self) -> bool:
        """Stops the service manager.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:

            self.stop_service(self.configuration.get_value(
                "service_id", "servicemanager"))
            self.service_manager_process.join(10)

            if self.service_manager_process.is_alive():

                self.service_manager_process.terminate()
                self.service_manager_process.join()
            else:
                self.service_manager_process.join()
            return True
        except Exception as ex:
            raise ex

    def start_service(self, service_id: str) -> bool:
        """Starts a service.

        Args:
            service_id (str): The unique id of the service to start.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            req: Request = ObjectFactory.get_new_instance("Request")
            req.set_action("StartServer")
            req.set_context(self.configuration.get_value(
                "service_id", "ServiceManager"))
            req.set_value("command", "start_service")
            req.set_value("target_service_id", service_id)
            req.set_format("pickled")
            self.subject_send_request(req, COMMAND_PROTOCOL, self.configuration.get_value(
                "service_id", "ServiceManager"))
            return True
        except Exception as ex:
            raise ex

    def stop_service(self, service_id: str) -> bool:
        """Starts a service.

        Args:
            service_id (str): The unique id of the service to start.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            req: Request = ObjectFactory.get_new_instance("Request")
            req.set_action(COMMAND_ACTION)
            req.set_context(self.configuration.get_value(
                "service_id", "servicemanager"))
            req.set_value("command", "stop_service")
            req.set_value("target_service_id", service_id)
            req.set_format("pickled")
            self.subject_send_request(req, COMMAND_PROTOCOL, self.configuration.get_value(
                "service_id", "ServiceManager"))
            return True
        except Exception as ex:
            raise ex

    def restart_service(self, service_id: str) -> bool:
        """Starts a service.

        Args:
            service_id (str): The unique id of the service to start.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            req: Request = ObjectFactory.get_new_instance("Request")
            req.set_action(COMMAND_ACTION)
            req.set_context(self.configuration.get_value(
                "service_id", "ServiceManager"))
            req.set_value("command", "restart_service")
            req.set_value("target_service_id", service_id)
            req.set_format("pickled")
            self.subject_send_request(req, COMMAND_PROTOCOL, self.configuration.get_value(
                "service_id", "ServiceManager"))
            return True
        except Exception as ex:
            raise ex

    def stop(self):
        """End the execution of the application"""
        self.stop_service_manager()
        self.stop_integration_manager_service()
        self.stop_routing_proxy_service()

        raise SystemExit

    def restart(self):
        # End and then restart the execution of the application
        self.stop()
        self.start()

    def save_state(self):
        # Persist the current state of the application to allow for future restoration
        pass

    def load_state(self):
        # Restore the application to a previously saved state
        pass

    def configure(self):
        """Set or modify the configuration of the application"""

    def get_status(self):
        # Retrieve the current status of the application (e.g. running, stopped, etc.)
        pass

    def get_logs(self):
        # Retrieve the log records generated by the application
        pass

    def shutdown(self):
        # Close all resources and terminate the application
        self.resources = []
        self.configurations = {}
