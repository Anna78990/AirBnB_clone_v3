#!/usr/bin/python3
"""
Places
"""
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place

@app_views.route('/places', methods=['GET', 'POST'], strict_slashes=False)
def places():
    """ return json object """
    if request.method == 'GET':
        all_place = storage.all(User)
        places = []
        for k, v in all_place.items():
            places.append(v.to_dict())
        return (jsonify(places))

    if request.method == "POST":
        params = request.get_json()
        if params is None:
            abort(400, "Not a JSON")
        if params['name'] is None:
            abort(400, "Missing name")
        else:
            new = Place(**params)
            serialized = new.to_dict()
            return make_response(jsonify(serialized), 201)

@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def place(place_id):
    """ return json object """
    place = storage.get(Place, place_id)
    if place == None:
        abort(404)

    if request.method == 'GET':
        return (jsonify(place.to_dict()))

    if request.method == "PUT":
        ig_list = ['id', 'created_at', 'updated_at']
        params = request.get_json()
        if params is None:
            abort(400, "Not a JSON")
        for k, v in params.items():
            if k not in ig_list:
                setattr(place, k, v)
                storage.save()
        return make_response(jsonify(place.to_dict), 200)

    if request.method == 'DELETE':
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)
