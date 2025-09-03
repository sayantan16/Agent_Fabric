## 5.5 Test the Templates

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generated.tools.extract_numbers import extract_numbers
from generated.tools.calculate_mean import calculate_mean
from generated.tools.calculate_median import calculate_median


def test_example_tools():
    """Test the example statistical tools."""
    print("\n" + "=" * 50)
    print("TESTING EXAMPLE TEMPLATE TOOLS")
    print("=" * 50)

    # Test extract_numbers
    print("\nTesting extract_numbers...")
    test_text = "The temperature was 23.5 degrees, with a high of 28 and low of -2.5"
    numbers = extract_numbers(test_text)
    print(f"  Input: '{test_text}'")
    print(f"  Extracted: {numbers}")
    assert len(numbers) == 4, "Should extract 4 numbers"

    # Test calculate_mean
    print("\nTesting calculate_mean...")
    test_numbers = [10, 20, 30, 40, 50]
    mean = calculate_mean(test_numbers)
    print(f"  Input: {test_numbers}")
    print(f"  Mean: {mean}")
    assert mean == 30.0, "Mean should be 30.0"

    # Test calculate_median
    print("\nTesting calculate_median...")
    median = calculate_median(test_numbers)
    print(f"  Input: {test_numbers}")
    print(f"  Median: {median}")
    assert median == 30.0, "Median should be 30.0"

    # Test with odd number of elements
    odd_numbers = [1, 3, 5, 7, 9]
    median_odd = calculate_median(odd_numbers)
    print(f"  Odd list: {odd_numbers}")
    print(f"  Median: {median_odd}")
    assert median_odd == 5.0, "Median should be 5.0"

    # Test edge cases
    print("\nTesting edge cases...")
    print(f"  Empty list mean: {calculate_mean([])}")
    print(f"  Empty list median: {calculate_median([])}")
    print(f"  Single value: {calculate_mean([42])}")

    print("\nAll template tool tests passed!")


if __name__ == "__main__":
    test_example_tools()
