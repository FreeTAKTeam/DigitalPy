#######################################################
# 
# core_name_controller.py
# Python implementation of the Class CoreNameRulesController
# Generated by Enterprise Architect
# Created on:      16-Dec-2022 10:56:02 AM
# Original author: Giu Platania
# 
#######################################################
from digitalpy.core.logic.impl.default_business_rule_controller import DefaultBusinessRuleController

class LogicController(DefaultBusinessRuleController):
    """contains all the business logic of this core package
    """
    def __init__(self):
        """the constructor of the Logic Controller
        """

    def execute(self, method: str=None, **kwargs):
        """this is the entry point for this controller

        Args:
            method (str, optional): the method to be executed. Defaults to None.
        """
        getattr(self, method)

    def parse_logic(self):
        """Creates the model object outline and passes it to the parser to fill the model
        object with the xml data
        """
        