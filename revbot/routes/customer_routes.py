from flask import Blueprint, jsonify, request, g
from revbot.models import Customer, Contract, RevenueSegment, Invoice
from sqlalchemy import exc  

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
    customer = g.db_session.query(Customer).get(customer_id)
    g.db_session.delete(customer)
    g.db_session.commit()
    return jsonify({'message': f'Customer {customer_id} deleted'}), 200

# Routes to obtain details for customers

@customer_routes.route('/customers', methods=['GET'])
def get_customers():
    customers = g.db_session.query(Customer).all()
    return jsonify([c.serialize() for c in customers])

@customer_routes.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = g.db_session.query(Customer).get(customer_id)
    return jsonify(customer.serialize())

