from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from models import Score

class ScoreSchema(SQLAlchemySchema):
    class Meta:
        model = Score
        load_instance = True

    id = auto_field()
    player_name = auto_field()
    difficulty = auto_field()
    attempts = auto_field()
    elapsed_time = auto_field()
    created_at = auto_field()