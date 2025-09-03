"""
Test Workflow Engine
Verifies that the workflow engine can execute multi-agent workflows
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.workflow_engine import WorkflowEngine, WorkflowState
from core.registry import RegistryManager


def test_workflow_creation():
    """Test creating workflows from agent sequences."""

    print("\n" + "=" * 50)
    print("TESTING WORKFLOW CREATION")
    print("=" * 50)

    engine = WorkflowEngine()
    registry = RegistryManager()

    # Test 1: Create simple single-agent workflow
    print("\nTest 1: Single-agent workflow...")

    try:
        workflow = engine.create_workflow(["email_extractor"])
        print("  Success: Created workflow with email_extractor")
    except Exception as e:
        print(f"  Error: {str(e)}")

    # Test 2: Create multi-agent workflow
    print("\nTest 2: Multi-agent workflow...")

    # Check which agents exist
    available_agents = [a["name"] for a in registry.list_agents()]
    print(f"  Available agents: {available_agents}")

    if (
        "text_analyzer" in available_agents
        and "statistics_calculator" in available_agents
    ):
        try:
            workflow = engine.create_workflow(
                ["text_analyzer", "statistics_calculator"]
            )
            print(
                "  Success: Created workflow with text_analyzer -> statistics_calculator"
            )
        except Exception as e:
            print(f"  Error: {str(e)}")
    else:
        print("  Skipping: Required agents not available")

    # Test 3: Invalid workflow (non-existent agent)
    print("\nTest 3: Invalid workflow...")

    try:
        workflow = engine.create_workflow(["non_existent_agent"])
        print("  Error: Should have failed with missing agent")
    except ValueError as e:
        print(f"  Success: Correctly rejected - {str(e)}")

    print("\nWorkflow creation tests complete!")


def test_workflow_execution():
    """Test executing workflows with real agents."""

    print("\n" + "=" * 50)
    print("TESTING WORKFLOW EXECUTION")
    print("=" * 50)

    engine = WorkflowEngine()
    registry = RegistryManager()

    # Test 1: Execute email extraction workflow
    print("\nTest 1: Email extraction workflow...")

    test_data = {
        "text": "Contact us at support@example.com or sales@company.org for more information.",
        "request": "Extract emails from text",
    }

    if registry.agent_exists("email_extractor"):
        try:
            result = engine.create_and_execute(
                agent_sequence=["email_extractor"], initial_data=test_data
            )

            print("  Execution completed!")
            print(f"  Execution path: {result.get('execution_path', [])}")

            if "email_extractor" in result.get("results", {}):
                agent_result = result["results"]["email_extractor"]
                if "data" in agent_result:
                    print(f"  Found emails: {agent_result['data'].get('emails', [])}")

            if result.get("errors"):
                print(f"  Errors: {result['errors']}")

        except Exception as e:
            print(f"  Error: {str(e)}")
    else:
        print("  Skipping: email_extractor not available")

    # Test 2: Execute multi-agent workflow
    print("\nTest 2: Text analysis pipeline...")

    test_data = {
        "text": "The temperature is 23.5 degrees. Contact admin@site.com for details. Visit https://example.com",
        "request": "Analyze text comprehensively",
    }

    # Try to use available agents
    if registry.agent_exists("text_analyzer"):
        try:
            result = engine.create_and_execute(
                agent_sequence=["text_analyzer"], initial_data=test_data
            )

            print("  Execution completed!")
            print(f"  Execution path: {result.get('execution_path', [])}")

            for agent_name in result.get("execution_path", []):
                if agent_name in result.get("results", {}):
                    print(
                        f"  {agent_name} status: {result['results'][agent_name].get('status')}"
                    )

        except Exception as e:
            print(f"  Error: {str(e)}")
    else:
        print("  Skipping: text_analyzer not available")

    print("\nWorkflow execution tests complete!")


def test_workflow_visualization():
    """Test workflow visualization."""

    print("\n" + "=" * 50)
    print("TESTING WORKFLOW VISUALIZATION")
    print("=" * 50)

    engine = WorkflowEngine()
    registry = RegistryManager()

    # Get available agents
    available = [a["name"] for a in registry.list_agents()][:3]  # Use first 3

    if available:
        print(f"\nVisualizing workflow with: {available}")
        visualization = engine.visualize_workflow(available)
        print(visualization)
    else:
        print("No agents available for visualization")


if __name__ == "__main__":
    # Test workflow creation
    test_workflow_creation()

    # Test workflow execution
    test_workflow_execution()

    # Test visualization
    test_workflow_visualization()

    print("\n" + "=" * 50)
    print("All workflow engine tests complete!")
