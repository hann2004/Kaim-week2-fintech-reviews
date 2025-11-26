"""
Google Play Store Review Scraper
Task 1: Data Collection

Scrapes reviews for three Ethiopian banks:
- Commercial Bank of Ethiopia (CBE)
- Bank of Abyssinia (BOA) 
- Dashen Bank
"""

import pandas as pd
from google_play_scraper import reviews, Sort
import time
from datetime import datetime
import os

# Verified app IDs that work
BANK_APPS = {
    'CBE': 'com.combanketh.mobilebanking',
    'BOA': 'com.boa.boaMobileBanking',
    'DASHEN': 'com.dashen.dashensuperapp'
}

# Bank name mapping
BANK_NAMES = {
    'CBE': 'Commercial Bank of Ethiopia',
    'BOA': 'Bank of Abyssinia',
    'DASHEN': 'Dashen Bank'
}

def scrape_bank_reviews(app_id, bank_name, count=450):
    """
    Scrape reviews for a single bank app
    """
    print(f"Scraping {bank_name}...")
    
    try:
        # Get reviews from Google Play Store
        result, continuation_token = reviews(
            app_id,
            lang='en',           # Language
            country='et',        # Country (Ethiopia)
            sort=Sort.MOST_RELEVANT,  # Sort by relevance
            count=count,         # Number of reviews to fetch
            filter_score_with=None  # Get all ratings (1-5 stars)
        )
        
        # Convert to required format
        reviews_list = []
        for review in result:
            reviews_list.append({
                'review': review['content'],
                'rating': review['score'],
                'date': review['at'].strftime('%Y-%m-%d'),  # Format as YYYY-MM-DD
                'bank': bank_name,
                'source': 'Google Play Store'
            })
        
        print(f"✓ Collected {len(reviews_list)} reviews for {bank_name}")
        return reviews_list
        
    except Exception as e:
        print(f"✗ Error scraping {bank_name}: {e}")
        return []

def main():
    """
    Main function to scrape all banks
    """
    print("Starting Google Play Store Review Scraping")
    print("=" * 50)
    
    all_reviews = []
    
    # Scrape each bank
    for bank_code, app_id in BANK_APPS.items():
        bank_name = BANK_NAMES[bank_code]
        
        reviews_data = scrape_bank_reviews(app_id, bank_name, 450)
        all_reviews.extend(reviews_data)
        
        # Be polite - wait between requests
        time.sleep(2)
    
    # Create DataFrame
    if all_reviews:
        df = pd.DataFrame(all_reviews)
        
        # Create data directory if it doesn't exist
        os.makedirs('data/raw', exist_ok=True)
        
        # Save to CSV
        output_path = 'data/raw/bank_reviews.csv'
        df.to_csv(output_path, index=False)
        
        # Print summary
        print("\n" + "=" * 50)
        print("SCRAPING SUMMARY")
        print("=" * 50)
        print(f"Total reviews collected: {len(df)}")
        print("\nReviews per bank:")
        print(df['bank'].value_counts())
        print(f"\nData saved to: {output_path}")
        
        return df
    else:
        print("No reviews were collected.")
        return None

if __name__ == "__main__":
    df = main()