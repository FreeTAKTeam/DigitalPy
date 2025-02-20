
from flask import Blueprint, request, make_response, send_file
from digitalpy.core.network.impl.network_flask_http_blueprints import BlueprintCommunicator


page = Blueprint('FilmologyManagement', __name__)

@page.route('/Movie', methods=["POST"])
def POSTMovie():
    """"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_flow_sync(
        	 "FilmologyManagement__POSTMovie",
        	{
        "body": request.data,
        }) # type: ignore
        return response.get_value("message")[0], 200
    except Exception as e:
    	return str(e), 500
@page.route('/Movie', methods=["DELETE"])
def DELETEMovie():
    """"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_flow_sync(
        	 "FilmologyManagement__DELETEMovie",
        	{
        "ID": request.args.get('ID'),
        }) # type: ignore
        return response.get_value("message")[0], 200
    except Exception as e:
    	return str(e), 500
@page.route('/Movie', methods=["GET"])
def GETMovie():
    """"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_flow_sync(
        	 "FilmologyManagement__GETMovie",
        	{
        }) # type: ignore
        return response.get_value("message"), 200
    except Exception as e:
    	return str(e), 500
@page.route('/Movie', methods=["PATCH"])
def PATCHMovie():
    """"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_flow_sync(
        	 "FilmologyManagement__PATCHMovie",
        	{
        "body": request.data,
        }) # type: ignore
        return response.get_value("message")[0], 200
    except Exception as e:
    	return str(e), 500
@page.route('/Director/<id>', methods=["GET"])
def GETDirectorId(id,):
    """"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_flow_sync(
        	 "FilmologyManagement__GETDirectorId",
        	{
        "ID": request.args.get('ID'),
        "id": id,
        }) # type: ignore
        return response.get_value("message")[0], 200
    except Exception as e:
    	return str(e), 500
@page.route('/Poster', methods=["POST"])
def POSTPoster():
    """"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_flow_sync(
        	 "FilmologyManagement__POSTPoster",
        	{
        "body": request.data,
        }) # type: ignore
        return response.get_value("message")[0], 200
    except Exception as e:
    	return str(e), 500
@page.route('/Poster', methods=["DELETE"])
def DELETEPoster():
    """"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_flow_sync(
        	 "FilmologyManagement__DELETEPoster",
        	{
        "ID": request.args.get('ID'),
        }) # type: ignore
        return response.get_value("message")[0], 200
    except Exception as e:
    	return str(e), 500
@page.route('/Poster', methods=["GET"])
def GETPoster():
    """"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_flow_sync(
        	 "FilmologyManagement__GETPoster",
        	{
        }) # type: ignore
        return response.get_value("message"), 200
    except Exception as e:
    	return str(e), 500
@page.route('/Poster', methods=["PATCH"])
def PATCHPoster():
    """"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_flow_sync(
        	 "FilmologyManagement__PATCHPoster",
        	{
        "body": request.data,
        }) # type: ignore
        return response.get_value("message")[0], 200
    except Exception as e:
    	return str(e), 500
@page.route('/Genre/<id>', methods=["GET"])
def GETGenreId(id,):
    """"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_flow_sync(
        	 "FilmologyManagement__GETGenreId",
        	{
        "ID": request.args.get('ID'),
        "id": id,
        }) # type: ignore
        return response.get_value("message")[0], 200
    except Exception as e:
    	return str(e), 500
@page.route('/Date', methods=["POST"])
def POSTDate():
    """"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_flow_sync(
        	 "FilmologyManagement__POSTDate",
        	{
        "body": request.data,
        }) # type: ignore
        return response.get_value("message")[0], 200
    except Exception as e:
    	return str(e), 500
@page.route('/Date', methods=["DELETE"])
def DELETEDate():
    """"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_flow_sync(
        	 "FilmologyManagement__DELETEDate",
        	{
        "ID": request.args.get('ID'),
        }) # type: ignore
        return response.get_value("message")[0], 200
    except Exception as e:
    	return str(e), 500
@page.route('/Date', methods=["GET"])
def GETDate():
    """"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_flow_sync(
        	 "FilmologyManagement__GETDate",
        	{
        }) # type: ignore
        return response.get_value("message"), 200
    except Exception as e:
    	return str(e), 500
@page.route('/Date', methods=["PATCH"])
def PATCHDate():
    """"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_flow_sync(
        	 "FilmologyManagement__PATCHDate",
        	{
        "body": request.data,
        }) # type: ignore
        return response.get_value("message")[0], 200
    except Exception as e:
    	return str(e), 500
@page.route('/Language/<id>', methods=["GET"])
def GETLanguageId(id,):
    """"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_flow_sync(
        	 "FilmologyManagement__GETLanguageId",
        	{
        "ID": request.args.get('ID'),
        "id": id,
        }) # type: ignore
        return response.get_value("message")[0], 200
    except Exception as e:
    	return str(e), 500
@page.route('/Director', methods=["POST"])
def POSTDirector():
    """"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_flow_sync(
        	 "FilmologyManagement__POSTDirector",
        	{
        "body": request.data,
        }) # type: ignore
        return response.get_value("message")[0], 200
    except Exception as e:
    	return str(e), 500
@page.route('/Director', methods=["DELETE"])
def DELETEDirector():
    """"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_flow_sync(
        	 "FilmologyManagement__DELETEDirector",
        	{
        "ID": request.args.get('ID'),
        }) # type: ignore
        return response.get_value("message")[0], 200
    except Exception as e:
    	return str(e), 500
@page.route('/Director', methods=["GET"])
def GETDirector():
    """"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_flow_sync(
        	 "FilmologyManagement__GETDirector",
        	{
        }) # type: ignore
        return response.get_value("message"), 200
    except Exception as e:
    	return str(e), 500
@page.route('/Director', methods=["PATCH"])
def PATCHDirector():
    """"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_flow_sync(
        	 "FilmologyManagement__PATCHDirector",
        	{
        "body": request.data,
        }) # type: ignore
        return response.get_value("message")[0], 200
    except Exception as e:
    	return str(e), 500
@page.route('/Date/<id>', methods=["GET"])
def GETDateId(id,):
    """"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_flow_sync(
        	 "FilmologyManagement__GETDateId",
        	{
        "ID": request.args.get('ID'),
        "id": id,
        }) # type: ignore
        return response.get_value("message")[0], 200
    except Exception as e:
    	return str(e), 500
@page.route('/Actor', methods=["POST"])
def POSTActor():
    """"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_flow_sync(
        	 "FilmologyManagement__POSTActor",
        	{
        "body": request.data,
        }) # type: ignore
        return response.get_value("message")[0], 200
    except Exception as e:
    	return str(e), 500
@page.route('/Actor', methods=["DELETE"])
def DELETEActor():
    """"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_flow_sync(
        	 "FilmologyManagement__DELETEActor",
        	{
        "ID": request.args.get('ID'),
        }) # type: ignore
        return response.get_value("message")[0], 200
    except Exception as e:
    	return str(e), 500
@page.route('/Actor', methods=["GET"])
def GETActor():
    """"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_flow_sync(
        	 "FilmologyManagement__GETActor",
        	{
        }) # type: ignore
        return response.get_value("message"), 200
    except Exception as e:
    	return str(e), 500
@page.route('/Actor', methods=["PATCH"])
def PATCHActor():
    """"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_flow_sync(
        	 "FilmologyManagement__PATCHActor",
        	{
        "body": request.data,
        }) # type: ignore
        return response.get_value("message")[0], 200
    except Exception as e:
    	return str(e), 500
@page.route('/Movie/<id>', methods=["GET"])
def GETMovieId(id,):
    """"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_flow_sync(
        	 "FilmologyManagement__GETMovieId",
        	{
        "ID": request.args.get('ID'),
        "id": id,
        }) # type: ignore
        return response.get_value("message")[0], 200
    except Exception as e:
    	return str(e), 500
@page.route('/Language', methods=["POST"])
def POSTLanguage():
    """"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_flow_sync(
        	 "FilmologyManagement__POSTLanguage",
        	{
        "body": request.data,
        }) # type: ignore
        return response.get_value("message")[0], 200
    except Exception as e:
    	return str(e), 500
@page.route('/Language', methods=["DELETE"])
def DELETELanguage():
    """"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_flow_sync(
        	 "FilmologyManagement__DELETELanguage",
        	{
        "ID": request.args.get('ID'),
        }) # type: ignore
        return response.get_value("message")[0], 200
    except Exception as e:
    	return str(e), 500
@page.route('/Language', methods=["GET"])
def GETLanguage():
    """"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_flow_sync(
        	 "FilmologyManagement__GETLanguage",
        	{
        }) # type: ignore
        return response.get_value("message"), 200
    except Exception as e:
    	return str(e), 500
@page.route('/Language', methods=["PATCH"])
def PATCHLanguage():
    """"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_flow_sync(
        	 "FilmologyManagement__PATCHLanguage",
        	{
        "body": request.data,
        }) # type: ignore
        return response.get_value("message")[0], 200
    except Exception as e:
    	return str(e), 500
@page.route('/Poster/<id>', methods=["GET"])
def GETPosterId(id,):
    """"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_flow_sync(
        	 "FilmologyManagement__GETPosterId",
        	{
        "ID": request.args.get('ID'),
        "id": id,
        }) # type: ignore
        return response.get_value("message")[0], 200
    except Exception as e:
    	return str(e), 500
@page.route('/Actor/<id>', methods=["GET"])
def GETActorId(id,):
    """"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_flow_sync(
        	 "FilmologyManagement__GETActorId",
        	{
        "ID": request.args.get('ID'),
        "id": id,
        }) # type: ignore
        return response.get_value("message")[0], 200
    except Exception as e:
    	return str(e), 500
@page.route('/Genre', methods=["POST"])
def POSTGenre():
    """"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_flow_sync(
        	 "FilmologyManagement__POSTGenre",
        	{
        "body": request.data,
        }) # type: ignore
        return response.get_value("message")[0], 200
    except Exception as e:
    	return str(e), 500
@page.route('/Genre', methods=["DELETE"])
def DELETEGenre():
    """"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_flow_sync(
        	 "FilmologyManagement__DELETEGenre",
        	{
        "ID": request.args.get('ID'),
        }) # type: ignore
        return response.get_value("message")[0], 200
    except Exception as e:
    	return str(e), 500
@page.route('/Genre', methods=["GET"])
def GETGenre():
    """"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_flow_sync(
        	 "FilmologyManagement__GETGenre",
        	{
        }) # type: ignore
        return response.get_value("message"), 200
    except Exception as e:
    	return str(e), 500
@page.route('/Genre', methods=["PATCH"])
def PATCHGenre():
    """"""
    try:
        # send data to the NetworkInterface
        response = BlueprintCommunicator().send_flow_sync(
        	 "FilmologyManagement__PATCHGenre",
        	{
        "body": request.data,
        }) # type: ignore
        return response.get_value("message")[0], 200
    except Exception as e:
    	return str(e), 500
