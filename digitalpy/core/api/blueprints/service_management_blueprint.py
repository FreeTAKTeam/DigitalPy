from flask import Blueprint, request, make_response, g

from digitalpy.core.network.impl.network_flask_http_blueprints import (
    BlueprintCommunicator,
)

page = Blueprint("ServiceManagement", __name__)


@page.route("/ServiceStatus", methods=["GET"])
def GETServiceStatus():
    """Gets the status of a given service."""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_flow_sync(
            "ServiceManagement_GetServiceStatus",
            {
                "service_id": request.args.get("service_id"),
            },
        )  # type: ignore
        return make_response(response.get_value("message"), 200)
    except Exception as e:
        return make_response(str(e), 500)


@page.route("/ReloadSystemHealth", methods=["GET"])
def GETReloadSystemHealth():
    """Reloads the system health by getting the current system information from the operating system."""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_flow_sync("ServiceManagement_GetReloadSystemHealth", {})  # type: ignore
        return make_response(response.get_value("message"), 200)
    except Exception as e:
        return make_response(str(e), 500)


@page.route("/Service/Stop", methods=["POST"])
def POSTServiceStop():
    """Stops the service."""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_flow_sync(
            "ServiceManagement_StopService",
            {
                "service_id": request.args.get("service_id"),
            },
        )  # type: ignore
        return make_response(response.get_value("message"), 200)
    except Exception as e:
        return make_response(str(e), 500)


@page.route("/Service/Start", methods=["POST"])
def POSTServiceStart():
    """Starts the service."""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_flow_sync(
            "ServiceManagement_StartService",
            {
                "service_id": request.args.get("service_id"),
            },
        )  # type: ignore
        return make_response(response.get_value("message"), 200)
    except Exception as e:
        return make_response(str(e), 500)


@page.route("/Service/Topics", methods=["GET"])
def GETServiceTopics():
    """Gets the topics a given service is subscribed."""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_flow_sync(
            "ServiceManagement_GetServiceTopics",
            {
                "service_id": request.args.get("service_id"),
            },
        )  # type: ignore
        return make_response(response.get_value("message"), 200)
    except Exception as e:
        return make_response(str(e), 500)


@page.route("/Service/Topic", methods=["PUT"])
def PUTServiceTopics():
    """Puts the topics a given service is subscribed."""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_flow_sync(
            "ServiceManagement_PutServiceTopic",
            {
                "service_id": request.args.get("service_id"),
                "topic": request.get_data(),
            },
        )  # type: ignore
        return make_response(response.get_value("message"), 200)
    except Exception as e:
        return make_response(str(e), 500)


@page.route("/Service/Topic", methods=["DELETE"])
def DELETEServiceTopics():
    """Deletes the topics a given service is subscribed."""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_flow_sync(
            "ServiceManagement_DeleteServiceTopic",
            {
                "service_id": request.args.get("service_id"),
                "topic": request.get_data(),
            },
        )  # type: ignore
        return make_response(response.get_value("message"), 200)
    except Exception as e:
        return make_response(str(e), 500)
