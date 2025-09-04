def extract_emails(input_data=None):
    """
    Extract all email addresses from input text.
    Returns list of unique email addresses found.
    """
    import re

    if input_data is None:
        return []

    try:
        # Handle different input types
        if isinstance(input_data, str):
            text = input_data
        elif isinstance(input_data, dict):
            text = str(input_data.get("text", input_data.get("content", input_data)))
        elif isinstance(input_data, list):
            text = " ".join(str(item) for item in input_data)
        else:
            text = str(input_data)

        # Email regex pattern
        email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

        # Find all emails
        emails = re.findall(email_pattern, text)

        # Return unique emails (lowercase)
        return list(set(email.lower() for email in emails))

    except Exception:
        return []
