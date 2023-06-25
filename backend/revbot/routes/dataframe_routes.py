import json
from flask import Blueprint, jsonify, request, g
from revbot.models import Customer, Contract, RevenueSegment, Invoice
from revbot.services import populate_dataframe
from sqlalchemy import exc  
import pandas as pd

dataframe_routes = Blueprint('dataframe_routes', __name__)

@dataframe_routes.route('/dataframe', methods=['GET'])
def get_dataframe():

    # Query for the revenue segments and invoices
    revenue_segments = g.db_session.query(RevenueSegment).all()
    invoices = g.db_session.query(Invoice).all()
    
    # Initialize dataframe with zero values
    num_months = 48
    df = pd.DataFrame(0, index=range(1, num_months), columns=['TCV', 'Rev', 'DefRev', 'UnbilledRev', 'AR', 'Cash'])

    # Populate the DataFrame
    df = populate_dataframe(revenue_segments, invoices, df, num_months)
    
    # Convert the DataFrame to JSON and return it
    return jsonify(json.loads(df.to_json(orient="split")))
