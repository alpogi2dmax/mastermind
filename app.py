from flask import Flask, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)
api = Api(app)

class GenerateCode(Resource):
    def get(self):

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
            numbers = [int(n) for n in response.text.strip().split('\n')]
            return {'secret': numbers}, 200
        except requests.RequestException as e:
            return {'error': 'Failed to generate code', 'details': str(e)}, 500

api.add_resource(GenerateCode, '/api/generate')

if __name__ == '__main__':
    app.run(debug=True)