import os
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'gym_db')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')

# Security Configuration
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
BCRYPT_ROUNDS = 12

# Fingerprint Device Configuration
FINGERPRINT_PORT = os.getenv('FINGERPRINT_PORT', '/dev/ttyUSB0')
FINGERPRINT_BAUDRATE = int(os.getenv('FINGERPRINT_BAUDRATE', '57600'))

# Backup Configuration
BACKUP_DIR = os.getenv('BACKUP_DIR', 'backups')
BACKUP_RETENTION_DAYS = int(os.getenv('BACKUP_RETENTION_DAYS', '30'))

# Application Configuration
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
APP_NAME = "نظام إدارة الصالة الرياضية"
VERSION = "1.0.0"
