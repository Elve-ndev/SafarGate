from typing import List, Dict, Any
from datetime import datetime, timedelta

REQUIRED_DOCUMENTS = [
    "application_summary",
    "pay_stub"
]

def check_packet_readiness(uploaded_docs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Evaluates the application packet against a checklist.
    Checks for missing documents and expired documents.
    """
    present_types = [doc.get("document_type") for doc in uploaded_docs]
    missing_docs = []
    
    for req in REQUIRED_DOCUMENTS:
        if req not in present_types:
            missing_docs.append(req)
            
    expired_docs = []
    warnings = []
    
    today = datetime.now()
    
    for doc in uploaded_docs:
        doc_type = doc.get("document_type")
        date_issued_str = doc.get("date_issued")
        
        if date_issued_str:
            try:
                # Try parsing common formats
                date_issued = datetime.strptime(date_issued_str, "%Y-%m-%d")
                # Check if older than 12 months (roughly 365 days)
                if (today - date_issued).days > 365:
                    expired_docs.append(f"{doc_type} is expired (older than 12 months).")
            except ValueError:
                warnings.append(f"Could not verify date for {doc_type}: {date_issued_str}")
                
    status = "READY" if not missing_docs and not expired_docs else "NEEDS_REVIEW"
    
    return {
        "status": status,
        "missing_documents": missing_docs,
        "expired_documents": expired_docs,
        "warnings": warnings,
        "message": "Your packet is ready to be downloaded!" if status == "READY" else "There are issues with your application packet."
    }
