#!/usr/bin/python3
"""
States API endpoint
"""
from models import storage
from models.state import State
from flask import jsonify, abort, request
from api.v1.views import app_views


@app_views.route("/states/", methods=["GET"])
def get_states():
    """Obtaining all the States"""
    states = [state.to_dict() for state in storage.all(State).values()]
    return (jsonify(states)), 200


@app_views.route("/states/<state_id>", methods=["GET"])
def get_state(state_id):
    """Obtaining a specific State"""
    if storage.get(State, state_id) is not None:
        state = storage.get(State, state_id)
        return jsonify(state.to_dict()), 200
    else:
        abort(404)


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """Deleting a State"""
    if storage.get(State, state_id) is not None:
        state = storage.get(State, state_id)
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/states/", methods=["POST"])
def create_state():
    """Creating a State"""
    if not request.is_json:
        abort(400, "Not a JSON")
    if 'name' not in request.get_json():
        abort(400, "Missing name")
    new_state = State(name=request.json['name'])
    storage.new(new_state)
    storage.save()
    state = new_state.to_dict()
    return jsonify(state), 201


@app_views.route("/states/<state_id>", methods=["PUT"])
def edit_state(state_id):
    """Editing a State"""
    if not request.is_json:
        abort(400, "Not a JSON")
    if storage.get(State, state_id) is not None:
        state = storage.get(State, state_id)
        if 'name' in request.get_json():
            state.name = request.json['name']
        storage.save()
        state = storage.get(State, state_id)
        return jsonify(state.to_dict()), 200
    else:
        abort(404)
