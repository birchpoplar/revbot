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
        print("Customer created successfully : id " + str(response.json()['id']))
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
        print("Contract created successfully : id " + str(response.json()['id']))
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
        "delay_inv_from_rev_mths" : -3,
        "invoice_schedule" : 'Monthly' 
    }
    response = requests.post('http://localhost:5000/revenuesegments', json=data)
    if response.status_code == 200:
        print("Revenue segment created successfully : id " + str(response.json()['id']))
    else:
        print("Failed to create revenue segment")
    return response.json()

def get_dataframe():
    response = requests.get('http://localhost:5000/dataframe')
    data = response.json()

    df = pd.DataFrame(data=data['data'], index=data['index'], columns=data['columns'])
    
    # Display the dataframe
    display_df(df)

def clear_database():
    response = requests.delete('http://localhost:5000/clear_database')
    if response.status_code == 200:
        print("Database cleared successfully")
    else:
        print("Failed to clear database")
    return response.json()

if __name__ == "__main__":
    # Clear database
    # clear_database()
    
    # Create customer
    customer = create_customer()
        
    # Create contract
    contract = create_contract(customer['id'])
    
    # Create revenue segment
    create_revenue_segment(contract['id'])
    
    # Get and display dataframe
    get_dataframe()
