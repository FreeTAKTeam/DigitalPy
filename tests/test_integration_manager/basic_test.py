import threading
from digitalpy.core.zmanager.integration_manager import IntegrationManager
import zmq

def test_basic_forwarding():
    # Create an instance of the IntegrationManager class
    manager = IntegrationManager()

    # Start the main loop in a separate thread
    thread = threading.Thread(target=manager.main)
    thread.start()

    # Create a client socket to send a request to the server
    client_socket = zmq.Context().socket(zmq.PUSH)
    client_socket.connect("tcp://127.0.0.1:12345")

    # Create a subscriber socket to receive the response from the server
    subscriber_socket = zmq.Context().socket(zmq.SUB)
    subscriber_socket.connect("tcp://127.0.0.1:12346")
    subscriber_socket.setsockopt(zmq.SUBSCRIBE, b'')  # subscribe to all messages

    # Send a request to the server
    request_protocol = "test"
    request_object = "request object"
    request = f"{request_protocol},{request_object}"
    client_socket.send_string(request)



    # Wait for a response from the server
    subject, response_object = subscriber_socket.recv_string().split(" ", 1)
    assert subject == f"/{request_protocol}/message"
    assert response_object == request_object

    # Stop the main loop
    thread.join()