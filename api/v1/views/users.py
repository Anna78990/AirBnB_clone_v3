#!/usr/bin/python3
"""
User
"""
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def users():
    """ return json object """
    if request.method == 'GET':
        all_user = storage.all(User)
        users = []
        for k, v in all_user.items():
            users.append(v.to_dict())
        return (jsonify(users))

    if request.method == "POST":
        params = request.get_json()
        if params is None:
            abort(400, "Not a JSON")
        if 'name' not in params.keys():
            abort(400, "Missing name")
        else:
            new = User(**params)
            serialized = new.to_dict()
            return make_response(jsonify(serialized), 201)


@app_views.route('/users/<user_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def user(user_id):
    """ return json object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if request.method == 'GET':
        return (jsonify(user.to_dict()))

    if request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == "PUT":
        put_list = ['id', 'email', 'created_at', 'updated_at']
        params = request.get_json()
        if params is None:
            abort(400, "Not a JSON")
        for k, v in params.items():
            if k not in put_list:
                setattr(user, k, v)
        storage.save()

        return make_response(jsonify(user.to_dict()), 200)
