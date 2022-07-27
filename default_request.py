class DefaultRequest(Request, AbstractControllerMessage):

    def __init__(self):
        self.response = None
        self.method = None
        
    def set_response(self, response):
        self.response = response
        if response.get_request != self:
            response.set_request(self)
    
    def get_response(self):
        return self.response

    def get_method(self):
        return self.method
    
    def get_matching_routes(request_path):
        matching_routes = []
        default_value_pattern = '([^/]+)'