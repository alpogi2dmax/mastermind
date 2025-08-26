from extensions import db
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

class Score(db.Model, SerializerMixin):
    __tablename__ = 'scores'

    id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(10), nullable=False)
    attempts = db.Column(db.Integer, nullable=False)
    elapsed_time = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)