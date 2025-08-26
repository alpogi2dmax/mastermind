import pytest
import random
from app import create_app
from extensions import db
from game import GAME

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
    # Reset GAME object before each test
    GAME['secret'] = [1, 2, 3, 4]
    GAME['hint'] = ['__'] * 4
    GAME['attempts'] = 0
    GAME['finished'] = False
    yield

# -------------------------
# TESTS
# -------------------------

def test_get_hint_success(client):
    response = client.get("/api/gethint")
    data = response.get_json()
    assert response.status_code == 200
    # One hint should now be revealed
    assert data['hint'].count('__') == 3
    assert data['attempts'] == 1
    assert data['finished'] is False

def test_get_hint_last_available(client):
    # Reveal 3 hints first
    GAME['hint'] = [1, 2, 3, '__']
    response = client.get("/api/gethint")
    data = response.get_json()
    assert response.status_code == 200
    # No blanks left, game should finish
    assert data['hint'].count('__') == 0
    assert data['finished'] is True

def test_get_hint_no_more_hints(client):
    # All hints already revealed
    GAME['hint'] = [1, 2, 3, 4]
    response = client.get("/api/gethint")
    data = response.get_json()
    assert response.status_code == 400
    assert "No more hints" in data['error']