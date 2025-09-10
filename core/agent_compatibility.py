"""
Agent Compatibility Analyzer - GPT-4 Powered
Analyzes compatibility between pipeline steps and existing agents using AI intelligence
"""

import os
import sys
import json
import asyncio
from typing import Dict, List, Optional, Any, Tuple
import openai

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.registry import RegistryManager
from config import OPENAI_API_KEY, ORCHESTRATOR_MODEL, ORCHESTRATOR_MAX_TOKENS


class AgentCompatibilityAnalyzer:
    """
    AI-powered compatibility analyzer that uses GPT-4 to understand and match
    agents to pipeline steps without any hardcoded logic.
    """

    def __init__(self, registry: RegistryManager):
        """Initialize with registry manager and OpenAI client."""
        self.registry = registry
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)

    async def find_compatible_agents(self, step: Dict) -> List[Dict]:
        """
        Find existing agents compatible with a pipeline step using GPT-4 intelligence.

        Args:
            step: Pipeline step specification with requirements

        Returns:
            List of compatible agents, sorted by AI-determined compatibility
        """
        print(
            f"DEBUG: Finding compatible agents for step: {step.get('name', 'unnamed')}"
        )

        available_agents = self.registry.list_agents(active_only=True)

        if not available_agents:
            print("DEBUG: No available agents found")
            return []

        # Use GPT-4 to intelligently analyze and rank agents
        analysis_prompt = f"""
You are an expert AI system analyzer. Your task is to evaluate which existing agents can best handle a specific pipeline step.

PIPELINE STEP TO HANDLE:
Name: {step.get('name', 'unknown')}
Description: {step.get('description', 'No description provided')}
Input Requirements: {json.dumps(step.get('input_requirements', {}), indent=2)}
Output Requirements: {json.dumps(step.get('output_requirements', {}), indent=2)}
Required Capabilities: {step.get('required_capabilities', [])}
Required Tools: {step.get('required_tools', [])}

AVAILABLE AGENTS TO EVALUATE:
{self._format_agents_for_analysis(available_agents)}

ANALYSIS INSTRUCTIONS:
1. Carefully read and understand what the pipeline step needs to accomplish
2. For each agent, analyze:
   - How well the agent's description matches the step requirements
   - Whether the agent's tools can handle the required processing
   - If the agent's capabilities align with what's needed
   - Any potential limitations or mismatches
3. Assign a compatibility score from 0.0 to 1.0 where:
   - 1.0 = Perfect match, agent can definitely handle this step
   - 0.8-0.9 = Excellent match with minor considerations
   - 0.6-0.7 = Good match, should work well
   - 0.4-0.5 = Moderate match, might work with some adaptation
   - 0.2-0.3 = Poor match, significant limitations
   - 0.0-0.1 = No match, agent cannot handle this step
4. Only include agents with score >= 0.3
5. Provide clear reasoning for each score

RESPOND WITH VALID JSON:
{{
    "analysis": {{
        "step_understanding": "What this step needs to accomplish",
        "key_requirements": ["requirement1", "requirement2"],
        "evaluation_criteria": ["criteria1", "criteria2"]
    }},
    "compatible_agents": [
        {{
            "name": "agent_name",
            "compatibility_score": 0.95,
            "reasoning": "Detailed explanation of why this agent matches",
            "strengths": ["strength1", "strength2"],
            "potential_issues": ["issue1", "issue2"],
            "confidence": "high|medium|low"
        }}
    ],
    "recommendation": {{
        "best_agent": "agent_name",
        "alternative_agents": ["agent2", "agent3"],
        "creation_needed": false,
        "notes": "Additional recommendations"
    }}
}}
"""

        try:
            response = self.client.chat.completions.create(
                model=ORCHESTRATOR_MODEL,
                max_completion_tokens=ORCHESTRATOR_MAX_TOKENS,
                messages=[{"role": "user", "content": analysis_prompt}],
            )

            content = response.choices[0].message.content

            # Extract and parse JSON
            analysis_result = self._extract_json_from_response(content)

            if not analysis_result:
                raise ValueError("Failed to parse GPT-4 response")

            # Convert to expected format
            compatible_agents = []
            agent_names = [a["name"] for a in available_agents]

            for agent_analysis in analysis_result.get("compatible_agents", []):
                agent_name = agent_analysis.get("name")
                compatibility_score = agent_analysis.get("compatibility_score", 0.0)

                # Find the actual agent data
                agent_data = next(
                    (a for a in available_agents if a["name"] == agent_name), None
                )

                if agent_data and compatibility_score >= 0.3:
                    agent_with_score = agent_data.copy()
                    agent_with_score["compatibility_score"] = compatibility_score
                    agent_with_score["ai_analysis"] = agent_analysis
                    compatible_agents.append(agent_with_score)

                    print(
                        f"DEBUG: Agent '{agent_name}' compatible with score: {compatibility_score:.2f}"
                    )
                    print(
                        f"DEBUG: Reasoning: {agent_analysis.get('reasoning', 'No reasoning provided')}"
                    )

            # Sort by compatibility score (highest first)
            compatible_agents.sort(key=lambda x: x["compatibility_score"], reverse=True)

            print(f"DEBUG: Found {len(compatible_agents)} compatible agents")
            return compatible_agents

        except Exception as e:
            print(
                f"DEBUG: GPT-4 agent analysis failed: {str(e)}, falling back to basic matching"
            )
            return self._emergency_fallback_matching(step, available_agents)

    async def find_compatible_agents_with_code_analysis(
        self, step: Dict, previous_step_output: Any = None
    ) -> List[Dict]:
        """
        Enhanced compatibility analysis that examines agent code and data flow.
        """
        print(f"DEBUG: Enhanced analysis for step: {step.get('name', 'unnamed')}")

        available_agents = self.registry.list_agents(active_only=True)

        if not available_agents:
            return []

        # Enhanced analysis prompt
        analysis_prompt = f"""
    You are an expert code analyzer. Evaluate agents by examining their actual code capabilities.

    PIPELINE STEP:
    Name: {step.get('name', 'unknown')}
    Description: {step.get('description', 'No description')}
    Expected Input Type: {type(previous_step_output).__name__ if previous_step_output is not None else 'text'}
    Input Sample: {str(previous_step_output)[:200] if previous_step_output else 'text input'}

    AGENTS WITH CODE ANALYSIS:
    {self._format_agents_with_code_analysis(available_agents)}

    ANALYSIS REQUIREMENTS:
    1. **Code Inspection**: Examine actual agent code for:
    - Input data type handling (string, dict, list, etc.)
    - Error handling capabilities
    - State management (pipeline context)
    - Tool usage patterns

    2. **Data Flow Compatibility**: Verify agent can:
    - Accept the expected input data type
    - Process pipeline state correctly
    - Return appropriate output format

    3. **Execution Context**: Check if agent:
    - Works in pipeline mode
    - Handles state dict properly
    - Has robust error handling

    SCORING (0.0 to 1.0):
    - 1.0: Perfect code match for this scenario
    - 0.8-0.9: Excellent with minor considerations
    - 0.6-0.7: Good, likely to work
    - 0.4-0.5: Moderate, needs adaptation
    - 0.2-0.3: Poor, significant issues
    - 0.0-0.1: Will definitely fail

    RESPOND WITH JSON:
    {{
        "compatible_agents": [
            {{
                "name": "agent_name",
                "compatibility_score": 0.95,
                "code_analysis": {{
                    "input_handling": "how agent handles input types",
                    "expected_data_type": "what agent expects",
                    "pipeline_compatibility": "how well it works in pipeline",
                    "error_scenarios": ["potential issues"],
                    "adaptation_needed": "none|minor|major"
                }},
                "reasoning": "detailed explanation",
                "confidence": "high|medium|low"
            }}
        ]
    }}
    """

        try:
            response = self.client.chat.completions.create(
                model=ORCHESTRATOR_MODEL,
                max_completion_tokens=ORCHESTRATOR_MAX_TOKENS,
                messages=[{"role": "user", "content": analysis_prompt}],
            )

            analysis_result = self._extract_json_from_response(
                response.choices[0].message.content
            )

            if analysis_result:
                return self._process_enhanced_compatibility_results(
                    analysis_result, available_agents
                )

        except Exception as e:
            print(f"DEBUG: Enhanced analysis failed: {str(e)}")

        # Fallback to basic analysis
        return await self.find_compatible_agents(step)

    def _format_agents_with_code_analysis(self, agents: List[Dict]) -> str:
        """Format agents with their actual code for GPT-4 analysis."""
        formatted = []

        for agent in agents[:5]:  # Limit to 5 agents to avoid prompt overflow
            name = agent.get("name", "unknown")
            desc = agent.get("description", "No description")
            location = agent.get("location", "")

            formatted.append(f"AGENT: {name}")
            formatted.append(f"Description: {desc}")
            formatted.append(f"Tools: {agent.get('uses_tools', [])}")

            # Read actual agent code
            try:
                if location:
                    # Handle relative paths
                    if not os.path.isabs(location):
                        current_dir = os.getcwd()
                        if current_dir.endswith("flask_app"):
                            project_root = os.path.dirname(current_dir)
                        else:
                            project_root = current_dir
                        location = os.path.join(project_root, location)

                    if os.path.exists(location):
                        with open(location, "r") as f:
                            code = f.read()
                            # Include relevant code sections
                            formatted.append(f"Code Preview:")
                            formatted.append(f"```python")
                            formatted.append(code[:1000])  # First 1000 chars
                            if len(code) > 1000:
                                formatted.append("... [code continues]")
                            formatted.append(f"```")
                    else:
                        formatted.append("Code: File not found")
                else:
                    formatted.append("Code: Location not specified")
            except Exception as e:
                formatted.append(f"Code: Error reading - {str(e)}")

            formatted.append("")  # Empty line

        return "\n".join(formatted)

    def _process_enhanced_compatibility_results(
        self, analysis_result: Dict, available_agents: List[Dict]
    ) -> List[Dict]:
        """Process enhanced compatibility analysis results."""
        compatible_agents = []

        for agent_analysis in analysis_result.get("compatible_agents", []):
            agent_name = agent_analysis.get("name")
            compatibility_score = agent_analysis.get("compatibility_score", 0.0)

            if compatibility_score >= 0.3:
                agent_data = next(
                    (a for a in available_agents if a["name"] == agent_name), None
                )

                if agent_data:
                    agent_with_analysis = agent_data.copy()
                    agent_with_analysis["compatibility_score"] = compatibility_score
                    agent_with_analysis["enhanced_analysis"] = agent_analysis
                    compatible_agents.append(agent_with_analysis)

                    print(
                        f"DEBUG: Enhanced - Agent '{agent_name}' score: {compatibility_score:.2f}"
                    )
                    print(
                        f"DEBUG: Adaptation needed: {agent_analysis.get('code_analysis', {}).get('adaptation_needed', 'unknown')}"
                    )

        compatible_agents.sort(key=lambda x: x["compatibility_score"], reverse=True)
        return compatible_agents

    def _format_agents_for_analysis(self, agents: List[Dict]) -> str:
        """Format agents with all relevant information for GPT-4 analysis."""
        formatted = []

        for i, agent in enumerate(agents, 1):
            name = agent.get("name", "unknown")
            desc = agent.get("description", "No description provided")
            uses_tools = agent.get("uses_tools", [])
            capabilities = agent.get("capabilities", [])
            input_format = agent.get("input_format", {})
            output_format = agent.get("output_format", {})
            status = agent.get("status", "unknown")

            formatted.append(f"AGENT {i}: {name}")
            formatted.append(f"  Description: {desc}")

            if uses_tools:
                formatted.append(f"  Tools Available: {', '.join(uses_tools)}")

            if capabilities:
                formatted.append(f"  Capabilities: {', '.join(capabilities)}")

            if input_format:
                formatted.append(f"  Input Format: {json.dumps(input_format)}")

            if output_format:
                formatted.append(f"  Output Format: {json.dumps(output_format)}")

            formatted.append(f"  Status: {status}")
            formatted.append("")  # Empty line for readability

        return "\n".join(formatted)

    def _extract_json_from_response(self, content: str) -> Optional[Dict]:
        """Extract JSON from GPT-4 response with multiple fallback strategies."""
        try:
            # Strategy 1: Look for JSON code blocks
            if "```json" in content:
                start = content.find("```json") + 7
                end = content.find("```", start)
                if end > start:
                    json_content = content[start:end].strip()
                    return json.loads(json_content)

            # Strategy 2: Look for JSON object boundaries
            if "{" in content and "}" in content:
                start = content.find("{")
                end = content.rfind("}") + 1
                if end > start:
                    json_content = content[start:end].strip()
                    return json.loads(json_content)

            # Strategy 3: Try parsing entire content
            return json.loads(content.strip())

        except json.JSONDecodeError as e:
            print(f"DEBUG: JSON parsing failed: {str(e)}")
            print(f"DEBUG: Content was: {content[:200]}...")
            return None

    def _emergency_fallback_matching(
        self, step: Dict, available_agents: List[Dict]
    ) -> List[Dict]:
        """Emergency fallback using basic name/description matching."""
        print("DEBUG: Using emergency fallback matching")

        step_name = step.get("name", "").lower()
        step_desc = step.get("description", "").lower()

        compatible_agents = []

        for agent in available_agents:
            agent_name = agent.get("name", "").lower()
            agent_desc = agent.get("description", "").lower()

            score = 0.0

            # Check for direct name component matches
            step_words = step_name.replace("_", " ").split()
            agent_words = agent_name.replace("_", " ").split()

            name_matches = len(set(step_words) & set(agent_words))
            if name_matches > 0:
                score += 0.4 * (name_matches / max(len(step_words), 1))

            # Check for description keyword matches
            if step_desc and agent_desc:
                step_keywords = set(step_desc.split())
                agent_keywords = set(agent_desc.split())

                desc_matches = len(step_keywords & agent_keywords)
                if desc_matches > 0:
                    score += 0.3 * (desc_matches / max(len(step_keywords), 1))

            # Boost score for obvious matches
            if any(word in agent_name for word in step_words):
                score += 0.3

            if score >= 0.3:
                agent_with_score = agent.copy()
                agent_with_score["compatibility_score"] = min(score, 1.0)
                agent_with_score["ai_analysis"] = {
                    "reasoning": "Emergency fallback matching based on name similarity",
                    "confidence": "low",
                }
                compatible_agents.append(agent_with_score)

                print(f"DEBUG: Fallback - Agent '{agent['name']}' score: {score:.2f}")

        # Sort by score
        compatible_agents.sort(key=lambda x: x["compatibility_score"], reverse=True)

        return compatible_agents

    async def analyze_missing_capabilities(
        self, step: Dict, compatible_agents: List[Dict]
    ) -> Dict[str, Any]:
        """
        AI-powered analysis of missing capabilities and suggestions.

        Args:
            step: Pipeline step specification
            compatible_agents: List of compatible agents (may be empty)

        Returns:
            AI analysis of missing capabilities and suggestions
        """
        if compatible_agents:
            # Analyze the best available option
            best_agent = compatible_agents[0]
            ai_analysis = best_agent.get("ai_analysis", {})

            return {
                "has_compatible_agent": True,
                "recommended_agent": best_agent["name"],
                "compatibility_score": best_agent["compatibility_score"],
                "ai_reasoning": ai_analysis.get("reasoning", "No reasoning available"),
                "potential_issues": ai_analysis.get("potential_issues", []),
                "confidence": ai_analysis.get("confidence", "medium"),
                "missing_capabilities": [],
            }

        # No compatible agents - use AI to analyze what's missing
        return await self._ai_analyze_missing_capabilities(step)

    async def _ai_analyze_missing_capabilities(self, step: Dict) -> Dict[str, Any]:
        """Use GPT-4 to analyze what capabilities are missing for a step."""

        available_tools = self.registry.list_tools()

        analysis_prompt = f"""
You are an expert AI system analyzer. Analyze what capabilities are missing to handle this pipeline step.

PIPELINE STEP THAT NEEDS HANDLING:
Name: {step.get('name', 'unknown')}
Description: {step.get('description', 'No description provided')}
Requirements: {json.dumps(step.get('input_requirements', {}), indent=2)}

AVAILABLE TOOLS IN SYSTEM:
{self._format_tools_for_analysis(available_tools)}

ANALYSIS TASK:
1. Understand what capabilities are needed for this step
2. Identify what type of agent would be required
3. Determine what tools the agent would need
4. Suggest the agent specification
5. Assess creation priority and complexity

RESPOND WITH VALID JSON:
{{
    "missing_analysis": {{
        "step_requirements": ["requirement1", "requirement2"],
        "required_capabilities": ["capability1", "capability2"],
        "required_agent_type": "description of needed agent",
        "complexity_assessment": "low|medium|high"
    }},
    "suggested_agent": {{
        "name": "suggested_agent_name",
        "description": "what this agent should do",
        "required_tools": ["tool1", "tool2"],
        "capabilities": ["cap1", "cap2"],
        "priority": "low|medium|high"
    }},
    "alternatives": {{
        "modify_existing": "suggestions for modifying existing agents",
        "tool_creation": "what new tools might be needed",
        "workaround": "alternative approaches"
    }}
}}
"""

        try:
            response = self.client.chat.completions.create(
                model=ORCHESTRATOR_MODEL,
                max_completion_tokens=ORCHESTRATOR_MAX_TOKENS,
                messages=[{"role": "user", "content": analysis_prompt}],
            )

            content = response.choices[0].message.content
            analysis_result = self._extract_json_from_response(content)

            if analysis_result:
                return {
                    "has_compatible_agent": False,
                    "recommended_agent": None,
                    "ai_analysis": analysis_result,
                    "missing_capabilities": analysis_result.get(
                        "missing_analysis", {}
                    ).get("required_capabilities", []),
                    "suggested_tools": analysis_result.get("suggested_agent", {}).get(
                        "required_tools", []
                    ),
                    "creation_priority": analysis_result.get("suggested_agent", {}).get(
                        "priority", "medium"
                    ),
                    "complexity": analysis_result.get("missing_analysis", {}).get(
                        "complexity_assessment", "medium"
                    ),
                }

        except Exception as e:
            print(f"DEBUG: AI missing capabilities analysis failed: {str(e)}")

        # Fallback response
        return {
            "has_compatible_agent": False,
            "recommended_agent": None,
            "missing_capabilities": ["unknown_capability"],
            "suggested_tools": [],
            "creation_priority": "high",
            "ai_analysis": {"error": "Analysis failed, using fallback"},
        }

    def _format_tools_for_analysis(self, tools: List[Dict]) -> str:
        """Format available tools for GPT-4 analysis."""
        if not tools:
            return "No tools available"

        formatted = []
        for tool in tools[:20]:  # Limit to prevent prompt overflow
            name = tool.get("name", "unknown")
            desc = tool.get("description", "No description")
            formatted.append(f"- {name}: {desc}")

        if len(tools) > 20:
            formatted.append(f"... and {len(tools) - 20} more tools")

        return "\n".join(formatted)

    async def suggest_agent_modifications(
        self, step: Dict, agent: Dict
    ) -> Dict[str, Any]:
        """
        AI-powered suggestions for modifying agents to improve compatibility.

        Args:
            step: Pipeline step specification
            agent: Agent that needs modification

        Returns:
            AI-generated modification suggestions
        """

        modification_prompt = f"""
You are an expert AI system modifier. Analyze how to improve an agent's compatibility with a specific pipeline step.

PIPELINE STEP REQUIREMENTS:
Name: {step.get('name', 'unknown')}
Description: {step.get('description', 'No description provided')}
Requirements: {json.dumps(step.get('input_requirements', {}), indent=2)}

CURRENT AGENT TO MODIFY:
Name: {agent.get('name', 'unknown')}
Description: {agent.get('description', 'No description provided')}
Current Tools: {agent.get('uses_tools', [])}
Current Capabilities: {agent.get('capabilities', [])}

ANALYSIS TASK:
1. Identify specific gaps between agent capabilities and step requirements
2. Suggest concrete modifications to improve compatibility
3. Estimate the impact of each modification
4. Assess implementation difficulty

RESPOND WITH VALID JSON:
{{
    "compatibility_analysis": {{
        "current_score": 0.5,
        "potential_score": 0.9,
        "main_gaps": ["gap1", "gap2"]
    }},
    "suggested_modifications": [
        {{
            "type": "add_tool|enhance_capability|modify_description",
            "description": "what to modify",
            "impact": "low|medium|high",
            "difficulty": "easy|moderate|hard",
            "estimated_improvement": 0.2
        }}
    ],
    "implementation_plan": {{
        "priority_order": ["modification1", "modification2"],
        "estimated_time": "time estimate",
        "risk_assessment": "low|medium|high"
    }}
}}
"""

        try:
            response = self.client.chat.completions.create(
                model=ORCHESTRATOR_MODEL,
                max_completion_tokens=ORCHESTRATOR_MAX_TOKENS,
                messages=[{"role": "user", "content": modification_prompt}],
            )

            content = response.choices[0].message.content
            modification_result = self._extract_json_from_response(content)

            if modification_result:
                return {
                    "agent_name": agent["name"],
                    "ai_analysis": modification_result,
                    "current_compatibility": modification_result.get(
                        "compatibility_analysis", {}
                    ).get("current_score", 0.0),
                    "potential_compatibility": modification_result.get(
                        "compatibility_analysis", {}
                    ).get("potential_score", 0.0),
                    "suggested_changes": modification_result.get(
                        "suggested_modifications", []
                    ),
                    "implementation_plan": modification_result.get(
                        "implementation_plan", {}
                    ),
                    "estimated_improvement": sum(
                        mod.get("estimated_improvement", 0)
                        for mod in modification_result.get(
                            "suggested_modifications", []
                        )
                    ),
                }

        except Exception as e:
            print(f"DEBUG: AI modification analysis failed: {str(e)}")

        # Fallback response
        return {
            "agent_name": agent["name"],
            "current_compatibility": 0.0,
            "suggested_changes": [],
            "estimated_improvement": 0.0,
            "ai_analysis": {"error": "Analysis failed"},
        }
