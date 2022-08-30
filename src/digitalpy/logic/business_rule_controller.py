from digitalpy.routing.controller import Controller

class BusinessRuleController(Controller):
    def __init__(self, business_rules, rule_context, **kwargs):
        super().__init__(**kwargs)
        