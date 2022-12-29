from flask_restful import Resource, request
import json
import mariadb

with open('data_skills.json', 'r') as file:
  list_skills = json.load(file)

data = []
with open('config.local.json') as f:
    data = json.load(f)

print('comecou',list_skills)

config = {
    'host': data['host'],
    'port': int(data['port']),
    'user': data['user'],
    'password': data['password'],
    'database': data['database'],
    'autocommit':True
}

def _all_skills():
    conn = mariadb.connect(**config)
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM skills")
    row_headers = [x[0] for x in cur.description]
    rv = cur.fetchall()
    data_tasks=[]
    for result in rv:
        data_tasks.append(dict(zip(row_headers,result)))
    return data_tasks

def _insert(skill_new):
    conn = mariadb.connect(**config)
    cur = conn.cursor()
    sql = f"""INSERT INTO restapi.skills 
            (id,name) values
            (null,
            '{skill_new['name']}'
            );"""
    print(sql)
    cur.execute(sql)
    conn.close()

def _alterar(id, name_new):
    alterou = False
    conn = mariadb.connect(**config)
    cur = conn.cursor()
    sql_consulta = f"SELECT id, name FROM skills WHERE id = {id};"
    cur.execute(sql_consulta)
    rv = cur.fetchall()
    if len(rv) > 0:    # Retorne true se o item que o usuario esta tentando alterar existe
        sql = f"""UPDATE restapi.skills SET
        name = '{name_new}'
        WHERE id = {id};"""
        cur.execute(sql)
        alterou = True
    conn.close()
    return alterou

def _delete(id):
    apagou = False
    conn = mariadb.connect(**config)
    cur = conn.cursor()
    sql_consulta = f"SELECT id, name FROM skills WHERE id = {id};"
    cur.execute(sql_consulta)
    rv = cur.fetchall()
    if len(rv) > 0:    # Retorne true se o item que o usuario esta tentando apagar existe
        sql = f"""DELETE FROM restapi.skills
        WHERE id = {id};"""
        cur.execute(sql)
        apagou = True
    conn.close()
    return apagou

class skills(Resource):
    def get(self):
        all_skills = _all_skills()
        return all_skills

    def post(self):
        skill = json.loads(request.data)
        _insert(skill)
        return skill

def _get_skill(id):
    conn = mariadb.connect(**config)
    cur = conn.cursor()
    id_contato = id
    cur.execute(f"SELECT id, name FROM skills WHERE id = {id_contato};")
    row_headers = [x[0] for x in cur.description]
    rv = cur.fetchall()
    if not (len(rv) == 0):
        print(rv[0])
        tasks = dict(zip(row_headers, rv[0]))
        return tasks
    else:
        return None

class skill(Resource):
    def get(self, id):
        skill = _get_skill(id)
        return skill

    def put(self, id):
        skill = json.loads(request.data)
        if _alterar(id, skill['name']):
            return {"mensage": f"Item {id} alterado com sucesso"}, 201
        return {"erro": f"Item  {id} não encontrado"}, 404

    def delete(self, id):
        if _delete(id):
            return {'status':'sucess', 'mensage':'deleted record'}
        return {"erro": f"Item  {id} não encontrado"}, 404

    # def delete(self, id):
    #     if _delete(id):
    #         return {'status':'sucess', 'mensage':'deleted record'}
    #     return {"erro": f"Item  {id} não encontrado"}, 404