"""
Register Example Tools
Registers example statistical tools to demonstrate tool patterns
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.registry import RegistryManager


def register_example_tools():
    """Register example statistical tools."""
    registry = RegistryManager()

    print("\n" + "=" * 50)
    print("REGISTERING EXAMPLE TOOLS")
    print("=" * 50)

    # Define tools to register
    tools_to_register = [
        {
            "name": "extract_numbers",
            "description": "Extracts all numbers from text, including integers and decimals",
            "tags": ["text-processing", "extraction", "numbers"],
        },
        {
            "name": "calculate_mean",
            "description": "Calculates the arithmetic mean of a list of numbers",
            "tags": ["statistics", "math", "aggregation"],
        },
        {
            "name": "calculate_median",
            "description": "Calculates the median value of a list of numbers",
            "tags": ["statistics", "math", "aggregation"],
        },
    ]

    registered_count = 0

    for tool_info in tools_to_register:
        # Check if tool already exists
        if registry.tool_exists(tool_info["name"]):
            print(f"Tool '{tool_info['name']}' already exists, skipping...")
            continue

        # Read the code from the file
        file_path = f"generated/tools/{tool_info['name']}.py"

        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                code = f.read()

            # Register the tool
            registry.register_tool(
                name=tool_info["name"],
                description=tool_info["description"],
                code=code,
                tags=tool_info["tags"],
            )
            registered_count += 1
        else:
            print(f"File not found: {file_path}")

    # Display statistics
    print(f"\nRegistered {registered_count} new example tools")

    # List statistical tools
    print("\nStatistical Tools Available:")
    stats_tools = registry.list_tools(tags=["statistics"])
    for tool in stats_tools:
        print(f"  - {tool['name']}: {tool['description']}")

    print("\nExample tool registration complete!")


if __name__ == "__main__":
    register_example_tools()
