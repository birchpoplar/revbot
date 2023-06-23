import pytest
import json
import os
from flask import g 
from revbot.app import create_app

@pytest.fixture(scope='module')
def client():
    config_class = os.getenv('FLASK_CONFIG', 'TestingConfig')
    app = create_app(config_class) # Create an app instance

    with app.test_client() as client:  # create a test client
        with app.app_context():
            yield app.test_client()

# Create tests

def test_create_customer(client):
    response = client.post(
        "/customers",
        data=json.dumps(dict(name="Test customer", email="test@example.com")),
        content_type='application/json',
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data['message'] == f'Customer 1 created'

def test_create_contract(client):
    response = client.post(
        "/contracts",
        data=json.dumps(dict(booked_month=1, customer_id=1)),
        content_type='application/json',
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data['message'] == f'Contract 1 created for customer 1 in month 1'

def test_create_revenuesegment(client):
    response = client.post(
        "/revenuesegments",
        data=json.dumps(dict(contract_id=1, amount=1000, name='Test revenue segment', type='Product', delay_rev_start_mths=0, length_rev_mths=1, delay_inv_from_rev_mths=0, invoice_schedule='Monthly')),
        content_type='application/json',
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data['message'] == f'Revenue segment 1 created for contract 1'

# Delete revenue segment test

def test_delete_revenuesegment(client):
    response = client.delete(
        "/revenuesegments/1"
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data['message'] == f'Revenue segment 1 deleted'

# Delete contract test

def test_delete_contract(client):
    response = client.delete(
        "/contracts/1"
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data['message'] == f'Contract 1 deleted'

# Delete customer test

def test_delete_customer(client):
    response = client.delete(
        "/customers/1"
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data['message'] == f'Customer 1 deleted'