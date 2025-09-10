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

from core.pipeline_executor import PipelineExecutor
from core.workflow_intelligence import WorkflowIntelligence


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

    def __init__(self, registry=None):
        """Initialize the workflow engine with optional registry parameter."""
        # Use provided registry or get shared instance for consistency
        self.registry = registry if registry is not None else get_shared_registry()
        self.checkpointer = MemorySaver()
        self.loaded_agents = {}
        self.active_workflows = {}
        self.execution_cache = {}

        print(
            f"DEBUG: WorkflowEngine initialized with registry ID: {id(self.registry)}"
        )

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
        """Create a node function for an agent - ENHANCED VERSION."""

        def agent_node(state: WorkflowState) -> WorkflowState:
            """Execute agent and update state."""
            try:
                # Ensure current_data is properly set
                if "current_data" not in state or state["current_data"] is None:
                    # Enhanced data extraction logic
                    if state.get("request"):
                        state["current_data"] = state["request"]
                    elif state.get("text"):
                        state["current_data"] = state["text"]
                    elif state.get("data"):
                        state["current_data"] = state["data"]
                    elif state.get("files") and len(state["files"]) > 0:
                        # Try to use file content if available
                        state["current_data"] = state["files"][0]
                    elif state.get("results"):
                        # Get the last successful agent's output
                        for prev_agent in reversed(state.get("execution_path", [])):
                            if prev_agent in state["results"]:
                                result = state["results"][prev_agent]
                                if (
                                    isinstance(result, dict)
                                    and result.get("status") == "success"
                                ):
                                    state["current_data"] = result.get("data")
                                    break

                    # If still no data, provide empty dict to prevent errors
                    if state.get("current_data") is None:
                        state["current_data"] = {}
                        state["warnings"].append(
                            {
                                "agent": agent_name,
                                "warning": "No input data available, using empty dict",
                            }
                        )

                # Update current agent
                state["current_agent"] = agent_name

                # Check retry count
                if agent_name not in state["retry_counts"]:
                    state["retry_counts"][agent_name] = 0

                # Load and execute agent
                agent_func = self._load_agent(agent_name)

                # Record start time
                start_time = datetime.now()

                # Create mutable copy of state
                agent_state = dict(state)

                # Execute with timeout
                # Execute with timeout using threading instead of signal
                import threading
                import time

                def run_agent_with_timeout():
                    nonlocal agent_state, execution_error
                    try:
                        agent_state = agent_func(agent_state)
                    except Exception as e:
                        execution_error = e

                execution_error = None
                agent_thread = threading.Thread(target=run_agent_with_timeout)
                agent_thread.start()
                agent_thread.join(timeout=AGENT_TIMEOUT_SECONDS)

                if agent_thread.is_alive():
                    # Timeout occurred
                    state["errors"].append(
                        {
                            "agent": agent_name,
                            "error": f"Agent {agent_name} timeout after {AGENT_TIMEOUT_SECONDS}s",
                            "type": "timeout",
                        }
                    )
                    state["results"][agent_name] = {
                        "status": "error",
                        "data": None,
                        "metadata": {
                            "agent": agent_name,
                            "error": "Execution timeout",
                            "execution_time": AGENT_TIMEOUT_SECONDS,
                        },
                    }
                elif execution_error:
                    # Agent had an error
                    raise execution_error

                # Record execution time
                execution_time = (datetime.now() - start_time).total_seconds()
                state["execution_metrics"][agent_name] = execution_time

                # Update tracking
                if agent_name not in state["execution_path"]:
                    state["execution_path"].append(agent_name)
                if agent_name not in state["completed_agents"]:
                    state["completed_agents"].append(agent_name)

                # Ensure current_data is preserved for next agent
                if agent_name in state.get("results", {}):
                    result = state["results"][agent_name]
                    if (
                        isinstance(result, dict)
                        and result.get("status") == "success"
                        and "data" in result
                    ):
                        state["current_data"] = result["data"]

                return state

            except Exception as e:
                # Record error but don't crash workflow
                import traceback

                state["errors"].append(
                    {
                        "agent": agent_name,
                        "error": str(e),
                        "traceback": traceback.format_exc(),
                        "type": "execution_error",
                    }
                )

                # Create error result
                state["results"][agent_name] = {
                    "status": "error",
                    "data": None,
                    "metadata": {"agent": agent_name, "error": str(e)},
                }

                # Still mark as completed (with error)
                if agent_name not in state["completed_agents"]:
                    state["completed_agents"].append(agent_name)

                # Don't stop the workflow
                return state

        return agent_node

    def _create_parallel_node(self, agents: List[str]) -> Callable:
        """Create node for parallel execution - FIXED VERSION."""

        def parallel_node(state: WorkflowState) -> WorkflowState:
            """Execute agents in parallel without duplication."""
            import concurrent.futures

            state["parallel_group"] = agents
            results = {}

            # Track which agents have already been executed
            already_executed = set(state.get("completed_agents", []))
            agents_to_run = [a for a in agents if a not in already_executed]

            if not agents_to_run:
                print(f"All parallel agents already executed: {agents}")
                return state

            with concurrent.futures.ThreadPoolExecutor(
                max_workers=min(len(agents_to_run), MAX_PARALLEL_AGENTS)
            ) as executor:
                # Submit all agents that haven't run yet
                futures = {}
                for agent_name in agents_to_run:
                    try:
                        agent_func = self._load_agent(agent_name)
                        # Create copy of state for each agent
                        agent_state = dict(state)
                        agent_state["current_agent"] = agent_name

                        future = executor.submit(agent_func, agent_state)
                        futures[future] = agent_name
                    except Exception as e:
                        print(f"Failed to submit agent {agent_name}: {e}")
                        state["errors"].append(
                            {
                                "agent": agent_name,
                                "error": f"Failed to submit: {str(e)}",
                            }
                        )

                # Collect results with timeout
                for future in concurrent.futures.as_completed(
                    futures, timeout=WORKFLOW_TIMEOUT_SECONDS
                ):
                    agent_name = futures[future]
                    try:
                        agent_state = future.result(timeout=AGENT_TIMEOUT_SECONDS)

                        # Merge results back to main state
                        if agent_name in agent_state.get("results", {}):
                            results[agent_name] = agent_state["results"][agent_name]

                        # Update completed list (avoid duplicates)
                        if agent_name not in state["completed_agents"]:
                            state["completed_agents"].append(agent_name)

                        # Add to execution path once
                        if agent_name not in state["execution_path"]:
                            state["execution_path"].append(agent_name)

                    except concurrent.futures.TimeoutError:
                        state["errors"].append(
                            {
                                "agent": agent_name,
                                "error": f"Timeout after {AGENT_TIMEOUT_SECONDS}s",
                            }
                        )
                    except Exception as e:
                        state["errors"].append({"agent": agent_name, "error": str(e)})

            # Merge all results at once
            state["results"].update(results)

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

        # Get agent info from registry
        agent_info = self.registry.get_agent(agent_name)
        if not agent_info:
            print(f"DEBUG: Agent '{agent_name}' not found in registry")
            raise ValueError(f"Agent '{agent_name}' not found in registry")

        print(f"DEBUG: Agent info found: {agent_info.get('location')}")

        # Load the agent module
        agent_path = agent_info["location"]

        # FIX: Handle relative paths correctly
        if not os.path.isabs(agent_path):
            # Get project root (parent of current directory when running from flask_app)
            current_dir = os.getcwd()
            if current_dir.endswith("flask_app"):
                project_root = os.path.dirname(current_dir)
            else:
                project_root = current_dir
            agent_path = os.path.join(project_root, agent_path)

        print(f"DEBUG: Full agent path: {agent_path}")

        if not os.path.exists(agent_path):
            raise FileNotFoundError(f"Agent file not found: {agent_path}")

        # Import the module
        import importlib.util

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

        # Determine current_data from multiple possible sources
        current_data = (
            initial_data.get("current_data")
            or initial_data.get("text")
            or initial_data.get("data")
            or initial_data.get("request")
            or initial_data
        )

        return {
            "request": initial_data.get("request", ""),
            "workflow_id": workflow_id,
            "workflow_type": initial_data.get("workflow_type", "sequential"),
            "current_data": current_data,
            # IMPORTANT: Also preserve original fields
            "text": initial_data.get("text"),
            "data": initial_data.get("data"),
            "input": initial_data.get("input"),
            "files": initial_data.get("files", []),
            "context": initial_data.get("context", {}),
            "execution_path": initial_data.get("execution_path", []),
            "current_agent": None,
            "pending_agents": [],
            "completed_agents": [],
            "results": initial_data.get("results", {}),
            "errors": initial_data.get("errors", []),
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

    # ADD THESE NEW METHODS to the WorkflowEngine class:

    async def execute_pipeline_workflow(
        self, pipeline_plan: Dict, user_request: str, files: List[Dict] = None
    ) -> Dict[str, Any]:
        """
        Execute a multi-step pipeline workflow with intelligence and adaptation.

        Args:
            pipeline_plan: Complete pipeline execution plan
            user_request: Original user request
            files: Uploaded files

        Returns:
            Pipeline execution results
        """
        print(f"DEBUG: WorkflowEngine executing pipeline workflow")

        # Initialize pipeline executor
        pipeline_executor = PipelineExecutor(self.registry)
        workflow_intelligence = WorkflowIntelligence(self.registry)

        # Execute pipeline with monitoring
        execution_result = await self._execute_monitored_pipeline(
            pipeline_executor, workflow_intelligence, pipeline_plan, user_request, files
        )

        return execution_result

    async def _execute_monitored_pipeline(
        self,
        pipeline_executor: PipelineExecutor,
        workflow_intelligence: WorkflowIntelligence,
        pipeline_plan: Dict,
        user_request: str,
        files: List[Dict],
    ) -> Dict[str, Any]:
        """Execute pipeline with real-time monitoring and adaptation."""

        try:
            # Start pipeline execution
            result = await pipeline_executor.execute_pipeline(
                pipeline_plan, user_request, files
            )

            # Monitor and adapt if needed
            if result["status"] in ["partial", "failed"] and result.get("errors"):
                print(
                    f"DEBUG: Pipeline had issues, checking for adaptation opportunities"
                )

                # Analyze pipeline performance
                performance_analysis = (
                    workflow_intelligence.analyze_pipeline_performance(
                        result.get("pipeline_id", "unknown")
                    )
                )

                print(
                    f"DEBUG: Pipeline performance grade: {performance_analysis.get('performance_grade', 'unknown')}"
                )

                # Add performance metadata
                if "metadata" not in result:
                    result["metadata"] = {}
                result["metadata"]["performance_analysis"] = performance_analysis

            return result

        except Exception as e:
            print(f"DEBUG: Pipeline execution failed with exception: {str(e)}")
            return {
                "status": "error",
                "error": f"Pipeline execution failed: {str(e)}",
                "pipeline_id": pipeline_plan.get("pipeline_id", "unknown"),
                "results": {},
                "errors": [{"type": "execution_error", "message": str(e)}],
            }

    async def execute_agent(
        self, agent_name: str, state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a single agent with enhanced error handling for pipeline context.
        """
        print(f"DEBUG: Executing agent '{agent_name}' with pipeline support")

        # Check if agent exists
        if not self.registry.agent_exists(agent_name):
            return {
                "status": "error",
                "error": f"Agent '{agent_name}' not found",
                "agent_name": agent_name,
            }

        # Get agent details
        agent = self.registry.get_agent(agent_name)
        agent_path = agent["location"]

        # Handle relative paths correctly
        if not os.path.isabs(agent_path):
            current_dir = os.getcwd()
            if current_dir.endswith("flask_app"):
                project_root = os.path.dirname(current_dir)
            else:
                project_root = current_dir
            agent_path = os.path.join(project_root, agent_path)

        # Verify agent file exists
        if not os.path.exists(agent_path):
            return {
                "status": "error",
                "error": f"Agent file not found: {agent_path}",
                "agent_name": agent_name,
            }

        try:
            start_time = datetime.now()

            # Load agent module
            spec = importlib.util.spec_from_file_location(agent_name, agent_path)
            agent_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(agent_module)

            # FIXED: Get agent function with correct naming convention
            agent_function = getattr(agent_module, f"{agent_name}_agent")

            print(f"DEBUG: Found agent function: {agent_name}_agent")
            print(f"DEBUG: Input state keys: {list(state.keys())}")

            # FIXED: Execute synchronously (no await, no asyncio.wait_for)
            agent_result = agent_function(state)

            print(
                f"DEBUG: Agent function returned. Result keys: {list(agent_result.keys()) if isinstance(agent_result, dict) else type(agent_result)}"
            )

            # Calculate execution time
            execution_time = (datetime.now() - start_time).total_seconds()

            # FIXED: Extract result correctly from state structure
            if isinstance(agent_result, dict) and "results" in agent_result:
                if agent_name in agent_result["results"]:
                    result = agent_result["results"][agent_name]

                    # Add execution metadata if missing
                    if "metadata" not in result:
                        result["metadata"] = {}
                    result["metadata"]["execution_time"] = execution_time
                    result["metadata"]["agent_name"] = agent_name

                    print(f"DEBUG: Extracted result: {result}")
                    return result
                else:
                    return {
                        "status": "error",
                        "error": f"Agent '{agent_name}' did not produce expected result in state",
                        "available_results": list(
                            agent_result.get("results", {}).keys()
                        ),
                        "agent_name": agent_name,
                    }
            else:
                return {
                    "status": "error",
                    "error": f"Agent returned invalid state structure: {type(agent_result)}",
                    "agent_name": agent_name,
                }

        except AttributeError as e:
            if "has no attribute" in str(e):
                return {
                    "status": "error",
                    "error": f"Agent function '{agent_name}_agent' not found in module",
                    "agent_name": agent_name,
                    "traceback": traceback.format_exc(),
                }
            else:
                return {
                    "status": "error",
                    "error": f"Attribute error: {str(e)}",
                    "agent_name": agent_name,
                    "traceback": traceback.format_exc(),
                }
        except Exception as e:
            print(f"DEBUG: Agent execution failed with exception: {str(e)}")
            print(f"DEBUG: Full traceback: {traceback.format_exc()}")
            return {
                "status": "error",
                "error": f"Agent execution failed: {str(e)}",
                "agent_name": agent_name,
                "traceback": traceback.format_exc(),
            }

    def create_pipeline_state(
        self, request: str, pipeline_plan: Dict, files: List[Dict] = None
    ) -> Dict[str, Any]:
        """
        Create enhanced state for pipeline execution.

        Args:
            request: User request
            pipeline_plan: Pipeline execution plan
            files: Uploaded files

        Returns:
            Enhanced pipeline state
        """

        pipeline_state = {
            "request": request,
            "pipeline_id": pipeline_plan.get(
                "pipeline_id", f"pipeline_{datetime.now().strftime('%H%M%S')}"
            ),
            "files": files or [],
            "execution_path": [],
            "current_data": {"user_request": request, "files": files},
            "results": {},
            "errors": [],
            # Pipeline-specific fields
            "pipeline_context": {
                "total_steps": pipeline_plan.get("total_steps", 0),
                "current_step": 0,
                "execution_strategy": pipeline_plan.get(
                    "execution_strategy", "sequential"
                ),
                "data_flow": pipeline_plan.get("data_flow", {}),
                "step_plans": pipeline_plan.get("steps", []),
            },
            # Timing information
            "started_at": datetime.now().isoformat(),
            "completed_at": None,
            # Monitoring data
            "step_results": {},
            "adaptations": [],
            "performance_metrics": {
                "steps_completed": 0,
                "total_execution_time": 0,
                "average_step_time": 0,
            },
        }

        return pipeline_state

    async def execute_workflow_step(
        self, step_plan: Dict, pipeline_state: Dict, workflow_intelligence=None
    ) -> Dict[str, Any]:
        """
        Execute a single workflow step with monitoring.

        Args:
            step_plan: Individual step execution plan
            pipeline_state: Current pipeline state
            workflow_intelligence: Optional intelligence engine for monitoring

        Returns:
            Step execution result
        """

        agent_name = step_plan.get("agent_assigned")
        step_name = step_plan.get("name", "unnamed_step")

        print(f"DEBUG: Executing workflow step: {step_name} with agent: {agent_name}")

        if not agent_name:
            return {
                "status": "error",
                "error": "No agent assigned to step",
                "step_name": step_name,
            }

        try:
            # Update pipeline context for this step
            pipeline_state["pipeline_context"]["current_step"] = step_plan.get(
                "step_index", 0
            )
            pipeline_state["pipeline_context"]["current_step_name"] = step_name

            # Execute the agent
            step_result = await self.execute_agent(agent_name, pipeline_state)

            # Add step metadata
            step_result["step_name"] = step_name
            step_result["step_index"] = step_plan.get("step_index", 0)

            # Monitor execution if intelligence engine provided
            if workflow_intelligence and step_result:
                monitoring_result = (
                    await workflow_intelligence.monitor_pipeline_execution(
                        pipeline_state, step_result
                    )
                )

                # Handle adaptation if needed
                if monitoring_result.get("adaptation_needed"):
                    adaptation_strategy = monitoring_result.get("adaptation_strategy")
                    if adaptation_strategy:
                        print(f"DEBUG: Executing adaptation for step: {step_name}")

                        adaptation_result = (
                            await workflow_intelligence.execute_adaptation(
                                adaptation_strategy, pipeline_state, step_plan
                            )
                        )

                        # Update step result if adaptation succeeded
                        if adaptation_result.get("status") == "success":
                            step_result = adaptation_result.get(
                                "recovery_result", step_result
                            )
                            step_result["adaptation_applied"] = True
                            step_result["adaptation_details"] = adaptation_result

            return step_result

        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "step_name": step_name,
                "agent_name": agent_name,
            }

    def validate_pipeline_state(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and fix pipeline state structure.

        Args:
            state: Pipeline state to validate

        Returns:
            Validation result with fixes applied
        """

        validation_result = {"valid": True, "issues_found": [], "fixes_applied": []}

        # Check required fields
        required_fields = ["request", "results", "errors", "execution_path"]
        for field in required_fields:
            if field not in state:
                state[field] = (
                    []
                    if field in ["errors", "execution_path"]
                    else ({} if field == "results" else "")
                )
                validation_result["fixes_applied"].append(
                    f"Added missing field: {field}"
                )

        # Check pipeline context
        if "pipeline_context" not in state:
            state["pipeline_context"] = {
                "total_steps": 0,
                "current_step": 0,
                "execution_strategy": "sequential",
            }
            validation_result["fixes_applied"].append("Added missing pipeline_context")

        # Validate data types
        if not isinstance(state["results"], dict):
            state["results"] = {}
            validation_result["fixes_applied"].append("Fixed results field type")

        if not isinstance(state["errors"], list):
            state["errors"] = []
            validation_result["fixes_applied"].append("Fixed errors field type")

        if not isinstance(state["execution_path"], list):
            state["execution_path"] = []
            validation_result["fixes_applied"].append("Fixed execution_path field type")

        # Check for issues
        if len(validation_result["fixes_applied"]) > 0:
            validation_result["valid"] = False
            validation_result["issues_found"] = [
                f"Structure issues fixed: {len(validation_result['fixes_applied'])} problems"
            ]

        return validation_result

    def get_pipeline_progress(self, pipeline_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get current pipeline execution progress.

        Args:
            pipeline_state: Current pipeline state

        Returns:
            Progress information
        """

        pipeline_context = pipeline_state.get("pipeline_context", {})

        current_step = pipeline_context.get("current_step", 0)
        total_steps = pipeline_context.get("total_steps", 0)

        # Calculate progress percentage
        progress_percent = (current_step / total_steps * 100) if total_steps > 0 else 0

        # Get timing information
        started_at = pipeline_state.get("started_at")
        current_time = datetime.now().isoformat()

        # Calculate elapsed time
        elapsed_time = 0
        if started_at:
            try:
                start = datetime.fromisoformat(started_at.replace("Z", "+00:00"))
                now = datetime.now()
                elapsed_time = (now - start).total_seconds()
            except:
                pass

        # Get step results summary
        step_results = pipeline_state.get("step_results", {})
        successful_steps = len(
            [r for r in step_results.values() if r.get("status") == "success"]
        )
        failed_steps = len(
            [r for r in step_results.values() if r.get("status") == "error"]
        )

        progress_info = {
            "pipeline_id": pipeline_state.get("pipeline_id", "unknown"),
            "current_step": current_step,
            "total_steps": total_steps,
            "progress_percent": round(progress_percent, 1),
            "successful_steps": successful_steps,
            "failed_steps": failed_steps,
            "elapsed_time": round(elapsed_time, 1),
            "execution_strategy": pipeline_context.get(
                "execution_strategy", "sequential"
            ),
            "status": "in_progress" if current_step < total_steps else "completed",
            "errors_count": len(pipeline_state.get("errors", [])),
            "adaptations_count": len(pipeline_state.get("adaptations", [])),
        }

        return progress_info
