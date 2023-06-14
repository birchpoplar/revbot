from .base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Contract(Base):
    __tablename__ = 'contracts'
    
    id = Column(Integer, primary_key=True)
    booked_month = Column(Integer)

    # Parent is Customer
    customer_id = Column(Integer, ForeignKey('customers.id')) 
    customer = relationship("Customer", back_populates="contracts")

    # Children are RevenueSegments
    revenue_segments = relationship("RevenueSegment", back_populates="contract", cascade="all, delete, delete-orphan")

    def __init__(self, booked_month):
        self.booked_month = booked_month

    def serialize(self):
        return {
            'id': self.id,
            'booked_month': self.booked_month,
            'customer': self.customer.serialize(),
            'revenue_segments': [revenue_segment.serialize() for revenue_segment in self.revenue_segments]
        }