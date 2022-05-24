#!/usr/bin/python3
"""
Places
"""
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET', 'POST'], strict_slashes=False)
def places(city_id):
    """ return json object """
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)

    if request.method == 'GET':
        place_list = []
        place = storage.all(Place).values()
        for p in place:
            if p.city_id == city_id:
                place_list.append(p.to_dict())
        return (jsonify(place_list))

    if request.method == "POST":
        params = request.get_json()
        if params is None:
            abort(400, "Not a JSON")
        if "user_id" not in params:
            abort(400, "Missing user_id")
        if storage.get(User, params['user_id']) is None:
            abort(404)
        if "name" not in params:
            abort(400, "Missing name")
        else:
            new = Place(**params)
            serialized = new.to_dict()
            return make_response(jsonify(serialized), 201)


@app_views.route('/places/<place_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def place(place_id):
    """ return json object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        return (jsonify(place.to_dict()))

    if request.method == "PUT":
        ig_list = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        params = request.get_json()
        if params is None:
            abort(400, "Not a JSON")
        for k, v in params.items():
            if k not in ig_list:
                setattr(place, k, v)
                storage.save()
        return make_response(jsonify(place.to_dict), 200)

    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return make_response(jsonify({}), 200)
