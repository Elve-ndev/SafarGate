from ai.schemas import DocumentExtractionResult

def clean_extraction_result(result: DocumentExtractionResult) -> DocumentExtractionResult:
    """
    Enforces data minimization and allowlist compliance.
    Cleans the model output by zeroing out or omitting fields not strictly required.
    """
    # Minimization: applicant_name is personal data and is not used anywhere in downstream calculations or packet generation.
    # To comply with "no hidden proxies" and data minimization, we clear it to prevent tracking unused PII.
    if result.applicant_name:
        result.applicant_name = None
        
    return result
