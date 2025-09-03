"""
Agentic Fabric Configuration
Minimal configuration for POC - keeping it simple and focused
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# =============================================================================
# API CONFIGURATION
# =============================================================================

# OpenAI Configuration (Orchestrator)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ORCHESTRATOR_MODEL = "gpt-4"  # or "gpt-4-turbo-preview" for faster/cheaper
ORCHESTRATOR_TEMPERATURE = 0.3  # Lower = more deterministic planning

# Anthropic Configuration (Agent/Tool Creation)
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CLAUDE_MODEL = "claude-3-haiku-20240307"  # Fast and cheap for code generation
CLAUDE_TEMPERATURE = 0.2  # Lower = more consistent code generation

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
# ORCHESTRATOR PROMPTS
# =============================================================================

ORCHESTRATOR_SYSTEM_PROMPT = """You are an intelligent orchestrator for a multi-agent system.
Your job is to:
1. Understand user requests
2. Check available agents and tools in the registry
3. Plan workflows using available agents
4. Identify missing capabilities that need to be created
5. Output structured workflow plans

Always output valid JSON with this structure:
{
    "workflow_steps": ["agent1", "agent2", ...],
    "missing_agents": ["agent_name", ...],
    "missing_tools": ["tool_name", ...],
    "workflow_type": "sequential" or "parallel"
}
"""

CLAUDE_AGENT_GENERATION_PROMPT = """Generate a Python agent function following these EXACT requirements:

CRITICAL DATA HANDLING RULES:
1. NEVER assume data type - always check isinstance() for EVERY input
2. Handle these input scenarios:
   - Direct string: state['current_data'] = "text"
   - Dict with various keys: state['current_data'] = {"text": "...", "data": "...", "content": "..."}
   - List/Array: state['current_data'] = [1, 2, 3]
   - Nested structures: state['current_data'] = {"results": {"data": [...]}}
   - Previous agent output: state['current_data'] = {"emails": [...], "numbers": [...]}
   - Empty/None: state['current_data'] = None or {}

3. EXTRACTION PATTERN (MANDATORY):
   ```python
   # Try multiple extraction methods
   data_to_process = None
   
   # Method 1: Direct current_data
   if isinstance(state.get('current_data'), str):
       data_to_process = state['current_data']
   
   # Method 2: Dict with common keys
   elif isinstance(state.get('current_data'), dict):
       for key in ['text', 'data', 'content', 'output', 'result']:
           if key in state['current_data']:
               data_to_process = state['current_data'][key]
               break
   
   # Method 3: Previous agent's specific output
   elif 'results' in state:
       # Check last agent's output
       last_agent_output = list(state['results'].values())[-1] if state['results'] else {}
       # Extract data from there
   
   # Method 4: Root state fallback
   if not data_to_process:
       for key in ['text', 'request', 'input']:
           if key in state:
               data_to_process = state[key]
               break

OUTPUT CONSISTENCY:

ALWAYS output a dict that can be consumed by any next agent
Include both processed and raw data
Add metadata about what was processed


IMPORTS MUST BE DYNAMIC:
pythontry:
    from generated.tools.tool_name import tool_name
except ImportError:
    # Fallback behavior
    return state

"""

CLAUDE_TOOL_GENERATION_PROMPT = """Generate a PURE Python function with UNIVERSAL input handling:

MANDATORY PATTERNS:
1. Accept ANY input type gracefully:
   ```python
   def tool_name(input_data):
       # Convert to expected type
       if input_data is None:
           return default_value
       
       if isinstance(input_data, expected_type):
           data = input_data
       elif isinstance(input_data, dict):
           # Extract from dict
           data = input_data.get('field', default)
       elif isinstance(input_data, list):
           # Process list
           data = process_list(input_data)
       else:
           # Try string conversion
           try:
               data = str(input_data)
           except:
               return default_value

NEVER crash - always return something usable
Type coercion over type errors
Meaningful defaults for all error cases
"""

# Add validation rules
AGENT_VALIDATION_RULES = {
    "must_handle_multiple_input_types": True,
    "must_have_fallback_behavior": True,
    "must_initialize_state": True,
    "must_handle_empty_input": True,
    "must_provide_structured_output": True,
}

TOOL_VALIDATION_RULES = {
    "must_accept_any_type": True,
    "must_return_consistent_type": True,
    "must_have_defaults": True,
    "no_exceptions_allowed": True,
}

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_TO_FILE = True
LOG_FILE_PATH = "agentic_fabric.log"
