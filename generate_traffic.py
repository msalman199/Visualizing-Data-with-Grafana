import requests
import time
import random
import threading
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "http://localhost:8080"

def make_request(endpoint):
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
        print(f"Request to {endpoint}: {response.status_code}")
        return response.status_code
    except Exception as e:
        print(f"Error requesting {endpoint}: {e}")
        return None

def generate_traffic():
    endpoints = [
        "/",
        "/api/users", 
        "/api/slow",
        "/health"
    ]
    
    while True:
        endpoint = random.choice(endpoints)
        make_request(endpoint)
        time.sleep(random.uniform(0.5, 2.0))

def run_load_test():
    print("Starting traffic generation...")
    
    # Create multiple threads to simulate concurrent users
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for i in range(3):
            future = executor.submit(generate_traffic)
            futures.append(future)
        
        try:
            # Run for a while
            time.sleep(300)  # Run for 5 minutes
        except KeyboardInterrupt:
            print("Stopping traffic generation...")

if __name__ == "__main__":
    run_load_test()
