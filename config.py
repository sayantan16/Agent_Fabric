"""
Agentic Fabric Configuration - REFINED VERSION
Complete configuration for dynamic agent orchestration
"""

import os
from dotenv import load_dotenv

load_dotenv()

# =============================================================================
# API CONFIGURATION
# =============================================================================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ORCHESTRATOR_MODEL = "gpt-4-turbo-preview"  # Better for JSON
ORCHESTRATOR_TEMPERATURE = 0.2

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CLAUDE_MODEL = "claude-3-haiku-20240307"
CLAUDE_TEMPERATURE = 0.1

# =============================================================================
# ORCHESTRATOR PROMPTS - CRITICAL FOR CONTROL
# =============================================================================

ORCHESTRATOR_ANALYSIS_PROMPT = """You are the master orchestrator of a multi-agent system.
Analyze the user's request and determine:
1. What agents are needed (check available list)
2. What workflow pattern to use
3. What data transformations are needed
4. Whether new capabilities need to be created

User Request: {request}
Files Provided: {files}

Available Agents:
{available_agents}

Available Tools:
{available_tools}

IMPORTANT WORKFLOW PATTERNS:
- Sequential: agent1 -> agent2 -> agent3
- Parallel: agent1 & agent2 -> merge -> agent3
- Conditional: if condition -> agentA else -> agentB
- Loop: repeat agent until condition met

Output a detailed analysis (not JSON yet)."""

ORCHESTRATOR_PLANNING_PROMPT = """Based on this analysis, create a workflow plan.

Analysis: {analysis}

CRITICAL: Output ONLY valid JSON with this EXACT structure:
{{
    "workflow_type": "sequential|parallel|conditional",
    "workflow_steps": [
        {{
            "step_id": "step_1",
            "agent": "agent_name",
            "inputs": ["source of input"],
            "outputs": ["what it produces"],
            "condition": null or "condition for conditional nodes"
        }}
    ],
    "data_flow": {{
        "step_1": {{"source": "input", "transforms": []}},
        "step_2": {{"source": "step_1.output", "transforms": []}}
    }},
    "missing_capabilities": {{
        "agents": [{{"name": "agent_name", "purpose": "what it does", "tools_needed": []}}],
        "tools": [{{"name": "tool_name", "purpose": "what it does", "type": "pure_function"}}]
    }},
    "expected_output": "description of final output",
    "reasoning": "why this workflow"
}}"""

ORCHESTRATOR_SYNTHESIS_PROMPT = """Synthesize the workflow results into a coherent response.

Original Request: {request}
Workflow Executed: {workflow}
Results from Each Agent: {results}

Create a natural language response that:
1. Directly answers the user's question
2. Highlights key findings
3. Explains any issues encountered
4. Suggests next steps if applicable

Keep it concise but complete."""

# =============================================================================
# AGENT GENERATION PROMPTS - FOR FLEXIBILITY
# =============================================================================

CLAUDE_AGENT_GENERATION_PROMPT = """Create a Python agent function that is UNIVERSALLY FLEXIBLE.

MANDATORY STRUCTURE:
```python
def {agent_name}_agent(state):
    '''Agent: {description}'''
    import sys
    import os
    from datetime import datetime
    
    # CRITICAL: Dynamic imports with fallback
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    tools_available = []
    {tool_imports}
    
    # MANDATORY: State initialization
    if 'results' not in state:
        state['results'] = {{}}
    if 'errors' not in state:
        state['errors'] = []
    if 'execution_path' not in state:
        state['execution_path'] = []
    if 'metadata' not in state:
        state['metadata'] = {{}}
    
    try:
        # MANDATORY: Universal input extraction
        data_to_process = None
        
        # Priority 1: Check current_data (can be ANY type)
        current = state.get('current_data')
        
        if current is not None:
            if isinstance(current, str):
                data_to_process = current
            elif isinstance(current, dict):
                # Try multiple keys
                for key in ['text', 'data', 'content', 'value', 'output', 'result']:
                    if key in current:
                        data_to_process = current[key]
                        break
                if data_to_process is None:
                    data_to_process = current  # Use whole dict
            elif isinstance(current, (list, tuple)):
                data_to_process = current
            else:
                data_to_process = str(current)
        
        # Priority 2: Check previous agent results
        if data_to_process is None and 'results' in state:
            for agent_result in reversed(list(state['results'].values())):
                if isinstance(agent_result, dict) and 'data' in agent_result:
                    data_to_process = agent_result['data']
                    break
        
        # Priority 3: Check root state
        if data_to_process is None:
            for key in ['text', 'data', 'input', 'request', 'content']:
                if key in state and state[key]:
                    data_to_process = state[key]
                    break
        
        # AGENT SPECIFIC LOGIC HERE
        {agent_logic}
        
        # MANDATORY: Structured output
        result = {{
            "status": "success",
            "data": processed_data,  # Must be consumable by next agent
            "raw_input": data_to_process,  # Preserve original
            "metadata": {{
                "agent": "{agent_name}",
                "tools_used": tools_available,
                "execution_time": 0.1,
                "data_type": type(processed_data).__name__
            }}
        }}
        
        # MANDATORY: State updates
        state['results']['{agent_name}'] = result
        state['current_data'] = result['data']  # Pass processed data
        state['execution_path'].append('{agent_name}')
        
    except Exception as e:
        import traceback
        state['errors'].append({{
            "agent": "{agent_name}",
            "error": str(e),
            "traceback": traceback.format_exc(),
            "timestamp": datetime.now().isoformat()
        }})
        
        # Graceful failure
        state['results']['{agent_name}'] = {{
            "status": "error",
            "data": None,
            "error": str(e)
        }}
    
    return state
Requirements:

Agent Name: {agent_name}
Description: {description}
Tools Needed: {tools}
Input: {input_desc}
Output: {output_desc}
Steps: {workflow_steps}
"""
CLAUDE_TOOL_GENERATION_PROMPT = """Create a PURE Python function that handles ANY input gracefully.
MANDATORY STRUCTURE:
pythondef {tool_name}(input_data=None):
    '''Tool: {description}'''
    {imports}
    
    # MANDATORY: Handle None
    if input_data is None:
        return {default_return}
    
    # MANDATORY: Type flexibility
    processed_input = None
    
    if isinstance(input_data, str):
        processed_input = input_data
    elif isinstance(input_data, dict):
        # Extract from dict
        for key in ['text', 'data', 'value', 'content']:
            if key in input_data:
                processed_input = input_data[key]
                break
    elif isinstance(input_data, (list, tuple)):
        processed_input = input_data
    else:
        try:
            processed_input = str(input_data)
        except:
            return {default_return}
    
    # TOOL LOGIC HERE
    try:
        {tool_logic}
        return result
    except Exception as e:
        # NEVER raise, always return default
        return {default_return}
Requirements:

Tool Name: {tool_name}
Purpose: {description}
Input: {input_desc}
Output: {output_desc}
Default Return: {default_return}
"""

# =============================================================================
# VALIDATION RULES
# =============================================================================

AGENT_VALIDATION_RULES = {
    "required_patterns": [
        "if 'results' not in state:",
        "state.get('current_data')",
        "isinstance(current",
        "for key in [",
        "state['results'][",
        "state['current_data'] =",
        "except Exception as e:",
        "data_to_process = None",
    ],
    "forbidden_patterns": [
        "raise Exception",
        "raise Error",
        "sys.exit",
        "quit()",
        "assert False",
    ],
}

TOOL_VALIDATION_RULES = {
    "required_patterns": [
        "if input_data is None:",
        "isinstance(input_data",
        "try:",
        "except",
        "return",
    ],
    "forbidden_patterns": ["raise", "assert", "open(", "requests.", "file("],
}
