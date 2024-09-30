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
