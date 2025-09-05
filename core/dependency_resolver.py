"""
Dependency Resolver
Handles topological sorting and dependency graph creation for agent-tool relationships
"""

import networkx as nx
from typing import Dict, List, Any, Tuple
from collections import defaultdict


class DependencyResolver:
    """Resolves and creates dependencies in correct order."""

    def __init__(self, registry):
        self.registry = registry
        self.dependency_graph = nx.DiGraph()

    def analyze_request(
        self, request: str, existing_agents: Dict, existing_tools: Dict
    ) -> Dict:
        """
        Analyze request and build dependency graph.

        Returns:
            Dict with capabilities needed and creation order
        """
        # Build capability map from request
        capabilities = self._extract_capabilities(request)

        # Build dependency graph
        graph = self._build_dependency_graph(
            capabilities, existing_agents, existing_tools
        )

        # Determine creation order
        creation_order = self._get_creation_order(graph)

        return {
            "capabilities": capabilities,
            "dependency_graph": graph,
            "creation_order": creation_order,
            "missing_components": self._identify_missing_components(
                graph, existing_agents, existing_tools
            ),
        }

    def _extract_capabilities(self, request: str) -> List[Dict]:
        """Extract required capabilities from request."""
        capabilities = []

        # Pattern matching for common operations
        request_lower = request.lower()

        # Extraction capabilities
        if any(word in request_lower for word in ["extract", "find", "get"]):
            if "email" in request_lower:
                capabilities.append(
                    {
                        "name": "email_extraction",
                        "agent": "email_extractor",
                        "tools": ["extract_emails"],
                    }
                )
            if "phone" in request_lower:
                capabilities.append(
                    {
                        "name": "phone_extraction",
                        "agent": "phone_extractor",
                        "tools": ["extract_phone"],
                    }
                )
            if "url" in request_lower or "link" in request_lower:
                capabilities.append(
                    {
                        "name": "url_extraction",
                        "agent": "url_extractor",
                        "tools": ["extract_urls"],
                    }
                )

        # Analysis capabilities
        if any(word in request_lower for word in ["analyze", "analysis", "examine"]):
            if "sentiment" in request_lower:
                capabilities.append(
                    {
                        "name": "sentiment_analysis",
                        "agent": "sentiment_analyzer",
                        "tools": ["analyze_sentiment", "score_sentiment"],
                    }
                )
            if "statistic" in request_lower or "stats" in request_lower:
                capabilities.append(
                    {
                        "name": "statistical_analysis",
                        "agent": "statistics_calculator",
                        "tools": [
                            "calculate_mean",
                            "calculate_median",
                            "calculate_std",
                        ],
                    }
                )

        # Generation capabilities
        if any(word in request_lower for word in ["generate", "create", "make"]):
            if "chart" in request_lower or "graph" in request_lower:
                capabilities.append(
                    {
                        "name": "chart_generation",
                        "agent": "chart_generator",
                        "tools": ["generate_chart", "format_chart_data"],
                    }
                )
            if "report" in request_lower:
                capabilities.append(
                    {
                        "name": "report_generation",
                        "agent": "report_generator",
                        "tools": ["format_report", "generate_summary"],
                    }
                )

        return capabilities

    def _build_dependency_graph(
        self, capabilities: List[Dict], existing_agents: Dict, existing_tools: Dict
    ) -> nx.DiGraph:
        """Build directed graph of dependencies."""
        graph = nx.DiGraph()

        for cap in capabilities:
            agent_name = cap["agent"]

            # Add agent node
            graph.add_node(
                agent_name,
                type="agent",
                exists=agent_name in existing_agents,
                capability=cap["name"],
            )

            # Add tool nodes and edges
            for tool_name in cap["tools"]:
                graph.add_node(
                    tool_name, type="tool", exists=tool_name in existing_tools
                )

                # Tool must exist before agent can use it
                graph.add_edge(tool_name, agent_name, relation="required_by")

        return graph

    def _get_creation_order(self, graph: nx.DiGraph) -> List[Tuple[str, str]]:
        """
        Get creation order using topological sort.

        Returns:
            List of (type, name) tuples in creation order
        """
        try:
            # Topological sort ensures dependencies are created first
            sorted_nodes = list(nx.topological_sort(graph))

            creation_order = []
            for node in sorted_nodes:
                if not graph.nodes[node]["exists"]:
                    node_type = graph.nodes[node]["type"]
                    creation_order.append((node_type, node))

            return creation_order

        except nx.NetworkXUnfeasible:
            # Graph has cycles - shouldn't happen with proper design
            print("WARNING: Dependency graph has cycles!")
            return []

    def _identify_missing_components(
        self, graph: nx.DiGraph, existing_agents: Dict, existing_tools: Dict
    ) -> Dict:
        """Identify what needs to be created."""
        missing = {"agents": [], "tools": []}

        for node, data in graph.nodes(data=True):
            if not data["exists"]:
                if data["type"] == "agent":
                    # Get required tools for this agent
                    required_tools = [
                        pred
                        for pred in graph.predecessors(node)
                        if graph.nodes[pred]["type"] == "tool"
                    ]

                    missing["agents"].append(
                        {
                            "name": node,
                            "required_tools": required_tools,
                            "capability": data.get("capability", ""),
                        }
                    )
                else:  # tool
                    missing["tools"].append(
                        {"name": node, "used_by": list(graph.successors(node))}
                    )

        return missing

    def visualize_dependencies(self, graph: nx.DiGraph) -> str:
        """Create text visualization of dependency graph."""
        lines = ["Dependency Graph:"]
        lines.append("=" * 50)

        # Group by component type
        tools = [n for n, d in graph.nodes(data=True) if d["type"] == "tool"]
        agents = [n for n, d in graph.nodes(data=True) if d["type"] == "agent"]

        lines.append("\nTools:")
        for tool in tools:
            status = "✓" if graph.nodes[tool]["exists"] else "✗"
            users = list(graph.successors(tool))
            lines.append(f"  {status} {tool} -> used by: {', '.join(users)}")

        lines.append("\nAgents:")
        for agent in agents:
            status = "✓" if graph.nodes[agent]["exists"] else "✗"
            deps = list(graph.predecessors(agent))
            lines.append(f"  {status} {agent} <- requires: {', '.join(deps)}")

        lines.append("\nCreation Order:")
        for node in nx.topological_sort(graph):
            if not graph.nodes[node]["exists"]:
                lines.append(f"  {graph.nodes[node]['type']}: {node}")

        return "\n".join(lines)
