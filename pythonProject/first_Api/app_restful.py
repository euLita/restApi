from flask import Flask, request
from flask_restful import Resource, Api
from skills import skills, skill
import mariadb
import json

app = Flask(__name__)
api = Api(app)

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


def _all_tasks():
    conn = mariadb.connect(**config)
    cur = conn.cursor()
    cur.execute("select id, owner, status, task from tasks")
    row_headers = [x[0] for x in cur.description]
    rv = cur.fetchall()
    data_tasks=[]
    for result in rv:
        data_tasks.append(dict(zip(row_headers,result)))
    return data_tasks

def _alterar(id, status_new):
    alterou = False
    conn = mariadb.connect(**config)
    cur = conn.cursor()
    sql_consulta = f"SELECT id, owner, status, task FROM tasks WHERE id = {id};"
    cur.execute(sql_consulta)
    rv = cur.fetchall()
    if len(rv) > 0:    # Retorne true se o item que o usuario esta tentando alterar existe
        sql = f"""UPDATE restapi.tasks SET
        status = '{status_new}'
        WHERE id = {id};"""
        cur.execute(sql)
        alterou = True
    conn.close()
    return alterou

def _delete(id):
    apagou = False
    conn = mariadb.connect(**config)
    cur = conn.cursor()
    sql_consulta = f"SELECT id, owner, status, task FROM tasks WHERE id = {id};"
    cur.execute(sql_consulta)
    rv = cur.fetchall()
    if len(rv) > 0:    # Retorne true se o item que o usuario esta tentando apagar existe
        sql = f"""DELETE FROM restapi.tasks
        WHERE id = {id};"""
        cur.execute(sql)
        apagou = True
    conn.close()
    return apagou

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
        if _delete(id):
            return {'status':'sucess', 'mensage':'deleted record'}
        return {"erro": f"Item  {id} não encontrado"}, 404
class developers(Resource):
    def get(self):
        all_tasks = _all_tasks()
        return all_tasks
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