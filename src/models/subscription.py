from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String, Enum
from sqlalchemy.orm import relationship
from .database import Base
from .member import MembershipType

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey('members.id'), nullable=False)
    type = Column(Enum(MembershipType), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    amount = Column(Float, nullable=False)
    payment_status = Column(String(20), nullable=False)  # paid, pending, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, ForeignKey('users.id'))
    payment_reference = Column(String(100))
    notes = Column(String(255))

    # Relationships
    member = relationship("Member", back_populates="subscriptions")
    creator = relationship("User")

    @property
    def is_active(self):
        """Check if the subscription is currently active"""
        now = datetime.utcnow()
        return self.payment_status == 'paid' and self.start_date <= now <= self.end_date

    @property
    def days_remaining(self):
        """Calculate remaining days in subscription"""
        now = datetime.utcnow()
        if now > self.end_date:
            return 0
        return (self.end_date - now).days
