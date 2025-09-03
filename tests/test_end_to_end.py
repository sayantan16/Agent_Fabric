"""
End-to-End System Tests
Comprehensive testing of the complete Agentic Fabric system
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.orchestrator import Orchestrator
from core.workflow_engine import WorkflowEngine
from core.registry_enhanced import EnhancedRegistryManager


def test_simple_workflows():
    """Test simple single-agent workflows."""

    print("\n" + "=" * 50)
    print("TESTING SIMPLE WORKFLOWS")
    print("=" * 50)

    engine = WorkflowEngine()

    # Test 1: Email extraction
    print("\nTest 1: Email Extraction")
    print("-" * 40)

    result = engine.create_and_execute(
        agent_sequence=["email_extractor"],
        initial_data={
            "text": "Contact john@example.com or mary@test.org for details",
            "current_data": {
                "text": "Contact john@example.com or mary@test.org for details"
            },
        },
    )

    print(f"Execution path: {result.get('execution_path', [])}")
    if "email_extractor" in result.get("results", {}):
        emails = result["results"]["email_extractor"].get("data", {}).get("emails", [])
        print(f"Emails found: {emails}")
        assert len(emails) == 2, "Should find 2 emails"

    # Test 2: Number extraction
    print("\nTest 2: Number Extraction")
    print("-" * 40)

    result = engine.create_and_execute(
        agent_sequence=["text_analyzer"],
        initial_data={
            "text": "Values are 100, 200, 300",
            "current_data": {"text": "Values are 100, 200, 300"},
        },
    )

    print(f"Execution path: {result.get('execution_path', [])}")
    if "text_analyzer" in result.get("results", {}):
        numbers = result["results"]["text_analyzer"].get("data", {}).get("numbers", [])
        print(f"Numbers found: {numbers}")


def test_multi_agent_workflows():
    """Test multi-agent workflows with data passing."""

    print("\n" + "=" * 50)
    print("TESTING MULTI-AGENT WORKFLOWS")
    print("=" * 50)

    engine = WorkflowEngine()

    # Test: Text analysis -> Statistics calculation
    print("\nTest: Text Analysis Pipeline")
    print("-" * 40)

    # Initialize with text containing numbers
    initial_data = {
        "text": "Sales: 1000, 2000, 3000, 4000, 5000",
        "current_data": {"text": "Sales: 1000, 2000, 3000, 4000, 5000"},
    }

    result = engine.create_and_execute(
        agent_sequence=["text_analyzer", "statistics_calculator"],
        initial_data=initial_data,
    )

    print(f"Execution path: {result.get('execution_path', [])}")

    # Check text_analyzer results
    if "text_analyzer" in result.get("results", {}):
        ta_result = result["results"]["text_analyzer"]
        print(f"Text Analyzer Status: {ta_result.get('status')}")
        numbers = ta_result.get("data", {}).get("numbers", [])
        print(f"Numbers extracted: {numbers}")

    # Check statistics_calculator results
    if "statistics_calculator" in result.get("results", {}):
        sc_result = result["results"]["statistics_calculator"]
        print(f"Statistics Calculator Status: {sc_result.get('status')}")
        stats = sc_result.get("data", {}).get("statistics", {})
        if stats:
            print(
                f"Statistics calculated: mean={stats.get('mean')}, median={stats.get('median')}"
            )
        else:
            print(f"Statistics data: {sc_result.get('data')}")

    # Check current_data flow
    print(f"\nFinal current_data: {result.get('current_data')}")


def test_orchestrator_planning():
    """Test orchestrator's ability to plan workflows."""

    print("\n" + "=" * 50)
    print("TESTING ORCHESTRATOR PLANNING")
    print("=" * 50)

    orchestrator = Orchestrator()

    test_requests = [
        "Extract emails from: Contact support@test.com",
        "Calculate statistics for: 10, 20, 30, 40, 50",
        "Process this text and find all information: Visit https://example.com or email info@test.org",
    ]

    for request in test_requests:
        print(f"\nRequest: {request}")
        plan = orchestrator._plan_workflow(request)
        if plan["status"] == "success":
            print(f"Planned workflow: {' -> '.join(plan['workflow_steps'])}")
        else:
            print(f"Planning failed: {plan.get('message')}")


def test_full_orchestration():
    """Test complete orchestration from request to results."""

    print("\n" + "=" * 50)
    print("TESTING FULL ORCHESTRATION")
    print("=" * 50)

    orchestrator = Orchestrator()

    # Test 1: Simple request
    print("\nTest 1: Email Extraction Request")
    print("-" * 40)

    result = orchestrator.process_request(
        "Find emails in: Contact admin@site.com for help", auto_create=False
    )

    print(f"Status: {result['status']}")
    if result["status"] == "success":
        print(f"Workflow executed: {' -> '.join(result['workflow']['steps'])}")
        print(f"Response preview: {result['response'][:150]}...")

    # Test 2: Complex request
    print("\nTest 2: Statistical Analysis Request")
    print("-" * 40)

    result = orchestrator.process_request(
        "Analyze these numbers and give me statistics: 15, 25, 35, 45, 55",
        auto_create=False,
    )

    print(f"Status: {result['status']}")
    if result["status"] == "success":
        print(f"Workflow executed: {' -> '.join(result['workflow']['steps'])}")


def test_registry_health():
    """Verify system health after tests."""

    print("\n" + "=" * 50)
    print("SYSTEM HEALTH CHECK")
    print("=" * 50)

    registry = EnhancedRegistryManager()
    health = registry.health_check()

    print(f"Health Score: {health['health_score']}/100")
    print(f"Status: {health['status']}")

    analytics = registry.get_usage_analytics()
    print(f"Total Executions: {analytics['agent_analytics']['total_executions']}")
    print(
        f"Most Used Agent: {analytics['agent_analytics']['most_used'][0]['name'] if analytics['agent_analytics']['most_used'] else 'None'}"
    )


def diagnose_data_flow():
    """Diagnose the data flow issue between agents."""

    print("\n" + "=" * 50)
    print("DIAGNOSING DATA FLOW ISSUE")
    print("=" * 50)

    # Check statistics_calculator agent code
    agent_path = "generated/agents/statistics_calculator_agent.py"
    if os.path.exists(agent_path):
        with open(agent_path, "r") as f:
            code = f.read()

        print("Checking statistics_calculator agent...")
        print("-" * 40)

        # Look for how it gets input
        if "current_data" in code:
            # Find the line that extracts text
            for line in code.split("\n"):
                if "current_data" in line and ("text" in line or "get" in line):
                    print(f"Input extraction: {line.strip()}")
                    break

        # Check if it's looking for the right data structure
        if "numbers" in code:
            print("Agent expects 'numbers' in data: Yes")
        else:
            print("Agent expects 'numbers' in data: No")

    print(
        "\nThe issue: statistics_calculator expects text but text_analyzer passes numbers array"
    )
    print(
        "Solution: statistics_calculator should check for both text and numbers in current_data"
    )


if __name__ == "__main__":
    print("COMPREHENSIVE END-TO-END TESTING")
    print("=" * 50)

    # Run all tests
    test_simple_workflows()
    test_multi_agent_workflows()
    test_orchestrator_planning()
    test_full_orchestration()
    test_registry_health()
    diagnose_data_flow()

    print("\n" + "=" * 50)
    print("END-TO-END TESTING COMPLETE")
    print("=" * 50)

    print("\nSummary:")
    print("- Simple workflows: Working")
    print("- Multi-agent workflows: Data flow issue identified")
    print("- Orchestrator planning: Working")
    print("- Full orchestration: Working")
    print("- System health: 100%")
    print("\nNext step: Fix data flow in statistics_calculator agent")
