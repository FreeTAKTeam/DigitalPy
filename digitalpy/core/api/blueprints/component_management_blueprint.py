
from flask import Blueprint, request, make_response, send_file
from digitalpy.core.network.impl.network_flask_http_blueprints import BlueprintCommunicator


page = Blueprint('Component_Management', __name__)

@page.route('/Component', methods=["DELETE"])
def DELETEComponent():
    """TODO"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_message_sync(
        	"DELETEComponent",
        	"^Component",
        	{
        "ID": request.args.get('ID'),
        }) # type: ignore
        return response.get_value("message")[0], 200
    except Exception as e:
    	return str(e), 500
@page.route('/Component', methods=["POST"])
def POSTComponent():
    """TODO"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_message_sync(
        	"POSTComponent",
        	"^Component",
        	{
        "body": request.data,
        }) # type: ignore
        return response.get_value("message")[0], 200
    except Exception as e:
    	return str(e), 500
@page.route('/Component', methods=["GET"])
def GETComponent():
    """TODO"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_message_sync(
        	"GETComponent",
        	"^Component",
        	{
        }) # type: ignore
        return response.get_value("message"), 200
    except Exception as e:
    	return str(e), 500
@page.route('/Component', methods=["PATCH"])
def PATCHComponent():
    """TODO"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_message_sync(
        	"PATCHComponent",
        	"^Component",
        	{
        "body": request.data,
        }) # type: ignore
        return response.get_value("message")[0], 200
    except Exception as e:
    	return str(e), 500
@page.route('/Component/<id>', methods=["GET"])
def GETComponentId(id,):
    """TODO"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_message_sync(
        	"GETComponentId",
        	"^Component^",
        	{
        "ID": request.args.get('ID'),
        "id": id,
        }) # type: ignore
        return response.get_value("message")[0], 200
    except Exception as e:
    	return str(e), 500
@page.route('/ComponentStatus', methods=["GET"])
def GETComponentStatus():
    """returns the status of the component or the last error"""
    try:
        # send data to the NetworkInterface
        BlueprintCommunicator().send_message_async(
        	"GETComponentStatus",
        	"^ComponentStatus",
        	{
        "ID": request.args.get('ID'),
        }) # type: ignore
        return '', 200
    except Exception as e:
    	return str(e), 500
@page.route('/ComponentRegister', methods=["POST"])
def POSTComponentRegister():
    """register a component"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_message_sync(
        	"POSTComponentRegister",
        	"^ComponentRegister",
        	{
        "ID": request.args.get('ID'),
        }) # type: ignore
        return response.get_value("message")[0], 200
    except Exception as e:
    	return str(e), 500
@page.route('/ComponentDiscovery', methods=["GET"])
def GETComponentDiscovery():
    """discover a list of components, other than list components, returns also components that are not activated or installed"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_message_sync(
        	"GETComponentDiscovery",
        	"^ComponentDiscovery",
        	{
        "Directory": request.args.get('Directory'),
        "import_root": request.args.get('import_root'),
        }) # type: ignore
        return response.get_value("message"), 200
    except Exception as e:
    	return str(e), 500
