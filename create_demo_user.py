#!/usr/bin/env python3
"""
Script to create a demo user in the database
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.database.core import SessionLocal, engine, Base
from src.entities.user import User
from src.auth.service import get_password_hash
from uuid import uuid4

def create_demo_user():
    """Create a demo user for testing"""
    print("🔧 Creating demo user...")
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if demo user already exists
        existing_user = db.query(User).filter(User.email == "demo@example.com").first()
        if existing_user:
            print("✅ Demo user already exists!")
            print(f"   Email: {existing_user.email}")
            print(f"   ID: {existing_user.id}")
            return existing_user
        
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
        
        print("✅ Demo user created successfully!")
        print(f"   Email: {demo_user.email}")
        print(f"   Password: demopassword123")
        print(f"   ID: {demo_user.id}")
        
        return demo_user
        
    except Exception as e:
        print(f"❌ Error creating demo user: {e}")
        db.rollback()
        return None
    finally:
        db.close()

if __name__ == "__main__":
    create_demo_user()
