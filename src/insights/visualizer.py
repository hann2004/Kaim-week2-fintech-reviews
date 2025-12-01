"""
Data Visualizer for Insights and Recommendations
Task 4: Professional visualizations

Creates publication-quality visualizations for business insights
and stakeholder presentations.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS
from typing import Dict, List
import os

class DataVisualizer:
    """Creates professional visualizations for bank review insights"""
    
    def __init__(self, data_path: str = None):
        """
        Initialize insights analyzer
        
        Args:
            data_path: Path to processed data CSV (if None, tries default locations)
        """
        if data_path is None:
            # Try multiple possible locations
            possible_paths = [
                "data/processed/sentiment_themes_analysis.csv",
                "../data/processed/sentiment_themes_analysis.csv",
                "./data/processed/sentiment_themes_analysis.csv",
                "/home/nabi/Kaim-week2-fintech-reviews/data/processed/sentiment_themes_analysis.csv"
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    self.data_path = path
                    print(f"Found data at: {path}")
                    break
            else:
                # If none found, use first one and will error when loading
                self.data_path = possible_paths[0]
                print(f"Warning: Data file not found in common locations")
        else:
            self.data_path = data_path
        
        self.df = None
        self.insights = {}
        self.output_dir = "reports/figures"
    
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Set professional style
        plt.style.use('seaborn-v0_8-whitegrid')
        sns.set_palette("colorblind")
        
    def load_data(self) -> bool:
        """Load processed data"""
        try:
            self.df = pd.read_csv(self.data_path)
            print(f"Loaded {len(self.df)} reviews for visualization")
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def plot_sentiment_comparison(self, save: bool = True) -> plt.Figure:
        """Create sentiment comparison plot across banks"""
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # Plot 1: Sentiment distribution by bank
        sentiment_counts = pd.crosstab(self.df['bank'], self.df['sentiment_label'])
        sentiment_counts.plot(kind='bar', ax=axes[0])
        axes[0].set_title('Sentiment Distribution by Bank')
        axes[0].set_xlabel('Bank')
        axes[0].set_ylabel('Number of Reviews')
        axes[0].legend(title='Sentiment')
        axes[0].tick_params(axis='x', rotation=45)
        
        # Plot 2: Average sentiment score by bank
        avg_sentiment = self.df.groupby('bank')['sentiment_score'].mean().sort_values(ascending=False)
        colors = ['green' if x > 0.5 else 'red' if x < 0.4 else 'gray' for x in avg_sentiment.values]
        avg_sentiment.plot(kind='bar', ax=axes[1], color=colors)
        axes[1].set_title('Average Sentiment Score by Bank')
        axes[1].set_xlabel('Bank')
        axes[1].set_ylabel('Average Sentiment Score')
        axes[1].tick_params(axis='x', rotation=45)
        axes[1].axhline(y=0.5, color='black', linestyle='--', alpha=0.5, label='Neutral Threshold')
        axes[1].legend()
        
        plt.tight_layout()
        
        if save:
            output_path = os.path.join(self.output_dir, 'sentiment_comparison.png')
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Saved sentiment comparison plot to {output_path}")
        
        return fig
    
    def plot_rating_distribution(self, save: bool = True) -> plt.Figure:
        """Create rating distribution visualization"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Plot 1: Overall rating distribution
        rating_counts = self.df['rating'].value_counts().sort_index()
        axes[0,0].bar(rating_counts.index, rating_counts.values, color='steelblue')
        axes[0,0].set_title('Overall Rating Distribution')
        axes[0,0].set_xlabel('Star Rating')
        axes[0,0].set_ylabel('Number of Reviews')
        axes[0,0].set_xticks(range(1, 6))
        
        # Plot 2: Rating distribution by bank
        rating_by_bank = pd.crosstab(self.df['bank'], self.df['rating'])
        rating_by_bank.plot(kind='bar', ax=axes[0,1], stacked=True)
        axes[0,1].set_title('Rating Distribution by Bank')
        axes[0,1].set_xlabel('Bank')
        axes[0,1].set_ylabel('Number of Reviews')
        axes[0,1].tick_params(axis='x', rotation=45)
        axes[0,1].legend(title='Rating', bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # Plot 3: Average rating by bank
        avg_rating = self.df.groupby('bank')['rating'].mean().sort_values(ascending=False)
        colors = ['gold' if x > 4 else 'orange' if x > 3 else 'lightcoral' for x in avg_rating.values]
        avg_rating.plot(kind='bar', ax=axes[1,0], color=colors)
        axes[1,0].set_title('Average Rating by Bank')
        axes[1,0].set_xlabel('Bank')
        axes[1,0].set_ylabel('Average Rating (Stars)')
        axes[1,0].tick_params(axis='x', rotation=45)
        axes[1,0].set_ylim(0, 5)
        
        # Plot 4: Rating vs Sentiment correlation
        sentiment_by_rating = self.df.groupby('rating')['sentiment_score'].mean()
        axes[1,1].plot(sentiment_by_rating.index, sentiment_by_rating.values, marker='o', linewidth=2)
        axes[1,1].set_title('Average Sentiment Score by Rating')
        axes[1,1].set_xlabel('Star Rating')
        axes[1,1].set_ylabel('Average Sentiment Score')
        axes[1,1].set_xticks(range(1, 6))
        axes[1,1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save:
            output_path = os.path.join(self.output_dir, 'rating_distribution.png')
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Saved rating distribution plot to {output_path}")
        
        return fig
    
    def plot_theme_analysis(self, save: bool = True) -> plt.Figure:
        """Create theme analysis visualization"""
        # Extract themes for analysis
        theme_data = []
        for idx, row in self.df.iterrows():
            if pd.notna(row['identified_themes']):
                themes = [t.strip() for t in str(row['identified_themes']).split(',') if t.strip() != 'No themes']
                for theme in themes:
                    theme_data.append({
                        'bank': row['bank'],
                        'theme': theme,
                        'sentiment': row['sentiment_label']
                    })
        
        theme_df = pd.DataFrame(theme_data)
        
        if len(theme_df) == 0:
            print("No theme data available for visualization")
            return None
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Plot 1: Top themes across all banks
        top_themes = theme_df['theme'].value_counts().head(10)
        axes[0,0].barh(range(len(top_themes)), top_themes.values)
        axes[0,0].set_yticks(range(len(top_themes)))
        axes[0,0].set_yticklabels(top_themes.index)
        axes[0,0].set_title('Top 10 Themes Across All Banks')
        axes[0,0].set_xlabel('Number of Mentions')
        axes[0,0].invert_yaxis()
        
        # Plot 2: Themes by bank
        pivot_data = theme_df.groupby(['bank', 'theme']).size().unstack(fill_value=0)
        top_bank_themes = pivot_data.sum().nlargest(5).index
        pivot_data[top_bank_themes].plot(kind='bar', ax=axes[0,1])
        axes[0,1].set_title('Top Themes by Bank')
        axes[0,1].set_xlabel('Bank')
        axes[0,1].set_ylabel('Number of Mentions')
        axes[0,1].tick_params(axis='x', rotation=45)
        axes[0,1].legend(title='Theme', bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # Plot 3: Theme sentiment analysis
        theme_sentiment = theme_df.groupby('theme')['sentiment'].apply(
            lambda x: (x == 'POSITIVE').mean() * 100
        ).sort_values(ascending=False)
        
        top_sentiment_themes = theme_sentiment.head(8)
        colors = ['green' if x > 60 else 'orange' if x > 40 else 'red' for x in top_sentiment_themes.values]
        axes[1,0].barh(range(len(top_sentiment_themes)), top_sentiment_themes.values, color=colors)
        axes[1,0].set_yticks(range(len(top_sentiment_themes)))
        axes[1,0].set_yticklabels(top_sentiment_themes.index)
        axes[1,0].set_title('Theme Positive Sentiment Percentage')
        axes[1,0].set_xlabel('Positive Reviews (%)')
        axes[1,0].invert_yaxis()
        axes[1,0].axvline(x=50, color='black', linestyle='--', alpha=0.5)
        
        # Plot 4: Bank-specific theme distribution
        bank_theme_counts = theme_df.groupby(['bank', 'theme']).size().groupby('bank').nlargest(3).reset_index(level=0, drop=True)
        
        banks = theme_df['bank'].unique()
        for i, bank in enumerate(banks[:2]):  # Show top 2 banks
            bank_themes = bank_theme_counts[bank_theme_counts.index.get_level_values('bank') == bank]
            if len(bank_themes) > 0:
                row = i
                col = 1
                bank_themes.plot(kind='bar', ax=axes[row, col])
                axes[row, col].set_title(f'Top Themes - {bank}')
                axes[row, col].set_xlabel('Theme')
                axes[row, col].set_ylabel('Mentions')
                axes[row, col].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        if save:
            output_path = os.path.join(self.output_dir, 'theme_analysis.png')
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Saved theme analysis plot to {output_path}")
        
        return fig
    
    def create_word_cloud(self, bank: str = None, save: bool = True) -> WordCloud:
        """Create word cloud from review text"""
        if bank:
            text_data = ' '.join(self.df[self.df['bank'] == bank]['review_text'].dropna().astype(str))
            title = f'Word Cloud - {bank}'
            filename = f'wordcloud_{bank.lower().replace(" ", "_")}.png'
        else:
            text_data = ' '.join(self.df['review_text'].dropna().astype(str))
            title = 'Word Cloud - All Banks'
            filename = 'wordcloud_all_banks.png'
        
        # Add custom stopwords
        stopwords = set(STOPWORDS)
        stopwords.update(['app', 'bank', 'please', 'thank', 'thanks', 'would', 'could', 'should'])
        
        # Generate word cloud
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            stopwords=stopwords,
            max_words=100,
            contour_width=1,
            contour_color='steelblue'
        ).generate(text_data)
        
        # Plot
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(title, fontsize=16, pad=20)
        
        if save:
            output_path = os.path.join(self.output_dir, filename)
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Saved word cloud to {output_path}")
        
        return wordcloud
    
    def create_all_visualizations(self):
        """Create all required visualizations"""
        print("Creating all visualizations...")
        
        if not self.load_data():
            print("Failed to load data for visualization")
            return False
        
        try:
            # Create all visualizations
            self.plot_sentiment_comparison()
            self.plot_rating_distribution()
            self.plot_theme_analysis()
            
            # Create word clouds for each bank
            for bank in self.df['bank'].unique():
                self.create_word_cloud(bank=bank)
            
            # Create overall word cloud
            self.create_word_cloud()
            
            print("\nAll visualizations created successfully")
            print(f"Output directory: {self.output_dir}")
            return True
            
        except Exception as e:
            print(f"Error creating visualizations: {e}")
            return False

def main():
    """Main execution function"""
    visualizer = DataVisualizer()
    
    if visualizer.create_all_visualizations():
        print("\nVisualization generation completed successfully")
        print("Check the 'reports/figures' directory for output files")
    else:
        print("Visualization generation failed")

if __name__ == "__main__":
    main()