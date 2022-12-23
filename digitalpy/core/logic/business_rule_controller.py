from digitalpy.core.main.controller import Controller
from abc import ABC, abstractmethod
from typing import Union

class BusinessRuleController(Controller, ABC):
    def __init__(self, business_rules, rule_context, **kwargs):
        super().__init__(**kwargs)
        
    @abstractmethod
    def evaluate_request(self, matchable: Union[dict, object] = None, rule_dict: dict = None, **kwargs):
        pass
    
    @abstractmethod
    def reload_business_rules(self):
        pass