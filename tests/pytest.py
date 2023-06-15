import pytest
import json
from flask import g 
from revbot.app import create_app

@pytest.fixture(scope='module')
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

def test_create_contract(client):
    response = client.post(
        "/contracts",
        data=json.dumps(dict(booked_month=1, customer_id=1)),
        content_type='application/json',
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data['message'] == 'Contract created for customer 1 in month 1'

def test_create_revenuesegment(client):
    response = client.post(
        "/revenuesegments",
        data=json.dumps(dict(contract_id=1, amount=1000, name='Test revenue segment', type='Product', delay_rev_start_mths=0, length_rev_mths=1, delay_inv_from_rev_mths=0, invoice_schedule='Monthly')),
        content_type='application/json',
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data['message'] == 'Revenue segment created for contract 1'
