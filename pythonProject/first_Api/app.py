from flask import Flask, jsonify, request, Response
import mariadb
import json

app = Flask(__name__)
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

def _get_by_id(id):
    conn = mariadb.connect(**config)
    cur = conn.cursor()
    id_contato = id
    cur.execute(f"SELECT id, owner, status, task FROM tasks WHERE id = {id_contato};")
    row_headers = [x[0] for x in cur.description]
    rv = cur.fetchall()
    if not(len(rv)==0):
        print(rv[0])
        tasks = dict(zip(row_headers, rv[0]))
        return tasks
    else:
        return None

def _all_tasks():   #here
    conn = mariadb.connect(**config)
    cur = conn.cursor()
    cur.execute("select id, owner, status, task from tasks")
    row_headers = [x[0] for x in cur.description]
    rv = cur.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    return json_data

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

def _alterar(id, status_new) :
    conn = mariadb.connect(**config)
    cur = conn.cursor()
    id_contato = int(request.args.get('id', ''))
    sql_consulta = f"select id, nome,telefone, cpf, rg, datanasc, genero from contatos WHERE id = {id_contato};"
    cur.execute(sql_consulta)
    row_headers=[x[0] for x in cur.description]
    rv = cur.fetchall()
    if request.method == 'POST':
        sql = f"""UPDATE contato.contatos SET nome = '{request.form['nome_completo']}',
        datanasc = '{request.form['data_de_nascimento']}',
        cpf = '{request.form['cpf']}', 
        telefone = '{request.form['telefone']}',
        rg = '{request.form['rg']}',
        genero = '{request.form['genero']}'
        WHERE id = {id_contato};"""
        print(sql)
        cur.execute(sql)
        cur.execute(sql_consulta)
        rv = cur.fetchall()
    conn.close()
    print('rv aqui',rv)
    contato=dict(zip(row_headers,rv[0]))
    return contato

    # # identifying index of item in the list
    # id_procurado = None
    # ind = 0
    # for item in tasks:
    #     if item["id"] == id:
    #         id_procurado = ind
    #     ind = ind + 1
    # # change status item
    # if (id_procurado is not None) and id_procurado <= len(tasks):
    #     tasks[id_procurado]['status'] = status_new
    #     return True
    # return False

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

@app.route('/tasks/<int:id>/')
def get_one(id):
    item = _get_by_id(id)
    if type(item) is dict:    #
        return jsonify(item)
    return Response({}, status=404)

@app.route('/tasks')
def get_all():
    all_tasks = _all_tasks()
    return jsonify(all_tasks)

@app.route('/tasks', methods=['POST'])
def insert():
    if _insert(request.get_json()):
        return jsonify(request.get_json())
    else:
        return Response({}, status=400)

@app.route('/tasks/<int:id>/', methods=['DELETE'])
def delete(id):
    st = 200
    if not _delete(id):
        st = 404
    return Response({}, status=st)

@app.route('/tasks/<int:id>', methods=['PUT'])
def update(id):
    task = request.get_json()
    if _alterar(id, task['status']):
        return jsonify({"mensage": f"Item {id} alterado com sucesso"}), 201
    return jsonify({"erro": f"Item  {id} não encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)