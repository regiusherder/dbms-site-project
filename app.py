from flask import Flask,send_from_directory,render_template
from flask import send_from_directory
from flask_restful import Resource, Api
from package.project import Projects, Project
from package.item import Items, Item
from package.labor import Labors, Labor
from package.land import Lands, Land
from package.transport import Transports, Transport
import json
import os

with open('config.json') as data_file:
    config = json.load(data_file)

app = Flask(__name__, static_url_path='')
api = Api(app)

api.add_resource(Projects, '/project')
api.add_resource(Project, '/project/<int:id>')
api.add_resource(Items, '/item')
api.add_resource(Item, '/item/<int:id>')
api.add_resource(Labors, '/labor')
api.add_resource(Labor, '/labor/<int:id>')
api.add_resource(Lands, '/land')
api.add_resource(Land, '/land/<int:id>')
api.add_resource(Transports, '/transport')
api.add_resource(Transport, '/transport/<int:id>')

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True,host=config['host'],port=config['port'])

