"""
Enhanced Multi-Agent Workflow Engine - AI-driven execution with context awareness
Location: core/workflow_engine.py (REPLACE EXISTING FILE)

This enhanced version integrates with the AI workflow planner and provides
context-aware agent execution with intelligent data flow.
"""

import asyncio
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
import importlib.util
import json

from anthropic import Anthropic
from config import ANTHROPIC_API_KEY, CLAUDE_MODEL
from core.specialized_agents import (
    PDFAnalyzerAgent,
    ChartGeneratorAgent,
    TextProcessorAgent,
)
from core.intelligent_agent_base import DataAnalysisAgent


class EnhancedMultiAgentWorkflowEngine:
    """
    AI-powered workflow engine that executes intelligent multi-agent workflows
    with context awareness and optimal data flow.
    """

    def __init__(self):
        self.agents = {
            "pdf_analyzer": PDFAnalyzerAgent(),
            "chart_generator": ChartGeneratorAgent(),
            "text_processor": TextProcessorAgent(),
            "data_analyzer": DataAnalysisAgent(),
        }
        self.workflow_state = {}
        self.dynamic_agents = {}

    async def execute_ai_planned_workflow(
        self, ai_workflow_plan: Dict, request: str, files: List[Dict] = None
    ) -> Dict:
        """
        Execute AI-planned workflow with context-aware agent coordination.

        Args:
            ai_workflow_plan: Plan from AIWorkflowPlanner
            request: Original user request
            files: Uploaded files with content

        Returns:
            Dict with comprehensive workflow results
        """

        workflow_id = f"ai_wf_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        start_time = datetime.now()

        # Initialize enhanced workflow state
        self.workflow_state = {
            "workflow_id": workflow_id,
            "workflow_type": "ai_planned",
            "request": request,
            "files": files or [],
            "ai_plan": ai_workflow_plan,
            "current_data": None,
            "step_results": {},
            "context_flow": [],
            "data_flow": [],
            "errors": [],
            "started_at": start_time.isoformat(),
            "agent_contexts": {},
        }

        try:
            # Get AI-planned execution strategy
            agent_sequence = ai_workflow_plan.get("agents", [])
            execution_strategy = ai_workflow_plan.get(
                "execution_strategy", "sequential"
            )
            agent_instructions = ai_workflow_plan.get("agent_instructions", {})

            print(f"🤖 Executing AI-planned workflow: {agent_sequence}")
            print(f"📋 Strategy: {execution_strategy}")

            # Execute based on AI-determined strategy
            if execution_strategy == "sequential":
                results = await self._execute_ai_sequential(
                    agent_sequence, request, files, agent_instructions, ai_workflow_plan
                )
            elif execution_strategy == "parallel":
                results = await self._execute_ai_parallel(
                    agent_sequence, request, files, agent_instructions, ai_workflow_plan
                )
            else:
                # Default to AI-guided sequential
                results = await self._execute_ai_sequential(
                    agent_sequence, request, files, agent_instructions, ai_workflow_plan
                )

            # Compile comprehensive results
            execution_time = (datetime.now() - start_time).total_seconds()

            # NEW: AI-powered response synthesis
            synthesizer = AIResponseSynthesizer()

            execution_metadata = {
                "execution_time": execution_time,
                "dynamic_agents_created": ai_workflow_plan.get("agents_created", 0),
                "agents_executed": len(agent_sequence),
                "strategy": execution_strategy,
            }

            # Generate natural language response
            ai_response = await synthesizer.synthesize_final_response(
                original_request=request,
                workflow_results=results,
                scenario_key=ai_workflow_plan.get("scenario"),
                execution_metadata=execution_metadata,
            )

            return {
                "status": "success",
                "workflow_id": workflow_id,
                "execution_time": execution_time,
                "results": results,
                "ai_response": ai_response,  # NEW: Natural language response
                "data_flow": self.workflow_state["data_flow"],
                "context_flow": self.workflow_state["context_flow"],
                "summary": self._generate_ai_workflow_summary(
                    results, ai_workflow_plan
                ),
                "ai_plan_used": ai_workflow_plan,
                "metadata": {
                    "agents_executed": len(agent_sequence),
                    "strategy": execution_strategy,
                    "files_processed": len(files) if files else 0,
                    "ai_confidence": ai_workflow_plan.get("confidence", 0.8),
                    "complexity": ai_workflow_plan.get("complexity", "medium"),
                    "planning_type": "ai_driven",
                },
            }

        except Exception as e:
            return {
                "status": "error",
                "workflow_id": workflow_id,
                "error": str(e),
                "partial_results": self.workflow_state.get("step_results", {}),
                "data_flow": self.workflow_state.get("data_flow", []),
                "ai_plan_attempted": ai_workflow_plan,
            }

    async def _execute_ai_sequential(
        self,
        agent_sequence: List[str],
        request: str,
        files: List[Dict],
        agent_instructions: Dict,
        ai_plan: Dict,
    ) -> Dict:
        """Execute agents sequentially with AI-guided context awareness."""

        results = {}
        current_data = None
        workflow_context = self._build_workflow_context(request, ai_plan)

        # Initialize with file data if available
        if files and files[0].get("read_success"):
            current_data = files[0]
            self.workflow_state["current_data"] = current_data

        for i, agent_name in enumerate(agent_sequence):
            print(f"🔄 Step {i+1}/{len(agent_sequence)}: Executing {agent_name}")

            # Get agent
            agent = await self._get_or_load_agent(agent_name)
            if not agent:
                print(f"❌ Agent {agent_name} not found, skipping")
                continue

            # Build context-aware step context
            step_context = self._build_step_context(
                i,
                agent_name,
                agent_sequence,
                workflow_context,
                agent_instructions,
                results,
                current_data,
            )

            # Execute agent with full context awareness
            try:
                step_result = await self._execute_context_aware_agent(
                    agent, agent_name, request, current_data, step_context
                )

                print(
                    f"✅ {agent_name} completed with status: {step_result.get('status', 'unknown')}"
                )

            except Exception as e:
                print(f"❌ {agent_name} failed with exception: {str(e)}")
                step_result = {"status": "error", "error": str(e), "data": None}

            # Store and process result
            results[agent_name] = step_result
            self.workflow_state["step_results"][agent_name] = step_result

            # Intelligent data flow management
            if step_result.get("status") == "success":
                current_data = await self._process_step_data_flow(
                    agent_name,
                    step_result,
                    current_data,
                    i,
                    agent_sequence,
                    step_context,
                )

                # Log context flow
                self.workflow_state["context_flow"].append(
                    {
                        "step": i + 1,
                        "agent": agent_name,
                        "context_received": step_context.get("workflow_position", ""),
                        "data_transformed": bool(step_result.get("data")),
                        "next_step_prepared": i + 1 < len(agent_sequence),
                        "timestamp": datetime.now().isoformat(),
                    }
                )

            else:
                # Handle step failure with context
                await self._handle_step_failure(
                    agent_name, step_result, i, agent_sequence, workflow_context
                )

        return results

    async def _execute_ai_parallel(
        self,
        agent_sequence: List[str],
        request: str,
        files: List[Dict],
        agent_instructions: Dict,
        ai_plan: Dict,
    ) -> Dict:
        """Execute agents in parallel with AI coordination."""

        print(f"⚡ Executing {len(agent_sequence)} agents in parallel")

        workflow_context = self._build_workflow_context(request, ai_plan)

        # Prepare parallel tasks with context
        tasks = []
        for i, agent_name in enumerate(agent_sequence):
            agent = await self._get_or_load_agent(agent_name)
            if agent:
                step_context = self._build_step_context(
                    i,
                    agent_name,
                    agent_sequence,
                    workflow_context,
                    agent_instructions,
                    {},
                    files[0] if files else None,
                )

                file_data = files[0] if files and files[0].get("read_success") else None
                task = self._execute_context_aware_agent(
                    agent, agent_name, request, file_data, step_context
                )
                tasks.append((agent_name, task))

        # Execute all tasks concurrently
        results = {}
        task_results = await asyncio.gather(
            *[task for _, task in tasks], return_exceptions=True
        )

        # Process parallel results
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
                print(f"✅ {agent_name} completed in parallel")

        return results

    def _build_workflow_context(self, request: str, ai_plan: Dict) -> Dict:
        """Build comprehensive workflow context for agents."""
        return {
            "original_request": request,
            "workflow_goal": ai_plan.get("context_analysis", {}).get(
                "user_goal", request
            ),
            "total_steps": len(ai_plan.get("agents", [])),
            "execution_strategy": ai_plan.get("execution_strategy", "sequential"),
            "complexity": ai_plan.get("complexity", "medium"),
            "data_flow_plan": ai_plan.get("data_flow", {}),
            "workflow_rationale": ai_plan.get("rationale", ""),
            "estimated_duration": ai_plan.get("estimated_duration", "unknown"),
        }

    def _build_step_context(
        self,
        step_index: int,
        agent_name: str,
        agent_sequence: List[str],
        workflow_context: Dict,
        agent_instructions: Dict,
        previous_results: Dict,
        current_data: Any,
    ) -> Dict:
        """Build context-aware step context for agent execution."""

        # Get AI-generated instructions for this agent
        specific_instructions = agent_instructions.get(agent_name, {})

        return {
            "step_number": step_index + 1,
            "total_steps": len(agent_sequence),
            "agent_name": agent_name,
            "workflow_position": f"Step {step_index + 1} of {len(agent_sequence)}",
            "is_first_step": step_index == 0,
            "is_last_step": step_index == len(agent_sequence) - 1,
            "next_agent": (
                agent_sequence[step_index + 1]
                if step_index + 1 < len(agent_sequence)
                else None
            ),
            "previous_agent": (
                agent_sequence[step_index - 1] if step_index > 0 else None
            ),
            # AI-generated context
            "primary_task": specific_instructions.get("primary_task", "Process data"),
            "input_expectations": specific_instructions.get("input_expectations", ""),
            "processing_focus": specific_instructions.get("processing_focus", ""),
            "output_requirements": specific_instructions.get("output_requirements", ""),
            "context_awareness": specific_instructions.get("context_awareness", ""),
            "success_criteria": specific_instructions.get("success_criteria", ""),
            # Workflow context
            "workflow_context": workflow_context,
            "previous_results": previous_results,
            "data_available": current_data is not None,
            "execution_mode": "context_aware_ai",
        }

    async def _execute_context_aware_agent(
        self,
        agent: Any,
        agent_name: str,
        request: str,
        file_data: Dict,
        step_context: Dict,
    ) -> Dict:
        """FIXED: Execute agent with full context awareness."""

        print(f"DEBUG: Executing agent {agent_name} with context")

        # Build state for agent execution
        state = {
            "current_data": file_data,
            "request": request,
            "results": step_context.get("previous_results", {}),
            "errors": [],
            "execution_path": [],
            "context": step_context,
        }

        try:
            # Execute the agent
            if hasattr(agent, "execute"):
                result = await agent.execute(state)
                print(f"DEBUG: Agent {agent_name} returned: {type(result)}")

                # Handle different result formats
                if isinstance(result, dict):
                    if "status" in result:
                        # Already in correct format
                        return result
                    elif "results" in result and agent_name in result["results"]:
                        # Extract agent-specific result
                        return result["results"][agent_name]
                    else:
                        # Wrap in standard format
                        return {
                            "status": "success",
                            "data": result,
                            "metadata": {"agent": agent_name},
                        }
                else:
                    return {
                        "status": "success",
                        "data": result,
                        "metadata": {"agent": agent_name},
                    }
            else:
                return {
                    "status": "error",
                    "error": f"Agent {agent_name} has no execute method",
                }

        except Exception as e:
            print(f"DEBUG: Agent execution exception: {str(e)}")
            return {"status": "error", "error": str(e)}

    def _build_enhanced_request(self, original_request: str, step_context: Dict) -> str:
        """Build context-enhanced request for agent execution."""

        base_request = original_request

        # Add context-aware instructions
        context_parts = [
            f"ORIGINAL REQUEST: {original_request}",
            f"YOUR ROLE: {step_context.get('primary_task', 'Process data')}",
            f"WORKFLOW POSITION: {step_context['workflow_position']}",
        ]

        if step_context.get("processing_focus"):
            context_parts.append(f"FOCUS ON: {step_context['processing_focus']}")

        if step_context.get("output_requirements"):
            context_parts.append(
                f"OUTPUT FORMAT: {step_context['output_requirements']}"
            )

        if step_context.get("context_awareness"):
            context_parts.append(
                f"WORKFLOW CONTEXT: {step_context['context_awareness']}"
            )

        if not step_context["is_last_step"]:
            context_parts.append(
                f"NEXT STEP: Data will be passed to {step_context.get('next_agent', 'next agent')}"
            )

        return "\n\n".join(context_parts)

    async def _process_step_data_flow(
        self,
        agent_name: str,
        step_result: Dict,
        current_data: Any,
        step_index: int,
        agent_sequence: List[str],
        step_context: Dict,
    ) -> Any:
        """Intelligently process data flow between workflow steps."""

        data_output = step_result.get("data", {})

        # Create enriched data for next step
        if current_data:
            # Merge new results with existing data
            enhanced_data = {
                **current_data,
                f"{agent_name}_results": data_output,
                "step_history": self.workflow_state.get("step_results", {}),
                "workflow_progress": {
                    "completed_steps": step_index + 1,
                    "remaining_steps": len(agent_sequence) - (step_index + 1),
                    "current_position": f"Step {step_index + 1} of {len(agent_sequence)}",
                },
            }
        else:
            # Create new data structure
            enhanced_data = {
                "content": data_output,
                "structure": "ai_processed",
                f"{agent_name}_results": data_output,
                "step_history": self.workflow_state.get("step_results", {}),
                "workflow_metadata": step_context.get("workflow_context", {}),
            }

        # Update workflow state
        self.workflow_state["current_data"] = enhanced_data

        # Log intelligent data flow
        self.workflow_state["data_flow"].append(
            {
                "from_step": agent_name,
                "to_step": (
                    agent_sequence[step_index + 1]
                    if step_index + 1 < len(agent_sequence)
                    else "final"
                ),
                "data_type": type(data_output).__name__,
                "data_size": len(str(data_output)) if data_output else 0,
                "enrichment_applied": True,
                "context_preserved": True,
                "timestamp": datetime.now().isoformat(),
            }
        )

        return enhanced_data

    async def _handle_step_failure(
        self,
        agent_name: str,
        step_result: Dict,
        step_index: int,
        agent_sequence: List[str],
        workflow_context: Dict,
    ):
        """Handle step failure with intelligent context."""

        error_msg = step_result.get("error", "Unknown error")

        self.workflow_state["errors"].append(
            {
                "step": step_index + 1,
                "agent": agent_name,
                "error": error_msg,
                "workflow_context": workflow_context.get("workflow_goal", ""),
                "recovery_attempted": False,
                "timestamp": datetime.now().isoformat(),
            }
        )

        print(f"❌ Step {step_index + 1} ({agent_name}) failed: {error_msg}")

    async def _load_agent_safely(self, agent_name: str):
        """
        FIXED: Safely load an agent from registry with proper error handling.
        """
        print(f"DEBUG: Loading agent '{agent_name}'")

        from core.registry_singleton import get_shared_registry

        registry = get_shared_registry()

        # Force reload to get latest agents
        from core.registry_singleton import force_global_reload

        force_global_reload()

        available_agents = registry.agents.get("agents", {})
        print(f"DEBUG: Available agent keys: {list(available_agents.keys())}")

        if agent_name not in available_agents:
            # Try to find the agent with a similar name
            for existing_name in available_agents.keys():
                if agent_name in existing_name or existing_name.endswith(
                    f"_{agent_name}"
                ):
                    print(
                        f"DEBUG: Found similar agent '{existing_name}' for '{agent_name}'"
                    )
                    agent_name = existing_name  # Use the existing name
                    break
            else:
                print(f"DEBUG: Agent '{agent_name}' not found in registry")
                print(f"DEBUG: Agent '{agent_name}' not found in registry")
                return None

        agent_info = available_agents[agent_name]

        # Check if agent is active
        if agent_info.get("status") != "active":
            print(f"DEBUG: Agent '{agent_name}' is not active")
            return None

        # Check built-in agents first
        if agent_name in self.agents:
            print(f"DEBUG: Using built-in agent '{agent_name}'")
            return self.agents[agent_name]

        # Check dynamic agents cache
        if agent_name in self.dynamic_agents:
            print(f"DEBUG: Using cached dynamic agent '{agent_name}'")
            return self.dynamic_agents[agent_name]

        # Try dynamic loading for generated agents
        try:
            agent_location = agent_info.get("location")
            if not agent_location or not os.path.exists(agent_location):
                print(f"DEBUG: Agent file not found: {agent_location}")
                return None

            print(f"DEBUG: Loading agent from: {agent_location}")

            # Dynamic import of the agent
            spec = importlib.util.spec_from_file_location(
                f"{agent_name}_module", agent_location
            )
            if spec is None or spec.loader is None:
                print(f"DEBUG: Could not create spec for {agent_name}")
                return None

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # FIXED: Look for the exact function name
            agent_function = None

            # Try exact agent name first
            if hasattr(module, agent_name):
                agent_function = getattr(module, agent_name)
                print(f"DEBUG: Found function with exact name: {agent_name}")
            else:
                # Try variations
                possible_names = [
                    f"{agent_name}_agent",
                    agent_name.replace("_", ""),
                    f"{agent_name}Agent",
                ]

                for name in possible_names:
                    if hasattr(module, name):
                        agent_function = getattr(module, name)
                        print(f"DEBUG: Found function with name: {name}")
                        break

            if agent_function is None:
                # List all available functions for debugging
                functions = [
                    name
                    for name in dir(module)
                    if callable(getattr(module, name)) and not name.startswith("_")
                ]
                print(f"DEBUG: Available functions in module: {functions}")
                return None

            # Create wrapper for the function
            class FunctionAgentWrapper:
                def __init__(self, func, name):
                    self.func = func
                    self.name = name

                async def execute(self, state):
                    """Execute the agent function with state"""
                    print(f"DEBUG: Executing agent function: {self.name}")
                    try:
                        result = self.func(state)
                        print(f"DEBUG: Agent execution result type: {type(result)}")

                        # Ensure result is in correct format
                        if isinstance(result, dict):
                            if "results" in result and self.name in result["results"]:
                                # Extract the actual result
                                agent_result = result["results"][self.name]
                                return agent_result
                            else:
                                # Return the full state result
                                return result
                        else:
                            return {"status": "error", "error": "Invalid result format"}

                    except Exception as e:
                        print(f"DEBUG: Agent execution failed: {str(e)}")
                        return {"status": "error", "error": str(e)}

            # Cache the wrapped agent
            wrapped_agent = FunctionAgentWrapper(agent_function, agent_name)
            self.dynamic_agents[agent_name] = wrapped_agent

            print(f"DEBUG: Successfully loaded and wrapped agent '{agent_name}'")
            return wrapped_agent

        except Exception as e:
            print(f"DEBUG: Error loading agent {agent_name}: {str(e)}")
            import traceback

            traceback.print_exc()
            return None

    async def _get_or_load_agent(self, agent_name: str):
        """Get agent from registry or load dynamically."""

        # Use the new safe loading method
        return await self._load_agent_safely(agent_name)

    def _generate_ai_workflow_summary(self, results: Dict, ai_plan: Dict) -> str:
        """Generate intelligent workflow summary based on AI plan."""

        successful_agents = []
        failed_agents = []

        for name, result in results.items():
            if isinstance(result, dict):
                if result.get("status") == "success":
                    successful_agents.append(name)
                else:
                    failed_agents.append(name)
            else:
                successful_agents.append(name)

        summary_parts = []

        # Add AI plan context
        workflow_goal = ai_plan.get("context_analysis", {}).get(
            "user_goal", "Process request"
        )
        summary_parts.append(f"🎯 Goal: {workflow_goal}")

        if successful_agents:
            summary_parts.append(f"✅ Completed: {', '.join(successful_agents)}")

            # Add AI-aware insights
            for agent_name in successful_agents:
                result = results.get(agent_name, {})
                if isinstance(result, dict) and result.get("data"):
                    data = result["data"]

                    if agent_name == "data_analyzer" and isinstance(data, dict):
                        summary_parts.append("📊 Data analysis completed with insights")
                    elif agent_name == "pdf_analyzer" and isinstance(data, dict):
                        summary_parts.append("📄 PDF analysis provided key findings")
                    elif agent_name == "chart_generator":
                        summary_parts.append("📈 Visualization generated successfully")
                    elif agent_name == "text_processor":
                        summary_parts.append(
                            "📝 Text processing completed with analysis"
                        )

        if failed_agents:
            summary_parts.append(f"❌ Issues: {', '.join(failed_agents)}")

        # Add AI confidence and complexity
        confidence = ai_plan.get("confidence", 0.8)
        complexity = ai_plan.get("complexity", "medium")
        summary_parts.append(
            f"🤖 AI Confidence: {confidence:.0%}, Complexity: {complexity}"
        )

        return " | ".join(summary_parts)

    # Keep existing methods for backward compatibility
    async def execute_workflow(
        self, workflow_plan: Dict, request: str, files: List[Dict] = None
    ) -> Dict:
        """Backward compatibility method - redirects to AI workflow execution."""
        # Convert old workflow plan to AI format
        ai_plan = {
            "agents": workflow_plan.get("agents", []),
            "execution_strategy": workflow_plan.get("execution_strategy", "sequential"),
            "rationale": workflow_plan.get("rationale", "Legacy workflow"),
            "confidence": 0.7,
            "complexity": "medium",
        }

        return await self.execute_ai_planned_workflow(ai_plan, request, files)

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

    def get_workflow_state(self) -> Dict:
        """Get current workflow state for debugging."""
        return self.workflow_state.copy()


class AIResponseSynthesizer:
    """
    AI-powered synthesizer that creates natural language responses
    from workflow results based on user intent and scenario
    """

    def __init__(self):
        self.claude = Anthropic(api_key=ANTHROPIC_API_KEY)

    async def synthesize_final_response(
        self,
        original_request: str,
        workflow_results: dict,
        scenario_key: str = None,
        execution_metadata: dict = None,
    ) -> str:
        """
        Create a natural language response based on workflow results
        """

        # Build context for AI synthesis
        synthesis_prompt = self._build_synthesis_prompt(
            original_request, workflow_results, scenario_key, execution_metadata
        )

        try:
            response = self.claude.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=1500,
                messages=[{"role": "user", "content": synthesis_prompt}],
            )

            return response.content[0].text

        except Exception as e:
            return f"Analysis completed successfully. {len(workflow_results)} agents processed your request with detailed results available."

    def _build_synthesis_prompt(
        self,
        original_request: str,
        workflow_results: dict,
        scenario_key: str = None,
        execution_metadata: dict = None,
    ) -> str:
        """Build the synthesis prompt based on scenario and results"""

        # Extract successful results
        successful_results = {}
        agent_outputs = {}

        for agent_name, result in workflow_results.items():
            if isinstance(result, dict) and result.get("status") == "success":
                successful_results[agent_name] = result
                data = result.get("data", {})
                agent_outputs[agent_name] = data

        # Build scenario-specific prompt
        if scenario_key == "sales_analysis":
            return self._build_sales_synthesis_prompt(
                original_request, agent_outputs, execution_metadata
            )
        elif scenario_key == "compliance_monitoring":
            return self._build_compliance_synthesis_prompt(
                original_request, agent_outputs, execution_metadata
            )
        else:
            return self._build_generic_synthesis_prompt(
                original_request, agent_outputs, execution_metadata
            )

    def _build_sales_synthesis_prompt(
        self, original_request: str, agent_outputs: dict, metadata: dict
    ) -> str:
        """Build synthesis prompt for sales analysis scenario"""

        return f"""
You are synthesizing results from a sales analysis workflow into a natural, executive-level response.

ORIGINAL USER REQUEST: "{original_request}"

WORKFLOW RESULTS:
{json.dumps(agent_outputs, indent=2)}

EXECUTION CONTEXT:
- Agents executed: {list(agent_outputs.keys())}
- Processing time: {metadata.get('execution_time', 'unknown')}s
- Dynamic agents created: {metadata.get('dynamic_agents_created', 0)}

SYNTHESIS INSTRUCTIONS:
1. Create a natural, conversational response that directly addresses the user's request
2. Extract key insights from the sales data analysis
3. Highlight the most important findings (revenue, trends, top performers)
4. Include actionable recommendations if available
5. Mention any reports or files generated
6. Keep the tone professional but approachable
7. Focus on business value and actionable insights

EXAMPLE STRUCTURE:
"I've completed your sales analysis and here are the key findings:

[Revenue insights and performance metrics]
[Regional/product performance highlights]  
[Key trends and patterns identified]
[Actionable recommendations]
[Any reports/files generated]

The analysis shows [overall conclusion]."

Generate a comprehensive but concise response that an executive would find valuable.
"""

    def _build_compliance_synthesis_prompt(
        self, original_request: str, agent_outputs: dict, metadata: dict
    ) -> str:
        """Build synthesis prompt for compliance monitoring scenario"""

        return f"""
You are synthesizing results from a compliance monitoring workflow into a professional audit response.

ORIGINAL USER REQUEST: "{original_request}"

WORKFLOW RESULTS:
{json.dumps(agent_outputs, indent=2)}

EXECUTION CONTEXT:
- Agents executed: {list(agent_outputs.keys())}
- Processing time: {metadata.get('execution_time', 'unknown')}s
- Compliance agents created: {metadata.get('dynamic_agents_created', 0)}

SYNTHESIS INSTRUCTIONS:
1. Create a formal, compliance-focused response
2. Summarize any violations or compliance issues identified
3. Highlight risk levels and severity
4. Include transaction monitoring results
5. Mention audit trail and documentation generated
6. Use appropriate compliance terminology
7. Ensure tone is professional and regulatory-appropriate

EXAMPLE STRUCTURE:
"Compliance monitoring analysis completed for [X] transactions:

[Violation summary and counts]
[Risk assessment results]
[Key compliance findings]
[Audit recommendations]
[Documentation and reports generated]

Overall compliance status: [assessment]"

Generate a professional compliance report summary.
"""

    def _build_generic_synthesis_prompt(
        self, original_request: str, agent_outputs: dict, metadata: dict
    ) -> str:
        """Build synthesis prompt for generic workflows"""

        return f"""
You are synthesizing results from an AI workflow into a helpful user response.

ORIGINAL USER REQUEST: "{original_request}"

WORKFLOW RESULTS:
{json.dumps(agent_outputs, indent=2)}

EXECUTION CONTEXT:
- Agents executed: {list(agent_outputs.keys())}
- Processing time: {metadata.get('execution_time', 'unknown')}s

SYNTHESIS INSTRUCTIONS:
1. Create a natural response that directly addresses what the user asked for
2. Extract the most relevant information from the agent outputs
3. Present findings in a logical, easy-to-understand way
4. Include any files, reports, or outputs generated
5. Maintain a helpful, professional tone
6. Focus on delivering value to the user

Generate a clear, helpful response based on the workflow results.
"""


# Alias for backward compatibility
MultiAgentWorkflowEngine = EnhancedMultiAgentWorkflowEngine
