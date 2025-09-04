def extract_urls(input_data=None):
    """
    Extract all URLs from input text.
    Returns list of unique URLs found.
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

        # URL regex pattern
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'

        # Find all URLs
        urls = re.findall(url_pattern, text)

        # Return unique URLs
        return list(set(urls))

    except Exception:
        return []
