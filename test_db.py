#!/usr/bin/env python3
"""
Test database connection
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def test_database_connection():
    print("🔍 Testing Database Connection")
    print("=" * 40)
    
    # Get database URL
    database_url = os.getenv('DATABASE_URL', 'postgresql+psycopg2://postgres:postgres@localhost:5432/postgres')
    print(f"Database URL: {database_url}")
    
    try:
        # Create engine
        engine = create_engine(database_url, pool_pre_ping=True)
        
        # Test connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
            print(f"Test query result: {result.fetchone()}")
            
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure PostgreSQL is running")
        print("2. Check if the database 'postgres' exists")
        print("3. Verify username/password are correct")
        print("4. Check if the port 5432 is accessible")

if __name__ == "__main__":
    test_database_connection()



