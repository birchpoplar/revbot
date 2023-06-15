import requests
import pandas as pd
import json
from revbot.services.display_df import display_df

def create_customer():
    data = {
        "name": "Test Customer"
    }
    response = requests.post('http://localhost:5000/customers', json=data)
    if response.status_code == 200:
        print("Customer created successfully")
    else:
        print("Failed to create customer")
    return response.json()

def create_contract(customer_id):
    data = {
        "customer_id": customer_id,
        "booked_month": 10,
    }
    response = requests.post('http://localhost:5000/contracts', json=data)
    if response.status_code == 200:
        print("Contract created successfully")
    else:
        print("Failed to create contract")
    return response.json()

def create_revenue_segment(contract_id):
    data = {
        "contract_id" : contract_id,
        "amount" : 1000,
        "name"  : 'Test revenue segment',
        "type" : 'Product',
        "delay_rev_start_mths" : 2,
        "length_rev_mths" : 12,
        "delay_inv_from_rev_mths" : 4,
        "invoice_schedule" : 'Monthly' 
    }
    response = requests.post('http://localhost:5000/revenuesegments', json=data)
    if response.status_code == 200:
        print("Revenue segment created successfully")
    else:
        print("Failed to create revenue segment")
    return response.json()

def get_dataframe():
    response = requests.get('http://localhost:5000/dataframe')
    data = json.loads(response.json())

    df = pd.DataFrame(data=data['data'], index=data['index'], columns=data['columns'])
    
    # Display the dataframe
    display_df(df)

if __name__ == "__main__":
    # Create customer
    customer_response = create_customer()
    
    # Create contract
    contract_response = create_contract(1)
    
    # Create revenue segment
    create_revenue_segment(1)
    
    # Get and display dataframe
    get_dataframe()
