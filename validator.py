from datetime import datetime

def validate_date(date_text):
    try:
        # Try parsing different date formats
        for fmt in ("%b %d, %Y", "%d-%m-%Y", "%d/%m/%Y"):
            try:
                parsed_date = datetime.strptime(date_text, fmt)
                if parsed_date > datetime.now():
                    return False, "Date is in the future"
                return True, "Valid Date"
            except ValueError:
                continue
        return False, "Invalid Date Format"
    except:
        return False, "Invalid Date"

def validate_amount(amount_text):
    try:
        amount = float(amount_text.replace(",", ""))
        if amount <= 0:
            return False, "Amount must be greater than 0"
        return True, "Valid Amount"
    except:
        return False, "Invalid Amount"
