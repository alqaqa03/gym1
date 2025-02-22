import sys
from PyQt6.QtWidgets import QApplication
from src.views.main_window import MainWindow
from src.models.database import engine, Base
from src.utils.config import APP_NAME

def setup_database():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)

def main():
    # Initialize database
    setup_database()

    # Create Qt application
    app = QApplication(sys.argv)
    
    # Create and show main window
    window = MainWindow()
    window.setWindowTitle(APP_NAME)
    window.show()
    
    # Start application event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
