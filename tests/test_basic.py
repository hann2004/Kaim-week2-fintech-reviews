"""
Basic unit tests for the project structure and imports
"""

def test_imports():
    """Test that essential packages can be imported"""
    try:
        import pandas as pd
        from google_play_scraper import app
        import numpy as np
        assert True
    except ImportError as e:
        assert False, f"Import error: {e}"

def test_project_structure():
    """Test that essential project files exist"""
    import os
    assert os.path.exists("requirements.txt"), "requirements.txt missing"
    assert os.path.exists("README.md"), "README.md missing"
    assert os.path.exists("src/data_collection/scraper.py"), "scraper.py missing"
    assert os.path.exists("tests/test_app_ids.py"), "test_app_ids.py missing"

def test_sample_data():
    """Test that we can create sample data structures"""
    import pandas as pd
    sample_data = {
        'review': ['Great app!', 'Needs improvement'],
        'rating': [5, 2],
        'date': ['2024-01-01', '2024-01-02'],
        'bank': ['CBE', 'BOA'],
        'source': ['Google Play Store', 'Google Play Store']
    }
    df = pd.DataFrame(sample_data)
    assert len(df) == 2, "Sample DataFrame creation failed"
    assert list(df.columns) == ['review', 'rating', 'date', 'bank', 'source'], "Wrong columns"