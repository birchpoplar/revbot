from flask import Blueprint, jsonify, request, g
from revbot.models import Customer, Contract, RevenueSegment, Invoice
from sqlalchemy import exc  

revenuesegment_routes = Blueprint('revenuesegment_routes', __name__)

# Routes to create and delete revenue segments

@revenuesegment_routes.route('/revenuesegments', methods=['POST'])
def create_revenuesegment():
    contract = g.db_session.get(Contract, request.json['contract_id'])
    if contract is None:
        return jsonify({'error': 'Contract not found'}), 404

    revenuesegment = RevenueSegment(
        contract=contract,
        amount=request.json['amount'],
        name=request.json['name'],
        type=request.json['type'],
        delay_rev_start_mths=request.json['delay_rev_start_mths'],
        length_rev_mths=request.json['length_rev_mths'],
        delay_inv_from_rev_mths=request.json['delay_inv_from_rev_mths'],
        invoice_schedule=request.json['invoice_schedule']
    )
    
    contract.revenue_segments.append(revenuesegment)
    g.db_session.commit()
    return jsonify({'message': f'Revenue segment {revenuesegment.id} created for contract {contract.id}', 'id': revenuesegment.id}), 200

@revenuesegment_routes.route('/revenuesegments/<int:revenuesegment_id>', methods=['DELETE'])
def delete_revenuesegment(revenuesegment_id):
    revenuesegment = g.db_session.get(RevenueSegment, revenuesegment_id)
    g.db_session.delete(revenuesegment)
    g.db_session.commit()
    return jsonify({'message': f'Revenue segment {revenuesegment_id} deleted'}), 200

@revenuesegment_routes.route('/revenuesegments/', methods=['GET'])
def get_revenuesegments():
    revenuesegments = g.db_session.query(RevenueSegment).all()
    return jsonify([r.serialize() for r in revenuesegments])

@revenuesegment_routes.route('/revenuesegments/<int:revenuesegment_id>', methods=['GET'])
def get_revenuesegment(revenuesegment_id):
    revenuesegment = g.db_session.get(RevenueSegment, revenuesegment_id)
    return jsonify(revenuesegment.serialize())

@revenuesegment_routes.route('/contracts/<int:contract_id>/revenuesegments', methods=['GET'])
def get_revenuesegments_for_contract(contract_id):
    contract = g.db_session.get(Contract, contract_id)
    if contract is None:
        return jsonify({'error': 'Contract not found'}), 404
    return jsonify([r.serialize() for r in contract.revenue_segments])