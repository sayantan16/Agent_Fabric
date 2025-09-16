"""
AI-Driven Workflow Planner - GPT-4 powered intelligent workflow orchestration
Location: core/ai_workflow_planner.py

This replaces rule-based workflow planning with AI-driven strategic planning
"""

import json
import openai
from typing import Dict, List, Any, Optional
from datetime import datetime

from config import OPENAI_API_KEY, ORCHESTRATOR_MODEL, ORCHESTRATOR_MAX_TOKENS


class AIWorkflowPlanner:
    """
    GPT-4 powered workflow planner that understands complex requests
    and plans optimal multi-agent execution strategies.
    """

    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

    async def plan_intelligent_workflow(
        self,
        request: str,
        files: List[Dict] = None,
        available_agents: List[str] = None,
        available_tools: List[str] = None,
        scenario_context: Dict = None,
    ) -> Dict:
        """
        Use GPT-4 to intelligently plan multi-agent workflows.

        Args:
            request: User's natural language request
            files: List of file data with structure information
            available_agents: List of available agent names
            available_tools: List of available tool names

        Returns:
            Dict with intelligent workflow plan
        """

        # Handle scenario-aware planning
        if scenario_context:
            print(
                f"📋 Planning with scenario context: {scenario_context.get('scenario_key')}"
            )

            # For scenario-based workflows, we already have the plan structure
            # Just need to adapt it to the specific request details
            from config import HACKATHON_SCENARIOS

            scenario_key = scenario_context.get("scenario_key")
            scenario = HACKATHON_SCENARIOS[scenario_key]

            # Use scenario template but allow for request-specific adaptations
            context_analysis = await self._analyze_request_context(request, files)
            context_analysis["scenario"] = scenario_context
            context_analysis["workflow_type"] = "scenario_based"

            # Return scenario-based plan with adaptations
            return {
                "workflow_type": "scenario_based",
                "scenario": scenario_key,
                "scenario_name": scenario["name"],
                "agents": scenario["workflow_pattern"]["agent_sequence"],
                "execution_strategy": scenario["workflow_pattern"][
                    "execution_strategy"
                ],
                "missing_capabilities": scenario["agents_to_create"],
                "context_analysis": context_analysis,
                "rationale": f"Scenario-based workflow for {scenario['name']}",
                "estimated_steps": len(scenario["workflow_pattern"]["agent_sequence"]),
                "complexity": scenario["complexity"],
                "confidence": 0.95,  # High confidence for known scenarios
                "expected_duration": scenario["expected_duration"],
            }

        # Step 1: Analyze request context with actual data
        context_analysis = await self._analyze_request_context(request, files)

        # Step 2: Plan optimal workflow strategy
        workflow_strategy = await self._plan_workflow_strategy(
            request, context_analysis, available_agents, available_tools
        )

        # Step 3: Design data flow between agents
        data_flow_plan = await self._design_data_flow(
            workflow_strategy, context_analysis
        )

        # Step 4: Create agent-specific instructions
        agent_instructions = await self._create_agent_instructions(
            workflow_strategy, data_flow_plan, request
        )

        return {
            "workflow_type": "ai_planned",
            "agents": workflow_strategy.get("agent_sequence", []),
            "execution_strategy": workflow_strategy.get(
                "execution_strategy", "sequential"
            ),
            "data_flow": data_flow_plan,
            "agent_instructions": agent_instructions,
            "context_analysis": context_analysis,
            "rationale": workflow_strategy.get("rationale", ""),
            "estimated_steps": len(workflow_strategy.get("agent_sequence", [])),
            "complexity": workflow_strategy.get("complexity", "medium"),
            "missing_capabilities": workflow_strategy.get("missing_capabilities", []),
            "confidence": workflow_strategy.get("confidence", 0.8),
        }

    async def _analyze_request_context(self, request: str, files: List[Dict]) -> Dict:
        """GPT-4 analyzes the request context with actual file data."""

        # Build context with real file data
        context_parts = [f"USER REQUEST: {request}"]

        if files:
            for file in files:
                if file.get("read_success"):
                    context_parts.append(
                        f"\nFILE: {file['original_name']} (Type: {file['structure']})"
                    )

                    content = file.get("content", {})
                    if file["structure"] == "tabular":
                        context_parts.append(f"Columns: {content.get('columns', [])}")
                        context_parts.append(
                            f"Sample data: {content.get('first_10_rows', [])[:2]}"
                        )
                    elif file["structure"] == "text":
                        context_parts.append(
                            f"Text content: {content.get('text', '')[:800]}"
                        )
                    elif file["structure"] in ["json", "yaml"]:
                        context_parts.append(
                            f"Data structure: {str(content.get('data', {}))[:800]}"
                        )

        prompt = f"""
        Analyze this request with the actual data provided:
        
        {chr(10).join(context_parts)}
        
        INTELLIGENT ANALYSIS REQUIRED:
        
        1. **GOAL UNDERSTANDING**: What does the user actually want to accomplish?
        2. **DATA ASSESSMENT**: What type of data do we have and what can be done with it?
        3. **PROCESSING REQUIREMENTS**: What specific transformations/analysis are needed?
        4. **OUTPUT EXPECTATIONS**: What should the final result look like?
        5. **COMPLEXITY EVALUATION**: How complex is this request (simple/medium/complex)?
        
        CRITICAL THINKING:
        - If they say "analyze CSV and create PDF report" - they want CSV analysis THEN PDF creation
        - If they say "extract from PDF" - they want PDF reading/extraction
        - If they ask about specific data values - look at the actual data columns and values
        - Be specific about what processing steps are actually needed
        
        Return JSON:
        {{
            "user_goal": "what user wants to accomplish",
            "data_assessment": {{
                "input_types": ["csv", "text", etc],
                "data_quality": "good|fair|poor",
                "data_size": "small|medium|large",
                "key_columns": ["if csv data"]
            }},
            "processing_requirements": [
                "step 1: specific processing needed",
                "step 2: next processing step",
                "step 3: final step"
            ],
            "output_expectations": {{
                "format": "pdf|chart|analysis|summary",
                "content_type": "report|visualization|extracted_data",
                "delivery_method": "file|text_response|both"
            }},
            "complexity": "simple|medium|complex",
            "estimated_time": "quick|moderate|extensive",
            "key_insights": ["insight about what's actually needed"]
        }}
        """

        response = self.openai_client.chat.completions.create(
            model=ORCHESTRATOR_MODEL,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            max_completion_tokens=ORCHESTRATOR_MAX_TOKENS,
        )

        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            return {
                "user_goal": "Process user request",
                "complexity": "medium",
                "processing_requirements": ["analyze_data", "generate_output"],
            }

    async def _plan_workflow_strategy(
        self,
        request: str,
        context_analysis: Dict,
        available_agents: List[str],
        available_tools: List[str],
    ) -> Dict:
        """Pure natural language workflow analysis without structural constraints."""

        # Phase 1: Completely unconstrained reasoning
        workflow_analysis = await self._analyze_workflow_naturally(
            request, context_analysis
        )

        # Phase 2: Extract structure from natural analysis
        workflow_structure = await self._extract_workflow_structure(workflow_analysis)

        # Phase 3: Match to agents
        agent_assignments = await self._match_structure_to_agents(
            workflow_structure, available_agents
        )

        return agent_assignments

    async def _analyze_workflow_naturally(
        self, request: str, context_analysis: Dict
    ) -> str:
        """Let AI reason completely naturally about the workflow."""

        prompt = f"""
        Analyze this request and explain what needs to happen:

        REQUEST: {request}
        CONTEXT: {json.dumps(context_analysis, indent=2)}

        Explain the processing flow needed to fulfill this request. 
        Think about what transformations are required to get from input to desired output.
        Be as detailed as necessary - don't worry about structure or format.
        """

        response = self.openai_client.chat.completions.create(
            model=ORCHESTRATOR_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_completion_tokens=ORCHESTRATOR_MAX_TOKENS,
        )

        natural_analysis = response.choices[0].message.content

        # DEBUG: Show the natural reasoning
        print(f"\n🧠 NATURAL WORKFLOW ANALYSIS:")
        print(f"{natural_analysis}")
        print(f"\n" + "=" * 50)

        return natural_analysis

    async def _extract_workflow_structure(self, natural_analysis: str) -> Dict:
        """Extract workflow structure from natural language analysis."""

        prompt = f"""
        Read this workflow analysis and identify the distinct processing operations:

        ANALYSIS:
        {natural_analysis}

        From this analysis, identify what distinct operations or transformations are described.
        Each operation should be something that could be handled as a separate processing unit.

        Return JSON identifying the operations you found:
        {{
            "operations_identified": [
                {{
                    "operation_description": "what this operation does",
                    "input_needed": "what input this operation requires",
                    "output_produced": "what this operation produces",
                    "processing_type": "what kind of processing this is"
                }}
            ],
            "workflow_complexity": "assessment of overall complexity",
            "execution_approach": "how these operations should be coordinated"
        }}
        """

        response = self.openai_client.chat.completions.create(
            model=ORCHESTRATOR_MODEL,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            max_completion_tokens=ORCHESTRATOR_MAX_TOKENS,
        )

        try:
            structure = json.loads(response.choices[0].message.content)

            # DEBUG: Show extracted structure
            print(f"\n📋 EXTRACTED WORKFLOW STRUCTURE:")
            print(
                f"Operations found: {len(structure.get('operations_identified', []))}"
            )
            for i, op in enumerate(structure.get("operations_identified", []), 1):
                print(f"  Operation {i}: {op.get('operation_description', 'unknown')}")
            print(f"Complexity: {structure.get('workflow_complexity', 'unknown')}")
            print(f"Execution: {structure.get('execution_approach', 'unknown')}")
            print(f"\n" + "=" * 50)

            return structure
        except json.JSONDecodeError:
            return {
                "operations_identified": [
                    {
                        "operation_description": "Process request",
                        "input_needed": "user request",
                        "output_produced": "processed response",
                        "processing_type": "general",
                    }
                ],
                "workflow_complexity": "medium",
                "execution_approach": "sequential",
            }

    async def _match_structure_to_agents(
        self, workflow_structure: Dict, available_agents: List[str]
    ) -> Dict:
        """Match extracted operations to available agents."""

        agent_details = await self._get_agent_details(available_agents)

        prompt = f"""
        Match these processing operations to available agents:

        OPERATIONS:
        {json.dumps(workflow_structure, indent=2)}

        AVAILABLE AGENTS:
        {json.dumps(agent_details, indent=2)}

        For each operation, determine if any available agent can handle it.
        Focus on capability alignment, not naming patterns.

        Return JSON:
        {{
            "agent_assignments": [
                {{
                    "operation": "operation description",
                    "assigned_agent": "agent_name or null",
                    "confidence": 0.85,
                    "reasoning": "why this agent matches this operation"
                }}
            ],
            "missing_capabilities": [
                {{
                    "operation": "operation description",
                    "required_agent": "description of needed agent"
                }}
            ]
        }}
        """

        response = self.openai_client.chat.completions.create(
            model=ORCHESTRATOR_MODEL,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            max_completion_tokens=ORCHESTRATOR_MAX_TOKENS,
        )

        try:
            matching_result = json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            matching_result = {"agent_assignments": [], "missing_capabilities": []}

        # Convert to final workflow format
        assigned_agents = []
        missing_capabilities = []

        for assignment in matching_result.get("agent_assignments", []):
            if assignment.get("assigned_agent"):
                assigned_agents.append(assignment["assigned_agent"])

        for missing in matching_result.get("missing_capabilities", []):
            missing_capabilities.append(
                {
                    "capability": missing.get("required_agent", "unknown"),
                    "priority": "high",
                }
            )

        # DEBUG: Show agent matching results
        print(f"\n🎯 AGENT MATCHING RESULTS:")
        for assignment in matching_result.get("agent_assignments", []):
            print(
                f"  {assignment.get('operation', 'unknown')} → {assignment.get('assigned_agent', 'none')}"
            )
            print(f"    Confidence: {assignment.get('confidence', 0)}")
            print(f"    Reasoning: {assignment.get('reasoning', 'none')}")

        missing = matching_result.get("missing_capabilities", [])
        if missing:
            print(f"  Missing capabilities: {len(missing)}")
            for miss in missing:
                print(f"    - {miss.get('operation', 'unknown')}")

        print(f"\n" + "=" * 50)

        return {
            "agent_sequence": assigned_agents,
            "execution_strategy": workflow_structure.get(
                "execution_approach", "sequential"
            ),
            "rationale": workflow_structure.get(
                "workflow_complexity", "AI analysis complete"
            ),
            "missing_capabilities": missing_capabilities,
            "confidence": 0.8,
            "workflow_structure": workflow_structure,
            "agent_matching": matching_result,
        }

    async def _analyze_capability_requirements(
        self, request: str, context_analysis: Dict
    ) -> List[Dict]:
        """AI analyzes what capabilities are actually needed for this request."""

        prompt = f"""
        Analyze this request to determine what capabilities are actually needed:

        REQUEST: {request}
        CONTEXT: {json.dumps(context_analysis, indent=2)}

        Think step-by-step about what processing is actually required:
        - Simple requests might need only 1 capability
        - Complex requests might need many sequential capabilities  
        - Consider what transforms the input into the desired output

        For each capability you identify, define:
        - What specific processing is needed
        - What type of input it expects
        - What type of output it produces
        - How it fits in the overall workflow

        Return JSON with however many steps are actually needed:
        {{
            "capability_requirements": [
                {{
                    "step_number": 1,
                    "capability_needed": "specific capability description",
                    "detailed_description": "what this step actually does",
                    "input_type": "input data type",
                    "output_type": "output data type", 
                    "processing_focus": "key processing activities",
                    "connects_to": "next step or final output"
                }}
            ]
        }}

        Base the number of steps on the actual request complexity, not any predetermined pattern.
        """

        response = self.openai_client.chat.completions.create(
            model=ORCHESTRATOR_MODEL,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            max_completion_tokens=ORCHESTRATOR_MAX_TOKENS,
        )

        try:
            result = json.loads(response.choices[0].message.content)
            return result.get("capability_requirements", [])
        except json.JSONDecodeError:
            # Fallback for any parsing issues
            return [
                {
                    "step_number": 1,
                    "capability_needed": "Process request",
                    "detailed_description": request,
                    "input_type": "any",
                    "output_type": "processed_data",
                    "processing_focus": "general processing",
                }
            ]

    async def _get_agent_details(self, available_agents: List[str]) -> Dict:
        """Get detailed agent information from registry for semantic analysis."""

        # Import registry to get agent details
        from core.registry_singleton import get_shared_registry

        registry = get_shared_registry()

        agent_details = {}
        for agent_name in available_agents:
            agent_info = registry.get_agent(agent_name)
            if agent_info:
                agent_details[agent_name] = {
                    "name": agent_name,
                    "description": agent_info.get("description", ""),
                    "capabilities": agent_info.get("uses_tools", []),
                    "input_schema": agent_info.get("input_schema", {}),
                    "output_schema": agent_info.get("output_schema", {}),
                    "tags": agent_info.get("tags", []),
                    "execution_count": agent_info.get("execution_count", 0),
                    "status": agent_info.get("status", "unknown"),
                }

        return agent_details

    async def _semantic_agent_matching(
        self, capability_requirements: List[Dict], agent_details: Dict
    ) -> Dict:
        """Use AI to semantically match capabilities to agents."""

        prompt = f"""
        You are an intelligent agent selector. Match capability requirements to available agents based on semantic understanding, NOT keyword matching.
        
        CAPABILITY REQUIREMENTS:
        {json.dumps(capability_requirements, indent=2)}
        
        AVAILABLE AGENTS:
        {json.dumps(agent_details, indent=2)}
        
        For each capability requirement, analyze:
        1. Does any agent's description semantically align with what's needed?
        2. Would the agent's typical input/output work for this step?
        3. How confident are you in this match?
        
        IMPORTANT: Base decisions on semantic meaning, not just keyword presence.
        - "read_text" agent that "processes text" CAN handle "extract key information from text"
        - "sentiment_analysis_agent" that "analyzes emotional tone" CAN handle "analyze sentiment"
        - Don't require exact keyword matches - understand intent and capability alignment
        
        Return JSON:
        {{
            "agent_assignments": [
                {{
                    "step_number": 1,
                    "capability_needed": "extract key information",
                    "assigned_agent": "read_text",
                    "confidence": 0.85,
                    "reasoning": "The read_text agent processes text input which aligns with extracting key information from text",
                    "semantic_match": "high"
                }}
            ],
            "unmatched_requirements": [
                {{
                    "step_number": 2,
                    "capability_needed": "sentiment analysis", 
                    "reason": "no agent description mentions sentiment analysis capability",
                    "suggested_agent_name": "sentiment_analyzer",
                    "required_description": "Analyze emotional tone and sentiment in text"
                }}
            ],
            "overall_confidence": 0.75
        }}
        """

        response = self.openai_client.chat.completions.create(
            model=ORCHESTRATOR_MODEL,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            max_completion_tokens=ORCHESTRATOR_MAX_TOKENS,
        )

        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            # Fallback with empty assignments
            return {
                "agent_assignments": [],
                "unmatched_requirements": capability_requirements,
                "overall_confidence": 0.3,
            }

    async def _build_workflow_from_assignments(
        self,
        agent_assignments: Dict,
        capability_requirements: List[Dict],
        context_analysis: Dict,
    ) -> Dict:
        """Build final workflow strategy from semantic assignments."""

        assigned_agents = []
        missing_capabilities = []

        # Extract assigned agents in order
        assignments = agent_assignments.get("agent_assignments", [])
        assignments.sort(key=lambda x: x.get("step_number", 0))

        for assignment in assignments:
            assigned_agents.append(assignment["assigned_agent"])

        # Handle unmatched requirements
        for unmatched in agent_assignments.get("unmatched_requirements", []):
            missing_capabilities.append(
                {
                    "capability": unmatched.get(
                        "suggested_agent_name", "unknown_capability"
                    ),
                    "priority": "high",
                    "description": unmatched.get("required_description", ""),
                    "step_number": unmatched.get("step_number", 0),
                }
            )

        # Determine execution strategy
        execution_strategy = "sequential"  # Default for data flow
        if len(assigned_agents) > 3 and context_analysis.get("complexity") == "simple":
            execution_strategy = "parallel"

        # Build rationale from AI reasoning
        reasoning_parts = []
        for assignment in assignments:
            reasoning_parts.append(
                f"Step {assignment['step_number']}: {assignment['reasoning']}"
            )

        return {
            "agent_sequence": assigned_agents,
            "execution_strategy": execution_strategy,
            "rationale": (
                " | ".join(reasoning_parts)
                if reasoning_parts
                else "Semantic agent matching completed"
            ),
            "step_descriptions": [
                f"Step {req['step_number']}: {req['detailed_description']}"
                for req in capability_requirements
            ],
            "missing_capabilities": missing_capabilities,
            "complexity": context_analysis.get("complexity", "medium"),
            "confidence": agent_assignments.get("overall_confidence", 0.7),
            "estimated_duration": "30-60 seconds",
            "semantic_matching": True,
            "capability_requirements": capability_requirements,
            "agent_assignments": assignments,
        }

    async def _design_data_flow(
        self, workflow_strategy: Dict, context_analysis: Dict
    ) -> Dict:
        """Design how data flows between workflow steps."""

        agent_sequence = workflow_strategy.get("agent_sequence", [])

        if len(agent_sequence) <= 1:
            return {"flow_type": "single_step", "steps": []}

        prompt = f"""
        Design data flow for this multi-agent workflow:
        
        WORKFLOW: {json.dumps(workflow_strategy, indent=2)}
        CONTEXT: {json.dumps(context_analysis, indent=2)}
        
        AGENT SEQUENCE: {agent_sequence}
        
        DATA FLOW DESIGN:
        
        For each step transition, specify:
        1. **INPUT**: What data does this agent receive?
        2. **PROCESSING**: What does this agent do with the data?
        3. **OUTPUT**: What data does this agent produce?
        4. **TRANSFORMATION**: How is data shaped for the next agent?
        5. **CONTEXT**: What context does the next agent need?
        
        Return JSON:
        {{
            "flow_type": "sequential|parallel|hybrid",
            "data_transformations": [
                {{
                    "from_agent": "agent1",
                    "to_agent": "agent2", 
                    "data_passed": "analysis results, processed data",
                    "transformation_needed": "format for next step",
                    "context_preserved": "original request, workflow goals"
                }}
            ],
            "state_management": {{
                "preserve_original_data": true,
                "accumulate_results": true,
                "pass_full_context": true
            }},
            "error_handling": {{
                "rollback_strategy": "partial|full",
                "recovery_options": ["retry", "skip", "alternative_agent"]
            }}
        }}
        """

        response = self.openai_client.chat.completions.create(
            model=ORCHESTRATOR_MODEL,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            max_completion_tokens=1000,
        )

        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            return {
                "flow_type": "sequential",
                "data_transformations": [],
                "state_management": {"preserve_original_data": True},
            }

    async def _create_agent_instructions(
        self, workflow_strategy: Dict, data_flow_plan: Dict, original_request: str
    ) -> Dict:
        """Create specific instructions for each agent in the workflow."""

        agent_sequence = workflow_strategy.get("agent_sequence", [])
        step_descriptions = workflow_strategy.get("step_descriptions", [])

        agent_instructions = {}

        for i, agent_name in enumerate(agent_sequence):
            instruction_prompt = f"""
            Create specific instructions for {agent_name} in this workflow:
            
            ORIGINAL REQUEST: {original_request}
            FULL WORKFLOW: {agent_sequence}
            AGENT POSITION: Step {i+1} of {len(agent_sequence)}
            STEP DESCRIPTION: {step_descriptions[i] if i < len(step_descriptions) else 'Process data'}
            
            WORKFLOW CONTEXT: {json.dumps(workflow_strategy, indent=2)}
            DATA FLOW: {json.dumps(data_flow_plan, indent=2)}
            
            Create specific instructions for this agent that include:
            1. **PRIMARY TASK**: What is this agent's main responsibility?
            2. **INPUT EXPECTATIONS**: What data/format will this agent receive?
            3. **PROCESSING FOCUS**: What specific processing should be emphasized?
            4. **OUTPUT REQUIREMENTS**: How should results be formatted for next step?
            5. **CONTEXT AWARENESS**: How does this fit into the larger workflow goal?
            
            Return JSON:
            {{
                "primary_task": "specific task for this agent",
                "input_expectations": "what this agent should expect to receive",
                "processing_focus": "key areas to focus on",
                "output_requirements": "how to format results",
                "context_awareness": "role in larger workflow",
                "success_criteria": "how to know if this step succeeded"
            }}
            """

            response = self.openai_client.chat.completions.create(
                model=ORCHESTRATOR_MODEL,
                messages=[{"role": "user", "content": instruction_prompt}],
                response_format={"type": "json_object"},
                max_completion_tokens=800,
            )

            try:
                agent_instructions[agent_name] = json.loads(
                    response.choices[0].message.content
                )
            except json.JSONDecodeError:
                agent_instructions[agent_name] = {
                    "primary_task": f"Process data for {agent_name}",
                    "context_awareness": f"Step {i+1} in workflow",
                }

        return agent_instructions

    def get_planning_metadata(self) -> Dict:
        """Get metadata about the planning process."""
        return {
            "planner_type": "ai_driven",
            "model_used": ORCHESTRATOR_MODEL,
            "planning_features": [
                "intelligent_context_analysis",
                "strategic_workflow_planning",
                "data_flow_design",
                "agent_specific_instructions",
            ],
            "capabilities": [
                "multi_step_reasoning",
                "capability_gap_detection",
                "optimal_sequence_planning",
                "context_aware_execution",
            ],
        }
