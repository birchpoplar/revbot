from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    contracts = relationship("Contract", back_populates="customer")

    def __init__(self, name):
        self.name = name

class Contract(Base):
    __tablename__ = 'contracts'
    
    id = Column(Integer, primary_key=True)
    booked_month = Column(Integer)

    # Parent is Customer
    customer_id = Column(Integer, ForeignKey('customers.id')) 
    customer = relationship("Customer", back_populates="contracts")

    # Children are RevenueSegments
    revenue_segments = relationship("RevenueSegment", back_populates="contract")

    def __init__(self, booked_month):
        self.booked_month = booked_month

class Invoice(Base):
    __tablename__ = 'invoices'

    id = Column(Integer, primary_key=True)
    issue_mth = Column(Integer)
    amount = Column(Integer)
    mths_payable = Column(Integer)

    # Parent is RevenueSegment
    revenue_segment_id = Column(Integer, ForeignKey('revenue_segments.id'))
    revenue_segment = relationship("RevenueSegment", back_populates="invoices")

    def __init__(self, months_delay, amount, mths_payable, contract_booked_month):
        super().__init__()
        self.amount = amount
        self.mths_payable = mths_payable

        # Set the issue month based on the delay
        self.issue_mth = contract_booked_month + months_delay

class RevenueSegment(Base):
    __tablename__ = 'revenue_segments'

    id = Column(Integer, primary_key=True)
    delay_rev_start_mths = Column(Integer) # number of months from booked date to start of revenue
    length_rev_mths = Column(Integer) # should be 1 for one-time revenue
    delay_inv_from_rev_mths = Column(Integer) # number of months from start of revenue to invoice, can be negative
    amount = Column(Integer) # one-time amount or recurring amount
    name = Column(String) 
    type = Column(Enum('Service', 'Product', name='revenue_segment_type'))
    invoice_schedule = Column(Enum('Upfront', 'Monthly', name='invoice_schedule'))
    _unbilled_balance = Column(Integer) # unbilled balance for this revenue segment (private variable)
    
    # Parent is Contract
    contract_id = Column(Integer, ForeignKey('contracts.id'))
    contract = relationship("Contract", back_populates="revenue_segments")

    # Children are Invoices
    invoices = relationship("Invoice", back_populates="revenue_segment")

    def __init__(self, contract, amount, name, type, delay_rev_start_mths, length_rev_mths, delay_inv_from_rev_mths=0, invoice_schedule='Upfront'):
        self.contract = contract
        self.delay_rev_start_mths = delay_rev_start_mths 
        self.length_rev_mths = length_rev_mths 
        self.delay_inv_from_rev_mths = delay_inv_from_rev_mths
        self.amount = amount
        self.name = name
        self.type = type
        self.invoice_schedule = invoice_schedule

        # Create invoice(s) for this revenue segment
        if self.invoice_schedule == 'Upfront':
            invoice = Invoice(
                months_delay=self.delay_rev_start_mths + self.delay_inv_from_rev_mths,
                amount=self.amount * self.length_rev_mths,
                mths_payable=1,
                contract_booked_month=self.contract.booked_month
            )
            self.invoices.append(invoice)
        elif self.invoice_schedule == 'Monthly':
            for i in range(self.length_rev_mths):
                invoice = Invoice(
                    months_delay=self.delay_rev_start_mths + delay_inv_from_rev_mths + i,
                    amount=self.amount,
                    mths_payable=1,
                    contract_booked_month=self.contract.booked_month
                )
                self.invoices.append(invoice)

    def get_total_revenue(self):
        return sum([invoice.amount for invoice in self.invoices])