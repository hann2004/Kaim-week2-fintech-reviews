"""
Test script to verify Google Play Store app IDs work correctly
This is a functional test, not a unit test
"""

from google_play_scraper import app

# Test app IDs for Ethiopian banks
BANK_APPS = {
    'CBE': 'com.combanketh.mobilebanking',
    'BOA': 'com.boa.boaMobileBanking', 
    'DASHEN': 'com.dashen.dashensuperapp'
}

def test_app_ids_functional():
    """Functional test to verify app IDs work before scraping"""
    print("Testing Google Play Store App IDs...")
    print("=" * 50)
    
    working_apps = 0
    
    for bank, app_id in BANK_APPS.items():
        try:
            print(f"\nTesting {bank}...")
            app_info = app(app_id)
            
            print(f"   SUCCESS: {bank}")
            print(f"   App Name: {app_info['title']}")
            print(f"   Rating: {app_info['score']} ⭐")
            print(f"   Reviews: {app_info['reviews']}")
            print(f"   Installs: {app_info['installs']}")
            
            working_apps += 1
            
        except Exception as e:
            print(f"   FAILED: {bank}")
            print(f"   Error: {e}")
            print(f"   App ID: {app_id} might be wrong")
    
    print("\n" + "=" * 50)
    print(f"Results: {working_apps}/3 apps working")
    
    if working_apps == 3:
        print("🎉 All app IDs are correct! Ready to scrape.")
        return True
    else:
        print("⚠ Some app IDs need fixing before scraping.")
        return False

if __name__ == "__main__":
    test_app_ids_functional()