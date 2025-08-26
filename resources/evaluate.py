from flask_restful import Resource
from flask import request
from game import GAME
from config import DEFAULT_PARAMS, PARAMS
import time

class EvaluateGuess(Resource):
    def post(self):
        data = request.get_json()
        guess = data.get('guess', [])

        if not GAME['secret']:
            return {'error': 'No secret code generated yet.'}, 400
        
        if len(guess) != len(GAME['secret']):
            return {'error': 'Guess must have the same length as secret code.'}, 400
        
        if not all (isinstance(d, int) and PARAMS['min'] <= d <= PARAMS['max'] for d in guess):
            return {'error': f"All digits must be integers between {PARAMS['min']} and {PARAMS['max']}"}
        
        correct_location = 0
        correct_number = 0
        secret_copy = GAME['secret'].copy()

        for i in range(len(guess)):
            if guess[i] == GAME['secret'][i]:
                correct_location += 1
            if guess[i] in secret_copy:
                correct_number += 1
                secret_copy.remove(guess[i])
        
        GAME['history'].append({
            'guess': guess,
            'correct_number': correct_number,
            'correct_location': correct_location
        })

        GAME['attempts'] += 1

        if correct_location == len(GAME['secret']) or GAME['attempts'] >= GAME['max_attempts']:
            GAME['finished'] = True
            GAME['end_time'] = time.time()
            GAME['elapsed_time'] = round(GAME['end_time'] - GAME['start_time'], 2)
            print(GAME['start_time'])
            print(GAME['elapsed_time'])
            print(GAME['end_time'])

        return GAME, 200