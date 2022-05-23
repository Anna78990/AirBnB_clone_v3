#!/usr/bin/python3
""" api definition
"""
from models import storage
from flask import Flask, Blueprint, jsonify
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(e):
    """ if 404 error occurs, return json objects """
    return jsonify({"error": "Not found"})


@app.teardown_appcontext
def teardown_appcontext(exception):
    """ storage close """
    storage.close()


if __name__ == "__main__":
    host_e = getenv("HBNB_API_HOST")
    if host_e is None:
        host_e = "0.0.0.0"
    port_e = getenv("HBNB_API_PORT")
    if port_e is None:
        port_e = "5000"
    app.debug = True
    app.run(host=host_e, port=port_e, threaded=True)
