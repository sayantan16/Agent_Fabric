"""
Pipeline Executor
Enhanced workflow execution engine for multi-step pipelines with data flow management
"""

import os
import sys
import json
import asyncio
import importlib.util
from typing import Dict, List, Optional, Any, TypedDict
from datetime import datetime
import traceback
import networkx as nx

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from config import (
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


class PipelineState(TypedDict):
    """Enhanced state schema for pipeline execution."""

    request: str
    pipeline_id: str
    current_step: int
    total_steps: int
    files: List[Dict]
    execution_path: List[str]
    step_results: Dict[str, Any]
    current_data: Any
    data_flow: Dict[str, Any]
    results: Dict[str, Any]
    errors: List[Dict]
    adaptations: List[Dict]
    started_at: str
    completed_at: Optional[str]


class PipelineExecutor:
    """
    Enhanced workflow execution engine for multi-step pipelines.
    Handles data flow, parallel execution, and real-time adaptation.
    """

    def __init__(self, registry: RegistryManager):
        """Initialize the pipeline executor."""
        self.registry = registry
        self.execution_history = []

    async def execute_pipeline(
        self, pipeline_plan: Dict, user_request: str, files: List[Dict] = None
    ) -> Dict[str, Any]:
        """
        Execute a complete pipeline with data flow management.

        Args:
            pipeline_plan: Complete pipeline execution plan
            user_request: Original user request
            files: Uploaded files

        Returns:
            Pipeline execution results
        """
        print(
            f"DEBUG: Executing pipeline {pipeline_plan.get('pipeline_id')} with {pipeline_plan.get('total_steps')} steps"
        )

        # Initialize pipeline state
        pipeline_state = PipelineState(
            request=user_request,
            pipeline_id=pipeline_plan.get(
                "pipeline_id", f"pipeline_{datetime.now().strftime('%H%M%S')}"
            ),
            current_step=0,
            total_steps=pipeline_plan.get("total_steps", 0),
            files=files or [],
            execution_path=[],
            step_results={},
            current_data={"user_request": user_request, "files": files},
            data_flow=pipeline_plan.get("data_flow", {}),
            results={},
            errors=[],
            adaptations=[],
            started_at=datetime.now().isoformat(),
            completed_at=None,
        )

        # Track execution
        self.execution_history.append(
            {
                "pipeline_id": pipeline_state["pipeline_id"],
                "started_at": pipeline_state["started_at"],
                "status": "in_progress",
            }
        )

        try:
            # Execute pipeline steps based on strategy
            execution_strategy = pipeline_plan.get("execution_strategy", "sequential")

            if execution_strategy == "sequential":
                final_state = await self._execute_sequential_pipeline(
                    pipeline_plan, pipeline_state
                )
            elif execution_strategy == "parallel":
                final_state = await self._execute_parallel_pipeline(
                    pipeline_plan, pipeline_state
                )
            else:
                final_state = await self._execute_sequential_pipeline(
                    pipeline_plan, pipeline_state
                )

            # Finalize execution
            final_state["completed_at"] = datetime.now().isoformat()

            # Determine final status
            if (
                final_state["current_step"] >= final_state["total_steps"]
                and not final_state["errors"]
            ):
                status = "success"
            elif final_state["current_step"] > 0:
                status = "partial"
            else:
                status = "failed"

            # Update execution history
            for exec_record in self.execution_history:
                if exec_record["pipeline_id"] == pipeline_state["pipeline_id"]:
                    exec_record["status"] = status
                    exec_record["completed_at"] = final_state["completed_at"]
                    break

            result = {
                "status": status,
                "pipeline_id": final_state["pipeline_id"],
                "steps_completed": final_state["current_step"],
                "total_steps": final_state["total_steps"],
                "results": final_state["results"],
                "step_results": final_state["step_results"],
                "errors": final_state["errors"],
                "adaptations": final_state["adaptations"],
                "execution_time": self._calculate_execution_time(
                    final_state["started_at"], final_state["completed_at"]
                ),
                "final_data": final_state["current_data"],
            }

            print(f"DEBUG: Pipeline execution completed - Status: {status}")
            return result

        except Exception as e:
            error_msg = f"Pipeline execution failed: {str(e)}"
            print(f"DEBUG: {error_msg}")

            return {
                "status": "error",
                "pipeline_id": pipeline_state["pipeline_id"],
                "error": error_msg,
                "steps_completed": pipeline_state["current_step"],
                "total_steps": pipeline_state["total_steps"],
                "results": pipeline_state["results"],
                "errors": pipeline_state["errors"]
                + [{"type": "execution_error", "message": error_msg}],
            }

    async def _execute_sequential_pipeline(
        self, pipeline_plan: Dict, state: PipelineState
    ) -> PipelineState:
        """Execute pipeline steps sequentially."""
        print(
            f"DEBUG: Executing sequential pipeline with {len(pipeline_plan['steps'])} steps"
        )

        for i, step_plan in enumerate(pipeline_plan["steps"]):
            print(
                f"DEBUG: Executing step {i+1}/{state['total_steps']}: {step_plan.get('name', 'unnamed')}"
            )

            state["current_step"] = i

            try:
                # Execute step with current data
                step_result = await self._execute_pipeline_step(step_plan, state)

                if step_result["status"] == "success":
                    # Update state with step results
                    state["step_results"][step_plan["name"]] = step_result
                    state["results"][step_plan["name"]] = step_result
                    state["execution_path"].append(step_plan["name"])

                    # Update current data for next step
                    state["current_data"] = self._extract_data_for_next_step(
                        step_result, step_plan, state
                    )

                    print(f"DEBUG: Step {i+1} completed successfully")

                else:
                    # Handle step failure
                    error_info = {
                        "step": step_plan["name"],
                        "step_index": i,
                        "error": step_result.get("error", "Unknown error"),
                        "timestamp": datetime.now().isoformat(),
                    }
                    state["errors"].append(error_info)

                    print(f"DEBUG: Step {i+1} failed: {error_info['error']}")

                    # For now, stop on first error (can be enhanced for recovery)
                    break

            except Exception as e:
                error_info = {
                    "step": step_plan["name"],
                    "step_index": i,
                    "error": str(e),
                    "type": "execution_exception",
                    "timestamp": datetime.now().isoformat(),
                }
                state["errors"].append(error_info)
                print(f"DEBUG: Step {i+1} exception: {str(e)}")
                break

        state["current_step"] = min(state["current_step"] + 1, state["total_steps"])
        return state

    async def _execute_parallel_pipeline(
        self, pipeline_plan: Dict, state: PipelineState
    ) -> PipelineState:
        """Execute pipeline steps in parallel where possible."""
        print(
            f"DEBUG: Executing parallel pipeline (not fully implemented - falling back to sequential)"
        )

        # For now, fall back to sequential execution
        # Can be enhanced to detect parallel opportunities
        return await self._execute_sequential_pipeline(pipeline_plan, state)

    async def _execute_pipeline_step(
        self, step_plan: Dict, state: PipelineState
    ) -> Dict[str, Any]:
        """
        Execute a single pipeline step with enhanced data handling.

        Args:
            step_plan: Step execution plan
            state: Current pipeline state

        Returns:
            Step execution result
        """
        agent_name = step_plan.get("agent_assigned")

        if not agent_name:
            return {
                "status": "error",
                "error": "No agent assigned to step",
                "step_name": step_plan.get("name", "unknown"),
            }

        try:
            # Load and execute the agent
            agent_result = await self._execute_agent_with_pipeline_context(
                agent_name, step_plan, state
            )
            return agent_result

        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "step_name": step_plan.get("name", "unknown"),
                "agent_name": agent_name,
            }

    def _get_agent_function_name(self, agent_name: str) -> str:
        """Smart function name resolution"""
        if agent_name.endswith("_agent"):
            return agent_name
        else:
            return f"{agent_name}_agent"

    async def _execute_agent_with_pipeline_context(
        self, agent_name: str, step_plan: Dict, state: PipelineState
    ) -> Dict[str, Any]:
        """Execute agent with pipeline context and enhanced data handling."""

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

        # Verify agent file exists
        if not os.path.exists(agent_path):
            return {
                "status": "error",
                "error": f"Agent file not found: {agent_path}",
                "agent_name": agent_name,
            }

        try:
            # Load agent module
            spec = importlib.util.spec_from_file_location(agent_name, agent_path)
            agent_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(agent_module)

            # Get agent function
            function_name = self._get_agent_function_name(agent_name)
            print(f"DEBUG: Looking for function: {function_name}")

            try:
                agent_function = getattr(agent_module, function_name)
                print(f"DEBUG: Found agent function: {function_name}")
            except AttributeError:
                # Try the other pattern
                fallback_name = (
                    agent_name
                    if agent_name.endswith("_agent")
                    else f"{agent_name}_agent"
                )
                if fallback_name != function_name:
                    try:
                        agent_function = getattr(agent_module, fallback_name)
                        print(f"DEBUG: Found with fallback: {fallback_name}")
                    except AttributeError:
                        available_funcs = [
                            name
                            for name in dir(agent_module)
                            if not name.startswith("_")
                        ]
                        print(f"DEBUG: Available functions: {available_funcs}")
                        raise AttributeError(
                            f"No agent function found. Tried: {function_name}, {fallback_name}"
                        )
                else:
                    available_funcs = [
                        name for name in dir(agent_module) if not name.startswith("_")
                    ]
                    print(f"DEBUG: Available functions: {available_funcs}")
                    raise AttributeError(f"Agent function not found: {function_name}")

            # Prepare agent state with pipeline context
            agent_state = self._prepare_agent_state_for_pipeline(state, step_plan)

            # Execute agent with timeout
            agent_result = await asyncio.wait_for(
                agent_function(agent_state), timeout=AGENT_TIMEOUT_SECONDS
            )

            # Validate and process result
            if isinstance(agent_result, dict):
                return self._process_agent_result(agent_result, agent_name, step_plan)
            else:
                return {
                    "status": "error",
                    "error": f"Agent returned invalid result type: {type(agent_result)}",
                    "agent_name": agent_name,
                }

        except asyncio.TimeoutError:
            return {
                "status": "error",
                "error": f"Agent execution timeout ({AGENT_TIMEOUT_SECONDS}s)",
                "agent_name": agent_name,
            }
        except Exception as e:
            return {
                "status": "error",
                "error": f"Agent execution failed: {str(e)}",
                "agent_name": agent_name,
                "traceback": traceback.format_exc(),
            }

    def _prepare_agent_state_for_pipeline(
        self, pipeline_state: PipelineState, step_plan: Dict
    ) -> Dict[str, Any]:
        """Prepare agent state with pipeline context and data."""

        # Base state structure
        agent_state = {
            "request": f"Pipeline step: {step_plan.get('description', step_plan.get('name', 'unknown'))}",
            "files": pipeline_state["files"],
            "current_data": pipeline_state["current_data"],
            "execution_path": pipeline_state["execution_path"].copy(),
            "results": {},
            "errors": [],
        }

        # Add pipeline context
        agent_state["pipeline_context"] = {
            "pipeline_id": pipeline_state["pipeline_id"],
            "step_index": pipeline_state["current_step"],
            "total_steps": pipeline_state["total_steps"],
            "step_name": step_plan.get("name", "unknown"),
            "previous_results": pipeline_state["step_results"],
            "data_flow": pipeline_state["data_flow"],
        }

        # Add step-specific requirements
        if "input_requirements" in step_plan:
            agent_state["input_requirements"] = step_plan["input_requirements"]

        if "output_requirements" in step_plan:
            agent_state["output_requirements"] = step_plan["output_requirements"]

        return agent_state

    def _process_agent_result(
        self, agent_result: Dict, agent_name: str, step_plan: Dict
    ) -> Dict[str, Any]:
        """Process and validate agent result."""

        # Check for valid agent result structure
        if "status" not in agent_result:
            agent_result["status"] = "success" if "data" in agent_result else "error"

        # Add metadata
        agent_result["agent_name"] = agent_name
        agent_result["step_name"] = step_plan.get("name", "unknown")
        agent_result["executed_at"] = datetime.now().isoformat()

        # Ensure metadata structure
        if "metadata" not in agent_result:
            agent_result["metadata"] = {}

        agent_result["metadata"]["step_index"] = step_plan.get("step_index", 0)
        agent_result["metadata"]["pipeline_step"] = True

        return agent_result

    def _extract_data_for_next_step(
        self, step_result: Dict, step_plan: Dict, state: PipelineState
    ) -> Any:
        """Extract appropriate data from step result for next step."""

        # Get the actual data from the step result
        if "data" in step_result:
            data = step_result["data"]
        else:
            data = step_result

        # For pipeline steps, we want to pass the processed data forward
        # This could be enhanced to handle specific data transformations

        # If the data is a dict with results, extract meaningful content
        if isinstance(data, dict):
            # Look for common result patterns
            if "processed_data" in data:
                return data["processed_data"]
            elif "extracted_data" in data:
                return data["extracted_data"]
            elif "results" in data:
                return data["results"]
            elif len(data) == 1:
                # If there's only one key, use its value
                return list(data.values())[0]

        # Default: return the data as-is
        return data

    def _calculate_execution_time(self, start_time: str, end_time: str) -> float:
        """Calculate execution time in seconds."""
        if not start_time or not end_time:
            return 0.0

        try:
            start = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
            end = datetime.fromisoformat(end_time.replace("Z", "+00:00"))
            return (end - start).total_seconds()
        except:
            return 0.0

    async def execute_step_with_recovery(
        self, step_plan: Dict, state: PipelineState, max_retries: int = 2
    ) -> Dict[str, Any]:
        """
        Execute a step with automatic recovery on failure.

        Args:
            step_plan: Step execution plan
            state: Current pipeline state
            max_retries: Maximum retry attempts

        Returns:
            Step execution result with recovery information
        """
        last_error = None

        for attempt in range(max_retries + 1):
            try:
                print(
                    f"DEBUG: Executing step (attempt {attempt + 1}/{max_retries + 1})"
                )

                result = await self._execute_pipeline_step(step_plan, state)

                if result["status"] == "success":
                    if attempt > 0:
                        result["recovery_info"] = {
                            "recovered": True,
                            "attempts": attempt + 1,
                            "last_error": str(last_error) if last_error else None,
                        }
                    return result
                else:
                    last_error = result.get("error", "Unknown error")
                    if attempt < max_retries:
                        print(f"DEBUG: Step failed, retrying... Error: {last_error}")
                        await asyncio.sleep(1)  # Brief delay before retry

            except Exception as e:
                last_error = str(e)
                if attempt < max_retries:
                    print(f"DEBUG: Step exception, retrying... Error: {last_error}")
                    await asyncio.sleep(1)

        # All attempts failed
        return {
            "status": "error",
            "error": f"Step failed after {max_retries + 1} attempts. Last error: {last_error}",
            "step_name": step_plan.get("name", "unknown"),
            "recovery_info": {
                "recovered": False,
                "attempts": max_retries + 1,
                "last_error": str(last_error),
            },
        }

    def get_execution_history(self) -> List[Dict]:
        """Get pipeline execution history."""
        return self.execution_history.copy()

    def create_data_flow_graph(self, pipeline_plan: Dict) -> nx.DiGraph:
        """Create a graph representing data flow in the pipeline."""
        graph = nx.DiGraph()

        steps = pipeline_plan.get("steps", [])

        for i, step in enumerate(steps):
            step_name = step.get("name", f"step_{i}")
            graph.add_node(step_name, **step)

            # Add edges based on data flow
            if i > 0:
                prev_step = steps[i - 1].get("name", f"step_{i-1}")
                graph.add_edge(prev_step, step_name)

        return graph

    def optimize_execution_order(self, pipeline_plan: Dict) -> Dict[str, Any]:
        """Optimize execution order for better performance."""
        # For now, return original plan
        # Can be enhanced to detect parallel opportunities

        optimized_plan = pipeline_plan.copy()
        optimized_plan["optimization_applied"] = False
        optimized_plan["optimization_notes"] = (
            "Sequential execution (no optimizations applied)"
        )

        return optimized_plan
