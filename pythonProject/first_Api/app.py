from flask import Flask, jsonify, request, Response

app = Flask(__name__)

tasks = [
    {
        'id': 13,
        'responsible': 'Gael',
        'task': 'Develop method GET',
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

if __name__ == '__main__':
    app.run(debug=True)