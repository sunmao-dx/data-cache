from flask_restful import Resource
from flask_restful import request

class Issue(Resource):
    def post(self):
        print(request.json)
        pass

    def get(self):
        pass
