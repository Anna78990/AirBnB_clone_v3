#!/usr/bin/python3
"""
Flask route that returns json status response
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'], strict_slashes=False)
def cities_per_state(state_id):
    """
        cities route to handle http method for requested cities by state
    """
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(state_obj.to_dict())

    if request.method == 'POST':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        if req_json.get("name") is None:
            abort(400, 'Missing name')
        new = City()
        for k, v in req_json.items():
            setattr(new, k, v)
        storage.save()
        serialized = new.to_dict()
        return make_response(jsonify(serialized), 201)

@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def cities_with_id(city_id):
    """
        cities route to handle http methods for given city
    """
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(city_obj.to_dict())

    if request.method == 'DELETE':
        storage.delete(city_obj)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        req_json = request.get_json()
        ig_list = ['id', 'state_id', 'created_at', 'updated_at']
        if req_json is None:
            abort(400, 'Not a JSON')
        for k, v in req_json.items():
            if k not in ig_list:
                setattr(city_obj, k, v)
        storage.save()
        return make_response(jsonify(city_obj.to_dict()), 200)
