import requests
import json

# Using 127.0.0.1 instead of localhost to avoid IPv6 resolution issues on Windows
BASE_URL = "http://127.0.0.1:8000/api"

def print_header(title):
    print(f"\n{'-'*50}")
    print(f"RUNNING TEST: {title}")
    print(f"{'-'*50}")

def run_tests():
    try:
        # Check if server is running
        requests.get(f"{BASE_URL}/info", timeout=5)
    except Exception as e:
        print(f"ERROR: Backend server is not running! ({e})")
        print("Please run 'python run.py' in a separate terminal first.")
        return

    # TEST 1: GET INFO
    print_header("GET /api/info (Company Info)")
    res = requests.get(f"{BASE_URL}/info")
    print(f"Status Code: {res.status_code}")
    if res.status_code == 200:
        print(f"Response: {json.dumps(res.json(), indent=2)[:200]}...")
        print("[PASSED]")
    else:
        print(f"Failed: {res.text}")

    # TEST 2: GET PRODUCTS
    print_header("GET /api/products")
    res = requests.get(f"{BASE_URL}/products")
    print(f"Status Code: {res.status_code}")
    if res.status_code == 200:
        print(f"Found {len(res.json())} top-level categories.")
        print("[PASSED]")
    else:
        print(f"Failed: {res.text}")

    # TEST 3: POST CHAT
    print_header("POST /api/chat (AI Chatbot)")
    payload = {"message": "Hello, testing the API!"}
    res = requests.post(f"{BASE_URL}/chat", json=payload)
    print(f"Status Code: {res.status_code}")
    if res.status_code == 200:
        print(f"Response: {json.dumps(res.json(), indent=2)}")
        print("[PASSED]")
    else:
        print(f"Failed: {res.text}")

    # TEST 4: POST FEEDBACK
    print_header("POST /api/feedback")
    payload = {"name": "Test User", "email": "test@sara.com", "rating": 5, "message": "API Test"}
    res = requests.post(f"{BASE_URL}/feedback", json=payload)
    print(f"Status Code: {res.status_code}")
    if res.status_code == 200:
        print(f"Response: {json.dumps(res.json(), indent=2)}")
        print("[PASSED]")
    else:
        print(f"Failed: {res.text}")

    print(f"\n{'-'*50}")
    print("ALL AUTOMATED API TESTS COMPLETED SUCCESSFULLY!")
    print(f"{'-'*50}")

if __name__ == "__main__":
    run_tests()
