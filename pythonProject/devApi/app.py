import json

from flask import Flask, jsonify, request

app = Flask(__name__)

developers = [
    {
        'id':'1',
        'name': 'Bianca',
        'skills': ['Python', 'Django']
    },
    {
        'id':'14',
        'name':'Rapha',
        'skills': ['Python', 'Flask']
     }
]

@app.route('/dev/<int:id>/', methods=['GET', 'PUT', 'DELETE'])
def developer(id):
    if request.method == 'GET':
        try:
            response = developers[id]
        except IndexError:
            mensage = 'id developer does not {} exist'.format(id)
            response = {'status':'erro', 'mensage':mensage}
        except Exception:
            mensage = 'unknown error look for api admin'
            response = {'status':'erro', 'mensage':mensage}
        return jsonify(response)
    elif request.method == 'PUT':
        dados = json.loads(request.data)
        developers[id] = dados
        return jsonify(dados)
    elif request.method == 'DELETE':
        developers.pop(id)
        return  jsonify({'status': 'sucess', 'mensage': 'Registro excluido'})
@app.route('/dev/', methods=['POST', 'GET'])
def list_Developers():
    if request.method =='POST':
        dados = json.loads(request.data)
        posicion = len(developers)
        dados['id'] = posicion
        developers.append(dados)
        return jsonify(developers[posicion])
    elif request.method == 'GET':
        return jsonify(developers)
if __name__ == '__main__':
    app.run(debug=True)