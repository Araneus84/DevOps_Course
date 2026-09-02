import requests
import time
import sys

def test_app():
    """Simple test to check if the app is working"""
    try:
        print("Testing application...")
        
        # Try to connect to the app
        response = requests.get('http://localhost:5001', timeout=10)
        
        # Check if we get a response
        if response.status_code == 200:
            print("✅ Test passed! App is responding with status:", response.status_code)
            return True
        else:
            print("❌ Test failed! App returned status:", response.status_code)
            return False
            
    except requests.exceptions.RequestException as e:
        print("❌ Test failed! Error connecting to app:", str(e))
        return False

if __name__ == "__main__":
    # Wait a moment for the container to fully start
    time.sleep(2)
    
    if test_app():
        print("All tests passed!")
        sys.exit(0)
    else:
        print("Tests failed!")
        sys.exit(1)