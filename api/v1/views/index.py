#!/usr/bin/python3
"""
Creating routes
"""
from flask import jsonify
from models import storage
from api.v1.views import app_views
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.base_model import BaseModel


classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review,
           "states": State, "users": User}


@app_views.route("/status", methods=["GET"])
def status_ok():
    """Yields OK"""
    return (jsonify({
        "status": "OK"
    }))


@app_views.route("/stats", methods=["GET"])
def stats():
    """ Yields statistics for the database"""
    stat_dict = {}
    for cls in classes:
        stat_dict[cls] = storage.count(classes[cls])

    return (jsonify(stat_dict))
