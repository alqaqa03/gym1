from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QLabel, QTableWidget, QTableWidgetItem, QComboBox,
                               QMessageBox, QDialog, QFormLayout, QLineEdit,
                               QDateEdit)
from PyQt6.QtCore import Qt, QDate
from src.models.database import SessionLocal
from src.models.member import Member, MembershipType
from src.models.subscription import Subscription
from datetime import datetime

class AddSubscriptionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("إضافة اشتراك جديد")
        self.setMinimumWidth(400)
        
        layout = QFormLayout()
        
        # Create form fields
        self.member_combo = QComboBox()
        self.load_members()
        
        self.type_combo = QComboBox()
        for type_name in MembershipType:
            self.type_combo.addItem(type_name.value)
            
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("0.00")
        
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate())
        
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate().addMonths(1))
        
        self.notes_input = QLineEdit()
        
        # Add fields to layout
        layout.addRow("العضو:", self.member_combo)
        layout.addRow("نوع الاشتراك:", self.type_combo)
        layout.addRow("المبلغ:", self.amount_input)
        layout.addRow("تاريخ البدء:", self.start_date)
        layout.addRow("تاريخ الانتهاء:", self.end_date)
        layout.addRow("ملاحظات:", self.notes_input)
        
        # Add buttons
        button_box = QHBoxLayout()
        save_button = QPushButton("حفظ")
        save_button.clicked.connect(self.accept)
        cancel_button = QPushButton("إلغاء")
        cancel_button.clicked.connect(self.reject)
        
        button_box.addWidget(save_button)
        button_box.addWidget(cancel_button)
        layout.addRow(button_box)
        
        self.setLayout(layout)
        
    def load_members(self):
        """Load members into combo box"""
        db = SessionLocal()
        try:
            members = db.query(Member).filter(Member.is_active == True).all()
            for member in members:
                self.member_combo.addItem(member.full_name, member.id)
        finally:
            db.close()

class SubscriptionsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Create header
        header_layout = QHBoxLayout()
        title = QLabel("إدارة الاشتراكات")
        title.setObjectName("page-title")
        header_layout.addWidget(title)
        
        # Add subscription button
        add_button = QPushButton("إضافة اشتراك")
        add_button.setObjectName("primary-button")
        add_button.clicked.connect(self.show_add_subscription_dialog)
        header_layout.addWidget(add_button)
        
        # Add filter
        self.status_filter = QComboBox()
        self.status_filter.addItems(["الكل", "نشط", "منتهي"])
        self.status_filter.currentTextChanged.connect(self.load_subscriptions)
        header_layout.addWidget(self.status_filter)
        
        layout.addLayout(header_layout)
        
        # Create table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "العضو", "نوع الاشتراك", "المبلغ", "تاريخ البدء",
            "تاريخ الانتهاء", "الأيام المتبقية", "الحالة"
        ])
        self.table.setColumnWidth(0, 200)  # Member
        self.table.setColumnWidth(1, 120)  # Type
        self.table.setColumnWidth(2, 100)  # Amount
        self.table.setColumnWidth(3, 120)  # Start Date
        self.table.setColumnWidth(4, 120)  # End Date
        self.table.setColumnWidth(5, 120)  # Days Remaining
        self.table.setColumnWidth(6, 100)  # Status
        
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
            #primary-button {
                background-color: #1a237e;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
            }
            #primary-button:hover {
                background-color: #283593;
            }
            QComboBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                margin: 5px;
            }
        """)
        
        # Load initial data
        self.load_subscriptions()
        
    def load_subscriptions(self):
        """Load subscriptions into table"""
        db = SessionLocal()
        try:
            query = db.query(Subscription).join(Member)
            
            # Apply filter
            if self.status_filter.currentText() == "نشط":
                query = query.filter(Subscription.end_date >= datetime.utcnow())
            elif self.status_filter.currentText() == "منتهي":
                query = query.filter(Subscription.end_date < datetime.utcnow())
                
            subscriptions = query.order_by(Subscription.start_date.desc()).all()
            self.table.setRowCount(len(subscriptions))
            
            for i, subscription in enumerate(subscriptions):
                self.table.setItem(i, 0, QTableWidgetItem(subscription.member.full_name))
                self.table.setItem(i, 1, QTableWidgetItem(subscription.type.value))
                self.table.setItem(i, 2, QTableWidgetItem(f"{subscription.amount:.2f}"))
                self.table.setItem(i, 3, QTableWidgetItem(subscription.start_date.strftime("%Y-%m-%d")))
                self.table.setItem(i, 4, QTableWidgetItem(subscription.end_date.strftime("%Y-%m-%d")))
                
                days_remaining = subscription.days_remaining
                days_item = QTableWidgetItem(str(days_remaining))
                if days_remaining <= 0:
                    days_item.setForeground(Qt.GlobalColor.red)
                elif days_remaining <= 7:
                    days_item.setForeground(Qt.GlobalColor.darkYellow)
                self.table.setItem(i, 5, days_item)
                
                status = "نشط" if subscription.is_active else "منتهي"
                status_item = QTableWidgetItem(status)
                status_item.setForeground(
                    Qt.GlobalColor.green if subscription.is_active else Qt.GlobalColor.red
                )
                self.table.setItem(i, 6, status_item)
                
        finally:
            db.close()
            
    def show_add_subscription_dialog(self):
        """Show dialog for adding new subscription"""
        dialog = AddSubscriptionDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            member_id = dialog.member_combo.currentData()
            
            subscription = Subscription(
                member_id=member_id,
                type=MembershipType(dialog.type_combo.currentText()),
                start_date=dialog.start_date.date().toPyDate(),
                end_date=dialog.end_date.date().toPyDate(),
                amount=float(dialog.amount_input.text() or 0),
                payment_status="paid",  # Default to paid for now
                notes=dialog.notes_input.text()
            )
            
            db = SessionLocal()
            try:
                db.add(subscription)
                
                # Update member dates
                member = db.query(Member).get(member_id)
                if member:
                    member.start_date = subscription.start_date
                    member.end_date = subscription.end_date
                    
                db.commit()
                QMessageBox.information(self, "نجاح", "تم إضافة الاشتراك بنجاح")
                self.load_subscriptions()
            except Exception as e:
                db.rollback()
                QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء إضافة الاشتراك: {str(e)}")
            finally:
                db.close()
