"""
Complete Flow Test - Validates entire system
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.orchestrator import Orchestrator


def test_complete_dynamic_flow():
    """Test the complete dynamic flow."""

    orchestrator = Orchestrator()

    # Test 1: Simple request with existing agents
    print("\n=== Test 1: Simple Request ===")
    result = orchestrator.process_request(
        "Extract emails from: Contact john@example.com and mary@test.org",
        auto_create=False,
    )
    assert result["status"] == "success"
    print(f"Result: {result['response'][:100]}...")

    # Test 2: Request requiring new capabilities
    print("\n=== Test 2: Dynamic Creation ===")
    result = orchestrator.process_request(
        "Calculate the fibonacci sequence up to 10 terms", auto_create=True
    )
    print(f"Status: {result['status']}")
    if result["status"] == "missing_capabilities":
        print(f"Would create: {result['missing']}")

    # Test 3: Multi-agent workflow
    print("\n=== Test 3: Multi-Agent ===")
    result = orchestrator.process_request(
        "Analyze this text and calculate statistics: The values are 10, 20, 30, 40, 50",
        auto_create=False,
    )
    print(f"Workflow: {result.get('workflow', {}).get('steps', [])}")

    # Test 4: Conditional workflow
    print("\n=== Test 4: Conditional ===")
    result = orchestrator.process_request(
        "If there are emails in this text, extract them, otherwise count the words: Hello world test",
        auto_create=True,
    )
    print(f"Status: {result['status']}")


if __name__ == "__main__":
    test_complete_dynamic_flow()
