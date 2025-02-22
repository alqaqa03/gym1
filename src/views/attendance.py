from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QLabel, QTableWidget, QTableWidgetItem, QComboBox,
                               QMessageBox)
from PyQt6.QtCore import Qt, QTimer
from src.models.database import SessionLocal
from src.models.member import Member
from src.models.attendance import AttendanceRecord
from datetime import datetime, timedelta

class AttendanceWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Create header
        header_layout = QHBoxLayout()
        title = QLabel("سجل الحضور")
        title.setObjectName("page-title")
        header_layout.addWidget(title)
        
        # Add check-in/out buttons
        self.check_in_button = QPushButton("تسجيل دخول")
        self.check_in_button.setObjectName("success-button")
        self.check_in_button.clicked.connect(self.handle_check_in)
        
        self.check_out_button = QPushButton("تسجيل خروج")
        self.check_out_button.setObjectName("warning-button")
        self.check_out_button.clicked.connect(self.handle_check_out)
        
        header_layout.addWidget(self.check_in_button)
        header_layout.addWidget(self.check_out_button)
        
        # Add date filter
        self.date_filter = QComboBox()
        self.date_filter.addItems(["اليوم", "الأسبوع", "الشهر"])
        self.date_filter.currentTextChanged.connect(self.load_attendance)
        header_layout.addWidget(self.date_filter)
        
        layout.addLayout(header_layout)
        
        # Create table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "الاسم", "وقت الدخول", "وقت الخروج", "المدة", "تم التحقق"
        ])
        self.table.setColumnWidth(0, 200)  # Name
        self.table.setColumnWidth(1, 150)  # Check-in
        self.table.setColumnWidth(2, 150)  # Check-out
        self.table.setColumnWidth(3, 100)  # Duration
        self.table.setColumnWidth(4, 100)  # Verified
        
        layout.addWidget(self.table)
        
        # Set main layout
        self.setLayout(layout)
        
        # Apply styles
        self.setStyleSheet("""
            #page-title {
                font-size: 24px;
                color: #1a237e;
                margin: 20px;
            }
            #success-button {
                background-color: #4caf50;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
            }
            #warning-button {
                background-color: #ff9800;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
            }
            QComboBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                margin: 5px;
            }
        """)
        
        # Load initial data
        self.load_attendance()
        
        # Update table every minute
        self.timer = QTimer()
        self.timer.timeout.connect(self.load_attendance)
        self.timer.start(60000)  # 1 minute
        
    def load_attendance(self):
        """Load attendance records based on selected date filter"""
        db = SessionLocal()
        try:
            now = datetime.utcnow()
            
            # Calculate date range
            if self.date_filter.currentText() == "اليوم":
                start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            elif self.date_filter.currentText() == "الأسبوع":
                start_date = now - timedelta(days=7)
            else:  # Month
                start_date = now - timedelta(days=30)
                
            # Get records
            records = db.query(AttendanceRecord).join(Member).filter(
                AttendanceRecord.check_in >= start_date
            ).order_by(AttendanceRecord.check_in.desc()).all()
            
            self.table.setRowCount(len(records))
            
            for i, record in enumerate(records):
                self.table.setItem(i, 0, QTableWidgetItem(record.member.full_name))
                self.table.setItem(i, 1, QTableWidgetItem(record.check_in.strftime("%Y-%m-%d %H:%M")))
                
                if record.check_out:
                    self.table.setItem(i, 2, QTableWidgetItem(record.check_out.strftime("%Y-%m-%d %H:%M")))
                    duration = record.duration
                    if duration:
                        hours = duration.total_seconds() / 3600
                        self.table.setItem(i, 3, QTableWidgetItem(f"{hours:.1f} ساعة"))
                else:
                    self.table.setItem(i, 2, QTableWidgetItem("-"))
                    self.table.setItem(i, 3, QTableWidgetItem("-"))
                    
                verified = "✓" if record.fingerprint_verified else "✗"
                verified_item = QTableWidgetItem(verified)
                verified_item.setForeground(
                    Qt.GlobalColor.green if record.fingerprint_verified else Qt.GlobalColor.red
                )
                self.table.setItem(i, 4, verified_item)
                
        finally:
            db.close()
            
    def handle_check_in(self):
        """Handle member check-in"""
        # TODO: Implement manual member selection for testing
        QMessageBox.information(self, "تنبيه", "سيتم إضافة خيار اختيار العضو في التحديث القادم")
            
    def handle_check_out(self):
        """Handle member check-out"""
        # TODO: Implement manual member selection for testing
        QMessageBox.information(self, "تنبيه", "سيتم إضافة خيار اختيار العضو في التحديث القادم")
