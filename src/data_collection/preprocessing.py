"""
Data Preprocessing Script
Task 1: Data Preprocessing

Cleans and preprocesses the scraped reviews data:
- Removes duplicates
- Handles missing data  
- Normalizes dates
- Cleans text data
- Saves processed data
"""

import pandas as pd
import numpy as np
from datetime import datetime
import re
import os

class ReviewPreprocessor:
    """Preprocessor for bank review data"""
    
    def __init__(self, input_path='data/raw/bank_reviews.csv', 
                 output_path='data/processed/bank_reviews_cleaned.csv'):
        self.input_path = input_path
        self.output_path = output_path
        self.df = None
        self.stats = {}
    
    def load_data(self):
        """Load the raw reviews data"""
        print("Loading raw data...")
        try:
            self.df = pd.read_csv(self.input_path)
            print(f"✓ Loaded {len(self.df)} reviews")
            self.stats['original_count'] = len(self.df)
            return True
        except Exception as e:
            print(f"✗ Error loading data: {e}")
            return False
    
    def remove_duplicates(self):
        """Remove duplicate reviews"""
        print("\n[1/5] Removing duplicates...")
        before = len(self.df)
        self.df = self.df.drop_duplicates(subset=['review'], keep='first')
        after = len(self.df)
        removed = before - after
        print(f"✓ Removed {removed} duplicate reviews")
        self.stats['duplicates_removed'] = removed
    
    def handle_missing_data(self):
        """Handle missing values"""
        print("\n[2/5] Handling missing data...")
        
        # Check missing values before
        missing_before = self.df.isnull().sum()
        print("Missing values before cleaning:")
        for col, count in missing_before.items():
            if count > 0:
                print(f"  {col}: {count}")
        
        # Remove rows with missing critical data
        critical_cols = ['review', 'rating', 'bank']
        self.df = self.df.dropna(subset=critical_cols)
        
        # Fill other missing values
        self.df['date'] = self.df['date'].fillna(datetime.now().strftime('%Y-%m-%d'))
        self.df['source'] = self.df['source'].fillna('Google Play Store')
        
        # Check missing values after
        missing_after = self.df.isnull().sum()
        print("Missing values after cleaning:")
        for col, count in missing_after.items():
            if count > 0:
                print(f"  {col}: {count}")
        
        self.stats['missing_handled'] = missing_before.sum() - missing_after.sum()
    
    def normalize_dates(self):
        """Normalize date formats to YYYY-MM-DD"""
        print("\n[3/5] Normalizing dates...")
        
        try:
            # Convert to datetime and format
            self.df['date'] = pd.to_datetime(self.df['date']).dt.strftime('%Y-%m-%d')
            print(f"✓ Dates normalized to YYYY-MM-DD format")
            
            # Add year and month columns for analysis
            self.df['review_year'] = pd.to_datetime(self.df['date']).dt.year
            self.df['review_month'] = pd.to_datetime(self.df['date']).dt.month
            
        except Exception as e:
            print(f"✗ Error normalizing dates: {e}")
    
    def clean_text(self):
        """Clean review text"""
        print("\n[4/5] Cleaning text data...")
        
        def clean_text_content(text):
            """Clean individual review text"""
            if pd.isna(text):
                return ""
            
            text = str(text)
            # Remove extra whitespace
            text = re.sub(r'\s+', ' ', text)
            # Remove leading/trailing whitespace
            text = text.strip()
            return text
        
        # Apply cleaning
        self.df['review_cleaned'] = self.df['review'].apply(clean_text_content)
        
        # Remove empty reviews after cleaning
        before = len(self.df)
        self.df = self.df[self.df['review_cleaned'].str.len() > 0]
        after = len(self.df)
        empty_removed = before - after
        
        print(f"✓ Cleaned text data")
        if empty_removed > 0:
            print(f"✓ Removed {empty_removed} empty reviews")
        
        self.stats['empty_reviews_removed'] = empty_removed
    
    def validate_data(self):
        """Validate data quality"""
        print("\n[5/5] Validating data...")
        
        # Validate ratings (should be 1-5)
        invalid_ratings = self.df[~self.df['rating'].between(1, 5)]
        if len(invalid_ratings) > 0:
            print(f"⚠ Found {len(invalid_ratings)} invalid ratings")
            self.df = self.df[self.df['rating'].between(1, 5)]
        
        # Check final data quality
        missing_final = self.df.isnull().sum().sum()
        if missing_final == 0:
            print("✓ No missing data in final dataset")
        else:
            print(f"⚠ {missing_final} missing values remain")
        
        self.stats['final_count'] = len(self.df)
        self.stats['data_quality'] = (1 - (missing_final / (len(self.df) * len(self.df.columns)))) * 100
    
    def save_data(self):
        """Save processed data"""
        print("\nSaving processed data...")
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        
        # Save to CSV
        self.df.to_csv(self.output_path, index=False)
        print(f"✓ Processed data saved to: {self.output_path}")
        
        return True
    
    def generate_report(self):
        """Generate preprocessing report"""
        print("\n" + "="*60)
        print("PREPROCESSING REPORT")
        print("="*60)
        
        print(f"\nOriginal records: {self.stats.get('original_count', 0)}")
        print(f"Duplicates removed: {self.stats.get('duplicates_removed', 0)}")
        print(f"Empty reviews removed: {self.stats.get('empty_reviews_removed', 0)}")
        print(f"Final records: {self.stats.get('final_count', 0)}")
        
        if self.stats.get('original_count', 0) > 0:
            retention = (self.stats['final_count'] / self.stats['original_count']) * 100
            error_rate = 100 - retention
            print(f"\nData retention rate: {retention:.2f}%")
            print(f"Data error rate: {error_rate:.2f}%")
            
            if error_rate < 5:
                print("✓ Data quality: EXCELLENT (<5% errors)")
            else:
                print("⚠ Data quality: Needs attention")
        
        print(f"\nReviews per bank:")
        bank_counts = self.df['bank'].value_counts()
        for bank, count in bank_counts.items():
            print(f"  {bank}: {count}")
        
        print(f"\nRating distribution:")
        rating_counts = self.df['rating'].value_counts().sort_index(ascending=False)
        for rating, count in rating_counts.items():
            pct = (count / len(self.df)) * 100
            print(f"  {'⭐' * int(rating)}: {count} ({pct:.1f}%)")
    
    def process(self):
        """Run complete preprocessing pipeline"""
        print("Starting data preprocessing...")
        print("="*60)
        
        if not self.load_data():
            return False
        
        self.remove_duplicates()
        self.handle_missing_data()
        self.normalize_dates()
        self.clean_text()
        self.validate_data()
        
        if self.save_data():
            self.generate_report()
            return True
        
        return False

def main():
    """Main execution function"""
    preprocessor = ReviewPreprocessor()
    success = preprocessor.process()
    
    if success:
        print("\n Preprocessing completed successfully!")
        return preprocessor.df
    else:
        print("\n Preprocessing failed!")
        return None

if __name__ == "__main__":
    processed_df = main()