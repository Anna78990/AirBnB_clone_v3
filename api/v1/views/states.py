#!/usr/bin/python3
"""
States
"""
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def states():
    """ return json object """
    if request.method == 'GET':
        all_states = storage.all(State)
        states = []
        for k, v in all_states.items():
            states.append(v.to_dict())
        return (jsonify(states))

    if request.method == "POST":
        params = request.get_json()
        if params is None:
            abort(400, "Not a JSON")
        if params['name'] is None:
            abort(400, "Missing name")
        else:
            new = State(**params)
            serialized = new.to_dict()
            return make_response(jsonify(serialized), 201)


@app_views.route('/states/<state_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def state_id(state_id):
    """ return json object """
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)

    if request.method == 'GET':
        return (jsonify(obj.to_dict()))

    if request.method == "PUT":
        ig_list = ['id', 'created_at', 'updated_at']
        params = request.get_json()
        if params is None:
            abort(400, "Not a JSON")
        for k, v in params.items():
            if k not in ig_list:
                setattr(obj, k, v)
        storage.save()
        return make_response(jsonify(obj.to_dict()), 200)

    if request.method == "DELETE":
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)
