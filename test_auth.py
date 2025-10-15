#!/usr/bin/env python3
"""
Simple test script to verify authentication flow
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_auth_flow():
    print("🧪 Testing Authentication Flow")
    print("=" * 50)
    print("📝 Make sure your FastAPI server is running on http://localhost:8000")
    print("   Start server with: uvicorn src.main:app --reload")
    print("=" * 50)
    
    # Test data
    test_user = {
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "testpassword123"
    }
    
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        # Step 1: Register user
        print("1️⃣ Registering user...")
        register_response = requests.post(f"{BASE_URL}/auth/", json=test_user)
        print(f"   Status: {register_response.status_code}")
        if register_response.status_code == 201:
            print("   ✅ User registered successfully")
            user_data = register_response.json()
            print(f"   User ID: {user_data.get('id')}")
            print(f"   Email: {user_data.get('email')}")
        else:
            print(f"   ❌ Registration failed: {register_response.text}")
            return
            
        # Step 2: Login user
        print("\n2️⃣ Logging in user...")
        login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print(f"   Status: {login_response.status_code}")
        if login_response.status_code == 200:
            print("   ✅ Login successful")
            token_data = login_response.json()
            access_token = token_data.get('access_token')
            print(f"   Token type: {token_data.get('token_type')}")
        else:
            print(f"   ❌ Login failed: {login_response.text}")
            return
            
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
            
        # Step 4: Test todos endpoint
        print("\n4️⃣ Testing todos endpoint...")
        todos_response = requests.get(f"{BASE_URL}/todos/", headers=headers)
        print(f"   Status: {todos_response.status_code}")
        if todos_response.status_code == 200:
            print("   ✅ Todos endpoint accessible")
            todos = todos_response.json()
            print(f"   Number of todos: {len(todos)}")
        else:
            print(f"   ❌ Todos endpoint failed: {todos_response.text}")
            
        print("\n🎉 Authentication flow test completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_auth_flow()
