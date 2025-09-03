"""
Register File Reader Tools
Registers the essential file reading tools in the registry
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.registry import RegistryManager


def register_file_readers():
    """Register all file reader tools."""
    registry = RegistryManager()

    print("\n" + "=" * 50)
    print("REGISTERING FILE READER TOOLS")
    print("=" * 50)

    # Read the actual code from files
    tools_to_register = [
        {
            "name": "read_pdf",
            "description": "Extracts text content from PDF files using PyPDF2",
            "tags": ["file-reader", "pdf", "text-extraction"],
        },
        {
            "name": "read_csv",
            "description": "Reads CSV files into structured data using pandas",
            "tags": ["file-reader", "csv", "data-processing"],
        },
        {
            "name": "read_json",
            "description": "Parses JSON files into Python objects",
            "tags": ["file-reader", "json", "data-processing"],
        },
        {
            "name": "read_text",
            "description": "Reads plain text files",
            "tags": ["file-reader", "text", "basic-io"],
        },
    ]

    for tool_info in tools_to_register:
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
        else:
            print(f"File not found: {file_path}")
            print(f"   Please create the file first before running this script")

    # Display registry statistics
    print("\nUpdated Registry Statistics:")
    stats = registry.get_statistics()
    print(f"  Total tools: {stats['total_tools']}")
    print(f"  Average tool lines: {stats['avg_tool_lines']}")

    # List all file readers
    print("\nFile Readers Registered:")
    file_readers = registry.list_tools(tags=["file-reader"])
    for reader in file_readers:
        print(f"  - {reader['name']}: {reader['description']}")
        print(f"    Location: {reader['location']}")
        print(f"    Lines: {reader['line_count']}")

    print("\nFile reader registration complete!")


if __name__ == "__main__":
    register_file_readers()
