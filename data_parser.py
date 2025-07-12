import re

def extract_invoice_number(text):
    pattern = r"INVOICE\s*(?:#|NUMBER)?\s*[:\-]?\s*(\w+)"
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1) if match else "Not Found"

def extract_date(text):
    pattern = r"Date\s*[:\-]?\s*([A-Za-z]{3,9}\s\d{1,2},\s\d{4}|\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})"
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1) if match else "Not Found"

def extract_vendor(text):
    pattern = r"^\s*(\w+)"
    match = re.search(pattern, text)
    return match.group(1) if match else "Not Found"

def extract_total_amount(text):
    pattern = r"Total\s*[:\-]?\s*[₹$]?\s*([\d,]+\.\d{2})"
    matches = re.findall(pattern, text, re.IGNORECASE)
    return matches[0] if matches else "Not Found"
