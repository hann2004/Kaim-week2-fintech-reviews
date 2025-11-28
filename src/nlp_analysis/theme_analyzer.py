"""
Professional Thematic Analysis for Bank Reviews
Keyword extraction and theme clustering using TF-IDF and rule-based classification
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation, NMF
from collections import Counter, defaultdict
import re
from typing import Dict, List, Tuple

class ThemeAnalyzer:
    """Professional thematic analysis for financial app reviews"""
    
    def __init__(self):
        self.theme_keywords = self._initialize_theme_keywords()
        self.vectorizer = TfidfVectorizer(
            max_features=100,
            stop_words='english',
            ngram_range=(1, 2),  # Single words and bigrams
            min_df=2,  # Ignore terms that appear in less than 2 documents
            max_df=0.8  # Ignore terms that appear in more than 80% of documents
        )
    
    def _initialize_theme_keywords(self) -> Dict[str, List[str]]:
        """Initialize theme keywords based on banking domain knowledge"""
        return {
            'APP_PERFORMANCE': [
                'slow', 'fast', 'speed', 'loading', 'crash', 'freeze', 'lag', 
                'performance', 'responsive', 'smooth', 'hanging'
            ],
            'RELIABILITY_ISSUES': [
                'error', 'bug', 'glitch', 'not working', 'problem', 'issue',
                'failed', 'broken', 'technical', 'malfunction', 'down'
            ],
            'USER_INTERFACE': [
                'interface', 'design', 'layout', 'navigation', 'menu',
                'button', 'screen', 'display', 'theme', 'color', 'font'
            ],
            'SECURITY_ACCESS': [
                'login', 'password', 'security', 'authentication', 'biometric',
                'fingerprint', 'face id', 'pin', 'verification', 'access'
            ],
            'TRANSACTIONS': [
                'transfer', 'payment', 'transaction', 'send money', 'receive',
                'bill', 'airtime', 'mobile banking', 'fund', 'amount'
            ],
            'CUSTOMER_SUPPORT': [
                'support', 'service', 'help', 'assistance', 'response',
                'contact', 'complaint', 'feedback', 'representative'
            ],
            'FEATURE_REQUEST': [
                'should', 'could', 'would', 'please add', 'need', 'want',
                'missing', 'suggestion', 'improvement', 'enhancement'
            ]
        }
    
    def extract_keywords_tfidf(self, texts: List[str], top_n: int = 20) -> List[Tuple[str, float]]:
        """Extract top keywords using TF-IDF"""
        try:
            tfidf_matrix = self.vectorizer.fit_transform(texts)
            feature_names = self.vectorizer.get_feature_names_out()
            
            # Get average TF-IDF scores across all documents
            scores = np.asarray(tfidf_matrix.mean(axis=0)).flatten()
            keyword_scores = list(zip(feature_names, scores))
            
            # Sort by score and return top N
            keyword_scores.sort(key=lambda x: x[1], reverse=True)
            return keyword_scores[:top_n]
        
        except Exception as e:
            print(f"TF-IDF extraction error: {e}")
            return []
    
    def extract_ngrams(self, texts: List[str], n: int = 2, top_n: int = 15) -> List[Tuple[str, int]]:
        """Extract common n-grams from texts"""
        ngrams = []
        
        for text in texts:
            words = text.split()
            for i in range(len(words) - n + 1):
                ngram = ' '.join(words[i:i + n])
                ngrams.append(ngram)
        
        return Counter(ngrams).most_common(top_n)
    
    def classify_review_themes(self, text: str, threshold: float = 0.1) -> List[str]:
        """Classify review into themes based on keyword matching"""
        if not text or pd.isna(text):
            return []
        
        text_lower = text.lower()
        theme_scores = {}
        
        for theme, keywords in self.theme_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    # Give more weight to exact matches and important keywords
                    if f' {keyword} ' in f' {text_lower} ':
                        score += 2
                    else:
                        score += 1
            
            if score > 0:
                theme_scores[theme] = score
        
        # Normalize scores and apply threshold
        if theme_scores:
            max_score = max(theme_scores.values())
            themes = [theme for theme, score in theme_scores.items() 
                     if score / max_score >= threshold]
            return themes
        
        return []
    
    def analyze_themes_by_bank(self, df: pd.DataFrame, text_column: str = 'processed_text') -> Dict:
        """Perform thematic analysis grouped by bank"""
        print("Starting thematic analysis by bank...")
        
        theme_analysis = {}
        
        for bank in df['bank'].unique():
            print(f"\nAnalyzing themes for {bank}...")
            bank_reviews = df[df['bank'] == bank][text_column].tolist()  
            
            # Extract keywords
            keywords = self.extract_keywords_tfidf(bank_reviews)
            bigrams = self.extract_ngrams(bank_reviews, n=2)
            trigrams = self.extract_ngrams(bank_reviews, n=3)
            
            # Classify themes for each review
            bank_df = df[df['bank'] == bank].copy()
            bank_df['themes'] = bank_df[text_column].apply(self.classify_review_themes)
            
            # Count theme frequency
            all_themes = [theme for themes in bank_df['themes'] for theme in themes]
            theme_counts = Counter(all_themes)
            
            theme_analysis[bank] = {
                'top_keywords': keywords[:10],
                'top_bigrams': bigrams,
                'top_trigrams': trigrams,
                'theme_distribution': dict(theme_counts.most_common()),
                'sample_reviews': self._get_theme_samples(bank_df)
            }
            
            print(f"✓ {bank}: {len(keywords)} keywords, {len(theme_counts)} themes identified")
        
        return theme_analysis
    
    def _get_theme_samples(self, df: pd.DataFrame, n_samples: int = 2) -> Dict[str, List[str]]:
        """Get sample reviews for each theme"""
        theme_samples = {}
        
        for theme in self.theme_keywords.keys():
            theme_reviews = df[df['themes'].apply(lambda x: theme in x)]
            if len(theme_reviews) > 0:
                samples = theme_reviews.head(n_samples)['review_cleaned'].tolist()
                theme_samples[theme] = samples
        
        return theme_samples
    
    def generate_theme_report(self, theme_analysis: Dict) -> None:
        """Generate comprehensive theme analysis report"""
        print("\n" + "="*60)
        print("THEMATIC ANALYSIS REPORT")
        print("="*60)
        
        for bank, analysis in theme_analysis.items():
            print(f"\n {bank.upper()}")
            print("-" * 40)
            
            print("\n Top Keywords:")
            for keyword, score in analysis['top_keywords']:
                print(f"  {keyword}: {score:.3f}")
            
            print("\n  Theme Distribution:")
            for theme, count in analysis['theme_distribution'].items():
                print(f"  {theme}: {count} reviews")
            
            print("\n Sample Bigrams:")
            for bigram, count in analysis['top_bigrams'][:5]:
                print(f"  '{bigram}': {count}")

# Example usage
if __name__ == "__main__":
    analyzer = ThemeAnalyzer()
    
    sample_reviews = [
        "The app is very slow when transferring money",
        "I love the user interface design",
        "Login keeps failing with error messages",
        "Great customer support team"
    ]
    
    for review in sample_reviews:
        themes = analyzer.classify_review_themes(review)
        print(f"Review: {review}")
        print(f"Themes: {themes}\n")