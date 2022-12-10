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

    new_review = Review(**review)
    review.place_id = place_id
    storage.new(new_review)
    new_review.save()
    return jsonify(new_review.to_dict()), 201
