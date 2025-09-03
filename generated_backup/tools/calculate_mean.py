def calculate_mean(numbers):
    """Calculate the arithmetic mean of a list of numbers."""
    if not numbers:
        return 0.0

    if not isinstance(numbers, (list, tuple)):
        return float(numbers)

    try:
        total = sum(numbers)
        count = len(numbers)
        mean = total / count
        return float(mean)
    except (TypeError, ValueError, ZeroDivisionError):
        return 0.0
