#!/usr/bin/python3
from models import storage
from models.city import City
from models.state import State
print("state objects: {}".format(storage.count(State)))
id = list(storage.all(State).values())[0].id
print("city: {}".format(storage.get(State, id)))

