from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                               QLineEdit, QPushButton, QMessageBox)
from PyQt6.QtCore import Qt
from sqlalchemy.orm import Session
from src.models.database import SessionLocal
from src.models.user import User

class LoginWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Create welcome label
        welcome_label = QLabel("مرحباً بكم في نظام إدارة الصالة الرياضية")
        welcome_label.setObjectName("welcome-label")
        layout.addWidget(welcome_label)
        
        # Create username input
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("اسم المستخدم")
        self.username_input.setObjectName("login-input")
        layout.addWidget(self.username_input)
        
        # Create password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("كلمة المرور")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setObjectName("login-input")
        layout.addWidget(self.password_input)
        
        # Create login button
        login_button = QPushButton("تسجيل الدخول")
        login_button.setObjectName("login-button")
        login_button.clicked.connect(self.handle_login)
        layout.addWidget(login_button)
        
        # Set layout
        self.setLayout(layout)
        
        # Apply styles
        self.setStyleSheet("""
            #welcome-label {
                font-size: 24px;
                color: #1a237e;
                margin-bottom: 20px;
            }
            #login-input {
                padding: 10px;
                margin: 5px;
                width: 250px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            #login-button {
                background-color: #1a237e;
                color: white;
                padding: 10px;
                width: 250px;
                border: none;
                border-radius: 4px;
                margin-top: 10px;
            }
            #login-button:hover {
                background-color: #283593;
            }
        """)
        
    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "خطأ", "الرجاء إدخال اسم المستخدم وكلمة المرور")
            return
        
        # Verify credentials
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.username == username).first()
            if user and user.check_password(password):
                if not user.is_active:
                    QMessageBox.warning(self, "خطأ", "هذا الحساب غير نشط")
                    return
                    
                # Update last login
                from datetime import datetime
                user.last_login = datetime.utcnow()
                db.commit()
                
                # Show main dashboard
                self.main_window.show_dashboard()
            else:
                QMessageBox.warning(self, "خطأ", "اسم المستخدم أو كلمة المرور غير صحيحة")
        finally:
            db.close()
            
    def clear_inputs(self):
        """Clear login inputs"""
        self.username_input.clear()
        self.password_input.clear()
