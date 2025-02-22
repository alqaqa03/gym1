from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                               QLabel, QFrame)
from PyQt6.QtCore import Qt, QTimer
from src.models.database import SessionLocal
from src.models.member import Member
from src.models.attendance import AttendanceRecord
from src.models.subscription import Subscription
from datetime import datetime, timedelta

class StatCard(QFrame):
    def __init__(self, title, value, icon=None):
        super().__init__()
        self.init_ui(title, value, icon)
        
    def init_ui(self, title, value, icon):
        self.setObjectName("stat-card")
        layout = QVBoxLayout()
        
        # Add title
        title_label = QLabel(title)
        title_label.setObjectName("stat-title")
        layout.addWidget(title_label)
        
        # Add value
        value_label = QLabel(str(value))
        value_label.setObjectName("stat-value")
        layout.addWidget(value_label)
        
        self.setLayout(layout)
        
class DashboardWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
        # Update stats every 5 minutes
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(300000)  # 5 minutes in milliseconds
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Create title
        title = QLabel("لوحة التحكم")
        title.setObjectName("dashboard-title")
        layout.addWidget(title)
        
        # Create stats container
        stats_layout = QHBoxLayout()
        
        # Create stat cards
        self.total_members = StatCard("إجمالي الأعضاء", "0")
        self.active_members = StatCard("الأعضاء النشطين", "0")
        self.today_attendance = StatCard("حضور اليوم", "0")
        self.expiring_soon = StatCard("اشتراكات تنتهي قريباً", "0")
        
        # Add cards to layout
        stats_layout.addWidget(self.total_members)
        stats_layout.addWidget(self.active_members)
        stats_layout.addWidget(self.today_attendance)
        stats_layout.addWidget(self.expiring_soon)
        
        # Add stats layout to main layout
        layout.addLayout(stats_layout)
        
        # Add stretch to push everything to the top
        layout.addStretch()
        
        # Set main layout
        self.setLayout(layout)
        
        # Apply styles
        self.setStyleSheet("""
            #dashboard-title {
                font-size: 24px;
                color: #1a237e;
                margin: 20px;
            }
            #stat-card {
                background-color: white;
                border-radius: 8px;
                padding: 20px;
                margin: 10px;
                min-width: 200px;
            }
            #stat-title {
                font-size: 16px;
                color: #666;
            }
            #stat-value {
                font-size: 24px;
                color: #1a237e;
                font-weight: bold;
            }
        """)
        
        # Initial stats update
        self.update_stats()
        
    def update_stats(self):
        """Update dashboard statistics"""
        db = SessionLocal()
        try:
            # Get total members
            total_members = db.query(Member).count()
            self.total_members.findChild(QLabel, "stat-value").setText(str(total_members))
            
            # Get active members
            now = datetime.utcnow()
            active_members = db.query(Member).filter(
                Member.is_active == True,
                Member.end_date >= now
            ).count()
            self.active_members.findChild(QLabel, "stat-value").setText(str(active_members))
            
            # Get today's attendance
            today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            today_attendance = db.query(AttendanceRecord).filter(
                AttendanceRecord.check_in >= today_start
            ).count()
            self.today_attendance.findChild(QLabel, "stat-value").setText(str(today_attendance))
            
            # Get subscriptions expiring in next 7 days
            week_later = now + timedelta(days=7)
            expiring_soon = db.query(Member).filter(
                Member.is_active == True,
                Member.end_date.between(now, week_later)
            ).count()
            self.expiring_soon.findChild(QLabel, "stat-value").setText(str(expiring_soon))
            
        finally:
            db.close()
