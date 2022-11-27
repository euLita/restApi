from flask import Flask, jsonify, request, Response

app = Flask(__name__)

tasks = [
    {
        'id': 13,
        'responsible': 'Gael',
        'task': 'Develop method GET2',
        'status': 'concluded'
    },
    {
        'id': 18,
        'responsible': 'Marci',
        'task': 'Develop method POST',
        'status': 'pending'
    }
]

def adicionar(new_task):
    tasks.append(new_task)

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

@app.route('/tasks/<int:id>/')
def get_one(id):
    developer = tasks[id]
    return jsonify(developer)

@app.route('/tasks')
def get_all():
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def insert():
    adicionar(request.get_json())
    return jsonify(request.get_json())

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