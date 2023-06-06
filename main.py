from datetime import datetime, timedelta
from models import Customer, Contract, RevenueSegment, Invoice
from database import reset_and_init_db, Session
import pandas as pd

def main():
    reset_and_init_db()
    print('Refreshed and initialized the database.')
    
    # Create a new session
    session = Session()

    # Create a new Customer
    customer = Customer(
        name='Acme Inc.',
    )

    # Add the customer to the session
    session.add(customer)

    # Create a new Contract
    contract = Contract(
        booked_month=2,
    )

    # Add the contract to the session
    customer.contracts.append(contract)

    # Create a recurring RevenueSegment for the Contract
    revenue_segment = RevenueSegment(
        contract=contract,
        delay_mths=3,
        length_mths=5,
        is_recurring=1,
        amount=100.00,
        type='Product',
        name='Recurring License Revenue',
    )

    # Add the revenue segment to the contract
    contract.revenue_segments.append(revenue_segment)

    # Commit the session to save these objects to the database
    session.commit()

    num_months = 12

    # Initialize dataframe with zero values
    df = pd.DataFrame(0, index=range(1, num_months), columns=['TCV', 'DefRev', 'Rev', 'AR', 'Cash'])

    # Query all objects
    revenue_segments = session.query(RevenueSegment).all()
    invoices = session.query(Invoice).all()

    # Populate the dataframe
    for segment in revenue_segments:
        total_contract_value = segment.get_total_revenue()
        booked_month = segment.contract.booked_month
        df.loc[booked_month, 'TCV'] += total_contract_value  # add to the current value
        for i in range(booked_month + segment.delay_mths, booked_month + segment.delay_mths + segment.length_mths):
            df.loc[i, 'Rev'] += segment.amount
            for j in range(i, num_months):
                df.loc[j, 'DefRev'] -= segment.amount

    for invoice in invoices:
        issue_month = invoice.issue_mth
        paid_month = invoice.issue_mth + invoice.mths_payable
        for i in range(issue_month, num_months):
            df.loc[i, 'AR'] += invoice.amount
            df.loc[i, 'DefRev'] += invoice.amount
        for i in range(paid_month, num_months):
            df.loc[i, 'Cash'] += invoice.amount
            df.loc[i, 'AR'] -= invoice.amount

    # Display the dataframe
    print(df.T)

    # Close the session
    session.close()


if __name__ == '__main__':
    main()
