from revbot.models import Customer, Contract, RevenueSegment, Invoice
from revbot.utils import reset_and_init_db, Session, populate_dataframe, display
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
        delay_rev_start_mths=2,
        delay_inv_from_rev_mths=2,
        length_rev_mths=7,
        amount=210.00,
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
    df = pd.DataFrame(0, index=range(1, num_months), columns=['TCV', 'Rev', 'DefRev', 'UnbilledRev', 'AR', 'Cash'])

    # Query all objects
    revenue_segments = session.query(RevenueSegment).all()
    invoices = session.query(Invoice).all()

    # Populate the dataframe
    populate_dataframe(revenue_segments, invoices, df, num_months)

    # Display the dataframe
    display.display_df(df)

    # Close the session
    session.close()


if __name__ == '__main__':
    main()
