#!/usr/bin/python3
""" create a route /status on the object app_views
    that returns a JSON: "status": "OK" """


from api.v1.views import app_views


@app_views.route('/status')
def status():
    return ("\"status\": \"OK\"")
