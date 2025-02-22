from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship
from .database import Base

class AttendanceRecord(Base):
    __tablename__ = "attendance_records"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey('members.id'), nullable=False)
    check_in = Column(DateTime, nullable=False)
    check_out = Column(DateTime)
    fingerprint_verified = Column(Boolean, default=False)
    recorded_by = Column(Integer, ForeignKey('users.id'))
    notes = Column(String(255))

    # Relationships
    member = relationship("Member", back_populates="attendance_records")
    user = relationship("User", back_populates="attendance_records")

    @property
    def duration(self):
        """Calculate the duration of the visit"""
        if not self.check_out:
            return None
        return self.check_out - self.check_in

    @classmethod
    def get_member_attendance(cls, db, member_id: int, start_date: datetime, end_date: datetime):
        """Get attendance records for a member within a date range"""
        return db.query(cls).filter(
            cls.member_id == member_id,
            cls.check_in >= start_date,
            cls.check_in <= end_date
        ).all()
