"""
Regenerate Agents with Improved Data Handling
"""

import sys
import os
import shutil

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.agent_factory import AgentFactory
from core.registry import RegistryManager


def cleanup_and_regenerate():
    """Remove problematic agents and regenerate with better prompts."""

    print("AGENT REGENERATION PROCESS")
    print("=" * 50)

    registry = RegistryManager()
    factory = AgentFactory()

    # Agents to regenerate for better data handling
    agents_to_regenerate = [
        {
            "name": "text_analyzer",
            "description": "Analyze text to extract emails and numbers, handling various input formats",
            "tools": ["extract_emails", "extract_numbers"],
            "input": "Text data from state in any format (string, dict with text field, etc.)",
            "output": "Dictionary with extracted emails and numbers arrays",
        },
        {
            "name": "statistics_calculator",
            "description": "Calculate statistics from numbers, accepting both raw text and pre-extracted number arrays",
            "tools": ["extract_numbers", "calculate_mean", "calculate_median"],
            "input": "Either raw text to extract numbers from, or pre-extracted numbers array from previous agent",
            "output": "Dictionary with calculated statistics including mean, median, min, max",
        },
    ]

    print("\n1. Backing up current agents...")
    os.makedirs("generated/agents_backup", exist_ok=True)

    for agent_info in agents_to_regenerate:
        agent_name = agent_info["name"]
        agent_file = f"generated/agents/{agent_name}_agent.py"

        if os.path.exists(agent_file):
            backup_file = f"generated/agents_backup/{agent_name}_agent.py"
            shutil.copy(agent_file, backup_file)
            print(f"  Backed up: {agent_name}")

    print("\n2. Removing agents from registry...")

    for agent_info in agents_to_regenerate:
        agent_name = agent_info["name"]
        if registry.agent_exists(agent_name):
            # Remove from registry
            del registry.agents["agents"][agent_name]
            print(f"  Removed from registry: {agent_name}")

    registry.save_all()

    print("\n3. Regenerating agents with improved data handling...")
    print("This will use Claude API credits.")
    confirm = input("Continue? (y/n): ").lower()

    if confirm != "y":
        print("Cancelled.")
        return

    for agent_info in agents_to_regenerate:
        print(f"\nRegenerating: {agent_info['name']}")

        result = factory.create_agent(
            agent_name=agent_info["name"],
            description=agent_info["description"],
            required_tools=agent_info["tools"],
            input_description=agent_info["input"],
            output_description=agent_info["output"],
            workflow_steps=[
                "Check multiple possible input locations in state",
                "Handle both raw and pre-processed data",
                "Process data with appropriate tools",
                "Format output consistently",
                "Update state for next agent",
            ],
        )

        if result["status"] == "success":
            print(
                f"  Success: {agent_info['name']} regenerated ({result['line_count']} lines)"
            )
        else:
            print(f"  Failed: {result.get('message')}")

    print("\n4. Testing regenerated agents...")

    from tests.test_end_to_end import test_multi_agent_workflows

    test_multi_agent_workflows()

    print("\nRegeneration complete!")


if __name__ == "__main__":
    cleanup_and_regenerate()
