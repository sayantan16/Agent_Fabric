"""
Test dynamic agent creation and immediate usage
File: test_dynamic_creation_step2.py
"""

import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.simplified_orchestrator import SimplifiedOrchestrator
from core.registry_singleton import get_shared_registry


async def test_dynamic_creation():
    print("TESTING DYNAMIC AGENT CREATION - STEP 2")
    print("=" * 60)

    # Check initial agent count
    registry = get_shared_registry()
    initial_count = len(registry.agents.get("agents", {}))
    print(f"Initial agent count: {initial_count}")

    orchestrator = SimplifiedOrchestrator()

    # Test case that should create a new agent
    test_request = (
        "Generate QR codes for these URLs: https://example.com, https://test.org"
    )

    print(f"\nTest Request: {test_request}")
    print("-" * 50)

    result = await orchestrator.process_request(test_request, auto_create=True)

    print(f"\nResults:")
    print(f"Status: {result['status']}")
    print(f"Workflow Type: {result.get('metadata', {}).get('workflow_type')}")

    if result["status"] == "success":
        print(f"Response: {result['response'][:200]}...")
    else:
        print(f"Error: {result.get('error')}")

    # Check if new agents were created
    from core.registry_singleton import force_global_reload

    force_global_reload()
    registry = get_shared_registry()
    final_count = len(registry.agents.get("agents", {}))

    print(f"\nAgent Count Changes:")
    print(f"Initial: {initial_count}")
    print(f"Final: {final_count}")
    print(f"New agents created: {final_count - initial_count}")

    if final_count > initial_count:
        print("✅ SUCCESS: New agents were created!")

        # List the new agents
        all_agents = list(registry.agents.get("agents", {}).keys())
        print(f"All agents now: {all_agents}")
    else:
        print("❌ No new agents were created")


if __name__ == "__main__":
    asyncio.run(test_dynamic_creation())
