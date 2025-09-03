def calculate_median(numbers):
    """Calculate the median of a list of numbers."""
    if not numbers:
        return 0.0

    if not isinstance(numbers, (list, tuple)):
        return float(numbers)

    try:
        sorted_numbers = sorted(numbers)
        n = len(sorted_numbers)

        if n % 2 == 0:
            # Even number of elements
            mid1 = sorted_numbers[n // 2 - 1]
            mid2 = sorted_numbers[n // 2]
            median = (mid1 + mid2) / 2
        else:
            # Odd number of elements
            median = sorted_numbers[n // 2]

        return float(median)
    except (TypeError, ValueError, IndexError):
        return 0.0
