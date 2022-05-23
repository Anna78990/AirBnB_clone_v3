#!/usr/bin/python3
"""
Amenity
"""
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity

@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def amenities():
    """ return json object """
    if request.method == 'GET':
        all_amenity = storage.all(Amenity)
        amenities = []
        for k, v in all_amenity.items():
            amenities.append(v.to_dict)
        return (jsonify(amenities))

    if request.method == "POST":
        params = request.get_json()
        if params is None:
            abort(400, "Not a JSON")
        if params['name'] is None:
            abort(400, "Missing name")
        else:
            new = Amenity(**params)
            serialized = new.to_dict()
            return make_response(jsonify(serialized), 201)

@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def amenity_id(amenity_id):
    """ return json object """
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)

    if request.method == 'GET':
        return (jsonify(obj))

    if request.method == "PUT":
        ig_list = ['id', 'created_at', 'updated_at']
        params = request.get_json()
        if params is None:
            abort(400, "Not a JSON")
        for k, v in params.items():
            if k not in ig_list:
                obj[k] = v
        storage.save()
        return make_response(jsonify(obj.to_dict), 200)

    if request.method == "DELETE":
        obj.delete()
        storage.save()
        return make_response(jsonify({}), 200)
