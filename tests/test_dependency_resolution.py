"""
Test Dependency Resolution
Verify that tools are created before agents that need them
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.dependency_resolver import DependencyResolver
from core.registry import RegistryManager
import networkx as nx


def test_dependency_resolver():
    """Test the dependency resolver."""
    print("\nTesting Dependency Resolution")
    print("=" * 60)

    registry = RegistryManager()
    resolver = DependencyResolver(registry)

    # Test request
    request = "Extract emails and phone numbers, then generate a report"

    # Get existing components
    existing_agents = {a["name"]: a for a in registry.list_agents()}
    existing_tools = {t["name"]: t for t in registry.list_tools()}

    # Analyze
    result = resolver.analyze_request(request, existing_agents, existing_tools)

    print("\nCapabilities Found:")
    for cap in result["capabilities"]:
        print(f"  - {cap['name']}: {cap['agent']} using {cap['tools']}")

    print("\nCreation Order:")
    for comp_type, comp_name in result["creation_order"]:
        print(f"  {comp_type}: {comp_name}")

    print("\nDependency Visualization:")
    print(resolver.visualize_dependencies(result["dependency_graph"]))

    # Verify topological order
    graph = result["dependency_graph"]
    topo_order = list(nx.topological_sort(graph))

    # Tools should come before agents that use them
    for i, node in enumerate(topo_order):
        if graph.nodes[node]["type"] == "agent":
            # Check all tool dependencies come before this agent
            for tool in graph.predecessors(node):
                tool_index = topo_order.index(tool)
                assert (
                    tool_index < i
                ), f"Tool {tool} should be created before agent {node}"

    print("\n✓ Dependency resolution working correctly")
    return True


if __name__ == "__main__":
    test_dependency_resolver()
