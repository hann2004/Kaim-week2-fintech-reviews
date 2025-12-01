"""
Unit tests for database operations
Tests should be in tests/ folder, not scripts/
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from src.database.db_manager import DatabaseManager

class TestDatabaseConnection:
    """Test database connectivity and basic operations"""
    
    def test_connection(self):
        """Test database connection"""
        db = DatabaseManager()
        assert db.connect() == True, "Database connection should succeed"
        db.disconnect()
    
    def test_version(self):
        """Test PostgreSQL version retrieval"""
        db = DatabaseManager()
        if db.connect():
            db.cursor.execute("SELECT version();")
            version = db.cursor.fetchone()
            assert version is not None, "Should retrieve PostgreSQL version"
            assert "PostgreSQL" in version[0], "Should be PostgreSQL version"
            db.disconnect()
    
    def test_table_count(self):
        """Test that tables exist"""
        db = DatabaseManager()
        if db.connect():
            db.cursor.execute("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = 'public';
            """)
            table_count = db.cursor.fetchone()[0]
            assert table_count >= 2, f"Should have at least 2 tables, got {table_count}"
            db.disconnect()

def test_database_integration():
    """Integration test for database operations"""
    print("\n🔍 Running Database Integration Test...")
    
    db = DatabaseManager()
    
    if db.connect():
        try:
            # Test 1: Check PostgreSQL version
            db.cursor.execute("SELECT version();")
            version = db.cursor.fetchone()
            print(f" PostgreSQL Version: {version[0]}")
            
            # Test 2: Count tables
            db.cursor.execute("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = 'public';
            """)
            table_count = db.cursor.fetchone()[0]
            print(f" Tables in database: {table_count}")
            
            # Test 3: Show table structure
            print("\n Table Structure:")
            db.cursor.execute("""
                SELECT table_name, column_name, data_type 
                FROM information_schema.columns 
                WHERE table_schema = 'public'
                ORDER BY table_name, ordinal_position;
            """)
            
            for table, column, dtype in db.cursor.fetchall():
                print(f"  {table}.{column}: {dtype}")
            
            return True
            
        except Exception as e:
            print(f" Test failed: {e}")
            return False
        finally:
            db.disconnect()
    else:
        return False

if __name__ == "__main__":
    # Run integration test when script is executed directly
    success = test_database_integration()
    
    if success:
        print("\n Database integration test PASSED!")
    else:
        print("\n Database integration test FAILED!")