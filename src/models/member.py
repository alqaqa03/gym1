from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, LargeBinary, Enum, Text, Boolean
from sqlalchemy.orm import relationship
from .database import Base
import enum

class MembershipType(enum.Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    SEMI_ANNUAL = "semi_annual"
    ANNUAL = "annual"

class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(100))
    fingerprint_data = Column(LargeBinary)
    membership_type = Column(Enum(MembershipType), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    emergency_contact = Column(String(100))
    medical_conditions = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, ForeignKey('users.id'))
    is_active = Column(Boolean, default=True)

    # Relationships
    attendance_records = relationship("AttendanceRecord", back_populates="member")
    subscriptions = relationship("Subscription", back_populates="member")
    creator = relationship("User")

    def is_membership_valid(self) -> bool:
        """Check if the member's membership is currently valid"""
        now = datetime.utcnow()
        return self.is_active and self.start_date <= now <= self.end_date

    def days_until_expiry(self) -> int:
        """Calculate days remaining until membership expires"""
        now = datetime.utcnow()
        if now > self.end_date:
            return 0
        return (self.end_date - now).days
