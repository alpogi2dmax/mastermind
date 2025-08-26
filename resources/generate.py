from flask_restful import Resource
from flask import request
import requests
from game import GAME, reset_game
from config import DEFAULT_PARAMS, PARAMS


class GenerateCode(Resource):
    def post(self):
        data = request.get_json()
        difficulty = data.get('difficulty')
        player = data.get('player')
        settings = data.get('settings', PARAMS)

        if settings['num'] > 8 or settings['num'] < 3:
            return {'error': 'Number of digits should not be less than 3 or more than 8'}, 400
        
        if settings['max'] > 10 or settings['max'] < 3:
            return {'error': 'Max value should not be less than 3 or more than 10'}, 400
        
        PARAMS['num'] = settings.get('num', PARAMS['num'])
        PARAMS['max'] = settings.get('max', PARAMS['max'])

        url = 'https://www.random.org/integers/'

        try:
            response = requests.get(
                url,
                params=PARAMS,
                headers={'User-Agent': 'mastermind-game/1.0'},
                timeout=5
            )
            response.raise_for_status()

            secret_code = [int(n) for n in response.text.strip().split('\n')]
            reset_game(secret_code, difficulty, player)

            return GAME, 200
        
        except requests.RequestException as e:
            return {'error': 'Failed to generate code', 'details': str(e)}, 500
