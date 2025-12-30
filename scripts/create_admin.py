#python scripts/create_admin.py

from app.db.session import SessionLocal
from app.db.models.user import User
from app.core.security import bcrypt_context
from app.core.enums import UserRole


db = SessionLocal()

try:
    existing_admin = db.query(User).filter(User.username == "admin").first()
    if existing_admin:
        print("Admin already exists")
    else:
        admin = User(
            username="admin",
            email="admin@yourapp.com",
            first_name="Admin",
            last_name="User",
            hashed_password=bcrypt_context.hash("myadminpassword123"),
            role=UserRole.ADMIN,
            is_active=True
        )
        db.add(admin)
        db.commit()
        print("Admin created")
finally:
    db.close()
