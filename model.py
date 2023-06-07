import pandas as pd

def populate_dataframe(revenue_segments, invoices, df, num_months):
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
        issue_month = invoice.issue_mth
        paid_month = invoice.issue_mth + invoice.mths_payable

        for i in range(issue_month, num_months):
            df.loc[i, 'AR'] += invoice.amount
            if segment.delay_inv_from_rev_mths > 0:
                if segment.delay_inv_from_rev_mths > segment.length_rev_mths:
                    df.loc[i, 'UnbilledRev'] -= invoice.amount
                else:
                    if segment.invoice_schedule == 'Monthly':
                        if issue_month < booked_month + segment.delay_rev_start_mths + segment.length_rev_mths:
                            df.loc[i, 'DefRev'] += invoice.amount
                        elif issue_month >= booked_month + segment.delay_rev_start_mths + segment.length_rev_mths:
                            df.loc[i, 'UnbilledRev'] -= invoice.amount
                    else:
                        df.loc[i, 'UnbilledRev'] -= segment.delay_inv_from_rev_mths * segment.amount
                        df.loc[i, 'DefRev'] += (segment.length_rev_mths - segment.delay_inv_from_rev_mths) * segment.amount
            else:
                df.loc[i, 'DefRev'] += invoice.amount    

        for i in range(paid_month, num_months):
            df.loc[i, 'Cash'] += invoice.amount
            df.loc[i, 'AR'] -= invoice.amount
    return df