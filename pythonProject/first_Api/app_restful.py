from flask import Flask
from flask_restful import Resource, Api

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

class developer(Resource):
    def get(self):
        return {'name':'Ruda'}
        # return 'Hey dev'
    def put(self):
        # pass
        return 'Hey dev'
    def delete(self):
        pass
        return 'Hey dev'

api.add_resource(developer, '/dev')

if __name__ == '__main__':
    app.run(debug=True)