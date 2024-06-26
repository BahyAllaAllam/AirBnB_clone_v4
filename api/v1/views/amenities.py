#!/usr/bin/python3
"""Api views for Ameities."""

from . import app_views
from flask import abort, jsonify, make_response, request, Response
from models import storage
from models.amenity import Amenity
import json


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    """Get all amenity objects."""
    amenities = [obj.to_dict()
                 for obj in storage.all("Amenity").values()]
    return jsonify(amenities)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenity_by_id(amenity_id):
    """Get an Amenity object by id."""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_by_id(amenity_id):
    """Delete an Amenity object by id."""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Create an Amenity object."""
    if not request.is_json:
        return make_response('Not a JSON', 400)
    data = request.get_json()
    if 'name' not in data:
        return make_response("Missing name", 400)
    amenity_obj = Amenity(**data)
    amenity_obj.save()
    return jsonify(amenity_obj.to_dict()), 201


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Update an Amenity object by id."""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if not request.is_json:
        return make_response("Not a JSON", 400)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
