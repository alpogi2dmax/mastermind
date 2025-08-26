from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import DB_URI
import requests
import random

db = SQLAlchemy()
migrate = Migrate()

def create_app():

    app = Flask(__name__)
    CORS(app, supports_credentials=True)

    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    import models

    from resources.generate import GenerateCode
    from resources.evaluate import EvaluateGuess
    from resources.hint import GetHint
    from resources.settings import Settings

    api = Api(app)

    api.add_resource(GenerateCode, '/api/generate')
    api.add_resource(EvaluateGuess, '/api/evaluate')
    api.add_resource(GetHint, '/api/gethint')
    api.add_resource(Settings, '/api/settings')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)