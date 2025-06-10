from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response

class DefaultRequest(Request):
    """default request object used in most cases
    """
    def __init__(self):
        """constructor for default request object
        """
        super().__init__()
        self.response = None
        self.method = None
        
    def set_response(self, response: Response):
        """Set the response for this request.

        This method sets the response object for this request and sets this request
        as the request for the response.

        Args:
            response (Response): The response object to set for this request.

        Returns:
            None.
        """
        self.response = response
        if response.get_request() != self:
            response.set_request(self)

    def get_response(self) -> Response:
        """Get the response for this request.

        This method returns the response object for this request.

        Returns:
            Response: The response object for this request.
        """
        return self.response

    def get_method(self) -> str:
        """Get the method of this request.

        This method returns the method of this request.

        Returns:
            str: The method of this request.
        """
        return self.method

    def set_format(self, format_: str):
        """Set the serialization format for this request.

        Args:
            format_ (str): The format name to assign.

        Returns:
            None
        """
        self.format = format_
        return None
