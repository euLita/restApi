from flask import Flask, request
from flask_restful import Resource, Api
from skills import skills
import json

app = Flask(__name__)
api = Api(app)

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

def _delete(id):
    # identifying index of item in the list
    id_procurado = None
    ind = 0
    for item in tasks:
        if item["id"] == id:
            id_procurado = ind
        ind = ind + 1
    # Deleting item
    if (id_procurado is not None) and id_procurado < len(tasks):
        del tasks[id_procurado]
        return True
    return False

def _insert(task_new):
    if not ('id' in task_new):
        task_new['id'] = len(tasks)
    # Validate data
    for item in tasks:
        if task_new['id'] == item['id']:
            return False
    # Insert data
    tasks.append(task_new)
    return True


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

    def delete(self, id):
        _delete(id)
        return {'status':'sucess', 'mensage':'deleted record'}

class list_developers(Resource):
    def get(self):
        return tasks
    def post(self):
        task = json.loads(request.data)
        _insert(task)
        return task

api.add_resource(developer, '/dev/<int:id>/')
api.add_resource(list_developers, '/dev/')
api.add_resource(skills, '/skills/')


if __name__ == '__main__':
    app.run(debug=True)