#!/usr/bin/python3
"""
Creates amenities
"""
from models import storage
from models.amenity import Amenity
from flask import jsonify, abort, request
from api.v1.views import app_views


@app_views.route("/amenities/", methods=["GET"])
def get_amenities():
    """Obtaining all the Amenities"""
    amens = [amenity.to_dict() for amenity in storage.all(Amenity).values()]
    return (jsonify(amens)), 200


@app_views.route("/amenities/<amenity_id>", methods=["GET"])
def get_amenity(amenity_id):
    """Obtaining a specific Amenity"""
    if storage.get(Amenity, amenity_id) is not None:
        amenity = storage.get(Amenity, amenity_id)
        return jsonify(amenity.to_dict()), 200
    else:
        abort(404)


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"])
def delete_amenity(amenity_id):
    """Deleting an Amenity"""
    if storage.get(Amenity, amenity_id) is not None:
        amenity = storage.get(Amenity, amenity_id)
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/amenities/", methods=["POST"])
def create_amenity():
    """Creating an Amenity"""
    if not request.is_json:
        abort(400, "Not a JSON")
    if 'name' not in request.get_json():
        abort(400, "Missing name")
    new_amenity = Amenity(name=request.json['name'])
    storage.new(new_amenity)
    storage.save()
    amenity = new_amenity.to_dict()
    return jsonify(amenity), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def edit_amenity(amenity_id):
    """Editing an Amenity"""
    if not request.is_json:
        abort(400, "Not a JSON")
    if storage.get(Amenity, amenity_id) is not None:
        amenity = storage.get(Amenity, amenity_id)
        amenity.name = request.json['name']
        storage.save()
        amenity = storage.get(Amenity, amenity_id)
        return jsonify(amenity.to_dict()), 200
    else:
        abort(404)
