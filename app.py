from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_cors import CORS
import requests

app = Flask(__name__)
# CORS(app)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
api = Api(app)

SECRET_CODE = []

class GenerateCode(Resource):
    def get(self):
        global SECRET_CODE
        url = 'https://random.org/integers/'
        params = {
            'num': 4,
            'min': 0,
            'max': 7,
            'col': 1,
            'base': 10,
            'format': 'plain',
            'rnd': 'new'
        }

        try:
            response = requests.get(
                url, 
                params=params, 
                headers={"User-Agent":"mastermind-game/1.0"}, 
                timeout=5
                )
            response.raise_for_status()
            # numbers = [int(n) for n in response.text.strip().split('\n')]
            SECRET_CODE = [int(n) for n in response.text.strip().split('\n')]
            return {'secret': SECRET_CODE}, 200
        except requests.RequestException as e:
            return {'error': 'Failed to generate code', 'details': str(e)}, 500
        
class EvaluateGuess(Resource):
    def post(self):
        global SECRET_CODE
        data = request.get_json()
        guess = data.get('guess', [])

        if not SECRET_CODE:
            return {'error': 'No secret code generated yet.'}, 400
        
        if len(guess) != len(SECRET_CODE):
            return {'error': 'Guess must have the same length as secret code.'}, 400
        
        correct_location = 0
        correct_number = 0
        secret_copy = SECRET_CODE.copy()

        for i in range(len(guess)):
            if guess[i] == SECRET_CODE[i]:
                correct_location += 1
            if guess[i] in secret_copy:
                correct_number += 1
                secret_copy.remove(guess[i])

        return {
            'correct_number': correct_number,
            'correct_location': correct_location
        }, 200


api.add_resource(GenerateCode, '/api/generate')
api.add_resource(EvaluateGuess, '/api/evaluate')

if __name__ == '__main__':
    app.run(debug=True)