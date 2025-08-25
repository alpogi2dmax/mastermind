from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_cors import CORS
import requests
import random

app = Flask(__name__)
CORS(app, supports_credentials=True)
api = Api(app)

from resources.generate import GenerateCode
from resources.evaluate import EvaluateGuess
from resources.hint import GetHint
from resources.settings import Settings




api.add_resource(GenerateCode, '/api/generate')
api.add_resource(EvaluateGuess, '/api/evaluate')
api.add_resource(GetHint, '/api/gethint')
api.add_resource(Settings, '/api/settings')

if __name__ == '__main__':
    app.run(debug=True)