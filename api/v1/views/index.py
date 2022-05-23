#!/usr/bin/python3
"""
index
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """ return json object """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """ return json object with the number of each objects """
    classes = {"amenities": "Amenity", "cities": "City",
               "places": "Place","reviews": "Review","states": "State","users": "User"}
    for k, v in classes.items():
        classes[k] = storage.count(v)
    return jsonify(classes)
