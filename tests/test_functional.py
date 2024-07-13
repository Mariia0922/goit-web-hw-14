import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_contacts():
    response = client.get("/contacts/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
