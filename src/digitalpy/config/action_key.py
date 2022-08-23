from digitalpy.config.action_key_provider import ActionKeyProvider


class ActionKey:
    action_delimiter = "?"
    def create_key(resource, context, action):
        return resource+ActionKey.action_delimiter+context+ActionKey.action_delimiter+action
    
    def parse_key(action_key):
        action_key_parts = action_key.split(ActionKey.action_delimiter)
        resource = action_key_parts[0]
        context = action_key_parts[1]
        action = action_key_parts[2]
        return {'resource': resource, 'context': context, 'action': action}
    
    def get_best_match(action_key_provider: ActionKeyProvider, resource, context, action):
        has_resource = len(resource) > 0
        has_context = len(context) > 0
        has_action = len(action) > 0

        if has_resource and has_context and has_action:
            key = ActionKey.create_key(resource, context, action)
            if action_key_provider.contains_key(key):
                return key
            
        # check resource??action
        if has_resource and has_action:
            key = ActionKey.create_key(resource, '', action)
            if action_key_provider.contains_key(key):
                return key
        
        

        # check resource?context?
        if has_resource and has_context :
            key = ActionKey.create_key(resource, context, '')
            if action_key_provider.contains_key(key):
                return key
            
        

        # check ?context?action
        if has_context and has_action :
            key = ActionKey.create_key('', context, action)
            if action_key_provider.contains_key(key):
                return key
        
        

        # check ??action
        if has_action:
            key = ActionKey.create_key('', '', action)
            if action_key_provider.contains_key(key):
                return key
        
        

        # check resource??
        if has_resource:
            key = ActionKey.create_key(resource, '', '')
            if action_key_provider.contains_key(key):
                return key
            
        

        # check ?context?
        if has_context:
            key = ActionKey.create_key('', context, '')
            if action_key_provider.contains_key(key):
                return key
        
        

        # check ??
        key = ActionKey.create_key('', '', '')
        if action_key_provider.contains_key(key):
            return key
        

        # no key found for requested key
        return ''