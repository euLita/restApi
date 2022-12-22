from flask import Flask, request
from flask_restful import Resource, Api
import json

app = Flask(__name__)
api = Api(app)

developers = [
    {
        'id': 1,
        'name': 'Faru',
        'skills': ['Java', 'Git']
    },
    {
        'id': 2,
        'name': 'Gleu',
        'skills': ['Php', 'Node']
    }
]
with open('data.json', 'r') as f:
  tasks = json.load(f)

def _alterar(id, status_new):
    # identifying index of item in the list
    id_procurado = None
    ind = 0
    for item in tasks:
        if item["id"] == id:
            id_procurado = ind
        ind = ind + 1
    # change status item
    if (id_procurado is not None) and id_procurado <= len(tasks):
        tasks[id_procurado]['status'] = status_new
        return True
    return False
def _get_by_id(id):
    # identifying index of item in the list
    id_procurado = None
    ind = 0
    for item in tasks:
        if item["id"] == id:
            id_procurado = ind
        ind = ind + 1
    # change status item

    if (id_procurado is not None) and id_procurado <= len(tasks):
        return tasks[id_procurado]
    return None

class developer(Resource):
    def get(self, id):
        developer = _get_by_id(id)
        return developer

    def put(self, id):
        task = json.loads(request.data)
        if _alterar(id, task['status']):
            return {"mensage": f"Item {id} alterado com sucesso"}, 201
        return {"erro": f"Item  {id} não encontrado"}, 404

    def delete(self):
        return developers

api.add_resource(developer, '/dev/<int:id>/')

if __name__ == '__main__':
    app.run(debug=True)