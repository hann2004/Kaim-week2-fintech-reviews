"""
Insights and Recommendations Analyzer
Task 4: Business insights generation

Analyzes sentiment and thematic data to generate actionable business insights
and recommendations for bank app improvements.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import json
import os

class InsightsAnalyzer:
    """Analyzes data to generate business insights and recommendations"""
    
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
        
    def load_data(self) -> bool:
        """Load processed data"""
        try:
            self.df = pd.read_csv(self.data_path)
            print(f"Loaded {len(self.df)} reviews for insights analysis")
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def analyze_sentiment_by_bank(self) -> Dict:
        """Analyze sentiment patterns by bank"""
        sentiment_analysis = {}
        
        for bank in self.df['bank'].unique():
            bank_data = self.df[self.df['bank'] == bank]
            
            sentiment_analysis[bank] = {
                'total_reviews': len(bank_data),
                'avg_rating': bank_data['rating'].mean(),
                'positive_pct': (bank_data['sentiment_label'] == 'POSITIVE').mean() * 100,
                'avg_sentiment_score': bank_data['sentiment_score'].mean(),
                'rating_distribution': bank_data['rating'].value_counts().to_dict()
            }
        
        return sentiment_analysis
    
    def analyze_themes_by_bank(self) -> Dict:
        """Analyze thematic patterns by bank"""
        theme_analysis = {}
        
        for bank in self.df['bank'].unique():
            bank_data = self.df[self.df['bank'] == bank]
            
            # Extract themes from identified_themes column
            all_themes = []
            for themes in bank_data['identified_themes'].dropna():
                theme_list = [t.strip() for t in str(themes).split(',') if t.strip() != 'No themes']
                all_themes.extend(theme_list)
            
            theme_counts = pd.Series(all_themes).value_counts()
            
            theme_analysis[bank] = {
                'total_theme_mentions': len(all_themes),
                'unique_themes': len(theme_counts),
                'top_themes': theme_counts.head(5).to_dict()
            }
        
        return theme_analysis
    
    def identify_pain_points(self) -> Dict:
        """Identify key pain points for each bank"""
        pain_points = {}
        
        for bank in self.df['bank'].unique():
            bank_data = self.df[self.df['bank'] == bank]
            
            # Focus on negative reviews for pain points
            negative_reviews = bank_data[bank_data['sentiment_label'] == 'NEGATIVE']
            
            if len(negative_reviews) > 0:
                # Analyze themes in negative reviews
                negative_themes = []
                for themes in negative_reviews['identified_themes'].dropna():
                    theme_list = [t.strip() for t in str(themes).split(',') if t.strip() != 'No themes']
                    negative_themes.extend(theme_list)
                
                theme_counts = pd.Series(negative_themes).value_counts()
                
                pain_points[bank] = {
                    'negative_review_count': len(negative_reviews),
                    'negative_percentage': (len(negative_reviews) / len(bank_data)) * 100,
                    'top_pain_points': theme_counts.head(3).to_dict(),
                    'avg_rating_negative': negative_reviews['rating'].mean()
                }
            else:
                pain_points[bank] = {
                    'negative_review_count': 0,
                    'negative_percentage': 0,
                    'top_pain_points': {},
                    'avg_rating_negative': None
                }
        
        return pain_points
    
    def identify_drivers(self) -> Dict:
        """Identify key satisfaction drivers for each bank"""
        drivers = {}
        
        for bank in self.df['bank'].unique():
            bank_data = self.df[self.df['bank'] == bank]
            
            # Focus on positive reviews for drivers
            positive_reviews = bank_data[bank_data['sentiment_label'] == 'POSITIVE']
            
            if len(positive_reviews) > 0:
                # Analyze themes in positive reviews
                positive_themes = []
                for themes in positive_reviews['identified_themes'].dropna():
                    theme_list = [t.strip() for t in str(themes).split(',') if t.strip() != 'No themes']
                    positive_themes.extend(theme_list)
                
                theme_counts = pd.Series(positive_themes).value_counts()
                
                drivers[bank] = {
                    'positive_review_count': len(positive_reviews),
                    'positive_percentage': (len(positive_reviews) / len(bank_data)) * 100,
                    'top_drivers': theme_counts.head(3).to_dict(),
                    'avg_rating_positive': positive_reviews['rating'].mean()
                }
            else:
                drivers[bank] = {
                    'positive_review_count': 0,
                    'positive_percentage': 0,
                    'top_drivers': {},
                    'avg_rating_positive': None
                }
        
        return drivers
    
    def generate_recommendations(self) -> Dict:
        """Generate actionable recommendations for each bank"""
        recommendations = {}
        
        sentiment_analysis = self.analyze_sentiment_by_bank()
        pain_points = self.identify_pain_points()
        drivers = self.identify_drivers()
        
        for bank in self.df['bank'].unique():
            bank_recs = []
            
            # Generate recommendations based on pain points
            if bank in pain_points and pain_points[bank]['top_pain_points']:
                for theme, count in pain_points[bank]['top_pain_points'].items():
                    if theme == 'TRANSACTIONS':
                        bank_recs.append({
                            'priority': 'HIGH',
                            'area': 'Transactions',
                            'recommendation': 'Optimize transaction processing speed and reliability',
                            'rationale': f'{count} negative reviews mention transaction issues'
                        })
                    elif theme == 'APP_PERFORMANCE':
                        bank_recs.append({
                            'priority': 'HIGH',
                            'area': 'App Performance',
                            'recommendation': 'Improve app loading times and reduce crashes',
                            'rationale': f'{count} negative reviews mention performance issues'
                        })
                    elif theme == 'RELIABILITY_ISSUES':
                        bank_recs.append({
                            'priority': 'HIGH',
                            'area': 'Reliability',
                            'recommendation': 'Address app crashes and error messages',
                            'rationale': f'{count} negative reviews mention reliability problems'
                        })
            
            # Generate recommendations based on strengths
            if bank in drivers and drivers[bank]['top_drivers']:
                for theme, count in drivers[bank]['top_drivers'].items():
                    if theme == 'APP_PERFORMANCE':
                        bank_recs.append({
                            'priority': 'MEDIUM',
                            'area': 'Performance Maintenance',
                            'recommendation': 'Continue optimizing app performance as it is a key strength',
                            'rationale': f'{count} positive reviews highlight good performance'
                        })
            
            recommendations[bank] = bank_recs
        
        return recommendations
    
    def generate_insights_report(self) -> Dict:
        """Generate comprehensive insights report"""
        if self.df is None:
            if not self.load_data():
                return {}
        
        report = {
            'summary_statistics': {
                'total_reviews': len(self.df),
                'banks_analyzed': self.df['bank'].nunique(),
                'overall_positive_pct': (self.df['sentiment_label'] == 'POSITIVE').mean() * 100,
                'overall_avg_rating': self.df['rating'].mean()
            },
            'sentiment_analysis': self.analyze_sentiment_by_bank(),
            'theme_analysis': self.analyze_themes_by_bank(),
            'pain_points': self.identify_pain_points(),
            'drivers': self.identify_drivers(),
            'recommendations': self.generate_recommendations(),
            'ethical_considerations': self.identify_ethical_considerations()
        }
        
        return report
    
    def identify_ethical_considerations(self) -> List[str]:
        """Identify potential ethical considerations and biases"""
        considerations = []
        
        # Check for review bias
        negative_pct = (self.df['sentiment_label'] == 'NEGATIVE').mean() * 100
        if negative_pct > 70:
            considerations.append(f"High negative bias: {negative_pct:.1f}% of reviews are negative. Users more likely to review when dissatisfied.")
        
        # Check rating distribution
        rating_dist = self.df['rating'].value_counts(normalize=True)
        if rating_dist.get(1, 0) > 0.4 or rating_dist.get(5, 0) > 0.4:
            considerations.append("Polarized ratings: Many 1-star and 5-star reviews suggest emotional rather than balanced feedback.")
        
        # Check sample representativeness
        reviews_per_bank = self.df['bank'].value_counts()
        if reviews_per_bank.std() / reviews_per_bank.mean() > 0.3:
            considerations.append("Uneven sample sizes across banks may affect comparative analysis.")
        
        return considerations
    
    def save_report(self, report: Dict, output_path: str = None):
        """Save insights report to JSON file"""
        if output_path is None:
            output_path = "data/processed/insights_report.json"
        
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"Insights report saved to {output_path}")
            return True
        except Exception as e:
            print(f"Error saving report: {e}")
            return False

def main():
    """Main execution function"""
    analyzer = InsightsAnalyzer()
    
    if analyzer.load_data():
        report = analyzer.generate_insights_report()
        
        if report:
            # Save report
            analyzer.save_report(report)
            
            # Print summary
            print("\n" + "="*60)
            print("INSIGHTS ANALYSIS SUMMARY")
            print("="*60)
            
            print(f"\nTotal reviews analyzed: {report['summary_statistics']['total_reviews']}")
            print(f"Overall positive reviews: {report['summary_statistics']['overall_positive_pct']:.1f}%")
            
            print("\nKey Findings by Bank:")
            for bank in report['sentiment_analysis']:
                print(f"\n{bank}:")
                print(f"  Average rating: {report['sentiment_analysis'][bank]['avg_rating']:.2f}")
                print(f"  Positive reviews: {report['sentiment_analysis'][bank]['positive_pct']:.1f}%")
            
            print("\nAnalysis complete. Report saved to data/processed/insights_report.json")
            
        else:
            print("Failed to generate insights report")
    else:
        print("Failed to load data for insights analysis")

if __name__ == "__main__":
    main()