#!/usr/bin/python3
"""Api views for Cities"""

from api.v1.views import app_views
from flask import jsonify, Response, abort, request, make_response
from models import storage
from models.city import City
from models.state import State
from werkzeug.exceptions import BadRequest
import json


@app_views.route('/states/<string:state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities_by_state(state_id):
    """"Retrieves a list of all Cities objects
    associated with a given state."""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city_by_id(city_id):
    """Retrieves a city by id."""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city_by_id(city_id):
    """Delete city by id."""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<string:state_id>/cities/', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Create a city by state id."""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if not request.is_json:
        return make_response("Not a JSON", 400)
    data = request.get_json()
    if 'name' not in data:
        return make_response("Missing name", 400)
    city_obj = City(name=data["name"], state_id=state_id)
    city_obj.save()
    return jsonify(city_obj.to_dict()), 201


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """Update a city by id."""
    if not request.is_json:
        return make_response("Not a JSON", 400)
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
