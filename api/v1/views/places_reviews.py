#!/usr/bin/python3
"""Script creates a route that returns status in JSON format."""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route(
    "/places/<place_id>/reviews", methods=['GET'], strict_slashes=False)
def reviews(place_id):
    """method retrieves list of all Review objects in a given Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        review_list = []
        for review in place.reviews:
            review_list.append(review.to_dict())
        return jsonify(review_list)


@app_views.route("/reviews/<review_id>", methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """method retrieves a Review object in JSON format"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        return jsonify(review.to_dict())


@app_views.route(
    "/reviews/<review_id>", methods=['DELETE'], strict_slashes=False)
def del_review(review_id):
    """method deletes a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200


@app_views.route(
    "/places/<place_id>/reviews", methods=['POST'], strict_slashes=False)
def post_review(place_id):
    """method creates a new Review object"""
    data = {}
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json(silent=True)
    if data is None:
        abort(400, 'Not a JSON')

    if "user_id" not in data.keys():
        abort(400, "Missing user_id")

    users = storage.get(User, data['user_id'])
    if users is None:
        abort(404)

    if "text" not in data.keys():
        abort(400, "Missing text")

    new_review = Review(**data)
    new_review.place_id = place_id
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """method updates an existing Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    elif not request.json or not request.is_json:
        abort(400, 'Not a JSON')
    else:
        ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        for key, value in request.get_json().items():
            if key not in ignore:
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict())
