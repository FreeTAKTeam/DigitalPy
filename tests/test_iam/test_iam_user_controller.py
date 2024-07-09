from digitalpy.core.IAM.persistence.user import User
from digitalpy.core.IAM.persistence.session import Session
from tests.testing_utilities.domain_utilities import initialize_test_network_client
from tests.testing_utilities.facade_utilities import initialize_test_environment, initialize_facade
from digitalpy.core.IAM.configuration import iam_constants

iam_constants.DB_PATH = "sqlite+pysqlite:///:memory:"

def test_connection():
    """
    Test the connection functionality of the IAM user controller.
    """
    request, response = initialize_test_environment()
    iam_facade = initialize_facade("digitalpy.core.IAM.IAM_facade.IAM", request, response)
    network_client = initialize_test_network_client()

    request.set_value("connection", network_client)
    iam_facade.execute("connection")

    request.set_value("uid", str(network_client.get_oid()))
    iam_facade.execute("get_session_by_uid")
    session: Session = response.get_value("session")
    assert session is not None
    assert session.uid == str(network_client.get_oid())
    assert session.session_contacts[0].user.callsign == "Anonymous"
