
from flask import Blueprint, request, make_response, send_file
from digitalpy.core.network.impl.network_flask_http_blueprints import BlueprintCommunicator


page = Blueprint('Files', __name__)

@page.route('/file/get-or-create', methods=["GET"])
def GETFileGet-or-create():
    """get a file from the filesystem based on the specified path or create a new file if one does not yet exist."""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_message_sync(
        	"GETFileGet-or-create",
        	"^file^get-or-create",
        	{
        "path": request.args.get('path'),
        }) # type: ignore
        return response.get_value("message"), 200
    except Exception as e:
    	return str(e), 500
@page.route('/folder/get-or-create', methods=["GET"])
def GETFolderGet-or-create():
    """get a folder from the filesystem based on the specified path or create a new folder if one does not yet exist."""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_message_sync(
        	"GETFolderGet-or-create",
        	"^folder^get-or-create",
        	{
        "path": request.args.get('path'),
        }) # type: ignore
        return response.get_value("message"), 200
    except Exception as e:
    	return str(e), 500
@page.route('/folder', methods=["GET"])
def GETFolder():
    """get a folder based on the specified path"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_message_sync(
        	"GETFolder",
        	"^folder",
        	{
        "path": request.args.get('path'),
        }) # type: ignore
        return response.get_value("message"), 200
    except Exception as e:
    	return str(e), 500
@page.route('/folder', methods=["POST"])
def POSTFolder():
    """create a new folder in the file system at the specified path"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_message_sync(
        	"POSTFolder",
        	"^folder",
        	{
        "path": request.args.get('path'),
        }) # type: ignore
        return response.get_value("message")[0], 200
    except Exception as e:
    	return str(e), 500
@page.route('/folder', methods=["DELETE"])
def DELETEFolder():
    """delete the given folder instance."""
    try:
        # send data to the NetworkInterface
        BlueprintCommunicator().send_message_async(
        	"DELETEFolder",
        	"^folder",
        	{
        "recursive": request.args.get('recursive'),
        }) # type: ignore
        return '', 200
    except Exception as e:
    	return str(e), 500
@page.route('/file', methods=["GET"])
def GETFile():
    """get a file from the file system based on the specified path"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_message_sync(
        	"GETFile",
        	"^file",
        	{
        "path": request.args.get('path'),
        }) # type: ignore
        return response.get_value("message"), 200
    except Exception as e:
    	return str(e), 500
@page.route('/file', methods=["POST"])
def POSTFile():
    """create a new file in the filesystem at the specified path."""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_message_sync(
        	"POSTFile",
        	"^file",
        	{
        "path": request.args.get('path'),
        }) # type: ignore
        return response.get_value("message")[0], 200
    except Exception as e:
    	return str(e), 500
@page.route('/file', methods=["DELETE"])
def DELETEFile():
    """delete the file at the specified path"""
    try:
        # send data to the NetworkInterface
        BlueprintCommunicator().send_message_async(
        	"DELETEFile",
        	"^file",
        	{
        }) # type: ignore
        return '', 200
    except Exception as e:
    	return str(e), 500
