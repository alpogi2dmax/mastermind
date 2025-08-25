from flask_restful import Resource
from config import DEFAULT_PARAMS

class Settings(Resource):
    def get (self):
        settings = {
            'num': DEFAULT_PARAMS['num'],
            'max': DEFAULT_PARAMS['max']
        }

        return settings, 200