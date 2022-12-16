#######################################################
# 
# DigitalPyService.py
# Python implementation of the Class DigitalPyService
# Generated by Enterprise Architect
# Created on:      02-Dec-2022 5:39:44 PM
# Original author: Giu Platania
# 
#######################################################
from digitalpy.core.service import Service
from digitalpy.routing.impl.zmq_subscriber import ZmqSubscriber
from digitalpy.routing.impl.zeroless_pusher import ZerolessPusher
import asyncio
import socket
from abc import abstractmethod

class DigitalPyService(Service, ZmqSubscriber, ZerolessPusher):
    # QUESTION: does collector == subject
    # QUESTION: does broker == integration manager
    #TODO: implement some sort of event driven framework to triger events
    # on the reception of messages from the subscriber interface or the socket
    #TODO: what is the service manager supposed to do? is this going to be a new service
    
    def __init__(self, service_id: str, subject_address: str, subject_port: int, integration_manager_address: str, integration_manager_port: int):
        self.subject_address = subject_address
        self.subject_port = subject_port
        self.integration_manager_address = integration_manager_address
        self.integration_port_address = integration_manager_port
        self.service_id = service_id
        
    def discovery(self):
        """report the service to a service manager
        """
        pass

    def send_heart_beat(self):
        """send service is alive
        """
        self.subject_send(self.service_id+"here")
    
    def initialize_connections(self):
        self.subject_bind(self.subject_address, self.subject_port)
        self.broker_connect(self.integration_port_address, self.integration_manager_address,self.service_id)

    def handle_sub_message(self, message):
        """handle the case where a subscriber message is received"""
        pass

    def handle_sock_message(self, message):
        """handle the case where a subscriber message is received"""
        pass

    def stop(self):
        """stop the service
        """
        pass
    
    def message_received(self, message):
        """method to be called when a message is received"""
        pass