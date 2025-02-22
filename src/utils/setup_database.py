from src.models.database import engine, SessionLocal, Base
from src.models.user import User, UserRole
from datetime import datetime

def init_database():
    """Initialize database tables and create default admin user"""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    db = SessionLocal()
    
    try:
        # Check if admin user exists
        admin = db.query(User).filter(User.username == "admin").first()
        
        if not admin:
            # Create default admin user
            admin = User(
                username="admin",
                email="admin@gym.local",
                full_name="مدير النظام",
                role=UserRole.ADMIN,
                is_active=True,
                created_at=datetime.utcnow()
            )
            admin.set_password("admin123")  # Set default password
            
            db.add(admin)
            db.commit()
            print("تم إنشاء حساب المدير بنجاح")
            print("اسم المستخدم: admin")
            print("كلمة المرور: admin123")
            print("يرجى تغيير كلمة المرور بعد تسجيل الدخول لأول مرة")
        else:
            print("حساب المدير موجود مسبقاً")
            
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
