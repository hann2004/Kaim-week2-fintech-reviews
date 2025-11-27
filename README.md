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
