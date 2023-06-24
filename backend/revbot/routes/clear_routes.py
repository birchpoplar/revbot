from flask import jsonify, Blueprint, g
from sqlalchemy import delete
from revbot.models import Customer, Contract, RevenueSegment, Invoice

# You may need to adjust these imports according to your app structure

clear_routes = Blueprint('clear_routes', __name__)

@clear_routes.route('/clear_database', methods=['DELETE'])
def clear_database():
    try:
        g.db_session.query(Invoice).delete()
        g.db_session.query(RevenueSegment).delete()
        g.db_session.query(Contract).delete()
        g.db_session.query(Customer).delete()
        g.db_session.commit()
        return jsonify({'message': 'Database cleared successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
