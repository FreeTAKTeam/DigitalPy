#######################################################
# 
# DigitalPyService.py
# Python implementation of the Class DigitalPyService
# Generated by Enterprise Architect
# Created on:      02-Dec-2022 5:39:44 PM
# Original author: Giu Platania
# 
#######################################################
import Service
import SUB
import PULL

class DigitalPyService(Service, SUB, PULL):
# default constructor  def __init__(self):  

    def BrokerConnect():
        """Connect or reconnect to broker
        """
        pass

    def BrokerReceive():
        """Returns the reply message or None if there was no reply
        """
        pass

    def BrokerSend():
        """Send request to broker
        """
        pass

    def collectorBind():
        """create the ZMQ zocket
        """
        pass

    def CollectorSend():
        """send the message to a SUbscriber
        """
        pass

    def Discovery():
        """report the service to a service manager
        """
        pass

    def sendHeartBeat():
        """send service is alive
        """
        pass

    def Start():
        """start the service
        """
        pass

    def Stop():
        """stop the service
        """
        pass