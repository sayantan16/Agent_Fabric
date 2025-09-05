"""Test that backend fixes are working."""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.registry_singleton import get_shared_registry, force_global_reload
from core.orchestrator import Orchestrator
import asyncio


def test_registry_singleton():
    """Test registry singleton is working."""
    print("Testing registry singleton...")

    # Get multiple references
    reg1 = get_shared_registry()
    reg2 = get_shared_registry()

    # Should be same instance
    assert reg1 is reg2, "Registry singleton broken!"

    # Test force reload
    force_global_reload()
    reg3 = get_shared_registry()

    print("✓ Registry singleton working")


async def test_orchestrator_planning():
    """Test orchestrator planning."""
    print("\nTesting orchestrator planning...")

    orchestrator = Orchestrator()

    # Test simple request
    result = await orchestrator.process_request(
        user_request="Extract emails from this text: test@example.com",
        auto_create=False,
    )

    assert result["status"] == "success", f"Planning failed: {result}"
    assert len(result.get("workflow", {}).get("steps", [])) > 0, "No agents planned"

    print("✓ Orchestrator planning working")


def test_tool_quality():
    """Test tools are functional."""
    print("\nTesting tool quality...")

    from generated.tools.extract_emails import extract_emails

    # Test with various inputs
    assert extract_emails(None) == []
    assert extract_emails("test@example.com") == ["test@example.com"]
    assert len(extract_emails("a@b.com and c@d.com")) == 2

    print("✓ Tools are functional")


if __name__ == "__main__":
    test_registry_singleton()
    asyncio.run(test_orchestrator_planning())
    test_tool_quality()
    print("\n✅ All backend fixes verified!")
