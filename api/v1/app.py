#!/usr/bin/python3
""" Connect to API and to return status of the API """
import os
from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, make_response
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_appcontext(code):
    """Closes the stroage"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """Retrun 404 page"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    """ Main Function """
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(os.getenv('HBNB_API_PORT', '5000')))
