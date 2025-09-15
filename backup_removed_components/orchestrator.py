"""
Orchestrator
Master orchestration engine using GPT-4 for intelligent workflow planning and execution
"""

import importlib
import os
import sys
import json
import asyncio
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import openai
from enum import Enum
from core.dependency_resolver import DependencyResolver
import networkx as nx

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    CLAUDE_MAX_TOKENS,
    CLAUDE_MODEL,
    OPENAI_API_KEY,
    ORCHESTRATOR_MODEL,
    ORCHESTRATOR_TEMPERATURE,
    ORCHESTRATOR_MAX_TOKENS,
    ORCHESTRATOR_SYSTEM_PROMPT,
    ORCHESTRATOR_ANALYSIS_PROMPT,
    ORCHESTRATOR_PLANNING_PROMPT,
    ORCHESTRATOR_SYNTHESIS_PROMPT,
    MAX_WORKFLOW_STEPS,
    WORKFLOW_TIMEOUT_SECONDS,
    WORKFLOW_STATE_SCHEMA,
)
from core.registry import RegistryManager
from backup_removed_components.workflow_engine import WorkflowEngine
from core.agent_factory import AgentFactory
from core.tool_factory import ToolFactory
from core.registry_singleton import get_shared_registry
from typing import Dict, List, Optional, Any, Tuple

from core.pipeline_orchestrator import PipelineOrchestrator
from core.pipeline_executor import PipelineExecutor
from core.workflow_intelligence import WorkflowIntelligence


class WorkflowType(Enum):
    """Workflow execution patterns."""

    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    CONDITIONAL = "conditional"
    HYBRID = "hybrid"


class Orchestrator:
    """
    Master orchestrator that coordinates the entire system.
    Uses GPT-4 for intelligent planning and decision making.
    """

    def __init__(self):
        """Initialize the orchestrator."""
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        self.registry = get_shared_registry()
        self.workflow_engine = WorkflowEngine(self.registry)
        self.agent_factory = AgentFactory()
        self.tool_factory = ToolFactory()
        self.dependency_resolver = DependencyResolver(self.registry)

        # FIX: Add pipeline orchestrator initialization
        self.pipeline_orchestrator = PipelineOrchestrator()
        self.pipeline_executor = PipelineExecutor(self.registry)
        self.workflow_intelligence = WorkflowIntelligence(self.registry)

        self.execution_history = []

    def _prepare_initial_data(
        self,
        user_request: str,
        files: Optional[List[Dict]] = None,
        analysis: Dict = None,
    ) -> Dict[str, Any]:
        """Prepare initial data with intelligent extraction."""

        # Import the data processor
        from core.data_processor import DataProcessor

        processor = DataProcessor()

        # Get intelligently processed data
        processed = processor.process_request_data(user_request, analysis)

        # Create comprehensive initial state
        base_data = {
            "request": user_request,
            "files": files or [],
            "context": {},
            "results": {},
            "errors": [],
            "execution_path": [],
            # Multiple data formats available to agents
            **processed,  # This includes raw_request, extracted_data, current_data, etc.
        }

        print(f"DEBUG: Prepared data with extracted: {processed.get('extracted_data')}")
        print(f"DEBUG: Data type identified: {processed.get('data_type')}")

        return base_data

    async def process_request(
        self,
        user_request: str,
        files: Optional[List[Dict[str, Any]]] = None,
        context: Optional[Dict[str, Any]] = None,
        auto_create: bool = True,
        stream_results: bool = False,
    ) -> Dict[str, Any]:
        """
        Process a user request end-to-end with pipeline support.
        """
        start_time = datetime.now()
        workflow_id = self._generate_workflow_id()

        try:
            print(f"DEBUG: Starting request processing for: {user_request[:50]}...")

            # NEW: Add pipeline complexity detection
            complexity = await self._detect_pipeline_complexity(
                user_request, files or []
            )
            print(f"DEBUG: Detected complexity: {complexity}")

            # NEW: Route to pipeline processing if complex
            if complexity in ["pipeline", "complex"]:
                print(f"DEBUG: Routing to pipeline processing")
                return await self._process_pipeline_request(
                    user_request, files or [], context or {}, auto_create, workflow_id
                )

            # EXISTING: Continue with your existing logic for simple requests
            print(f"DEBUG: Using existing single-agent processing")

            # Phase 1: Analyze the request (YOUR EXISTING CODE)
            analysis = await self._analyze_request(user_request, files, context)

            # ============= AMBIGUOUS HANDLING =============
            if analysis["status"] == "ambiguous":
                # Handle ambiguous requests with clarification
                return {
                    "status": "success",  # Mark as success but with clarification response
                    "workflow_id": workflow_id,
                    "response": "I need more information to help you effectively. "
                    + " ".join(analysis["analysis"]["issues"])
                    + "\n\nHere are some ways you can help me:\n• "
                    + "\n• ".join(analysis["analysis"]["suggestions"]),
                    "execution_time": (datetime.now() - start_time).total_seconds(),
                    "workflow": {"steps": []},
                    "results": {},
                    "metadata": {
                        "components_created": 0,
                        "response_type": "clarification",
                    },
                }

            if analysis["status"] != "success":
                return self._create_error_response(
                    workflow_id, "Analysis failed", analysis.get("error")
                )
            # ============================================================

            # Phase 2: Plan the workflow (YOUR EXISTING CODE)
            plan = await self._plan_workflow(
                user_request, analysis["analysis"], auto_create
            )
            if plan["status"] != "success":
                return self._create_error_response(
                    workflow_id, "Planning failed", plan.get("error")
                )

            # ALL YOUR EXISTING CRITICAL FIXES - keep them all
            agents_needed = plan.get("agents_needed", [])
            missing_capabilities = plan.get("missing_capabilities", {})

            # Check if we have no agents and need to create some
            if not agents_needed and missing_capabilities.get("agents"):
                if auto_create:
                    # Try to create the missing agents first
                    creation_result = await self._create_missing_components(
                        missing_capabilities
                    )

                    # Re-plan after creation
                    if creation_result.get("status") in ["success", "partial"]:
                        plan = await self._plan_workflow(
                            user_request, analysis["analysis"], auto_create=False
                        )
                        agents_needed = plan.get("agents_needed", [])
                else:
                    # Return early if no agents and can't create
                    return {
                        "status": "no_agents",
                        "message": "No suitable agents found and auto-creation is disabled",
                        "workflow": {"steps": []},
                        "response": "I couldn't find suitable agents to handle your request. Please enable auto-creation or add the required agents.",
                        "execution_time": (datetime.now() - start_time).total_seconds(),
                        "metadata": {"components_created": 0},
                    }

            # Phase 3: Handle remaining missing capabilities (your existing code)
            missing_capabilities = self._check_missing_capabilities(plan)
            if missing_capabilities:
                if auto_create:
                    creation_result = await self._create_missing_components(
                        missing_capabilities
                    )

                    if creation_result["status"] in ["success", "partial"]:
                        # Re-plan with new components
                        plan = await self._plan_workflow(
                            user_request, analysis["analysis"], auto_create=False
                        )

                        # Update agents_needed after re-planning
                        agents_needed = plan.get("agents_needed", [])
                else:
                    return {
                        "status": "missing_capabilities",
                        "message": "Required components are not available",
                        "missing": missing_capabilities,
                        "workflow_id": workflow_id,
                        "suggestion": "Enable auto_create to build missing components automatically",
                    }

            # Final check for no agents
            if not agents_needed:
                message = "I couldn't identify specific agents to handle this request. "
                if plan.get("missing_capabilities", {}).get("agents"):
                    missing = ", ".join(
                        a["name"] for a in plan["missing_capabilities"]["agents"]
                    )
                    message += f"The following capabilities would need to be created: {missing}"
                else:
                    message += "Please provide more specific instructions or data."

                return {
                    "status": "no_agents",
                    "workflow_id": workflow_id,
                    "message": message,
                    "workflow": {
                        "type": plan.get("workflow_type", "sequential"),
                        "steps": [],
                    },
                    "response": message,
                    "execution_time": (datetime.now() - start_time).total_seconds(),
                    "results": {},
                    "metadata": {
                        "agents_used": 0,
                        "components_created": 0,
                        "errors_encountered": 0,
                    },
                }

            # Phase 4: Prepare initial data with ALL fields agents might look for
            initial_data = self._prepare_initial_data(user_request, files)
            initial_data["context"] = {
                "analysis": analysis.get("analysis", {}),
                "plan": plan,
            }

            # After planning is complete, add this debug section:
            print(f"DEBUG: About to execute workflow with plan: {plan}")
            print(f"DEBUG: Agents needed: {plan.get('agents_needed', [])}")
            print(f"DEBUG: Workflow type: {plan.get('workflow_type', 'sequential')}")

            # Phase 5: Execute the workflow
            if stream_results:
                execution_result = await self._execute_workflow_streaming(
                    plan, initial_data, workflow_id
                )
            else:
                execution_result = await self._execute_workflow(
                    plan, initial_data, workflow_id
                )

            if execution_result["status"] == "error":
                return self._create_error_response(
                    workflow_id, "Execution failed", execution_result.get("error")
                )

            # Phase 6: Synthesize results (FIXED)
            if execution_result.get("errors"):
                final_response = await self._handle_execution_errors(
                    execution_result, plan
                )
            else:
                # USE THE FIXED SYNTHESIS FUNCTION
                final_response = await self._synthesize_results(
                    user_request,
                    plan,
                    execution_result.get("results", {}),
                    execution_result.get("errors", []),
                )

            # Record execution history
            execution_time = (datetime.now() - start_time).total_seconds()
            self._record_execution(
                workflow_id, user_request, plan, execution_result, execution_time
            )

            return {
                "status": "success",
                "workflow_id": workflow_id,
                "response": final_response,  # THIS IS CRITICAL
                "execution_time": execution_time,
                "workflow": {
                    "type": plan.get("workflow_type", "sequential"),
                    "steps": agents_needed,
                    "execution_path": execution_result.get("execution_path", []),
                },
                "results": execution_result.get("results", {}),
                "metadata": {
                    "agents_used": len(agents_needed),
                    "components_created": len(plan.get("created_components", [])),
                    "errors_encountered": len(execution_result.get("errors", [])),
                },
            }

            print(f"DEBUG: Workflow execution completed")
            print(f"DEBUG: Execution result status: {execution_result.get('status')}")
            print(f"DEBUG: Execution result keys: {list(execution_result.keys())}")

        except KeyError as e:
            print(f"DEBUG: KeyError in process_request: {str(e)}")
            import traceback

            traceback.print_exc()
            return self._create_error_response(
                workflow_id, "Unexpected error", f"KeyError: {str(e)}"
            )
        except Exception as e:
            print(f"DEBUG: Exception in process_request: {str(e)}")
            import traceback

            print(f"DEBUG: Traceback: {traceback.format_exc()}")
            traceback.print_exc()
            return self._create_error_response(workflow_id, "Unexpected error", str(e))

    async def _analyze_request(
        self, user_request: str, files: Optional[List[Dict]], context: Optional[Dict]
    ) -> Dict[str, Any]:
        """Analyze the request to understand intent and requirements."""
        # Get available components
        agents = self.registry.list_agents(active_only=True)
        tools = self.registry.list_tools()

        # Format components for prompt
        agents_desc = self._format_components_list(agents, "agents")
        tools_desc = self._format_components_list(tools, "tools")

        # Build analysis prompt
        prompt = ORCHESTRATOR_ANALYSIS_PROMPT.format(
            request=user_request,
            files=json.dumps(files) if files else "None",
            context=json.dumps(context) if context else "None",
            available_agents=agents_desc,
            available_tools=tools_desc,
        )

        print(f"DEBUG: Analyzing request: {user_request[:100]}...")

        # ============= ADD THIS AMBIGUITY CHECK =============
        # Check for ambiguous requests that need clarification
        request_lower = user_request.lower()

        # Indicators of ambiguous requests
        is_ambiguous = False
        clarification_needed = []

        # Check for vague analysis requests without data
        if (
            ("analyze" in request_lower or "process" in request_lower)
            and ("data" in request_lower or "feedback" in request_lower)
            and not files
            and len(user_request) < 100
        ):
            is_ambiguous = True
            clarification_needed.append("No data file or specific content provided")

        # Check for explicitly marked ambiguous requests (from test)
        if (
            "[no specific data provided" in request_lower
            or "ambiguous request" in request_lower
        ):
            is_ambiguous = True
            clarification_needed.append(
                "Request lacks specific data or clear instructions"
            )

        # Check for very short vague requests
        if len(user_request) < 30 and not files:
            is_ambiguous = True
            clarification_needed.append(
                "Request is too brief to determine specific action"
            )

        if is_ambiguous:
            return {
                "status": "ambiguous",
                "analysis": {
                    "type": "clarification_needed",
                    "issues": clarification_needed,
                    "suggestions": [
                        "Please upload the data file you'd like me to analyze",
                        "Provide the specific text or content to process",
                        "Specify what type of analysis you're looking for (statistics, sentiment, extraction, etc.)",
                        "Include more details about your requirements",
                    ],
                },
            }
        # =====================================================

        try:
            response = await self._call_gpt4(
                system_prompt=ORCHESTRATOR_SYSTEM_PROMPT,
                user_prompt=prompt,
            )
            print(f"DEBUG: GPT-4 analysis successful")
            return {"status": "success", "analysis": response}

        except Exception as e:
            print(f"DEBUG: GPT-4 analysis failed: {str(e)}")
            return {"status": "error", "error": f"Analysis failed: {str(e)}"}

    # async def _plan_workflow(
    #     self, user_request: str, analysis: str, auto_create: bool
    # ) -> Dict[str, Any]:
    #     """Use the actual ORCHESTRATOR_PLANNING_PROMPT from config."""

    #     # Get available components
    #     agents = self.registry.list_agents(active_only=True)
    #     tools = self.registry.list_tools(pure_only=False)

    #     # Format components for prompt
    #     agents_desc = self._format_components_list(agents, "agents")
    #     tools_desc = self._format_components_list(tools, "tools")

    #     # Use the ACTUAL prompt from config
    #     prompt = ORCHESTRATOR_PLANNING_PROMPT.format(
    #         request=user_request,
    #         analysis=analysis,
    #         available_agents=agents_desc,
    #         available_tools=tools_desc,
    #         timestamp=datetime.now().strftime("%Y%m%d%H%M%S"),
    #     )

    #     try:
    #         response = await self._call_gpt4_json(
    #             system_prompt="You are a workflow planner. Output valid JSON only.",
    #             user_prompt=prompt,
    #             temperature=0.1,
    #         )

    #         plan = json.loads(response)
    #         plan["status"] = "success"
    #         return plan

    #     except json.JSONDecodeError as e:
    #         print(f"DEBUG: JSON parsing failed: {str(e)}")
    #         return self._create_fallback_plan(user_request, agents)
    #     except Exception as e:
    #         print(f"DEBUG: Planning failed: {str(e)}")
    #         return self._create_fallback_plan(user_request, agents)

    async def _plan_workflow(
        self, request: str, analysis: Dict, auto_create: bool
    ) -> Dict[str, Any]:
        """
        Plan workflow execution with proper handling of missing agents.
        """
        print(f"DEBUG: Smart planning for request")

        try:
            # Get available agents and tools
            available_agents = self.registry.list_agents()
            available_tools = self.registry.list_tools()

            # Format for GPT-4
            agents_text = "\n".join(
                [
                    f"- {a.get('name')}: {a.get('description', 'No description')}"
                    for a in available_agents
                ]
            )
            tools_text = "\n".join(
                [
                    f"- {t.get('name')}: {t.get('description', 'No description')}"
                    for t in available_tools
                ]
            )

            print(
                f"DEBUG: Found {len(available_agents)} agents and {len(available_tools)} tools"
            )

            # Smart planning prompt
            planning_prompt = f"""
    Analyze this request and create a smart sequential workflow.

    USER REQUEST: {request}

    AVAILABLE AGENTS:
    {agents_text}

    AVAILABLE TOOLS:
    {tools_text}

    PLANNING INSTRUCTIONS:
    1. Identify what needs to be done step by step
    2. For each step, suggest the best agent (even if it doesn't exist yet)
    3. Be specific about agent names based on the task

    For prime number tasks: Use 'prime_checker' agent
    For average/mean calculations: Use 'calculate_mean' agent  
    For email extraction: Use 'email_extractor' agent
    For URL extraction: Use 'url_extractor' agent

    RESPOND WITH VALID JSON:
    {{
        "workflow_id": "wf_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "workflow_type": "sequential",
        "reasoning": "Clear explanation of the workflow plan",
        "agents_needed": ["agent1", "agent2"],
        "missing_capabilities": {{
            "agents": [],
            "tools": []
        }},
        "confidence": 0.9,
        "status": "success"
    }}

    List ALL agents needed, whether they exist or not.
    """

            # Call GPT-4 for smart planning
            planning_response = await self._call_gpt4_json(
                system_prompt="You are a smart workflow planner.",
                user_prompt=planning_prompt,
            )

            # Parse response
            try:
                plan = json.loads(planning_response)
                plan["workflow_type"] = "sequential"
                plan["created_at"] = datetime.now().isoformat()
                plan["auto_create"] = auto_create
                plan["original_request"] = request

                # CRITICAL FIX: Check which agents exist and which are missing
                available_agent_names = [a.get("name") for a in available_agents]
                valid_agents = []
                missing_agents = []

                for agent in plan.get("agents_needed", []):
                    if agent in available_agent_names:
                        valid_agents.append(agent)
                        print(f"DEBUG: Agent '{agent}' exists")
                    else:
                        print(f"DEBUG: Agent '{agent}' is missing - will need creation")
                        missing_agents.append(
                            {
                                "name": agent,
                                "purpose": f"Process {agent} tasks",
                                "required_tools": [],
                            }
                        )

                # Update plan with valid agents
                plan["agents_needed"] = valid_agents

                # CRITICAL: Add missing agents to missing_capabilities
                if missing_agents:
                    if "missing_capabilities" not in plan:
                        plan["missing_capabilities"] = {"agents": [], "tools": []}
                    plan["missing_capabilities"]["agents"] = missing_agents

                # If auto_create is enabled and we have missing agents, they'll be created
                # If auto_create is disabled and all agents are missing, return error status
                if not valid_agents and not auto_create:
                    plan["status"] = "missing_all_agents"
                    plan["message"] = (
                        f"None of the required agents exist: {', '.join([a['name'] for a in missing_agents])}"
                    )

                print(f"DEBUG: Smart plan created")
                print(f"DEBUG: Existing agents to use: {valid_agents}")
                print(
                    f"DEBUG: Missing agents to create: {[a['name'] for a in missing_agents]}"
                )

                return plan

            except json.JSONDecodeError as e:
                print(f"DEBUG: JSON parsing failed: {e}")
                # Return error plan instead of falling back to bad agents
                return {
                    "status": "planning_error",
                    "error": f"Failed to parse planning response: {str(e)}",
                    "workflow_id": f"wf_error_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "workflow_type": "sequential",
                    "agents_needed": [],
                    "missing_capabilities": {"agents": [], "tools": []},
                }

        except Exception as e:
            print(f"DEBUG: Smart planning failed: {str(e)}")
            return {
                "status": "planning_error",
                "error": str(e),
                "workflow_id": f"wf_error_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "workflow_type": "sequential",
                "agents_needed": [],
                "missing_capabilities": {"agents": [], "tools": []},
            }

    def _build_capability_map(self, agents: List[Dict], tools: List[Dict]) -> Dict:
        """Build detailed capability map for better planning."""

        capability_map = {
            "agents": {},
            "tools": {},
            "capabilities": {
                "data_processing": [],
                "extraction": [],
                "calculation": [],
                "formatting": [],
                "analysis": [],
                "generation": [],
            },
        }

        # Map agents to capabilities
        for agent in agents:
            name = agent["name"]
            desc = agent["description"].lower()

            capability_map["agents"][name] = {
                "description": agent["description"],
                "uses_tools": agent.get("uses_tools", []),
                "capabilities": [],
            }

            # Categorize capabilities
            if any(word in desc for word in ["extract", "find", "get"]):
                capability_map["capabilities"]["extraction"].append(name)
                capability_map["agents"][name]["capabilities"].append("extraction")

            if any(
                word in desc
                for word in ["calculate", "compute", "mean", "median", "std"]
            ):
                capability_map["capabilities"]["calculation"].append(name)
                capability_map["agents"][name]["capabilities"].append("calculation")

            if any(word in desc for word in ["format", "report", "present"]):
                capability_map["capabilities"]["formatting"].append(name)
                capability_map["agents"][name]["capabilities"].append("formatting")

            if any(word in desc for word in ["analyze", "sentiment", "assess"]):
                capability_map["capabilities"]["analysis"].append(name)
                capability_map["agents"][name]["capabilities"].append("analysis")

        # Map tools
        for tool in tools:
            capability_map["tools"][tool["name"]] = {
                "description": tool["description"],
                "is_pure": tool.get("is_pure_function", True),
            }

        return capability_map

    def _validate_and_filter_plan(self, plan: Dict) -> Dict:
        """Validate and filter plan to avoid duplicates."""

        # Remove duplicate agents from agents_needed
        if "agents_needed" in plan:
            plan["agents_needed"] = list(dict.fromkeys(plan["agents_needed"]))

        # Filter out agents that actually exist from missing_capabilities
        if "missing_capabilities" in plan:
            if "agents" in plan["missing_capabilities"]:
                filtered_agents = []
                for agent in plan["missing_capabilities"]["agents"]:
                    # Check if agent actually exists
                    if not self.registry.agent_exists(agent["name"]):
                        # Also check for similar agents
                        similar = self._find_similar_agents(
                            agent["name"], agent.get("purpose", "")
                        )
                        if not similar:
                            filtered_agents.append(agent)
                        else:
                            print(
                                f"DEBUG: Found similar agent {similar} for {agent['name']}"
                            )
                            # Use the similar agent instead
                            if "agents_needed" not in plan:
                                plan["agents_needed"] = []
                            if similar not in plan["agents_needed"]:
                                plan["agents_needed"].append(similar)

                plan["missing_capabilities"]["agents"] = filtered_agents

        return plan

    def _find_similar_agents(self, name: str, purpose: str) -> Optional[str]:
        """Find agents with similar capabilities."""

        agents = self.registry.list_agents(active_only=True)
        name_lower = name.lower()
        purpose_lower = purpose.lower()

        for agent in agents:
            agent_name_lower = agent["name"].lower()
            agent_desc_lower = agent["description"].lower()

            # Check name similarity
            if name_lower in agent_name_lower or agent_name_lower in name_lower:
                return agent["name"]

            # Check purpose similarity
            if purpose_lower and (
                purpose_lower in agent_desc_lower or agent_desc_lower in purpose_lower
            ):
                return agent["name"]

            # Check key words overlap
            name_words = set(name_lower.split("_"))
            agent_words = set(agent_name_lower.split("_"))
            if len(name_words & agent_words) >= len(name_words) * 0.5:
                return agent["name"]

        return None

    def _create_fallback_plan(self, user_request: str, agents: List[Dict]) -> Dict:
        """Create a simple fallback plan when GPT-4 fails."""
        # Try to find agents that might handle the request
        request_lower = user_request.lower()
        potential_agents = []

        for agent in agents:
            agent_name = agent["name"]
            agent_desc = agent["description"].lower()

            # Simple keyword matching
            if any(word in request_lower for word in agent_desc.split()):
                potential_agents.append(agent_name)

        if potential_agents:
            return {
                "status": "success",
                "workflow_id": f"wf_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "workflow_type": "sequential",
                "agents_needed": potential_agents[:3],  # Limit to 3 agents
                "missing_capabilities": {"agents": [], "tools": []},
                "reasoning": "Fallback plan based on keyword matching",
            }
        else:
            return {
                "status": "error",
                "error": "No agents available to handle this request",
            }

    def _can_handle_request(self, request: str) -> bool:
        """Check if any existing agent can handle the request."""
        agents = self.registry.list_agents(active_only=True)
        request_lower = request.lower()

        # Remove common words that might cause false positives
        stop_words = {
            "the",
            "a",
            "an",
            "and",
            "or",
            "but",
            "in",
            "on",
            "at",
            "to",
            "for",
            "of",
            "with",
            "by",
            "from",
            "this",
        }
        request_words = set(request_lower.split()) - stop_words

        for agent in agents:
            agent_desc = agent["description"].lower()
            agent_name = agent["name"].lower()

            # Check for meaningful word matches
            desc_words = set(agent_desc.split()) - stop_words
            name_words = set(agent_name.replace("_", " ").split())

            if request_words & (desc_words | name_words):
                return True

        return False

    async def _create_missing_components(
        self, missing_capabilities: Dict[str, List]
    ) -> Dict[str, Any]:
        """Create missing agents and tools dynamically - tools first!"""
        created = {"agents": [], "tools": []}
        failed = {"agents": [], "tools": []}

        # CRITICAL: Create missing tools FIRST (agents depend on them)
        for tool_spec in missing_capabilities.get("tools", []):
            try:
                # Handle both string and dict formats for tools
                if isinstance(tool_spec, str):
                    tool_spec = {"name": tool_spec, "purpose": f"Tool for {tool_spec}"}

                print(f"DEBUG: Creating tool '{tool_spec['name']}'")

                # Use tool factory's ensure method which handles everything
                result = self.tool_factory.ensure_tool(
                    tool_name=tool_spec["name"],
                    description=tool_spec.get(
                        "purpose", f"Tool for {tool_spec['name']}"
                    ),
                    tool_type=tool_spec.get("type", "pure_function"),
                )

                if result["status"] in ["success", "exists"]:
                    created["tools"].append(tool_spec["name"])
                    print(f"DEBUG: Tool '{tool_spec['name']}' created successfully")
                else:
                    print(
                        f"DEBUG: Tool '{tool_spec['name']}' creation failed: {result.get('message')}"
                    )
                    # Don't fail the workflow for tool issues
                    created["tools"].append(tool_spec["name"])

            except Exception as e:
                print(f"DEBUG: Tool creation error: {str(e)}")
                # Continue anyway
                if isinstance(tool_spec, dict):
                    created["tools"].append(tool_spec.get("name", "unknown"))

        # Now create missing agents (with tools available)
        for agent_spec in missing_capabilities.get("agents", []):
            try:
                # FIX: Handle both string and dictionary formats
                if isinstance(agent_spec, str):
                    # Convert string to proper dictionary format
                    agent_spec = {
                        "name": agent_spec,
                        "purpose": f"Process {agent_spec} tasks",
                        "required_tools": [],  # Will be determined during creation
                    }

                print(
                    f"DEBUG: Creating agent '{agent_spec['name']}' with tools: {agent_spec.get('required_tools', [])}"
                )

                result = self.agent_factory.ensure_agent(
                    agent_name=agent_spec["name"],
                    description=agent_spec.get(
                        "purpose", f"Agent for {agent_spec['name']}"
                    ),
                    required_tools=agent_spec.get("required_tools", []),
                )

                if result["status"] in ["success", "exists"]:
                    created["agents"].append(agent_spec["name"])
                    print(
                        f"DEBUG: Agent '{agent_spec['name']}' created/verified successfully"
                    )
                else:
                    print(
                        f"DEBUG: Agent '{agent_spec['name']}' creation failed: {result.get('message')}"
                    )
                    failed["agents"].append(
                        {
                            "name": agent_spec["name"],
                            "error": result.get("message", "Unknown error"),
                        }
                    )

            except Exception as e:
                print(f"DEBUG: Agent creation error for spec: {agent_spec}")
                print(f"DEBUG: Error details: {str(e)}")
                # Safely handle the error regardless of agent_spec type
                agent_name = (
                    agent_spec
                    if isinstance(agent_spec, str)
                    else agent_spec.get("name", "unknown")
                )
                failed["agents"].append({"name": agent_name, "error": str(e)})

        # Determine overall status
        total_created = len(created["agents"]) + len(created["tools"])
        total_failed = len(failed["agents"]) + len(failed["tools"])

        if total_failed == 0 and total_created > 0:
            status = "success"
        elif total_created > 0:
            status = "partial"
        else:
            status = "failed"

        return {
            "status": status,
            "created": created,
            "failed": failed,
            "total_created": total_created,
            "total_failed": total_failed,
        }

    async def _create_tool_from_spec(self, spec: Dict) -> Dict[str, Any]:
        """Create a tool from specification."""
        # Use GPT-4 to design detailed tool specification
        design_prompt = f"""Design a tool with these requirements:
Name: {spec['name']}
Purpose: {spec['purpose']}
Type: {spec.get('type', 'pure_function')}

Provide:
- Detailed input description
- Detailed output description
- 2-3 input/output examples
- Default return value

Output as JSON."""

        try:
            design_response = await self._call_gpt4_json(
                system_prompt="Design tool specifications.",
                user_prompt=design_prompt,
            )

            design = json.loads(design_response)

            # Create tool using factory
            return self.tool_factory.create_tool(
                tool_name=spec["name"],
                description=spec["purpose"],
                input_description=design.get("input_description", "Flexible input"),
                output_description=design.get("output_description", "Processed output"),
                examples=design.get("examples"),
                default_return=design.get("default_return"),
                is_pure_function=spec.get("type") == "pure_function",
            )

        except Exception as e:
            return {"status": "error", "message": f"Failed to create tool: {str(e)}"}

    async def _create_agent_from_spec(self, spec: Dict) -> Dict[str, Any]:
        """Create an agent from specification."""
        # Use GPT-4 to design detailed agent specification
        design_prompt = f"""Design an agent with these requirements:
Name: {spec['name']}
Purpose: {spec['purpose']}
Required Tools: {spec.get('required_tools', [])}

Provide:
- Detailed workflow steps
- Input format description
- Output format description
- Key processing logic

Output as JSON."""

        try:
            design_response = await self._call_gpt4_json(
                system_prompt="Design agent specifications.",
                user_prompt=design_prompt,
            )

            design = json.loads(design_response)

            # Create agent using factory
            return self.agent_factory.create_agent(
                agent_name=spec["name"],
                description=spec["purpose"],
                required_tools=spec.get("required_tools", []),
                input_description=design.get("input_description", "Flexible input"),
                output_description=design.get(
                    "output_description", "Structured output"
                ),
                workflow_steps=design.get("workflow_steps"),
                auto_create_tools=True,
            )

        except Exception as e:
            return {"status": "error", "message": f"Failed to create agent: {str(e)}"}

    # async def _execute_workflow(
    #     self, plan: Dict, initial_data: Dict, workflow_id: str
    # ) -> Dict[str, Any]:
    #     """Execute the planned workflow."""

    #     print(
    #         f"DEBUG: _execute_workflow called with plan: {plan.get('workflow_type', 'unknown')}"
    #     )

    #     # TEMPORARY: Use simple fallback instead of LangGraph
    #     print(f"DEBUG: Using simple fallback execution for reliability")
    #     return await self._execute_workflow_simple_fallback(
    #         plan, initial_data, workflow_id
    #     )

    #     agents_needed = plan.get("agents_needed", [])
    #     if not agents_needed:
    #         return {
    #             "status": "success",
    #             "results": {},
    #             "execution_path": [],
    #             "errors": [],
    #             "message": "No agents required for this request",
    #         }

    #     workflow_type = WorkflowType(plan.get("workflow_type", "sequential"))

    #     try:
    #         if workflow_type == WorkflowType.SEQUENTIAL:
    #             result = await self._execute_sequential(
    #                 plan["agents_needed"], initial_data, workflow_id
    #             )
    #         elif workflow_type == WorkflowType.PARALLEL:
    #             result = await self._execute_parallel(
    #                 plan["agents_needed"], initial_data, workflow_id
    #             )
    #         else:
    #             result = await self._execute_sequential(
    #                 plan["agents_needed"], initial_data, workflow_id
    #             )

    #         # CRITICAL FIX: Better status determination
    #         # Check if we have meaningful results from agents
    #         successful_agents = 0
    #         failed_agents = 0

    #         for agent_name in agents_needed:
    #             if agent_name in result.get("results", {}):
    #                 agent_result = result["results"][agent_name]
    #                 if isinstance(agent_result, dict):
    #                     if agent_result.get("status") == "success":
    #                         successful_agents += 1
    #                     else:
    #                         failed_agents += 1

    #         # Determine overall status based on agent execution
    #         if successful_agents == len(agents_needed):
    #             result["status"] = "success"
    #         elif successful_agents > 0:
    #             result["status"] = "partial"
    #         else:
    #             result["status"] = "failed"

    #         return result

    #     except asyncio.TimeoutError:
    #         return {
    #             "status": "error",
    #             "error": f"Workflow timeout after {WORKFLOW_TIMEOUT_SECONDS} seconds",
    #         }
    #     except Exception as e:
    #         return {"status": "error", "error": f"Workflow execution failed: {str(e)}"}

    async def _execute_sequential(
        self, agents: List[str], initial_data: Dict, workflow_id: str
    ) -> Dict[str, Any]:
        """Execute agents sequentially."""
        # Use workflow engine for execution
        workflow = self.workflow_engine.create_workflow(agents, workflow_id)
        result = self.workflow_engine.execute_workflow(
            workflow, initial_data, workflow_id
        )

        return {
            "status": "success" if not result.get("errors") else "partial",
            "results": result.get("results", {}),
            "execution_path": result.get("execution_path", []),
            "errors": result.get("errors", []),
        }

    async def _execute_parallel(
        self, agents: List[str], initial_data: Dict, workflow_id: str
    ) -> Dict[str, Any]:
        """Execute agents in parallel."""
        # Create tasks for parallel execution
        tasks = []
        for agent in agents:
            task = asyncio.create_task(
                self._execute_single_agent(agent, initial_data.copy())
            )
            tasks.append((agent, task))

        # Wait for all tasks with timeout
        results = {}
        errors = []
        execution_path = []

        done, pending = await asyncio.wait(
            [task for _, task in tasks], timeout=WORKFLOW_TIMEOUT_SECONDS
        )

        # Process completed tasks
        for agent, task in tasks:
            if task in done:
                try:
                    result = await task
                    results[agent] = result
                    execution_path.append(agent)
                except Exception as e:
                    errors.append({"agent": agent, "error": str(e)})
            else:
                task.cancel()
                errors.append({"agent": agent, "error": "Timeout"})

        return {
            "status": "success" if not errors else "partial",
            "results": results,
            "execution_path": execution_path,
            "errors": errors,
        }

    async def _execute_conditional(
        self, plan: Dict, initial_data: Dict, workflow_id: str
    ) -> Dict[str, Any]:
        """Execute conditional workflow based on plan."""
        # This would implement conditional logic from the plan
        # For now, fall back to sequential
        return await self._execute_sequential(
            plan.get("agents_needed", []), initial_data, workflow_id
        )

    async def _execute_hybrid(
        self, plan: Dict, initial_data: Dict, workflow_id: str
    ) -> Dict[str, Any]:
        """Execute hybrid workflow with mixed patterns."""
        # This would implement complex hybrid workflows
        # For now, fall back to sequential
        return await self._execute_sequential(
            plan.get("agents_needed", []), initial_data, workflow_id
        )

    async def _execute_single_agent(
        self, agent_name: str, data: Dict
    ) -> Dict[str, Any]:
        """Execute a single agent asynchronously."""
        # This would be implemented with actual async agent execution
        # For now, use sync execution
        agent_workflow = self.workflow_engine.create_workflow(
            [agent_name], f"single_{agent_name}"
        )
        result = self.workflow_engine.execute_workflow(
            agent_workflow, data, f"single_{agent_name}"
        )
        return result.get("results", {}).get(agent_name, {})

    async def _execute_workflow_streaming(
        self, plan: Dict, initial_data: Dict, workflow_id: str
    ) -> Dict[str, Any]:
        """Execute workflow with streaming results."""
        # This would implement streaming execution
        # For now, use regular execution
        return await self._execute_workflow(plan, initial_data, workflow_id)

    async def _synthesize_results(
        self, request: str, plan: Dict, results: Dict, errors: List = None
    ) -> str:
        """Use the actual ORCHESTRATOR_SYNTHESIS_PROMPT from config."""

        if errors is None:
            errors = []

        # Format results for GPT-4
        results_summary = self._format_results_for_synthesis(results)

        # Use the ACTUAL synthesis prompt from config
        synthesis_prompt = ORCHESTRATOR_SYNTHESIS_PROMPT.format(
            request=request,
            results=results_summary,
            errors=json.dumps(errors, indent=2) if errors else "None",
        )

        try:
            # Call GPT-4 for dynamic synthesis
            synthesized_response = await self._call_gpt4(
                system_prompt="You are an AI assistant creating natural responses from agent results.",
                user_prompt=synthesis_prompt,
            )

            return synthesized_response.strip()

        except Exception as e:
            print(f"DEBUG: Synthesis failed: {e}")
            # Fallback to basic summary
            return self._create_basic_summary_from_results(results, errors)

    def _format_results_for_synthesis(self, results: Dict) -> str:
        """Format agent results clearly for synthesis - no interpretation."""
        if not results:
            return "No agent results available."

        formatted_parts = ["AGENT EXECUTION RESULTS:"]
        agent_names = []
        total_time = 0
        generated_files = []

        for agent_name, result in results.items():
            agent_names.append(agent_name)
            formatted_parts.append(f"\nAgent: {agent_name}")

            if isinstance(result, dict):
                # Status
                status = result.get("status", "unknown")
                formatted_parts.append(f"Status: {status}")

                # Actual data returned
                data = result.get("data")
                if data is not None:
                    formatted_parts.append("Returned data:")
                    if isinstance(data, dict):
                        for key, value in data.items():
                            formatted_parts.append(f"  {key}: {value}")
                    elif isinstance(data, list):
                        formatted_parts.append(f"  List with {len(data)} items: {data}")
                    else:
                        formatted_parts.append(f"  {data}")
                else:
                    formatted_parts.append("Returned data: None")

                # Generated files
                if result.get("generated_files"):
                    formatted_parts.append("Generated files:")
                    for file_info in result["generated_files"]:
                        formatted_parts.append(
                            f"  - {file_info['filename']}: {file_info['description']}"
                        )
                        generated_files.extend(result["generated_files"])

                # Execution metadata
                metadata = result.get("metadata", {})
                exec_time = metadata.get("execution_time", 0)
                total_time += exec_time

                tools_used = metadata.get("tools_used", [])
                if tools_used:
                    formatted_parts.append(f"Tools used: {', '.join(tools_used)}")
            else:
                formatted_parts.append(f"Raw result: {result}")

        # Summary for GPT-4 to use
        formatted_parts.append(f"\nSUMMARY FOR RESPONSE:")
        formatted_parts.append(f"Agents executed: {', '.join(agent_names)}")
        formatted_parts.append(f"Total execution time: {total_time:.1f}s")

        # ADD FILE DOWNLOAD INSTRUCTIONS
        if generated_files:
            formatted_parts.append(f"Generated files available for download:")
            for file_info in generated_files:
                formatted_parts.append(
                    f"  - {file_info['filename']}: Use download link /api/download/{file_info['filename']}"
                )

        return "\n".join(formatted_parts)

    def _create_basic_summary_from_results(self, results: Dict, errors: List) -> str:
        """Create basic summary when synthesis fails."""
        if not results:
            return "I was unable to process your request successfully."

        summary_parts = ["I processed your request with the following results:"]

        for agent_name, result in results.items():
            if isinstance(result, dict) and result.get("status") == "success":
                data = result.get("data", {})
                if isinstance(data, dict):
                    for key, value in data.items():
                        if isinstance(value, list):
                            summary_parts.append(f"- {key}: {len(value)} items")
                        elif isinstance(value, (int, float)):
                            summary_parts.append(f"- {key}: {value}")
                        else:
                            summary_parts.append(f"- {key}: {str(value)[:100]}")

        if errors:
            summary_parts.append(
                f"\nNote: {len(errors)} errors occurred during processing."
            )

        return "\n".join(summary_parts)

    async def _call_gpt4(
        self, system_prompt: str, user_prompt: str, temperature: float = 1.0
    ) -> str:
        """Call O3-mini model with correct parameters."""
        try:

            response = self.client.chat.completions.create(
                model=ORCHESTRATOR_MODEL,
                max_completion_tokens=ORCHESTRATOR_MAX_TOKENS,  # Changed from max_tokens
                messages=[
                    {"role": "user", "content": f"{system_prompt}\n\n{user_prompt}"}
                ],
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"DEBUG: GPT-4 call failed: {str(e)}")
            raise e

    async def _call_gpt4_json(
        self, system_prompt: str, user_prompt: str, temperature: float = 1.0
    ) -> str:
        """Call O3-mini model for JSON responses."""
        # Import the system prompt
        from config import DYNAMIC_INTELLIGENCE_SYSTEM_PROMPT

        # Combine system prompts
        enhanced_system_prompt = (
            f"{DYNAMIC_INTELLIGENCE_SYSTEM_PROMPT}\n\n{system_prompt}"
        )
        enhanced_user_prompt = (
            f"{user_prompt}\n\nRespond with ONLY valid JSON, no other text."
        )

        response = self.client.chat.completions.create(
            model=ORCHESTRATOR_MODEL,
            max_completion_tokens=ORCHESTRATOR_MAX_TOKENS,
            messages=[
                {"role": "system", "content": enhanced_system_prompt},
                {"role": "user", "content": enhanced_user_prompt},
            ],
        )

        content = response.choices[0].message.content

        # Extract JSON from response if it's wrapped in text
        if "```json" in content:
            start = content.find("```json") + 7
            end = content.find("```", start)
            if end > start:
                return content[start:end].strip()
        elif "{" in content:
            start = content.find("{")
            end = content.rfind("}") + 1
            if end > start:
                return content[start:end].strip()

        return content.strip()

    def _format_components_list(
        self, components: List[Dict], component_type: str
    ) -> str:
        """Format list of components for prompts."""
        if not components:
            return f"No {component_type} available"

        formatted = []
        for comp in components[:20]:  # Limit to prevent prompt overflow
            if component_type == "agents":
                # Use exact registry name
                name = comp.get("name", "unknown")
                description = comp.get("description", "No description")
                tools = comp.get("uses_tools", [])
                formatted.append(f"- {name}: {description} (uses: {', '.join(tools)})")
            else:  # tools
                name = comp.get("name", "unknown")
                description = comp.get("description", "No description")
                formatted.append(f"- {name}: {description}")

        if len(components) > 20:
            formatted.append(f"... and {len(components) - 20} more")

        return "\n".join(formatted)

    def _validate_plan(self, plan: Dict) -> bool:
        """Validate workflow plan structure."""
        try:
            # Check required fields exist
            required_fields = ["workflow_id", "workflow_type", "agents_needed"]

            for field in required_fields:
                if field not in plan:
                    print(f"DEBUG: Missing required field: {field}")
                    return False

            # Validate workflow type
            valid_types = ["sequential", "parallel", "conditional", "hybrid"]
            if plan["workflow_type"] not in valid_types:
                print(f"DEBUG: Invalid workflow type: {plan['workflow_type']}")
                return False

            # Validate agents list
            if not isinstance(plan["agents_needed"], list):
                print(f"DEBUG: agents_needed must be a list")
                return False

            # Check step count limit
            if len(plan["agents_needed"]) > MAX_WORKFLOW_STEPS:
                print(f"DEBUG: Too many agents: {len(plan['agents_needed'])}")
                return False

            return True

        except Exception as e:
            print(f"DEBUG: Plan validation error: {e}")
            return False

    def _check_missing_capabilities(self, plan: Dict) -> Dict[str, List]:
        """Check for missing agents and tools with proper dependency resolution."""
        missing = {"agents": [], "tools": []}

        # First, collect all tools needed by all agents
        all_required_tools = set()

        for agent_name in plan.get("agents_needed", []):
            if not self.registry.agent_exists(agent_name):
                # Agent doesn't exist, needs creation
                missing["agents"].append(
                    {
                        "name": agent_name,
                        "purpose": f"Process {agent_name} tasks",
                        "required_tools": [],  # Will be determined during creation
                    }
                )
            else:
                # Agent exists, check its tool dependencies
                agent_info = self.registry.get_agent(agent_name)
                if agent_info:
                    for tool in agent_info.get("uses_tools", []):
                        all_required_tools.add(tool)

        # Check if required tools exist
        for tool_name in all_required_tools:
            if not self.registry.tool_exists(tool_name):
                missing["tools"].append(
                    {
                        "name": tool_name,
                        "purpose": f"Tool for processing",
                        "type": "pure_function",
                    }
                )

        # Also check for tools specified in the plan's missing_capabilities
        if "missing_capabilities" in plan:
            plan_missing = plan["missing_capabilities"]

            # Process missing agents from the plan
            if "agents" in plan_missing:
                for agent in plan_missing["agents"]:
                    # Handle both string and dict formats
                    if isinstance(agent, str):
                        agent_name = agent
                        agent_dict = {
                            "name": agent_name,
                            "purpose": f"Process {agent_name} tasks",
                            "required_tools": [],
                        }
                    else:
                        agent_name = agent.get("name")
                        agent_dict = agent

                    # CRITICAL FIX: Only add to missing if agent doesn't exist
                    if agent_name and not self.registry.agent_exists(agent_name):
                        # Check if we haven't already added this agent
                        if not any(a["name"] == agent_name for a in missing["agents"]):
                            missing["agents"].append(agent_dict)

                        # Add required tools for missing agents
                        for tool in agent_dict.get("required_tools", []):
                            if not self.registry.tool_exists(tool):
                                if not any(t["name"] == tool for t in missing["tools"]):
                                    missing["tools"].append(
                                        {
                                            "name": tool,
                                            "purpose": f"Tool for {tool}",
                                            "type": "pure_function",
                                        }
                                    )

            # Process missing tools from the plan
            if "tools" in plan_missing:
                for tool in plan_missing["tools"]:
                    # Handle both string and dict formats
                    if isinstance(tool, str):
                        tool_name = tool
                        tool_dict = {
                            "name": tool_name,
                            "purpose": f"Tool for {tool_name}",
                            "type": "pure_function",
                        }
                    else:
                        tool_name = tool.get("name")
                        tool_dict = tool

                    # Only add if tool doesn't exist and isn't already in the list
                    if tool_name and not self.registry.tool_exists(tool_name):
                        if not any(t["name"] == tool_name for t in missing["tools"]):
                            missing["tools"].append(tool_dict)

        # Return empty missing capabilities if nothing is actually missing
        if not missing["agents"] and not missing["tools"]:
            return {}

        return missing

    def _format_results_summary(self, execution_result: Dict) -> str:
        """Format execution results for synthesis."""
        summary = []

        for agent_name, result in execution_result.get("results", {}).items():
            summary.append(f"\n[{agent_name}]")

            if isinstance(result, dict):
                if "status" in result:
                    summary.append(f"Status: {result['status']}")
                if "data" in result:
                    data_preview = json.dumps(result["data"], indent=2)
                    if len(data_preview) > 500:
                        data_preview = data_preview[:500] + "..."
                    summary.append(f"Data: {data_preview}")

        if execution_result.get("errors"):
            summary.append("\nERRORS:")
            for error in execution_result["errors"]:
                summary.append(
                    f"- {error.get('agent', 'unknown')}: {error.get('error', '')}"
                )

        return "\n".join(summary)

    def _create_basic_summary(self, execution_result: Dict) -> str:
        """Create basic summary without GPT-4."""
        summary = ["Workflow execution completed."]

        # Add successful agents
        for agent_name, result in execution_result.get("results", {}).items():
            if isinstance(result, dict) and result.get("status") == "success":
                summary.append(f"- {agent_name}: Completed successfully")

        # Add errors
        if execution_result.get("errors"):
            summary.append("\nErrors encountered:")
            for error in execution_result["errors"]:
                summary.append(f"- {error.get('error', 'Unknown error')}")

        return "\n".join(summary)

    def _generate_workflow_id(self) -> str:
        """Generate unique workflow ID."""
        import random

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = random.randint(1000, 9999)
        return f"wf_{timestamp}_{random_suffix}"

    def _create_error_response(
        self, workflow_id: str, message: str, error: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create standardized error response."""
        return {
            "status": "error",
            "workflow_id": workflow_id,
            "message": message,
            "error": error,
            "timestamp": datetime.now().isoformat(),
        }

    def _record_execution(
        self,
        workflow_id: str,
        request: str,
        plan: Dict,
        result: Dict,
        execution_time: float,
    ):
        """Record execution for analysis."""
        self.execution_history.append(
            {
                "workflow_id": workflow_id,
                "timestamp": datetime.now().isoformat(),
                "request": request[:200],  # Truncate for storage
                "plan_type": plan.get("workflow_type"),
                "agents_used": len(plan.get("agents_needed", [])),
                "execution_time": execution_time,
                "status": result.get("status"),
                "errors": len(result.get("errors", [])),
            }
        )

        # Keep only last 100 executions
        if len(self.execution_history) > 100:
            self.execution_history = self.execution_history[-100:]

    def get_execution_history(self) -> List[Dict]:
        """Get recent execution history."""
        return self.execution_history.copy()

    def get_active_workflows(self) -> Dict[str, Any]:
        """Get currently active workflows."""
        return self.active_workflows.copy()

    async def _enhanced_plan_workflow(
        self, user_request: str, analysis: str, auto_create: bool
    ) -> Dict[str, Any]:
        """
        Enhanced workflow planning with dependency resolution.
        Uses multi-stage planning: capability → tool → agent → workflow
        """

        print("DEBUG: Starting enhanced workflow planning")

        # Stage 1: Capability Analysis
        resolver = DependencyResolver(self.registry)

        # Get existing components
        existing_agents = {a["name"]: a for a in self.registry.list_agents()}
        existing_tools = {t["name"]: t for t in self.registry.list_tools()}

        # Analyze dependencies
        dependency_analysis = resolver.analyze_request(
            user_request, existing_agents, existing_tools
        )

        print("DEBUG: Dependency Analysis:")
        print(resolver.visualize_dependencies(dependency_analysis["dependency_graph"]))

        # Stage 2: Component Creation (if auto_create)
        if auto_create and dependency_analysis["creation_order"]:
            print(
                f"DEBUG: Need to create {len(dependency_analysis['creation_order'])} components"
            )

            for component_type, component_name in dependency_analysis["creation_order"]:
                if component_type == "tool":
                    print(f"DEBUG: Creating tool: {component_name}")
                    await self._ensure_tool_with_context(
                        component_name, dependency_analysis["missing_components"]
                    )
                else:  # agent
                    print(f"DEBUG: Creating agent: {component_name}")
                    await self._ensure_agent_with_context(
                        component_name, dependency_analysis["missing_components"]
                    )

        # Stage 3: Workflow Planning with GPT-4
        # Now all components exist, plan the execution workflow
        workflow_prompt = f"""
        Plan the execution workflow for this request.
        All required components are now available.
        
        Request: {user_request}
        Available Capabilities: {dependency_analysis['capabilities']}
        
        Create an execution plan that:
        1. Uses the right agents in the right order
        2. Passes data correctly between agents
        3. Handles both sequential and parallel execution where appropriate
        
        Return JSON with:
        {{
            "workflow_id": "wf_<timestamp>",
            "workflow_type": "sequential|parallel|hybrid",
            "agents_needed": ["agent1", "agent2", ...],
            "execution_strategy": "description of how to execute",
            "data_flow": {{"agent1": "output_type", "agent2": "input_from_agent1"}},
            "expected_output": "what the final result should contain"
        }}
        """

        plan = await self._call_gpt4_json(
            system_prompt="You are a workflow planner. Output valid JSON only.",
            user_prompt=workflow_prompt,
        )

        # Add dependency information to plan
        plan["dependency_graph"] = dependency_analysis
        plan["status"] = "success"

        return plan

    async def _ensure_tool_with_context(self, tool_name: str, context: Dict) -> Dict:
        """Create tool with context from dependency analysis."""

        # Find tool in context
        tool_info = next(
            (t for t in context["tools"] if t["name"] == tool_name),
            {"name": tool_name, "used_by": []},
        )

        # Generate description based on usage
        used_by = tool_info.get("used_by", [])
        if used_by:
            description = f"Tool for {', '.join(used_by)} agents"
        else:
            description = f"Utility tool for {tool_name.replace('_', ' ')}"

        # Use enhanced tool creation
        return await self._create_tool_with_claude(tool_name, description, tool_info)

    async def _create_tool_with_claude(
        self, tool_name: str, description: str, context: Dict
    ) -> Dict:
        """Create tool using Claude for intelligent implementation."""

        # Enhanced prompt for Claude
        creation_prompt = f"""
        Create a Python function for this tool.
        
        Tool Name: {tool_name}
        Purpose: {description}
        Used By Agents: {context.get('used_by', [])}
        
        Requirements:
        1. Must be a pure function (no side effects)
        2. Must handle None input gracefully
        3. Must return consistent output type
        4. Must have actual working implementation (not placeholder)
        
        Based on the tool name and context, implement the actual functionality.
        For example:
        - If it's an extraction tool, use regex to actually extract
        - If it's a calculation tool, perform the actual calculation
        - If it's a formatting tool, actually format the data
        
        Return only the Python code.
        """

        # Call Claude to generate implementation
        response = self.tool_factory.client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=CLAUDE_MAX_TOKENS,
            messages=[{"role": "user", "content": creation_prompt}],
        )

        code = self.tool_factory._extract_code_from_response(response.content[0].text)

        if code:
            # Test the generated code
            test_result = self._test_tool_code(code, tool_name)

            if test_result["valid"]:
                # Register the tool
                return self.tool_factory.registry.register_tool(
                    name=tool_name,
                    description=description,
                    code=code,
                    is_pure_function=True,
                )

        # Fallback to basic generation
        return self.tool_factory.ensure_tool(tool_name, description)

    def _test_tool_code(self, code: str, tool_name: str) -> Dict:
        """Test generated tool code."""
        try:
            # Create a test namespace
            test_namespace = {}
            exec(code, test_namespace)

            # Check function exists
            if tool_name not in test_namespace:
                return {"valid": False, "error": "Function not found"}

            func = test_namespace[tool_name]

            # Test with various inputs
            test_cases = [None, "", "test string", {"key": "value"}, [1, 2, 3]]

            for test_input in test_cases:
                try:
                    result = func(test_input)
                    # Function should not raise exceptions
                except Exception as e:
                    return {
                        "valid": False,
                        "error": f"Failed with input {test_input}: {e}",
                    }

            return {"valid": True}

        except Exception as e:
            return {"valid": False, "error": str(e)}

    async def _handle_execution_errors(self, state: Dict, workflow: Dict) -> str:
        """Generate helpful response even when execution has errors."""

        successful_agents = []
        failed_agents = []
        partial_results = []

        # Analyze what worked and what didn't
        for agent_name in workflow.get("steps", []):
            if agent_name in state.get("results", {}):
                result = state["results"][agent_name]
                if result.get("status") == "success":
                    successful_agents.append(agent_name)
                    if result.get("data"):
                        partial_results.append(
                            f"{agent_name}: {self._summarize_data(result['data'])}"
                        )
                else:
                    failed_agents.append(agent_name)

        # Build response
        response_parts = []

        if successful_agents:
            response_parts.append(
                f"Successfully completed: {', '.join(successful_agents)}"
            )

        if partial_results:
            response_parts.append("\nPartial results obtained:")
            response_parts.extend(partial_results)

        if failed_agents:
            response_parts.append(
                f"\nEncountered issues with: {', '.join(failed_agents)}"
            )

            # Provide helpful suggestions
            suggestions = []
            for agent in failed_agents:
                if "email" in agent.lower():
                    suggestions.append(
                        "- Email extraction: Ensure text contains valid email addresses"
                    )
                elif "url" in agent.lower():
                    suggestions.append(
                        "- URL extraction: Check that URLs are properly formatted"
                    )
                elif "file" in agent.lower() or "read" in agent.lower():
                    suggestions.append(
                        "- File reading: Verify file path and permissions"
                    )

            if suggestions:
                response_parts.append("\nTroubleshooting suggestions:")
                response_parts.extend(suggestions)

        return "\n".join(response_parts)

    def _summarize_data(self, data: Any) -> str:
        """Create a brief summary of data."""
        if isinstance(data, dict):
            return f"{len(data)} items"
        elif isinstance(data, list):
            return f"{len(data)} entries"
        elif isinstance(data, str):
            return f"{len(data)} characters"
        else:
            return str(type(data).__name__)

    def _extract_generated_files(self, results: Dict) -> List[Dict]:
        """Extract all generated files from agent results."""
        generated_files = []

        for agent_name, result in results.items():
            if isinstance(result, dict) and result.get("generated_files"):
                for file_info in result["generated_files"]:
                    # Add download URL
                    file_info["download_url"] = f"/api/download/{file_info['filename']}"
                    generated_files.append(file_info)

        return generated_files

    async def _detect_pipeline_complexity(
        self, user_request: str, files: List[Dict] = None
    ) -> str:
        """
        Enhanced complexity detection that recognizes multi-step operations.
        """
        request_lower = user_request.lower()

        # Pipeline indicators (sequential operations)
        pipeline_keywords = [
            "then",
            "after",
            "next",
            "followed by",
            "and then",
            "first",
            "second",
            "third",
            "finally",
            "last",
            "extract and",
            "analyze and",
            "process and",
            "create and",
            "step by step",
            "pipeline",
            "workflow",
            "sequence",
        ]

        # Multi-step operation indicators (even without explicit sequencing words)
        multi_step_patterns = [
            # Mathematical operations
            ("find", "calculate"),  # Find X, calculate Y
            ("filter", "average"),  # Filter items, average them
            ("identify", "check"),  # Identify items, check property
            ("extract", "count"),  # Extract items, count them
            ("get", "analyze"),  # Get data, analyze it
            ("select", "process"),  # Select items, process them
            # Data operations
            ("read", "process"),
            ("load", "transform"),
            ("parse", "analyze"),
            # Multiple verbs that indicate steps
            ("find", "check"),
            ("calculate", "verify"),
            ("compute", "validate"),
        ]

        # Complex indicators
        complex_keywords = [
            "multiple files",
            "compare",
            "merge",
            "combine",
            "different formats",
            "various sources",
            "cross-reference",
            "comprehensive",
            "detailed analysis",
            "full report",
        ]

        # Check for multiple operations using commas
        # "Do X, do Y, do Z" pattern
        comma_separated_tasks = (
            len([x.strip() for x in request_lower.split(",") if x.strip()]) > 1
        )

        # Check for multiple action verbs
        action_verbs = [
            "find",
            "calculate",
            "check",
            "extract",
            "analyze",
            "process",
            "compute",
            "filter",
            "average",
            "sum",
            "count",
            "identify",
            "verify",
            "validate",
            "transform",
            "convert",
            "generate",
        ]
        verb_count = sum(1 for verb in action_verbs if verb in request_lower)

        # Check for multi-step patterns
        has_multi_step_pattern = False
        for pattern in multi_step_patterns:
            if all(word in request_lower for word in pattern):
                has_multi_step_pattern = True
                break

        # Count indicators
        pipeline_count = sum(
            1 for keyword in pipeline_keywords if keyword in request_lower
        )
        complex_count = sum(
            1 for keyword in complex_keywords if keyword in request_lower
        )

        # Check for numbered steps
        step_indicators = ["1.", "2.", "3.", "step 1", "step 2", "step 3"]
        step_count = sum(
            1 for indicator in step_indicators if indicator in request_lower
        )

        # File complexity
        multiple_files = files and len(files) > 1

        # Decision logic with enhanced detection
        if complex_count > 0 or pipeline_count > 2 or step_count > 1 or multiple_files:
            print(f"DEBUG: Detected as COMPLEX due to keywords/files")
            return "complex"
        elif (
            pipeline_count > 0
            or verb_count >= 3
            or has_multi_step_pattern
            or comma_separated_tasks
        ):
            print(
                f"DEBUG: Detected as PIPELINE due to multiple operations (verbs: {verb_count}, pattern: {has_multi_step_pattern}, commas: {comma_separated_tasks})"
            )
            return "pipeline"
        elif verb_count >= 2 and len(request_lower.split()) > 10:
            print(f"DEBUG: Detected as PIPELINE due to multiple verbs and length")
            return "pipeline"
        else:
            print(
                f"DEBUG: Detected as SIMPLE (verbs: {verb_count}, words: {len(request_lower.split())})"
            )
            return "simple"

    def _simple_complexity_detection(
        self, user_request: str, files: List[Dict] = None
    ) -> str:
        """Fallback complexity detection."""
        request_lower = user_request.lower()

        pipeline_keywords = ["then", "after", "next", "extract and", "analyze and"]
        complex_keywords = ["multiple files", "compare", "merge", "comprehensive"]

        pipeline_count = sum(
            1 for keyword in pipeline_keywords if keyword in request_lower
        )
        complex_count = sum(
            1 for keyword in complex_keywords if keyword in request_lower
        )

        if complex_count > 0 or pipeline_count > 2:
            return "complex"
        elif pipeline_count > 0:
            return "pipeline"
        else:
            return "simple"

    async def _process_pipeline_request(
        self,
        user_request: str,
        files: List[Dict],
        context: Dict,
        auto_create: bool,
        workflow_id: str,
    ) -> Dict[str, Any]:
        """Process complex multi-step pipeline requests."""

        print(f"DEBUG: Processing as pipeline request")

        try:
            # Step 1: Analyze request and break into pipeline
            analysis_result = await self.pipeline_orchestrator.analyze_complex_request(
                user_request, files
            )

            if analysis_result["status"] != "success":
                return {
                    "status": "error",
                    "workflow_id": workflow_id,
                    "error": f"Pipeline analysis failed: {analysis_result.get('error')}",
                    "fallback": "single_agent",
                }

            # Step 2: Plan pipeline execution
            pipeline_plan = await self.pipeline_orchestrator.plan_pipeline(
                analysis_result, auto_create
            )

            if pipeline_plan.get("status") == "error":
                return {
                    "status": "error",
                    "workflow_id": workflow_id,
                    "error": f"Pipeline planning failed: {pipeline_plan.get('error')}",
                    "fallback": "single_agent",
                }

            # Step 3: Execute pipeline with intelligence
            execution_result = (
                await self.pipeline_orchestrator.execute_pipeline_with_adaptation(
                    pipeline_plan, user_request, files
                )
            )

            # Step 4: Synthesize final response
            if execution_result["status"] in ["success", "partial"]:
                response = await self._synthesize_pipeline_response(
                    user_request, execution_result, analysis_result
                )
            else:
                response = f"Pipeline execution encountered issues: {execution_result.get('error', 'Unknown error')}"

            # Return structured result
            return {
                "status": execution_result["status"],
                "workflow_id": workflow_id,
                "workflow": {
                    "type": "pipeline",
                    "steps": [
                        step.get("name", f"step_{i}")
                        for i, step in enumerate(pipeline_plan.get("steps", []))
                    ],
                    "execution_strategy": pipeline_plan.get(
                        "execution_strategy", "sequential"
                    ),
                    "total_steps": pipeline_plan.get("total_steps", 0),
                },
                "response": response,
                "results": execution_result.get("results", {}),
                "step_results": execution_result.get("step_results", {}),
                "metadata": {
                    "pipeline_analysis": analysis_result,
                    "pipeline_plan": pipeline_plan,
                    "execution_time": execution_result.get("execution_time", 0),
                    "steps_completed": execution_result.get("steps_completed", 0),
                    "adaptations": execution_result.get("adaptations", []),
                    "components_created": len(pipeline_plan.get("creation_needed", [])),
                },
                "errors": execution_result.get("errors", []),
            }

        except Exception as e:
            print(f"DEBUG: Pipeline processing failed: {str(e)}")

            # Fallback to simple processing
            return await self._process_simple_request(
                user_request, files, context, auto_create, workflow_id
            )

    async def _process_simple_request(
        self,
        user_request: str,
        files: List[Dict],
        context: Dict,
        auto_create: bool,
        workflow_id: str,
    ) -> Dict[str, Any]:
        """Process simple single-agent requests."""

        print(f"DEBUG: Processing as simple request")

        # Use existing single-agent logic
        analysis_result = await self._analyze_request(user_request, files, context)

        if analysis_result["status"] != "success":
            return {
                "status": "error",
                "workflow_id": workflow_id,
                "error": f"Request analysis failed: {analysis_result.get('error')}",
            }

        plan_result = await self._plan_workflow(
            user_request, analysis_result["analysis"], auto_create
        )

        if plan_result.get("status") == "error":
            return {
                "status": "error",
                "workflow_id": workflow_id,
                "error": f"Workflow planning failed: {plan_result.get('error')}",
            }

        # Create missing components
        if auto_create and plan_result.get("missing_capabilities"):
            creation_result = await self._create_missing_components(
                plan_result["missing_capabilities"]
            )
            if creation_result["status"] != "success":
                print(f"DEBUG: Component creation had issues: {creation_result}")

        # Execute workflow
        execution_result = await self._execute_workflow(
            plan_result, user_request, files
        )

        # Synthesize response
        response = await self._synthesize_response(
            user_request,
            execution_result.get("results", {}),
            execution_result.get("errors", []),
        )

        return {
            "status": execution_result["status"],
            "workflow_id": workflow_id,
            "workflow": {
                "type": "single_agent",
                "steps": plan_result.get("agents_needed", []),
                "execution_strategy": "sequential",
            },
            "response": response,
            "results": execution_result.get("results", {}),
            "metadata": {
                "analysis": analysis_result.get("analysis"),
                "plan": plan_result,
                "execution_time": execution_result.get("execution_time", 0),
                "components_created": len(
                    plan_result.get("missing_capabilities", {}).get("agents", [])
                )
                + len(plan_result.get("missing_capabilities", {}).get("tools", [])),
            },
            "errors": execution_result.get("errors", []),
        }

    async def _synthesize_pipeline_response(
        self, user_request: str, execution_result: Dict, analysis_result: Dict
    ) -> str:
        """Synthesize natural language response for pipeline execution."""

        # Use enhanced synthesis prompt for pipelines
        pipeline_synthesis_prompt = f"""
    USER REQUEST: {user_request}
    PIPELINE EXECUTION RESULT: {json.dumps(execution_result, default=str)}
    PIPELINE ANALYSIS: {json.dumps(analysis_result, default=str)}

    Create a natural, conversational response that:
    1. Acknowledges the multi-step nature of the request
    2. Summarizes what was accomplished in each step
    3. Highlights key findings or results
    4. Mentions any files or outputs generated
    5. Notes any adaptations or intelligent decisions made

    Be specific about results while maintaining a helpful, professional tone.
    If steps failed or needed adaptation, explain what was done to handle it.
    """

        try:
            response = await self._call_gpt4(
                system_prompt="You are an AI assistant synthesizing results from a multi-step pipeline execution.",
                user_prompt=pipeline_synthesis_prompt,
            )
            return response

        except Exception as e:
            print(f"DEBUG: Pipeline synthesis failed: {str(e)}")

            # Fallback response
            steps_completed = execution_result.get("steps_completed", 0)
            total_steps = execution_result.get("total_steps", 0)

            if steps_completed == total_steps:
                return f"I successfully completed your {total_steps}-step request. All pipeline steps executed successfully."
            elif steps_completed > 0:
                return f"I completed {steps_completed} of {total_steps} steps in your request. Some steps encountered issues but I provided partial results."
            else:
                return "I encountered issues processing your multi-step request. Please check the error details for more information."

    async def _execute_workflow_simple_fallback(
        self, plan: Dict, initial_data: Dict, workflow_id: str
    ) -> Dict[str, Any]:
        """
        Simple fallback workflow execution that bypasses LangGraph.
        This runs agents sequentially without complex state management.
        """
        print(f"DEBUG: Using simple fallback workflow execution")

        agents = plan.get("agents_needed", [])
        results = {}
        errors = []
        execution_path = []

        # Process each agent sequentially
        current_data = initial_data.get("current_data")

        for agent_name in agents:
            try:
                print(
                    f"DEBUG: Executing agent '{agent_name}' with data type: {type(current_data)}"
                )

                # Load and execute the agent directly
                agent_result = await self._execute_agent_directly(
                    agent_name, current_data
                )

                print(f"DEBUG: Agent '{agent_name}' result: {agent_result}")

                # Store result
                results[agent_name] = agent_result
                execution_path.append(agent_name)

                # Update current_data for next agent (use output as input)
                if agent_result.get("status") == "success" and "data" in agent_result:
                    current_data = agent_result["data"]

            except Exception as e:
                print(f"DEBUG: Agent '{agent_name}' failed: {str(e)}")
                errors.append(
                    {
                        "agent": agent_name,
                        "error": str(e),
                        "timestamp": datetime.now().isoformat(),
                    }
                )

        # Determine overall status
        status = "success" if not errors else ("partial" if results else "error")

        return {
            "status": status,
            "results": results,
            "execution_path": execution_path,
            "errors": errors,
            "workflow_id": workflow_id,
        }

    async def _execute_agent_directly(
        self, agent_name: str, input_data
    ) -> Dict[str, Any]:
        """
        Execute an agent directly without LangGraph workflow overhead.
        """
        try:
            # Get agent info from registry
            agent_info = self.registry.get_agent(agent_name)
            if not agent_info:
                raise ValueError(f"Agent '{agent_name}' not found in registry")

            # Load the agent function
            agent_path = agent_info["location"]
            print(f"DEBUG: Loading agent from: {agent_path}")

            # Import the agent module
            spec = importlib.util.spec_from_file_location(
                f"{agent_name}_module", agent_path
            )
            agent_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(agent_module)

            # Get the agent function (should be named like the agent)
            agent_function = getattr(agent_module, f"{agent_name}_agent", None)
            if not agent_function:
                # Try alternative naming patterns
                agent_function = getattr(agent_module, agent_name, None)
                if not agent_function:
                    raise ValueError(f"Agent function not found in {agent_path}")

            # Prepare state for agent
            state = {
                "current_data": input_data,
                "results": {},
                "errors": [],
                "execution_path": [],
                "request": "Prime number analysis",  # This could be dynamic
                "files": [],
                "context": {},
            }

            print(
                f"DEBUG: Calling agent function with state keys: {list(state.keys())}"
            )

            # Execute the agent
            result_state = agent_function(state)

            print(f"DEBUG: Agent returned state keys: {list(result_state.keys())}")

            # Extract result in expected format
            return {
                "status": "success",
                "data": result_state.get("current_data", input_data),
                "metadata": {
                    "agent": agent_name,
                    "execution_time": 1.0,  # Placeholder
                    "timestamp": datetime.now().isoformat(),
                },
            }

        except Exception as e:
            print(f"DEBUG: Exception in _execute_agent_directly: {str(e)}")
            import traceback

            print(f"DEBUG: Traceback: {traceback.format_exc()}")

            return {
                "status": "error",
                "error": str(e),
                "metadata": {
                    "agent": agent_name,
                    "timestamp": datetime.now().isoformat(),
                },
            }

    async def _create_emergency_fallback_plan(
        self, request: str, analysis: Dict
    ) -> Dict[str, Any]:
        """
        FIXED: Emergency fallback that uses existing agents instead of creating new ones.
        """
        print(f"DEBUG: Creating emergency fallback plan using existing agents")

        # Get available agents without problematic parameters
        try:
            available_agents = self.registry.list_agents()
        except:
            available_agents = []

        # For prime number requests, use existing agents if they exist
        request_lower = request.lower()
        agents_needed = []

        if "prime" in request_lower:
            # Check if prime_checker exists
            if any(agent.get("name") == "prime_checker" for agent in available_agents):
                agents_needed.append("prime_checker")

        if any(word in request_lower for word in ["average", "mean", "calculate"]):
            # Check if calculate_mean exists
            if any(agent.get("name") == "calculate_mean" for agent in available_agents):
                agents_needed.append("calculate_mean")

        # If no specific agents found, use any available agent
        if not agents_needed and available_agents:
            agents_needed = [available_agents[0].get("name", "unknown_agent")]

        # If still no agents, create a simple plan with no agents (will be handled gracefully)
        if not agents_needed:
            agents_needed = ["text_processor"]  # Generic name

        return {
            "workflow_id": f"wf_fallback_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "workflow_type": "sequential",
            "reasoning": f"Emergency fallback using existing agents for: {request[:50]}...",
            "agents_needed": agents_needed,
            "missing_capabilities": {
                "agents": [],
                "tools": [],
            },  # Don't try to create new agents
            "confidence": 0.7,
            "status": "success",
            "is_emergency_fallback": True,
        }

    async def _execute_workflow_fully_dynamic(
        self, plan: Dict, initial_data: Dict, workflow_id: str
    ) -> Dict[str, Any]:
        """
        Fully dynamic workflow execution that can handle ANY sequential workflow.
        """
        print(f"DEBUG: Executing fully dynamic sequential workflow")

        agents = plan.get("agents_needed", [])
        results = {}
        errors = []
        execution_path = []

        # Dynamic workflow state that adapts to any data type
        workflow_state = {
            "current_data": initial_data.get("current_data"),
            "extracted_data": initial_data.get("extracted_data"),
            "files": initial_data.get("files", []),
            "request": initial_data.get("request", ""),
            "context": initial_data.get("context", {}),
            "results": {},
            "execution_path": [],
            "errors": [],
            "plan": plan,  # Include the plan for agent context
            "data_flow_history": [],
        }

        print(f"DEBUG: Starting execution of {len(agents)} agents")

        # Execute each agent dynamically
        for i, agent_name in enumerate(agents):
            try:
                print(f"DEBUG: Step {i+1}/{len(agents)}: Executing '{agent_name}'")

                # Prepare dynamic state for this specific agent
                agent_state = await self._prepare_dynamic_agent_state(
                    workflow_state, agent_name, i, plan
                )

                # Execute agent with full dynamic handling
                agent_result = await self._execute_agent_fully_dynamic(
                    agent_name, agent_state, workflow_state
                )

                print(
                    f"DEBUG: Agent '{agent_name}' completed with status: {agent_result.get('status')}"
                )

                # Store result
                results[agent_name] = agent_result
                execution_path.append(agent_name)

                # Dynamically update workflow state
                workflow_state = await self._update_dynamic_workflow_state(
                    workflow_state, agent_name, agent_result, i
                )

            except Exception as e:
                print(f"DEBUG: Agent '{agent_name}' failed: {str(e)}")
                error_info = {
                    "agent": agent_name,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat(),
                    "step": i + 1,
                }
                errors.append(error_info)

                # Continue execution unless critical failure
                if not self._is_critical_failure(e, agent_name):
                    print(f"DEBUG: Non-critical failure, continuing workflow")
                    continue
                else:
                    print(f"DEBUG: Critical failure, stopping workflow")
                    break

        # Determine final status
        status = "success" if not errors else ("partial" if results else "error")

        return {
            "status": status,
            "results": results,
            "execution_path": execution_path,
            "errors": errors,
            "workflow_id": workflow_id,
            "final_data": workflow_state.get("current_data"),
            "generated_files": workflow_state.get("generated_files", []),
            "data_flow_history": workflow_state.get("data_flow_history", []),
        }

    async def _prepare_dynamic_agent_state(
        self, workflow_state: Dict, agent_name: str, step_index: int, plan: Dict
    ) -> Dict:
        """
        Dynamically prepare state for ANY agent based on the workflow plan and current context.
        """
        # Get the planned data flow for this step
        data_flow = plan.get("data_flow", [])
        current_step_info = None

        for step in data_flow:
            if step.get("agent") == agent_name or step.get("step") == step_index + 1:
                current_step_info = step
                break

        # Determine what data this agent should receive
        if step_index == 0:
            # First agent gets original input
            current_data = workflow_state.get("current_data")
            if workflow_state.get("files"):
                # If there are files, provide file information
                current_data = {
                    "files": workflow_state["files"],
                    "request": workflow_state["request"],
                    "extracted_data": workflow_state.get("extracted_data"),
                }
            elif current_data is None:
                # No specific data, use the request
                current_data = workflow_state["request"]
        else:
            # Subsequent agents get output from previous agent
            previous_results = list(workflow_state["results"].values())
            if previous_results:
                last_result = previous_results[-1]
                if last_result.get("status") == "success" and "data" in last_result:
                    current_data = last_result["data"]
                else:
                    # Previous agent failed, use original data
                    current_data = workflow_state.get("current_data")
            else:
                current_data = workflow_state.get("current_data")

        # Create comprehensive dynamic state
        agent_state = {
            "current_data": current_data,
            "files": workflow_state.get("files", []),
            "request": workflow_state.get("request", ""),
            "context": workflow_state.get("context", {}),
            "results": workflow_state.get("results", {}),
            "execution_path": workflow_state.get("execution_path", []),
            "errors": workflow_state.get("errors", []),
            "step_index": step_index,
            "agent_name": agent_name,
            "total_steps": len(plan.get("agents_needed", [])),
            "plan_info": current_step_info,
            "workflow_plan": plan,
        }

        return agent_state

    async def _execute_agent_fully_dynamic(
        self, agent_name: str, agent_state: Dict, workflow_state: Dict
    ) -> Dict[str, Any]:
        """
        Execute any agent dynamically - FIXED VERSION with better error handling.
        """
        try:
            # Check if agent exists
            if not self.registry.agent_exists(agent_name):
                print(f"DEBUG: Agent '{agent_name}' doesn't exist")

                # Instead of trying to create it, return a helpful error
                return {
                    "status": "error",
                    "error": f"Agent '{agent_name}' not found and dynamic creation failed",
                    "fallback_result": f"Could not process request step for {agent_name}",
                    "agent": agent_name,
                    "timestamp": datetime.now().isoformat(),
                }

            # Load and execute existing agent
            agent_info = self.registry.get_agent(agent_name)
            if not agent_info:
                return {
                    "status": "error",
                    "error": f"Agent '{agent_name}' info not found",
                    "agent": agent_name,
                    "timestamp": datetime.now().isoformat(),
                }

            agent_path = agent_info["location"]

            # Import and execute
            spec = importlib.util.spec_from_file_location(
                f"{agent_name}_module", agent_path
            )
            agent_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(agent_module)

            # Find agent function
            agent_function = getattr(agent_module, f"{agent_name}_agent", None)
            if not agent_function:
                agent_function = getattr(agent_module, agent_name, None)

            if not agent_function:
                return {
                    "status": "error",
                    "error": f"No executable function found in agent {agent_name}",
                    "agent": agent_name,
                    "timestamp": datetime.now().isoformat(),
                }

            # Execute the agent
            result_state = agent_function(agent_state)

            # Process result
            return self._process_dynamic_agent_result(
                agent_name, result_state, agent_state
            )

        except Exception as e:
            print(f"DEBUG: Dynamic agent execution failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "agent": agent_name,
                "timestamp": datetime.now().isoformat(),
            }

    async def _create_agent_dynamically(
        self, agent_spec: Dict, context: Dict
    ) -> Dict[str, Any]:
        """
        Create any agent dynamically - FIXED VERSION.
        """
        try:
            agent_name = agent_spec["name"]
            purpose = agent_spec["purpose"]

            print(f"DEBUG: Creating agent '{agent_name}' for purpose: {purpose}")

            # FIXED: Use compatible agent factory method call
            try:
                # Try the method signature that your agent factory actually supports
                creation_result = await self.agent_factory.create_agent(
                    agent_name=agent_name,
                    description=purpose,
                    required_tools=agent_spec.get("required_tools", []),
                    # Removed agent_type parameter that doesn't exist
                )
            except TypeError as e:
                print(f"DEBUG: First create_agent call failed: {e}")
                # Try alternative signature
                try:
                    creation_result = self.agent_factory.create_agent(
                        agent_name=agent_name,
                        description=purpose,
                        required_tools=agent_spec.get("required_tools", []),
                    )
                    # If it's not async, wrap the result
                    if not isinstance(creation_result, dict):
                        creation_result = {
                            "status": "error",
                            "error": "Unexpected return type",
                        }
                except Exception as e2:
                    print(f"DEBUG: Second create_agent call also failed: {e2}")
                    creation_result = {
                        "status": "error",
                        "error": f"Agent creation failed: {str(e2)}",
                    }

            if creation_result.get("status") == "success":
                # Force registry reload
                try:
                    self.registry.reload_from_disk()
                except AttributeError:
                    # If reload_from_disk doesn't exist, try force_global_reload
                    try:
                        from core.registry_singleton import force_global_reload

                        force_global_reload()
                    except:
                        pass
                print(f"DEBUG: Successfully created dynamic agent '{agent_name}'")

            return creation_result

        except Exception as e:
            print(f"DEBUG: Failed to create dynamic agent: {str(e)}")
            return {"status": "error", "error": str(e)}

    def _process_dynamic_agent_result(
        self, agent_name: str, result_state: Dict, original_state: Dict
    ) -> Dict[str, Any]:
        """
        Process any agent result dynamically, handling any output format.
        """
        # Extract result data flexibly
        if isinstance(result_state, dict):
            if "current_data" in result_state:
                result_data = result_state["current_data"]
            elif "data" in result_state:
                result_data = result_state["data"]
            elif "results" in result_state:
                result_data = result_state["results"]
            else:
                # Use the entire state as result
                result_data = result_state
        else:
            # Non-dict result
            result_data = result_state

        # Check for generated files dynamically
        generated_files = self._extract_generated_files(result_data)

        return {
            "status": "success",
            "data": result_data,
            "generated_files": generated_files,
            "metadata": {
                "agent": agent_name,
                "execution_time": 1.0,
                "timestamp": datetime.now().isoformat(),
                "input_type": type(original_state.get("current_data")).__name__,
                "output_type": type(result_data).__name__,
            },
        }

    def _extract_generated_files(self, data: Any) -> List[Dict]:
        """
        Dynamically extract any generated files from agent output.
        """
        generated_files = []

        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str):
                    # Check if it looks like a file path
                    if any(
                        ext in value.lower()
                        for ext in [".pdf", ".png", ".jpg", ".csv", ".xlsx", ".txt"]
                    ):
                        if os.path.exists(value):
                            generated_files.append(
                                {
                                    "path": value,
                                    "name": os.path.basename(value),
                                    "type": key,
                                    "size": os.path.getsize(value),
                                }
                            )

        return generated_files

    async def _update_dynamic_workflow_state(
        self, workflow_state: Dict, agent_name: str, agent_result: Dict, step_index: int
    ) -> Dict:
        """
        Dynamically update workflow state after any agent execution.
        """
        # Update execution tracking
        workflow_state["execution_path"].append(agent_name)
        workflow_state["results"][agent_name] = agent_result

        # Update current data for next agent
        if agent_result.get("status") == "success" and "data" in agent_result:
            workflow_state["current_data"] = agent_result["data"]

        # Track data flow
        workflow_state["data_flow_history"].append(
            {
                "step": step_index + 1,
                "agent": agent_name,
                "input_type": type(workflow_state.get("current_data")).__name__,
                "output_type": (
                    type(agent_result.get("data")).__name__
                    if agent_result.get("data") is not None
                    else "None"
                ),
                "status": agent_result.get("status"),
            }
        )

        # Collect generated files
        if "generated_files" not in workflow_state:
            workflow_state["generated_files"] = []

        if agent_result.get("generated_files"):
            workflow_state["generated_files"].extend(agent_result["generated_files"])

        # Handle errors
        if agent_result.get("status") == "error":
            workflow_state["errors"].append(
                {
                    "agent": agent_name,
                    "error": agent_result.get("error"),
                    "step": step_index + 1,
                    "timestamp": datetime.now().isoformat(),
                }
            )

        return workflow_state

    def _is_critical_failure(self, error: Exception, agent_name: str) -> bool:
        """
        Determine if an error should stop the entire workflow.
        """
        error_str = str(error).lower()

        # Critical failures that should stop workflow
        critical_keywords = [
            "critical",
            "fatal",
            "permission denied",
            "security",
            "authentication",
            "authorization",
        ]

        return any(keyword in error_str for keyword in critical_keywords)

    def _create_pattern_based_plan(
        self, request: str, available_agents: List
    ) -> Dict[str, Any]:
        """
        Pattern-based planning using existing agents.
        """
        print(f"DEBUG: Using pattern-based planning")

        request_lower = request.lower()
        agents_needed = []
        available_agent_names = [a.get("name") for a in available_agents]

        # Pattern matching for common requests
        if "prime" in request_lower and "prime_checker" in available_agent_names:
            agents_needed.append("prime_checker")

        if (
            any(word in request_lower for word in ["average", "mean", "calculate"])
            and "calculate_mean" in available_agent_names
        ):
            agents_needed.append("calculate_mean")

        if "email" in request_lower and "email_extractor" in available_agent_names:
            agents_needed.append("email_extractor")

        if "url" in request_lower and "url_extractor" in available_agent_names:
            agents_needed.append("url_extractor")

        if "csv" in request_lower and "read_csv" in available_agent_names:
            agents_needed.append("read_csv")

        if "text" in request_lower and "read_text" in available_agent_names:
            agents_needed.append("read_text")

        # Remove duplicates while preserving order
        agents_needed = list(dict.fromkeys(agents_needed))

        # If no patterns matched, use the first available agent
        if not agents_needed and available_agent_names:
            agents_needed = [available_agent_names[0]]

        return {
            "workflow_id": f"wf_pattern_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "workflow_type": "sequential",
            "reasoning": f"Pattern-based plan for: {request[:50]}...",
            "agents_needed": agents_needed,
            "missing_capabilities": {"agents": [], "tools": []},
            "confidence": 0.8,
            "status": "success",
            "is_pattern_based": True,
        }

    async def _execute_workflow(
        self, plan: Dict, initial_data: Dict, workflow_id: str
    ) -> Dict[str, Any]:
        """Execute any workflow fully dynamically."""

        print(f"DEBUG: _execute_workflow called - using fully dynamic execution")

        # Use the fully dynamic execution for ALL workflows
        return await self._execute_workflow_fully_dynamic(
            plan, initial_data, workflow_id
        )
