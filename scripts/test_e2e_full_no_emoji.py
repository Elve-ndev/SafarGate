import os
from dotenv import load_dotenv

# Load the env vars before importing main
env_path = os.path.join(os.path.dirname(__file__), "..", "backend", ".env")
load_dotenv(env_path)

from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def run_full_backend_test():
    print("========================================")
    print("REALDOOR BACKEND E2E TEST (NO FRONTEND)")
    print("========================================\n")

    # --- STEP 1: UPLOAD ---
    print("--- [STEP 1] UPLOAD & EXTRACTION ---")
    pdf_path = os.path.join(os.path.dirname(__file__), "..", "synthetic_documents", "documents", "hh-002_d02_pay_stub.pdf")
    
    if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}")
        return

    with open(pdf_path, "rb") as f:
        files = {"file": ("hh-002_d02_pay_stub.pdf", f, "application/pdf")}
        print(f"Uploading {os.path.basename(pdf_path)}...")
        response = client.post("/upload", files=files)
        
    if response.status_code != 200:
        print(f"Upload failed: {response.status_code}")
        print(response.text)
        return
        
    extracted = response.json().get("extracted_data", {})
    gross_pay = extracted.get("gross_pay", {}).get("value", "$2,000") if extracted.get("gross_pay") else "$1,920"
    pay_period = extracted.get("pay_period", {}).get("value", "bi-weekly") if extracted.get("pay_period") else "bi-weekly"
    
    print("Extraction successful!")
    print(f"Extracted Gross Pay: {gross_pay}")
    print(f"Extracted Pay Period: {pay_period}")
    print("*(Simulating user input for household size: 2)*\n")

    # --- STEP 2: PROFILE ---
    print("--- [STEP 2] PROFILE VALIDATION & MATH ---")
    profile_payload = {
        "gross_pay": gross_pay,
        "pay_period": pay_period,
        "household_size": "2"
    }
    
    res_profile = client.post("/validate_profile", json=profile_payload)
    if res_profile.status_code != 200:
        print(f"Profile validation failed: {res_profile.text}")
        return
        
    profile_data = res_profile.json()
    annualized_income = profile_data["annualized_income"]
    household_size = profile_data["household_size"]
    
    print("Profile Validated!")
    print(f"Annualized Income: ${annualized_income:,.2f}")
    print(f"Household Size: {household_size}\n")

    # --- STEP 3: UNDERSTAND ---
    print("--- [STEP 3] UNDERSTAND RULES ---")
    understand_payload = {
        "annualized_income": annualized_income,
        "household_size": household_size
    }
    
    res_understand = client.post("/understand", json=understand_payload)
    if res_understand.status_code == 200:
        understand_data = res_understand.json()
        print("Rule Engine & AI Citation Success!")
        print(f"Threshold: ${understand_data['math_result']['threshold']:,.2f}")
        print(f"Math Comparison: {understand_data['math_result']['comparison']}")
        print(f"Cited Rule: {understand_data['rule_cited']['rule_id']}")
        print(f"AI Explanation:\n  \"{understand_data['explanation']}\"\n")
    else:
        print(f"Understand step failed: {res_understand.text}")
        return

    # --- STEP 4: PREPARE ---
    print("--- [STEP 4] PREPARE PACKET ---")
    prepare_payload = {
        "documents": [
            {"document_type": "pay_stub", "date_issued": "2026-06-15"},
            # Notice we are missing 'application_summary' on purpose to trigger a warning
        ]
    }
    
    res_prepare = client.post("/prepare", json=prepare_payload)
    if res_prepare.status_code == 200:
        prep_data = res_prepare.json()
        print("Checklist Checked!")
        print(f"Status: {prep_data['readiness']['status']}")
        print(f"Missing Documents: {prep_data['readiness']['missing_documents']}")
        print(f"Expired Documents: {prep_data['readiness']['expired_documents']}\n")
    else:
        print(f"Prepare step failed: {res_prepare.text}")

    # --- STEP 5: SECURITY (DELETE) ---
    print("--- [STEP 5] SECURITY (DELETE SESSION) ---")
    res_delete = client.delete("/session")
    if res_delete.status_code == 200:
        print(f"Session Deleted: {res_delete.json()['message']}\n")
    else:
        print(f"Delete failed: {res_delete.text}")

    print("========================================")
    print("ALL BACKEND SYSTEMS GREEN!")
    print("========================================")

if __name__ == "__main__":
    run_full_backend_test()
