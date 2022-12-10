#!/usr/bin/python3
""" """


from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.state import State
from models.amenity import Amenity


@app_views.route('/amenities', methods=["GET"], strict_slashes=False)
def amenities_ret():
    """ """
    all_objs = storage.all(Amenity)
    return jsonify([obj.to_dict() for obj in all_objs.values()])


@app_views.route('/amenities/<amenity_id>',
                 methods=["GET"], strict_slashes=False)
def by_amenity_id(amenity_id):
    """ """
    obj = storage.get("Amenity", amenity_id)
    return (abort(404) if obj is None else jsonify(obj.to_dict()))


@app_views.route('/amenities/<amenity_id>', methods=["DELETE"])
def amenity_delete(amenity_id=None):
    """delete an object by id"""
    obj = storage.get("Amenity", amenity_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=["POST"], strict_slashes=False)
def amenity_post():
    """add new amenity object"""
    dic = request.get_json(silent=True)
    if dic is None:
        abort(400, "Not a JSON")
    if "name" not in dic.keys():
        abort(400, "Missing name")
    new_amenity = Amenity(**dic)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=["PUT"], strict_slashes=False)
def update_amenity(amenity_id=None):
    """update new amenity object"""
    dic = {}
    obj = storage.get("Amenity", amenity_id)
    if obj is None:
        abort(404)
    dic = request.get_json(silent=True)
    if dic is None:
        abort(400, "Not a JSON")
    for key, value in dic.items():
        setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200
