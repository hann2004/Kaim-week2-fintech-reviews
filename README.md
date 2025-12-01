# Kaim-week2-fintech-reviews
## Task 1: Data Collection & Preprocessing - COMPLETED 

### Methodology
1. **Data Collection**: Used `google-play-scraper` to collect 450 reviews per bank
2. **App IDs Verified**: 
   - CBE: `com.combanketh.mobilebanking`
   - BOA: `com.boa.boaMobileBanking`
   - Dashen: `com.dashen.dashensuperapp`
3. **Preprocessing Steps**:
   - Duplicate removal (4 duplicates found)
   - Date normalization to YYYY-MM-DD
   - Text cleaning and whitespace removal
   - Data validation and quality checks

### Results
- **Total Reviews**: 1,346 (after preprocessing)
- **Data Quality**: 99.7% retention rate, 0.30% error rate
- **Reviews per Bank**: 
  - Commercial Bank of Ethiopia: 450
  - Bank of Abyssinia: 450  
  - Dashen Bank: 446
- **Files Created**:
  - `data/raw/bank_reviews.csv` - Raw scraped data
  - `data/processed/bank_reviews_cleaned.csv` - Processed data

## Database Schema

### Tables Structure

#### 1. `banks` Table
- `bank_id` SERIAL PRIMARY KEY
- `bank_name` VARCHAR(100) NOT NULL UNIQUE
- `app_name` VARCHAR(200)
- `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP

#### 2. `reviews` Table
- `review_id` SERIAL PRIMARY KEY
- `bank_id` INTEGER NOT NULL REFERENCES banks(bank_id) ON DELETE CASCADE
- `review_text` TEXT NOT NULL
- `rating` INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5)
- `review_date` DATE NOT NULL
- `sentiment_label` VARCHAR(20)
- `sentiment_score` DECIMAL(5,4) CHECK (sentiment_score >= 0 AND sentiment_score <= 1)
- `source` VARCHAR(50) DEFAULT 'Google Play Store'
- `processed_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP

### Indexes
- `idx_reviews_bank_id` ON reviews(bank_id)
- `idx_reviews_rating` ON reviews(rating)
- `idx_reviews_sentiment` ON reviews(sentiment_label)
- `idx_reviews_date` ON reviews(review_date)

### Data Statistics
- Total banks: 3
- Total reviews: 1,346
- Reviews per bank: CBE(450), BOA(450), Dashen(446)
- Database: PostgreSQL 16.10
