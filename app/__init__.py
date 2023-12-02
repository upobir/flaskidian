from flask import Flask
from flask_redis import FlaskRedis

app = Flask(__name__)
app.config.from_object("config.Config")

redis_store = FlaskRedis(app)

from app import routes
