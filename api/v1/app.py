#!/usr/bin/python3
""" endpoint (route) that will be return the status of your API """


from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv as get


# create a variable appp, instance of flask
app = Flask(__name__)

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


if __name__ == "__main__":
    host = get("HBNB_API_HOST", "0.0.0.0")
    port = get("HBNB_API_PORT", "5000")
    app.run(host=host, port=port, debug=True, threaded=True)
