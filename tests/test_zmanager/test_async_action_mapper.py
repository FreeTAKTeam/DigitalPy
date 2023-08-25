from unittest.mock import MagicMock, patch
from digitalpy.core.zmanager.impl.async_action_mapper import AsyncActionMapper
from digitalpy.core.zmanager.impl.default_request import DefaultRequest
from digitalpy.core.zmanager.impl.default_response import DefaultResponse
from digitalpy.core.parsing.impl.default_formatter import DefaultFormatter
from digitalpy.core.parsing.impl.pickled_format import PickledFormat

@patch('zmq.Context')
def test_process_action_no_return(zmq_context_mock):
    request = DefaultRequest()
    response = DefaultResponse()

    formatter = DefaultFormatter({"pickled": PickledFormat()})

    async_action_mapper = AsyncActionMapper(MagicMock(), MagicMock(), formatter, MagicMock(), MagicMock())

    request.set_sender("test_sender")
    request.set_action("test_action")
    request.set_context("test_context")
    request.set_format("pickled")
    request.set_id("test_id")
    request.set_value("test_value", "test_value")

    async_action_mapper.process_action(request, response, False, "test_protocol")