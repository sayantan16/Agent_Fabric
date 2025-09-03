"""
Test Tool Factory
Verifies that the tool factory can create new tools dynamically
"""

import sys
import os
import importlib.util

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.tool_factory import ToolFactory
from core.registry import RegistryManager


def dynamic_import_tool(tool_name):
    """Dynamically import a tool after it's created."""
    tool_path = f"generated/tools/{tool_name}.py"
    if not os.path.exists(tool_path):
        return None

    spec = importlib.util.spec_from_file_location(tool_name, tool_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, tool_name)


def test_tool_creation():
    """Test creating a new tool."""

    print("\n" + "=" * 50)
    print("TESTING TOOL FACTORY")
    print("=" * 50)

    factory = ToolFactory()
    registry = RegistryManager()

    # Test 1: Create a simple extraction tool
    print("\nTest 1: Creating extract_urls tool...")

    result = factory.create_tool(
        tool_name="extract_urls",
        description="Extract all URLs from text",
        input_description="A string containing text with URLs",
        output_description="A list of unique URLs found in the text",
        examples=[
            {
                "input": "Visit https://example.com and http://test.org",
                "output": "['https://example.com', 'http://test.org']",
            }
        ],
    )

    if result["status"] == "success":
        print(f"  Success: Created {result['line_count']} lines of code")

        # Dynamically import and test the created tool
        extract_urls = dynamic_import_tool("extract_urls")
        if extract_urls:
            test_text = "Check out https://github.com and https://google.com"
            urls = extract_urls(test_text)
            print(f"  Test run: Found {len(urls) if urls else 0} URLs")
        else:
            print("  Warning: Could not import created tool")
    else:
        print(f"  Result: {result['status']} - {result['message']}")

    # Test 2: Try to create duplicate tool
    print("\nTest 2: Attempting to create duplicate tool...")

    result = factory.create_tool(
        tool_name="extract_urls",
        description="Extract URLs again",
        input_description="Text",
        output_description="URLs",
    )

    print(f"  Result: {result['status']} - {result['message']}")

    # Test 3: Create a calculation tool
    print("\nTest 3: Creating calculate_percentage tool...")

    result = factory.create_tool(
        tool_name="calculate_percentage",
        description="Calculate percentage of a value",
        input_description="Two numbers: value and total",
        output_description="The percentage as a float",
        examples=[
            {"input": "value=25, total=100", "output": "25.0"},
            {"input": "value=7, total=50", "output": "14.0"},
        ],
    )

    if result["status"] == "success":
        print(f"  Success: Created {result['line_count']} lines of code")

        # Dynamically import and test the created tool
        calculate_percentage = dynamic_import_tool("calculate_percentage")
        if calculate_percentage:
            try:
                percentage = calculate_percentage(50, 200)
                print(f"  Test run: 50 out of 200 = {percentage}%")
            except TypeError:
                # Tool might expect different parameter format
                try:
                    percentage = calculate_percentage({"value": 50, "total": 200})
                    print(f"  Test run: 50 out of 200 = {percentage}%")
                except:
                    print("  Warning: Could not test tool with sample inputs")
        else:
            print("  Warning: Could not import created tool")
    else:
        print(f"  Result: {result['status']} - {result['message']}")

    # Display registry statistics
    print("\nRegistry Statistics:")
    stats = registry.get_statistics()
    print(f"  Total tools: {stats['total_tools']}")
    print(f"  Average tool lines: {stats['avg_tool_lines']}")

    # List newly created tools
    print("\nNewly Created Tools:")
    new_tools = ["extract_urls", "calculate_percentage"]
    for tool_name in new_tools:
        if registry.tool_exists(tool_name):
            tool = registry.get_tool(tool_name)
            print(f"  - {tool_name}: {tool['description']}")


def test_validation():
    """Test tool code validation."""

    print("\n" + "=" * 50)
    print("TESTING TOOL VALIDATION")
    print("=" * 50)

    factory = ToolFactory()

    # Test invalid code (too short)
    print("\nTesting validation with too short code...")
    short_code = "def test():\n    return 1"
    result = factory._validate_tool_code(short_code, "test")
    print(f"  Valid: {result['valid']}")
    if not result["valid"]:
        print(f"  Error: {result['error']}")

    # Test invalid code (wrong name)
    print("\nTesting validation with wrong function name...")
    wrong_name_code = "def wrong_name(x):\n" + "    " * 10 + "return x"
    result = factory._validate_tool_code(wrong_name_code, "expected_name")
    print(f"  Valid: {result['valid']}")
    if not result["valid"]:
        print(f"  Error: {result['error']}")

    # Test invalid code (contains file I/O)
    print("\nTesting validation with file I/O...")
    file_io_code = (
        """def read_file(path):
    '''Read a file.'''
    with open(path, 'r') as f:
        return f.read()
    """
        + "\n" * 20
    )  # Add lines to meet minimum
    result = factory._validate_tool_code(file_io_code, "read_file")
    print(f"  Valid: {result['valid']}")
    if not result["valid"]:
        print(f"  Error: {result['error']}")

    print("\nValidation tests complete!")


if __name__ == "__main__":
    # Run validation tests first (no API calls)
    test_validation()

    # Ask before running API tests
    print("\n" + "=" * 50)
    response = input(
        "\nRun API tests? This will use Claude API credits (y/n): "
    ).lower()

    if response == "y":
        test_tool_creation()
    else:
        print("Skipping API tests.")
