"""Initialize missing prebuilt components."""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.registry import RegistryManager
from core.tool_factory import ToolFactory


def initialize_prebuilt_tools():
    """Create missing prebuilt tools."""

    registry = RegistryManager()
    tool_factory = ToolFactory()

    # Define essential tools
    essential_tools = [
        ("extract_urls", "Extract URLs from text"),
        ("extract_emails", "Extract email addresses from text"),
        ("extract_phones", "Extract phone numbers from text"),
        ("calculate_mean", "Calculate mean of numbers"),
        ("calculate_median", "Calculate median of numbers"),
        ("calculate_std", "Calculate standard deviation"),
        ("analyze_sentiment", "Analyze sentiment of text"),
    ]

    for tool_name, description in essential_tools:
        if not registry.tool_exists(tool_name):
            print(f"Creating tool: {tool_name}")
            result = tool_factory.ensure_tool(tool_name, description)
            print(f"  Result: {result['status']}")
        else:
            print(f"Tool exists: {tool_name}")


if __name__ == "__main__":
    initialize_prebuilt_tools()
