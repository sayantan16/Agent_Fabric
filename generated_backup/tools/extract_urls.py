def extract_urls(text):
    import re
    from urllib.parse import urlparse

    if not text:
        return []

    url_pattern = r'(https?://\S+)'
    urls = re.findall(url_pattern, text)

    # Remove duplicates while preserving order
    seen = set()
    unique_urls = []
    for url in urls:
        parsed_url = urlparse(url)
        if parsed_url.netloc not in seen:
            seen.add(parsed_url.netloc)
            unique_urls.append(url)

    return unique_urls