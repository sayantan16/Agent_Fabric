"""
Test Orchestrator
Verifies that the GPT-4 orchestrator can plan and execute workflows
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.orchestrator import Orchestrator
from core.registry import RegistryManager


def test_workflow_planning():
    """Test workflow planning capabilities."""

    print("\n" + "=" * 50)
    print("TESTING WORKFLOW PLANNING")
    print("=" * 50)

    orchestrator = Orchestrator()

    # Test 1: Simple email extraction request
    print("\nTest 1: Email extraction request...")

    plan = orchestrator._plan_workflow(
        "Extract emails from this text: Contact support@example.com and sales@test.org"
    )

    if plan["status"] == "success":
        print(f"  Planned workflow: {' -> '.join(plan['workflow_steps'])}")
        print(f"  Reasoning: {plan.get('reasoning', 'N/A')}")
    else:
        print(f"  Error: {plan.get('message')}")

    # Test 2: Multi-step analysis request
    print("\nTest 2: Complex analysis request...")

    plan = orchestrator._plan_workflow(
        "Analyze this text to find all numbers and calculate statistics: The values are 10, 20, 30, 40, 50"
    )

    if plan["status"] == "success":
        print(f"  Planned workflow: {' -> '.join(plan['workflow_steps'])}")
        if plan.get("missing_agents"):
            print(f"  Missing agents: {plan['missing_agents']}")
    else:
        print(f"  Error: {plan.get('message')}")

    # Test 3: Request with missing capabilities
    print("\nTest 3: Request requiring non-existent capabilities...")

    plan = orchestrator._plan_workflow(
        "Translate this text to French and create a word cloud visualization"
    )

    if plan["status"] == "success":
        print(f"  Planned workflow: {' -> '.join(plan['workflow_steps'])}")
        if plan.get("missing_agents"):
            print(f"  Missing agents identified: {plan['missing_agents']}")
        if plan.get("missing_tools"):
            print(f"  Missing tools identified: {plan['missing_tools']}")
    else:
        print(f"  Error: {plan.get('message')}")


def test_end_to_end_processing():
    """Test complete request processing."""

    print("\n" + "=" * 50)
    print("TESTING END-TO-END PROCESSING")
    print("=" * 50)

    orchestrator = Orchestrator()

    # Test 1: Process a simple request
    print("\nTest 1: Simple text analysis...")

    result = orchestrator.process_request(
        "Find all emails in: Please contact john@example.com or mary@test.org for details",
        auto_create=False,
    )

    print(f"  Status: {result['status']}")
    if result["status"] == "success":
        print(f"  Workflow: {' -> '.join(result['workflow']['steps'])}")
        print(f"  Response preview: {result['response'][:200]}...")
    else:
        print(f"  Message: {result.get('message', 'N/A')}")

    # Test 2: Process request with numbers
    print("\nTest 2: Statistical analysis...")

    result = orchestrator.process_request(
        "Calculate statistics for these numbers: 15.5, 22.3, 18.9, 25.1, 30.2",
        auto_create=False,
    )

    print(f"  Status: {result['status']}")
    if result["status"] == "success":
        print(f"  Workflow: {' -> '.join(result['workflow']['steps'])}")
    elif result["status"] == "missing_capabilities":
        print(f"  Missing: {result['missing']}")


def test_result_synthesis():
    """Test result synthesis capabilities."""

    print("\n" + "=" * 50)
    print("TESTING RESULT SYNTHESIS")
    print("=" * 50)

    orchestrator = Orchestrator()

    # Mock workflow result
    mock_result = {
        "results": {
            "email_extractor": {
                "status": "success",
                "data": {"emails": ["john@example.com", "mary@test.org"], "count": 2},
            },
            "text_analyzer": {
                "status": "success",
                "data": {"numbers": [15.5, 22.3], "emails": ["john@example.com"]},
            },
        },
        "execution_path": ["email_extractor", "text_analyzer"],
        "errors": [],
    }

    mock_plan = {"workflow_steps": ["email_extractor", "text_analyzer"]}

    print("\nSynthesizing mock results...")

    synthesis = orchestrator._synthesize_results(
        "Extract emails and numbers from the text", mock_result, mock_plan
    )

    print(f"Synthesized response:")
    print(f"  {synthesis[:300]}...")


if __name__ == "__main__":
    print("\nNote: These tests will use GPT-4 API credits")
    response = input("Continue with tests? (y/n): ").lower()

    if response == "y":
        test_workflow_planning()
        test_end_to_end_processing()
        test_result_synthesis()
        print("\n" + "=" * 50)
        print("All orchestrator tests complete!")
    else:
        print("Tests cancelled")
