from digitalpy.core.main.controller import Controller
from digitalpy.core.logic.contexts import Contexts
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.zmanager.action_mapper import ActionMapper

import rule_engine
from typing import Dict, Callable, List, Union
import json

from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response


class DefaultBusinessRuleController(Controller):
    """this is the default base class from which all controllers which use business rules should take advantage of
    """
    def __init__(
        self,
        business_rules_path: Dict[str, List[Callable]],
        internal_action_mapper: ActionMapper,
        **kwargs
    ):
        """the constructor for default business rules

        Args:
            business_rules_path (Dict[str, List[Callable]]): this is the path where business rules are defined
            internal_action_mapper (ActionMapper): the internal action mapper of this component
        """
        super().__init__(**kwargs)
        self.internal_action_mapper = internal_action_mapper
        self.business_rules_path = business_rules_path
        self.reload_business_rules(business_rules_path)

    def reload_business_rules(self, business_rules_path: str=None):
        """reload the business rules

        Args:
            business_rules_path (str, optional): the path to the business rules. Defaults to None.
        """
        if business_rules_path is None:
            business_rules_path = self.business_rules_path
        with open(
            self.business_rules_path, "r", encoding="utf-8"
        ) as business_rules_file:
            self.business_rules = json.load(business_rules_file)

    def evaluate_request(
        self, matchable: Union[dict, object] = None, rule_dict: dict = None, *args, **kwargs
    ):
        """evaluate a given request based on the defined action rules

        Args:
            matchable (Union[dict, object], optional): the object used to be matched against a given business rule. defaults to None.
            rule_dict (dict, optional): a dictionary of business rules. defaults to None.
        """
        if rule_dict is None:
            rule_dict = self.business_rules

        for k, v in kwargs.items():
            self.request.set_value(k, v)
        
        self._evaluate_actions(rule_dict)

        if rule_dict.get("rules", None) is not None:
            matchable = self._get_matchable_object(matchable, rule_dict)

            resolver = self._get_resolver(matchable, rule_dict)

            self._evaluate_sub_rules(matchable, rule_dict, resolver)

    def _get_matchable_object(self, matchable, rule_dict):
        # TODO: it may be better to get the matchable from the response
        # instead of the request
        new_matchable = rule_dict.get("matchable", None)
        if new_matchable is None:
            matchable = self.request.get_values()
        else:
            matchable = self.request.get_value(new_matchable)
        return matchable

    def _evaluate_sub_rules(self, matchable: Union[object, dict], rule_dict: dict, resolver: "Resolver") -> None:
        """evaluate the sub rules of a given rule evaluation

        Args:
            matchable (Union[object, dict]): the object used to be matched against a given business rule
            rule_dict (dict): a dictionary of business rules
            resolver (Resolver): a rule_engine resolver capable of resolving the attributes of the matchable type
        """
        for sub_rule in rule_dict["rules"]:
            if rule_engine.Rule(
                sub_rule,
                context=rule_engine.Context(resolver=resolver),
            ).matches(matchable):
                self.evaluate_request(rule_dict=rule_dict["rules"][sub_rule])

    def _get_resolver(self, matchable: Union[object, dict], rule_dict: dict):
        """get the resolver based on the matchable type

        Args:
            matchable (Union[object, dict]): the object used to be matched against a given business rule
            rule_dict (dict): a dictionary of business rules

        Raises:
            ValueError: thrown when the type of the matchable is not an object n'or a dictionary

        Returns:
            Resolver: a rule_engine resolver capable of resolving the attributes of the matchable type
        """

        resolver = rule_dict.get("resolver")

        if resolver is None:
            if isinstance(matchable, dict):
                resolver = getattr(rule_engine, Contexts.ITEM_CTX.value)

            elif isinstance(matchable, object):
                resolver = getattr(rule_engine, Contexts.ATTRIBUTE_CTX.value)

            else:
                raise ValueError(
                    "matchable is of unsupported type: %s" % type(matchable)
                )

        else:
            resolver = getattr(rule_engine, getattr(Contexts, resolver))
        return resolver
		
    def _evaluate_actions(self, rule_dict: dict):
        """evaluate the action of a rule_dictionary

        Args:
            rule_dict (dict): the rule dictionary to be evaluated
        """
        if "actions" in rule_dict:
            cur_request = self.get_request()
            cur_response = self.get_response()
            for action in rule_dict["actions"]:
                sub_request = self.create_request(
                    sender=self.__class__.__name__,
                    context=cur_request.get_context(),
                    action=action,
                    values=cur_request.get_values(),
                    format=cur_request.get_format(),
                )
                sub_response = self.create_response(format=cur_response.get_format())
                self.internal_action_mapper.process_action(sub_request, sub_response)
                
                for key, value in sub_response.get_values().items():
                    cur_response.set_value(key, value)
                
                # add support for next_action outside of the internal_action_mapper
                if sub_response.get_action() != sub_request.get_action():
                    cur_response.set_action(sub_response.get_action())
                    
                if sub_response.get_context() != sub_request.get_context():
                    cur_response.set_context(sub_response.get_context())

    def create_request(self, sender: str=None, context: str=None, action: str=None, values: Union[dict, str]={}, format: str=None) -> Request:
        """create a request object

        Args:
            sender (str, optional): the class name of the sender of the request. Defaults to None.
            context (str, optional): the context of the request. Defaults to None.
            action (str, optional): the action of the request. Defaults to None.
            values (Union[dict, str], optional): the values dictionary of the request serialized or unserialized. Defaults to empty dictionary.
            format (str, optional): the format used to serialize or de-serialize the values dictionary. Defaults to None.

        Returns:
            Request: a request object with the given parameters
        """
        request: Request = ObjectFactory.get_instance("request")
        request.set_sender(sender)
        request.set_context(context)
        request.set_action(action)
        request.set_values(values)
        request.set_format(format)
        return request

    def create_response(self, sender: str=None, context: str=None, action: str=None, values: Union[dict, str] = {}, format: str=None) -> Response:
        """create a response object

        Args:
            sender (str, optional): the class name of the sender of the response. Defaults to None.
            context (str, optional): the context of the response. Defaults to None.
            action (str, optional): the action of the response. Defaults to None.
            values (dict, optional): the values dictionary of the response serialized or unserialized. Defaults to empty dictionary.
            format (str, optional): the format used to serialize or de-serialize the values dictionary. Defaults to None.

        Returns:
            response: a response object with the given parameters
        """
        response: Response = ObjectFactory.get_instance("response")
        response.set_sender(sender)
        response.set_context(context)
        response.set_action(action)
        response.set_values(values)
        response.set_format(format)
        return response

    def _process_response(self, rule_dict: dict):
        """process the response from a rule_dict

        Args:
            rule_dict (dict): the rule dict to be processed
        """
        # process the response according to the rules defined in the configuration
        if "response" in rule_dict:
            for key, value in rule_dict["response"].items():
                # set the response value according to the configuration
                self.response.set_value(key, value)
        else:
            # if no response is defined in the configuration, set the response to an empty dictionary
            self.response.set_value({})

    def run(self):
        # evaluate the request according to the business rules defined in the configuration
        self.evaluate_request()
        # process the response according to the rules defined in the configuration
        self._process_response(self.business_rules)
