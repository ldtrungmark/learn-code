class TodoModel:
    def __init__(self, **kwargs):
        self.id = kwargs.pop('id')
        self.task = kwargs.get('task')

    def to_dict(self):
        return self.__dict__
