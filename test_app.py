import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_route(client):
    """Test the home route returns 200"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Hello from Flask DevOps Challenge!' in response.data

def test_health_route(client):
    """Test the health check route"""
    response = client.get('/health')
    assert response.status_code == 200
    assert b'healthy' in response.data

def test_about_route(client):
    """Test the about route"""
    response = client.get('/about')
    assert response.status_code == 200
    assert b'DevOps Challenge Flask App' in response.data

def test_json_response(client):
    """Test that responses are JSON"""
    response = client.get('/')
    assert response.content_type == 'application/json'
