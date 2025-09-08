# flask_app/services/registry_service.py
"""
Registry Service
Interfaces with backend registry for agent/tool information
"""

import os
import sys
from typing import Dict, List, Any, Optional

# Add project root to path
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(project_root)

try:
    from core.registry_singleton import get_shared_registry
    from core.registry import RegistryManager
except ImportError as e:
    print(f"Warning: Could not import registry components: {e}")
    get_shared_registry = None


class RegistryService:
    """Service layer for registry operations."""

    def __init__(self):
        """Initialize registry service."""
        self.registry = get_shared_registry() if get_shared_registry else None

    def is_available(self) -> bool:
        """Check if registry is available."""
        return self.registry is not None

    def get_agents_list(
        self, tags: List[str] = None, active_only: bool = True
    ) -> List[Dict[str, Any]]:
        """Get list of available agents."""
        if not self.is_available():
            return []

        try:
            agents = self.registry.list_agents(tags=tags, active_only=active_only)

            # Add formatted data for UI
            for agent in agents:
                agent["formatted_created_at"] = self._format_timestamp(
                    agent.get("created_at")
                )
                agent["capabilities_summary"] = self._summarize_capabilities(agent)
                agent["performance_indicator"] = self._get_performance_indicator(agent)

            return agents
        except Exception as e:
            print(f"Error fetching agents: {e}")
            return []

    def get_tools_list(
        self, tags: List[str] = None, pure_only: bool = False
    ) -> List[Dict[str, Any]]:
        """Get list of available tools."""
        if not self.is_available():
            return []

        try:
            tools = self.registry.list_tools(tags=tags, pure_only=pure_only)

            # Add formatted data for UI
            for tool in tools:
                tool["formatted_created_at"] = self._format_timestamp(
                    tool.get("created_at")
                )
                tool["usage_summary"] = self._get_tool_usage_summary(tool)
                tool["complexity_level"] = self._assess_tool_complexity(tool)

            return tools
        except Exception as e:
            print(f"Error fetching tools: {e}")
            return []

    def get_agent_details(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific agent."""
        if not self.is_available():
            return None

        try:
            agent = self.registry.get_agent(agent_name)
            if agent:
                # Add dependency information
                agent["dependencies"] = self.registry.get_agent_dependencies(agent_name)
                agent["formatted_created_at"] = self._format_timestamp(
                    agent.get("created_at")
                )

            return agent
        except Exception as e:
            print(f"Error fetching agent details: {e}")
            return None

    def get_tool_details(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific tool."""
        if not self.is_available():
            return None

        try:
            tool = self.registry.get_tool(tool_name)
            if tool:
                # Add usage information
                tool["used_by"] = self.registry.get_tool_usage(tool_name)
                tool["formatted_created_at"] = self._format_timestamp(
                    tool.get("created_at")
                )

            return tool
        except Exception as e:
            print(f"Error fetching tool details: {e}")
            return None

    def get_registry_stats(self) -> Dict[str, Any]:
        """Get comprehensive registry statistics - FIXED."""
        if not self.is_available():
            return {
                "available": False,
                "statistics": {"total_agents": 0, "total_tools": 0},
                "summary": {"health_score": 0, "status": "unavailable"},
            }

        try:
            # Get actual counts from registry
            agents = self.registry.list_agents(active_only=True)
            tools = self.registry.list_tools()

            stats = {
                "total_agents": len(agents),
                "total_tools": len(tools),
                "total_components": len(agents) + len(tools),
            }

            # Calculate health score
            health_score = 100 if stats["total_components"] > 0 else 0

            return {
                "available": True,
                "statistics": stats,
                "summary": {
                    "health_score": health_score,
                    "status": "healthy" if health_score > 50 else "degraded",
                },
            }
        except Exception as e:
            print(f"Error getting registry stats: {e}")
            return {
                "available": True,
                "statistics": {"total_agents": 0, "total_tools": 0},
                "summary": {"health_score": 0, "status": "error"},
            }

    def get_dependency_graph(self) -> Dict[str, Any]:
        """Get dependency graph for visualization."""
        if not self.is_available():
            return {
                "nodes": [],
                "edges": [],
                "stats": {
                    "total_agents": 0,
                    "total_tools": 0,
                    "missing_dependencies": 0,
                    "unused_tools": 0,
                },
            }

        try:
            deps = self.registry.get_dependency_graph()

            # Convert to visualization format
            nodes = []
            edges = []

            # Add agent nodes
            for agent_name, tools in deps.get("agents_to_tools", {}).items():
                nodes.append(
                    {
                        "id": agent_name,
                        "type": "agent",
                        "name": agent_name,  # Add name field
                        "label": agent_name,
                        "description": self._get_agent_description(agent_name),
                        "uses_tools": tools,  # Add for UI
                    }
                )

                # Add edges to tools
                for tool_name in tools:
                    edges.append(
                        {"from": tool_name, "to": agent_name, "type": "dependency"}
                    )

            # Add tool nodes
            for tool_name, agents_using in deps.get("tools_to_agents", {}).items():
                nodes.append(
                    {
                        "id": tool_name,
                        "type": "tool",
                        "name": tool_name,  # Add name field
                        "label": tool_name,
                        "description": self._get_tool_description(tool_name),
                        "used_by": agents_using,  # Add for UI
                    }
                )

            # Calculate statistics
            agent_nodes = [n for n in nodes if n["type"] == "agent"]
            tool_nodes = [n for n in nodes if n["type"] == "tool"]
            unused_tools = [t for t in tool_nodes if not t.get("used_by")]

            return {
                "nodes": nodes,
                "edges": edges,
                "stats": {
                    "total_agents": len(agent_nodes),
                    "total_tools": len(tool_nodes),
                    "total_nodes": len(nodes),
                    "total_edges": len(edges),
                    "missing_dependencies": len(deps.get("missing_dependencies", [])),
                    "unused_tools": len(unused_tools),
                },
            }

        except Exception as e:
            print(f"Error building dependency graph: {e}")
            return {
                "nodes": [],
                "edges": [],
                "error": str(e),
                "stats": {
                    "total_agents": 0,
                    "total_tools": 0,
                    "missing_dependencies": 0,
                    "unused_tools": 0,
                },
            }

    def search_components(self, query: str) -> Dict[str, List[Dict]]:
        """Search agents and tools by query."""
        if not self.is_available():
            return {"agents": [], "tools": []}

        try:
            agents = self.registry.search_agents(query)
            tools = self.registry.search_tools(query)

            return {
                "agents": agents,
                "tools": tools,
                "total_results": len(agents) + len(tools),
            }
        except Exception as e:
            print(f"Error searching components: {e}")
            return {"agents": [], "tools": [], "error": str(e)}

    def _format_timestamp(self, timestamp: str = None) -> str:
        """Format timestamp for display."""
        if not timestamp:
            from datetime import datetime

            return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            from datetime import datetime

            dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            return timestamp

    def _summarize_capabilities(self, agent: Dict) -> str:
        """Create a summary of agent capabilities."""
        tools = agent.get("uses_tools", [])
        tags = agent.get("tags", [])

        if tools:
            return f"Uses {len(tools)} tools: {', '.join(tools[:3])}{'...' if len(tools) > 3 else ''}"
        elif tags:
            return f"Tags: {', '.join(tags[:3])}{'...' if len(tags) > 3 else ''}"
        else:
            return "General purpose agent"

    def _get_performance_indicator(self, agent: Dict) -> str:
        """Get performance indicator for agent."""
        exec_count = agent.get("execution_count", 0)
        avg_time = agent.get("avg_execution_time", 0)

        if exec_count == 0:
            return "New"
        elif avg_time < 2:
            return "Fast"
        elif avg_time < 10:
            return "Normal"
        else:
            return "Slow"

    def _get_tool_usage_summary(self, tool: Dict) -> str:
        """Get usage summary for tool."""
        used_by = tool.get("used_by_agents", [])
        if not used_by:
            return "Unused"
        elif len(used_by) == 1:
            return f"Used by {used_by[0]}"
        else:
            return f"Used by {len(used_by)} agents"

    def _assess_tool_complexity(self, tool: Dict) -> str:
        """Assess tool complexity level."""
        line_count = tool.get("line_count", 0)
        if line_count < 30:
            return "Simple"
        elif line_count < 100:
            return "Medium"
        else:
            return "Complex"

    def _get_agent_description(self, agent_name: str) -> str:
        """Get agent description for visualization."""
        agent = self.get_agent_details(agent_name)
        return agent.get("description", "Agent") if agent else "Agent"

    def _get_tool_description(self, tool_name: str) -> str:
        """Get tool description for visualization."""
        tool = self.get_tool_details(tool_name)
        return tool.get("description", "Tool") if tool else "Tool"


# Global service instance
registry_service = RegistryService()
