from models.animal import AnimalModel


class AnimalService:
    def __init__(self):
        self.counter = 0
        self.animals = []

    def get(self, animal_id):
        for animal in self.animals:
            if animal['id'] == animal_id:
                return animal
        return None

    def create(self, data):
        data['id'] = self.counter = self.counter + 1
        self.animals.append(AnimalModel(**data).to_dict())
        return data

    def update(self, todo_id, data):
        ...

    def delete(self, todo_id):
        ...


"""Init dataset"""
DAO = AnimalService()
DAO.create({'name': 'Dog'})
DAO.create({'name': 'Bird'})
DAO.create({'name': 'Cat'})
DAO.create({'name': 'Pig'})
