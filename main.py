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
        delay_rev_start_mths=5,
        delay_inv_from_rev_mths=-3,
        length_rev_mths=4,
        amount=100.00,
        type='Product',
        name='Recurring License Revenue',
        invoice_schedule='Upfront',
    )

    # Add the revenue segment to the contract
    contract.revenue_segments.append(revenue_segment)

    # Commit the session to save these objects to the database
    session.commit()

    num_months = 13

    # Initialize dataframe with zero values
    df = pd.DataFrame(0, index=range(1, num_months), columns=['TCV', 'DefRev', 'UnbilledRev', 'Rev', 'AR', 'Cash'])

    # Query all objects
    revenue_segments = session.query(RevenueSegment).all()
    invoices = session.query(Invoice).all()

    # Populate the dataframe
    for segment in revenue_segments:
        total_contract_value = segment.get_total_revenue()
        booked_month = segment.contract.booked_month

        # Post the total contract value to the booked month
        df.loc[booked_month, 'TCV'] += total_contract_value

        # Record revenue for each month
        for i in range(booked_month + segment.delay_rev_start_mths, booked_month + segment.delay_rev_start_mths + segment.length_rev_mths):
            df.loc[i, 'Rev'] += segment.amount
            if segment.delay_inv_from_rev_mths > 0 and i < booked_month + segment.delay_rev_start_mths + segment.delay_inv_from_rev_mths:
                for j in range(i, num_months):
                    df.loc[j, 'UnbilledRev'] += segment.amount
            else:
                for j in range(i, num_months):
                    df.loc[j, 'DefRev'] -= segment.amount

    for invoice in invoices:
        print('processing invoice')
        issue_month = invoice.issue_mth
        paid_month = invoice.issue_mth + invoice.mths_payable

        for i in range(issue_month, num_months):
            df.loc[i, 'AR'] += invoice.amount
            if segment.delay_inv_from_rev_mths > 0:
                if i > booked_month + segment.delay_rev_start_mths + segment.length_rev_mths:
                    df.loc[i, 'UnbilledRev'] -= invoice.amount
                else:
                    df.loc[i, 'UnbilledRev'] -= segment.delay_inv_from_rev_mths * segment.amount
                    df.loc[i, 'DefRev'] += (segment.length_rev_mths - segment.delay_inv_from_rev_mths) * segment.amount
            else:
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
