#!/usr/bin/python3
""" endpoint (route) that will be return the status of your API """


from flask import Flask
from flask import make_response
from flask import jsonify
from models import storage
from api.v1.views import app_views
from os import getenv as get
from flask_cors import CORS

# create a variable appp, instance of flask
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# register the blueprint app_views to your instance app
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(self):
    """
    declaring a method to handle @app.teardown_appcontext
    what is called storage.close
    in order to close the appeal
    """
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """
    handler for 404 errors that returns a JSON-formatted 404 status code
    response. The content should be: "error": "Not found"
    """

    error = {"error": "Not found"}
    return make_response(jsonify(error), 404)


if __name__ == "__main__":
    host = get("HBNB_API_HOST", "0.0.0.0")
    port = get("HBNB_API_PORT", "5000")
    app.run(host=host, port=port, debug=True, threaded=True)
