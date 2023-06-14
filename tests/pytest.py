import pytest
import json
from flask import g 
from revbot.app import create_app

@pytest.fixture
def client():
    app = create_app()  # create an instance of your Flask application

    with app.test_client() as client:  # create a test client
        with app.app_context():
            yield app.test_client()

def test_create_customer(client):
    response = client.post(
        "/customers",
        data=json.dumps(dict(name="Test customer", email="test@example.com")),
        content_type='application/json',
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data['message'] == 'Customer created'
