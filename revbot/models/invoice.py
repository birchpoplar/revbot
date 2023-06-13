from .base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

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

    def serialize(self):
        return {
            'id': self.id,
            'issue_mth': self.issue_mth,
            'amount': self.amount,
            'mths_payable': self.mths_payable
        }