from flask import Blueprint, jsonify, request, g, abort
from revbot.models import Customer, Contract, RevenueSegment, Invoice
from sqlalchemy import exc  
from sqlalchemy.orm.exc import NoResultFound

customer_routes = Blueprint('customer_routes', __name__) 

# Routes to create and delete customers

@customer_routes.route('/customers', methods=['POST'])
def create_customer():
    customer = Customer(request.json['name'])
    g.db_session.add(customer)
    g.db_session.commit()
    return jsonify({'message': f'Customer {customer.id} created', 'id': customer.id}), 200

@customer_routes.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = g.db_session.get(Customer, customer_id)
    if customer is None:
        return jsonify({'message': f'Customer {customer_id} not found'}), 404
    g.db_session.delete(customer)
    g.db_session.commit()
    return jsonify({'message': f'Customer {customer_id} deleted'}), 200

# Routes to obtain details for customers

@customer_routes.route('/customers', methods=['GET'])
def get_customers():
    customers = g.db_session.query(Customer).all()
    return jsonify({'message': f'Customer list retrieved', 'data': [c.serialize() for c in customers]})

@customer_routes.route('/customers/id/<int:customer_id>', methods=['GET'])
def get_customer_by_id(customer_id):
    customer = g.db_session.query(Customer).get(customer_id)
    return jsonify(customer.serialize())

@customer_routes.route('/customers/name/<string:customer_name>', methods=['GET'])
def get_customer_by_name(customer_name):
    try:
        customer = g.db_session.query(Customer).filter_by(name=customer_name).one()
        return jsonify({'message': f'Customer details retrieved', 'data': customer.serialize()})
    except NoResultFound:
        abort(403, description="Customer not found")

@customer_routes.route('/customers/id/<int:customer_id>/contracts', methods=['GET'])
def get_contracts_for_customer(customer_id):
    customer = g.db_session.query(Customer).get(customer_id)
    if customer is None:
        return jsonify({'error': 'Customer not found'}), 404
    return jsonify([c.serialize() for c in customer.contracts])