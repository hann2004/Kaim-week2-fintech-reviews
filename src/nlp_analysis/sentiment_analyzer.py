"""
Professional Sentiment Analysis for Bank Reviews
Using DistilBERT for accurate sentiment classification
"""

import pandas as pd
import numpy as np
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from typing import Dict, Tuple
import torch

class SentimentAnalyzer:
    """Professional sentiment analysis using DistilBERT"""
    
    def __init__(self, model_name: str = "distilbert-base-uncased-finetuned-sst-2-english"):
        print("Initializing sentiment analyzer...")
        
        # Use GPU if available
        self.device = 0 if torch.cuda.is_available() else -1
        print(f"Using device: {'GPU' if self.device == 0 else 'CPU'}")
        
        try:
            self.classifier = pipeline(
                "sentiment-analysis",
                model=model_name,
                device=self.device,
                truncation=True
            )
            self.model_loaded = True
            print("✓ DistilBERT sentiment model loaded successfully")
        except Exception as e:
            print(f"⚠ Could not load DistilBERT: {e}")
            self.model_loaded = False
            self._setup_fallback()
    
    def _setup_fallback(self):
        """Setup fallback sentiment analysis"""
        try:
            from textblob import TextBlob
            self.use_textblob = True
            print("✓ TextBlob fallback loaded")
        except ImportError:
            self.use_textblob = False
            print("⚠ No sentiment analysis fallback available")
    
    def analyze_sentiment_distilbert(self, text: str) -> Tuple[str, float]:
        """Analyze sentiment using DistilBERT"""
        if not text or len(text.strip()) == 0:
            return "NEUTRAL", 0.5
        
        try:
            result = self.classifier(text[:512])[0]  # Truncate to model limit
            label = result['label']
            score = result['score']
            
            # Convert to our format
            if label == 'POSITIVE':
                return 'POSITIVE', score
            elif label == 'NEGATIVE':
                return 'NEGATIVE', score
            else:
                return 'NEUTRAL', 0.5
                
        except Exception as e:
            print(f"Sentiment analysis error: {e}")
            return "NEUTRAL", 0.5
    
    def analyze_sentiment_textblob(self, text: str) -> Tuple[str, float]:
        """Fallback sentiment analysis using TextBlob"""
        from textblob import TextBlob
        
        analysis = TextBlob(text)
        polarity = analysis.sentiment.polarity
        
        if polarity > 0.1:
            return 'POSITIVE', (polarity + 1) / 2
        elif polarity < -0.1:
            return 'NEGATIVE', (1 - polarity) / 2
        else:
            return 'NEUTRAL', 0.5
    
    def analyze_dataframe(self, df: pd.DataFrame, text_column: str = 'processed_text') -> pd.DataFrame:
        """Perform sentiment analysis on entire DataFrame"""
        print("Starting sentiment analysis...")
        
        sentiments = []
        scores = []
        
        for idx, text in enumerate(df[text_column]):
            if idx % 100 == 0:
                print(f"Processed {idx}/{len(df)} reviews...")
            
            if self.model_loaded:
                sentiment, score = self.analyze_sentiment_distilbert(text)
            elif self.use_textblob:
                sentiment, score = self.analyze_sentiment_textblob(text)
            else:
                sentiment, score = "NEUTRAL", 0.5
            
            sentiments.append(sentiment)
            scores.append(score)
        
        df['sentiment_label'] = sentiments
        df['sentiment_score'] = scores
        
        print("✓ Sentiment analysis completed")
        print(f"Sentiment distribution:")
        print(df['sentiment_label'].value_counts())
        
        return df
    
    def generate_sentiment_report(self, df: pd.DataFrame) -> Dict:
        """Generate comprehensive sentiment report"""
        report = {
            'total_reviews': len(df),
            'sentiment_distribution': df['sentiment_label'].value_counts().to_dict(),
            'sentiment_by_bank': df.groupby('bank')['sentiment_label'].value_counts().unstack().to_dict(),
            'avg_sentiment_score_by_bank': df.groupby('bank')['sentiment_score'].mean().to_dict(),
            'sentiment_by_rating': df.groupby('rating')['sentiment_label'].value_counts().unstack().to_dict()
        }
        
        return report

# Example usage
if __name__ == "__main__":
    analyzer = SentimentAnalyzer()
    sample_texts = [
        "This app is amazing and very useful!",
        "I hate this app, it keeps crashing.",
        "The app works okay but could be better."
    ]
    
    for text in sample_texts:
        sentiment, score = analyzer.analyze_sentiment_distilbert(text)
        print(f"Text: {text}")
        print(f"Sentiment: {sentiment}, Score: {score:.3f}\n")