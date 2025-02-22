from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QLabel, QTableWidget, QTableWidgetItem, QComboBox,
                               QMessageBox, QDialog, QFormLayout, QLineEdit,
                               QDateEdit)
from PyQt6.QtCore import Qt, QDate
from src.models.database import SessionLocal
from src.models.member import Member
from src.models.attendance import AttendanceRecord
from src.models.subscription import Subscription
from datetime import datetime, timedelta
import pandas as pd

class ReportsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Create header
        header_layout = QHBoxLayout()
        title = QLabel("التقارير")
        title.setObjectName("page-title")
        header_layout.addWidget(title)
        
        # Report type selector
        self.report_type = QComboBox()
        self.report_type.addItems(["الحضور", "الاشتراكات", "الإيرادات"])
        self.report_type.currentTextChanged.connect(self.load_report)
        header_layout.addWidget(self.report_type)
        
        # Date range selector
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addMonths(-1))
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        
        header_layout.addWidget(QLabel("من:"))
        header_layout.addWidget(self.start_date)
        header_layout.addWidget(QLabel("إلى:"))
        header_layout.addWidget(self.end_date)
        
        # Refresh button
        refresh_button = QPushButton("تحديث")
        refresh_button.clicked.connect(self.load_report)
        header_layout.addWidget(refresh_button)
        
        layout.addLayout(header_layout)
        
        # Create table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "التاريخ", "العضو", "نوع التقرير", "القيمة", "ملاحظات"
        ])
        self.table.setColumnWidth(0, 120)  # Date
        self.table.setColumnWidth(1, 200)  # Member
        self.table.setColumnWidth(2, 120)  # Report Type
        self.table.setColumnWidth(3, 100)  # Value
        self.table.setColumnWidth(4, 200)  # Notes
        
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
            QComboBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                margin: 5px;
            }
        """)
        
        # Load initial data
        self.load_report()
        
    def load_report(self):
        """Load report data based on selected type and date range"""
        report_type = self.report_type.currentText()
        start_date = self.start_date.date().toPyDate()
        end_date = self.end_date.date().toPyDate()
        
        db = SessionLocal()
        try:
            if report_type == "الحضور":
                self.load_attendance_report(db, start_date, end_date)
            elif report_type == "الاشتراكات":
                self.load_subscriptions_report(db, start_date, end_date)
            elif report_type == "الإيرادات":
                self.load_revenue_report(db, start_date, end_date)
        finally:
            db.close()
            
    def load_attendance_report(self, db, start_date, end_date):
        """Load attendance report"""
        records = db.query(AttendanceRecord).filter(
            AttendanceRecord.check_in >= start_date,
            AttendanceRecord.check_in <= end_date
        ).all()
        
        self.table.setRowCount(len(records))
        for i, record in enumerate(records):
            self.table.setItem(i, 0, QTableWidgetItem(record.check_in.strftime("%Y-%m-%d %H:%M")))
            self.table.setItem(i, 1, QTableWidgetItem(record.member.full_name))
            self.table.setItem(i, 2, QTableWidgetItem("الحضور"))
            self.table.setItem(i, 3, QTableWidgetItem("1"))
            self.table.setItem(i, 4, QTableWidgetItem(record.notes or ""))
            
    def load_subscriptions_report(self, db, start_date, end_date):
        """Load subscriptions report"""
        subscriptions = db.query(Subscription).filter(
            Subscription.start_date >= start_date,
            Subscription.start_date <= end_date
        ).all()
        
        self.table.setRowCount(len(subscriptions))
        for i, subscription in enumerate(subscriptions):
            self.table.setItem(i, 0, QTableWidgetItem(subscription.start_date.strftime("%Y-%m-%d")))
            self.table.setItem(i, 1, QTableWidgetItem(subscription.member.full_name))
            self.table.setItem(i, 2, QTableWidgetItem("الاشتراكات"))
            self.table.setItem(i, 3, QTableWidgetItem(f"{subscription.amount:.2f}"))
            self.table.setItem(i, 4, QTableWidgetItem(subscription.notes or ""))
            
    def load_revenue_report(self, db, start_date, end_date):
        """Load revenue report"""
        subscriptions = db.query(Subscription).filter(
            Subscription.start_date >= start_date,
            Subscription.start_date <= end_date
        ).all()
        
        df = pd.DataFrame([{
            "date": sub.start_date,
            "amount": sub.amount
        } for sub in subscriptions])
        
        if not df.empty:
            df = df.groupby(pd.Grouper(key="date", freq="D")).sum().reset_index()
            
        self.table.setRowCount(len(df))
        for i, row in df.iterrows():
            self.table.setItem(i, 0, QTableWidgetItem(row["date"].strftime("%Y-%m-%d")))
            self.table.setItem(i, 1, QTableWidgetItem(""))
            self.table.setItem(i, 2, QTableWidgetItem("الإيرادات"))
            self.table.setItem(i, 3, QTableWidgetItem(f"{row['amount']:.2f}"))
            self.table.setItem(i, 4, QTableWidgetItem(""))
