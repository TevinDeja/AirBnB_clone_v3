#!/usr/bin/python3
"""
Reviews API endpoint
"""
from models import storage
import models
from models.place import Place
from models.amenity import Amenity
from models.user import User
from flask import jsonify, abort, request
from api.v1.views import app_views


@app_views.route("/places/<place_id>/amenities", methods=["GET"])
def get_amenities_by_place(place_id):
    """Handles amenities route"""
    if storage.get(Place, place_id) is not None:
        place = storage.get(Place, place_id)
        if models.storage_t == 'db':
            all = place.amenities
        else:
            amenity_ids = place.amenity_ids
            all = [storage.get(Amenity, amenity) for amenity in amenity_ids]
        amenities = [amenity.to_dict() for amenity in all]
        mat = [review for review in amenities if review.get('place_id') == place.id]
        return jsonify(mat)
    else:
        abort(404)


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST"])
def link_amenity(place_id, amenity_id):
    """Linking Amenities route"""
    if storage.get(Place, place_id) is not None:
        place = storage.get(Place, place_id)
        if storage.get(Amenity, amenity_id) is not None:
            amenity = storage.get(Amenity, amenity_id)
            if amenity in place.amenities:
                if models.storage_t == 'db':
                    place.amenities.append(amenity)
                else:
                    place.amenity_ids.append(amenity_id)
                storage.save()
            else:
                abort(404)
            return jsonify(amenity.to_dict()), 201
    else:
        abort(404)

    
@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["DELETE"])
def delete_amenity_by_place(place_id, amenity_id):
    """Deleting Amenities"""
    if storage.get(Place, place_id) is not None:
        place = storage.get(Place, place_id)
        if storage.get(Amenity, amenity_id) is not None:
            amenity = storage.get(Amenity, amenity_id)
            if amenity in place.amenities:
                if models.storage_t == 'db':
                    place.amenities.remove(amenity)
                else:
                    place.amenity_ids.remove(amenity_id)
                storage.save()
            else:
                abort(404)
            return jsonify({}), 200
    else:
        abort(404)
