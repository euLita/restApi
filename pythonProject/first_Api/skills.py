from flask_restful import Resource

list_skills = ['C', 'JavaScript', 'Node', 'Python', 'Java', 'Flask']
class skills(Resource):
    def get(self):
        return list_skills