from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QLabel, QLineEdit, QFormLayout, QMessageBox)
from PyQt6.QtCore import Qt
from src.models.database import SessionLocal
from src.models.user import User
from src.models.member import Member
from src.models.attendance import AttendanceRecord
from src.models.subscription import Subscription

class SettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Create header
        header_layout = QHBoxLayout()
        title = QLabel("الإعدادات")
        title.setObjectName("page-title")
        header_layout.addWidget(title)
        
        layout.addLayout(header_layout)
        
        # Create form
        form = QFormLayout()
        
        # Database settings
        self.db_host = QLineEdit()
        self.db_host.setPlaceholderText("localhost")
        form.addRow("مضيف قاعدة البيانات:", self.db_host)
        
        self.db_port = QLineEdit()
        self.db_port.setPlaceholderText("3306")
        form.addRow("منفذ قاعدة البيانات:", self.db_port)
        
        self.db_name = QLineEdit()
        self.db_name.setPlaceholderText("gym_db")
        form.addRow("اسم قاعدة البيانات:", self.db_name)
        
        self.db_user = QLineEdit()
        self.db_user.setPlaceholderText("root")
        form.addRow("مستخدم قاعدة البيانات:", self.db_user)
        
        self.db_password = QLineEdit()
        self.db_password.setPlaceholderText("كلمة المرور")
        self.db_password.setEchoMode(QLineEdit.EchoMode.Password)
        form.addRow("كلمة مرور قاعدة البيانات:", self.db_password)
        
        # Save button
        save_button = QPushButton("حفظ")
        save_button.setObjectName("primary-button")
        save_button.clicked.connect(self.save_settings)
        
        layout.addLayout(form)
        layout.addWidget(save_button)
        
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
        """)
        
        # Load initial settings
        self.load_settings()
        
    def load_settings(self):
        """Load current settings from .env file"""
        try:
            with open(".env", "r") as f:
                for line in f:
                    if line.startswith("DB_HOST"):
                        self.db_host.setText(line.split("=")[1].strip())
                    elif line.startswith("DB_PORT"):
                        self.db_port.setText(line.split("=")[1].strip())
                    elif line.startswith("DB_NAME"):
                        self.db_name.setText(line.split("=")[1].strip())
                    elif line.startswith("DB_USER"):
                        self.db_user.setText(line.split("=")[1].strip())
                    elif line.startswith("DB_PASSWORD"):
                        self.db_password.setText(line.split("=")[1].strip())
        except FileNotFoundError:
            pass
        
    def save_settings(self):
        """Save settings to .env file"""
        try:
            with open(".env", "w") as f:
                f.write(f"DB_HOST={self.db_host.text()}\n")
                f.write(f"DB_PORT={self.db_port.text()}\n")
                f.write(f"DB_NAME={self.db_name.text()}\n")
                f.write(f"DB_USER={self.db_user.text()}\n")
                f.write(f"DB_PASSWORD={self.db_password.text()}\n")
                
            QMessageBox.information(self, "نجاح", "تم حفظ الإعدادات بنجاح")
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء حفظ الإعدادات: {str(e)}")
