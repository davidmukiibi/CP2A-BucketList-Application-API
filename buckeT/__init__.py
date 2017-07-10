from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from instance.config import app_config
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    jwt.init_app(app)

    return app

app = create_app('development')
api = Api(app=app, prefix="/api/bucketlist/v1")
