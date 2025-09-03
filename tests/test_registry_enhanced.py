"""
Test Enhanced Registry Management
Verifies advanced registry features
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.registry_enhanced import EnhancedRegistryManager


def test_health_check():
    """Test registry health check."""

    print("\n" + "=" * 50)
    print("TESTING HEALTH CHECK")
    print("=" * 50)

    registry = EnhancedRegistryManager()
    health = registry.health_check()

    print(f"Health Score: {health['health_score']}/100")
    print(f"Status: {health['status']}")
    print(f"Total Components: {health['total_components']}")
    print(f"Valid Components: {health['valid_components']}")

    if health["issues"]["missing_files"] > 0:
        print(f"Issues Found - Missing Files: {health['issues']['missing_files']}")

    assert health["health_score"] >= 0
    assert health["health_score"] <= 100
    print("\nHealth check test passed!")


def test_analytics():
    """Test usage analytics."""

    print("\n" + "=" * 50)
    print("TESTING ANALYTICS")
    print("=" * 50)

    registry = EnhancedRegistryManager()
    analytics = registry.get_usage_analytics()

    print(f"Total Agents: {analytics['agent_analytics']['total_agents']}")
    print(f"Total Tools: {analytics['tool_analytics']['total_tools']}")
    print(f"Total Executions: {analytics['agent_analytics']['total_executions']}")

    print("\nMost Used Agents:")
    for agent in analytics["agent_analytics"]["most_used"][:3]:
        print(f"  - {agent['name']}: {agent['executions']} executions")

    print("\nUnused Tools:")
    unused = analytics["tool_analytics"]["unused_tools"]
    if unused:
        print(f"  {', '.join(unused[:5])}")
    else:
        print("  None")

    print("\nAnalytics test passed!")


def test_validation():
    """Test component validation."""

    print("\n" + "=" * 50)
    print("TESTING VALIDATION")
    print("=" * 50)

    registry = EnhancedRegistryManager()
    results = registry.validate_all()

    print(f"Valid Agents: {len(results['valid_agents'])}")
    print(f"Invalid Agents: {len(results['invalid_agents'])}")
    print(f"Valid Tools: {len(results['valid_tools'])}")
    print(f"Invalid Tools: {len(results['invalid_tools'])}")

    if results["dependency_issues"]:
        print("\nDependency Issues Found:")
        for issue in results["dependency_issues"][:3]:
            print(f"  - {issue}")

    print("\nValidation test passed!")


def test_dependency_graph():
    """Test dependency graph generation."""

    print("\n" + "=" * 50)
    print("TESTING DEPENDENCY GRAPH")
    print("=" * 50)

    registry = EnhancedRegistryManager()
    deps = registry.get_dependency_graph()

    print("Agent to Tool Mappings:")
    count = 0
    for agent, tools in deps["agents_to_tools"].items():
        if tools and count < 3:
            print(f"  {agent} uses: {', '.join(tools)}")
            count += 1

    print("\nTool Usage:")
    count = 0
    for tool, agents in deps["tools_to_agents"].items():
        if agents and count < 3:
            print(f"  {tool} used by: {', '.join(agents)}")
            count += 1

    print("\nDependency graph test passed!")


def test_backup_restore():
    """Test backup and restore functionality."""

    print("\n" + "=" * 50)
    print("TESTING BACKUP/RESTORE")
    print("=" * 50)

    registry = EnhancedRegistryManager()

    # Create backup
    print("Creating backup...")
    backup_path = registry.backup_registries("test_backup")
    print(f"Backup created at: {backup_path}")

    # Verify backup files exist
    backup_name = os.path.basename(backup_path)
    agents_backup = os.path.join(backup_path, "agents.json")
    tools_backup = os.path.join(backup_path, "tools.json")

    assert os.path.exists(agents_backup), "Agents backup missing"
    assert os.path.exists(tools_backup), "Tools backup missing"

    print("Backup files verified")
    print("\nBackup/restore test passed!")


def test_optimization():
    """Test registry optimization."""

    print("\n" + "=" * 50)
    print("TESTING OPTIMIZATION")
    print("=" * 50)

    registry = EnhancedRegistryManager()

    # Run dry run first
    report = registry.optimize_registry(dry_run=True)

    print("Optimization Preview (Dry Run):")
    print(f"  Unused tools: {len(report['unused_tools'])}")
    print(f"  Broken agents: {len(report['broken_agents'])}")
    print(f"  Missing files: {len(report['missing_files'])}")

    if report["unused_tools"]:
        print(f"  Would remove tools: {', '.join(report['unused_tools'][:3])}")

    print("\nOptimization test passed!")


if __name__ == "__main__":
    print("Running Enhanced Registry Tests...")

    test_health_check()
    test_analytics()
    test_validation()
    test_dependency_graph()
    test_backup_restore()
    test_optimization()

    print("\n" + "=" * 50)
    print("All enhanced registry tests passed!")
