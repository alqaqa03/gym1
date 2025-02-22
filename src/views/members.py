from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
                               QComboBox, QMessageBox, QDialog, QFormLayout,
                               QDateEdit, QTextEdit)
from PyQt6.QtCore import Qt, QDate
from src.models.database import SessionLocal
from src.models.member import Member, MembershipType
from src.models.user import User
from datetime import datetime, timedelta
import bcrypt

class AddMemberDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("إضافة عضو جديد")
        self.setMinimumWidth(400)
        
        layout = QFormLayout()
        
        # Create form fields
        self.name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()
        self.emergency_contact_input = QLineEdit()
        self.medical_conditions_input = QTextEdit()
        
        self.membership_type_combo = QComboBox()
        for type_name in MembershipType:
            self.membership_type_combo.addItem(type_name.value)
            
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate())
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate().addMonths(1))
        
        # Add fields to layout
        layout.addRow("الاسم الكامل:", self.name_input)
        layout.addRow("رقم الهاتف:", self.phone_input)
        layout.addRow("البريد الإلكتروني:", self.email_input)
        layout.addRow("رقم للطوارئ:", self.emergency_contact_input)
        layout.addRow("الحالة الصحية:", self.medical_conditions_input)
        layout.addRow("نوع العضوية:", self.membership_type_combo)
        layout.addRow("تاريخ البدء:", self.start_date)
        layout.addRow("تاريخ الانتهاء:", self.end_date)
        
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

class MembersWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Create header
        header_layout = QHBoxLayout()
        title = QLabel("إدارة الأعضاء")
        title.setObjectName("page-title")
        header_layout.addWidget(title)
        
        # Add member button
        add_button = QPushButton("إضافة عضو")
        add_button.setObjectName("primary-button")
        add_button.clicked.connect(self.show_add_member_dialog)
        header_layout.addWidget(add_button)
        
        # Add search box
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("بحث عن عضو...")
        self.search_input.textChanged.connect(self.filter_members)
        header_layout.addWidget(self.search_input)
        
        layout.addLayout(header_layout)
        
        # Create table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "الاسم", "رقم الهاتف", "البريد الإلكتروني",
            "نوع العضوية", "تاريخ البدء", "تاريخ الانتهاء", "الحالة"
        ])
        self.table.setColumnWidth(0, 200)  # Name
        self.table.setColumnWidth(1, 120)  # Phone
        self.table.setColumnWidth(2, 200)  # Email
        self.table.setColumnWidth(3, 120)  # Membership Type
        self.table.setColumnWidth(4, 120)  # Start Date
        self.table.setColumnWidth(5, 120)  # End Date
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
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                margin: 5px;
            }
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)
        
        # Load initial data
        self.load_members()
        
    def load_members(self):
        """Load members from database into table"""
        db = SessionLocal()
        try:
            members = db.query(Member).all()
            self.table.setRowCount(len(members))
            
            for i, member in enumerate(members):
                self.table.setItem(i, 0, QTableWidgetItem(member.full_name))
                self.table.setItem(i, 1, QTableWidgetItem(member.phone))
                self.table.setItem(i, 2, QTableWidgetItem(member.email or ""))
                self.table.setItem(i, 3, QTableWidgetItem(member.membership_type.value))
                self.table.setItem(i, 4, QTableWidgetItem(member.start_date.strftime("%Y-%m-%d")))
                self.table.setItem(i, 5, QTableWidgetItem(member.end_date.strftime("%Y-%m-%d")))
                
                status = "نشط" if member.is_membership_valid() else "منتهي"
                status_item = QTableWidgetItem(status)
                status_item.setForeground(Qt.GlobalColor.green if status == "نشط" else Qt.GlobalColor.red)
                self.table.setItem(i, 6, status_item)
                
        finally:
            db.close()
            
    def show_add_member_dialog(self):
        """Show dialog for adding new member"""
        dialog = AddMemberDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Create new member
            member = Member(
                full_name=dialog.name_input.text(),
                phone=dialog.phone_input.text(),
                email=dialog.email_input.text(),
                emergency_contact=dialog.emergency_contact_input.text(),
                medical_conditions=dialog.medical_conditions_input.toPlainText(),
                membership_type=MembershipType(dialog.membership_type_combo.currentText()),
                start_date=dialog.start_date.date().toPyDate(),
                end_date=dialog.end_date.date().toPyDate(),
                is_active=True,
                created_at=datetime.utcnow()
            )
            
            db = SessionLocal()
            try:
                db.add(member)
                db.commit()
                QMessageBox.information(self, "نجاح", "تم إضافة العضو بنجاح")
                self.load_members()
            except Exception as e:
                db.rollback()
                QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء إضافة العضو: {str(e)}")
            finally:
                db.close()
                
    def filter_members(self):
        """Filter members table based on search input"""
        search_text = self.search_input.text().lower()
        for row in range(self.table.rowCount()):
            show_row = False
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item and search_text in item.text().lower():
                    show_row = True
                    break
            self.table.setRowHidden(row, not show_row)
