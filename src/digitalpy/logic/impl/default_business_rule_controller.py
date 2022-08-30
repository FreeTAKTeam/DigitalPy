from digitalpy.routing.controller import Controller
from digitalpy.logic.contexts import Contexts
import rule_engine
from typing import Dict, Callable, List, Union


class DefaultBusinessRuleController(Controller):
    def __init__(self, business_rules: Dict[str, List[Callable]], **kwargs):
        super().__init__(**kwargs)
        self.business_rules = business_rules

    def evaluate_request(
        self, matchable: Union[dict, object] = None, rule_dict: dict = None, **kwargs
    ):
        self.response.set_values(kwargs)
        if rule_dict is None:
            rule_dict = self.business_rules
        if "callbacks" in rule_dict:
            for callback in rule_dict["callbacks"]:
                callback(**self.request.get_values())

        if rule_dict.get("rules", None) is not None:
            new_matchable = rule_dict.get("matchable", None)
            if new_matchable is None:
                matchable = self.request.get_value(matchable)
            else:
                matchable = self.request.get_value(new_matchable)

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

            for sub_rule in rule_dict["rules"]:
                if rule_engine.Rule(
                    sub_rule,
                    context=rule_engine.Context(resolver=resolver),
                ).matches(matchable):
                    self.evaluate_request(rule_dict=rule_dict["rules"][sub_rule])
