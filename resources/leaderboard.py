from flask_restful import Resource
from flask import request
import requests
from game import GAME, reset_game
from config import DEFAULT_PARAMS, PARAMS
from schema  import ScoreSchema
from models import Score

score_schema = ScoreSchema(many=True)


class GetLeaderboard(Resource):
    def get(self):
        leaderboard = {}
        for difficulty in ['Easy', 'Normal', 'Hard']:
            scores = (
                Score.query.filter_by(difficulty=difficulty).order_by(Score.elapsed_time.asc()).limit(10).all()
            )
            leaderboard[difficulty] = score_schema.dump(scores)
        return leaderboard, 200