"""
Pipeline Orchestrator
Master coordinator for dynamic multi-agent pipeline execution
"""

import os
import sys
import json
import asyncio
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import openai
import networkx as nx

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    OPENAI_API_KEY,
    ORCHESTRATOR_MODEL,
    ORCHESTRATOR_TEMPERATURE,
    ORCHESTRATOR_MAX_TOKENS,
    PIPELINE_ANALYSIS_PROMPT,
    AGENT_COMPATIBILITY_PROMPT,
    PIPELINE_PLANNING_PROMPT,
    DYNAMIC_AGENT_SPEC_PROMPT,
    PIPELINE_RECOVERY_PROMPT,
)
from core.registry import RegistryManager
from core.agent_compatibility import AgentCompatibilityAnalyzer
from core.agent_factory import AgentFactory
from core.tool_factory import ToolFactory


class PipelineOrchestrator:
    """
    Master coordinator for dynamic multi-agent pipeline execution.
    Handles complex request analysis, pipeline planning, and real-time adaptation.
    """

    def __init__(self):
        """Initialize the pipeline orchestrator."""
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        from core.registry_singleton import get_shared_registry

        self.registry = get_shared_registry()  # ← FIX: Use shared instance
        self.compatibility_analyzer = AgentCompatibilityAnalyzer(self.registry)
        self.agent_factory = AgentFactory()
        self.tool_factory = ToolFactory()

    async def analyze_complex_request(
        self, request: str, files: List[Dict] = None
    ) -> Dict[str, Any]:
        """
        Analyze complex request and break it into pipeline steps.

        Args:
            request: User's natural language request
            files: Uploaded files with metadata

        Returns:
            Pipeline analysis with steps and requirements
        """
        print(f"DEBUG: Analyzing complex request: {request[:100]}...")

        # Get available components
        agents = self.registry.list_agents(active_only=True)
        tools = self.registry.list_tools()

        # Format components for prompt
        agents_desc = self._format_components_list(agents, "agents")
        tools_desc = self._format_components_list(tools, "tools")

        # Build analysis prompt
        prompt = PIPELINE_ANALYSIS_PROMPT.format(
            request=request,
            files=json.dumps(files) if files else "None",
            available_agents=agents_desc,
            available_tools=tools_desc,
        )

        try:
            response = await self._call_gpt4_json(
                system_prompt="You are a pipeline analyzer. Analyze requests and break them into logical steps.",
                user_prompt=prompt,
            )

            analysis = json.loads(response)
            analysis["status"] = "success"

            print(
                f"DEBUG: Pipeline analysis found {len(analysis.get('steps', []))} steps"
            )
            return analysis

        except Exception as e:
            print(f"DEBUG: Pipeline analysis failed: {str(e)}")
            return {
                "status": "error",
                "error": f"Pipeline analysis failed: {str(e)}",
                "steps": [],
            }

    async def plan_pipeline(
        self, analysis: Dict, auto_create: bool = True
    ) -> Dict[str, Any]:
        """
        Plan optimal pipeline execution with agent compatibility analysis.

        Args:
            analysis: Pipeline analysis from analyze_complex_request
            auto_create: Whether to auto-create missing agents

        Returns:
            Complete pipeline execution plan
        """
        print(f"DEBUG: Planning pipeline with {len(analysis.get('steps', []))} steps")

        steps = analysis.get("steps", [])
        if not steps:
            return {"status": "error", "error": "No pipeline steps to plan"}

        # Analyze agent compatibility for each step
        pipeline_plan = {
            "pipeline_id": f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "total_steps": len(steps),
            "execution_strategy": "sequential",  # Default, can be enhanced
            "steps": [],
            "creation_needed": [],
            "data_flow": {},
            "estimated_time": 0,
        }

        for i, step in enumerate(steps):
            previous_output = None
            if i > 0:
                # Get output from previous step if available
                prev_step_name = pipeline_plan["steps"][i - 1].get("name")
                # This would need to be enhanced to track actual data flow

            step_plan = await self._plan_step(step, i, auto_create, previous_output)
            pipeline_plan["steps"].append(step_plan)

            if step_plan.get("needs_creation"):
                pipeline_plan["creation_needed"].extend(step_plan["creation_specs"])

            # Estimate execution time
            pipeline_plan["estimated_time"] += step_plan.get("estimated_time", 5)

        # Plan data flow between steps
        pipeline_plan["data_flow"] = self._plan_data_flow(pipeline_plan["steps"])

        # Determine execution strategy
        pipeline_plan["execution_strategy"] = self._determine_execution_strategy(
            pipeline_plan["steps"]
        )

        print(
            f"DEBUG: Pipeline planned - {len(pipeline_plan['creation_needed'])} components need creation"
        )
        return pipeline_plan

    def _predict_step_output(self, previous_step: Dict, current_step: Dict) -> Any:
        """Predict output from previous step for planning purposes."""

        # Analyze what the previous step should produce
        prev_name = previous_step.get("name", "").lower()
        prev_desc = previous_step.get("description", "").lower()

        current_name = current_step.get("name", "").lower()
        current_desc = current_step.get("description", "").lower()

        # Pattern-based output prediction
        if "extract" in prev_desc:
            if "email" in prev_desc:
                return ["john@example.com", "mary@company.org"]  # Sample emails
            elif "url" in prev_desc:
                return [
                    "https://example.com",
                    "https://docs.example.com",
                ]  # Sample URLs
            else:
                return {"extracted_data": "sample extracted content"}

        elif "read" in prev_desc or "process" in prev_desc:
            if "text" in prev_desc:
                return "Sample processed text content"
            else:
                return {"processed_data": "sample processed content"}

        elif "calculate" in prev_desc or "analyze" in prev_desc:
            return {"result": 42, "analysis": "sample analysis"}

        # Default prediction based on current step needs
        if "text" in current_desc:
            return "sample text for processing"
        elif "list" in current_desc or "extract" in current_desc:
            return ["item1", "item2", "item3"]
        else:
            return {"data": "sample data", "type": "unknown"}

    async def _generate_agent_spec_for_step(
        self, step: Dict, step_index: int
    ) -> Dict[str, Any]:
        """Generate detailed agent specification for a pipeline step."""

        # Use GPT-4 to design pipeline-aware agent
        prompt = DYNAMIC_AGENT_SPEC_PROMPT.format(
            step_description=step.get("description", ""),
            step_index=step_index,
            input_requirements=json.dumps(step.get("input_requirements", {})),
            output_requirements=json.dumps(step.get("output_requirements", {})),
            available_tools=json.dumps([t["name"] for t in self.registry.list_tools()]),
        )

        try:
            response = await self._call_gpt4_json(
                system_prompt="Design pipeline-aware agent specifications.",
                user_prompt=prompt,
            )

            spec = json.loads(response)

            # Add pipeline context
            spec["pipeline_context"] = {
                "step_index": step_index,
                "input_format": step.get("input_requirements", {}),
                "output_format": step.get("output_requirements", {}),
                "created_for_pipeline": True,
            }

            return spec

        except Exception as e:
            print(f"DEBUG: Agent spec generation failed: {str(e)}")
            # Fallback specification
            return {
                "name": f"pipeline_agent_step_{step_index}",
                "description": step.get(
                    "description", f"Agent for pipeline step {step_index}"
                ),
                "required_tools": [],
                "pipeline_context": {
                    "step_index": step_index,
                    "created_for_pipeline": True,
                },
            }

    async def _generate_enhanced_agent_spec(
        self, step: Dict, step_index: int, previous_step_output: Any = None
    ) -> Dict[str, Any]:
        """Generate enhanced agent specification with data type awareness."""

        input_type = (
            type(previous_step_output).__name__
            if previous_step_output is not None
            else "string"
        )
        input_sample = (
            str(previous_step_output)[:200] if previous_step_output else "text input"
        )

        # Enhanced prompt that DISCOURAGES unnecessary tool creation
        prompt = f"""
    Design a pipeline-aware agent for this step. IMPORTANT: Agents should be self-sufficient and only request tools for complex external operations.

    STEP REQUIREMENTS:
    - Name: {step.get('name', f'step_{step_index}')}  
    - Description: {step.get('description', '')}
    - Step Index: {step_index}
    - Expected Input Type: {input_type}
    - Input Sample: {input_sample}

    TOOL CREATION GUIDELINES:
    - DO NOT create tools for simple logic (prime checking, basic math, string operations)
    - DO NOT create tools for data parsing or filtering
    - ONLY create tools for:
    * External API calls
    * Complex file I/O operations  
    * Specialized libraries (PDF parsing, Excel manipulation)
    * Database connections

    For this step, determine if ANY tools are actually needed. Most likely, the answer is NO.

    Simple operations like:
    - Checking if a number is prime → Agent code
    - Calculating averages → Agent code  
    - Parsing strings → Agent code
    - Filtering lists → Agent code

    RESPOND WITH JSON:
    {{
        "name": "descriptive_agent_name",
        "description": "what this agent does",
        "required_tools": [],  // Usually empty! Only add if TRULY needed
        "new_tools_needed": [],  // Usually empty!
        "input_handling": {{
            "expected_type": "{input_type}",
            "error_handling": "how to handle wrong types",
            "data_extraction": "how to get data from pipeline state"
        }},
        "output_format": {{
            "type": "expected_output_type",
            "structure": "description of output structure"
        }},
        "agent_logic_description": "Describe what the agent will do internally WITHOUT external tools",
        "pipeline_context": {{
            "step_index": {step_index},
            "works_with_state": true,
            "data_flow_aware": true
        }}
    }}
    """

        try:
            response = await self._call_gpt4_json(
                system_prompt="Design intelligent pipeline agents that are self-sufficient.",
                user_prompt=prompt,
            )

            spec = json.loads(response)

            # Ensure required fields exist
            if "name" not in spec:
                spec["name"] = f"pipeline_agent_step_{step_index}"

            if "description" not in spec:
                spec["description"] = (
                    f"Agent for step {step_index} handling {input_type} input"
                )

            # Default to NO tools unless absolutely necessary
            if "required_tools" not in spec:
                spec["required_tools"] = []

            return spec

        except Exception as e:
            print(f"DEBUG: Enhanced agent spec generation failed: {str(e)}")
            # Fallback with NO tools
            return {
                "name": f"pipeline_agent_step_{step_index}",
                "description": f"Agent for step {step_index}",
                "required_tools": [],  # No tools by default
                "input_handling": {
                    "expected_type": input_type,
                    "error_handling": "flexible input processing",
                    "data_extraction": "extract from current_data in pipeline state",
                },
                "pipeline_context": {
                    "step_index": step_index,
                    "works_with_state": True,
                    "data_flow_aware": True,
                },
            }

    def _plan_data_flow(self, steps: List[Dict]) -> Dict[str, Any]:
        """Plan data flow between pipeline steps."""
        data_flow = {"flow_graph": {}, "transformations": [], "validation_points": []}

        for i, step in enumerate(steps):
            step_name = step["name"]

            # Input sources
            if i == 0:
                data_flow["flow_graph"][step_name] = {
                    "inputs": ["user_input"],
                    "outputs": [],
                }
            else:
                prev_step = steps[i - 1]["name"]
                data_flow["flow_graph"][step_name] = {
                    "inputs": [prev_step],
                    "outputs": [],
                }

            # Output targets
            if i < len(steps) - 1:
                next_step = steps[i + 1]["name"]
                data_flow["flow_graph"][step_name]["outputs"].append(next_step)
            else:
                data_flow["flow_graph"][step_name]["outputs"].append("final_output")

        return data_flow

    def _determine_execution_strategy(self, steps: List[Dict]) -> str:
        """Determine optimal execution strategy for the pipeline."""
        # For now, default to sequential
        # Can be enhanced to detect parallel opportunities
        return "sequential"

    async def execute_pipeline_with_adaptation(
        self, pipeline_plan: Dict, user_request: str, files: List[Dict] = None
    ) -> Dict[str, Any]:
        """
        Execute pipeline with real-time adaptation and recovery.

        Args:
            pipeline_plan: Complete pipeline execution plan
            user_request: Original user request
            files: Uploaded files

        Returns:
            Pipeline execution results
        """
        print(f"DEBUG: Executing pipeline with {pipeline_plan['total_steps']} steps")

        # Create missing agents/tools first
        if pipeline_plan.get("creation_needed"):
            creation_result = await self._create_pipeline_components(
                pipeline_plan["creation_needed"]
            )
            if creation_result["status"] != "success":
                return {
                    "status": "error",
                    "error": "Failed to create required components",
                }

        # VERIFY ALL AGENTS EXIST BEFORE EXECUTION
        required_agents = [
            step["agent_assigned"]
            for step in pipeline_plan["steps"]
            if step.get("agent_assigned")
        ]
        if not self._verify_agents_exist(required_agents):
            return {
                "status": "error",
                "error": "Required agents not found in registry after creation",
            }

        # Execute pipeline steps
        execution_result = {
            "status": "in_progress",
            "pipeline_id": pipeline_plan["pipeline_id"],
            "steps_completed": 0,
            "results": {},
            "errors": [],
            "adaptations": [],
        }

        current_data = {"user_request": user_request, "files": files}

        for i, step_plan in enumerate(pipeline_plan["steps"]):
            print(f"DEBUG: Executing step {i}: {step_plan['name']}")

            try:
                step_result = await self._execute_step_with_adaptation(
                    step_plan, current_data, execution_result
                )

                if step_result["status"] == "success":
                    execution_result["results"][step_plan["name"]] = step_result
                    execution_result["steps_completed"] += 1
                    current_data = step_result.get("data", current_data)
                else:
                    # Handle step failure with adaptation
                    adaptation_result = await self._handle_step_failure(
                        step_plan, step_result, pipeline_plan
                    )

                    if adaptation_result["status"] == "recovered":
                        execution_result["adaptations"].append(adaptation_result)
                        step_result = adaptation_result["recovery_result"]
                        execution_result["results"][step_plan["name"]] = step_result
                        execution_result["steps_completed"] += 1
                        current_data = step_result.get("data", current_data)
                    else:
                        execution_result["errors"].append(
                            {
                                "step": step_plan["name"],
                                "error": step_result.get("error", "Unknown error"),
                                "recovery_failed": True,
                            }
                        )
                        break

            except Exception as e:
                execution_result["errors"].append(
                    {"step": step_plan["name"], "error": str(e), "exception": True}
                )
                break

        # Determine final status
        if execution_result["steps_completed"] == pipeline_plan["total_steps"]:
            execution_result["status"] = "success"
        elif execution_result["steps_completed"] > 0:
            execution_result["status"] = "partial"
        else:
            execution_result["status"] = "failed"

        print(
            f"DEBUG: Pipeline execution completed - Status: {execution_result['status']}"
        )
        return execution_result

    async def _create_pipeline_components(
        self, creation_specs: List[Dict]
    ) -> Dict[str, Any]:
        """Create all required pipeline components."""
        print(f"DEBUG: Creating {len(creation_specs)} pipeline components")

        created = {"agents": [], "tools": []}
        failed = {"agents": [], "tools": []}

        for spec in creation_specs:
            try:
                if spec.get("type") == "agent" or "name" in spec:
                    # Create agent
                    result = self.agent_factory.create_pipeline_agent(spec)
                    print(f"DEBUG: Agent creation result: {result}")

                    if result["status"] == "success":
                        created["agents"].append(spec["name"])
                        print(f"DEBUG: Agent {spec['name']} created successfully")

                    else:
                        print(
                            f"DEBUG: Agent {spec['name']} creation failed: {result.get('message', 'unknown error')}"
                        )
                        failed["agents"].append(
                            {"name": spec["name"], "error": result.get("message")}
                        )

                elif spec.get("type") == "tool":
                    # Create tool
                    result = self.tool_factory.create_tool(
                        tool_name=spec["name"],
                        description=spec.get("description", ""),
                    )
                    if result["status"] == "success":
                        created["tools"].append(spec["name"])
                    else:
                        failed["tools"].append(
                            {"name": spec["name"], "error": result.get("message")}
                        )

            except Exception as e:
                print(f"DEBUG: Exception in component creation: {str(e)}")
                import traceback

                print(f"DEBUG: Traceback: {traceback.format_exc()}")
                failed["agents"].append(
                    {"name": spec.get("name", "unknown"), "error": str(e)}
                )

        if created["agents"] or created["tools"]:
            return {"status": "success", "created": created, "failed": failed}
        else:
            return {"status": "error", "created": created, "failed": failed}

    async def _execute_step_with_adaptation(
        self, step_plan: Dict, current_data: Any, execution_context: Dict
    ) -> Dict[str, Any]:
        """Execute a single pipeline step with adaptation capability."""
        agent_name = step_plan["agent_assigned"]

        if not agent_name:
            return {"status": "error", "error": "No agent assigned to step"}

        # Import and execute the agent
        try:
            from backup_removed_components.workflow_engine import WorkflowEngine
            from core.registry_singleton import get_shared_registry, force_global_reload

            # COMPREHENSIVE REGISTRY SYNCHRONIZATION
            force_global_reload()
            fresh_registry = get_shared_registry()

            # Verify agent exists before proceeding
            if not fresh_registry.agent_exists(agent_name):
                print(f"DEBUG: CRITICAL - Agent '{agent_name}' not found in registry")
                print(
                    f"DEBUG: Available agents: {list(fresh_registry.agents.get('agents', {}).keys())}"
                )
                return {
                    "status": "error",
                    "error": f"Agent '{agent_name}' not found in registry",
                }

            workflow_engine = WorkflowEngine(fresh_registry)
            print(
                f"DEBUG: Successfully verified agent '{agent_name}' exists in registry"
            )

            # Create minimal workflow state for single agent execution
            workflow_state = {
                "request": f"Execute step: {step_plan['description']}",
                "current_data": current_data,
                "execution_path": [],
                "results": {},
                "errors": [],
            }

            # Execute the agent
            result = await workflow_engine.execute_agent(agent_name, workflow_state)

            return result

        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def _handle_step_failure(
        self, step_plan: Dict, step_result: Dict, pipeline_plan: Dict
    ) -> Dict[str, Any]:
        """Handle step failure with real-time adaptation."""
        print(f"DEBUG: Handling failure for step: {step_plan['name']}")

        # Analyze failure reason
        failure_analysis = await self._analyze_step_failure(step_plan, step_result)

        # Generate recovery strategy
        recovery_prompt = PIPELINE_RECOVERY_PROMPT.format(
            step_name=step_plan["name"],
            step_description=step_plan["description"],
            failure_reason=step_result.get("error", "Unknown error"),
            failure_analysis=json.dumps(failure_analysis),
            available_agents=json.dumps(
                [a["name"] for a in self.registry.list_agents()]
            ),
        )

        try:
            response = await self._call_gpt4_json(
                system_prompt="Generate recovery strategies for failed pipeline steps.",
                user_prompt=recovery_prompt,
            )

            recovery_strategy = json.loads(response)

            # Execute recovery strategy
            if recovery_strategy.get("action") == "create_replacement_agent":
                # Create new agent to replace failed one
                replacement_spec = recovery_strategy.get("replacement_spec", {})
                creation_result = self.agent_factory.create_pipeline_agent(
                    replacement_spec
                )

                if creation_result["status"] == "success":
                    # Retry step with new agent
                    step_plan["agent_assigned"] = replacement_spec["name"]
                    retry_result = await self._execute_step_with_adaptation(
                        step_plan, {}, {}
                    )

                    return {
                        "status": "recovered",
                        "recovery_action": "created_replacement_agent",
                        "new_agent": replacement_spec["name"],
                        "recovery_result": retry_result,
                    }

            return {
                "status": "recovery_failed",
                "reason": "No viable recovery strategy",
            }

        except Exception as e:
            return {"status": "recovery_failed", "reason": str(e)}

    async def _analyze_step_failure(
        self, step_plan: Dict, step_result: Dict
    ) -> Dict[str, Any]:
        """Analyze why a pipeline step failed."""
        return {
            "step_name": step_plan["name"],
            "agent_used": step_plan["agent_assigned"],
            "error_message": step_result.get("error", "Unknown error"),
            "error_type": "execution_error",  # Can be enhanced
            "suggested_fixes": ["create_replacement_agent", "modify_input_format"],
        }

    def _format_components_list(
        self, components: List[Dict], component_type: str
    ) -> str:
        """Format list of components for prompts."""
        if not components:
            return f"No {component_type} available"

        formatted = []
        for comp in components:
            name = comp.get("name", "unknown")
            desc = comp.get("description", "No description")
            formatted.append(f"- {name}: {desc}")

        return "\n".join(formatted)

    async def _call_gpt4_json(
        self, system_prompt: str, user_prompt: str, temperature: float = 0.1
    ) -> str:
        """Call GPT-4 for JSON responses."""
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

    async def _analyze_request_complexity(
        self, user_request: str, files: List[Dict] = None
    ) -> str:
        """Analyze request complexity for pipeline routing."""
        request_lower = user_request.lower()

        # Pipeline indicators
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

        # Decision logic
        if complex_count > 0 or pipeline_count > 2 or step_count > 1 or multiple_files:
            return "complex"
        elif pipeline_count > 0 or len(request_lower.split()) > 20:
            return "pipeline"
        else:
            return "simple"

    async def _plan_step(
        self,
        step: Dict,
        step_index: int,
        auto_create: bool,
        previous_step_output: Any = None,
    ) -> Dict[str, Any]:
        """Plan execution for a single pipeline step."""
        step_plan = {
            "step_index": step_index,
            "name": step.get("name", f"step_{step_index}"),
            "description": step.get("description", ""),
            "input_requirements": step.get("input_requirements", {}),
            "output_requirements": step.get("output_requirements", {}),
            "agent_assigned": None,
            "needs_creation": False,
            "creation_specs": [],
            "estimated_time": 5,
        }

        # Find compatible agents
        compatible_agents = await self.compatibility_analyzer.find_compatible_agents(
            step
        )

        if compatible_agents:
            best_agent = compatible_agents[0]
            compatibility_score = best_agent.get("compatibility_score", 0.0)

            if compatibility_score >= 0.6:
                step_plan["agent_assigned"] = best_agent["name"]
                step_plan["estimated_time"] = best_agent.get("avg_execution_time", 5)
            elif auto_create:
                # Create new agent for better compatibility
                step_plan["needs_creation"] = True
                agent_spec = await self._generate_enhanced_agent_spec(
                    step, step_index, previous_step_output
                )
                # FIX: Convert agent name to lowercase
                agent_spec["name"] = agent_spec["name"].lower()
                step_plan["creation_specs"].append(agent_spec)
                step_plan["agent_assigned"] = agent_spec["name"]
            else:
                # Use best available even if not perfect
                step_plan["agent_assigned"] = best_agent["name"]

        elif auto_create:
            # No compatible agents - create new one
            step_plan["needs_creation"] = True
            agent_spec = await self._generate_enhanced_agent_spec(
                step, step_index, previous_step_output
            )
            # FIX: Convert agent name to lowercase
            agent_spec["name"] = agent_spec["name"].lower()
            step_plan["creation_specs"].append(agent_spec)
            step_plan["agent_assigned"] = agent_spec["name"]

        return step_plan

    def _verify_agents_exist(self, agent_names: List[str]) -> bool:
        """Verify all required agents exist in registry"""
        from core.registry_singleton import get_shared_registry, force_global_reload

        force_global_reload()
        registry = get_shared_registry()

        available_agents = list(registry.agents.get("agents", {}).keys())
        print(f"DEBUG: Available agents in registry: {available_agents}")

        missing_agents = []
        for agent_name in agent_names:
            if not registry.agent_exists(agent_name):
                missing_agents.append(agent_name)

        if missing_agents:
            print(f"DEBUG: Missing agents: {missing_agents}")
            return False

        print(f"DEBUG: All required agents found: {agent_names}")
        return True
