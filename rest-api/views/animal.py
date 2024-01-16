from flask import abort
from flask_restx import Resource, fields
from . import api
from services.animal import DAO
from const import STATUS_CODE

"""Init namespace for component API: ANIMAL Management"""
ns = api.namespace('person', description='ANIMAL operations')

"""Define ANIMAL model"""
animal = api.model('Animal', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'name': fields.String(required=True, description='The name unique of the animal')})


@ns.route('/')
class AnimalList(Resource):
    """Shows a list of all todos, and lets you POST to add new tasks"""

    @ns.doc('Get all animal')
    @ns.response(STATUS_CODE.NOT_FOUND, 'No found any animal')
    @ns.marshal_list_with(animal)
    def get(self):
        data = DAO.animals
        if data:
            return data
        abort(STATUS_CODE.NOT_FOUND, "No found any animal ~~.")
