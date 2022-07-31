#######################################################
# 
# Emergency.py
# Python implementation of the Class Emergency
# Generated by Enterprise Architect
# Created on:      13-Apr-2020 4:40:22 PM
# Original author: Corvo
# 
#######################################################
from emergency_RI.model.model_constants import EmergencyVariables as vars
from digitalpy.model.node import Node

class emergency(Node):
    """An Emergency beacon the is continually send to all the connected clients until
    deactivated from the original creator
    """
    def __init__(self, configuration, model):
        super().__init__(self.__class__.__name__, configuration, model)
        self.type = None
        self.alert = None
    # if true the Emergency beacon is canceled
        self.cancel = None
        self.INTAG = None

    def settype(self, type=None):
        self.type = type
    
    def gettype(self):
        return self.type

    def setAlert(self, alert=None):
        self.alert = alert

    def getAlert(self):
        return self.alert

    def setcancel(self, cancel=None):
        self.cancel = cancel

    def getcancel(self):
        return self.cancel

    def setINTAG(self, INTAG=None):
        self.INTAG = INTAG

    def getINTAG(self):
        return self.INTAG
