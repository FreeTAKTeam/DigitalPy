from digitalpy.routing.controller import Controller
from digitalpy.logic.contexts import Contexts
from digitalpy.core.object_factory import ObjectFactory
import rule_engine
from typing import Dict, Callable, List, Union
import json


class DefaultBusinessRuleController(Controller):
    def __init__(
        self,
        business_rules_path: Dict[str, List[Callable]],
        internal_action_mapper,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.internal_action_mapper = internal_action_mapper
        self.business_rules_path = business_rules_path
        self.reload_business_rules(business_rules_path)

    def reload_business_rules(self, business_rules_path=None):
        if business_rules_path is None:
            business_rules_path = self.business_rules_path
        with open(
            self.business_rules_path, "r", encoding="utf-8"
        ) as business_rules_file:
            self.business_rules = json.load(business_rules_file)

    def evaluate_request(
        self, matchable: Union[dict, object] = None, rule_dict: dict = None, **kwargs
    ):
        self.response.set_values(kwargs)
        if rule_dict is None:
            rule_dict = self.business_rules
        self._evaluate_actions(rule_dict)

        if rule_dict.get("rules", None) is not None:
            matchable = self._get_matchable_object(matchable, rule_dict)

            resolver = self._get_resolver(matchable, rule_dict)

            self._evaluate_sub_rules(matchable, rule_dict, resolver)

    def _evaluate_sub_rules(self, matchable, rule_dict, resolver):
        for sub_rule in rule_dict["rules"]:
            if rule_engine.Rule(
                sub_rule,
                context=rule_engine.Context(resolver=resolver),
            ).matches(matchable):
                self.evaluate_request(rule_dict=rule_dict["rules"][sub_rule])

    def _get_resolver(self, matchable, rule_dict):
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

    def _get_matchable_object(self, matchable, rule_dict):
        new_matchable = rule_dict.get("matchable", None)
        if new_matchable is None:
            matchable = self.request.get_value(matchable)
        else:
            matchable = self.request.get_value(new_matchable)
        return matchable

    def _evaluate_actions(self, rule_dict):
        if "actions" in rule_dict:
            for action in rule_dict["actions"]:
                cur_request = self.get_request()
                sub_request = ObjectFactory.get_new_instance("request")
                sub_request.set_sender(self.__class__.__name__)
                sub_request.set_context(cur_request.get_context())
                sub_request.set_action(action)
                sub_request.set_values(cur_request.get_values())
                sub_response = ObjectFactory.get_new_instance("response")
                self.internal_action_mapper.process_action(sub_request, sub_response)