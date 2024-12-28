
from flask import Blueprint, request, make_response, send_file
from digitalpy.core.network.impl.network_flask_http_blueprints import BlueprintCommunicator


page = Blueprint('component_management', __name__)

@page.route('/Component/RequiredAlfaVersion', methods=["POST"])
def POSTComponentRequiredAlfaVersion():
    """"""
    try:
        # send data to the NetworkInterface
        BlueprintCommunicator().send_message_async(
        	"POSTComponentRequiredAlfaVersion",
        	"^Component^RequiredAlfaVersion",
        	{
        "system_installedAlfaVersion": request.args.get('system_installedAlfaVersion'),
        "body": request.data,
        }) # type: ignore
        return '', 200
    except Exception as e:
    	return str(e), 500
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
        response = BlueprintCommunicator().send_flow_sync(
        	"ComponentManagement_GetComponent",
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
        BlueprintCommunicator().send_flow_sync(
        	"ComponentManagement_GetComponentStatus",
        	{
        "ID": request.args.get('ID'),
        }) # type: ignore
        return '', 200
    except Exception as e:
    	return str(e), 500
@page.route('/ActionKey', methods=["POST"])
def POSTActionKey():
    """TODO"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_message_sync(
        	"POSTActionKey",
        	"^ActionKey",
        	{
        "body": request.data,
        }) # type: ignore
        return response.get_value("message")[0], 200
    except Exception as e:
    	return str(e), 500
@page.route('/ActionKey', methods=["DELETE"])
def DELETEActionKey():
    """TODO"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_message_sync(
        	"DELETEActionKey",
        	"^ActionKey",
        	{
        "ID": request.args.get('ID'),
        }) # type: ignore
        return response.get_value("message")[0], 200
    except Exception as e:
    	return str(e), 500
@page.route('/ActionKey', methods=["GET"])
def GETActionKey():
    """TODO"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_message_sync(
        	"GETActionKey",
        	"^ActionKey",
        	{
        }) # type: ignore
        return response.get_value("message"), 200
    except Exception as e:
    	return str(e), 500
@page.route('/ActionKey', methods=["PATCH"])
def PATCHActionKey():
    """TODO"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_message_sync(
        	"PATCHActionKey",
        	"^ActionKey",
        	{
        "body": request.data,
        }) # type: ignore
        return response.get_value("message")[0], 200
    except Exception as e:
    	return str(e), 500
@page.route('/ComponentRegister', methods=["GET"])
def GETComponentRegister():
    """register a component"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_message_sync(
        	"GETComponentRegister",
        	"^ComponentRegister",
        	{
        "ID": request.args.get('ID'),
        }) # type: ignore
        return response.get_value("message"), 200
    except Exception as e:
    	return str(e), 500
@page.route('/ComponentDiscovery', methods=["GET"])
def GETComponentDiscovery():
    """TODO"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_message_sync(
        	"GETComponentDiscovery",
        	"^ComponentDiscovery",
        	{
        }) # type: ignore
        return response.get_value("message"), 200
    except Exception as e:
    	return str(e), 500
@page.route('/ActionKey/<id>', methods=["GET"])
def GETActionKeyId(id,):
    """TODO"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_message_sync(
        	"GETActionKeyId",
        	"^ActionKey^",
        	{
        "ID": request.args.get('ID'),
        "id": id,
        }) # type: ignore
        return response.get_value("message")[0], 200
    except Exception as e:
    	return str(e), 500
@page.route('/PullComponent', methods=["GET"])
def GETPullComponent():
    """TODO"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_message_sync(
        	"GETPullComponent",
        	"^PullComponent",
        	{
        "url": request.args.get('url'),
        }) # type: ignore
        return response.get_value("message"), 200
    except Exception as e:
    	return str(e), 500