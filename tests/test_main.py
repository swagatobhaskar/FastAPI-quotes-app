from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/root")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}

def test_home_root():
    response = client.get("/")
    assert response.status_code == 200

def test_all_quotes_route():
    response = client.get("/api/all-quotes")
    assert response.status_code == 200

def test_new_quote():
    pass
