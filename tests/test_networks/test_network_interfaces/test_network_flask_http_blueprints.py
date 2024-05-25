from flask import Blueprint
from tests.testing_utilities.domain_utilities import initialize_test_service_description
from tests.testing_utilities.facade_utilities import initialize_test_environment
from tests.testing_utilities.network_utilities import send_get_request
from digitalpy.core.network.impl.network_flask_http_blueprints import FlaskHTTPNetworkBlueprints, BlueprintCommunicator
import pytest_asyncio
import asyncio
import pytest
from digitalpy.core.main.object_factory import ObjectFactory

testBlueprint = Blueprint('Test', __name__)

@testBlueprint.route('/testSyncGet', methods=['GET'])
def syncGet():
    print("received request")
    try:
        resp = BlueprintCommunicator().send_message_sync(
            "GETSyncTest",
            "^Test",
            {
                "key": "value"
            }
        )
        return resp.get_value("message")
    except Exception as e:
        return str(e)

@pytest.mark.asyncio
async def test_network_connection():
    """this test is responsible for testing the a new connection to the network, and the response to that connection
    the first half tests that the connection action is triggered when no session cookie is sent, and the second half 
    tests that the connection action is not triggered when a session cookie is sent.
    """
    # initialize the test environment
    request, response = initialize_test_environment()
    network = FlaskHTTPNetworkBlueprints()
    test_service_desc = initialize_test_service_description(request, response)
    network.intialize_network('127.0.0.1', 5000, [testBlueprint], test_service_desc)
    await asyncio.sleep(3)

    # send a request to the network and process it
    request_task = asyncio.create_task(send_get_request('http://' + network.host + ':' + str(network.port) + '/testSyncGet'))
    requests = []
    while len(requests) == 0:
        requests = network.service_connections()
        await asyncio.sleep(1)
    assert requests[0].get_value("action", None) == "connection"
    response = ObjectFactory.get_new_instance("response")
    response.set_value("message", "success")
    response.id = requests[0].id
    network.send_response(response)

    # check the response
    http_response, http_session = await request_task
    assert http_response == "success"
    assert http_session is not None

    # send a second request to the network and process it
    request_task = asyncio.create_task(send_get_request('http://' + network.host + ':' + str(network.port) + '/testSyncGet', {"session": http_session}))
    requests = []
    while len(requests) == 0:
        requests = network.service_connections()
        await asyncio.sleep(1)
    assert requests[0].get_value("action", None) != "connection"
    response = ObjectFactory.get_new_instance("response")
    response.set_value("message", "success request 2")
    response.id = requests[0].id
    network.send_response(response)

    # check the response
    http_response, http_session = await request_task
    assert http_response == "success request 2"

    # stop the network
    network.teardown_network()