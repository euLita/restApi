from flask_restful import Resource, request
import json

with open('data_skills.json', 'r') as file:
  list_skills = json.load(file)

def _alterar(id, name_new):
    # identifying index of item in the list
    id_procurado = None
    ind = 0
    for item in list_skills:
        if item["id"] == id:
            id_procurado = ind
        ind = ind + 1
    # change status item
    if (id_procurado is not None) and id_procurado <= len(list_skills):
        list_skills[id_procurado]['name'] = name_new
        return True
    return False

def _insert(skill_new):
    if not ('id' in skill_new):
        skill_new['id'] = len(list_skills)
    # Validate data
    for item in list_skills:
        if skill_new['id'] == item['id']:
            return False
    # Insert data
    list_skills.append(skill_new)
    return True

def _delete(id):
    # identifying index of item in the list
    id_procurado = None
    ind = 0
    for item in list_skills:
        if item["id"] == id:
            id_procurado = ind
        ind = ind + 1
    # Deleting item
    if (id_procurado is not None) and id_procurado < len(list_skills):
        del list_skills[id_procurado]
        return True
    return False

class skills(Resource):
    def get(self):
        return list_skills

    def post(self):
        skill = json.loads(request.data)
        _insert(skill)
        return skill

def _get_skill(id):
    # identifying index of item in the list
    id_procurado = None
    ind = 0
    for item in list_skills:
        if item["id"] == id:
            id_procurado = ind
        ind = ind + 1
    # change status item
    if (id_procurado is not None) and id_procurado <= len(list_skills):
        return list_skills[id_procurado]
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
        _delete(id)
        return {'status':'sucess', 'mensage':'deleted record'}
