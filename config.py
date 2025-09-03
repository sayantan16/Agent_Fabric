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
# GENERATION CONSTRAINTS
# =============================================================================

# Agent Constraints
MIN_AGENT_LINES = 50
MAX_AGENT_LINES = 300
AGENT_TIMEOUT_SECONDS = 10  # Max execution time for any agent

# Tool Constraints
MIN_TOOL_LINES = 15
MAX_TOOL_LINES = 100
TOOL_MUST_BE_PURE = True  # Tools must be pure functions (no side effects)

# =============================================================================
# SYSTEM PATHS
# =============================================================================

# Directory paths
GENERATED_AGENTS_DIR = "generated/agents"
GENERATED_TOOLS_DIR = "generated/tools"
CORE_DIR = "core"

# Registry paths
AGENTS_REGISTRY_PATH = "agents.json"
TOOLS_REGISTRY_PATH = "tools.json"

# =============================================================================
# LANGGRAPH CONFIGURATION
# =============================================================================

# Workflow settings
MAX_WORKFLOW_STEPS = 10  # Maximum agents in a single workflow
WORKFLOW_TIMEOUT_SECONDS = 60  # Total workflow execution timeout
ENABLE_PARALLEL_EXECUTION = False  # Start with sequential, add parallel later
MAX_RETRIES_PER_AGENT = 2  # Retry failed agents

# State management
STATE_CHECKPOINT_ENABLED = True  # Save state between agent executions
STATE_VERBOSE_LOGGING = True  # Detailed logging for debugging

# =============================================================================
# UI CONFIGURATION
# =============================================================================

# Streamlit settings
UI_TITLE = "Agentic Fabric POC"
UI_THEME = "light"
MAX_FILE_UPLOAD_SIZE_MB = 10
SUPPORTED_FILE_TYPES = ["txt", "pdf", "csv", "json", "xlsx"]

# Display settings
SHOW_AGENT_EXECUTION_TIME = True
SHOW_WORKFLOW_VISUALIZATION = True
SHOW_GENERATED_CODE = False  # Show the actual generated code in UI (debug mode)

# =============================================================================
# VALIDATION SETTINGS
# =============================================================================

# Code validation
VALIDATE_SYNTAX_BEFORE_SAVE = True
VALIDATE_IMPORTS = True  # Check that imports are from allowed list
TEST_GENERATED_CODE = True  # Run basic tests on generated code

# Allowed imports for generated code (security)
ALLOWED_IMPORTS = [
    "re",
    "json",
    "datetime",
    "math",
    "statistics",
    "pandas",
    "numpy",  # Data processing
    "PyPDF2",
    "pdfplumber",  # PDF processing
    "csv",
    "openpyxl",  # File processing
    "urllib.parse",
    "base64",
    "hashlib",  # Utilities
    "collections",
    "itertools",
    "functools",  # Python utilities
]


# =============================================================================
# EXAMPLE TEMPLATES
# =============================================================================

# These help Claude understand the expected structure

EXAMPLE_TOOL_TEMPLATE = '''def extract_numbers(text):
    """Extract all numbers from text - both integers and decimals."""
    import re
    
    if not text:
        return []
    
    # Find all numeric patterns
    patterns = [
        r'-?\d+\.?\d*',  # Regular numbers (integers and decimals)
        r'-?\.\d+'       # Numbers starting with decimal point
    ]
    
    numbers = []
    for pattern in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            try:
                # Try to convert to float
                num = float(match)
                numbers.append(num)
            except ValueError:
                continue
    
    # Remove duplicates while preserving order
    seen = set()
    unique_numbers = []
    for num in numbers:
        if num not in seen:
            seen.add(num)
            unique_numbers.append(num)
    
    return unique_numbers
'''

EXAMPLE_AGENT_TEMPLATE = '''def calculate_statistics_agent(state):
    """Agent that calculates basic statistics from numbers in text or data."""
    import sys
    import os
    from datetime import datetime
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from generated.tools.extract_numbers import extract_numbers
    from generated.tools.calculate_mean import calculate_mean
    from generated.tools.calculate_median import calculate_median
    
    try:
        # CRITICAL: Initialize state components if missing
        if 'results' not in state:
            state['results'] = {}
        if 'errors' not in state:
            state['errors'] = []
        if 'execution_path' not in state:
            state['execution_path'] = []
            
        # CRITICAL: Flexible input handling - check multiple possible data locations
        current_data = state.get('current_data', {})
        numbers = []
        
        # Handle various input formats
        if isinstance(current_data, dict):
            # Check for pre-processed numbers from previous agent
            if 'numbers' in current_data:
                numbers = current_data['numbers']
            # Check for text field in dict
            elif 'text' in current_data:
                numbers = extract_numbers(current_data['text'])
            # Check for data field
            elif 'data' in current_data:
                if isinstance(current_data['data'], str):
                    numbers = extract_numbers(current_data['data'])
                elif isinstance(current_data['data'], list):
                    numbers = current_data['data']
        elif isinstance(current_data, str):
            # Direct string input
            numbers = extract_numbers(current_data)
        elif isinstance(current_data, list):
            # Direct list of numbers
            numbers = current_data
        
        # Fallback to checking root state for text
        if not numbers and 'text' in state:
            numbers = extract_numbers(state['text'])
        
        # Process the numbers
        if numbers and len(numbers) > 0:
            mean = calculate_mean(numbers)
            median = calculate_median(numbers)
            
            result = {
                "status": "success",
                "data": {
                    "numbers_found": len(numbers),
                    "numbers": numbers[:10],  # First 10 for preview
                    "statistics": {
                        "mean": round(mean, 2),
                        "median": median,
                        "min": min(numbers),
                        "max": max(numbers),
                        "sum": sum(numbers)
                    }
                },
                "metadata": {
                    "agent": "calculate_statistics",
                    "tools_used": ["extract_numbers", "calculate_mean", "calculate_median"],
                    "execution_time": 0.3
                }
            }
        else:
            result = {
                "status": "warning",
                "data": {
                    "message": "No numbers found in input",
                    "numbers_found": 0
                },
                "metadata": {
                    "agent": "calculate_statistics",
                    "tools_used": ["extract_numbers"],
                    "execution_time": 0.1
                }
            }
        
        # CRITICAL: Always update state properly
        state['results']['calculate_statistics'] = result
        state['current_data'] = result['data']
        state['execution_path'].append('calculate_statistics')
        
    except Exception as e:
        # CRITICAL: Proper error handling
        state['errors'].append({
            "agent": "calculate_statistics",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        })
        
        # Still update results with error status
        state['results']['calculate_statistics'] = {
            "status": "error",
            "data": None,
            "metadata": {
                "agent": "calculate_statistics",
                "error": str(e)
            }
        }
    
    return state
'''

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
