from flask import Flask
from flask_restful import Api

app = Flask(__name__)
app.config.from_object("config.Config")

api = Api(app)

from app import routes
