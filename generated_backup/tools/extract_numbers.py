def extract_numbers(text):
    """Extract all numbers from text - both integers and decimals."""
    import re

    if not text:
        return []

    # Find all numeric patterns
    patterns = [
        r"-?\d+\.?\d*",  # Regular numbers (integers and decimals)
        r"-?\.\d+",  # Numbers starting with decimal point
    ]

    numbers = []
    for pattern in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            try:
                # Try to convert to float
                num = float(match)
                numbers.append(num)
            except ValueError:
                continue

    # Remove duplicates while preserving order
    seen = set()
    unique_numbers = []
    for num in numbers:
        if num not in seen:
            seen.add(num)
            unique_numbers.append(num)

    return unique_numbers
