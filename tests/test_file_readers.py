"""
Test File Reader Tools
Verifies that all file reader tools work correctly
"""

import sys
import os
import json
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generated.tools.read_pdf import read_pdf
from generated.tools.read_csv import read_csv
from generated.tools.read_json import read_json
from generated.tools.read_text import read_text


def create_test_files():
    """Create test files for verification."""
    test_dir = "tests/test_files"
    os.makedirs(test_dir, exist_ok=True)

    # Create test text file
    with open(f"{test_dir}/test.txt", "w") as f:
        f.write(
            "This is a test file.\nIt has multiple lines.\nFor testing the text reader."
        )

    # Create test JSON file
    test_data = {
        "name": "Test Document",
        "type": "json",
        "items": [1, 2, 3],
        "metadata": {"created": "2024-01-01"},
    }
    with open(f"{test_dir}/test.json", "w") as f:
        json.dump(test_data, f, indent=2)

    # Create test CSV file
    df = pd.DataFrame(
        {
            "name": ["Alice", "Bob", "Charlie"],
            "age": [25, 30, 35],
            "city": ["NYC", "LA", "Chicago"],
        }
    )
    df.to_csv(f"{test_dir}/test.csv", index=False)

    print("Test files created in tests/test_files/")
    return test_dir


def test_readers():
    """Test all file reader tools."""
    print("\n" + "=" * 50)
    print("TESTING FILE READER TOOLS")
    print("=" * 50)

    # Create test files
    test_dir = create_test_files()

    # Test text reader
    print("\nTesting read_text...")
    result = read_text(f"{test_dir}/test.txt")
    if result["status"] == "success":
        print(f"Read {result['lines']} lines, {result['chars']} characters")
    else:
        print(f"Error: {result['error']}")

    # Test JSON reader
    print("\nTesting read_json...")
    result = read_json(f"{test_dir}/test.json")
    if result["status"] == "success":
        print(f"Parsed {result['type']} with keys: {list(result['data'].keys())}")
    else:
        print(f"Error: {result['error']}")

    # Test CSV reader
    print("\nTesting read_csv...")
    result = read_csv(f"{test_dir}/test.csv")
    if result["status"] == "success":
        print(
            f"Read {result['shape']['rows']} rows, {result['shape']['columns']} columns"
        )
        print(f"     Columns: {result['columns']}")
    else:
        print(f"Error: {result['error']}")

    # Test with non-existent file
    print("\nTesting error handling...")
    result = read_text("non_existent_file.txt")
    if result["status"] == "error":
        print(f"Correctly handled missing file")

    print("\nAll file reader tests complete!")


if __name__ == "__main__":
    test_readers()
