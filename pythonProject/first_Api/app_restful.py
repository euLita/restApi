from flask import Flask, request
from flask_restful import Resource, Api
from skills import skills, skill
import mariadb
import json

app = Flask(__name__)
api = Api(app)

with open('data.json', 'r') as f:
  tasks = json.load(f)

data = []
with open('config.local.json') as f:
    data = json.load(f)

config = {
    'host': data['host'],
    'port': int(data['port']),
    'user': data['user'],
    'password': data['password'],
    'database': data['database'],
    'autocommit':True
}

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
    conn = mariadb.connect(**config)
    cur = conn.cursor()
    sql = f"""INSERT INTO restapi.tasks 
            (id,owner,status,task) values
            (null,
            '{task_new['owner']}',
            '{task_new['status']}',
            '{task_new['task']}'
            );"""
    print(sql)
    cur.execute(sql)
    conn.close()

def _get_by_id(id):
    conn = mariadb.connect(**config)
    cur = conn.cursor()
    id_contato = id
    cur.execute(f"SELECT id, owner, status, task FROM tasks WHERE id = {id_contato};")
    row_headers = [x[0] for x in cur.description]
    rv = cur.fetchall()
    if not (len(rv) == 0):
        print(rv[0])
        tasks = dict(zip(row_headers, rv[0]))
        return tasks
    else:
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

class developers(Resource):
    def get(self):
        return tasks
    def post(self):
        task = json.loads(request.data)
        _insert(task)
        return task

api.add_resource(developer, '/dev/<int:id>/')
api.add_resource(developers, '/dev/')
api.add_resource(skills, '/skills/')
api.add_resource(skill, '/skills/<int:id>/')


if __name__ == '__main__':
    app.run(debug=True)