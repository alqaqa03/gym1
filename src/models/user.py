from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship
from .database import Base
import bcrypt
import enum

class UserRole(enum.Enum):
    ADMIN = "admin"
    SUPERVISOR = "supervisor"
    EMPLOYEE = "employee"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)

    # Relationships
    attendance_records = relationship("AttendanceRecord", back_populates="user")

    def set_password(self, password: str):
        """Hash and set the user's password"""
        salt = bcrypt.gensalt()
        self.hashed_password = bcrypt.hashpw(password.encode(), salt)

    def check_password(self, password: str) -> bool:
        """Verify the user's password"""
        return bcrypt.checkpw(password.encode(), self.hashed_password)

    def has_permission(self, permission: str) -> bool:
        """Check if user has specific permission based on role"""
        permission_map = {
            UserRole.ADMIN: ["all"],
            UserRole.SUPERVISOR: ["manage_members", "view_reports", "manage_attendance"],
            UserRole.EMPLOYEE: ["view_members", "record_attendance"]
        }
        allowed_permissions = permission_map.get(self.role, [])
        return "all" in allowed_permissions or permission in allowed_permissions
