import os
from dotenv import load_dotenv

# Load the env vars before importing main so that OpenAI clients initialize properly
env_path = os.path.join(os.path.dirname(__file__), "..", "backend", ".env")
load_dotenv(env_path)

from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def run_e2e_test():
    print("=== TESTING STEP 1: UPLOAD & EXTRACTION ===")
    pdf_path = os.path.join(os.path.dirname(__file__), "..", "synthetic_documents", "documents", "hh-001_d01_application_summary.pdf")
    
    if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}")
        return

    with open(pdf_path, "rb") as f:
        files = {"file": ("hh-001_d01_application_summary.pdf", f, "application/pdf")}
        print(f"Uploading {pdf_path}...")
        response = client.post("/upload", files=files)
        
    if response.status_code != 200:
        print(f"Upload failed: {response.status_code}")
        print(response.text)
        return
        
    data = response.json()
    extracted = data["extracted_data"]
    print("Extraction successful!")
    print(f"Annualized Income: {extracted.get('annualized_income')}")
    print(f"Household Size: {extracted.get('household_size')}")
    
    print("\n=== TESTING STEP 3: UNDERSTAND (CALCULATION & CITATION) ===")
    annualized_income = extracted.get("annualized_income")
    household_size = extracted.get("household_size")
    
    if annualized_income is None or household_size is None:
        print("Missing income or household size in extracted data. Cannot proceed.")
        return
        
    payload = {
        "annualized_income": float(annualized_income),
        "household_size": int(household_size)
    }
    
    response2 = client.post("/understand", json=payload)
    
    if response2.status_code == 200:
        data2 = response2.json()
        print("\n--- TEST SUCCESS ---")
        print(f"Math Result Comparison: {data2['math_result']['comparison']}")
        print(f"Threshold: ${data2['math_result']['threshold']:,.0f}")
        print(f"Rule Cited: {data2['rule_cited']['rule_id']}")
        print(f"\nAI Explanation:\n{data2['explanation']}")
    else:
        print(f"Test failed with status {response2.status_code}")
        print(response2.text)

if __name__ == "__main__":
    import asyncio
    run_e2e_test()
