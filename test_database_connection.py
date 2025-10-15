#!/usr/bin/env python3
"""
Test database connection and basic operations
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.database.core import SessionLocal, engine, Base
from src.entities.user import User
from src.auth.service import get_password_hash
from uuid import uuid4

def test_database_connection():
    """Test database connection and basic operations"""
    print("🔧 Testing database connection...")
    
    try:
        # Test database connection
        db = SessionLocal()
        print("✅ Database connection successful")
        
        # Test table creation
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created/verified successfully")
        
        # Test user creation
        test_user = User(
            id=uuid4(),
            email="test@example.com",
            first_name="Test",
            last_name="User",
            password_hash=get_password_hash("testpassword123")
        )
        
        db.add(test_user)
        db.commit()
        print("✅ User creation successful")
        
        # Test user query
        found_user = db.query(User).filter(User.email == "test@example.com").first()
        if found_user:
            print("✅ User query successful")
            print(f"   Found user: {found_user.email}")
        else:
            print("❌ User query failed")
            return False
        
        # Test password verification
        from src.auth.service import verify_password
        if verify_password("testpassword123", found_user.password_hash):
            print("✅ Password verification successful")
        else:
            print("❌ Password verification failed")
            return False
        
        # Clean up test user
        db.delete(found_user)
        db.commit()
        print("✅ Test user cleaned up")
        
        db.close()
        print("🎉 All database operations successful!")
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

if __name__ == "__main__":
    test_database_connection()
