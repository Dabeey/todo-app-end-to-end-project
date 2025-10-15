#!/usr/bin/env python3
"""
Comprehensive fix script for all authentication issues
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def fix_import_issues():
    """Fix any import issues"""
    print("🔧 Fixing import issues...")
    
    # Check if all required modules are available
    try:
        from src.database.core import SessionLocal, engine, Base
        from src.entities.user import User
        from src.auth.service import get_password_hash, verify_password
        from src.auth.schemas import LoginRequest, Token
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_database_schema():
    """Test database schema consistency"""
    print("🔧 Testing database schema...")
    
    try:
        from src.database.core import SessionLocal, engine, Base
        from src.entities.user import User
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        
        # Test that the User model has the correct field
        user_fields = [column.name for column in User.__table__.columns]
        if 'password_hash' in user_fields:
            print("✅ User model has correct password_hash field")
        else:
            print("❌ User model missing password_hash field")
            return False
            
        return True
    except Exception as e:
        print(f"❌ Database schema test failed: {e}")
        return False

def test_user_operations():
    """Test user creation and authentication"""
    print("🔧 Testing user operations...")
    
    try:
        from src.database.core import SessionLocal
        from src.entities.user import User
        from src.auth.service import get_password_hash, verify_password, authenticate_user
        from uuid import uuid4
        
        db = SessionLocal()
        
        # Create test user
        test_user = User(
            id=uuid4(),
            email="test@example.com",
            first_name="Test",
            last_name="User",
            password_hash=get_password_hash("testpassword123")
        )
        
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        print("✅ User creation successful")
        
        # Test authentication
        auth_result = authenticate_user("test@example.com", "testpassword123", db)
        if auth_result:
            print("✅ User authentication successful")
        else:
            print("❌ User authentication failed")
            return False
        
        # Test wrong password
        auth_result = authenticate_user("test@example.com", "wrongpassword", db)
        if not auth_result:
            print("✅ Wrong password correctly rejected")
        else:
            print("❌ Wrong password incorrectly accepted")
            return False
        
        # Clean up
        db.delete(test_user)
        db.commit()
        db.close()
        print("✅ User deletion successful")
        
        return True
    except Exception as e:
        print(f"❌ User operations test failed: {e}")
        return False

def test_jwt_operations():
    """Test JWT token creation and verification"""
    print("🔧 Testing JWT operations...")
    
    try:
        from src.auth.service import create_access_token, verify_token
        from datetime import timedelta
        from uuid import uuid4
        
        # Test token creation
        user_id = uuid4()
        token = create_access_token("test@example.com", user_id, timedelta(minutes=30))
        print("✅ JWT token creation successful")
        
        # Test token verification
        token_data = verify_token(token)
        if token_data.user_id == str(user_id):
            print("✅ JWT token verification successful")
        else:
            print("❌ JWT token verification failed")
            return False
        
        return True
    except Exception as e:
        print(f"❌ JWT operations test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Running comprehensive authentication system tests")
    print("=" * 60)
    
    tests = [
        ("Import Issues", fix_import_issues),
        ("Database Schema", test_database_schema),
        ("User Operations", test_user_operations),
        ("JWT Operations", test_jwt_operations)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 Testing {test_name}...")
        result = test_func()
        results.append((test_name, result))
    
    print("\n📊 Test Results Summary")
    print("=" * 30)
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All tests passed! Authentication system is ready.")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
    
    return all_passed

if __name__ == "__main__":
    main()
