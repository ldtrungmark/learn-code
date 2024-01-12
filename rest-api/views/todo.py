from flask import abort
from flask_restx import Resource, fields
from . import api
from services.todo import DAO
from const import STATUS_CODE

"""Init namespace for component API: TODO Management"""
ns = api.namespace('todo', description='TODO operations')

"""Define TODO model"""
todo = api.model('Todo', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'task': fields.String(required=True, description='The task details')})


@ns.route('/')
class TodoList(Resource):
    """Shows a list of all todos, and lets you POST to add new tasks"""
    @ns.doc('list_todos')
    @ns.response(STATUS_CODE.NOT_FOUND, 'No found TODO data')  # Define error response in swagger ui
    @ns.marshal_list_with(todo)
    def get(self):
        """List all tasks"""
        if DAO.todos:
            return DAO.todos
        abort(STATUS_CODE.NOT_FOUND, "No found any TODO data")

    @ns.doc('create_todo')
    @ns.expect(todo)  # Expect parameters input of API
    @ns.marshal_with(todo, code=201)
    def post(self):
        """Create a new task"""
        return DAO.create(api.payload), 201


@ns.route('/<int:id>')
@ns.response(STATUS_CODE.NOT_FOUND, 'Todo no found')
@ns.param('id', 'The task identifier')
class Todo(Resource):
    """Show a single todo item and lets you delete them"""

    @ns.doc('get_todo')
    @ns.marshal_with(todo)
    def get(self, id):
        """Fetch a given resource"""
        data = DAO.get(id)
        if data:
            return data
        abort(STATUS_CODE.NOT_FOUND, f"No found TODO with id: {id}")

    @ns.doc('delete_todo')
    @ns.response(STATUS_CODE.NO_CONTENT, 'Todo deleted')
    def delete(self, id):
        """Delete a task given its identifier"""
        is_delete = DAO.delete(id)
        if is_delete:
            return '', STATUS_CODE.NO_CONTENT
        abort(STATUS_CODE.NOT_FOUND, f"No found TODO id {id} for deleted")

    @ns.expect(todo)
    @ns.marshal_with(todo)
    def put(self, id):
        """Update a task given its identifier"""
        data = DAO.update(id, api.payload)
        if data:
            return data
        abort(STATUS_CODE.NOT_FOUND, f"No found TODO id {id} for deleted")
