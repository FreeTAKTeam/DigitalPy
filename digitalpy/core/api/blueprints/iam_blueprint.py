
from flask import Blueprint, request, make_response, g
from flask_jwt_extended import get_jwt, get_csrf_token

from digitalpy.core.network.impl.network_flask_http_blueprints import BlueprintCommunicator

page = Blueprint('IAM', __name__)


@page.route('/Authenticate', methods=["POST"])
def GETAuthenticate():
    """Creates a new employee record."""
    try:
        request_body: dict = request.get_json(force=True)
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_message_sync(
            "authenticate",
            "",
            {
                "user_id": request_body.get("user_id"),
                "name": request_body.get("name"),
                "password": request_body.get("password")
            })  # type: ignore

        # TODO: update to use proper model
        resp = make_response(
            {
                "authenticated": response.get_value("authenticated"),
                "jwt": g._iam_encoded_jwt,
            }, 200)
        return resp
    except Exception as e:
        return str(e), 500
