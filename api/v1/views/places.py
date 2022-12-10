#!/usr/bin/python3
"""view of City objects"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.city import City
from models.state import State
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=["GET"], strict_slashes=False)
def places_from_city(city_id):
    """return all city objects"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = []
    for place in storage.all(Place).values():
        if place.city_id == city_id:
            places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=["GET"], strict_slashes=False)
def return_place(place_id):
    """return json City object"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    else:
        return jsonify(obj.to_dict())


@app_views.route('/places/<place_id>', methods=["DELETE"])
def delete_place(place_id):
    """ delete object by id """
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=["POST"], strict_slashes=False)
def add_place(city_id):
    """ add a city to a state """
    data = {}
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json(silent=True)
    if data is None:
        abort(400, "Not a JSON")
    if "name" not in data.keys():
        abort(400, "Missing name")
    if "user_id" not in data.keys():
        abort(400, "Missing user_id")
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    new_place = Place(**data)
    new_place.city_id = city_id
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=["PUT"], strict_slashes=False)
def update_place(place_id=None):
    """ update the new place """
    dic = {}
    obj = storage.get("Place", place_id)
    if obj is None:
        abort(404)
    dic = request.get_json(silent=True)
    if dic is None:
        abort(400, "Not a JSON")
    for key, value in dic.items():
        setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200
