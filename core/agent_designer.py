"""
Intelligent Agent Designer - GPT-4 designs optimal agent architectures
"""

import json
import openai
from typing import Dict, List
from config import OPENAI_API_KEY, ORCHESTRATOR_MODEL


class IntelligentAgentDesigner:
    """GPT-4 designs complete agent specifications"""

    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

    async def design_agent_architecture(
        self, agent_requirement: Dict, context: Dict
    ) -> Dict:
        """GPT-4 creates detailed agent specification"""

        design_prompt = f"""
        INTELLIGENT AGENT ARCHITECTURE DESIGN
        
        AGENT REQUIREMENT:
        {json.dumps(agent_requirement, indent=2)}
        
        SYSTEM CONTEXT:
        - Available Tools: {context.get('available_tools', [])}
        - Existing Agents: {context.get('existing_agents', [])}
        - File Types: {context.get('file_types', [])}
        - User Request Context: {context.get('user_request', '')}
        
        DESIGN SPECIFICATIONS:
        
        1. INPUT ANALYSIS:
           - What data formats will this agent receive?
           - How should it extract/parse input data?
           - What edge cases must be handled?
        
        2. PROCESSING DESIGN:
           - What core algorithms/logic are needed?
           - Which existing tools can be reused?
           - What new tools need to be created?
           - How should errors be handled?
        
        3. OUTPUT SPECIFICATION:
           - What format should results be in?
           - How should output integrate with other agents?
           - What metadata should be included?
        
        4. INTEGRATION STRATEGY:
           - How does this agent fit in workflows?
           - What data does it need from previous agents?
           - What data should it pass to next agents?
        
        RESPONSE FORMAT (JSON):
        {{
            "agent_specification": {{
                "name": "precise_descriptive_name",
                "description": "clear_purpose_statement",
                "category": "data_processing|analysis|transformation|integration|validation",
                "complexity": "simple|moderate|complex"
            }},
            "input_design": {{
                "primary_inputs": ["input_type_1", "input_type_2"],
                "input_sources": ["files", "previous_agents", "user_request"],
                "parsing_requirements": ["requirement1", "requirement2"],
                "validation_rules": ["rule1", "rule2"]
            }},
            "processing_design": {{
                "core_algorithms": ["algorithm1", "algorithm2"],
                "existing_tools_needed": ["tool1", "tool2"],
                "new_tools_required": [
                    {{"name": "tool_name", "purpose": "tool_purpose", "complexity": "simple|complex"}}
                ],
                "error_handling": ["scenario1", "scenario2"],
                "performance_requirements": "fast|standard|thorough"
            }},
            "output_design": {{
                "output_format": "json|text|file|structured_data",
                "output_schema": {{
                    "field1": "description",
                    "field2": "description"
                }},
                "metadata_included": ["execution_time", "confidence_score", "data_quality"],
                "next_agent_compatibility": "description"
            }},
            "integration_design": {{
                "workflow_position": "first|middle|last|flexible",
                "dependencies": ["agent1", "agent2"],
                "data_flow": "how_data_moves_through_agent",
                "parallel_execution_safe": true/false
            }},
            "claude_prompt_design": {{
                "analysis_prompt": "prompt for Claude to analyze input",
                "processing_prompt": "prompt for Claude to process data", 
                "output_prompt": "prompt for Claude to format results"
            }}
        }}
        """

        response = self.openai_client.chat.completions.create(
            model=ORCHESTRATOR_MODEL,
            messages=[{"role": "user", "content": design_prompt}],
            response_format={"type": "json_object"},
        )

        return json.loads(response.choices[0].message.content)
