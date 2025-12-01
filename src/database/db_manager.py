"""
PostgreSQL Database Manager for Bank Reviews
"""

import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch
from typing import Dict, List, Optional
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class DatabaseManager:
    """Manages PostgreSQL database operations for bank reviews"""
    
    def __init__(self):
        """
        Initialize database connection using environment variables
        """
        self.connection_params = {
            'dbname': os.getenv('DB_NAME', 'bank_reviews'),
            'user': os.getenv('DB_USER', 'nabi'),
            'password': os.getenv('DB_PASSWORD', None),  # None for peer authentication
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432')
        }
        self.conn = None
        self.cursor = None
        
    def connect(self) -> bool:
        """Establish database connection"""
        try:
            # For peer authentication (no password), remove password if None
            if self.connection_params['password'] is None:
                self.connection_params.pop('password', None)
            
            self.conn = psycopg2.connect(**self.connection_params)
            self.cursor = self.conn.cursor()
            print(" Connected to PostgreSQL database successfully!")
            return True
        except Exception as e:
            print(f" Database connection failed: {e}")
            print(f"   Connection params: {self.connection_params}")
            return False
    
    # Rest of the methods remain the same...
    def disconnect(self) -> None:
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print(" Database connection closed.")
    
    def insert_banks(self, banks_data: List[Dict]) -> int:
        """Insert banks data into banks table"""
        if not self.conn:
            print(" Not connected to database")
            return 0
        
        insert_query = """
        INSERT INTO banks (bank_name, app_name) 
        VALUES (%s, %s)
        ON CONFLICT (bank_name) DO NOTHING
        RETURNING bank_id;
        """
        
        try:
            inserted_count = 0
            for bank in banks_data:
                self.cursor.execute(insert_query, (bank['bank_name'], bank['app_name']))
                result = self.cursor.fetchone()
                if result:
                    bank['bank_id'] = result[0]  # Store the generated bank_id
                    inserted_count += 1
            
            self.conn.commit()
            print(f" Inserted {inserted_count} banks")
            return inserted_count
            
        except Exception as e:
            self.conn.rollback()
            print(f" Error inserting banks: {e}")
            return 0
    
    def insert_reviews(self, reviews_data: List[Dict], bank_mapping: Dict[str, int]) -> int:
        """Insert reviews data into reviews table"""
        if not self.conn:
            print(" Not connected to database")
            return 0
        
        insert_query = """
        INSERT INTO reviews 
        (bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, source)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING;
        """
        
        # Prepare data for insertion
        prepared_data = []
        for review in reviews_data:
            bank_name = review['bank']
            if bank_name in bank_mapping:
                prepared_data.append((
                    bank_mapping[bank_name],  # bank_id
                    review['review_text'][:10000],  # Limit text length
                    review['rating'],
                    review['date'],
                    review['sentiment_label'],
                    review['sentiment_score'],
                    review.get('source', 'Google Play Store')
                ))
        
        try:
            # Use execute_batch for efficient bulk insertion
            execute_batch(self.cursor, insert_query, prepared_data)
            self.conn.commit()
            
            inserted_count = len(prepared_data)
            print(f" Inserted {inserted_count} reviews")
            return inserted_count
            
        except Exception as e:
            self.conn.rollback()
            print(f" Error inserting reviews: {e}")
            return 0
    
    def load_data_from_csv(self, csv_path: str = "data/processed/sentiment_themes_analysis.csv") -> bool:
        """Load data from CSV file into database"""
        print(" Loading data from CSV...")
        
        try:
            # Read CSV
            df = pd.read_csv(csv_path)
            print(f" Loaded {len(df)} reviews from CSV")
            
            # Prepare banks data
            banks_info = {
                'Commercial Bank of Ethiopia': 'com.combanketh.mobilebanking',
                'Bank of Abyssinia': 'com.boa.boaMobileBanking',
                'Dashen Bank': 'com.dashen.dashensuperapp'
            }
            
            banks_data = [
                {'bank_name': bank, 'app_name': app_id}
                for bank, app_id in banks_info.items()
            ]
            
            # Insert banks and get bank_id mapping
            self.insert_banks(banks_data)
            
            # Create bank name to ID mapping
            self.cursor.execute("SELECT bank_id, bank_name FROM banks;")
            bank_rows = self.cursor.fetchall()
            bank_mapping = {name: bank_id for bank_id, name in bank_rows}
            
            # Convert DataFrame to list of dictionaries for reviews
            reviews_data = df.to_dict('records')
            
            # Insert reviews
            inserted = self.insert_reviews(reviews_data, bank_mapping)
            
            return inserted > 0
            
        except Exception as e:
            print(f" Error loading data from CSV: {e}")
            return False

# Helper function for main execution
def main():
    """Main function to demonstrate database operations"""
    db = DatabaseManager()
    
    if db.connect():
        try:
            # Test connection
            db.cursor.execute("SELECT version();")
            version = db.cursor.fetchone()
            print(f" PostgreSQL Version: {version[0]}")
            
            # Load data from CSV
            success = db.load_data_from_csv()
            
            if success:
                print("\n Database population completed successfully!")
            else:
                print("\n Database population failed!")
                
        finally:
            db.disconnect()

if __name__ == "__main__":
    main()