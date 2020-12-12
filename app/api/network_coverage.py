import requests
from flask import abort
from flask import jsonify
from sqlalchemy import func

from app import db
from app.api import bp
from app.db_models.operator import Operator
from app.db_models.position import Position
from papernest import app


def get_coordinates_from_address(address):
    """
    Calls government API and returns x,y coordinates in long,lat format for a given input address
    :param address: the address to look for
    :return: tuple of coordinates (long, lat)
    """
    api_address = app.config['GOUV_API_ADDRESS']
    result = requests.get(url=api_address, params={"q": address})
    json = result.json()
    if "features" not in json or not json["features"]:
        abort(400, "Could not find any valid address for the input provided on government API " + api_address)
    if "geometry" not in json["features"][0] or "coordinates" not in json["features"][0]["geometry"]:
        abort(500, "The result from government api " + api_address + " was malformed and could not be read.")
    return json["features"][0]["geometry"]["coordinates"]


@bp.route('/address_coordinates/<string:address>/')
def get_coordinates(address):
    return jsonify(get_coordinates_from_address(address))


@bp.route('/network_coverage/<string:address>/', defaults={'max_distance': 1000})
@bp.route('/network_coverage/<string:address>/<float:max_distance>')
def get_coverage(address, max_distance):
    """
    Get GPS coordinates from an address and looks for all operators available in distance range of max_distance.
    :param address the input address
    :param max_distance in meters between initial address and operator positions
    :return: output JSON with availability (2g, 3g, 4g) of each operator in range.
    """
    coordinates = get_coordinates_from_address(address)
    query = db.session.query(
        Operator.name.label("Operator"),
        func.bool_or(Position.has_2g).label("2G"),
        func.bool_or(Position.has_3g).label("3G"),
        func.bool_or(Position.has_4g).label("4G")
    ).filter(
        Operator.mcc_mnc == Position.operator_code
    ).filter(
        Position.within_distance_func(coordinates, max_distance)
    ).group_by(Operator.name)
    output_headers = [desc["name"] for desc in query.column_descriptions]
    return jsonify([dict(zip(output_headers, row)) for row in query.all()])
