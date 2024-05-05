#!/usr/bin/python3
"""
Index file for setting up th api
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


classes = {"users": User,
           "places": Place,
           "states": State,
           "cities": City,
           "amenities": Amenity,
           "reviews": Review}


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns the status in json format."""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """Returns count of all objs in json format."""
    count_objs = {}
    for key, value in classes.items():
        count_objs[key] = storage.count(value)
    return jsonify(count_objs)
