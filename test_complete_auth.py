#!/usr/bin/env python3
"""
Complete authentication flow test script
"""
import requests
import json
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

BASE_URL = "http://localhost:8000"

def test_demo_user_login():
    """Test login with demo user"""
    print("🧪 Testing Demo User Login")
    print("=" * 50)
    
    demo_login_data = {
        "email": "demo@example.com",
        "password": "demopassword123"
    }
    
    try:
        print("🔑 Logging in with demo user...")
        login_response = requests.post(f"{BASE_URL}/auth/login", json=demo_login_data)
        print(f"   Status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            print("   ✅ Demo user login successful")
            token_data = login_response.json()
            access_token = token_data.get('access_token')
            print(f"   Token type: {token_data.get('token_type')}")
            print(f"   Access token: {access_token[:50]}...")
            
            # Test protected endpoint
            print("\n🔒 Testing protected endpoint...")
            headers = {"Authorization": f"Bearer {access_token}"}
            me_response = requests.get(f"{BASE_URL}/users/me", headers=headers)
            print(f"   Status: {me_response.status_code}")
            
            if me_response.status_code == 200:
                print("   ✅ Protected endpoint accessible")
                user_info = me_response.json()
                print(f"   User info: {json.dumps(user_info, indent=2)}")
            else:
                print(f"   ❌ Protected endpoint failed: {me_response.text}")
                
        else:
            print(f"   ❌ Demo user login failed: {login_response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure the server is running on http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    return True

def test_new_user_flow():
    """Test complete flow with new user registration and login"""
    print("\n🧪 Testing New User Registration and Login")
    print("=" * 50)
    
    # Test data
    test_user = {
        "email": "newuser@example.com",
        "first_name": "New",
        "last_name": "User",
        "password": "newpassword123"
    }
    
    login_data = {
        "email": "newuser@example.com",
        "password": "newpassword123"
    }
    
    try:
        # Step 1: Register user
        print("1️⃣ Registering new user...")
        register_response = requests.post(f"{BASE_URL}/auth/", json=test_user)
        print(f"   Status: {register_response.status_code}")
        
        if register_response.status_code == 201:
            print("   ✅ User registered successfully")
            user_data = register_response.json()
            print(f"   User ID: {user_data.get('id')}")
            print(f"   Email: {user_data.get('email')}")
        else:
            print(f"   ❌ Registration failed: {register_response.text}")
            return False
            
        # Step 2: Login user
        print("\n2️⃣ Logging in new user...")
        login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print(f"   Status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            print("   ✅ Login successful")
            token_data = login_response.json()
            access_token = token_data.get('access_token')
            print(f"   Token type: {token_data.get('token_type')}")
        else:
            print(f"   ❌ Login failed: {login_response.text}")
            return False
            
        # Step 3: Test protected endpoint
        print("\n3️⃣ Testing protected endpoint...")
        headers = {"Authorization": f"Bearer {access_token}"}
        me_response = requests.get(f"{BASE_URL}/users/me", headers=headers)
        print(f"   Status: {me_response.status_code}")
        
        if me_response.status_code == 200:
            print("   ✅ Protected endpoint accessible")
            user_info = me_response.json()
            print(f"   User info: {json.dumps(user_info, indent=2)}")
        else:
            print(f"   ❌ Protected endpoint failed: {me_response.text}")
            
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure the server is running on http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_oauth2_endpoint():
    """Test OAuth2 compatible endpoint"""
    print("\n🧪 Testing OAuth2 Compatible Endpoint")
    print("=" * 50)
    
    oauth2_data = {
        "username": "demo@example.com",  # OAuth2 uses 'username' field
        "password": "demopassword123"
    }
    
    try:
        print("🔑 Testing OAuth2 login...")
        login_response = requests.post(f"{BASE_URL}/auth/token", data=oauth2_data)
        print(f"   Status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            print("   ✅ OAuth2 login successful")
            token_data = login_response.json()
            print(f"   Token type: {token_data.get('token_type')}")
            return True
        else:
            print(f"   ❌ OAuth2 login failed: {login_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    print("🚀 Complete Authentication Flow Test")
    print("=" * 60)
    print("📝 Make sure your FastAPI server is running on http://localhost:8000")
    print("   Start server with: uvicorn src.main:app --reload")
    print("=" * 60)
    
    # Test demo user login
    demo_success = test_demo_user_login()
    
    # Test new user flow
    new_user_success = test_new_user_flow()
    
    # Test OAuth2 endpoint
    oauth2_success = test_oauth2_endpoint()
    
    print("\n📊 Test Results Summary")
    print("=" * 30)
    print(f"Demo user login: {'✅ PASS' if demo_success else '❌ FAIL'}")
    print(f"New user flow: {'✅ PASS' if new_user_success else '❌ FAIL'}")
    print(f"OAuth2 endpoint: {'✅ PASS' if oauth2_success else '❌ FAIL'}")
    
    if all([demo_success, new_user_success, oauth2_success]):
        print("\n🎉 All tests passed! Authentication system is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main()
