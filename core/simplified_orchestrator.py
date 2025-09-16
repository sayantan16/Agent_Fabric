"""
Simplified AI-Powered Orchestrator
Uses GPT-4 for planning and Claude for agent execution
"""

import os
import json
import asyncio
import importlib
from typing import Dict, List, Optional, Any
from datetime import datetime
import openai
from anthropic import Anthropic

from config import (
    OPENAI_API_KEY,
    ANTHROPIC_API_KEY,
    ORCHESTRATOR_MODEL,
    CLAUDE_MODEL,
    ORCHESTRATOR_MAX_TOKENS,
    CLAUDE_MAX_TOKENS,
)
from core.registry import RegistryManager
from core.registry_singleton import get_shared_registry
from core.file_content_reader import FileContentReader
from core.agent_factory import AgentFactory
from core.tool_factory import ToolFactory

from core.workflow_engine import (
    EnhancedMultiAgentWorkflowEngine as MultiAgentWorkflowEngine,
)
from core.capability_analyzer import CapabilityAnalyzer
from core.ai_workflow_planner import AIWorkflowPlanner
from core.specialized_agents import (
    PDFAnalyzerAgent,
    ChartGeneratorAgent,
    TextProcessorAgent,
)


class SimplifiedOrchestrator:
    """
    Simplified orchestrator that uses AI for all major decisions.
    Core principle: Let AI handle complexity, not code.
    """

    def __init__(self):
        # Initialize registry
        self.registry = RegistryManager()
        self.agent_factory = AgentFactory()
        self.tool_factory = ToolFactory()
        self.file_reader = FileContentReader()

        # Use enhanced workflow engine
        self.workflow_engine = MultiAgentWorkflowEngine()

        self.capability_analyzer = CapabilityAnalyzer()

        # Initialize OpenAI client
        self.openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

        # Initialize Claude client
        self.claude_client = Anthropic(api_key=ANTHROPIC_API_KEY)

        # ADD this new AI planner:
        self.ai_workflow_planner = AIWorkflowPlanner()

        print(f"DEBUG: ANTHROPIC_API_KEY present: {bool(ANTHROPIC_API_KEY)}")
        print(
            f"DEBUG: ANTHROPIC_API_KEY length: {len(ANTHROPIC_API_KEY) if ANTHROPIC_API_KEY else 0}"
        )

    def _detect_scenario(self, request: str, files: List[Dict] = None) -> Optional[str]:
        """Detect if request matches a known scenario pattern"""

        from config import HACKATHON_SCENARIOS

        request_lower = request.lower()

        # Check each scenario
        for scenario_key, scenario_config in HACKATHON_SCENARIOS.items():
            # Check keywords
            keyword_match = any(
                keyword in request_lower for keyword in scenario_config["keywords"]
            )

            # Check file types if files provided
            file_match = True
            if files and scenario_config["file_indicators"]:
                file_match = any(
                    any(
                        indicator in str(f.get("name", "")).lower()
                        for indicator in scenario_config["file_indicators"]
                    )
                    for f in files
                )

            if keyword_match and file_match:
                print(f"🎯 Scenario detected: {scenario_config['name']}")
                return scenario_key

        return None

    async def process_request(
        self,
        user_request: str,
        files: Optional[List[Dict]] = None,
        auto_create: bool = True,
    ) -> Dict[str, Any]:
        """
        ENHANCED process_request with TRUE AI-driven orchestration.

        This method REPLACES the existing process_request in simplified_orchestrator.py
        """
        workflow_id = f"ai_wf_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        start_time = datetime.now()

        try:
            print(f"🚀 Starting AI-driven workflow for: {user_request[:100]}...")

            # Step 1: Read actual file contents (existing code)
            enriched_files = []
            if files:
                enriched_files = self.file_reader.process_all_files(files)
                print(f"📁 Processed {len(enriched_files)} files")

            # Step 2: Get available capabilities for AI planning
            available_agents = list(self.registry.agents.get("agents", {}).keys())
            available_tools = list(self.registry.tools.get("tools", {}).keys())

            print(f"🤖 Available agents: {available_agents}")
            print(f"🔧 Available tools: {len(available_tools)} tools")

            # Step 2.5: Check for scenario match
            scenario_key = self._detect_scenario(user_request, enriched_files)

            if scenario_key == "sales_analysis":
                # Use scenario-aware workflow planning for sales
                print(f"📊 Executing Sales Analysis Pipeline")

                from config import (
                    HACKATHON_SCENARIOS,
                    SCENARIO_AWARE_ORCHESTRATION_PROMPT,
                )

                scenario = HACKATHON_SCENARIOS[scenario_key]

                # Determine which agents need creation
                missing_agents = [
                    {
                        "name": agent,
                        "purpose": f"Sales-specialized {agent.replace('_', ' ')}",
                    }
                    for agent in scenario["agents_to_create"]
                    if agent not in available_agents
                ]

                print(f"📋 Available agents: {available_agents}")
                print(f"🔧 Will create: {[a['name'] for a in missing_agents]}")

                # Create missing agents for sales scenario
                if missing_agents:
                    print(
                        f"🎯 Creating {len(missing_agents)} sales-specialized agents..."
                    )

                    for agent_spec in missing_agents:
                        agent_name = agent_spec["name"]
                        purpose = agent_spec["purpose"]

                        print(f"   Creating: {agent_name}")

                        creation_result = (
                            await self.agent_factory.create_scenario_agent(
                                agent_name, scenario_key, purpose
                            )
                        )

                        if creation_result["status"] == "success":
                            print(f"   ✅ Created: {agent_name}")
                            # Force registry reload
                            from core.registry_singleton import force_global_reload

                            force_global_reload()

                            # Update available agents list
                            available_agents.append(agent_name)
                        else:
                            print(
                                f"   ❌ Failed: {agent_name} - {creation_result.get('error')}"
                            )

                # Build simple workflow plan for sales
                ai_workflow_plan = {
                    "workflow_type": "scenario_based",
                    "scenario": scenario_key,
                    "scenario_name": scenario["name"],
                    "agents": scenario["workflow_pattern"]["agent_sequence"],
                    "execution_strategy": "sequential",
                    "confidence": 0.95,
                    "agents_created": len(missing_agents),
                    "complexity": "medium",
                }

                # Execute sales workflow
                print(f"⚡ Executing sales workflow: {ai_workflow_plan['agents']}")

                workflow_result = (
                    await self.workflow_engine.execute_ai_planned_workflow(
                        ai_workflow_plan, user_request, enriched_files
                    )
                )

                # Use AI-generated response instead of template
                final_response = workflow_result.get(
                    "ai_response", "Analysis completed successfully"
                )

                return {
                    "status": "success",
                    "workflow_id": workflow_id,
                    "response": final_response,  # AI-generated natural language response
                    "execution_time": workflow_result.get("execution_time", 0),
                    "workflow": ai_workflow_plan,
                    "results": workflow_result.get("results", {}),
                    "metadata": {
                        "workflow_type": "sales_analysis",
                        "scenario": scenario_key,
                        "dynamic_agents_created": len(missing_agents),
                        "innovation_demonstrated": len(missing_agents) > 0,
                        "ai_response_generated": True,
                    },
                }

            elif scenario_key == "compliance_monitoring":
                # Use scenario-aware workflow planning for compliance
                print(f"🏛️ Executing Compliance Monitoring Pipeline")

                from config import (
                    HACKATHON_SCENARIOS,
                    SCENARIO_AWARE_ORCHESTRATION_PROMPT,
                )

                scenario = HACKATHON_SCENARIOS[scenario_key]

                # Determine which agents need creation (all of them for compliance)
                missing_agents = [
                    {
                        "name": agent,
                        "purpose": f"Compliance-specialized {agent.replace('_', ' ')}",
                    }
                    for agent in scenario["agents_to_create"]
                    if agent not in available_agents
                ]

                print(f"📋 Available agents: {available_agents}")
                print(f"🔧 Will create: {[a['name'] for a in missing_agents]}")

                # Create missing agents for compliance scenario
                if missing_agents:
                    print(
                        f"🎯 Creating {len(missing_agents)} compliance-specialized agents..."
                    )

                    for agent_spec in missing_agents:
                        agent_name = agent_spec["name"]
                        purpose = agent_spec["purpose"]

                        print(f"   Creating: {agent_name}")

                        creation_result = (
                            await self.agent_factory.create_scenario_agent(
                                agent_name, scenario_key, purpose
                            )
                        )

                        if creation_result["status"] == "success":
                            print(f"   ✅ Created: {agent_name}")
                            # Force registry reload
                            from core.registry_singleton import force_global_reload

                            force_global_reload()

                            # Update available agents list
                            available_agents.append(agent_name)
                        else:
                            print(
                                f"   ❌ Failed: {agent_name} - {creation_result.get('error')}"
                            )

                # Build workflow plan for compliance
                ai_workflow_plan = {
                    "workflow_type": "scenario_based",
                    "scenario": scenario_key,
                    "scenario_name": scenario["name"],
                    "agents": scenario["workflow_pattern"]["agent_sequence"],
                    "execution_strategy": "sequential",
                    "confidence": 0.95,
                    "agents_created": len(missing_agents),
                    "complexity": "high",
                }

                # Execute compliance workflow
                print(f"⚡ Executing compliance workflow: {ai_workflow_plan['agents']}")

                workflow_result = (
                    await self.workflow_engine.execute_ai_planned_workflow(
                        ai_workflow_plan, user_request, enriched_files
                    )
                )

                # Use AI-generated response instead of template
                final_response = workflow_result.get(
                    "ai_response", "Compliance analysis completed successfully"
                )

                return {
                    "status": "success",
                    "workflow_id": workflow_id,
                    "response": final_response,  # AI-generated compliance response
                    "execution_time": workflow_result.get("execution_time", 0),
                    "workflow": ai_workflow_plan,
                    "results": workflow_result.get("results", {}),
                    "metadata": {
                        "workflow_type": "compliance_monitoring",
                        "scenario": scenario_key,
                        "dynamic_agents_created": len(missing_agents),
                        "innovation_demonstrated": len(missing_agents) > 0,
                        "ai_response_generated": True,
                    },
                }

            else:
                # Continue with existing generic AI workflow planning
                print("🧠 Running generic AI workflow analysis...")
                ai_workflow_plan = (
                    await self.ai_workflow_planner.plan_intelligent_workflow(
                        request=user_request,
                        files=enriched_files,
                        available_agents=available_agents,
                        available_tools=available_tools,
                    )
                )

            # Log AI planning results
            planned_agents = ai_workflow_plan.get("agents", [])
            confidence = ai_workflow_plan.get("confidence", 0.0)
            complexity = ai_workflow_plan.get("complexity", "unknown")

            print(
                f"🎯 AI Plan: {len(planned_agents)} agents, {confidence:.0%} confidence, {complexity} complexity"
            )
            print(f"📋 Agent sequence: {planned_agents}")
            print(
                f"💡 Rationale: {ai_workflow_plan.get('rationale', 'No rationale provided')}"
            )

            # Step 4: Check for missing capabilities and create if needed
            missing_capabilities = ai_workflow_plan.get("missing_capabilities", [])
            if missing_capabilities and auto_create:
                print(f"🔍 Found {len(missing_capabilities)} missing capabilities")

                # Enhanced capability analysis with AI plan context
                compatibility_analysis = (
                    await self.capability_analyzer.analyze_agent_compatibility(
                        user_request, {"agents": planned_agents}, enriched_files
                    )
                )

                overall_confidence = compatibility_analysis["compatibility_analysis"][
                    "overall_confidence"
                ]

                if overall_confidence < 0.7:
                    print(
                        f"⚠️  Low compatibility confidence ({overall_confidence:.2f}), attempting agent creation..."
                    )

                    creation_result = await self._create_required_agents(
                        compatibility_analysis
                    )

                    if creation_result["status"] == "success":
                        print(
                            f"✅ Created {len(creation_result['agents_created'])} new agents"
                        )

                        # Refresh registry and re-plan with new agents
                        from core.registry_singleton import force_global_reload

                        force_global_reload()

                        # Update available agents list
                        available_agents = list(
                            self.registry.agents.get("agents", {}).keys()
                        )

                        # Re-plan workflow with new capabilities
                        print("🔄 Re-planning workflow with new agents...")
                        ai_workflow_plan = (
                            await self.ai_workflow_planner.plan_intelligent_workflow(
                                request=user_request,
                                files=enriched_files,
                                available_agents=available_agents,
                                available_tools=available_tools,
                            )
                        )

                        print(f"🆕 Updated plan: {ai_workflow_plan.get('agents', [])}")

            # Step 5: Execute AI-planned workflow
            planned_agents = ai_workflow_plan.get("agents", [])

            if len(planned_agents) == 0:
                # Fallback to simple processing
                print("⚠️  No agents planned, falling back to simple processing")
                return await self._process_simple_request(
                    user_request, enriched_files, workflow_id, start_time
                )

            elif len(planned_agents) == 1:
                # Single agent execution with AI context
                print(f"🎯 Single agent AI-guided execution: {planned_agents[0]}")

                result = await self._execute_ai_guided_single_agent(
                    planned_agents[0], user_request, enriched_files, ai_workflow_plan
                )

                return {
                    "status": "success",
                    "workflow_id": workflow_id,
                    "response": result.get("response", ""),
                    "execution_time": (datetime.now() - start_time).total_seconds(),
                    "workflow": ai_workflow_plan,
                    "results": {planned_agents[0]: result},
                    "metadata": {
                        "workflow_type": "single_agent_ai_guided",
                        "agent_used": planned_agents[0],
                        "ai_confidence": confidence,
                        "planning_intelligence": "gpt4_driven",
                    },
                }

            else:
                # Multi-agent AI-driven workflow execution
                print(f"🎭 Multi-agent AI workflow: {len(planned_agents)} agents")

                workflow_result = (
                    await self.workflow_engine.execute_ai_planned_workflow(
                        ai_workflow_plan, user_request, enriched_files
                    )
                )

                # AI-driven response synthesis
                response = await self._synthesize_ai_workflow_response(
                    user_request, workflow_result, ai_workflow_plan
                )

                return {
                    "status": "success",
                    "workflow_id": workflow_id,
                    "response": response,
                    "execution_time": (datetime.now() - start_time).total_seconds(),
                    "workflow": ai_workflow_plan,
                    "results": workflow_result.get("results", {}),
                    "workflow_summary": workflow_result.get("summary", ""),
                    "data_flow": workflow_result.get("data_flow", []),
                    "context_flow": workflow_result.get("context_flow", []),
                    "metadata": {
                        "workflow_type": "multi_agent_ai_driven",
                        "agents_used": len(planned_agents),
                        "execution_strategy": ai_workflow_plan.get(
                            "execution_strategy", "sequential"
                        ),
                        "ai_confidence": confidence,
                        "complexity": complexity,
                        "planning_intelligence": "gpt4_strategic",
                    },
                }

        except Exception as e:
            print(f"❌ AI workflow execution failed: {str(e)}")
            import traceback

            traceback.print_exc()

            return {
                "status": "error",
                "workflow_id": workflow_id,
                "error": str(e),
                "response": f"AI workflow failed: {str(e)}",
                "workflow": {},
                "metadata": {"error_type": "ai_workflow_failure"},
            }

    async def _execute_ai_guided_single_agent(
        self, agent_name: str, request: str, files: List[Dict], ai_plan: Dict
    ) -> Dict:
        """Execute single agent with AI-driven context."""

        # Get agent instructions from AI plan
        agent_instructions = ai_plan.get("agent_instructions", {}).get(agent_name, {})

        # Build enhanced context
        context = {
            "ai_guided": True,
            "primary_task": agent_instructions.get("primary_task", "Process request"),
            "processing_focus": agent_instructions.get("processing_focus", ""),
            "output_requirements": agent_instructions.get("output_requirements", ""),
            "workflow_goal": ai_plan.get("context_analysis", {}).get(
                "user_goal", request
            ),
            "ai_confidence": ai_plan.get("confidence", 0.8),
            "single_agent_mode": True,
        }

        # Execute with enhanced context
        result = await self._execute_specialized_agent(
            agent_name, request, files, context
        )

        return result

    async def _synthesize_ai_workflow_response(
        self, request: str, workflow_result: Dict, ai_plan: Dict
    ) -> str:
        """AI-driven synthesis of workflow results into user response."""

        if workflow_result.get("status") == "error":
            return f"AI workflow encountered an issue: {workflow_result.get('error', 'Unknown error')}"

        results = workflow_result.get("results", {})
        context_analysis = ai_plan.get("context_analysis", {})
        user_goal = context_analysis.get("user_goal", request)

        # Build intelligent response
        response_parts = []

        # Add goal completion status
        response_parts.append(f"AI Workflow Complete: {user_goal}")

        # Add workflow summary with intelligence
        workflow_summary = workflow_result.get("summary", "")
        if workflow_summary:
            response_parts.append(workflow_summary)

        # Add specific agent results with context awareness
        successful_results = []
        for agent_name, result in results.items():
            if isinstance(result, dict) and result.get("status") == "success":
                data = result.get("data", {})

                # Get agent's role from AI plan
                agent_instructions = ai_plan.get("agent_instructions", {}).get(
                    agent_name, {}
                )
                agent_role = agent_instructions.get(
                    "primary_task", f"{agent_name} processing"
                )

                if agent_name == "data_analyzer" and isinstance(data, dict):
                    successful_results.append(
                        f"📊 Data Analysis ({agent_role}): Completed with insights"
                    )
                elif agent_name == "pdf_analyzer" and isinstance(data, dict):
                    if data.get("specific_answer"):
                        successful_results.append(
                            f"📄 PDF Analysis: {data['specific_answer'][:100]}..."
                        )
                    else:
                        successful_results.append(
                            f"📄 PDF Analysis ({agent_role}): Completed"
                        )
                elif agent_name == "chart_generator":
                    successful_results.append(
                        f"📈 Visualization ({agent_role}): Generated successfully"
                    )
                elif agent_name == "text_processor":
                    successful_results.append(
                        f"📝 Text Processing ({agent_role}): Completed"
                    )
                else:
                    # Dynamic or unknown agent
                    successful_results.append(
                        f"🔧 {agent_name.title()} ({agent_role}): Completed"
                    )

        if successful_results:
            response_parts.extend(successful_results)

        # Add AI metadata
        confidence = ai_plan.get("confidence", 0.8)
        complexity = ai_plan.get("complexity", "medium")
        response_parts.append(
            f"🤖 AI Orchestration: {confidence:.0%} confidence, {complexity} complexity"
        )

        return " | ".join(response_parts)

    async def _create_required_agents(self, compatibility_analysis: Dict) -> Dict:
        """Create all required agents from compatibility analysis"""

        creation_results = {"agents_created": [], "errors": []}

        # Get suggested agents from the compatibility analysis
        suggested_agents = compatibility_analysis.get(
            "creation_recommendation", {}
        ).get("suggested_agents", [])

        if not suggested_agents:
            return {
                "status": "no_agents_to_create",
                "message": "No agents suggested for creation",
                **creation_results,
            }

        for agent_requirement in suggested_agents:
            try:
                print(f"🎯 Creating agent: {agent_requirement['agent_name']}")

                # Use the enhanced agent factory method
                result = await self.agent_factory.create_agent_from_requirement(
                    agent_requirement
                )

                if result["status"] == "success":
                    creation_results["agents_created"].append(result["agent_name"])
                    print(f"✅ Created agent: {result['agent_name']}")
                else:
                    creation_results["errors"].append(
                        result.get("error", "Unknown error")
                    )
                    print(
                        f"❌ Failed to create agent: {agent_requirement['agent_name']}"
                    )

            except Exception as e:
                error_msg = (
                    f"Failed to create {agent_requirement['agent_name']}: {str(e)}"
                )
                creation_results["errors"].append(error_msg)
                print(f"❌ Exception creating agent: {str(e)}")

        return {
            "status": "success" if creation_results["agents_created"] else "error",
            **creation_results,
        }

    def _get_system_context(self) -> Dict:
        """Provide current system context for agent design"""
        from core.registry_singleton import get_shared_registry

        registry = get_shared_registry()

        return {
            "available_tools": list(registry.tools.get("tools", {}).keys()),
            "existing_agents": list(registry.agents.get("agents", {}).keys()),
            "file_types": ["csv", "pdf", "json", "text", "excel"],
            "workflow_patterns": ["sequential", "parallel"],
        }

    async def _analyze_with_ai(self, request: str, files: List[Dict]) -> Dict:
        """Use GPT-4 to analyze request with ACTUAL DATA - works with ANY file type."""

        # Build context with whatever data we have
        context_parts = [f"User request: {request}"]

        if files:
            for file in files:
                if file.get("read_success"):
                    context_parts.append(
                        f"\nFile: {file['original_name']} (Type: {file['structure']})"
                    )

                    # Let GPT-4 see the actual content based on file type
                    content = file.get("content", {})

                    if file["structure"] == "tabular":
                        # CSV/Excel - show columns and sample data
                        context_parts.append(f"Columns: {content.get('columns', [])}")
                        context_parts.append(
                            f"Sample data: {content.get('first_10_rows', [])[:3]}"
                        )

                    elif file["structure"] == "text":
                        # Text/PDF/Word - show actual text
                        context_parts.append(
                            f"Text content: {content.get('text', '')[:1000]}"
                        )

                    elif file["structure"] == "json":
                        # JSON - show structure and data
                        context_parts.append(
                            f"JSON data: {json.dumps(content.get('data', {}), indent=2)[:1000]}"
                        )

                    elif file["structure"] == "yaml":
                        # YAML - show parsed data
                        context_parts.append(
                            f"YAML data: {json.dumps(content.get('data', {}), indent=2)[:1000]}"
                        )

                    else:
                        # Unknown type - show what we have
                        context_parts.append(f"Content: {str(content)[:1000]}")

        # Let GPT-4 figure out what to do with ANY data type
        prompt = f"""
        {chr(10).join(context_parts)}
        
        Available agents: {list(self.registry.agents['agents'].keys())}
        
        YOU CAN SEE THE ACTUAL DATA ABOVE. Based on what you see:
        1. What type of data is this?
        2. What does the user want to do with it?
        3. What specific processing is needed?
        4. Which agents should handle this?
        
        If it's CSV data with sales, actually look at the values and answer the question.
        If it's text, analyze the actual text content.
        If it's JSON, understand the structure and process accordingly.
        
        Be specific based on the ACTUAL DATA you can see, not generic descriptions.
        
        Return JSON with your analysis and plan.
        """

        response = self.openai_client.chat.completions.create(
            model=ORCHESTRATOR_MODEL,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )

        return json.loads(response.choices[0].message.content)

    async def _ai_plan_workflow(
        self, request: str, files: List[Dict], analysis: Dict
    ) -> Dict:
        """
        GPT-4 plans workflow with knowledge of actual data structure.
        """
        available_agents = self.registry.list_agents()
        available_tools = self.registry.list_tools()

        prompt = f"""
        Create a workflow plan based on ACTUAL data structure:
        
        REQUEST: {request}
        
        ANALYSIS: {json.dumps(analysis, indent=2)}
        
        AVAILABLE AGENTS: {[a['name'] for a in available_agents]}
        AVAILABLE TOOLS: {[t['name'] for t in available_tools]}
        
        Return JSON with:
        {{
            "agents": ["agent1", "agent2"],
            "missing_components": {{"agents": [], "tools": []}},
            "execution_strategy": "sequential",
            "data_flow": {{"step1": "description", "step2": "description"}},
            "expected_output": "description"
        }}
        
        IMPORTANT: You can see the actual data columns and structure. Plan based on what's really there.
        """

        response = self.openai_client.chat.completions.create(
            model=ORCHESTRATOR_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_completion_tokens=ORCHESTRATOR_MAX_TOKENS,
            response_format={"type": "json_object"},
        )

        plan = json.loads(response.choices[0].message.content)
        plan["ai_calls"] = 2  # Track AI usage
        return plan

    async def _create_missing_components(self, missing: Dict):
        """
        Create missing agents/tools using AI.
        """
        # Create tools first (agents depend on them)
        for tool_name in missing.get("tools", []):
            print(f"Creating tool: {tool_name}")
            self.tool_factory.ensure_tool(tool_name, f"Tool for {tool_name}")

        # Create agents
        for agent_name in missing.get("agents", []):
            print(f"Creating agent: {agent_name}")
            self.agent_factory.ensure_agent(agent_name, f"Agent for {agent_name}")

    async def _execute_ai_workflow(
        self, plan: Dict, request: str, files: List[Dict]
    ) -> Dict:
        """Execute workflow with actual data - ANY file type."""

        results = {}

        # FIXED: Handle the case when there are no files properly
        if files and files[0].get("read_success"):
            # We have actual file data
            actual_data = files[0]["content"]  # The ACTUAL content
            data_type = files[0]["structure"]
        else:
            # No files - use the request as text data
            actual_data = request
            data_type = "text"  # Treat request as text to be processed

        for agent_name in plan.get("agents", []):
            print(f"Executing Agent: {agent_name}")

            # Let Claude work with the actual data
            agent_prompt = f"""
            You are the '{agent_name}' agent.
            
            Original request: {request}
            Data type: {data_type}
            
            ACTUAL DATA TO PROCESS:
            {self._format_data_for_prompt(actual_data, data_type)}
            
            INSTRUCTIONS:
            - Work with the ACTUAL data above
            - If it's a question like "What is 2+2?", calculate and provide the answer
            - If it's CSV data, analyze the real values
            - If it's text, process the actual text
            - If it's JSON, work with the real structure
            - Provide specific answers based on what you see
            - Don't just describe what you would do - DO IT
            
            For example:
            - If asked "What is 2+2?", answer "4"
            - If asked for highest sales region, tell me which region and the value
            - If asked to extract emails, show the actual emails you found
            - If asked to summarize, provide the actual summary
            """

            response = self.claude_client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=CLAUDE_MAX_TOKENS,
                messages=[{"role": "user", "content": agent_prompt}],
            )

            results[agent_name] = response.content[0].text

        return results

    def _format_data_for_prompt(self, data: Any, data_type: str) -> str:
        """Format ANY data type for AI prompt - FIXED VERSION."""

        try:
            if data_type == "tabular":
                # CSV/Excel data
                if isinstance(data, dict):
                    output = f"Columns: {data.get('columns', [])}\n"
                    output += f"Total rows: {data.get('total_rows', 0)}\n"
                    output += (
                        f"Data:\n{json.dumps(data.get('first_10_rows', []), indent=2)}"
                    )
                    return output[:2000]
                else:
                    return f"Tabular data (non-dict): {str(data)[:2000]}"

            elif data_type == "text":
                # Text content - handle both dict and string
                if isinstance(data, dict):
                    return str(data.get("text", data))[:2000]
                else:
                    # If it's already a string, use it directly
                    return str(data)[:2000]

            elif data_type in ["json", "yaml"]:
                # Structured data
                if isinstance(data, dict):
                    return json.dumps(data.get("data", data), indent=2)[:2000]
                else:
                    return (
                        json.dumps(data, indent=2)[:2000] if data else str(data)[:2000]
                    )

            # Default - safely convert to string
            return str(data)[:2000]

        except Exception as e:
            print(f"DEBUG: Error formatting data: {e}")
            return f"Data formatting error: {str(data)[:500]}"

    async def _ai_synthesize_response(
        self, request: str, plan: Dict, results: Dict
    ) -> str:
        """
        GPT-4 creates final user-friendly response.
        FIXED: Handle string results from Claude agents properly.
        """

        # FIXED: Handle both string and dict results properly
        formatted_results = {}
        for k, v in results.items():
            if isinstance(v, dict):
                # If result is a dict, try to get 'output' or use the whole dict
                formatted_results[k] = str(v.get("output", v))[:500]
            elif isinstance(v, str):
                # If result is a string (which it is from Claude), use it directly
                formatted_results[k] = v[:500]
            else:
                # For any other type, convert to string
                formatted_results[k] = str(v)[:500]

        prompt = f"""
        Create a natural response for the user:
        
        ORIGINAL REQUEST: {request}
        
        WORKFLOW EXECUTED: {plan.get('agents', [])}
        
        RESULTS: {json.dumps(formatted_results, indent=2)}
        
        Synthesize a clear, helpful response that directly answers the user's request.
        Include specific details from the results.
        Be conversational and helpful.
        """

        response = self.openai_client.chat.completions.create(
            model=ORCHESTRATOR_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_completion_tokens=ORCHESTRATOR_MAX_TOKENS,
        )

        return response.choices[0].message.content

    async def _execute_specialized_agent(
        self, agent_name: str, request: str, files: List[Dict], context: Dict = None
    ) -> Dict:
        """
        ENHANCED specialized agent execution with AI context.
        This REPLACES the existing method in simplified_orchestrator.py
        """

        # Get the agent
        agent = self.workflow_engine.agents.get(agent_name)
        if not agent:
            # Try to load dynamic agent
            load_result = await self.workflow_engine.load_dynamic_agent(agent_name)
            if load_result.get("status") == "success":
                agent = self.workflow_engine.dynamic_agents.get(agent_name)

            if not agent:
                return {"status": "error", "error": f"Agent {agent_name} not found"}

        # Prepare file data
        file_data = files[0] if files and files[0].get("read_success") else None

        # Execute with context awareness
        if hasattr(agent, "execute") and agent_name in [
            "pdf_analyzer",
            "text_processor",
            "chart_generator",
        ]:
            # New specialized agents - use enhanced context
            result = await agent.execute(
                request=request, file_data=file_data, context=context or {}
            )
        else:
            # Old IntelligentAgent format
            state = {
                "current_data": file_data,
                "request": request,
                "results": {},
                "errors": [],
                "execution_path": [],
                "context": context or {},
            }
            result = await agent.execute(state)

        # Generate enhanced response based on AI context
        if result.get("status") == "success":
            data = result.get("data", {})

            # Use AI context to improve response
            if context and context.get("ai_guided"):
                primary_task = context.get("primary_task", "")
                response_parts = [f"AI-Guided {agent_name.title()}: {primary_task}"]
            else:
                response_parts = [f"{agent_name.title()} Processing Complete:"]

            # Add specific results
            if agent_name == "pdf_analyzer" and isinstance(data, dict):
                if data.get("specific_answer"):
                    response_parts.append(f"Answer: {data['specific_answer']}")
                elif data.get("summary"):
                    response_parts.append(f"Summary: {data['summary'][:150]}...")

            elif agent_name == "data_analyzer" and isinstance(data, dict):
                response_parts.append(
                    "Data analysis completed with statistical insights"
                )

            elif agent_name == "text_processor" and isinstance(data, dict):
                if data.get("processed_text"):
                    response_parts.append(f"Result: {data['processed_text'][:150]}...")

            elif agent_name == "chart_generator":
                response_parts.append("Visualization generated successfully")

            response = " | ".join(response_parts)
        else:
            response = f"Processing failed: {result.get('error', 'Unknown error')}"

        return {"response": response, **result}

    async def _process_simple_request(
        self,
        user_request: str,
        enriched_files: List[Dict],
        workflow_id: str,
        start_time,
    ) -> Dict:
        """Process simple requests using the original logic."""

        # Use original logic for simple cases
        analysis = await self._analyze_with_ai(user_request, enriched_files)
        plan = await self._ai_plan_workflow(user_request, enriched_files, analysis)
        results = await self._execute_ai_workflow(plan, user_request, enriched_files)
        response = await self._ai_synthesize_response(user_request, plan, results)

        return {
            "status": "success",
            "workflow_id": workflow_id,
            "response": response,
            "execution_time": (datetime.now() - start_time).total_seconds(),
            "workflow": plan,
            "results": results,
            "metadata": {
                "workflow_type": "simple",
                "files_processed": len(enriched_files),
                "agents_used": len(plan.get("agents", [])),
            },
        }

    async def _synthesize_workflow_response(
        self, request: str, workflow_result: Dict
    ) -> str:
        """Synthesize final response from multi-agent workflow results - FIXED VERSION."""

        if workflow_result.get("status") == "error":
            return f"Workflow failed: {workflow_result.get('error', 'Unknown error')}"

        results = workflow_result.get("results", {})
        workflow_summary = workflow_result.get("summary", "")

        # Build comprehensive response
        response_parts = ["Multi-agent workflow completed successfully."]

        if workflow_summary:
            response_parts.append(workflow_summary)

        # FIXED: Add specific results from each agent with proper type checking
        for agent_name, result in results.items():
            if isinstance(result, dict) and result.get("status") == "success":
                data = result.get("data", {})

                if agent_name == "pdf_analyzer":
                    if isinstance(data, dict) and data.get("specific_answer"):
                        response_parts.append(
                            f"📄 PDF Analysis: {data['specific_answer']}"
                        )
                    elif isinstance(data, dict) and data.get("summary"):
                        response_parts.append(
                            f"📄 PDF Analysis: {data['summary'][:100]}..."
                        )

                elif agent_name == "text_processor":
                    if isinstance(data, dict) and data.get("processed_text"):
                        response_parts.append(
                            f"📝 Text Processing: {data['processed_text'][:150]}..."
                        )
                    elif isinstance(data, str):
                        response_parts.append(f"📝 Text Processing: {data[:150]}...")

                elif agent_name == "chart_generator":
                    response_parts.append("📊 Chart generated successfully")
                    if isinstance(data, dict) and data.get("chart_type"):
                        response_parts.append(f"Chart type: {data['chart_type']}")

                elif agent_name == "data_analyzer":
                    response_parts.append("📈 Data analysis completed with insights")
                    if isinstance(data, dict) and data.get("analysis"):
                        response_parts.append(f"Key findings available")

            elif isinstance(result, str):
                # Handle cases where result is a string directly
                response_parts.append(f"• {agent_name}: {result[:100]}...")

        return (
            " | ".join(response_parts) if len(response_parts) > 1 else response_parts[0]
        )
