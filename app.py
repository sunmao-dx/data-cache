from flask import Flask
from flask_restful import Api
from resources.data_agent import Issue
# from myapi.resources.bar import Bar
# from myapi.resources.baz import Baz

app = Flask(__name__)
api = Api(app)

api.add_resource(Issue, '/Issue')
# api.add_resource(Bar, '/Bar', '/Bar/<string:id>')
# api.add_resource(Baz, '/Baz', '/Baz/<string:id>')

if __name__ == '__main__':
    app.run(debug=True)