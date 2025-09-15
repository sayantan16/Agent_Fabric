"""
Multi-Agent Workflow Engine - Sequential processing with data flow
Location: core/workflow_engine.py
"""

import asyncio
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
import importlib.util
import json
from core.specialized_agents import (
    PDFAnalyzerAgent,
    ChartGeneratorAgent,
    TextProcessorAgent,
)
from core.intelligent_agent_base import DataAnalysisAgent


class MultiAgentWorkflowEngine:
    """Orchestrates sequential multi-agent workflows with intelligent data flow."""

    def __init__(self):
        self.agents = {
            "pdf_analyzer": PDFAnalyzerAgent(),
            "chart_generator": ChartGeneratorAgent(),
            "text_processor": TextProcessorAgent(),
            "data_analyzer": DataAnalysisAgent(),
        }
        self.workflow_state = {}
        self.dynamic_agents = {}

    async def execute_workflow(
        self, workflow_plan: Dict, request: str, files: List[Dict] = None
    ) -> Dict:
        """
        Execute multi-agent workflow with sequential processing and data flow.

        Args:
            workflow_plan: Plan from orchestrator with agent sequence
            request: Original user request
            files: Uploaded files with content

        Returns:
            Dict with complete workflow results
        """

        workflow_id = f"wf_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        start_time = datetime.now()

        # Initialize workflow state
        self.workflow_state = {
            "workflow_id": workflow_id,
            "request": request,
            "files": files or [],
            "current_data": None,
            "step_results": {},
            "data_flow": [],
            "errors": [],
            "started_at": start_time.isoformat(),
        }

        try:
            # Get agent sequence from plan
            agent_sequence = workflow_plan.get("agents", [])
            execution_strategy = workflow_plan.get("execution_strategy", "sequential")

            if execution_strategy == "sequential":
                results = await self._execute_sequential(agent_sequence, request, files)
            elif execution_strategy == "parallel":
                results = await self._execute_parallel(agent_sequence, request, files)
            else:
                # Default to sequential
                results = await self._execute_sequential(agent_sequence, request, files)

            # Compile final results
            execution_time = (datetime.now() - start_time).total_seconds()

            return {
                "status": "success",
                "workflow_id": workflow_id,
                "execution_time": execution_time,
                "results": results,
                "data_flow": self.workflow_state["data_flow"],
                "summary": self._generate_workflow_summary(results),
                "metadata": {
                    "agents_executed": len(agent_sequence),
                    "strategy": execution_strategy,
                    "files_processed": len(files) if files else 0,
                },
            }

        except Exception as e:
            return {
                "status": "error",
                "workflow_id": workflow_id,
                "error": str(e),
                "partial_results": self.workflow_state.get("step_results", {}),
                "data_flow": self.workflow_state.get("data_flow", []),
            }

    async def _execute_sequential(
        self, agent_sequence: List[str], request: str, files: List[Dict]
    ) -> Dict:
        """Execute agents sequentially with data flowing between steps."""

        results = {}
        current_data = None

        # Start with file data if available
        if files and files[0].get("read_success"):
            current_data = files[0]
            self.workflow_state["current_data"] = current_data

        for i, agent_name in enumerate(agent_sequence):
            print(f"Step {i+1}: Executing {agent_name}")

            # Get agent
            agent = self.agents.get(agent_name)
            if not agent:
                print(f"Agent {agent_name} not found, skipping")
                continue

            # Prepare context for this step
            step_context = {
                "step_number": i + 1,
                "total_steps": len(agent_sequence),
                "previous_results": results,
                "workflow_request": request,
            }

            # FIXED: Execute agent with proper method signature
            try:
                if agent_name in ["pdf_analyzer", "text_processor", "chart_generator"]:
                    # New specialized agents - use keyword arguments
                    step_result = await agent.execute(
                        request=request, file_data=current_data, context=step_context
                    )
                else:
                    # Old IntelligentAgent - use state format
                    state = {
                        "current_data": current_data,
                        "request": request,
                        "results": results,
                        "errors": [],
                        "execution_path": [],
                    }
                    step_result = await agent.execute(state)

            except Exception as e:
                print(f"Agent {agent_name} failed: {str(e)}")
                step_result = {"status": "error", "error": str(e), "data": None}

            # Store result
            results[agent_name] = step_result
            self.workflow_state["step_results"][agent_name] = step_result

            # Update data flow for next step
            if step_result.get("status") == "success":
                # Pass successful data to next agent
                data_output = step_result.get("data", {})

                # Create enriched data for next step
                if current_data:
                    # Merge new results with existing data
                    enhanced_data = {
                        **current_data,
                        "previous_analysis": data_output,
                        "step_history": results,
                    }
                else:
                    # Create new data structure
                    enhanced_data = {
                        "content": data_output,
                        "structure": "processed",
                        "previous_analysis": data_output,
                        "step_history": results,
                    }

                current_data = enhanced_data
                self.workflow_state["current_data"] = current_data

                # Log data flow
                self.workflow_state["data_flow"].append(
                    {
                        "from_step": agent_name,
                        "to_step": (
                            agent_sequence[i + 1]
                            if i + 1 < len(agent_sequence)
                            else "final"
                        ),
                        "data_type": type(data_output).__name__,
                        "data_size": len(str(data_output)) if data_output else 0,
                        "timestamp": datetime.now().isoformat(),
                    }
                )

                print(f"{agent_name} completed successfully")

            else:
                error_msg = step_result.get("error", "Unknown error")
                print(f"{agent_name} failed: {error_msg}")
                self.workflow_state["errors"].append(
                    {
                        "step": agent_name,
                        "error": error_msg,
                        "timestamp": datetime.now().isoformat(),
                    }
                )

        return results

    async def _execute_parallel(
        self, agent_sequence: List[str], request: str, files: List[Dict]
    ) -> Dict:
        """Execute agents in parallel (for independent tasks)."""

        print(f"🔄 Executing {len(agent_sequence)} agents in parallel")

        # Prepare tasks
        tasks = []
        for agent_name in agent_sequence:
            agent = self.agents.get(agent_name)
            if agent:
                # Each agent gets the original file data
                file_data = files[0] if files and files[0].get("read_success") else None
                task = agent.execute(
                    request=request,
                    file_data=file_data,
                    context={"execution_mode": "parallel"},
                )
                tasks.append((agent_name, task))

        # Execute all tasks concurrently
        results = {}
        task_results = await asyncio.gather(
            *[task for _, task in tasks], return_exceptions=True
        )

        # Process results
        for i, (agent_name, result) in enumerate(
            zip([name for name, _ in tasks], task_results)
        ):
            if isinstance(result, Exception):
                results[agent_name] = {
                    "status": "error",
                    "error": str(result),
                    "data": None,
                }
                print(f"❌ {agent_name} failed: {result}")
            else:
                results[agent_name] = result
                print(f"✅ {agent_name} completed")

        return results

    def _generate_workflow_summary(self, results: Dict) -> str:
        """Generate human-readable workflow summary - FIXED VERSION."""

        successful_agents = []
        failed_agents = []

        # FIXED: Handle different result structures safely
        for name, result in results.items():
            if isinstance(result, dict):
                if result.get("status") == "success":
                    successful_agents.append(name)
                elif result.get("status") == "error":
                    failed_agents.append(name)
                else:
                    # Unknown status, treat as successful if no error
                    successful_agents.append(name)
            elif isinstance(result, str):
                # String result - assume successful
                successful_agents.append(name)
            else:
                # Other type - assume successful
                successful_agents.append(name)

        summary_parts = []

        if successful_agents:
            summary_parts.append(
                f"✅ Successfully executed: {', '.join(successful_agents)}"
            )

            # Add key insights from each agent - FIXED with type checking
            for agent_name in successful_agents:
                result = results.get(agent_name, {})

                # Handle different result types
                if isinstance(result, dict):
                    data = result.get("data", {})

                    if (
                        agent_name == "pdf_analyzer"
                        and isinstance(data, dict)
                        and data.get("summary")
                    ):
                        summary_parts.append(
                            f"📄 PDF Analysis: {str(data['summary'])[:100]}..."
                        )

                    elif agent_name == "text_processor":
                        if isinstance(data, dict) and data.get("processed_text"):
                            summary_parts.append(
                                f"📝 Text Processing: {str(data['processed_text'])[:100]}..."
                            )
                        elif isinstance(data, str):
                            summary_parts.append(f"📝 Text Processing: {data[:100]}...")

                    elif (
                        agent_name == "chart_generator"
                        and isinstance(data, dict)
                        and data.get("chart_type")
                    ):
                        summary_parts.append(f"📊 Generated {data['chart_type']} chart")

                    elif agent_name == "data_analyzer":
                        summary_parts.append(
                            f"📈 Data Analysis: Key insights identified"
                        )

                elif isinstance(result, str):
                    # Handle string results
                    summary_parts.append(f"• {agent_name}: {result[:50]}...")

        if failed_agents:
            summary_parts.append(f"❌ Failed: {', '.join(failed_agents)}")

        return " | ".join(summary_parts) if summary_parts else "Workflow completed"

    def get_workflow_state(self) -> Dict:
        """Get current workflow state for debugging."""
        return self.workflow_state.copy()

    async def load_dynamic_agent(self, agent_name: str) -> Dict:
        """Load newly created agent into workflow engine"""

        if agent_name in self.dynamic_agents:
            return {"status": "already_loaded", "agent": agent_name}

        try:
            from core.registry_singleton import get_shared_registry

            registry = get_shared_registry()

            if not registry.agent_exists(agent_name):
                return {
                    "status": "error",
                    "error": f"Agent {agent_name} not found in registry",
                }

            agent_info = registry.get_agent(agent_name)
            agent_file = agent_info["location"]

            if not os.path.exists(agent_file):
                return {
                    "status": "error",
                    "error": f"Agent file not found: {agent_file}",
                }

            # Load agent module dynamically
            spec = importlib.util.spec_from_file_location(
                f"{agent_name}_module", agent_file
            )
            agent_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(agent_module)

            # Find agent function
            agent_function = getattr(agent_module, agent_name)

            # Create wrapper that matches existing agent interface
            class DynamicAgentWrapper:
                def __init__(self, func):
                    self.func = func
                    self.name = agent_name

                async def execute(
                    self, request: str, file_data: Dict = None, context: Dict = None
                ) -> Dict:
                    # Convert to format expected by dynamic agents
                    input_data = {
                        "request": request,
                        "file_data": file_data,
                        "context": context,
                    }
                    return self.func(input_data)

            # Cache the wrapped agent
            self.dynamic_agents[agent_name] = DynamicAgentWrapper(agent_function)

            return {"status": "success", "agent_loaded": agent_name}

        except Exception as e:
            return {
                "status": "error",
                "error": f"Failed to load agent {agent_name}: {str(e)}",
            }


class WorkflowPlanner:
    """Plans optimal multi-agent workflows based on requests and data."""

    def __init__(self):
        self.available_agents = {
            "pdf_analyzer": {
                "best_for": ["pdf", "document_analysis", "text_extraction"],
                "input_types": ["pdf", "document"],
                "output_types": ["analysis", "extracted_text", "insights"],
            },
            "text_processor": {
                "best_for": ["text_analysis", "entity_extraction", "sentiment"],
                "input_types": ["text", "string", "document"],
                "output_types": ["processed_text", "entities", "analysis"],
            },
            "chart_generator": {
                "best_for": ["visualization", "charts", "graphs", "plotting"],
                "input_types": ["tabular", "csv", "data"],
                "output_types": ["chart", "visualization", "graph"],
            },
            "data_analyzer": {
                "best_for": ["data_analysis", "statistics", "patterns"],
                "input_types": ["tabular", "csv", "numbers"],
                "output_types": ["analysis", "statistics", "insights"],
            },
        }

    def plan_workflow(self, request: str, files: List[Dict] = None) -> Dict:
        """Plan optimal workflow based on request and available data."""

        request_lower = request.lower()
        file_types = [f.get("structure", "unknown") for f in files] if files else []

        planned_agents = []
        execution_strategy = "sequential"  # Default to sequential for data flow

        # Analyze request intent
        if "pdf" in request_lower or "document" in request_lower or "pdf" in file_types:
            planned_agents.append("pdf_analyzer")

            # If also asking for charts/analysis, add those
            if any(
                word in request_lower
                for word in ["chart", "graph", "plot", "visualize"]
            ):
                planned_agents.append("chart_generator")
            if any(
                word in request_lower for word in ["analyze", "analysis", "insights"]
            ):
                planned_agents.append("text_processor")

        elif (
            "chart" in request_lower
            or "graph" in request_lower
            or "visualize" in request_lower
        ):
            # Data analysis first, then chart generation
            if "tabular" in file_types or "csv" in str(files).lower():
                planned_agents.extend(["data_analyzer", "chart_generator"])
            else:
                planned_agents.append("chart_generator")

        elif any(
            word in request_lower
            for word in ["analyze", "analysis", "extract", "process"]
        ):
            if "tabular" in file_types:
                planned_agents.append("data_analyzer")
            else:
                planned_agents.append("text_processor")

        # Default workflow
        if not planned_agents:
            if file_types:
                if "pdf" in file_types:
                    planned_agents.append("pdf_analyzer")
                elif "tabular" in file_types:
                    planned_agents.append("data_analyzer")
                else:
                    planned_agents.append("text_processor")
            else:
                planned_agents.append("text_processor")

        # FIXED: Always use sequential for multi-agent workflows to enable data flow
        if len(planned_agents) > 1:
            execution_strategy = "sequential"
        else:
            execution_strategy = (
                "sequential"  # Even single agents benefit from sequential processing
            )

        return {
            "agents": planned_agents,
            "execution_strategy": execution_strategy,
            "rationale": f"Selected {len(planned_agents)} agents based on request analysis",
            "data_flow_required": len(planned_agents) > 1,
        }
