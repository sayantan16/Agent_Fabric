"""
Registry Manager
Unified registry management for agents and tools with advanced features
"""

import json
import os
import shutil
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path

# Import configuration
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (
    AGENTS_REGISTRY_PATH,
    TOOLS_REGISTRY_PATH,
    GENERATED_AGENTS_DIR,
    GENERATED_TOOLS_DIR,
    PREBUILT_AGENTS_DIR,
    PREBUILT_TOOLS_DIR,
    BACKUP_DIR,
    CLAUDE_MODEL,
    AGENT_OUTPUT_SCHEMA,
    MIN_AGENT_LINES,
    MAX_AGENT_LINES,
    MIN_TOOL_LINES,
    MAX_TOOL_LINES,
)


class RegistryManager:
    """
    Centralized registry management for the Agentic Fabric POC.
    Handles agent and tool registration, validation, dependencies, and analytics.
    """

    def __init__(self, agents_path: str = None, tools_path: str = None):
        """Initialize registry manager with paths from config."""
        self.agents_path = agents_path or AGENTS_REGISTRY_PATH
        self.tools_path = tools_path or TOOLS_REGISTRY_PATH
        self.backup_dir = BACKUP_DIR

        # Create necessary directories
        os.makedirs(GENERATED_AGENTS_DIR, exist_ok=True)
        os.makedirs(GENERATED_TOOLS_DIR, exist_ok=True)
        os.makedirs(PREBUILT_AGENTS_DIR, exist_ok=True)
        os.makedirs(PREBUILT_TOOLS_DIR, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)

        # ADD THIS DEBUG AND VERIFICATION
        print(f"DEBUG: Loading registries from:")
        print(f"  Agents: {self.agents_path}")
        print(f"  Tools: {self.tools_path}")
        print(f"  Agents file exists: {os.path.exists(self.agents_path)}")
        print(f"  Tools file exists: {os.path.exists(self.tools_path)}")

        # Load registries
        self.agents = self._load_registry(self.agents_path)
        self.tools = self._load_registry(self.tools_path)

        # ADD THIS VERIFICATION
        print(f"DEBUG: Loaded {len(self.agents.get('agents', {}))} agents")
        print(f"DEBUG: Loaded {len(self.tools.get('tools', {}))} tools")
        print(f"DEBUG: Agent keys: {list(self.agents.get('agents', {}).keys())}")
        print(f"DEBUG: Tool keys: {list(self.tools.get('tools', {}).keys())}")

    def _load_registry(self, path: str) -> Dict:
        """Load registry from JSON file with proper structure."""
        print(f"DEBUG: Loading registry from {path}")

        try:
            if not os.path.exists(path):
                print(f"DEBUG: Registry file doesn't exist: {path}")
                if "agents" in path:
                    return {"agents": {}}
                else:
                    return {"tools": {}}

            with open(path, "r") as f:
                data = json.load(f)
                print(f"DEBUG: Loaded registry data keys: {list(data.keys())}")

                # Ensure proper structure
                if "agents" in path and "agents" not in data:
                    print(
                        f"DEBUG: Agents registry missing 'agents' key, creating empty"
                    )
                    return {"agents": {}}
                elif "tools" in path and "tools" not in data:
                    print(f"DEBUG: Tools registry missing 'tools' key, creating empty")
                    return {"tools": {}}

                return data

        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"DEBUG: Error loading registry {path}: {e}")
            # Initialize empty registry with proper structure
            if "agents" in path:
                return {"agents": {}}
            else:
                return {"tools": {}}

    def _save_registry(self, data: Dict, path: str):
        """Save registry to JSON file."""
        # Ensure directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(data, f, indent=2, default=str)

    def save_all(self):
        """Save both registries to disk and notify singleton to reload."""
        self._save_registry(self.agents, self.agents_path)
        self._save_registry(self.tools, self.tools_path)

        # Notify singleton pattern to reload for other instances
        try:
            from core.registry_singleton import RegistrySingleton

            # Only reload if we're not already the singleton instance
            singleton_instance = RegistrySingleton()
            if singleton_instance.get_registry() is not self:
                singleton_instance.force_reload()
        except:
            pass  # Ignore circular import or other issues

    # =============================================================================
    # AGENT OPERATIONS
    # =============================================================================

    def register_agent(
        self,
        name: str,
        description: str,
        code: str,
        uses_tools: List[str] = None,
        input_schema: Dict = None,
        output_schema: Dict = None,
        tags: List[str] = None,
        is_prebuilt: bool = False,
    ) -> Dict[str, Any]:
        """
        Register a new agent in the registry.

        Args:
            name: Agent identifier
            description: What the agent does
            code: Python code for the agent
            uses_tools: List of required tools
            input_schema: Expected input structure
            output_schema: Output structure (should match AGENT_OUTPUT_SCHEMA)
            tags: Categorization tags
            is_prebuilt: Whether this is a prebuilt agent

        Returns:
            Dictionary with status and details
        """
        # Validate code size
        line_count = len(code.splitlines())
        if line_count < MIN_AGENT_LINES or line_count > MAX_AGENT_LINES:
            return {
                "status": "error",
                "message": f"Agent must be {MIN_AGENT_LINES}-{MAX_AGENT_LINES} lines, got {line_count}",
            }

        # Determine file path
        if is_prebuilt:
            file_path = os.path.join(PREBUILT_AGENTS_DIR, f"{name}_agent.py")
        else:
            file_path = os.path.join(GENERATED_AGENTS_DIR, f"{name}_agent.py")

        # Save code to file
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            f.write(code)

        # Generate version hash
        version_hash = hashlib.md5(code.encode()).hexdigest()[:8]

        # Create agent entry
        agent_entry = {
            "name": name,
            "description": description,
            "uses_tools": uses_tools or [],
            "input_schema": input_schema or {"data": "any"},
            "output_schema": output_schema or AGENT_OUTPUT_SCHEMA,
            "location": file_path,
            "is_prebuilt": is_prebuilt,
            "created_by": CLAUDE_MODEL,
            "created_at": datetime.now().isoformat(),
            "version": f"1.0.{version_hash}",
            "execution_count": 0,
            "avg_execution_time": 0.0,
            "last_executed": None,
            "tags": tags or [],
            "line_count": line_count,
            "status": "active",
        }

        # Update registry
        self.agents["agents"][name] = agent_entry

        # Update tool references
        if uses_tools:
            for tool_name in uses_tools:
                if tool_name in self.tools.get("tools", {}):
                    if "used_by_agents" not in self.tools["tools"][tool_name]:
                        self.tools["tools"][tool_name]["used_by_agents"] = []
                    if name not in self.tools["tools"][tool_name]["used_by_agents"]:
                        self.tools["tools"][tool_name]["used_by_agents"].append(name)

        print(f"DEBUG: Agent '{name}' registered successfully")
        print(
            f"DEBUG: Registry now has agents: {list(self.agents.get('agents', {}).keys())}"
        )

        # Save changes
        self.save_all()

        return {
            "status": "success",
            "message": f"Agent '{name}' registered successfully",
            "location": file_path,
            "line_count": line_count,
        }

    def get_agent(self, name: str) -> Optional[Dict]:
        """Get agent details by name."""
        return self.agents.get("agents", {}).get(name)

    def list_agents(
        self, tags: List[str] = None, active_only: bool = True
    ) -> List[Dict]:
        """List agents with optional filtering."""
        agents = []
        for name, details in self.agents.get("agents", {}).items():
            # Filter by status
            if active_only and details.get("status") != "active":
                continue

            # Filter by tags
            if tags and not any(tag in details.get("tags", []) for tag in tags):
                continue

            agents.append({"name": name, **details})

        return sorted(agents, key=lambda x: x.get("created_at", ""), reverse=True)

    def agent_exists(self, name: str) -> bool:
        """Check if an agent exists and is active."""
        print(f"DEBUG: Checking if agent '{name}' exists")
        print(
            f"DEBUG: Available agent keys: {list(self.agents.get('agents', {}).keys())}"
        )

        agent = self.get_agent(name)
        exists = agent is not None and agent.get("status") == "active"

        print(f"DEBUG: Agent '{name}' exists: {exists}")
        if agent:
            print(f"DEBUG: Agent status: {agent.get('status')}")
        else:
            print(f"DEBUG: Agent '{name}' not found in registry")

        return exists

    def update_agent_metrics(self, name: str, execution_time: float):
        """Update execution metrics for an agent."""
        if name in self.agents.get("agents", {}):
            agent = self.agents["agents"][name]
            count = agent.get("execution_count", 0)
            avg_time = agent.get("avg_execution_time", 0)

            # Calculate new average
            new_count = count + 1
            new_avg = ((avg_time * count) + execution_time) / new_count

            agent["execution_count"] = new_count
            agent["avg_execution_time"] = round(new_avg, 3)
            agent["last_executed"] = datetime.now().isoformat()

            self.save_all()

    # =============================================================================
    # TOOL OPERATIONS
    # =============================================================================

    def register_tool(
        self,
        name: str,
        description: str,
        code: str,
        signature: str = None,
        tags: List[str] = None,
        is_prebuilt: bool = False,
        is_pure_function: bool = True,
    ) -> Dict[str, Any]:
        """
        Register a new tool in the registry.

        Args:
            name: Tool identifier
            description: What the tool does
            code: Python code for the tool
            signature: Function signature
            tags: Categorization tags
            is_prebuilt: Whether this is a prebuilt tool
            is_pure_function: Whether tool has no side effects

        Returns:
            Dictionary with status and details
        """
        # Validate code size
        line_count = len(code.splitlines())
        if line_count < MIN_TOOL_LINES or line_count > MAX_TOOL_LINES:
            return {
                "status": "error",
                "message": f"Tool must be {MIN_TOOL_LINES}-{MAX_TOOL_LINES} lines, got {line_count}",
            }

        # Determine file path
        if is_prebuilt:
            file_path = os.path.join(PREBUILT_TOOLS_DIR, f"{name}.py")
        else:
            file_path = os.path.join(GENERATED_TOOLS_DIR, f"{name}.py")

        # Save code to file
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            f.write(code)

        # Extract signature if not provided
        if not signature:
            for line in code.split("\n"):
                if line.strip().startswith("def "):
                    signature = line.strip()
                    break

        # Create tool entry
        tool_entry = {
            "name": name,
            "description": description,
            "signature": signature or f"def {name}(input_data=None)",
            "location": file_path,
            "is_prebuilt": is_prebuilt,
            "is_pure_function": is_pure_function,
            "used_by_agents": [],
            "created_by": CLAUDE_MODEL,
            "created_at": datetime.now().isoformat(),
            "tags": tags or [],
            "line_count": line_count,
            "status": "active",
        }

        print(f"DEBUG: Tool '{name}' registered successfully")
        print(
            f"DEBUG: Registry now has tools: {list(self.tools.get('tools', {}).keys())}"
        )

        # Update registry
        self.tools["tools"][name] = tool_entry
        self.save_all()

        return {
            "status": "success",
            "message": f"Tool '{name}' registered successfully",
            "location": file_path,
            "line_count": line_count,
        }

    def get_tool(self, name: str) -> Optional[Dict]:
        """Get tool details by name."""
        return self.tools.get("tools", {}).get(name)

    def list_tools(self, tags: List[str] = None, pure_only: bool = False) -> List[Dict]:
        """List tools with optional filtering."""
        tools = []
        for name, details in self.tools.get("tools", {}).items():
            # Filter by purity
            if pure_only and not details.get("is_pure_function", True):
                continue

            # Filter by tags
            if tags and not any(tag in details.get("tags", []) for tag in tags):
                continue

            tools.append({"name": name, **details})

        return sorted(tools, key=lambda x: x.get("created_at", ""), reverse=True)

    def tool_exists(self, name: str) -> bool:
        """Check if a tool exists and is active."""
        print(f"DEBUG: Checking if tool '{name}' exists")
        print(f"DEBUG: Available tool keys: {list(self.tools.get('tools', {}).keys())}")

        tool = self.get_tool(name)
        exists = tool is not None and tool.get("status") == "active"

        print(f"DEBUG: Tool '{name}' exists: {exists}")
        if tool:
            print(f"DEBUG: Tool status: {tool.get('status')}")
        else:
            print(f"DEBUG: Tool '{name}' not found in registry")

        return exists

    # =============================================================================
    # DEPENDENCY MANAGEMENT
    # =============================================================================

    def get_agent_dependencies(self, agent_name: str) -> Dict[str, List[str]]:
        """Get all dependencies for an agent."""
        agent = self.get_agent(agent_name)
        if not agent:
            return {"tools": [], "missing_tools": []}

        tools_needed = agent.get("uses_tools", [])
        missing_tools = [tool for tool in tools_needed if not self.tool_exists(tool)]

        return {
            "tools": tools_needed,
            "missing_tools": missing_tools,
            "available_tools": [t for t in tools_needed if self.tool_exists(t)],
        }

    def get_tool_usage(self, tool_name: str) -> List[str]:
        """Get list of agents using a specific tool."""
        tool = self.get_tool(tool_name)
        return tool.get("used_by_agents", []) if tool else []

    def get_dependency_graph(self) -> Dict[str, Any]:
        """Build complete dependency graph."""
        graph = {
            "agents_to_tools": {},
            "tools_to_agents": {},
            "missing_dependencies": [],
            "unused_tools": [],
        }

        # Build agent to tool mapping
        for agent_name, agent_data in self.agents.get("agents", {}).items():
            if agent_data.get("status") == "active":
                tools = agent_data.get("uses_tools", [])
                graph["agents_to_tools"][agent_name] = tools

                # Check for missing dependencies
                for tool in tools:
                    if not self.tool_exists(tool):
                        graph["missing_dependencies"].append(
                            {"agent": agent_name, "missing_tool": tool}
                        )

        # Build tool to agent mapping
        for tool_name, tool_data in self.tools.get("tools", {}).items():
            if tool_data.get("status") == "active":
                agents = tool_data.get("used_by_agents", [])
                graph["tools_to_agents"][tool_name] = agents

                # Check for unused tools
                if not agents:
                    graph["unused_tools"].append(tool_name)

        return graph

    # =============================================================================
    # VALIDATION
    # =============================================================================

    def validate_all(self) -> Dict[str, List]:
        """Validate all components in the registry."""
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
            issues = []

            # Check file existence
            if not os.path.exists(file_path):
                issues.append(f"Missing file: {file_path}")
                results["missing_files"].append(f"Agent: {name}")

            # Check dependencies
            deps = self.get_agent_dependencies(name)
            if deps["missing_tools"]:
                issues.append(f"Missing tools: {', '.join(deps['missing_tools'])}")
                results["dependency_issues"].append(
                    {"agent": name, "missing": deps["missing_tools"]}
                )

            # Check line count
            line_count = agent.get("line_count", 0)
            if line_count < MIN_AGENT_LINES or line_count > MAX_AGENT_LINES:
                issues.append(f"Invalid size: {line_count} lines")

            if issues:
                results["invalid_agents"].append({"name": name, "issues": issues})
            else:
                results["valid_agents"].append(name)

        # Validate tools
        for name, tool in self.tools.get("tools", {}).items():
            file_path = tool.get("location", "")
            issues = []

            # Check file existence
            if not os.path.exists(file_path):
                issues.append(f"Missing file: {file_path}")
                results["missing_files"].append(f"Tool: {name}")

            # Check line count
            line_count = tool.get("line_count", 0)
            if line_count < MIN_TOOL_LINES or line_count > MAX_TOOL_LINES:
                issues.append(f"Invalid size: {line_count} lines")

            if issues:
                results["invalid_tools"].append({"name": name, "issues": issues})
            else:
                results["valid_tools"].append(name)

        return results

    def health_check(self) -> Dict[str, Any]:
        """Perform comprehensive health check."""
        validation = self.validate_all()
        stats = self.get_statistics()

        # Calculate health score
        total_agents = stats["total_agents"]
        total_tools = stats["total_tools"]
        valid_agents = len(validation["valid_agents"])
        valid_tools = len(validation["valid_tools"])

        health_score = 100.0
        if total_agents > 0:
            health_score -= (1 - valid_agents / total_agents) * 50
        if total_tools > 0:
            health_score -= (1 - valid_tools / total_tools) * 50

        return {
            "health_score": round(max(0, health_score), 1),
            "status": (
                "healthy"
                if health_score >= 80
                else "degraded" if health_score >= 50 else "unhealthy"
            ),
            "total_components": total_agents + total_tools,
            "valid_components": valid_agents + valid_tools,
            "issues": {
                "invalid_agents": len(validation["invalid_agents"]),
                "invalid_tools": len(validation["invalid_tools"]),
                "missing_files": len(validation["missing_files"]),
                "dependency_issues": len(validation["dependency_issues"]),
            },
            "statistics": stats,
            "validation_details": validation,
        }

    # =============================================================================
    # SEARCH AND DISCOVERY
    # =============================================================================

    def search_agents(self, query: str) -> List[Dict]:
        """Search agents by name or description."""
        query_lower = query.lower()
        results = []

        for name, details in self.agents.get("agents", {}).items():
            if details.get("status") != "active":
                continue

            if (
                query_lower in name.lower()
                or query_lower in details.get("description", "").lower()
                or any(query_lower in tag for tag in details.get("tags", []))
            ):
                results.append({"name": name, **details})

        return results

    def search_tools(self, query: str) -> List[Dict]:
        """Search tools by name or description."""
        query_lower = query.lower()
        results = []

        for name, details in self.tools.get("tools", {}).items():
            if details.get("status") != "active":
                continue

            if (
                query_lower in name.lower()
                or query_lower in details.get("description", "").lower()
                or any(query_lower in tag for tag in details.get("tags", []))
            ):
                results.append({"name": name, **details})

        return results

    def find_capable_agents(self, task: str) -> List[Dict]:
        """Find agents capable of handling a task."""
        # Search by task keywords
        agents = self.search_agents(task)

        # Sort by relevance (execution count as proxy for reliability)
        agents.sort(key=lambda x: x.get("execution_count", 0), reverse=True)

        return agents

    # =============================================================================
    # STATISTICS AND ANALYTICS
    # =============================================================================

    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive registry statistics."""
        agents_list = self.agents.get("agents", {})
        tools_list = self.tools.get("tools", {})

        active_agents = [a for a in agents_list.values() if a.get("status") == "active"]
        active_tools = [t for t in tools_list.values() if t.get("status") == "active"]

        # Calculate metrics
        total_executions = sum(a.get("execution_count", 0) for a in active_agents)

        return {
            "total_agents": len(active_agents),
            "total_tools": len(active_tools),
            "prebuilt_agents": sum(1 for a in active_agents if a.get("is_prebuilt")),
            "generated_agents": sum(
                1 for a in active_agents if not a.get("is_prebuilt")
            ),
            "prebuilt_tools": sum(1 for t in active_tools if t.get("is_prebuilt")),
            "generated_tools": sum(1 for t in active_tools if not t.get("is_prebuilt")),
            "total_executions": total_executions,
            "avg_agent_lines": round(
                sum(a.get("line_count", 0) for a in active_agents)
                / max(len(active_agents), 1),
                1,
            ),
            "avg_tool_lines": round(
                sum(t.get("line_count", 0) for t in active_tools)
                / max(len(active_tools), 1),
                1,
            ),
            "tool_reuse_rate": round(
                sum(len(t.get("used_by_agents", [])) for t in active_tools)
                / max(len(active_tools), 1),
                2,
            ),
            "most_used_agent": (
                max(active_agents, key=lambda x: x.get("execution_count", 0))["name"]
                if active_agents
                else None
            ),
            "newest_agent": (
                max(active_agents, key=lambda x: x.get("created_at", ""))["name"]
                if active_agents
                else None
            ),
        }

    # =============================================================================
    # BACKUP AND RESTORE
    # =============================================================================

    def backup_registries(self, tag: str = None) -> str:
        """Create backup of current registries."""
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
            "health": self.health_check(),
        }

        with open(os.path.join(backup_path, "metadata.json"), "w") as f:
            json.dump(metadata, f, indent=2)

        return backup_path

    def restore_registries(self, backup_name: str) -> bool:
        """Restore registries from backup."""
        backup_path = os.path.join(self.backup_dir, backup_name)

        if not os.path.exists(backup_path):
            return False

        try:
            # Create current backup before restore
            self.backup_registries("before_restore")

            # Restore files
            shutil.copy(os.path.join(backup_path, "agents.json"), self.agents_path)
            shutil.copy(os.path.join(backup_path, "tools.json"), self.tools_path)

            # Reload registries
            self.agents = self._load_registry(self.agents_path)
            self.tools = self._load_registry(self.tools_path)

            return True
        except Exception:
            return False

    # =============================================================================
    # CLEANUP AND OPTIMIZATION
    # =============================================================================

    def optimize_registry(self, dry_run: bool = True) -> Dict[str, Any]:
        """Optimize registry by cleaning up issues."""
        report = {
            "unused_tools": [],
            "broken_agents": [],
            "broken_tools": [],
            "fixed_dependencies": [],
            "actions_taken": [],
        }

        # Find unused tools
        deps = self.get_dependency_graph()
        report["unused_tools"] = deps["unused_tools"]

        # Find broken components
        validation = self.validate_all()
        report["broken_agents"] = [a["name"] for a in validation["invalid_agents"]]
        report["broken_tools"] = [t["name"] for t in validation["invalid_tools"]]

        if not dry_run:
            # Remove unused tools
            for tool_name in report["unused_tools"]:
                if tool_name in self.tools["tools"]:
                    self.tools["tools"][tool_name]["status"] = "deprecated"
                    report["actions_taken"].append(
                        f"Deprecated unused tool: {tool_name}"
                    )

            # Mark broken components
            for agent_name in report["broken_agents"]:
                if agent_name in self.agents["agents"]:
                    self.agents["agents"][agent_name]["status"] = "broken"
                    report["actions_taken"].append(f"Marked broken agent: {agent_name}")

            for tool_name in report["broken_tools"]:
                if tool_name in self.tools["tools"]:
                    self.tools["tools"][tool_name]["status"] = "broken"
                    report["actions_taken"].append(f"Marked broken tool: {tool_name}")

            self.save_all()

        return report

    def cleanup_deprecated(self) -> int:
        """Remove deprecated components."""
        count = 0

        # Clean deprecated agents
        for name in list(self.agents["agents"].keys()):
            if self.agents["agents"][name].get("status") == "deprecated":
                del self.agents["agents"][name]
                count += 1

        # Clean deprecated tools
        for name in list(self.tools["tools"].keys()):
            if self.tools["tools"][name].get("status") == "deprecated":
                del self.tools["tools"][name]
                count += 1

        if count > 0:
            self.save_all()

        return count
