from flask import Blueprint
from flask_restx import Api

"""Init Flask API"""
api_v1 = Blueprint("api", __name__, url_prefix="")
api = Api(api_v1, version='1.0', title='TodoMVC API', description='A simple TodoMVC API')

"""Import the components API"""
from views import todo, animal
