from flask import Blueprint, jsonify, request, g
from revbot.models import Customer, Contract, RevenueSegment, Invoice
from sqlalchemy import exc  

contract_routes = Blueprint('contract_routes', __name__)

# Routes to create and delete contracts

@contract_routes.route('/contracts', methods=['POST'])
def create_contract():
    customer_id = request.json['customer_id']
    booked_month = request.json['booked_month']

    customer = g.db_session.get(Customer, customer_id)
    if customer is None:
        return jsonify({'error': 'Customer not found'}), 404
    
    contract = Contract(booked_month)
    customer.contracts.append(contract)
    # g.db_session.add(contract)
    g.db_session.commit()
    return jsonify({'message': f'Contract created for customer {customer_id} in month {booked_month}'}), 200

@contract_routes.route('/contracts/<int:contract_id>', methods=['DELETE'])
def delete_contract(contract_id):
    contract = g.db_session.get(Contract, contract_id)
    g.db_session.delete(contract)
    g.db_session.commit()
    return jsonify({'message': f'Contract {contract_id} deleted'}), 200

# Routes to obtain details for contracts

@contract_routes.route('/contracts', methods=['GET'])
def get_contracts():
    contracts = g.db_session.query(Contract).all()
    return jsonify([c.serialize() for c in contracts])

@contract_routes.route('/contracts/<int:contract_id>', methods=['GET'])
def get_contract(contract_id):
    contract = g.db_session.query(Contract).get(contract_id)
    return jsonify(contract.serialize())

# Route to get contracts for a customer

@contract_routes.route('/customers/<int:customer_id>/contracts', methods=['GET'])
def get_contracts_for_customer(customer_id):
    customer = g.db_session.query(Customer).get(customer_id)
    if customer is None:
        return jsonify({'error': 'Customer not found'}), 404
    return jsonify([c.serialize() for c in customer.contracts])

