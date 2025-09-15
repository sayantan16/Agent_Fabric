"""
Enhanced Capability Analyzer with Intelligent Agent Compatibility
File: core/capability_analyzer.py (ENHANCED VERSION)
"""

import json
from typing import Dict, List, Any
from config import OPENAI_API_KEY, ORCHESTRATOR_MODEL
import openai
from core.registry_singleton import get_shared_registry


class CapabilityAnalyzer:
    """GPT-4 analyzes requests and intelligently matches against existing agents"""

    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

    async def analyze_agent_compatibility(
        self, request: str, proposed_plan: Dict, files: List[Dict]
    ) -> Dict:
        """
        Intelligent analysis: Are the proposed agents actually suitable for this request?
        Returns compatibility analysis with confidence scores.
        """

        # Get complete agent registry data
        registry = get_shared_registry()
        all_agents = registry.agents.get("agents", {})

        # Extract proposed agents and their details
        proposed_agents = proposed_plan.get("agents", [])
        agent_details = {}

        for agent_name in proposed_agents:
            if agent_name in all_agents:
                agent_info = all_agents[agent_name]
                agent_details[agent_name] = {
                    "description": agent_info.get("description", ""),
                    "uses_tools": agent_info.get("uses_tools", []),
                    "tags": agent_info.get("tags", []),
                    "location": agent_info.get("location", ""),
                }

        # Get file context
        file_context = []
        if files:
            for file_info in files:
                file_context.append(
                    {
                        "type": file_info.get("type", "unknown"),
                        "structure": file_info.get("structure", {}),
                        "size": file_info.get("size", 0),
                    }
                )

        analysis_prompt = f"""
        INTELLIGENT AGENT COMPATIBILITY ANALYSIS
        
        USER REQUEST: "{request}"
        FILE CONTEXT: {json.dumps(file_context, indent=2)}
        
        PROPOSED WORKFLOW PLAN:
        {json.dumps(proposed_plan, indent=2)}
        
        COMPLETE AGENT REGISTRY:
        {json.dumps(all_agents, indent=2)}
        
        ANALYSIS OBJECTIVES:
        1. COMPATIBILITY ASSESSMENT: Are the proposed agents actually suitable for this specific request?
        2. CAPABILITY MATCHING: Do the agents' described capabilities align with request requirements?
        3. ALTERNATIVE EVALUATION: Are there better-suited agents available in the registry?
        4. GAP IDENTIFICATION: What capabilities are missing entirely?
        5. CONFIDENCE SCORING: How confident are we in the current assignment?
        
        EVALUATION CRITERIA:
        - Agent description relevance to request
        - Tool compatibility with required operations
        - Input/output format alignment
        - Specialization vs generic capability match
        - Past performance indicators (if available)
        
        RESPONSE FORMAT (JSON):
        {{
            "compatibility_analysis": {{
                "overall_confidence": 0.0-1.0,
                "recommendation": "use_proposed|find_alternatives|create_new|hybrid_approach",
                "reasoning": "detailed explanation of compatibility assessment"
            }},
            "agent_evaluations": [
                {{
                    "agent_name": "proposed_agent_name",
                    "compatibility_score": 0.0-1.0,
                    "strengths": ["strength1", "strength2"],
                    "limitations": ["limitation1", "limitation2"],
                    "suitability": "excellent|good|fair|poor|unsuitable"
                }}
            ],
            "better_alternatives": [
                {{
                    "agent_name": "alternative_agent_name", 
                    "compatibility_score": 0.0-1.0,
                    "why_better": "explanation of why this is more suitable"
                }}
            ],
            "missing_capabilities": [
                {{
                    "capability": "missing_capability_name",
                    "importance": "critical|important|nice_to_have",
                    "description": "what this capability would provide"
                }}
            ],
            "creation_recommendation": {{
                "should_create_new": true/false,
                "rationale": "why creation is/isn't recommended",
                "suggested_agents": [
                    {{
                        "agent_name": "suggested_name",
                        "purpose": "specific_capability_description",
                        "priority": "high|medium|low"
                    }}
                ]
            }}
        }}
        """

        response = self.openai_client.chat.completions.create(
            model=ORCHESTRATOR_MODEL,
            messages=[{"role": "user", "content": analysis_prompt}],
            response_format={"type": "json_object"},
        )

        return json.loads(response.choices[0].message.content)

    async def analyze_capability_gaps(
        self, request: str, current_plan: Dict, files: List[Dict]
    ) -> Dict:
        """Legacy method - kept for backward compatibility"""

        # If no agents proposed, do traditional gap analysis
        if not current_plan.get("agents"):
            return await self._traditional_gap_analysis(request, current_plan, files)

        # Otherwise, do intelligent compatibility analysis
        compatibility_result = await self.analyze_agent_compatibility(
            request, current_plan, files
        )

        # Convert to legacy format for existing integration
        return {
            "creation_required": compatibility_result["creation_recommendation"][
                "should_create_new"
            ],
            "gap_analysis": {
                "missing_capabilities": [
                    cap["capability"]
                    for cap in compatibility_result["missing_capabilities"]
                ],
                "capability_importance": {
                    cap["capability"]: cap["importance"]
                    for cap in compatibility_result["missing_capabilities"]
                },
                "current_limitations": compatibility_result["compatibility_analysis"][
                    "reasoning"
                ],
            },
            "agent_requirements": compatibility_result["creation_recommendation"][
                "suggested_agents"
            ],
            "rationale": compatibility_result["compatibility_analysis"]["reasoning"],
            "compatibility_analysis": compatibility_result,  # Include full analysis
        }

    async def _traditional_gap_analysis(
        self, request: str, current_plan: Dict, files: List[Dict]
    ) -> Dict:
        """Traditional gap analysis when no agents are proposed"""

        registry = get_shared_registry()
        all_agents = registry.agents.get("agents", {})

        analysis_prompt = f"""
        CAPABILITY GAP ANALYSIS - NO SUITABLE AGENTS FOUND
        
        USER REQUEST: "{request}"
        AVAILABLE AGENTS: {json.dumps(all_agents, indent=2)}
        FILE CONTEXT: {json.dumps([f.get("structure") for f in files] if files else [], indent=2)}
        
        Since no agents were initially selected, analyze what capabilities are needed
        and determine if any existing agents could actually handle this request.
        
        RESPONSE FORMAT (JSON):
        {{
            "creation_required": true/false,
            "gap_analysis": {{
                "missing_capabilities": ["capability1", "capability2"],
                "capability_importance": {{"capability1": "high", "capability2": "medium"}},
                "current_limitations": "description of what existing agents cannot do"
            }},
            "agent_requirements": [
                {{
                    "agent_name": "suggested_name",
                    "purpose": "specific_capability_description",
                    "priority": "high/medium/low"
                }}
            ],
            "rationale": "detailed explanation"
        }}
        """

        response = self.openai_client.chat.completions.create(
            model=ORCHESTRATOR_MODEL,
            messages=[{"role": "user", "content": analysis_prompt}],
            response_format={"type": "json_object"},
        )

        return json.loads(response.choices[0].message.content)
