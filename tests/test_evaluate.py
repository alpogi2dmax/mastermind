import pytest
from app import create_app
from extensions import db
from game import GAME, reset_game

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(autouse=True)
def reset_game_before_each_test():
    # Clear the GAME object before each test
    GAME['secret'] = []
    GAME['history'] = []
    GAME['attempts'] = 0
    GAME['finished'] = False
    GAME['player'] = None
    GAME['difficulty'] = 'Normal'
    GAME['start_time'] = 0
    GAME['end_time'] = 0
    GAME['elapsed_time'] = 0
    GAME['max_attempts'] = 10
    yield

# -------------------------
# TESTS
# -------------------------

def test_evaluate_guess_no_secret(client):
    payload = {"guess": [1,2,3,4]}
    response = client.post("/api/evaluate", json=payload)
    data = response.get_json()
    assert response.status_code == 400
    assert "No secret code generated" in data['error']

def test_evaluate_guess_invalid_length(client):
    # Set secret code
    GAME['secret'] = [1,2,3,4]
    payload = {"guess": [1,2]}
    response = client.post("/api/evaluate", json=payload)
    data = response.get_json()
    assert response.status_code == 400
    assert "same length" in data['error']

def test_evaluate_guess_invalid_digit(client):
    # Set secret code
    GAME['secret'] = [1,2,3,4]
    payload = {"guess": [1,2,3,20]}  # 20 is outside default PARAMS['max']
    response = client.post("/api/evaluate", json=payload)
    data = response.get_json()
    assert response.status_code == 200
    assert "All digits must be integers" in data['error']

def test_evaluate_guess_correct(client):
    # Set secret code and player
    GAME['secret'] = [1,2,3,4]
    GAME['player'] = "Alpogi"
    GAME['start_time'] = 1  # to avoid elapsed_time=0
    payload = {"guess": [1,2,3,4]}
    response = client.post("/api/evaluate", json=payload)
    data = response.get_json()
    assert response.status_code == 200
    assert data['finished'] is True
    assert data['attempts'] == 1
    assert len(data['history']) == 1
    assert data['history'][0]['correct_location'] == 4