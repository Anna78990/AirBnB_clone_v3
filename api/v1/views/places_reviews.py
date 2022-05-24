#!/usr/bin/python3
"""
Amenity
"""
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User

@app_views.route('places/<place_id>/reviews', methods=['GET', 'POST'], strict_slashes=False)
def place_reviews(place_id):
    """ return json object """
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)

    if request.method == 'GET':
        return (jsonify(obj))

    if request.method == "POST":
        params = request.get_json()
        if params is None:
            abort(400, "Not a JSON")
        if params['user_id'] is None:
            abort(400, "Missing user_id")
        else:
            user_id = params['user_id']
            if storage.get(User, user_id) is None:
                abort(404)
        if params['text'] is None:
            abort(404, "Missing text")
        else:
            new = User(**params)
            serialized = new.to_dict()
            return make_response(jsonify(serialized), 201)


@app_views.route('/reviews/<review_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def review_id(review_id):
    """ return json object """
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)

    if request.method == 'GET':
        return (jsonify(obj))

    if request.method == "PUT":
        ig_list = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        params = request.get_json()
        if params is None:
            abort(400, "Not a JSON")
        for k, v in params.items():
            if k not in ig_list:
                setattr(obj, k, v)
        storage.save()
        return make_response(jsonify(obj.to_dict), 200)

    if request.method == "DELETE":
        obj.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)
