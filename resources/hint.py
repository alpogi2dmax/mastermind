from flask_restful import Resource
import random
from game import GAME

class GetHint(Resource):
    def get(self):
        blank_index = [i for i, val in enumerate(GAME['hint']) if val == '__']

        if not blank_index:
            return {'error': 'No more hints avaialble'}, 400
        
        pos = random.choice(blank_index)

        GAME['hint'][pos] = GAME['secret'][pos]

        GAME['attempts'] += 1

        if (len(blank_index)) == 1:
            GAME['finished'] = True
        
        return GAME, 200