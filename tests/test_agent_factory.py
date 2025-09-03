"""
Test Agent Factory
Verifies that the agent factory can create new agents dynamically
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.agent_factory import AgentFactory
from core.registry import RegistryManager


def test_agent_creation():
    """Test creating a new agent."""

    print("\n" + "=" * 50)
    print("TESTING AGENT FACTORY")
    print("=" * 50)

    factory = AgentFactory()
    registry = RegistryManager()

    # Test 1: Create a simple text processing agent
    print("\nTest 1: Creating text_analyzer agent...")

    result = factory.create_agent(
        agent_name="text_analyzer",
        description="Analyze text to extract emails and numbers",
        required_tools=["extract_emails", "extract_numbers"],
        input_description="Text data from state containing mixed content",
        output_description="Dictionary with extracted emails and numbers",
        workflow_steps=[
            "Get text from state current_data",
            "Extract email addresses using extract_emails tool",
            "Extract numbers using extract_numbers tool",
            "Combine results into output dictionary",
            "Update state with results",
        ],
    )

    if result["status"] == "success":
        print(f"  Success: Created {result['line_count']} lines of code")
        print(f"  Agent registered: text_analyzer_agent")
    elif result["status"] == "exists":
        print(f"  Agent already exists: {result['message']}")
    else:
        print(f"  Result: {result['status']} - {result['message']}")

    # Test 2: Try to create agent with missing tool
    print("\nTest 2: Attempting to create agent with missing tool...")

    result = factory.create_agent(
        agent_name="invalid_agent",
        description="Agent that uses non-existent tool",
        required_tools=["non_existent_tool"],
        input_description="Any input",
        output_description="Any output",
    )

    print(f"  Result: {result['status']} - {result['message']}")
    if "missing_tools" in result:
        print(f"  Missing tools: {result['missing_tools']}")

    # Test 3: Create a statistics agent
    print("\nTest 3: Creating statistics_calculator agent...")

    result = factory.create_agent(
        agent_name="statistics_calculator",
        description="Calculate statistics from numbers in text",
        required_tools=["extract_numbers", "calculate_mean", "calculate_median"],
        input_description="Text containing numbers",
        output_description="Statistical analysis with mean, median, count",
        workflow_steps=[
            "Extract numbers from input text",
            "Calculate mean of the numbers",
            "Calculate median of the numbers",
            "Count total numbers found",
            "Return statistics dictionary",
        ],
    )

    if result["status"] == "success":
        print(f"  Success: Created {result['line_count']} lines of code")
    else:
        print(f"  Result: {result['status']} - {result['message']}")

    # Display registry statistics
    print("\nRegistry Statistics:")
    stats = registry.get_statistics()
    print(f"  Total agents: {stats['total_agents']}")
    print(f"  Total tools: {stats['total_tools']}")
    print(f"  Average agent lines: {stats['avg_agent_lines']}")

    # List all agents
    print("\nRegistered Agents:")
    agents = registry.list_agents()
    for agent in agents:
        print(f"  - {agent['name']}: {agent['description']}")
        print(f"    Uses tools: {agent['uses_tools']}")


def test_validation():
    """Test agent code validation."""

    print("\n" + "=" * 50)
    print("TESTING AGENT VALIDATION")
    print("=" * 50)

    factory = AgentFactory()

    # Test invalid code (missing state parameter)
    print("\nTesting validation with missing state parameter...")
    bad_code = """def test_agent():
    return {'status': 'success'}
"""
    result = factory._validate_agent_code(bad_code, "test")
    print(f"  Valid: {result['valid']}")
    if not result["valid"]:
        print(f"  Error: {result['error']}")

    # Test invalid code (missing state operations)
    print("\nTesting validation with missing state operations...")
    incomplete_code = (
        """def test_agent(state):
    '''Agent without proper state handling.'''
    result = {'status': 'success'}
    return state
"""
        + "\n" * 50
    )  # Pad to meet line requirement

    result = factory._validate_agent_code(incomplete_code, "test")
    print(f"  Valid: {result['valid']}")
    if not result["valid"]:
        print(f"  Error: {result['error']}")

    print("\nValidation tests complete!")


if __name__ == "__main__":
    # Run validation tests first
    test_validation()

    # Ask before running API tests
    print("\n" + "=" * 50)
    response = input(
        "\nRun API tests? This will use Claude API credits (y/n): "
    ).lower()

    if response == "y":
        test_agent_creation()
    else:
        print("Skipping API tests.")
