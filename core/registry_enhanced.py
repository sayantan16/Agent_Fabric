"""
Enhanced Registry Manager
Advanced registry operations including validation, cleanup, and analytics
"""

import json
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import shutil

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.registry import RegistryManager


class EnhancedRegistryManager(RegistryManager):
    """Extended registry with advanced management features."""

    def __init__(
        self, agents_path: str = "agents.json", tools_path: str = "tools.json"
    ):
        super().__init__(agents_path, tools_path)
        self.backup_dir = "registry_backups"
        os.makedirs(self.backup_dir, exist_ok=True)

    # =============================================================================
    # BACKUP AND RESTORE
    # =============================================================================

    def backup_registries(self, tag: str = None) -> str:
        """
        Create backup of current registries.

        Args:
            tag: Optional tag for the backup

        Returns:
            Backup file path
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}"
        if tag:
            backup_name += f"_{tag}"

        backup_path = os.path.join(self.backup_dir, backup_name)
        os.makedirs(backup_path, exist_ok=True)

        # Copy registry files
        shutil.copy(self.agents_path, os.path.join(backup_path, "agents.json"))
        shutil.copy(self.tools_path, os.path.join(backup_path, "tools.json"))

        # Save metadata
        metadata = {
            "timestamp": datetime.now().isoformat(),
            "tag": tag,
            "stats": self.get_statistics(),
        }

        with open(os.path.join(backup_path, "metadata.json"), "w") as f:
            json.dump(metadata, f, indent=2)

        print(f"Backup created: {backup_path}")
        return backup_path

    def restore_registries(self, backup_name: str) -> bool:
        """
        Restore registries from backup.

        Args:
            backup_name: Name of backup directory

        Returns:
            Success status
        """
        backup_path = os.path.join(self.backup_dir, backup_name)

        if not os.path.exists(backup_path):
            print(f"Backup not found: {backup_path}")
            return False

        try:
            # Restore files
            shutil.copy(os.path.join(backup_path, "agents.json"), self.agents_path)
            shutil.copy(os.path.join(backup_path, "tools.json"), self.tools_path)

            # Reload registries
            self.agents = self._load_registry(self.agents_path)
            self.tools = self._load_registry(self.tools_path)

            print(f"Registries restored from: {backup_path}")
            return True

        except Exception as e:
            print(f"Restore failed: {str(e)}")
            return False

    # =============================================================================
    # VALIDATION AND HEALTH CHECKS
    # =============================================================================

    def validate_all(self) -> Dict[str, List[str]]:
        """
        Validate all agents and tools.

        Returns:
            Dict with validation results
        """
        results = {
            "valid_agents": [],
            "invalid_agents": [],
            "valid_tools": [],
            "invalid_tools": [],
            "missing_files": [],
            "dependency_issues": [],
        }

        # Validate agents
        for name, agent in self.agents.get("agents", {}).items():
            file_path = agent.get("location", "")

            if not os.path.exists(file_path):
                results["missing_files"].append(f"Agent: {name} - {file_path}")
                results["invalid_agents"].append(name)
            else:
                # Check dependencies
                missing_deps = []
                for tool in agent.get("uses_tools", []):
                    if not self.tool_exists(tool):
                        missing_deps.append(tool)

                if missing_deps:
                    results["dependency_issues"].append(
                        f"Agent '{name}' missing tools: {', '.join(missing_deps)}"
                    )
                    results["invalid_agents"].append(name)
                else:
                    results["valid_agents"].append(name)

        # Validate tools
        for name, tool in self.tools.get("tools", {}).items():
            file_path = tool.get("location", "")

            if not os.path.exists(file_path):
                results["missing_files"].append(f"Tool: {name} - {file_path}")
                results["invalid_tools"].append(name)
            else:
                results["valid_tools"].append(name)

        return results

    def health_check(self) -> Dict[str, Any]:
        """
        Perform comprehensive health check.

        Returns:
            Health status report
        """
        validation = self.validate_all()
        stats = self.get_statistics()

        # Calculate health score
        total_agents = len(self.agents.get("agents", {}))
        total_tools = len(self.tools.get("tools", {}))
        valid_agents = len(validation["valid_agents"])
        valid_tools = len(validation["valid_tools"])

        health_score = 0
        if total_agents > 0:
            health_score += (valid_agents / total_agents) * 50
        if total_tools > 0:
            health_score += (valid_tools / total_tools) * 50

        return {
            "health_score": round(health_score, 1),
            "status": (
                "healthy"
                if health_score >= 80
                else "degraded" if health_score >= 50 else "unhealthy"
            ),
            "total_components": total_agents + total_tools,
            "valid_components": valid_agents + valid_tools,
            "issues": {
                "missing_files": len(validation["missing_files"]),
                "dependency_issues": len(validation["dependency_issues"]),
                "invalid_agents": len(validation["invalid_agents"]),
                "invalid_tools": len(validation["invalid_tools"]),
            },
            "statistics": stats,
            "validation_details": validation,
        }

    # =============================================================================
    # ADVANCED ANALYTICS
    # =============================================================================

    def get_usage_analytics(self) -> Dict[str, Any]:
        """
        Get detailed usage analytics.

        Returns:
            Usage statistics and patterns
        """
        agents_list = self.agents.get("agents", {})
        tools_list = self.tools.get("tools", {})

        # Agent analytics
        most_used_agents = sorted(
            agents_list.items(),
            key=lambda x: x[1].get("execution_count", 0),
            reverse=True,
        )[:5]

        # Tool analytics
        tool_usage = {}
        for tool_name, tool_data in tools_list.items():
            usage_count = len(tool_data.get("used_by_agents", []))
            tool_usage[tool_name] = usage_count

        most_used_tools = sorted(tool_usage.items(), key=lambda x: x[1], reverse=True)[
            :5
        ]

        # Calculate averages
        total_executions = sum(
            a.get("execution_count", 0) for a in agents_list.values()
        )
        avg_execution_time = sum(
            a.get("avg_execution_time", 0) for a in agents_list.values()
        ) / max(len(agents_list), 1)

        return {
            "agent_analytics": {
                "total_agents": len(agents_list),
                "most_used": [
                    {"name": name, "executions": data.get("execution_count", 0)}
                    for name, data in most_used_agents
                ],
                "total_executions": total_executions,
                "average_execution_time": round(avg_execution_time, 2),
            },
            "tool_analytics": {
                "total_tools": len(tools_list),
                "most_reused": [
                    {"name": name, "used_by": count} for name, count in most_used_tools
                ],
                "unused_tools": [
                    name for name, count in tool_usage.items() if count == 0
                ],
            },
            "complexity_metrics": {
                "avg_agent_size": round(
                    sum(a.get("line_count", 0) for a in agents_list.values())
                    / max(len(agents_list), 1),
                    1,
                ),
                "avg_tool_size": round(
                    sum(t.get("line_count", 0) for t in tools_list.values())
                    / max(len(tools_list), 1),
                    1,
                ),
                "avg_tools_per_agent": round(
                    sum(len(a.get("uses_tools", [])) for a in agents_list.values())
                    / max(len(agents_list), 1),
                    1,
                ),
            },
        }

    # =============================================================================
    # DEPENDENCY MANAGEMENT
    # =============================================================================

    def get_dependency_graph(self) -> Dict[str, Dict[str, List[str]]]:
        """
        Build complete dependency graph.

        Returns:
            Dependency relationships
        """
        graph = {"agents_to_tools": {}, "tools_to_agents": {}, "agent_chains": {}}

        # Build agent to tool mapping
        for agent_name, agent_data in self.agents.get("agents", {}).items():
            graph["agents_to_tools"][agent_name] = agent_data.get("uses_tools", [])

        # Build tool to agent mapping
        for tool_name, tool_data in self.tools.get("tools", {}).items():
            graph["tools_to_agents"][tool_name] = tool_data.get("used_by_agents", [])

        # Identify potential agent chains (agents that could work together)
        for agent_name, agent_data in self.agents.get("agents", {}).items():
            output_schema = agent_data.get("output_schema", {})

            # Find agents that could consume this agent's output
            potential_next = []
            for other_name, other_data in self.agents.get("agents", {}).items():
                if other_name != agent_name:
                    input_schema = other_data.get("input_schema", {})
                    # Simple compatibility check
                    if self._schemas_compatible(output_schema, input_schema):
                        potential_next.append(other_name)

            if potential_next:
                graph["agent_chains"][agent_name] = potential_next

        return graph

    def _schemas_compatible(self, output_schema: Dict, input_schema: Dict) -> bool:
        """
        Check if output schema is compatible with input schema.
        Simple implementation - can be enhanced.
        """
        # Basic compatibility - if both have 'data' or 'text' fields
        output_keys = set(output_schema.keys())
        input_keys = set(input_schema.keys())

        common_keys = output_keys.intersection(input_keys)
        return len(common_keys) > 0 or "any" in input_schema.values()

    # =============================================================================
    # CLEANUP AND OPTIMIZATION
    # =============================================================================

    def optimize_registry(self, dry_run: bool = True) -> Dict[str, Any]:
        """
        Optimize registry by cleaning up unused components and fixing issues.

        Args:
            dry_run: If True, only report what would be done

        Returns:
            Optimization report
        """
        report = {
            "unused_tools": [],
            "broken_agents": [],
            "missing_files": [],
            "fixed_dependencies": [],
            "removed_components": [],
        }

        # Find unused tools
        for tool_name, tool_data in self.tools.get("tools", {}).items():
            if len(tool_data.get("used_by_agents", [])) == 0:
                report["unused_tools"].append(tool_name)
                if not dry_run:
                    # Remove tool
                    del self.tools["tools"][tool_name]
                    report["removed_components"].append(f"Tool: {tool_name}")

        # Find broken agents
        for agent_name, agent_data in self.agents.get("agents", {}).items():
            # Check file exists
            if not os.path.exists(agent_data.get("location", "")):
                report["broken_agents"].append(agent_name)
                report["missing_files"].append(agent_data.get("location", ""))
                if not dry_run:
                    # Remove agent
                    del self.agents["agents"][agent_name]
                    report["removed_components"].append(f"Agent: {agent_name}")

            # Check dependencies
            for tool in agent_data.get("uses_tools", []):
                if not self.tool_exists(tool):
                    report["fixed_dependencies"].append(
                        f"Removed missing tool '{tool}' from agent '{agent_name}'"
                    )
                    if not dry_run:
                        agent_data["uses_tools"].remove(tool)

        if not dry_run:
            self.save_all()
            report["status"] = "optimized"
        else:
            report["status"] = "dry_run"

        return report

    # =============================================================================
    # EXPORT AND IMPORT
    # =============================================================================

    def export_to_markdown(self, output_file: str = "registry_report.md") -> str:
        """
        Export registry information to markdown report.

        Args:
            output_file: Output file path

        Returns:
            Path to generated file
        """
        health = self.health_check()
        analytics = self.get_usage_analytics()
        deps = self.get_dependency_graph()

        content = []
        content.append("# Agentic Fabric Registry Report")
        content.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        content.append("")

        # Health Status
        content.append("## System Health")
        content.append(f"- **Health Score**: {health['health_score']}/100")
        content.append(f"- **Status**: {health['status'].upper()}")
        content.append(f"- **Total Components**: {health['total_components']}")
        content.append(f"- **Valid Components**: {health['valid_components']}")
        content.append("")

        # Agents
        content.append("## Registered Agents")
        for name, data in self.agents.get("agents", {}).items():
            content.append(f"### {name}")
            content.append(f"- **Description**: {data.get('description', 'N/A')}")
            content.append(f"- **Tools Used**: {', '.join(data.get('uses_tools', []))}")
            content.append(f"- **Executions**: {data.get('execution_count', 0)}")
            content.append(f"- **Lines**: {data.get('line_count', 0)}")
            content.append("")

        # Tools
        content.append("## Registered Tools")
        for name, data in self.tools.get("tools", {}).items():
            content.append(f"### {name}")
            content.append(f"- **Description**: {data.get('description', 'N/A')}")
            content.append(
                f"- **Used By**: {', '.join(data.get('used_by_agents', [])) or 'None'}"
            )
            content.append(f"- **Lines**: {data.get('line_count', 0)}")
            content.append("")

        # Analytics
        content.append("## Usage Analytics")
        content.append(
            f"- **Total Executions**: {analytics['agent_analytics']['total_executions']}"
        )
        content.append(
            f"- **Average Agent Size**: {analytics['complexity_metrics']['avg_agent_size']} lines"
        )
        content.append(
            f"- **Average Tool Size**: {analytics['complexity_metrics']['avg_tool_size']} lines"
        )
        content.append("")

        # Write to file
        with open(output_file, "w") as f:
            f.write("\n".join(content))

        print(f"Registry report exported to: {output_file}")
        return output_file


class RegistryManagementCLI:
    """CLI for registry management operations."""

    def __init__(self):
        self.registry = EnhancedRegistryManager()

    def run(self):
        """Run interactive registry management."""

        while True:
            print("\n" + "=" * 50)
            print("REGISTRY MANAGEMENT")
            print("=" * 50)

            print("\n1. Health Check")
            print("2. View Analytics")
            print("3. Validate All Components")
            print("4. Optimize Registry")
            print("5. Backup Registry")
            print("6. Export Report")
            print("7. View Dependency Graph")
            print("8. Exit")

            choice = input("\nChoice (1-8): ").strip()

            if choice == "1":
                self._health_check()
            elif choice == "2":
                self._view_analytics()
            elif choice == "3":
                self._validate_all()
            elif choice == "4":
                self._optimize()
            elif choice == "5":
                self._backup()
            elif choice == "6":
                self._export_report()
            elif choice == "7":
                self._view_dependencies()
            elif choice == "8":
                print("Exiting...")
                break
            else:
                print("Invalid choice")

    def _health_check(self):
        """Run health check."""
        health = self.registry.health_check()

        print("\n" + "-" * 40)
        print("HEALTH CHECK RESULTS")
        print("-" * 40)
        print(f"Health Score: {health['health_score']}/100")
        print(f"Status: {health['status'].upper()}")
        print(f"Total Components: {health['total_components']}")
        print(f"Valid Components: {health['valid_components']}")

        if health["issues"]["missing_files"] > 0:
            print(f"\nMissing Files: {health['issues']['missing_files']}")
        if health["issues"]["dependency_issues"] > 0:
            print(f"Dependency Issues: {health['issues']['dependency_issues']}")

    def _view_analytics(self):
        """View usage analytics."""
        analytics = self.registry.get_usage_analytics()

        print("\n" + "-" * 40)
        print("USAGE ANALYTICS")
        print("-" * 40)

        print("\nAgent Analytics:")
        print(f"  Total Agents: {analytics['agent_analytics']['total_agents']}")
        print(f"  Total Executions: {analytics['agent_analytics']['total_executions']}")
        print(
            f"  Avg Execution Time: {analytics['agent_analytics']['average_execution_time']}s"
        )

        print("\nMost Used Agents:")
        for agent in analytics["agent_analytics"]["most_used"]:
            print(f"  - {agent['name']}: {agent['executions']} executions")

        print("\nTool Analytics:")
        print(f"  Total Tools: {analytics['tool_analytics']['total_tools']}")

        print("\nMost Reused Tools:")
        for tool in analytics["tool_analytics"]["most_reused"]:
            print(f"  - {tool['name']}: used by {tool['used_by']} agents")

        if analytics["tool_analytics"]["unused_tools"]:
            print(
                f"\nUnused Tools: {', '.join(analytics['tool_analytics']['unused_tools'])}"
            )

    def _validate_all(self):
        """Validate all components."""
        results = self.registry.validate_all()

        print("\n" + "-" * 40)
        print("VALIDATION RESULTS")
        print("-" * 40)

        print(f"Valid Agents: {len(results['valid_agents'])}")
        print(f"Invalid Agents: {len(results['invalid_agents'])}")
        print(f"Valid Tools: {len(results['valid_tools'])}")
        print(f"Invalid Tools: {len(results['invalid_tools'])}")

        if results["missing_files"]:
            print("\nMissing Files:")
            for file in results["missing_files"][:5]:
                print(f"  - {file}")

        if results["dependency_issues"]:
            print("\nDependency Issues:")
            for issue in results["dependency_issues"][:5]:
                print(f"  - {issue}")

    def _optimize(self):
        """Optimize registry."""
        # First do dry run
        dry_report = self.registry.optimize_registry(dry_run=True)

        print("\n" + "-" * 40)
        print("OPTIMIZATION PREVIEW")
        print("-" * 40)

        if dry_report["unused_tools"]:
            print(f"Unused Tools to Remove: {', '.join(dry_report['unused_tools'])}")
        if dry_report["broken_agents"]:
            print(f"Broken Agents to Remove: {', '.join(dry_report['broken_agents'])}")

        if dry_report["unused_tools"] or dry_report["broken_agents"]:
            confirm = input("\nProceed with optimization? (y/n): ").lower()
            if confirm == "y":
                report = self.registry.optimize_registry(dry_run=False)
                print(
                    f"\nOptimization complete. Removed {len(report['removed_components'])} components."
                )
        else:
            print("Registry is already optimized!")

    def _backup(self):
        """Create backup."""
        tag = input("Enter backup tag (optional): ").strip()
        path = self.registry.backup_registries(tag if tag else None)
        print(f"Backup created at: {path}")

    def _export_report(self):
        """Export markdown report."""
        filename = input("Report filename (default: registry_report.md): ").strip()
        if not filename:
            filename = "registry_report.md"
        path = self.registry.export_to_markdown(filename)
        print(f"Report exported to: {path}")

    def _view_dependencies(self):
        """View dependency graph."""
        deps = self.registry.get_dependency_graph()

        print("\n" + "-" * 40)
        print("DEPENDENCY GRAPH")
        print("-" * 40)

        print("\nAgent → Tool Dependencies:")
        for agent, tools in deps["agents_to_tools"].items():
            if tools:
                print(f"  {agent} → {', '.join(tools)}")

        print("\nTool → Agent Usage:")
        for tool, agents in deps["tools_to_agents"].items():
            if agents:
                print(f"  {tool} ← {', '.join(agents)}")

        if deps["agent_chains"]:
            print("\nPotential Agent Chains:")
            for agent, next_agents in deps["agent_chains"].items():
                print(f"  {agent} → {', '.join(next_agents[:3])}")


if __name__ == "__main__":
    cli = RegistryManagementCLI()
    cli.run()
