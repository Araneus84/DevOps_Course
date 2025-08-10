import requests
import time

def test_app():
    """Simple test to check if the app is working"""
    try:
        # Wait a bit for the app to start
        time.sleep(5)
        
        # Try to connect to the app
        response = requests.get('http://localhost:5000')
        
        # Check if we get a response
        if response.status_code == 200:
            print("✅ App is working!")
            return True
        else:
            print("❌ App returned status:", response.status_code)
            return False
            
    except Exception as e:
        print("❌ Error testing app:", str(e))
        return False

if __name__ == "__main__":
    test_app()