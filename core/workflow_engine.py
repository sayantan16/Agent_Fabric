"""
Workflow Engine
Executes multi-agent workflows using LangGraph with advanced state management
"""

import os
import sys
import json
import asyncio
import importlib.util
from typing import Dict, List, Optional, Any, TypedDict, Callable
from datetime import datetime
from enum import Enum
import traceback

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from config import (
    WORKFLOW_STATE_SCHEMA,
    MAX_WORKFLOW_STEPS,
    WORKFLOW_TIMEOUT_SECONDS,
    AGENT_TIMEOUT_SECONDS,
    AGENT_MAX_RETRIES,
    ENABLE_PARALLEL_EXECUTION,
    MAX_PARALLEL_AGENTS,
    GENERATED_AGENTS_DIR,
    PREBUILT_AGENTS_DIR,
)
from core.registry import RegistryManager
from core.registry_singleton import get_shared_registry


class WorkflowState(TypedDict):
    """Enhanced state schema for workflow execution."""

    # Core fields
    request: str
    workflow_id: str
    workflow_type: str

    # Data flow
    current_data: Any
    files: List[Dict[str, Any]]
    context: Dict[str, Any]

    # Execution tracking
    execution_path: List[str]
    current_agent: Optional[str]
    pending_agents: List[str]
    completed_agents: List[str]

    # Results and errors
    results: Dict[str, Any]
    errors: List[Dict[str, str]]
    warnings: List[Dict[str, str]]

    # Metadata
    started_at: str
    completed_at: Optional[str]
    execution_metrics: Dict[str, float]
    retry_counts: Dict[str, int]

    # Control flow
    should_continue: bool
    next_agent: Optional[str]
    parallel_group: Optional[List[str]]


class ExecutionStatus(Enum):
    """Workflow execution statuses."""

    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"


class WorkflowEngine:
    """
    Advanced workflow execution engine using LangGraph.
    Handles complex multi-agent orchestration with state management.
    """

    def __init__(self):
        """Initialize the workflow engine."""
        self.registry = get_shared_registry()
        self.checkpointer = MemorySaver()
        self.loaded_agents = {}
        self.active_workflows = {}
        self.execution_cache = {}

    def create_workflow(
        self,
        agent_sequence: List[str],
        workflow_id: Optional[str] = None,
        workflow_type: str = "sequential",
    ) -> StateGraph:
        """
        Create a LangGraph workflow from agent sequence.

        Args:
            agent_sequence: List of agent names to execute
            workflow_id: Optional workflow identifier
            workflow_type: Type of workflow (sequential, parallel, conditional)

        Returns:
            Configured StateGraph ready for execution
        """
        # Validate agents exist
        validation_result = self._validate_agents(agent_sequence)
        if not validation_result["valid"]:
            raise ValueError(f"Invalid agents: {validation_result['errors']}")

        # Create the state graph
        workflow = StateGraph(WorkflowState)

        # Add nodes based on workflow type
        if workflow_type == "sequential":
            self._build_sequential_workflow(workflow, agent_sequence)
        elif workflow_type == "parallel":
            self._build_parallel_workflow(workflow, agent_sequence)
        elif workflow_type == "conditional":
            self._build_conditional_workflow(workflow, agent_sequence)
        else:
            self._build_hybrid_workflow(workflow, agent_sequence)

        # Compile with checkpointer for state persistence
        return workflow.compile(checkpointer=self.checkpointer)

    def execute_workflow(
        self,
        workflow: StateGraph,
        initial_data: Dict[str, Any],
        workflow_id: Optional[str] = None,
        timeout: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Execute a compiled workflow synchronously.
        """
        workflow_id = workflow_id or self._generate_workflow_id()
        timeout = timeout or WORKFLOW_TIMEOUT_SECONDS

        # Prepare initial state
        initial_state = self._prepare_initial_state(workflow_id, initial_data)

        # CRITICAL FIX: Ensure current_data is properly initialized
        if "current_data" not in initial_state or initial_state["current_data"] is None:
            # Set current_data from various possible sources
            if initial_data.get("text"):
                initial_state["current_data"] = initial_data["text"]
            elif initial_data.get("data"):
                initial_state["current_data"] = initial_data["data"]
            elif initial_data.get("request"):
                initial_state["current_data"] = initial_data["request"]
            else:
                initial_state["current_data"] = initial_data

        # Track workflow
        self.active_workflows[workflow_id] = {
            "status": ExecutionStatus.RUNNING,
            "started_at": initial_state["started_at"],
        }

        try:
            # Configure execution
            config = {
                "configurable": {"thread_id": workflow_id, "checkpoint_ns": workflow_id}
            }

            # Execute workflow with timeout
            final_state = self._execute_with_timeout(
                workflow, initial_state, config, timeout
            )

            # Mark completion
            final_state["completed_at"] = datetime.now().isoformat()
            final_state["execution_metrics"]["total_time"] = (
                datetime.fromisoformat(final_state["completed_at"])
                - datetime.fromisoformat(final_state["started_at"])
            ).total_seconds()

            # CRITICAL FIX: Determine success based on completed agents vs errors
            has_critical_errors = False
            if final_state.get("errors"):
                # Check if errors are critical (not just warnings)
                for error in final_state["errors"]:
                    if "critical" in str(error.get("error", "")).lower():
                        has_critical_errors = True
                        break

            # Success if we have results and no critical errors
            if final_state.get("results") and not has_critical_errors:
                status = ExecutionStatus.SUCCESS
            elif final_state.get("results") and final_state.get("errors"):
                status = ExecutionStatus.PARTIAL
            else:
                status = ExecutionStatus.FAILED

            # Update tracking
            self.active_workflows[workflow_id]["status"] = status

            # Update agent metrics
            self._update_agent_metrics(final_state)

            return final_state

        except Exception as e:
            # Handle execution failure
            self.active_workflows[workflow_id]["status"] = ExecutionStatus.FAILED

            return self._create_error_state(
                initial_state, f"Workflow execution failed: {str(e)}"
            )
        finally:
            # Clean up
            if workflow_id in self.active_workflows:
                del self.active_workflows[workflow_id]

    async def execute_workflow_async(
        self,
        workflow: StateGraph,
        initial_data: Dict[str, Any],
        workflow_id: Optional[str] = None,
        stream_callback: Optional[Callable] = None,
    ) -> Dict[str, Any]:
        """
        Execute workflow asynchronously with streaming support.

        Args:
            workflow: Compiled StateGraph
            initial_data: Initial data
            workflow_id: Optional workflow identifier
            stream_callback: Optional callback for streaming results

        Returns:
            Final workflow state
        """
        workflow_id = workflow_id or self._generate_workflow_id()

        # Prepare initial state
        initial_state = self._prepare_initial_state(workflow_id, initial_data)

        try:
            # Execute with streaming
            config = {
                "configurable": {"thread_id": workflow_id, "checkpoint_ns": workflow_id}
            }

            final_state = initial_state
            async for output in workflow.astream(initial_state, config):
                # Stream intermediate results
                if stream_callback:
                    await stream_callback(output)

                # Update state
                for key, value in output.items():
                    if key != "__end__":
                        final_state = value

            # Mark completion
            final_state["completed_at"] = datetime.now().isoformat()

            return final_state

        except Exception as e:
            return self._create_error_state(
                initial_state, f"Async execution failed: {str(e)}"
            )

    def _build_sequential_workflow(self, workflow: StateGraph, agents: List[str]):
        """Build sequential workflow structure."""
        for i, agent_name in enumerate(agents):
            # Create agent node
            agent_func = self._create_agent_node(agent_name)
            workflow.add_node(agent_name, agent_func)

            # Set edges
            if i == 0:
                workflow.set_entry_point(agent_name)

            if i < len(agents) - 1:
                # Add conditional edge for error handling
                workflow.add_conditional_edges(
                    agent_name, self._should_continue, {True: agents[i + 1], False: END}
                )
            else:
                workflow.add_edge(agent_name, END)

    def _build_parallel_workflow(self, workflow: StateGraph, agents: List[str]):
        """Build parallel workflow structure."""
        # Add parallel execution node
        parallel_node = self._create_parallel_node(agents)
        workflow.add_node("parallel_execution", parallel_node)

        # Add merge node
        merge_node = self._create_merge_node()
        workflow.add_node("merge_results", merge_node)

        # Set edges
        workflow.set_entry_point("parallel_execution")
        workflow.add_edge("parallel_execution", "merge_results")
        workflow.add_edge("merge_results", END)

    def _build_conditional_workflow(self, workflow: StateGraph, agents: List[str]):
        """Build conditional workflow structure."""
        # Add decision node
        decision_node = self._create_decision_node()
        workflow.add_node("decision", decision_node)

        # Add agent nodes
        for agent_name in agents:
            agent_func = self._create_agent_node(agent_name)
            workflow.add_node(agent_name, agent_func)
            workflow.add_edge(agent_name, END)

        # Set conditional routing
        workflow.set_entry_point("decision")

        # Create routing map
        route_map = {agent: agent for agent in agents}
        route_map["none"] = END

        workflow.add_conditional_edges("decision", self._route_decision, route_map)

    def _build_hybrid_workflow(self, workflow: StateGraph, agents: List[str]):
        """Build hybrid workflow with mixed patterns."""
        # This is a simplified hybrid - can be extended
        # For now, treat as sequential with parallel groups
        self._build_sequential_workflow(workflow, agents)

    def _create_agent_node(self, agent_name: str) -> Callable:
        """Create a node function for an agent."""

        def agent_node(state: WorkflowState) -> WorkflowState:
            """Execute agent and update state."""
            try:
                # Update current agent
                state["current_agent"] = agent_name

                # Check retry count
                if agent_name not in state["retry_counts"]:
                    state["retry_counts"][agent_name] = 0

                # Load and execute agent
                agent_func = self._load_agent(agent_name)

                # Record start time
                start_time = datetime.now()

                # CRITICAL FIX: Create a mutable copy of state for agent execution
                # This ensures the agent can modify state and changes are preserved
                agent_state = dict(state)  # Convert from TypedDict to regular dict

                # Execute with timeout
                import signal

                def timeout_handler(signum, frame):
                    raise TimeoutError(f"Agent {agent_name} timeout")

                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(AGENT_TIMEOUT_SECONDS)

                try:
                    # Execute agent with mutable state
                    agent_state = agent_func(agent_state)

                    # CRITICAL FIX: Merge agent state changes back into workflow state
                    for key, value in agent_state.items():
                        state[key] = value

                finally:
                    signal.alarm(0)

                # Record execution time
                execution_time = (datetime.now() - start_time).total_seconds()
                state["execution_metrics"][agent_name] = execution_time

                # Update tracking
                if agent_name not in state["execution_path"]:
                    state["execution_path"].append(agent_name)
                if agent_name not in state["completed_agents"]:
                    state["completed_agents"].append(agent_name)

                # CRITICAL FIX: Ensure current_data is available for next agent
                if agent_name in state.get("results", {}):
                    result = state["results"][agent_name]
                    if isinstance(result, dict) and "data" in result:
                        # Preserve current_data for next agent
                        state["current_data"] = result["data"]

                # Check for errors and handle properly
                if agent_name in state.get("results", {}):
                    result = state["results"][agent_name]
                    if isinstance(result, dict) and result.get("status") == "error":
                        # Handle agent error
                        if state["retry_counts"][agent_name] < AGENT_MAX_RETRIES:
                            state["retry_counts"][agent_name] += 1
                            state["warnings"].append(
                                {
                                    "agent": agent_name,
                                    "warning": f"Retry {state['retry_counts'][agent_name]}",
                                }
                            )
                            # Retry by re-executing
                            return agent_node(state)
                        else:
                            state["errors"].append(
                                {
                                    "agent": agent_name,
                                    "error": result.get("metadata", {}).get(
                                        "error", "Unknown error"
                                    ),
                                }
                            )
                            # Don't stop workflow for individual agent failures
                            # Let orchestrator decide based on overall results

                return state

            except Exception as e:
                # Record error
                state["errors"].append(
                    {
                        "agent": agent_name,
                        "error": str(e),
                        "traceback": traceback.format_exc(),
                    }
                )

                # Attempt retry
                if state["retry_counts"][agent_name] < AGENT_MAX_RETRIES:
                    state["retry_counts"][agent_name] += 1
                    return agent_node(state)

                # Don't set should_continue to False here
                # Let the workflow continue with other agents
                return state

        return agent_node

    def _create_parallel_node(self, agents: List[str]) -> Callable:
        """Create node for parallel execution."""

        def parallel_node(state: WorkflowState) -> WorkflowState:
            """Execute agents in parallel."""
            import concurrent.futures

            state["parallel_group"] = agents
            results = {}

            with concurrent.futures.ThreadPoolExecutor(
                max_workers=MAX_PARALLEL_AGENTS
            ) as executor:
                # Submit all agents
                futures = {}
                for agent_name in agents:
                    agent_func = self._load_agent(agent_name)
                    # Create copy of state for each agent
                    agent_state = state.copy()
                    future = executor.submit(agent_func, agent_state)
                    futures[future] = agent_name

                # Collect results
                for future in concurrent.futures.as_completed(
                    futures, timeout=WORKFLOW_TIMEOUT_SECONDS
                ):
                    agent_name = futures[future]
                    try:
                        agent_state = future.result()
                        if agent_name in agent_state.get("results", {}):
                            results[agent_name] = agent_state["results"][agent_name]
                        state["completed_agents"].append(agent_name)
                    except Exception as e:
                        state["errors"].append({"agent": agent_name, "error": str(e)})

            # Merge results
            state["results"].update(results)
            state["execution_path"].extend(agents)

            return state

        return parallel_node

    def _create_merge_node(self) -> Callable:
        """Create node for merging parallel results."""

        def merge_node(state: WorkflowState) -> WorkflowState:
            """Merge results from parallel execution."""
            # Aggregate data from all results
            merged_data = {}

            for agent_name, result in state.get("results", {}).items():
                if isinstance(result, dict) and result.get("status") == "success":
                    data = result.get("data", {})
                    if isinstance(data, dict):
                        merged_data.update(data)
                    else:
                        merged_data[agent_name] = data

            state["current_data"] = merged_data
            return state

        return merge_node

    def _create_decision_node(self) -> Callable:
        """Create node for conditional decisions."""

        def decision_node(state: WorkflowState) -> WorkflowState:
            """Make routing decision based on state."""
            # Analyze current data to determine next agent
            # This is a simplified implementation
            state["next_agent"] = self._determine_next_agent(state)
            return state

        return decision_node

    def _should_continue(self, state: WorkflowState) -> bool:
        """Determine if workflow should continue."""
        # Check explicit flag
        if not state.get("should_continue", True):
            return False

        # CRITICAL FIX: Don't stop on non-critical errors
        # Only stop if ALL agents have failed
        if state.get("errors"):
            # Count successful vs failed agents
            successful = len(
                [
                    a
                    for a in state.get("completed_agents", [])
                    if state.get("results", {}).get(a, {}).get("status") == "success"
                ]
            )

            # Continue if at least one agent succeeded
            if successful > 0:
                return True

            # Check if all agents have failed critically
            total_agents = len(state.get("execution_path", []))
            critical_errors = len(
                [
                    e
                    for e in state["errors"]
                    if "critical" in str(e.get("error", "")).lower()
                ]
            )

            # Stop only if all agents failed
            if total_agents > 0 and critical_errors >= total_agents:
                return False

        # Check step limit
        if len(state.get("execution_path", [])) >= MAX_WORKFLOW_STEPS:
            return False

        return True

    def _route_decision(self, state: WorkflowState) -> str:
        """Route to next agent based on decision."""
        return state.get("next_agent", "none")

    def _determine_next_agent(self, state: WorkflowState) -> str:
        """Determine next agent based on current state."""
        # Simple logic - can be enhanced
        current_data = state.get("current_data", {})

        # Check data type and route accordingly
        if isinstance(current_data, dict):
            if "emails" in current_data:
                return "email_processor"
            elif "numbers" in current_data:
                return "statistics_calculator"

        return "none"

    def _load_agent(self, agent_name: str) -> Callable:
        """Load an agent function dynamically."""

        print(f"DEBUG: Loading agent '{agent_name}'")

        # Check cache first
        if agent_name in self.loaded_agents:
            return self.loaded_agents[agent_name]

        # Get agent info from registry
        agent_info = self.registry.get_agent(agent_name)
        if not agent_info:
            print(f"DEBUG: Agent '{agent_name}' not found in registry")
            raise ValueError(f"Agent '{agent_name}' not found in registry")
        print(f"DEBUG: Agent info found: {agent_info.get('location')}")

        # Load the agent module
        agent_path = agent_info["location"]
        if not os.path.exists(agent_path):
            raise FileNotFoundError(f"Agent file not found: {agent_path}")

        # Import the module
        spec = importlib.util.spec_from_file_location(
            f"{agent_name}_module", agent_path
        )
        module = importlib.util.module_from_spec(spec)
        sys.modules[f"{agent_name}_module"] = module
        spec.loader.exec_module(module)

        # Get the agent function
        possible_names = [f"{agent_name}_agent", agent_name, "agent", "execute"]

        agent_func = None
        for name in possible_names:
            if hasattr(module, name):
                agent_func = getattr(module, name)
                break

        if not agent_func:
            raise AttributeError(f"No valid agent function found in {agent_path}")

        # Cache for future use
        self.loaded_agents[agent_name] = agent_func

        return agent_func

    def _validate_agents(self, agents: List[str]) -> Dict[str, Any]:
        """Validate that all agents exist and are valid."""

        print(f"DEBUG: Validating agents: {agents}")

        missing = []
        inactive = []

        for agent_name in agents:
            print(f"DEBUG: Checking agent '{agent_name}'")
            agent = self.registry.get_agent(agent_name)
            if not agent:
                print(f"DEBUG: Agent '{agent_name}' not found in registry")
                missing.append(agent_name)
            elif agent.get("status") != "active":
                print(f"DEBUG: Agent '{agent_name}' status: {agent.get('status')}")
                inactive.append(agent_name)
            else:
                print(f"DEBUG: Agent '{agent_name}' is valid and active")

        errors = []
        if missing:
            errors.append(f"Missing agents: {', '.join(missing)}")
        if inactive:
            errors.append(f"Inactive agents: {', '.join(inactive)}")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "missing": missing,
            "inactive": inactive,
        }

    def _prepare_initial_state(
        self, workflow_id: str, initial_data: Dict[str, Any]
    ) -> WorkflowState:
        """Prepare initial workflow state."""
        return {
            "request": initial_data.get("request", ""),
            "workflow_id": workflow_id,
            "workflow_type": initial_data.get("workflow_type", "sequential"),
            "current_data": initial_data,
            "files": initial_data.get("files", []),
            "context": initial_data.get("context", {}),
            "execution_path": [],
            "current_agent": None,
            "pending_agents": [],
            "completed_agents": [],
            "results": {},
            "errors": [],
            "warnings": [],
            "started_at": datetime.now().isoformat(),
            "completed_at": None,
            "execution_metrics": {},
            "retry_counts": {},
            "should_continue": True,
            "next_agent": None,
            "parallel_group": None,
        }

    def _execute_with_timeout(
        self,
        workflow: StateGraph,
        initial_state: WorkflowState,
        config: Dict,
        timeout: int,
    ) -> WorkflowState:
        """Execute workflow with timeout."""
        import threading

        result = [None]
        exception = [None]

        def run_workflow():
            try:
                final_state = initial_state
                for output in workflow.stream(initial_state, config):
                    if isinstance(output, dict):
                        for key, value in output.items():
                            if key != "__end__":
                                final_state = value
                result[0] = final_state
            except Exception as e:
                exception[0] = e

        thread = threading.Thread(target=run_workflow)
        thread.start()
        thread.join(timeout=timeout)

        if thread.is_alive():
            # Timeout occurred
            raise TimeoutError(f"Workflow timeout after {timeout} seconds")

        if exception[0]:
            raise exception[0]

        return result[0]

    def _update_agent_metrics(self, state: WorkflowState):
        """Update agent metrics in registry."""
        for agent_name in state.get("completed_agents", []):
            if agent_name in state.get("execution_metrics", {}):
                execution_time = state["execution_metrics"][agent_name]
                self.registry.update_agent_metrics(agent_name, execution_time)

    def _create_error_state(
        self, initial_state: WorkflowState, error_message: str
    ) -> WorkflowState:
        """Create error state for failed execution."""
        initial_state["errors"].append(
            {
                "agent": "workflow_engine",
                "error": error_message,
                "timestamp": datetime.now().isoformat(),
            }
        )
        initial_state["completed_at"] = datetime.now().isoformat()
        initial_state["should_continue"] = False
        return initial_state

    def _generate_workflow_id(self) -> str:
        """Generate unique workflow ID."""
        import random

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = random.randint(1000, 9999)
        return f"wf_{timestamp}_{random_suffix}"

    def get_workflow_status(self, workflow_id: str) -> Optional[Dict]:
        """Get status of a workflow."""
        return self.active_workflows.get(workflow_id)

    def cancel_workflow(self, workflow_id: str) -> bool:
        """Cancel an active workflow."""
        if workflow_id in self.active_workflows:
            self.active_workflows[workflow_id]["status"] = ExecutionStatus.CANCELLED
            return True
        return False

    def visualize_workflow(
        self, agent_sequence: List[str], workflow_type: str = "sequential"
    ) -> str:
        """Create text visualization of workflow."""
        viz = ["\nWorkflow Visualization"]
        viz.append("=" * 50)
        viz.append(f"Type: {workflow_type}")
        viz.append(f"Agents: {len(agent_sequence)}")
        viz.append("")

        if workflow_type == "sequential":
            viz.append("START")
            for i, agent in enumerate(agent_sequence):
                viz.append(f"  │")
                viz.append(f"  ▼")
                viz.append(f"[{i+1}. {agent}]")
                agent_info = self.registry.get_agent(agent)
                if agent_info:
                    viz.append(f"    {agent_info['description']}")
            viz.append(f"  │")
            viz.append(f"  ▼")
            viz.append("END")

        elif workflow_type == "parallel":
            viz.append("START")
            viz.append("  │")
            viz.append("  ▼")
            viz.append("[Parallel Execution]")
            for agent in agent_sequence:
                viz.append(f"  ├─> {agent}")
            viz.append("  │")
            viz.append("  ▼")
            viz.append("[Merge Results]")
            viz.append("  │")
            viz.append("  ▼")
            viz.append("END")

        return "\n".join(viz)
