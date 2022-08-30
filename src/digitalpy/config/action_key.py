from digitalpy.config.action_key_provider import ActionKeyProvider


class ActionKey:
    """ An action key is a combination of a resource, context and action that is
    represented as a string. ActionKey is a helper class for handling
    action keys.
    """
    action_delimiter = "?"
    
    @staticmethod
    def create_key(resource: str, context: str, action: str):
        """Create an action key from the given values"""
        return resource+ActionKey.action_delimiter+context+ActionKey.action_delimiter+action
    
    @staticmethod
    def parse_key(action_key):
        """Parse an action"""
        action_key_parts = action_key.split(ActionKey.action_delimiter)
        resource = action_key_parts[0]
        context = action_key_parts[1]
        action = action_key_parts[2]
        return {'resource': resource, 'context': context, 'action': action}
    
    @staticmethod
    def get_best_match(action_key_provider: ActionKeyProvider, resource: str, context: str, action: str):
        """Get an action key that matches a given combination of resource, context, action best."""
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