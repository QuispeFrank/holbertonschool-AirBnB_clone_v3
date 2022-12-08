#!/usr/bin/python3
""" file index """

from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status", strict_slashes=False)
def app_views_status():
    """ return status """
    statusok = {"status": "OK"}
    return jsonify(statusok)
