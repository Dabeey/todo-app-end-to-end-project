#!/usr/bin/env python3
"""
Comprehensive test to ensure perfect code with no errors
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test all imports work correctly"""
    print("🔧 Testing imports...")
    try:
        from src.database.core import SessionLocal, engine, Base
        from src.entities.user import User
        from src.auth.service import get_password_hash, verify_password, authenticate_user, create_access_token, verify_token
        from src.auth.schemas import LoginRequest, Token, RegisterUserRequest
        from src.auth.controller import router as auth_router
        from src.users.controller import router as users_router
        from src.todos.controller import router as todos_router
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_bcrypt_compatibility():
    """Test bcrypt compatibility and password hashing"""
    print("🔧 Testing bcrypt compatibility...")
    try:
        from src.auth.service import get_password_hash, verify_password
        
        # Test short password
        short_password = "test123"
        hashed_short = get_password_hash(short_password)
        if verify_password(short_password, hashed_short):
            print("✅ Short password hashing/verification works")
        else:
            print("❌ Short password verification failed")
            return False
        
        # Test long password (over 72 bytes)
        long_password = "a" * 100  # 100 character password
        hashed_long = get_password_hash(long_password)
        if verify_password(long_password, hashed_long):
            print("✅ Long password hashing/verification works")
        else:
            print("❌ Long password verification failed")
            return False
        
        # Test wrong password
        if not verify_password("wrongpassword", hashed_short):
            print("✅ Wrong password correctly rejected")
        else:
            print("❌ Wrong password incorrectly accepted")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Bcrypt compatibility test failed: {e}")
        return False

def test_database_operations():
    """Test database operations"""
    print("🔧 Testing database operations...")
    try:
        from src.database.core import SessionLocal, engine, Base
        from src.entities.user import User
        from src.auth.service import get_password_hash, verify_password, authenticate_user
        from uuid import uuid4
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        
        db = SessionLocal()
        
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
        db.refresh(test_user)
        print("✅ User creation successful")
        
        # Test user query
        found_user = db.query(User).filter(User.email == "test@example.com").first()
        if found_user:
            print("✅ User query successful")
        else:
            print("❌ User query failed")
            return False
        
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
        db.delete(found_user)
        db.commit()
        db.close()
        print("✅ Database cleanup successful")
        
        return True
    except Exception as e:
        print(f"❌ Database operations test failed: {e}")
        return False

def test_jwt_operations():
    """Test JWT token operations"""
    print("🔧 Testing JWT operations...")
    try:
        from src.auth.service import create_access_token, verify_token
        from datetime import timedelta
        from uuid import uuid4
        
        # Test token creation
        user_id = uuid4()
        token = create_access_token("test@example.com", user_id, timedelta(minutes=30))
        if token:
            print("✅ JWT token creation successful")
        else:
            print("❌ JWT token creation failed")
            return False
        
        # Test token verification
        token_data = verify_token(token)
        if token_data and token_data.user_id == str(user_id):
            print("✅ JWT token verification successful")
        else:
            print("❌ JWT token verification failed")
            return False
        
        return True
    except Exception as e:
        print(f"❌ JWT operations test failed: {e}")
        return False

def test_demo_user_creation():
    """Test demo user creation"""
    print("🔧 Testing demo user creation...")
    try:
        from src.database.core import SessionLocal, engine, Base
        from src.entities.user import User
        from src.auth.service import get_password_hash
        from uuid import uuid4
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        
        db = SessionLocal()
        
        # Check if demo user exists
        existing_user = db.query(User).filter(User.email == "demo@example.com").first()
        if existing_user:
            db.delete(existing_user)
            db.commit()
            print("✅ Existing demo user removed")
        
        # Create demo user
        demo_user = User(
            id=uuid4(),
            email="demo@example.com",
            first_name="Demo",
            last_name="User",
            password_hash=get_password_hash("demopassword123")
        )
        
        db.add(demo_user)
        db.commit()
        db.refresh(demo_user)
        print("✅ Demo user creation successful")
        
        # Verify demo user
        found_user = db.query(User).filter(User.email == "demo@example.com").first()
        if found_user:
            print("✅ Demo user verification successful")
        else:
            print("❌ Demo user verification failed")
            return False
        
        db.close()
        return True
    except Exception as e:
        print(f"❌ Demo user creation test failed: {e}")
        return False

def test_authentication_flow():
    """Test complete authentication flow"""
    print("🔧 Testing complete authentication flow...")
    try:
        from src.database.core import SessionLocal
        from src.entities.user import User
        from src.auth.service import authenticate_user, create_access_token, verify_token
        from datetime import timedelta
        
        db = SessionLocal()
        
        # Test authentication
        user = authenticate_user("demo@example.com", "demopassword123", db)
        if not user:
            print("❌ Demo user authentication failed")
            return False
        
        # Test token creation
        token = create_access_token(user.email, user.id, timedelta(minutes=30))
        if not token:
            print("❌ Token creation failed")
            return False
        
        # Test token verification
        token_data = verify_token(token)
        if not token_data or token_data.user_id != str(user.id):
            print("❌ Token verification failed")
            return False
        
        db.close()
        print("✅ Complete authentication flow successful")
        return True
    except Exception as e:
        print(f"❌ Authentication flow test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Running comprehensive perfect code tests")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Bcrypt Compatibility", test_bcrypt_compatibility),
        ("Database Operations", test_database_operations),
        ("JWT Operations", test_jwt_operations),
        ("Demo User Creation", test_demo_user_creation),
        ("Authentication Flow", test_authentication_flow)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 Testing {test_name}...")
        result = test_func()
        results.append((test_name, result))
        if not result:
            print(f"❌ {test_name} failed - stopping tests")
            break
    
    print("\n📊 Test Results Summary")
    print("=" * 30)
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED! Code is perfect and ready!")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
    
    return all_passed

if __name__ == "__main__":
    main()
