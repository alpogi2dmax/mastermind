import pytest
from app import create_app
from extensions import db
from models import Score

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(autouse=True)
def setup_scores(app):
    # Populate some test scores
    with app.app_context():
        Score.query.delete()
        scores = [
            Score(player_name="Alice", difficulty="Easy", attempts=3, elapsed_time=15.2),
            Score(player_name="Bob", difficulty="Easy", attempts=4, elapsed_time=20.0),
            Score(player_name="Charlie", difficulty="Normal", attempts=2, elapsed_time=10.0),
            Score(player_name="Dana", difficulty="Hard", attempts=5, elapsed_time=30.0),
        ]
        db.session.add_all(scores)
        db.session.commit()
    yield
    # Cleanup
    with app.app_context():
        Score.query.delete()
        db.session.commit()

# -------------------------
# TESTS
# -------------------------

def test_get_leaderboard(client):
    response = client.get("/api/getleaderboard")
    data = response.get_json()
    
    assert response.status_code == 200
    # Check keys
    assert "Easy" in data
    assert "Normal" in data
    assert "Hard" in data
    
    # Check that scores are returned
    assert len(data['Easy']) == 2
    assert data['Easy'][0]['player_name'] == "Alice"  # fastest first
    assert len(data['Normal']) == 1
    assert len(data['Hard']) == 1