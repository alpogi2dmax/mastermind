import pytest
from unittest.mock import patch, Mock
import requests
from app import create_app
from extensions import db

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:/memory:'
    })
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@patch('resources.generate.requests.get')
def test_generate_code_success(mock_get, client):

    mock_response = Mock()
    mock_response.text = '1\n2\n3\n4'
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    payload = {
        'difficulty': 'easy',
        'player': 'Alice',
        'settings': {'num': 4, 'min': 0, 'max': 6}
    }

    response = client.post('/api/generate', json=payload)
    data = response.get_json()

    assert response.status_code == 200
    assert data['secret'] == [1, 2, 3, 4]
    assert data['attempts'] == 0
    assert data['finished'] is False

def test_generate_code_num_validation(client):
    payload = {
        'difficulty': 'easy',
        'player': 'David',
        'settings': {'num': 9, 'min': 0, 'max': 6}
    }

    response = client.post('/api/generate', json=payload)
    data = response.get_json()

    assert response.status_code == 400
    assert 'error' in data

def test_generate_code_max_validation(client):
    payload = {
        "difficulty": "easy",
        "player": "Alice",
        "settings": {"num": 4, "max": 12}  # invalid max > 10
    }

    response = client.post("/api/generate", json=payload)
    data = response.get_json()

    assert response.status_code == 400
    assert "error" in data

@patch("resources.generate.requests.get")
def test_generate_code_request_exception(mock_get, client):
    mock_get.side_effect = requests.RequestException("Connection error")

    payload = {
        "difficulty": "easy",
        "player": "Alice",
        "settings": {"num": 4, "max": 6}
    }

    response = client.post("/api/generate", json=payload)
    data = response.get_json()

    assert response.status_code == 500
    assert "error" in data