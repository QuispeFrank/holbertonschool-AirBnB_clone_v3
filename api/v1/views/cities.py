#!/usr/bin/python3
"""view of City objects"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 methods=["GET"], strict_slashes=False)
def return_cities(state_id):
    """return all cities objects"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = []
    for city in storage.all(City).values():
        if city.state_id == state_id and state_id == state.id:
            cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=["GET"], strict_slashes=False)
def return_city(city_id):
    """return json City object"""
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    else:
        return jsonify(obj.to_dict())


@app_views.route('/cities/<city_id>', methods=["DELETE"])
def delete_city(city_id):
    """ delete object by id """
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=["POST"], strict_slashes=False)
def add_city(state_id):
    """ add a city to a state """
    data = {}
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json(silent=True)
    if data is None:
        abort(400, "Not a JSON")
    if "name" not in data.keys():
        abort(400, "Missing name")
    new_city = City(**data)
    new_city.state_id = state_id
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=["PUT"], strict_slashes=False)
def update_city(city_id=None):
    """ update the new city """
    dic = {}
    obj = storage.get("City", city_id)
    if obj is None:
        abort(404)
    dic = request.get_json(silent=True)
    if dic is None:
        abort(400, "Not a JSON")
    for key, value in dic.items():
        setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200
