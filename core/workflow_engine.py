"""
Workflow Engine
Executes multi-agent workflows using LangGraph
"""

import sys
import os
from typing import Dict, List, Optional, Any, TypedDict
from datetime import datetime
import json
import importlib.util

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from core.registry import RegistryManager


class WorkflowState(TypedDict):
    """State schema for workflow execution."""

    # Core request info
    request: str
    files: List[Dict[str, Any]]

    # Execution tracking
    execution_path: List[str]
    current_agent: Optional[str]

    # Data flow
    current_data: Any
    results: Dict[str, Any]

    # Error handling
    errors: List[Dict[str, str]]

    # Metadata
    workflow_id: str
    started_at: str
    completed_at: Optional[str]


class WorkflowEngine:
    def __init__(self):
        self.registry = RegistryManager()
        self.checkpointer = MemorySaver()
        self.loaded_agents = {}

    def create_workflow(
        self, agent_sequence: List[str], workflow_id: str = None
    ) -> StateGraph:
        """
        Create a LangGraph workflow from a sequence of agents.

        Args:
            agent_sequence: List of agent names to execute in order
            workflow_id: Optional workflow identifier

        Returns:
            Configured StateGraph ready for execution
        """

        # Validate all agents exist
        missing_agents = []
        for agent_name in agent_sequence:
            if not self.registry.agent_exists(agent_name):
                missing_agents.append(agent_name)

        if missing_agents:
            raise ValueError(f"Missing agents: {', '.join(missing_agents)}")

        # Create the graph
        workflow = StateGraph(WorkflowState)

        # Load and add each agent as a node
        for agent_name in agent_sequence:
            agent_func = self._load_agent(agent_name)
            workflow.add_node(agent_name, agent_func)

        # Add edges to create sequential flow
        for i, agent_name in enumerate(agent_sequence):
            if i == 0:
                # First agent connects from START
                workflow.set_entry_point(agent_name)

            if i < len(agent_sequence) - 1:
                # Connect to next agent
                next_agent = agent_sequence[i + 1]
                workflow.add_edge(agent_name, next_agent)
            else:
                # Last agent connects to END
                workflow.add_edge(agent_name, END)

        # Compile the workflow
        return workflow.compile(checkpointer=self.checkpointer)

    def execute_workflow(
        self,
        workflow: StateGraph,
        initial_data: Dict[str, Any],
        workflow_id: str = None,
    ) -> Dict[str, Any]:
        """
        Execute a compiled workflow.

        Args:
            workflow: Compiled StateGraph
            initial_data: Initial data to pass to first agent
            workflow_id: Optional workflow identifier

        Returns:
            Final workflow state with all results
        """

        # Prepare initial state
        initial_state = {
            "request": initial_data.get("request", ""),
            "files": initial_data.get("files", []),
            "execution_path": [],
            "current_agent": None,
            "current_data": initial_data,
            "results": {},
            "errors": [],
            "workflow_id": workflow_id or self._generate_workflow_id(),
            "started_at": datetime.now().isoformat(),
            "completed_at": None,
        }

        try:
            # Execute the workflow
            config = {"configurable": {"thread_id": workflow_id or "default"}}

            # Run through all nodes
            final_state = None
            for output in workflow.stream(initial_state, config):
                final_state = output

                # Print progress for debugging
                if isinstance(output, dict):
                    for key, value in output.items():
                        if key != "__end__":
                            print(f"  Executed: {key}")
                            if isinstance(value, dict) and "errors" in value:
                                if value["errors"]:
                                    print(f"    Errors: {value['errors']}")

            # Extract the final state
            if final_state and "__end__" in final_state:
                result_state = final_state["__end__"]
            else:
                # Get the last non-end state
                result_state = final_state
                for key, value in final_state.items():
                    if key != "__end__":
                        result_state = value
                        break

            # Mark completion
            result_state["completed_at"] = datetime.now().isoformat()

            # Update agent metrics
            for agent_name in result_state.get("execution_path", []):
                # Simple timing estimate
                self.registry.update_agent_metrics(agent_name, 1.0)

            return result_state

        except Exception as e:
            # Return error state
            initial_state["errors"].append(
                {"agent": "workflow_engine", "error": str(e)}
            )
            initial_state["completed_at"] = datetime.now().isoformat()
            return initial_state

    def create_and_execute(
        self,
        agent_sequence: List[str],
        initial_data: Dict[str, Any],
        workflow_id: str = None,
    ) -> Dict[str, Any]:
        """
        Convenience method to create and execute a workflow in one step.

        Args:
            agent_sequence: List of agent names to execute
            initial_data: Initial data for the workflow
            workflow_id: Optional workflow identifier

        Returns:
            Final workflow state with results
        """

        workflow = self.create_workflow(agent_sequence, workflow_id)
        return self.execute_workflow(workflow, initial_data, workflow_id)

    def _load_agent(self, agent_name: str):
        """
        Dynamically load an agent function from its file.

        Args:
            agent_name: Name of the agent to load

        Returns:
            The agent function
        """

        # Check cache first
        if agent_name in self.loaded_agents:
            return self.loaded_agents[agent_name]

        # Get agent info from registry
        agent_info = self.registry.get_agent(agent_name)
        if not agent_info:
            raise ValueError(f"Agent '{agent_name}' not found in registry")

        # Load the agent module
        agent_path = agent_info["location"]
        if not os.path.exists(agent_path):
            raise FileNotFoundError(f"Agent file not found: {agent_path}")

        # Import the module
        spec = importlib.util.spec_from_file_location(f"{agent_name}_agent", agent_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Get the agent function
        # Try both patterns: agent_name_agent and agent_name
        func_name = f"{agent_name}_agent"
        if hasattr(module, func_name):
            agent_func = getattr(module, func_name)
        elif hasattr(module, agent_name):
            agent_func = getattr(module, agent_name)
        else:
            raise AttributeError(
                f"Agent function '{func_name}' not found in {agent_path}"
            )

        # Cache for future use
        self.loaded_agents[agent_name] = agent_func

        return agent_func

    def _generate_workflow_id(self) -> str:
        """Generate a unique workflow ID."""
        from datetime import datetime
        import random

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = random.randint(1000, 9999)
        return f"workflow_{timestamp}_{random_suffix}"

    def visualize_workflow(self, agent_sequence: List[str]) -> str:
        """
        Create a text visualization of the workflow.

        Args:
            agent_sequence: List of agent names

        Returns:
            Text representation of the workflow
        """

        visualization = "\nWorkflow Visualization:\n"
        visualization += "=" * 50 + "\n"

        for i, agent_name in enumerate(agent_sequence):
            agent_info = self.registry.get_agent(agent_name)

            # Node representation
            visualization += f"\n[{i+1}. {agent_name}]\n"

            if agent_info:
                visualization += f"    Description: {agent_info['description']}\n"
                visualization += (
                    f"    Uses tools: {', '.join(agent_info['uses_tools'])}\n"
                )

            # Edge representation
            if i < len(agent_sequence) - 1:
                visualization += "         |\n"
                visualization += "         v\n"
            else:
                visualization += "         |\n"
                visualization += "        END\n"

        visualization += "\n" + "=" * 50
        return visualization

    def get_available_workflows(self) -> Dict[str, List[str]]:
        """
        Get pre-defined workflow templates.

        Returns:
            Dictionary of workflow templates
        """

        return {
            "text_analysis": ["text_analyzer"],
            "document_extraction": ["document_processor"],
            "pdf_email": ["pdf_email_extractor"],
            "csv_statistics": ["csv_analyzer", "statistics_calculator"],
            "full_document_analysis": [
                "document_processor",
                "text_analyzer",
                "statistics_calculator",
            ],
        }

    def create_conditional_workflow(self, workflow_plan: Dict) -> StateGraph:
        """Create workflow with conditional routing."""

        workflow = StateGraph(WorkflowState)

        # Add all agent nodes
        for step in workflow_plan["workflow_steps"]:
            agent_name = step["agent"]
            agent_func = self._load_agent(agent_name)
            workflow.add_node(agent_name, agent_func)

        # Add conditional routing
        def route_condition(state):
            """Determine next node based on state."""
            last_result = (
                list(state.get("results", {}).values())[-1]
                if state.get("results")
                else None
            )

            if last_result and last_result.get("status") == "error":
                return "error_handler"

            # Check custom conditions from plan
            for step in workflow_plan["workflow_steps"]:
                if step.get("condition"):
                    # Evaluate condition
                    if eval(step["condition"], {"state": state}):
                        return step["agent"]

            return END

        # Add conditional edges
        workflow.add_conditional_edges(
            source="start",
            path=route_condition,
            path_map={
                node: node
                for node in [s["agent"] for s in workflow_plan["workflow_steps"]]
            },
        )

        return workflow.compile(checkpointer=self.checkpointer)

    def create_parallel_workflow(self, agents: List[str]) -> StateGraph:
        """Create workflow with parallel execution."""

        from langgraph.graph import StateGraph, END
        from langgraph.pregel import Channel

        workflow = StateGraph(WorkflowState)

        # Add parallel nodes
        parallel_nodes = []
        for agent_name in agents:
            agent_func = self._load_agent(agent_name)
            workflow.add_node(agent_name, agent_func)
            parallel_nodes.append(agent_name)

        # Add merge node
        def merge_results(state):
            """Merge results from parallel agents."""
            merged_data = {}
            for agent in parallel_nodes:
                if agent in state.get("results", {}):
                    result = state["results"][agent]
                    if result.get("status") == "success":
                        merged_data[agent] = result.get("data")

            state["current_data"] = merged_data
            return state

        workflow.add_node("merge", merge_results)

        # Connect parallel nodes to merge
        for node in parallel_nodes:
            workflow.add_edge(node, "merge")

        workflow.add_edge("merge", END)

        return workflow.compile(checkpointer=self.checkpointer)


class WorkflowCLI:
    """Command-line interface for testing workflows."""

    def __init__(self):
        self.engine = WorkflowEngine()
        self.registry = RegistryManager()

    def run(self):
        """Run interactive workflow execution."""

        print("\n" + "=" * 50)
        print("WORKFLOW ENGINE - Interactive Execution")
        print("=" * 50)

        # Show available agents
        print("\nAvailable Agents:")
        agents = self.registry.list_agents()
        for agent in agents:
            print(f"  - {agent['name']}: {agent['description']}")

        # Show pre-defined workflows
        print("\nPre-defined Workflows:")
        workflows = self.engine.get_available_workflows()
        for name, sequence in workflows.items():
            print(f"  - {name}: {' -> '.join(sequence)}")

        # Get user choice
        print("\nOptions:")
        print("1. Use pre-defined workflow")
        print("2. Create custom workflow")

        choice = input("\nChoice (1 or 2): ").strip()

        if choice == "1":
            # Use pre-defined
            workflow_name = input("Workflow name: ").strip()
            if workflow_name in workflows:
                agent_sequence = workflows[workflow_name]
            else:
                print("Invalid workflow name")
                return
        else:
            # Create custom
            print("\nEnter agent sequence (comma-separated):")
            sequence_input = input("Agents: ").strip()
            agent_sequence = [a.strip() for a in sequence_input.split(",")]

        # Get input data
        print("\nEnter input data:")
        input_type = input("Data type (text/file): ").strip().lower()

        if input_type == "file":
            file_path = input("File path: ").strip()
            initial_data = {
                "file_path": file_path,
                "request": f"Process file: {file_path}",
            }
        else:
            text = input("Enter text: ").strip()
            initial_data = {"text": text, "request": "Process text input"}

        # Show workflow visualization
        print(self.engine.visualize_workflow(agent_sequence))

        # Execute workflow
        print("\nExecuting workflow...")
        print("-" * 40)

        try:
            result = self.engine.create_and_execute(
                agent_sequence=agent_sequence, initial_data=initial_data
            )

            print("\n" + "-" * 40)
            print("Workflow completed!")

            # Show results
            print("\nExecution Path:")
            for agent in result.get("execution_path", []):
                print(f"  - {agent}")

            print("\nResults:")
            for agent_name, agent_result in result.get("results", {}).items():
                print(f"\n  [{agent_name}]")
                if isinstance(agent_result, dict):
                    print(f"    Status: {agent_result.get('status', 'unknown')}")
                    if "data" in agent_result:
                        print(
                            f"    Data: {json.dumps(agent_result['data'], indent=6)[:500]}"
                        )

            if result.get("errors"):
                print("\nErrors:")
                for error in result["errors"]:
                    print(f"  - {error['agent']}: {error['error']}")

        except Exception as e:
            print(f"Workflow execution failed: {str(e)}")


if __name__ == "__main__":
    cli = WorkflowCLI()
    cli.run()
