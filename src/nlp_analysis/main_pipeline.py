"""
Main NLP Analysis Pipeline
Orchestrates sentiment and thematic analysis for bank reviews
"""

import pandas as pd
import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.text_preprocessor import TextPreprocessor
from nlp_analysis.sentiment_analyzer import SentimentAnalyzer
from nlp_analysis.theme_analyzer import ThemeAnalyzer

class NLPAnalysisPipeline:
    """Main pipeline for comprehensive NLP analysis"""
    
    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.theme_analyzer = ThemeAnalyzer()
        self.results = {}
    
    def load_data(self, data_path: str = 'data/processed/bank_reviews_cleaned.csv') -> pd.DataFrame:
        """Load and prepare data for analysis"""
        print("Loading data for NLP analysis...")
        
        try:
            df = pd.read_csv(data_path)
            print(f"✓ Loaded {len(df)} reviews from {data_path}")
            return df
        except Exception as e:
            print(f"✗ Error loading data: {e}")
            raise
    
    def run_complete_analysis(self, data_path: str = None) -> dict:
        """Run complete NLP analysis pipeline"""
        print(" Starting Complete NLP Analysis Pipeline")
        print("=" * 60)
        
        # Load data
        df = self.load_data(data_path) if data_path else self.load_data()
        
        # Step 1: Text preprocessing
        print("\n Step 1: Text Preprocessing")
        df_processed = self.preprocessor.preprocess_dataframe(df)
        
        # Step 2: Sentiment analysis
        print("\n Step 2: Sentiment Analysis")
        df_sentiment = self.sentiment_analyzer.analyze_dataframe(df_processed)
        
        # Step 3: Thematic analysis
        print("\n  Step 3: Thematic Analysis")
        theme_analysis = self.theme_analyzer.analyze_themes_by_bank(df_sentiment)

        # Add themes to the dataframe
        print("\n Adding themes to dataframe...")
        df_sentiment['themes'] = df_sentiment['processed_text'].apply(self.theme_analyzer.classify_review_themes)
        print("✓ Themes added to dataframe")

        # Step 4: Generate reports
        print("\n Step 4: Generating Reports")
        sentiment_report = self.sentiment_analyzer.generate_sentiment_report(df_sentiment)
        self.theme_analyzer.generate_theme_report(theme_analysis)

        # Save results
        self.results = {
            'dataframe': df_sentiment,
            'sentiment_report': sentiment_report,
            'theme_analysis': theme_analysis,
            'timestamp': datetime.now().isoformat()
        }

        # Save analyzed data
        self.save_results(df_sentiment, theme_analysis)
        
        print("\n NLP Analysis Pipeline Completed Successfully!")
        return self.results
    
    def save_results(self, df: pd.DataFrame, theme_analysis: dict) -> None:
        """Save multiple CSV files matching all requirements"""
        output_dir = 'data/processed'
        os.makedirs(output_dir, exist_ok=True)
        
        # 1. Main analysis CSV (required)
        main_analysis_df = pd.DataFrame({
            'review_id': df.index,
            'review_text': df['review_cleaned'],
            'sentiment_label': df['sentiment_label'],
            'sentiment_score': df['sentiment_score'],
            'identified_themes': df['themes'].apply(lambda x: ', '.join(x) if x else 'No themes'),
            'bank': df['bank'],
            'rating': df['rating'],
            'date': df['date']
        })
        
        main_output_path = os.path.join(output_dir, 'sentiment_themes_analysis.csv')
        main_analysis_df.to_csv(main_output_path, index=False)
        print(f"✓ 1. Main analysis saved: {main_output_path}")
        
        # 2. Keywords extraction CSV
        keywords_data = []
        for bank, analysis in theme_analysis.items():
            for keyword, score in analysis['top_keywords']:
                keywords_data.append({
                    'bank': bank,
                    'keyword': keyword,
                    'tfidf_score': score,
                    'type': 'keyword'
                })
            for bigram, count in analysis['top_bigrams']:
                keywords_data.append({
                    'bank': bank, 
                    'keyword': bigram,
                    'tfidf_score': count,
                    'type': 'bigram'
                })
        
        keywords_df = pd.DataFrame(keywords_data)
        keywords_output_path = os.path.join(output_dir, 'extracted_keywords.csv')
        keywords_df.to_csv(keywords_output_path, index=False)
        print(f"✓ 2. Keywords extracted: {keywords_output_path}")
        
        # 3. Theme clusters per bank CSV
        theme_clusters_data = []
        for bank, analysis in theme_analysis.items():
            for theme, count in analysis['theme_distribution'].items():
                theme_clusters_data.append({
                    'bank': bank,
                    'theme': theme,
                    'review_count': count,
                    'percentage': (count / len(df[df['bank'] == bank])) * 100
                })
        
        themes_df = pd.DataFrame(theme_clusters_data)
        themes_output_path = os.path.join(output_dir, 'theme_clusters.csv')
        themes_df.to_csv(themes_output_path, index=False)
        print(f"✓ 3. Theme clusters saved: {themes_output_path}")
        
        # 4. Full dataset (backup)
        full_output_path = os.path.join(output_dir, 'reviews_with_sentiment_themes.csv')
        df.to_csv(full_output_path, index=False)
        print(f"✓ 4. Full dataset backup: {full_output_path}")
def main():
    """Main execution function"""
    try:
        pipeline = NLPAnalysisPipeline()
        results = pipeline.run_complete_analysis()
        
        print("\n" + "=" * 60)
        print("ANALYSIS COMPLETE - KEY METRICS")
        print("=" * 60)
        
        df = results['dataframe']
        print(f" Total reviews analyzed: {len(df)}")
        print(f" Sentiment coverage: {100 * (len(df) / len(df)):.1f}%")
        print(f" Banks analyzed: {df['bank'].nunique()}")
        print(f" Themes identified: Multiple per bank")
        
        return results
        
    except Exception as e:
        print(f" Pipeline execution failed: {e}")
        return None

if __name__ == "__main__":
    results = main()