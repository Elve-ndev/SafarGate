from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def run_test():
    print("Testing /understand endpoint...")
    payload = {
        "annualized_income": 65000,
        "household_size": 2
    }
    
    response = client.post("/understand", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print("\n--- TEST SUCCESS ---")
        print(f"Math Result Comparison: {data['math_result']['comparison']}")
        print(f"Threshold: ${data['math_result']['threshold']:,.0f}")
        print(f"Rule Cited: {data['rule_cited']['rule_id']}")
        print(f"\nAI Explanation:\n{data['explanation']}")
    else:
        print(f"Test failed with status {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    run_test()
