from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String, Enum
from sqlalchemy.orm import relationship
from .database import Base
import enum

class TransactionType(enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"

class TransactionCategory(enum.Enum):
    SUBSCRIPTION = "subscription"
    MAINTENANCE = "maintenance"
    SALARY = "salary"
    UTILITIES = "utilities"
    OTHER = "other"

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(TransactionType), nullable=False)
    category = Column(Enum(TransactionCategory), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String(255), nullable=False)
    date = Column(DateTime, nullable=False)
    created_by = Column(Integer, ForeignKey('users.id'))
    reference_id = Column(String(100))  # For linking to subscriptions or other records
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    creator = relationship("User")

    @classmethod
    def get_balance_sheet(cls, db, start_date: datetime, end_date: datetime):
        """Generate a balance sheet for a given period"""
        transactions = db.query(cls).filter(
            cls.date >= start_date,
            cls.date <= end_date
        ).all()

        total_income = sum(t.amount for t in transactions if t.type == TransactionType.INCOME)
        total_expense = sum(t.amount for t in transactions if t.type == TransactionType.EXPENSE)
        
        return {
            'total_income': total_income,
            'total_expense': total_expense,
            'net_profit': total_income - total_expense,
            'transactions': transactions
        }
