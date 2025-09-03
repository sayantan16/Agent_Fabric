"""
Registry Manager
Manages dual registries for agents and tools with dependency tracking
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
import hashlib


class RegistryManager:
    def __init__(
        self, agents_path: str = "agents.json", tools_path: str = "tools.json"
    ):
        self.agents_path = agents_path
        self.tools_path = tools_path
        self.agents = self._load_registry(agents_path)
        self.tools = self._load_registry(tools_path)

    def _load_registry(self, path: str) -> Dict:
        """Load registry from JSON file."""
        try:
            with open(path, "r") as f:
                data = json.load(f)
                # Ensure proper structure
                if path == self.agents_path and "agents" not in data:
                    return {"agents": {}}
                elif path == self.tools_path and "tools" not in data:
                    return {"tools": {}}
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            # Initialize empty registry
            return {"agents": {}} if "agents" in path else {"tools": {}}

    def _save_registry(self, data: Dict, path: str):
        """Save registry to JSON file."""
        with open(path, "w") as f:
            json.dump(data, f, indent=2, default=str)

    def save_all(self):
        """Save both registries."""
        self._save_registry(self.agents, self.agents_path)
        self._save_registry(self.tools, self.tools_path)

    # =============================================================================
    # AGENT REGISTRY OPERATIONS
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
    ) -> bool:
        """Register a new agent."""

        # Generate file path
        file_path = f"generated/agents/{name}.py"

        # Save the code to file
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            f.write(code)

        # Generate a version hash from code
        version_hash = hashlib.md5(code.encode()).hexdigest()[:8]

        # Create agent entry
        agent_entry = {
            "description": description,
            "uses_tools": uses_tools or [],
            "input_schema": input_schema or {"data": "any"},
            "output_schema": output_schema or {"data": "any"},
            "location": file_path,
            "created_by": "claude-3-haiku",
            "created_at": datetime.now().isoformat(),
            "version": f"1.0.{version_hash}",
            "execution_count": 0,
            "avg_execution_time": 0,
            "tags": tags or [],
            "line_count": len(code.splitlines()),
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

        # Save registries
        self.save_all()

        print(
            f"Agent '{name}' registered successfully ({len(code.splitlines())} lines)"
        )
        return True

    def get_agent(self, name: str) -> Optional[Dict]:
        """Get agent details by name."""
        return self.agents.get("agents", {}).get(name)

    def list_agents(self, tags: List[str] = None) -> List[Dict]:
        """List all agents, optionally filtered by tags."""
        agents = []
        for name, details in self.agents.get("agents", {}).items():
            if tags:
                if any(tag in details.get("tags", []) for tag in tags):
                    agents.append({"name": name, **details})
            else:
                agents.append({"name": name, **details})
        return agents

    def agent_exists(self, name: str) -> bool:
        """Check if an agent exists."""
        return name in self.agents.get("agents", {})

    def update_agent_metrics(self, name: str, execution_time: float):
        """Update agent execution metrics."""
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
    # TOOL REGISTRY OPERATIONS
    # =============================================================================

    def register_tool(
        self,
        name: str,
        description: str,
        code: str,
        signature: str = None,
        tags: List[str] = None,
    ) -> bool:
        """Register a new tool."""

        # Generate file path
        file_path = f"generated/tools/{name}.py"

        # Save the code to file
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            f.write(code)

        # Extract signature if not provided
        if not signature:
            # Simple extraction of function signature from code
            lines = code.split("\n")
            for line in lines:
                if line.startswith("def "):
                    signature = line.strip()
                    break

        # Create tool entry
        tool_entry = {
            "description": description,
            "signature": signature or f"def {name}(*args, **kwargs)",
            "location": file_path,
            "used_by_agents": [],
            "created_by": "claude-3-haiku",
            "created_at": datetime.now().isoformat(),
            "is_pure_function": True,
            "tags": tags or [],
            "line_count": len(code.splitlines()),
        }

        # Update registry
        self.tools["tools"][name] = tool_entry
        self.save_all()

        print(f"Tool '{name}' registered successfully ({len(code.splitlines())} lines)")
        return True

    def get_tool(self, name: str) -> Optional[Dict]:
        """Get tool details by name."""
        return self.tools.get("tools", {}).get(name)

    def list_tools(self, tags: List[str] = None) -> List[Dict]:
        """List all tools, optionally filtered by tags."""
        tools = []
        for name, details in self.tools.get("tools", {}).items():
            if tags:
                if any(tag in details.get("tags", []) for tag in tags):
                    tools.append({"name": name, **details})
            else:
                tools.append({"name": name, **details})
        return tools

    def tool_exists(self, name: str) -> bool:
        """Check if a tool exists."""
        return name in self.tools.get("tools", {})

    # =============================================================================
    # DEPENDENCY OPERATIONS
    # =============================================================================

    def get_agent_dependencies(self, agent_name: str) -> Dict[str, List[str]]:
        """Get all dependencies for an agent."""
        agent = self.get_agent(agent_name)
        if not agent:
            return {}

        dependencies = {"tools": agent.get("uses_tools", []), "missing_tools": []}

        # Check which tools are missing
        for tool in dependencies["tools"]:
            if not self.tool_exists(tool):
                dependencies["missing_tools"].append(tool)

        return dependencies

    def get_tool_usage(self, tool_name: str) -> List[str]:
        """Get list of agents using a specific tool."""
        tool = self.get_tool(tool_name)
        if tool:
            return tool.get("used_by_agents", [])
        return []

    def can_delete_tool(self, tool_name: str) -> bool:
        """Check if a tool can be safely deleted (no agents using it)."""
        return len(self.get_tool_usage(tool_name)) == 0

    # =============================================================================
    # SEARCH OPERATIONS
    # =============================================================================

    def search_agents(self, query: str) -> List[Dict]:
        """Search agents by description or name."""
        query_lower = query.lower()
        results = []

        for name, details in self.agents.get("agents", {}).items():
            if (
                query_lower in name.lower()
                or query_lower in details.get("description", "").lower()
            ):
                results.append({"name": name, **details})

        return results

    def search_tools(self, query: str) -> List[Dict]:
        """Search tools by description or name."""
        query_lower = query.lower()
        results = []

        for name, details in self.tools.get("tools", {}).items():
            if (
                query_lower in name.lower()
                or query_lower in details.get("description", "").lower()
            ):
                results.append({"name": name, **details})

        return results

    # =============================================================================
    # STATISTICS
    # =============================================================================

    def get_statistics(self) -> Dict:
        """Get registry statistics."""
        agents_list = self.agents.get("agents", {})
        tools_list = self.tools.get("tools", {})

        # Calculate agent stats
        total_executions = sum(
            a.get("execution_count", 0) for a in agents_list.values()
        )
        avg_agent_lines = sum(
            a.get("line_count", 0) for a in agents_list.values()
        ) / max(len(agents_list), 1)

        # Calculate tool stats
        avg_tool_lines = sum(t.get("line_count", 0) for t in tools_list.values()) / max(
            len(tools_list), 1
        )
        tool_reuse = sum(len(t.get("used_by_agents", [])) for t in tools_list.values())

        return {
            "total_agents": len(agents_list),
            "total_tools": len(tools_list),
            "total_executions": total_executions,
            "avg_agent_lines": round(avg_agent_lines, 1),
            "avg_tool_lines": round(avg_tool_lines, 1),
            "tool_reuse_count": tool_reuse,
            "most_used_agent": (
                max(agents_list.items(), key=lambda x: x[1].get("execution_count", 0))[
                    0
                ]
                if agents_list
                else None
            ),
            "newest_agent": (
                max(agents_list.items(), key=lambda x: x[1].get("created_at", ""))[0]
                if agents_list
                else None
            ),
        }

    def cleanup_unused(self, dry_run: bool = True) -> List[str]:
        """Remove unused tools (with confirmation)."""
        unused = []
        for tool_name in self.tools.get("tools", {}):
            if self.can_delete_tool(tool_name):
                unused.append(tool_name)
                if not dry_run:
                    # Delete file
                    tool_path = self.tools["tools"][tool_name]["location"]
                    if os.path.exists(tool_path):
                        os.remove(tool_path)
                    # Remove from registry
                    del self.tools["tools"][tool_name]

        if not dry_run:
            self.save_all()
            print(f"Cleaned up {len(unused)} unused tools")

        return unused
