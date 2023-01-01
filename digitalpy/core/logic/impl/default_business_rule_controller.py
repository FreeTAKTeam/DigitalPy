from digitalpy.core.main.controller import Controller
from digitalpy.core.logic.contexts import Contexts
from digitalpy.core.main.object_factory import ObjectFactory
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
                resolver = getattr(rule_engine,
	
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
		
		def _evaluate_actions(self, rule_dict):
			if "actions" in rule_dict:
				cur_request = self.get_request()
				cur_response = self.get_response()
				for action in rule_dict["actions"]:
					sub_request = Request(
						sender=self.__class__.__name__,
						context=cur_request.get_context(),
						action=action,
						values=cur_request.get_values(),
						format=cur_request.get_format(),
					)
					sub_response = Response(format=cur_response.get_format())
					self.internal_action_mapper.process_action(sub_request, sub_response)
					cur_response.update(sub_response.get_values())
		
		def _process_response(self, rule_dict):
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
