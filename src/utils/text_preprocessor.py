"""
Text Preprocessing Utilities for NLP Analysis
Professional text cleaning and preprocessing for sentiment and thematic analysis
"""

import re
import pandas as pd
import spacy
from typing import List, Tuple

class TextPreprocessor:
    """Professional text preprocessing for financial reviews"""
    
    def __init__(self):
        # Try to load spaCy model, fallback to basic processing
        try:
            self.nlp = spacy.load("en_core_web_sm")
            self.has_spacy = True
        except OSError:
            self.has_spacy = False
            print("⚠ spaCy model not found. Using basic text processing.")
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text for analysis"""
        if pd.isna(text):
            return ""
        
        text = str(text)
        
        # Basic cleaning
        text = text.lower()
        text = re.sub(r'http\S+', '', text)  # Remove URLs
        text = re.sub(r'@\w+', '', text)     # Remove mentions
        text = re.sub(r'#\w+', '', text)     # Remove hashtags
        text = re.sub(r'\d+', '', text)      # Remove numbers
        text = re.sub(r'[^\w\s]', ' ', text) # Remove punctuation
        text = re.sub(r'\s+', ' ', text)     # Remove extra whitespace
        text = text.strip()
        
        return text
    
    def tokenize_text(self, text: str) -> List[str]:
        """Tokenize text using spaCy or basic method"""
        clean_text = self.clean_text(text)
        
        if self.has_spacy:
            doc = self.nlp(clean_text)
            tokens = [token.lemma_ for token in doc 
                     if not token.is_stop and not token.is_punct and token.is_alpha]
        else:
            # Basic tokenization as fallback
            tokens = [word for word in clean_text.split() if len(word) > 2]
        
        return tokens
    
    def preprocess_dataframe(self, df: pd.DataFrame, text_column: str = 'review_cleaned') -> pd.DataFrame:
        """Preprocess entire DataFrame for NLP analysis"""
        print("Preprocessing text data for NLP analysis...")
        
        # Create processed text column
        df['processed_text'] = df[text_column].apply(self.clean_text)
        
        # Tokenize
        df['tokens'] = df['processed_text'].apply(self.tokenize_text)
        
        # Create text length features
        df['token_count'] = df['tokens'].apply(len)
        df['char_count'] = df['processed_text'].apply(len)
        
        print(f"✓ Preprocessed {len(df)} reviews")
        print(f"✓ Average tokens per review: {df['token_count'].mean():.1f}")
        
        return df

# Example usage
if __name__ == "__main__":
    preprocessor = TextPreprocessor()
    sample_text = "The app is amazing! But it crashes sometimes. "
    print(f"Original: {sample_text}")
    print(f"Cleaned: {preprocessor.clean_text(sample_text)}")
    print(f"Tokens: {preprocessor.tokenize_text(sample_text)}")