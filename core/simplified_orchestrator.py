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

from core.workflow_engine import MultiAgentWorkflowEngine, WorkflowPlanner
from core.capability_analyzer import CapabilityAnalyzer
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

        self.workflow_engine = MultiAgentWorkflowEngine()
        self.workflow_planner = WorkflowPlanner()
        self.capability_analyzer = CapabilityAnalyzer()

        # FIX: Initialize the OpenAI openai_client properly
        self.openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)  # Add this line!

        # Initialize Claude openai_client
        self.claude_client = Anthropic(api_key=ANTHROPIC_API_KEY)

        print(f"DEBUG: ANTHROPIC_API_KEY present: {bool(ANTHROPIC_API_KEY)}")
        print(
            f"DEBUG: ANTHROPIC_API_KEY length: {len(ANTHROPIC_API_KEY) if ANTHROPIC_API_KEY else 0}"
        )

    async def process_request(
        self,
        user_request: str,
        files: Optional[List[Dict]] = None,
        auto_create: bool = True,
    ) -> Dict[str, Any]:
        """Enhanced process_request with multi-agent workflow support."""
        workflow_id = f"wf_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        start_time = datetime.now()

        try:
            # Step 1: Read actual file contents
            enriched_files = []
            if files:
                enriched_files = self.file_reader.process_all_files(files)

            # Step 2: Determine if this needs multi-agent workflow
            workflow_plan = self.workflow_planner.plan_workflow(
                user_request, enriched_files
            )

            # Enhanced: Intelligent agent compatibility analysis
            if auto_create:
                print("Analyzing agent compatibility and capability gaps...")

                compatibility_analysis = (
                    await self.capability_analyzer.analyze_agent_compatibility(
                        user_request, workflow_plan, enriched_files
                    )
                )

                overall_confidence = compatibility_analysis["compatibility_analysis"][
                    "overall_confidence"
                ]
                recommendation = compatibility_analysis["compatibility_analysis"][
                    "recommendation"
                ]

                print(f"Agent compatibility confidence: {overall_confidence:.2f}")
                print(f"AI Recommendation: {recommendation}")

                # Show agent evaluations
                for evaluation in compatibility_analysis.get("agent_evaluations", []):
                    agent_name = evaluation["agent_name"]
                    score = evaluation["compatibility_score"]
                    suitability = evaluation["suitability"]
                    print(
                        f"  {agent_name}: {score:.2f} confidence, {suitability} suitability"
                    )

                # NEW: Override workflow plan if confidence is too low
                if overall_confidence < 0.7:
                    print(
                        f"Confidence too low ({overall_confidence:.2f}), checking for better alternatives..."
                    )

                    # Check if better alternatives exist
                    better_alternatives = compatibility_analysis.get(
                        "better_alternatives", []
                    )
                    if better_alternatives:
                        # Use the best alternative
                        best_alternative = max(
                            better_alternatives,
                            key=lambda x: x.get("compatibility_score", 0),
                        )
                        if best_alternative["compatibility_score"] > overall_confidence:
                            print(
                                f"Using better alternative: {best_alternative['agent_name']}"
                            )
                            workflow_plan["agents"] = [best_alternative["agent_name"]]
                            workflow_plan["execution_strategy"] = "sequential"

                    # If still low confidence or no alternatives, mark for creation
                    if overall_confidence < 0.7 and recommendation in [
                        "create_new",
                        "hybrid_approach",
                    ]:
                        print("AI recommends creating specialized agents...")

                        # Actually create the required agents
                        creation_result = await self._create_required_agents(
                            compatibility_analysis
                        )

                        if creation_result["status"] == "success":
                            print(
                                f"✅ Created {len(creation_result['agents_created'])} agents successfully"
                            )

                            # Refresh the workflow plan with newly created agents
                            from core.registry_singleton import force_global_reload

                            force_global_reload()  # Reload registry to see new agents

                            # Re-plan workflow with new agents available
                            from core.registry_singleton import get_shared_registry

                            updated_registry = get_shared_registry()
                            print(
                                f"Registry after creation: {list(updated_registry.agents.get('agents', {}).keys())}"
                            )

                            workflow_plan = self.workflow_planner.plan_workflow(
                                user_request, enriched_files
                            )
                            print(f"Updated workflow plan: {workflow_plan['agents']}")

                            # If planner still doesn't pick up the new agent, force it
                            created_agents = creation_result.get("agents_created", [])
                            if (
                                created_agents
                                and workflow_plan.get("agents") != created_agents
                            ):
                                print(
                                    f"🔧 Forcing workflow to use newly created agents: {created_agents}"
                                )
                                workflow_plan["agents"] = created_agents
                                workflow_plan["execution_strategy"] = "sequential"
                                print(
                                    f"Forced workflow plan: {workflow_plan['agents']}"
                                )

                            # Update confidence since we now have suitable agents
                            overall_confidence = 1.0

                        elif creation_result["status"] == "no_agents_to_create":
                            print("No agents needed to be created")
                        else:
                            print(
                                f"❌ Agent creation failed: {creation_result.get('errors', [])}"
                            )

                            # Show what was attempted
                            suggested_agents = compatibility_analysis.get(
                                "creation_recommendation", {}
                            ).get("suggested_agents", [])
                            if suggested_agents:
                                print("Attempted to create:")
                                for suggested in suggested_agents:
                                    print(
                                        f"  - {suggested['agent_name']}: {suggested['purpose']}"
                                    )

                # Show better alternatives if found
                better_alternatives = compatibility_analysis.get(
                    "better_alternatives", []
                )
                if better_alternatives:
                    print("Better alternatives found in registry:")
                    for alt in better_alternatives:
                        print(f"  - {alt['agent_name']}: {alt['why_better']}")

                # If still using unsuitable agent after analysis, provide helpful response
                if (
                    overall_confidence < 0.3
                    and recommendation == "create_new"
                    and not better_alternatives
                ):

                    print(
                        "No suitable agents available - providing capability explanation"
                    )

                    # Instead of executing with wrong agent, explain what's needed
                    suggested_agents = compatibility_analysis.get(
                        "creation_recommendation", {}
                    ).get("suggested_agents", [])
                    if suggested_agents:
                        explanation = f"This request requires specialized capabilities not currently available. "
                        explanation += f"Would need: {', '.join([a['agent_name'] for a in suggested_agents])}. "
                        explanation += "Dynamic agent creation will be available in the next system update."

                        return {
                            "status": "capability_gap",
                            "workflow_id": workflow_id,
                            "response": explanation,
                            "execution_time": (
                                datetime.now() - start_time
                            ).total_seconds(),
                            "workflow": workflow_plan,
                            "metadata": {
                                "workflow_type": "capability_gap_detected",
                                "missing_capabilities": [
                                    a["agent_name"] for a in suggested_agents
                                ],
                                "confidence": overall_confidence,
                            },
                        }

            if len(workflow_plan["agents"]) > 1:
                print(f"Multi-agent workflow detected: {workflow_plan['agents']}")

                # Execute multi-agent workflow
                workflow_result = await self.workflow_engine.execute_workflow(
                    workflow_plan, user_request, enriched_files
                )

                # Synthesize final response from workflow
                response = await self._synthesize_workflow_response(
                    user_request, workflow_result
                )

                return {
                    "status": "success",
                    "workflow_id": workflow_id,
                    "response": response,
                    "execution_time": (datetime.now() - start_time).total_seconds(),
                    "workflow": workflow_plan,
                    "results": workflow_result.get("results", {}),
                    "workflow_summary": workflow_result.get("summary", ""),
                    "metadata": {
                        "workflow_type": "multi_agent",
                        "agents_used": len(workflow_plan["agents"]),
                        "execution_strategy": workflow_plan.get(
                            "execution_strategy", "sequential"
                        ),
                    },
                }

            elif workflow_plan["agents"]:
                # Single specialized agent
                agent_name = workflow_plan["agents"][0]
                print(f"Single specialized agent workflow: {agent_name}")

                result = await self._execute_specialized_agent(
                    agent_name, user_request, enriched_files
                )

                return {
                    "status": "success",
                    "workflow_id": workflow_id,
                    "response": result.get("response", ""),
                    "execution_time": (datetime.now() - start_time).total_seconds(),
                    "workflow": workflow_plan,
                    "results": {agent_name: result},
                    "metadata": {
                        "workflow_type": "single_agent_specialized",
                        "agent_used": agent_name,
                    },
                }
            else:
                # Fall back to original simple processing
                return await self._process_simple_request(
                    user_request, enriched_files, workflow_id, start_time
                )

        except Exception as e:
            print(f"Error: {str(e)}")
            import traceback

            traceback.print_exc()
            return {
                "status": "error",
                "workflow_id": workflow_id,
                "error": str(e),
                "response": f"An error occurred: {str(e)}",
                "workflow": {},
                "metadata": {},
            }

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

    # async def _execute_specialized_agent(
    #     self, agent_name: str, request: str, files: List[Dict]
    # ) -> Dict:
    #     """Execute a specialized agent directly."""

    #     # Get the specialized agent
    #     agent = self.workflow_engine.agents.get(agent_name)
    #     if not agent:
    #         return {"status": "error", "error": f"Agent {agent_name} not found"}

    #     # Execute with file data
    #     file_data = files[0] if files and files[0].get("read_success") else None
    #     result = await agent.execute(request, file_data)

    #     # Generate response
    #     if result.get("status") == "success":
    #         data = result.get("data", {})
    #         response_parts = []

    #         if agent_name == "pdf_analyzer":
    #             response_parts.append("PDF Analysis Complete:")
    #             if data.get("summary"):
    #                 response_parts.append(f"Summary: {data['summary']}")
    #             if data.get("key_points"):
    #                 response_parts.append(
    #                     f"Key Points: {', '.join(data['key_points'][:3])}"
    #                 )

    #         elif agent_name == "text_processor":
    #             response_parts.append("Text Processing Complete:")
    #             if data.get("processed_text"):
    #                 response_parts.append(f"Result: {data['processed_text'][:200]}...")
    #             if data.get("sentiment"):
    #                 response_parts.append(f"Sentiment: {data['sentiment']}")

    #         elif agent_name == "chart_generator":
    #             response_parts.append("Chart Generation Complete:")
    #             if data.get("chart_type"):
    #                 response_parts.append(f"Generated {data['chart_type']} chart")

    #         response = (
    #             " | ".join(response_parts)
    #             if response_parts
    #             else "Processing completed successfully."
    #         )
    #     else:
    #         response = f"Processing failed: {result.get('error', 'Unknown error')}"

    #     return {"response": response, **result}

    async def _execute_specialized_agent(
        self, agent_name: str, request: str, files: List[Dict]
    ) -> Dict:
        """Execute a specialized agent directly - FIXED VERSION."""

        # Get the specialized agent
        agent = self.workflow_engine.agents.get(agent_name)
        if not agent:
            return {"status": "error", "error": f"Agent {agent_name} not found"}

        # Prepare file data
        file_data = files[0] if files and files[0].get("read_success") else None

        # FIXED: Check if this is a new specialized agent or old IntelligentAgent
        if hasattr(agent, "execute") and agent_name in [
            "pdf_analyzer",
            "text_processor",
            "chart_generator",
        ]:
            # New specialized agents - use keyword arguments
            result = await agent.execute(
                request=request, file_data=file_data, context=None
            )
        else:
            # Old IntelligentAgent - use state format
            state = {
                "current_data": file_data,
                "request": request,
                "results": {},
                "errors": [],
                "execution_path": [],
            }
            result = await agent.execute(state)

        # Generate response (rest stays the same)
        if result.get("status") == "success":
            data = result.get("data", {})
            response_parts = []

            if agent_name == "pdf_analyzer":
                response_parts.append("PDF Analysis Complete:")
                if data.get("summary"):
                    response_parts.append(f"Summary: {data['summary']}")
                if data.get("key_points"):
                    response_parts.append(
                        f"Key Points: {', '.join(data['key_points'][:3])}"
                    )

            elif agent_name == "text_processor":
                response_parts.append("Text Processing Complete:")
                if data.get("processed_text"):
                    response_parts.append(f"Result: {data['processed_text'][:200]}...")
                if data.get("sentiment"):
                    response_parts.append(f"Sentiment: {data['sentiment']}")

            elif agent_name == "chart_generator":
                response_parts.append("Chart Generation Complete:")
                if data.get("chart_type"):
                    response_parts.append(f"Generated {data['chart_type']} chart")

            elif agent_name == "data_analyzer":
                response_parts.append("Data Analysis Complete:")
                if isinstance(data, dict) and data.get("processed_data"):
                    response_parts.append(
                        f"Analysis: {str(data['processed_data'])[:100]}..."
                    )

            response = (
                " | ".join(response_parts)
                if response_parts
                else "Processing completed successfully."
            )
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
