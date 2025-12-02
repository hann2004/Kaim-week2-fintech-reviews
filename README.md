
# Fintech App Reviews Analytics: Customer Insights for Ethiopian Banks

[![CI](https://github.com/hann2004/Kaim-week2-fintech-reviews/actions/workflows/unittests.yml/badge.svg)]()
[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)]()
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-blue?logo=postgresql)]()
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?logo=jupyter)]()
[![License](https://img.shields.io/badge/License-MIT-green)]()

A comprehensive data engineering pipeline to analyze customer satisfaction for three leading Ethiopian banks by scraping Google Play Store reviews, performing sentiment and thematic analysis, and storing insights in a production-ready PostgreSQL database.

This project was completed as the **final submission for the 10 Academy — AI Mastery Program (Week 2 Challenge)**.

---

##  Objectives

Omega Consultancy aimed to help banks improve mobile app retention and features. This project delivers:

* **Data Collection**: Automated scraping of 1,300+ user reviews per bank from Google Play Store.
* **Sentiment Analysis**: Quantification using the **DistilBERT** NLP model.
* **Thematic Analysis**: Identification of key issues through TF-IDF and rule-based clustering.
* **Database Engineering**: Normalized PostgreSQL schema for persistent storage.
* **Actionable Business Intelligence**: A professional report with insights for product teams.

---

##  Repository Structure

```
Kaim-week2-fintech-reviews/
├── data/
│   ├── raw/
│   └── processed/
├── database/
│   └── schema.sql
├── notebooks/
│   ├── preprocessing_EDA.ipynb
│   ├── sentiment_thematic_analysis.ipynb
│   ├── database_integration.ipynb
│   └── insights_recommendations.ipynb
├── reports/
│   └── figures/
├── src/
│   ├── data_collection/
│   ├── nlp_analysis/
│   ├── database/
│   ├── insights/
│   └── utils/
├── tests/
├── scripts/
├── .github/workflows/
│   └── unittests.yml
├── .env.example
├── requirements.txt
└── README.md
```

---

##  Features Implemented

### **Task 1: Data Collection & Preprocessing**

* Scraped 1,346+ reviews per bank using `google-play-scraper`.
* Cleaned and normalized data.
* Achieved **99.7% data retention**.

### **Task 2: Sentiment & Thematic Analysis**

* Used **DistilBERT-base-uncased** for sentiment scoring.
* TF-IDF + rule-based thematic classification into 7 themes.
* 100% coverage of all reviews.

### **Task 3: PostgreSQL Database Integration**

* Designed normalized schema (`banks`, `reviews`).
* Loaded all data using a Python pipeline with `psycopg2`.
* Applied constraints, indexes, and foreign keys.

### **Task 4: Insights, Visualization & Reporting**

* Generated business insights for each bank.
* Created professional visualizations (Matplotlib/Seaborn).
* Delivered a 10-page Medium-style report.

### **Engineering Practices**

* Modular, production-quality code.
* Git feature-branch workflow.
* CI with GitHub Actions.
* Secure environment variable management.

---

##  Environment Setup

### 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/Kaim-week2-fintech-reviews.git
cd Kaim-week2-fintech-reviews
```

### 2. Create Environment

```bash
conda create -n kaim_week2 python=3.9 -y
conda activate kaim_week2
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 4. Setup PostgreSQL

```bash
sudo -u postgres psql -c "CREATE DATABASE bank_reviews OWNER nabi;"
cp .env.example .env
```

Edit `.env` with your database credentials.

---

##  Running the Full Pipeline

### Run main scripts

```bash
python src/data_collection/scraper.py
python src/data_collection/preprocessing.py
python src/nlp_analysis/main_pipeline.py
python src/database/db_manager.py
python src/insights/analyzer.py
python src/insights/visualizer.py
```

### Or use notebooks

```bash
jupyter notebook notebooks/
```

---

##  Running Tests

```bash
pytest tests/ -v
```

---

##  Key Findings & Insights

* **Dashen Bank leads** with **65.9% positive sentiment**.
* **CBE and BOA** show **~84% negative sentiment** driven mainly by:

  * Transaction failures
  * App crashes
  * Performance lag

**Recommendations:**

* CBE/BOA: Prioritize backend stabilization.
* Dashen: Invest in innovation and user experience enhancements.

All processed data is stored in PostgreSQL with complete referential integrity.

---

##  Visualizations

Located in `reports/figures/`:

* `sentiment_comparison.png`
* `rating_distribution.png`
* `theme_analysis.png`
* `wordcloud_*.png`

---

##  Future Improvements

* Automated weekly scraping.
* Predictive modeling on rating trends.
* Streamlit dashboard.
* iOS App Store integration.
* Global fintech benchmarking.

---

##  Author

**Hanan Nasir**
10 Academy — AI Mastery Program, Week 2
Data Analyst, Omega Consultancy

---

##  License

Released under the MIT License.

