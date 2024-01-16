from models.todo import TodoModel


class TodoService:
    def __init__(self):
        self.counter = 0
        self.todos = []

    def get(self, todo_id):
        for todo in self.todos:
            if todo['id'] == todo_id:
                return todo
        return None

    def create(self, data):
        todo = data
        todo['id'] = self.counter = self.counter + 1
        self.todos.append(TodoModel(**todo).to_dict())
        return todo

    def update(self, todo_id, data):
        todo = self.get(todo_id)
        if todo:
            todo.update(data)
            return todo
        return None

    def delete(self, todo_id):
        todo = self.get(todo_id)
        if todo:
            self.todos.remove(todo)
            return True
        return False


"""Init dataset"""
DAO = TodoService()
DAO.create({'task': 'Init Project'})
DAO.create({'task': 'Build API'})
DAO.create({'task': 'Deploy and Test Project'})
DAO.create({'task': 'Deployment'})
