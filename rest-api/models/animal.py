class AnimalModel:
    def __init__(self, **kwargs):
        self.id = kwargs.pop('id')
        self.name = kwargs.get('name')

    def to_dict(self):
        return self.__dict__
