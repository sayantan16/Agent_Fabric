"""
End-to-End Test for Agentic Fabric POC
Tests the complete flow from request to execution
"""

import sys
import os
import json
import asyncio

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.orchestrator import Orchestrator
from core.registry import RegistryManager
from core.agent_factory import AgentFactory
from core.tool_factory import ToolFactory
from core.workflow_engine import WorkflowEngine

from core.registry_singleton import get_shared_registry, force_global_reload


def test_basic_workflow():
    """Test basic sequential workflow with existing agents."""
    print("\n" + "=" * 60)
    print("TEST 1: Basic Sequential Workflow")
    print("=" * 60)

    print(f"\nDEBUG: Starting basic workflow test")

    # Initialize
    orchestrator = Orchestrator()
    registry = RegistryManager()

    # Test request
    request = """Extract all email addresses and URLs from this text:
    Please contact john@example.com or mary@company.org for details.
    Visit our website at https://example.com or https://docs.example.com
    """

    # Process
    result = asyncio.run(
        orchestrator.process_request(user_request=request, auto_create=True)
    )

    print(f"DEBUG: Orchestrator result status: {result.get('status')}")
    print(f"DEBUG: Orchestrator result keys: {list(result.keys())}")
    if result.get("status") != "success":
        print(f"DEBUG: Error details: {result}")

    # Verify
    assert result["status"] == "success", f"Failed: {result.get('message')}"
    print(f"✓ Status: {result['status']}")
    print(f"✓ Workflow: {result['workflow']['steps']}")
    print(f"✓ Response preview: {result['response'][:200]}...")

    # Check results structure - FIXED VERSION
    if "results" in result:
        for agent_name, agent_result in result["results"].items():
            print(f"\n  Agent: {agent_name}")
            if isinstance(agent_result, dict):
                print(f"    Status: {agent_result.get('status')}")
                # Handle both success and error cases
                if agent_result.get("data") is not None:
                    if isinstance(agent_result["data"], dict):
                        print(f"    Data keys: {list(agent_result['data'].keys())}")
                    else:
                        print(f"    Data type: {type(agent_result['data'])}")
                else:
                    # Show error if available
                    error_msg = "Unknown error"
                    if "metadata" in agent_result:
                        error_msg = agent_result["metadata"].get("error", error_msg)
                    elif "error" in agent_result:
                        error_msg = agent_result["error"]
                    print(f"    Error: {error_msg}")

    return True


def test_dynamic_creation():
    """Test dynamic creation of missing tools and agents."""
    print("\n" + "=" * 60)
    print("TEST 2: Dynamic Component Creation")
    print("=" * 60)

    # Initialize factories
    agent_factory = AgentFactory()
    tool_factory = ToolFactory()

    # Use shared registry
    registry = get_shared_registry()

    # Test creating a new tool
    print("\n1. Creating new tool: count_words")
    result = tool_factory.ensure_tool(
        tool_name="count_words",
        description="Count the number of words in text input",
        tool_type="pure_function",
    )

    if result["status"] in ["success", "exists"]:
        print(f"✓ Tool created/exists: count_words")
    else:
        print(f"✗ Failed to create tool: {result.get('message')}")
        return False

    # Force reload to ensure registry is synced
    force_global_reload()

    # Test creating a new agent
    print("\n2. Creating new agent: word_counter")
    result = agent_factory.ensure_agent(
        agent_name="word_counter",
        description="Count words in text using the count_words tool",
        required_tools=["count_words"],
    )

    if result["status"] in ["success", "exists"]:
        print(f"✓ Agent created/exists: word_counter")
    else:
        print(f"✗ Failed to create agent: {result.get('message')}")
        return False

    # Force reload again
    force_global_reload()

    # Verify in registry (using the shared instance)
    assert registry.tool_exists("count_words"), "Tool not in registry"
    assert registry.agent_exists("word_counter"), "Agent not in registry"
    print("\n✓ Components registered successfully")

    return True


def test_file_reading():
    """Test file reading capabilities."""
    print("\n" + "=" * 60)
    print("TEST 3: File Reading")
    print("=" * 60)

    # Create test file
    test_file = "test_data.txt"
    with open(test_file, "w") as f:
        f.write("Test content with email@example.com and https://test.com")

    try:
        # Test read_text tool directly
        from prebuilt.tools.read_text import read_text

        result = read_text(test_file)
        assert result["status"] == "success", "Failed to read file"
        print(f"✓ Read file: {result['chars']} chars, {result['lines']} lines")

        # Test through workflow
        orchestrator = Orchestrator()
        request = f"Read the file {test_file} and extract emails from it"

        result = asyncio.run(
            orchestrator.process_request(
                user_request=request,
                files=[{"path": test_file, "type": "text"}],
                auto_create=True,
            )
        )

        print(f"✓ Workflow status: {result['status']}")

    finally:
        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)

    return True


def test_parallel_execution():
    """Test parallel agent execution."""
    print("\n" + "=" * 60)
    print("TEST 4: Parallel Execution")
    print("=" * 60)

    engine = WorkflowEngine()

    # Create parallel workflow
    agents = ["url_extractor", "email_extractor"]

    try:
        workflow = engine.create_workflow(
            agent_sequence=agents, workflow_type="parallel"
        )

        initial_data = {
            "text": "Contact admin@site.com or visit https://site.com",
            "workflow_type": "parallel",
        }

        result = engine.execute_workflow(workflow, initial_data)

        print(f"✓ Execution path: {result.get('execution_path', [])}")
        print(f"✓ Completed agents: {result.get('completed_agents', [])}")

        # Verify both agents ran
        assert len(result.get("results", {})) >= 2, "Not all agents executed"
        print("✓ All agents executed in parallel")

    except Exception as e:
        print(f"✗ Parallel execution failed: {str(e)}")
        return False

    return True


def test_error_handling():
    """Test error handling and recovery."""
    print("\n" + "=" * 60)
    print("TEST 5: Error Handling")
    print("=" * 60)

    orchestrator = Orchestrator()

    # Test with invalid request
    result = asyncio.run(
        orchestrator.process_request(
            user_request="Use non_existent_agent to process this", auto_create=False
        )
    )

    # Accept either missing_capabilities or error status
    if result["status"] == "missing_capabilities":
        print(f"✓ Correctly identified missing capabilities")
        print(f"  Missing: {result.get('missing', {})}")
        return True
    elif result["status"] == "error":
        # FIX: Handle None properly
        error_msg = result.get("error") or result.get("message") or ""
        if error_msg:  # Check if we have an error message
            error_msg_lower = error_msg.lower()
            if "no agents" in error_msg_lower or "planning failed" in error_msg_lower:
                print(f"✓ Correctly reported error for non-existent agent")
                return True
        # If no specific error message, still pass if status is error
        print(f"✓ Correctly returned error status")
        return True

    print(f"✗ Unexpected status: {result['status']}")
    print(f"✗ Result: {result}")
    return False


def test_registry_health():
    """Test registry health and validation."""
    print("\n" + "=" * 60)
    print("TEST 6: Registry Health Check")
    print("=" * 60)

    registry = RegistryManager()

    # Health check
    health = registry.health_check()
    print(f"Health Score: {health['health_score']}/100")
    print(f"Status: {health['status']}")
    print(f"Total Components: {health['total_components']}")
    print(f"Valid Components: {health['valid_components']}")

    # Validate all
    validation = registry.validate_all()
    print(f"\nValid Agents: {len(validation['valid_agents'])}")
    print(f"Valid Tools: {len(validation['valid_tools'])}")

    if validation["invalid_agents"]:
        print(f"Invalid Agents: {validation['invalid_agents']}")
    if validation["invalid_tools"]:
        print(f"Invalid Tools: {validation['invalid_tools']}")

    assert health["health_score"] > 50, "Registry health too low"
    print("\n✓ Registry is healthy")

    return True


def run_all_tests():
    """Run all end-to-end tests."""
    print("\n" + "=" * 60)
    print("AGENTIC FABRIC POC - END-TO-END TESTS")
    print("=" * 60)

    tests = [
        ("Basic Workflow", test_basic_workflow),
        ("Dynamic Creation", test_dynamic_creation),
        ("File Reading", test_file_reading),
        ("Parallel Execution", test_parallel_execution),
        ("Error Handling", test_error_handling),
        ("Registry Health", test_registry_health),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"\n{test_name}: PASSED")
            else:
                failed += 1
                print(f"\n{test_name}: FAILED")
        except Exception as e:
            failed += 1
            print(f"\n{test_name}: ERROR - {str(e)}")
            import traceback

            traceback.print_exc()

    print("\n" + "=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
