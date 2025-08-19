from ..core.config import settings

# Minimal field extraction placeholder.
# In production, call OpenAI (if key present) or run simple heuristic parsing.

def extract_fields(ocr_text: str) -> dict:
    # If OpenAI key is provided, we could integrate here later.
    # For now, return a simple demo mapping based on naive heuristics.
    lines = [l.strip() for l in ocr_text.splitlines() if l.strip()]
    out = {}
    for line in lines:
        lower = line.lower()
        if 'name' in lower and ':' in line:
            out['student_name'] = line.split(':', 1)[1].strip()
        if 'registration' in lower and ':' in line:
            out['registration_no'] = line.split(':', 1)[1].strip()
        if 'degree' in lower and ':' in line:
            out['degree'] = line.split(':', 1)[1].strip()
        if 'date of birth' in lower and ':' in line:
            out['date_of_birth'] = line.split(':', 1)[1].strip()
        if 'year' in lower and ':' in line:
            out['year'] = line.split(':', 1)[1].strip()
        if 'class' in lower and ':' in line:
            out['classification'] = line.split(':', 1)[1].strip()
    return out or {"raw": ocr_text[:500]}

