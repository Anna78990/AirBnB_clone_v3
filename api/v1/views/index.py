#!/usr/bin/python3
""" create a route /status on the object app_views
    that returns a JSON: "status": "OK" """


from api.v1.views import app_views
from v1 import stats

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}
counter = count()
    with open('stats', 'w') as f:
        with redirect_stdout(f):
            print("\"{}\": {}".format(cls, counter)
@app_views.route('/status')
def status():
    return ("\"status\": \"OK\"")
