# flask_app/services/workflow_service.py
"""
Workflow Service
Handles workflow visualization and real-time updates
"""

import os
import sys
import json
from typing import Dict, List, Any, Optional, Generator
from datetime import datetime

# Add project root to path
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(project_root)

try:
    from backup_removed_components.workflow_engine import WorkflowEngine, WorkflowState
except ImportError as e:
    print(f"Warning: Could not import workflow components: {e}")
    WorkflowEngine = None


class WorkflowService:
    """Service layer for workflow operations."""

    def __init__(self):
        """Initialize workflow service - FIXED VERSION."""
        # FIXED: Properly handle WorkflowEngine initialization
        try:
            if WorkflowEngine:
                # Try to initialize with registry first (if it requires one)
                try:
                    from core.registry_singleton import get_shared_registry

                    registry = get_shared_registry()
                    if registry:
                        self.workflow_engine = WorkflowEngine(registry)
                    else:
                        self.workflow_engine = WorkflowEngine()
                except TypeError:
                    # If WorkflowEngine doesn't accept registry, use default constructor
                    self.workflow_engine = WorkflowEngine()
                except Exception as e:
                    print(
                        f"DEBUG: Failed to initialize WorkflowEngine with registry: {e}"
                    )
                    # Fallback to no-argument constructor
                    self.workflow_engine = WorkflowEngine()
            else:
                self.workflow_engine = None

            self.workflow_cache = {}
            print("DEBUG: WorkflowService initialized successfully")

        except Exception as e:
            print(f"WARNING: Failed to initialize WorkflowService: {e}")
            self.workflow_engine = None
            self.workflow_cache = {}

    def is_available(self) -> bool:
        """Check if workflow engine is available."""
        return self.workflow_engine is not None

    def get_workflow_visualization(self, workflow_id: str) -> Dict[str, Any]:
        """Get workflow visualization data."""
        if not self.is_available():
            return {"error": "Workflow engine not available"}

        # Check cache first
        if workflow_id in self.workflow_cache:
            workflow_data = self.workflow_cache[workflow_id]
        else:
            try:
                workflow_status = self.workflow_engine.get_workflow_status(workflow_id)
                if not workflow_status:
                    return {"error": "Workflow not found"}
                workflow_data = workflow_status
            except Exception as e:
                return {"error": f"Failed to get workflow status: {str(e)}"}

        return self._create_visualization_data(workflow_data)

    def stream_workflow_updates(self, workflow_id: str) -> Generator[str, None, None]:
        """Stream real-time workflow updates."""
        if not self.is_available():
            yield f"data: {json.dumps({'error': 'Workflow engine not available'})}\n\n"
            return

        # This would connect to real workflow engine streaming
        # For now, simulate updates
        import time

        try:
            for i in range(10):  # Simulate 10 updates
                time.sleep(1)

                update = {
                    "workflow_id": workflow_id,
                    "timestamp": datetime.now().isoformat(),
                    "type": "status_update",
                    "data": {
                        "step": i + 1,
                        "status": "processing" if i < 9 else "completed",
                        "message": f"Processing step {i + 1}/10",
                    },
                }

                yield f"data: {json.dumps(update)}\n\n"

            # Final completion message
            completion = {
                "workflow_id": workflow_id,
                "timestamp": datetime.now().isoformat(),
                "type": "completion",
                "data": {
                    "status": "completed",
                    "message": "Workflow completed successfully",
                },
            }
            yield f"data: {json.dumps(completion)}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    def create_workflow_diagram(
        self, agents: List[str], workflow_type: str = "sequential"
    ) -> str:
        """Create Mermaid diagram for workflow."""
        if workflow_type == "sequential":
            return self._create_sequential_diagram(agents)
        elif workflow_type == "parallel":
            return self._create_parallel_diagram(agents)
        else:
            return self._create_conditional_diagram(agents)

    def get_execution_timeline(self, workflow_id: str) -> List[Dict[str, Any]]:
        """Get execution timeline for workflow."""
        if workflow_id in self.workflow_cache:
            workflow_data = self.workflow_cache[workflow_id]
            return self._extract_timeline(workflow_data)

        return []

    def _create_visualization_data(self, workflow_data: Dict) -> Dict[str, Any]:
        """Create visualization data structure."""
        agents = workflow_data.get("agents", [])
        workflow_type = workflow_data.get("type", "sequential")

        return {
            "workflow_id": workflow_data.get("id", "unknown"),
            "type": workflow_type,
            "diagram": self.create_workflow_diagram(agents, workflow_type),
            "nodes": self._create_node_data(agents, workflow_data),
            "edges": self._create_edge_data(agents, workflow_type),
            "timeline": self.get_execution_timeline(workflow_data.get("id", "")),
            "status": workflow_data.get("status", "unknown"),
            "progress": self._calculate_progress(workflow_data),
        }

    def _create_node_data(self, agents: List[str], workflow_data: Dict) -> List[Dict]:
        """Create node data for visualization."""
        nodes = []

        for i, agent in enumerate(agents):
            status = self._get_agent_status(agent, workflow_data)

            nodes.append(
                {
                    "id": agent,
                    "label": agent.replace("_", " ").title(),
                    "type": "agent",
                    "status": status,
                    "position": {"x": i * 200, "y": 100},
                    "metadata": {
                        "execution_time": workflow_data.get("execution_times", {}).get(
                            agent, 0
                        ),
                        "tools_used": workflow_data.get("tools_used", {}).get(
                            agent, []
                        ),
                        "output_size": workflow_data.get("output_sizes", {}).get(
                            agent, 0
                        ),
                    },
                }
            )

        return nodes

    def _create_edge_data(self, agents: List[str], workflow_type: str) -> List[Dict]:
        """Create edge data for visualization."""
        edges = []

        if workflow_type == "sequential":
            for i in range(len(agents) - 1):
                edges.append(
                    {"from": agents[i], "to": agents[i + 1], "type": "sequential"}
                )
        elif workflow_type == "parallel":
            # All agents connect to a merge point
            for agent in agents:
                edges.append({"from": "start", "to": agent, "type": "parallel"})
                edges.append({"from": agent, "to": "merge", "type": "parallel"})

        return edges

    def _create_sequential_diagram(self, agents: List[str]) -> str:
        """Create Mermaid diagram for sequential workflow."""
        diagram = "graph TD\n"
        diagram += "    Start([Start])\n"

        for i, agent in enumerate(agents):
            agent_id = f"A{i+1}"
            agent_label = agent.replace("_", " ").title()
            diagram += f"    {agent_id}[{agent_label}]\n"

            if i == 0:
                diagram += f"    Start --> {agent_id}\n"
            else:
                prev_id = f"A{i}"
                diagram += f"    {prev_id} --> {agent_id}\n"

        diagram += f"    A{len(agents)} --> End([End])\n"

        # Add styling
        diagram += "\n    classDef startEnd fill:#e1f5fe\n"
        diagram += "    classDef agent fill:#f3e5f5\n"
        diagram += "    class Start,End startEnd\n"
        diagram += (
            f"    class {','.join([f'A{i+1}' for i in range(len(agents))])} agent\n"
        )

        return diagram

    def _create_parallel_diagram(self, agents: List[str]) -> str:
        """Create Mermaid diagram for parallel workflow."""
        diagram = "graph TD\n"
        diagram += "    Start([Start])\n"
        diagram += "    Merge([Merge Results])\n"
        diagram += "    End([End])\n"

        for i, agent in enumerate(agents):
            agent_id = f"A{i+1}"
            agent_label = agent.replace("_", " ").title()
            diagram += f"    {agent_id}[{agent_label}]\n"
            diagram += f"    Start --> {agent_id}\n"
            diagram += f"    {agent_id} --> Merge\n"

        diagram += "    Merge --> End\n"

        # Add styling
        diagram += "\n    classDef startEnd fill:#e1f5fe\n"
        diagram += "    classDef agent fill:#f3e5f5\n"
        diagram += "    classDef merge fill:#fff3e0\n"
        diagram += "    class Start,End startEnd\n"
        diagram += "    class Merge merge\n"
        diagram += (
            f"    class {','.join([f'A{i+1}' for i in range(len(agents))])} agent\n"
        )

        return diagram

    def _create_conditional_diagram(self, agents: List[str]) -> str:
        """Create Mermaid diagram for conditional workflow."""
        diagram = "graph TD\n"
        diagram += "    Start([Start])\n"
        diagram += "    Decision{Decision}\n"
        diagram += "    Start --> Decision\n"

        for i, agent in enumerate(agents):
            agent_id = f"A{i+1}"
            agent_label = agent.replace("_", " ").title()
            diagram += f"    {agent_id}[{agent_label}]\n"
            diagram += f"    Decision -->|Option {i+1}| {agent_id}\n"
            diagram += f"    {agent_id} --> End([End])\n"

        return diagram

    def _get_agent_status(self, agent: str, workflow_data: Dict) -> str:
        """Get current status of an agent in workflow."""
        if agent in workflow_data.get("completed", []):
            return "completed"
        elif agent in workflow_data.get("active", []):
            return "active"
        elif agent in workflow_data.get("failed", []):
            return "error"
        else:
            return "pending"

    def _calculate_progress(self, workflow_data: Dict) -> float:
        """Calculate overall workflow progress."""
        total_agents = len(workflow_data.get("agents", []))
        completed_agents = len(workflow_data.get("completed", []))

        if total_agents == 0:
            return 0.0

        return (completed_agents / total_agents) * 100

    def _extract_timeline(self, workflow_data: Dict) -> List[Dict[str, Any]]:
        """Extract execution timeline from workflow data."""
        timeline = []

        # This would extract real timeline data from workflow execution
        # For now, create sample timeline
        events = workflow_data.get("events", [])

        for event in events:
            timeline.append(
                {
                    "timestamp": event.get("timestamp", datetime.now().isoformat()),
                    "agent": event.get("agent", "unknown"),
                    "event_type": event.get("type", "execution"),
                    "message": event.get("message", "Agent executed"),
                    "duration": event.get("duration", 0),
                }
            )

        return sorted(timeline, key=lambda x: x["timestamp"])

    def get_workflow_statistics(self) -> Dict[str, Any]:
        """Get comprehensive workflow statistics."""
        try:
            # This would integrate with your actual workflow data
            return {
                "total_workflows": len(self.workflow_cache),
                "active_workflows": sum(
                    1
                    for w in self.workflow_cache.values()
                    if w.get("status") == "running"
                ),
                "success_rate": 0.85,  # Calculate from actual data
                "avg_execution_time": 5.2,  # Calculate from actual data
                "most_used_agents": ["email_extractor", "url_extractor"],
                "performance_trends": {
                    "last_hour": [1.2, 2.1, 1.8, 2.3, 1.9],
                    "success_rates": [0.9, 0.85, 0.92, 0.88, 0.87],
                },
            }
        except Exception as e:
            print(f"Error getting workflow statistics: {e}")
            return {}

    def create_mermaid_workflow_diagram(
        self, agents: List[str], status_data: Dict = None
    ) -> str:
        """Create a Mermaid diagram with real-time status."""
        diagram = "graph TD\n"
        diagram += "    Start([User Request])\n"

        for i, agent in enumerate(agents):
            agent_id = f"A{i+1}"
            agent_label = agent.replace("_", " ").title()

            # Determine status styling
            if status_data and agent in status_data:
                status = status_data[agent].get("status", "pending")
                if status == "completed":
                    diagram += f"    {agent_id}[{agent_label}]:::completed\n"
                elif status == "active":
                    diagram += f"    {agent_id}[{agent_label}]:::active\n"
                elif status == "error":
                    diagram += f"    {agent_id}[{agent_label}]:::error\n"
                else:
                    diagram += f"    {agent_id}[{agent_label}]:::pending\n"
            else:
                diagram += f"    {agent_id}[{agent_label}]\n"

            # Add connections
            if i == 0:
                diagram += f"    Start --> {agent_id}\n"
            else:
                diagram += f"    A{i} --> {agent_id}\n"

        diagram += f"    A{len(agents)} --> End([Response])\n"
        diagram += "\n"

        # Add CSS classes for styling
        diagram += "    classDef completed fill:#d4edda,stroke:#c3e6cb,color:#155724\n"
        diagram += "    classDef active fill:#fff3cd,stroke:#ffeaa7,color:#856404\n"
        diagram += "    classDef error fill:#f8d7da,stroke:#f5c6cb,color:#721c24\n"
        diagram += "    classDef pending fill:#f8f9fa,stroke:#dee2e6,color:#495057\n"

        return diagram

    def get_current_workflow_status(self) -> Dict[str, Any]:
        """Get current workflow execution status for sidebar display."""
        try:
            # Get active workflows from orchestrator service
            from flask_app.services.orchestrator_service import orchestrator_service

            active_workflows = orchestrator_service.get_active_workflows()

            if not active_workflows:
                return {
                    "status": "idle",
                    "message": "No active workflows",
                    "current_workflow": None,
                }

            # Get the most recent active workflow
            current = active_workflows[0]

            return {
                "status": "active",
                "message": f"Processing: {current.get('request', 'Unknown task')[:50]}...",
                "current_workflow": {
                    "id": current.get("workflow_id"),
                    "request": current.get("request"),
                    "status": current.get("status"),
                    "started_at": current.get("started_at"),
                    "progress": self._calculate_workflow_progress(current),
                },
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error getting workflow status: {str(e)}",
                "current_workflow": None,
            }

    def _calculate_workflow_progress(self, workflow_data: Dict) -> int:
        """Calculate workflow progress percentage."""
        # This is a simple calculation - you can make it more sophisticated
        if workflow_data.get("status") == "completed":
            return 100
        elif workflow_data.get("status") == "processing":
            return 50  # Assume 50% when processing
        else:
            return 0

    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get current workflow status."""
        if not self.is_available():
            return {
                "workflow_id": workflow_id,
                "status": "unavailable",
                "message": "Workflow engine not available",
            }

        try:
            if hasattr(self.workflow_engine, "get_workflow_status"):
                status = self.workflow_engine.get_workflow_status(workflow_id)
                if status:
                    return status

            # Return default status if workflow not found
            return {
                "workflow_id": workflow_id,
                "status": "not_found",
                "message": "Workflow not found",
            }

        except Exception as e:
            return {
                "workflow_id": workflow_id,
                "status": "error",
                "message": f"Error getting workflow status: {str(e)}",
            }

    def list_workflows(self) -> List[Dict[str, Any]]:
        """List all workflows."""
        if not self.is_available():
            return []

        try:
            if hasattr(self.workflow_engine, "list_workflows"):
                return self.workflow_engine.list_workflows()
            else:
                # Return empty list if method not available
                return []
        except Exception as e:
            print(f"Error listing workflows: {e}")
            return []


# Global service instance
workflow_service = WorkflowService()
