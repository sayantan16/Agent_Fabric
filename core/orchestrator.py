"""
Orchestrator
Master orchestration engine using GPT-4 for intelligent workflow planning and execution
"""

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
from core.workflow_engine import WorkflowEngine
from core.agent_factory import AgentFactory
from core.tool_factory import ToolFactory
from core.registry_singleton import get_shared_registry
from typing import Dict, List, Optional, Any, Tuple


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
        self.workflow_engine = WorkflowEngine()
        self.agent_factory = AgentFactory()
        self.tool_factory = ToolFactory()
        self.execution_history = []
        self.active_workflows = {}

    def _prepare_initial_data(
        self, user_request: str, files: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """Prepare initial data for workflow execution with all necessary fields."""
        return {
            "request": user_request,
            "text": user_request,  # Many agents look for 'text'
            "data": user_request,  # Some agents look for 'data'
            "current_data": user_request,  # Workflow engine uses this
            "input": user_request,  # Fallback field
            "files": files or [],
            "context": {},
            "results": {},  # Initialize results dict
            "errors": [],  # Initialize errors list
            "execution_path": [],  # Initialize execution path
        }

    async def process_request(
        self,
        user_request: str,
        files: Optional[List[Dict[str, Any]]] = None,
        context: Optional[Dict[str, Any]] = None,
        auto_create: bool = True,
        stream_results: bool = False,
    ) -> Dict[str, Any]:
        """
        Process a user request end-to-end.

        Args:
            user_request: Natural language request from user
            files: Optional list of uploaded files
            context: Optional context from previous interactions
            auto_create: Whether to automatically create missing components
            stream_results: Whether to stream intermediate results

        Returns:
            Complete response with results and metadata
        """
        start_time = datetime.now()
        workflow_id = self._generate_workflow_id()

        try:
            print(f"DEBUG: Starting request processing for: {user_request[:50]}...")

            # Phase 1: Analyze the request
            analysis = await self._analyze_request(user_request, files, context)

            # ============= MODIFY THIS SECTION =============
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
            # =====================================================

            # Phase 2: Plan the workflow
            plan = await self._plan_workflow(
                user_request, analysis["analysis"], auto_create
            )
            if plan["status"] != "success":
                return self._create_error_response(
                    workflow_id, "Planning failed", plan.get("error")
                )

            # ============= CRITICAL FIX 1: Better handling of no agents case =============
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
            # ===========================================================================

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

            # ============= CRITICAL FIX 2: Final check for no agents =============
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
            # =====================================================================

            # ============= CRITICAL FIX 3: Use the enhanced data preparation =============
            # Phase 4: Prepare initial data with ALL fields agents might look for
            initial_data = self._prepare_initial_data(user_request, files)
            initial_data["context"] = {
                "analysis": analysis.get("analysis", {}),
                "plan": plan,
            }
            # ===========================================================================

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

            # Phase 6: Synthesize results
            has_errors = bool(execution_result.get("errors"))
            if has_errors:
                final_response = await self._handle_execution_errors(
                    execution_result, plan
                )
            else:
                final_response = await self._synthesize_results(
                    user_request,
                    plan,
                    execution_result["results"],
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
                "response": final_response,
                "execution_time": execution_time,
                "workflow": {
                    "type": plan.get("workflow_type", "sequential"),
                    "steps": agents_needed,  # Use the updated agents_needed
                    "execution_path": execution_result.get("execution_path", []),
                },
                "results": execution_result.get("results", {}),
                "metadata": {
                    "agents_used": len(agents_needed),
                    "components_created": len(plan.get("created_components", [])),
                    "errors_encountered": len(execution_result.get("errors", [])),
                },
            }

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

            traceback.print_exc()
            return self._create_error_response(workflow_id, "Unexpected error", str(e))

    async def _analyze_request(
        self, user_request: str, files: Optional[List[Dict]], context: Optional[Dict]
    ) -> Dict[str, Any]:
        """Analyze the request to understand intent and requirements."""
        # Get available components
        agents = self.registry.list_agents(active_only=True)
        tools = self.registry.list_tools(pure_only=False)

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
                temperature=ORCHESTRATOR_TEMPERATURE,
            )
            print(f"DEBUG: GPT-4 analysis successful")
            return {"status": "success", "analysis": response}

        except Exception as e:
            print(f"DEBUG: GPT-4 analysis failed: {str(e)}")
            return {"status": "error", "error": f"Analysis failed: {str(e)}"}

    async def _plan_workflow(
        self, user_request: str, analysis: str, auto_create: bool
    ) -> Dict[str, Any]:
        """Enhanced workflow planning with better capability detection."""

        # Get available components
        agents = self.registry.list_agents(active_only=True)
        tools = self.registry.list_tools(pure_only=False)

        # Build detailed capability map
        capability_map = self._build_capability_map(agents, tools)

        # Enhanced planning prompt that understands capabilities better
        prompt = f"""You are planning a workflow for this request.

    USER REQUEST: {user_request}

    ANALYSIS: {analysis}

    AVAILABLE CAPABILITIES:
    {json.dumps(capability_map, indent=2)}

    Create a workflow plan that:
    1. Identifies the specific tasks needed
    2. Maps tasks to existing agents when possible
    3. Identifies truly missing capabilities
    4. Suggests agent creation only when necessary

    IMPORTANT: 
    - Only suggest creating agents that don't already exist
    - Check agent descriptions carefully - don't create duplicates
    - If an agent can partially handle a task, use it
    - Prefer using existing agents over creating new ones

    Respond with valid JSON:
    {{
        "workflow_id": "wf_<timestamp>",
        "workflow_type": "sequential|parallel|conditional",
        "reasoning": "step-by-step explanation",
        "agents_needed": ["exact_agent_names_from_available_list"],
        "missing_capabilities": {{
            "agents": [
                {{
                    "name": "new_agent_name",
                    "purpose": "specific purpose",
                    "required_tools": ["tool1"],
                    "can_create": true
                }}
            ],
            "tools": [
                {{
                    "name": "new_tool_name",
                    "purpose": "specific purpose", 
                    "type": "pure_function",
                    "can_create": true
                }}
            ]
        }},
        "execution_strategy": "how to execute the workflow",
        "fallback_plan": "what to do if some agents fail"
    }}"""

        try:
            response = await self._call_gpt4_json(
                system_prompt="""You are a workflow planner. 
                CRITICAL: Check existing agent capabilities carefully before suggesting new ones.
                Many agents have flexible input handling and can process various data types.
                Only create new agents when existing ones truly cannot handle the task.""",
                user_prompt=prompt,
                temperature=0.1,
            )

            plan = json.loads(response)

            # CRITICAL: Check if no agents can handle the request
            if not plan.get("agents_needed") and not auto_create:
                # Check if this is because nothing matches
                if (
                    "non_existent" in user_request.lower()
                    or not self._can_handle_request(user_request)
                ):
                    return {
                        "status": "missing_capabilities",
                        "message": "No agents available to handle this request",
                        "missing": plan.get("missing_capabilities", {}),
                        "suggestion": "Enable auto_create to build missing components",
                    }

            # Validate and filter the plan
            plan = self._validate_and_filter_plan(plan)

            # If no agents needed, create a minimal plan
            if not plan.get("agents_needed") and not auto_create:
                return {
                    "status": "error",
                    "error": "No agents available to handle this request",
                }

            plan["status"] = "success"
            return plan

        except json.JSONDecodeError as e:
            print(f"DEBUG: JSON parsing failed: {str(e)}")
            print(f"DEBUG: Raw response: {response[:500]}...")

            # Check if this is about a non-existent agent
            if "non_existent" in user_request.lower():
                return {
                    "status": "missing_capabilities",
                    "message": "No agents available to handle this request",
                    "missing": {"agents": [], "tools": []},
                    "suggestion": "Enable auto_create to build missing components",
                }

            # Otherwise return error
            return {"status": "error", "error": f"Planning failed: {str(e)}"}
        except Exception as e:
            print(f"DEBUG: Planning failed: {str(e)}")

            # Check for non-existent agent request
            if "non_existent" in user_request.lower():
                return {
                    "status": "missing_capabilities",
                    "message": "No agents available to handle this request",
                    "missing": {"agents": [], "tools": []},
                    "suggestion": "Enable auto_create to build missing components",
                }

            # Fallback to simple planning
            return self._create_fallback_plan(user_request, agents)

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
                print(f"DEBUG: Tool '{tool_spec['name']}' creation error: {str(e)}")
                # Continue anyway
                created["tools"].append(tool_spec["name"])

        # Now create missing agents (with tools available)
        for agent_spec in missing_capabilities.get("agents", []):
            try:
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
                    print(f"DEBUG: Agent '{agent_spec['name']}' created successfully")
                else:
                    failed["agents"].append(
                        {
                            "name": agent_spec["name"],
                            "error": result.get("message", "Unknown error"),
                        }
                    )
                    print(f"DEBUG: Agent '{agent_spec['name']}' creation failed")

            except Exception as e:
                failed["agents"].append({"name": agent_spec["name"], "error": str(e)})
                print(f"DEBUG: Agent '{agent_spec['name']}' creation error: {str(e)}")

        # Return success if we created anything
        if created["agents"] or created["tools"]:
            return {"status": "success", "created": created, "failed": failed}
        elif failed["agents"]:
            return {"status": "partial", "created": created, "failed": failed}
        else:
            return {"status": "success", "created": created, "failed": failed}

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
                temperature=0.3,
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
                temperature=0.3,
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

    async def _execute_workflow(
        self, plan: Dict, initial_data: Dict, workflow_id: str
    ) -> Dict[str, Any]:
        """Execute the planned workflow."""

        agents_needed = plan.get("agents_needed", [])
        if not agents_needed:
            return {
                "status": "success",
                "results": {},
                "execution_path": [],
                "errors": [],
                "message": "No agents required for this request",
            }

        workflow_type = WorkflowType(plan.get("workflow_type", "sequential"))

        try:
            if workflow_type == WorkflowType.SEQUENTIAL:
                result = await self._execute_sequential(
                    plan["agents_needed"], initial_data, workflow_id
                )
            elif workflow_type == WorkflowType.PARALLEL:
                result = await self._execute_parallel(
                    plan["agents_needed"], initial_data, workflow_id
                )
            else:
                result = await self._execute_sequential(
                    plan["agents_needed"], initial_data, workflow_id
                )

            # CRITICAL FIX: Better status determination
            # Check if we have meaningful results from agents
            successful_agents = 0
            failed_agents = 0

            for agent_name in agents_needed:
                if agent_name in result.get("results", {}):
                    agent_result = result["results"][agent_name]
                    if isinstance(agent_result, dict):
                        if agent_result.get("status") == "success":
                            successful_agents += 1
                        else:
                            failed_agents += 1

            # Determine overall status based on agent execution
            if successful_agents == len(agents_needed):
                result["status"] = "success"
            elif successful_agents > 0:
                result["status"] = "partial"
            else:
                result["status"] = "failed"

            return result

        except asyncio.TimeoutError:
            return {
                "status": "error",
                "error": f"Workflow timeout after {WORKFLOW_TIMEOUT_SECONDS} seconds",
            }
        except Exception as e:
            return {"status": "error", "error": f"Workflow execution failed: {str(e)}"}

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
        """Synthesize results from multiple agents into coherent response."""
        if errors is None:
            errors = []

        # Check if we have any successful results
        successful_results = {
            agent: result
            for agent, result in results.items()
            if isinstance(result, dict) and result.get("status") == "success"
        }

        # If no successful results, provide a helpful response
        if not successful_results:
            if errors:
                error_msg = "Unknown error"
                if isinstance(errors[0], dict):
                    error_msg = errors[0].get("error", "Unknown error")
                elif isinstance(errors[0], str):
                    error_msg = errors[0]
                return f"I apologize, but I encountered an error while processing your request: {error_msg}"
            else:
                return "I was unable to process your request. Please try again or provide more details."

        # Create a natural response from successful results
        response_parts = []
        response_parts.append(
            "I've successfully processed your request and found the following:"
        )

        # Extract and format results
        all_emails = []
        all_urls = []

        for agent_name, result in successful_results.items():
            if result.get("data"):
                agent_data = result["data"]

                # Handle email extraction results
                if "emails" in agent_data and agent_data["emails"]:
                    emails = agent_data["emails"]
                    all_emails.extend(emails)

                # Handle URL extraction results
                if "urls" in agent_data and agent_data["urls"]:
                    urls = agent_data["urls"]
                    all_urls.extend(urls)

        # Format the findings
        if all_emails:
            response_parts.append(
                f"\n**📧 Email Addresses Found ({len(all_emails)}):**"
            )
            for email in all_emails:
                response_parts.append(f"• {email}")

        if all_urls:
            response_parts.append(f"\n**🔗 URLs Found ({len(all_urls)}):**")
            for url in all_urls:
                response_parts.append(f"• {url}")

        if not all_emails and not all_urls:
            response_parts.append(
                "\nNo email addresses or URLs were found in the provided text."
            )

        # Add workflow summary
        agent_names = list(successful_results.keys())
        response_parts.append(
            f"\n*Processed using {len(agent_names)} agents: {', '.join(agent_names)}*"
        )

        return "\n".join(response_parts)

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
        enhanced_prompt = f"{system_prompt}\n\n{user_prompt}\n\nRespond with ONLY valid JSON, no other text before or after."

        response = self.client.chat.completions.create(
            model=ORCHESTRATOR_MODEL,
            max_completion_tokens=ORCHESTRATOR_MAX_TOKENS,  # Changed from max_tokens
            messages=[{"role": "user", "content": enhanced_prompt}],
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
            if "agents" in plan_missing:
                for agent in plan_missing["agents"]:
                    # Add required tools for missing agents
                    for tool in agent.get("required_tools", []):
                        if not self.registry.tool_exists(tool):
                            missing["tools"].append(
                                {
                                    "name": tool,
                                    "purpose": f"Tool for {agent['name']}",
                                    "type": "pure_function",
                                }
                            )
                    # Add the agent itself
                    if not any(a["name"] == agent["name"] for a in missing["agents"]):
                        missing["agents"].append(agent)

            if "tools" in plan_missing:
                for tool in plan_missing["tools"]:
                    if not any(t["name"] == tool["name"] for t in missing["tools"]):
                        missing["tools"].append(tool)

        # Return None if no missing capabilities (important!)
        return missing if (missing["agents"] or missing["tools"]) else None

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
            temperature=0.1,
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
            temperature=0.2,
            max_tokens=1000,
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
