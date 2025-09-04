def calculate_mean(input_data=None):
    """
    Calculate arithmetic mean of numbers.
    Returns mean value or 0 if no valid numbers.
    """

    if input_data is None:
        return 0

    try:
        # Handle different input types
        if isinstance(input_data, (int, float)):
            return float(input_data)
        elif isinstance(input_data, list):
            numbers = input_data
        elif isinstance(input_data, dict):
            # Try to extract numbers from dict
            if "numbers" in input_data:
                numbers = input_data["numbers"]
            elif "data" in input_data:
                numbers = input_data["data"]
            else:
                return 0
        else:
            return 0

        # Filter valid numbers
        valid_numbers = []
        for item in numbers:
            try:
                num = float(item)
                if not (num != num):  # Check for NaN
                    valid_numbers.append(num)
            except (TypeError, ValueError):
                continue

        # Calculate mean
        if valid_numbers:
            return sum(valid_numbers) / len(valid_numbers)
        else:
            return 0

    except Exception:
        return 0
