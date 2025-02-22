from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QPushButton, QLabel, QStackedWidget)
from PyQt6.QtCore import Qt
from .login import LoginWidget
from .dashboard import DashboardWidget
from .members import MembersWidget
from .attendance import AttendanceWidget
from .subscriptions import SubscriptionsWidget
from .reports import ReportsWidget
from .settings import SettingsWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # Set window properties
        self.setMinimumSize(1200, 800)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)
        
        # Create sidebar
        sidebar = self.create_sidebar()
        layout.addWidget(sidebar)
        
        # Create stacked widget for main content
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)
        
        # Set layout ratio between sidebar and main content
        layout.setStretch(0, 1)  # Sidebar takes 1 part
        layout.setStretch(1, 4)  # Main content takes 4 parts
        
        # Initialize widgets
        self.init_widgets()
        
        # Show login screen first
        self.show_login()
        
    def create_sidebar(self):
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar_layout = QVBoxLayout(sidebar)
        
        # Add buttons
        self.dashboard_btn = self.create_nav_button("لوحة التحكم")
        self.members_btn = self.create_nav_button("الأعضاء")
        self.attendance_btn = self.create_nav_button("الحضور")
        self.subscriptions_btn = self.create_nav_button("الاشتراكات")
        self.reports_btn = self.create_nav_button("التقارير")
        self.settings_btn = self.create_nav_button("الإعدادات")
        
        # Add buttons to layout
        sidebar_layout.addWidget(self.dashboard_btn)
        sidebar_layout.addWidget(self.members_btn)
        sidebar_layout.addWidget(self.attendance_btn)
        sidebar_layout.addWidget(self.subscriptions_btn)
        sidebar_layout.addWidget(self.reports_btn)
        sidebar_layout.addStretch()
        sidebar_layout.addWidget(self.settings_btn)
        
        # Connect buttons
        self.dashboard_btn.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.dashboard))
        self.members_btn.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.members))
        self.attendance_btn.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.attendance))
        self.subscriptions_btn.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.subscriptions))
        self.reports_btn.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.reports))
        self.settings_btn.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.settings))
        
        return sidebar
    
    def create_nav_button(self, text):
        button = QPushButton(text)
        button.setObjectName("nav-button")
        button.setCheckable(True)
        return button
    
    def init_widgets(self):
        # Create all main widgets
        self.login = LoginWidget(self)
        self.dashboard = DashboardWidget()
        self.members = MembersWidget()
        self.attendance = AttendanceWidget()
        self.subscriptions = SubscriptionsWidget()
        self.reports = ReportsWidget()
        self.settings = SettingsWidget()
        
        # Add widgets to stacked widget
        self.stacked_widget.addWidget(self.login)
        self.stacked_widget.addWidget(self.dashboard)
        self.stacked_widget.addWidget(self.members)
        self.stacked_widget.addWidget(self.attendance)
        self.stacked_widget.addWidget(self.subscriptions)
        self.stacked_widget.addWidget(self.reports)
        self.stacked_widget.addWidget(self.settings)
    
    def show_login(self):
        """Show login screen and hide sidebar"""
        self.stacked_widget.setCurrentWidget(self.login)
        self.dashboard_btn.setVisible(False)
        self.members_btn.setVisible(False)
        self.attendance_btn.setVisible(False)
        self.subscriptions_btn.setVisible(False)
        self.reports_btn.setVisible(False)
        self.settings_btn.setVisible(False)
    
    def show_dashboard(self):
        """Show dashboard and sidebar after successful login"""
        self.stacked_widget.setCurrentWidget(self.dashboard)
        self.dashboard_btn.setVisible(True)
        self.members_btn.setVisible(True)
        self.attendance_btn.setVisible(True)
        self.subscriptions_btn.setVisible(True)
        self.reports_btn.setVisible(True)
        self.settings_btn.setVisible(True)
        
    def apply_stylesheet(self):
        """Apply custom styling to the application"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f2f5;
            }
            #sidebar {
                background-color: #1a237e;
                min-width: 200px;
                max-width: 200px;
                padding: 20px;
            }
            #nav-button {
                background-color: transparent;
                border: none;
                color: white;
                text-align: right;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            #nav-button:hover {
                background-color: #283593;
            }
            #nav-button:checked {
                background-color: #3949ab;
            }
        """)
