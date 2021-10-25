import os
import logging
from flask import Flask
from flask_restful import Api
from resources.data_agent import Issue
# from myapi.resources.bar import Bar
# from myapi.resources.baz import Baz

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'WARN').upper()
logging.basicConfig(level=LOG_LEVEL)

app = Flask(__name__)
api = Api(app)

#api.add_resource(Issue, '/Issue')
api.add_resource(Issue, '/api/dataCache/pushGiteeIssue')
# api.add_resource(Bar, '/Bar', '/Bar/<string:id>')
# api.add_resource(Baz, '/Baz', '/Baz/<string:id>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
