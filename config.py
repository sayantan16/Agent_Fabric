"""
Agentic Fabric POC - Master Configuration
Single source of truth for all system configuration, prompts, and constraints
"""

import os
from dotenv import load_dotenv
from typing import List, Dict, Any

# Load environment variables
load_dotenv()

# =============================================================================
# API CONFIGURATION
# =============================================================================

# OpenAI Configuration (Master Orchestrator)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ORCHESTRATOR_MODEL = "o3-mini"  # Best for JSON and planning
ORCHESTRATOR_TEMPERATURE = 1.0  # Low for consistent planning
ORCHESTRATOR_MAX_TOKENS = 4000

# Anthropic Configuration (Agent Execution Engine)
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CLAUDE_MODEL = "claude-3-haiku-20240307"  # Fast and efficient for agents
CLAUDE_TEMPERATURE = 0.1  # Very low for consistent code generation
CLAUDE_MAX_TOKENS = 2000

# =============================================================================
# SYSTEM CONSTRAINTS
# =============================================================================

# Agent Size Constraints
MIN_AGENT_LINES = 50
MAX_AGENT_LINES = 300
AGENT_TIMEOUT_SECONDS = 10
AGENT_MAX_RETRIES = 3

# Tool Size Constraints
MIN_TOOL_LINES = 20
MAX_TOOL_LINES = 100
TOOL_MUST_BE_PURE = True
TOOL_TIMEOUT_SECONDS = 5

# Workflow Constraints
MAX_WORKFLOW_STEPS = 10
WORKFLOW_TIMEOUT_SECONDS = 60
MAX_PARALLEL_AGENTS = 5
ENABLE_PARALLEL_EXECUTION = True

# =============================================================================
# FILE PATHS
# =============================================================================

# Directories
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
GENERATED_AGENTS_DIR = os.path.join(PROJECT_ROOT, "generated", "agents")
GENERATED_TOOLS_DIR = os.path.join(PROJECT_ROOT, "generated", "tools")
PREBUILT_AGENTS_DIR = os.path.join(PROJECT_ROOT, "prebuilt", "agents")
PREBUILT_TOOLS_DIR = os.path.join(PROJECT_ROOT, "prebuilt", "tools")

# Registry Files
AGENTS_REGISTRY_PATH = os.path.join(PROJECT_ROOT, "agents.json")
TOOLS_REGISTRY_PATH = os.path.join(PROJECT_ROOT, "tools.json")

# Backup Directory
BACKUP_DIR = os.path.join(PROJECT_ROOT, "registry_backups")

# =============================================================================
# ALLOWED IMPORTS (Security)
# =============================================================================

ALLOWED_IMPORTS = [
    # Standard library
    "re",
    "json",
    "datetime",
    "math",
    "statistics",
    "collections",
    "itertools",
    "functools",
    "typing",
    "enum",
    "dataclasses",
    "csv",
    "io",
    "os",
    "sys",
    "pathlib",
    "hashlib",
    "base64",
    "urllib.parse",
    "copy",
    "random",
    "time",
    # Data processing
    "pandas",
    "numpy",
    # File processing
    "PyPDF2",
    "pdfplumber",
    "openpyxl",
    "xlrd",
    # Text processing
    "nltk",
    "textstat",
    # Visualization
    "matplotlib",
    "seaborn",
    "plotly",
    # Utilities
    "requests",  # Only for declared connectors
]

# =============================================================================
# STANDARD SCHEMAS
# =============================================================================

# Agent Output Envelope Schema
AGENT_OUTPUT_SCHEMA = {
    "type": "object",
    "required": ["status", "data", "metadata"],
    "properties": {
        "status": {"type": "string", "enum": ["success", "error", "partial"]},
        "data": {
            "type": ["object", "array", "null"],
            "description": "Agent-specific output data",
        },
        "metadata": {
            "type": "object",
            "required": ["agent", "execution_time"],
            "properties": {
                "agent": {"type": "string"},
                "execution_time": {"type": "number"},
                "tools_used": {"type": "array", "items": {"type": "string"}},
                "errors": {"type": "array", "items": {"type": "string"}},
                "warnings": {"type": "array", "items": {"type": "string"}},
            },
        },
    },
}

# Workflow State Schema
WORKFLOW_STATE_SCHEMA = {
    "request": "string",
    "files": "array",
    "execution_path": "array",
    "current_data": "any",
    "results": "object",
    "errors": "array",
    "workflow_id": "string",
    "started_at": "string",
    "completed_at": "string",
}

# =============================================================================
# VALIDATION RULES
# =============================================================================

# Agent Validation Rules
AGENT_VALIDATION_RULES = {
    "required_patterns": [
        # State initialization
        "if 'results' not in state:",
        "if 'errors' not in state:",
        "if 'execution_path' not in state:",
        # Flexible input handling
        "state.get('current_data'",
        "isinstance(",
        # Output envelope
        "'status':",
        "'data':",
        "'metadata':",
        # Error handling
        "try:",
        "except Exception as e:",
    ],
    "forbidden_patterns": [
        "exec(",
        "eval(",
        "__import__",
        "compile(",
        "globals(",
        "locals(",
    ],
    "required_structure": {
        "has_state_param": True,
        "returns_state": True,
        "handles_exceptions": True,
        "updates_results": True,
    },
}

# Tool Validation Rules
TOOL_VALIDATION_RULES = {
    "required_patterns": [
        # Universal input handling
        "if input_data is None:",
        "isinstance(input_data",
        # Error handling
        "try:",
        "except:",
        "return",
    ],
    "forbidden_patterns": [
        # No side effects for pure functions
        "open(",
        "with open",
        "file(",
        "os.system",
        "subprocess",
        "exec(",
        "eval(",
        "__import__",
        # No network unless connector
        "requests." if "connector" not in "{tool_type}" else "",
        "urllib.request",
        "socket.",
    ],
    "required_structure": {
        "handles_none": True,
        "handles_type_errors": True,
        "returns_consistent_type": True,
        "no_exceptions_raised": True,
    },
}

# =============================================================================
# ORCHESTRATOR PROMPTS
# =============================================================================

ORCHESTRATOR_SYSTEM_PROMPT = """You are an intelligent orchestrator for a multi-agent system. Think step-by-step through complex requests to plan optimal workflows.

Your process:
1. Analyze what the user wants to accomplish
2. Break complex tasks into logical steps  
3. Map steps to available agents/tools
4. Identify missing capabilities that need creation
5. Plan efficient execution (sequential/parallel)

Available agents and their capabilities will be provided. Use exact agent names from the registry."""

ORCHESTRATOR_PLANNING_PROMPT = """Plan a workflow for this request:

REQUEST: {request}
ANALYSIS: {analysis}

AVAILABLE AGENTS:
{available_agents}

AVAILABLE TOOLS: 
{available_tools}

Think through this systematically:

STEP 1: What specific tasks need to be done?
STEP 2: Which available agents can handle each task?
STEP 3: What's missing and needs to be created?
STEP 4: What's the optimal execution order?

Respond with valid JSON:
{{
    "workflow_id": "wf_" + timestamp,
    "workflow_type": "sequential|parallel",
    "reasoning": "your step-by-step thinking",
    "agents_needed": ["exact_agent_names"],
    "missing_capabilities": {{
        "agents": [
            {{
                "name": "agent_name",
                "purpose": "what it does",
                "required_tools": ["tool1"],
                "justification": "why needed"
            }}
        ],
        "tools": [
            {{
                "name": "tool_name", 
                "purpose": "what it does",
                "type": "pure_function",
                "justification": "why needed"
            }}
        ]
    }},
    "confidence": 0.95
}}"""

ORCHESTRATOR_ANALYSIS_PROMPT = """Analyze this user request to understand intent and requirements:

REQUEST: {request}
FILES: {files}
CONTEXT: {context}

AVAILABLE AGENTS (use exact names):
{available_agents}

AVAILABLE TOOLS:
{available_tools}

Analyze systematically:

1. CORE INTENT: What does the user want to accomplish?
2. INPUT DATA: What data/content needs processing?
3. REQUIRED OUTPUTS: What should the final result contain?
4. PROCESSING STEPS: What transformations are needed?
5. CAPABILITY MATCH: Which available agents can handle parts of this?
6. MISSING PIECES: What capabilities don't exist yet?

Be specific about agent names and realistic about what each can do."""

ORCHESTRATOR_SYNTHESIS_PROMPT = """Synthesize the workflow execution results into a coherent response.

Original Request: {request}
Workflow Plan: {plan}
Execution Results: {results}
Errors Encountered: {errors}

Create a natural language response that:
1. Directly answers the user's question
2. Highlights key findings and insights
3. Explains any issues encountered
4. Suggests next steps if applicable
5. Maintains professional tone

Focus on value and clarity, not technical details."""

# =============================================================================
# AGENT GENERATION PROMPTS
# =============================================================================

CLAUDE_AGENT_GENERATION_PROMPT = """Create a Python agent function that follows our EXACT standards.

Agent Name: {agent_name}
Purpose: {description}
Required Tools: {tools}
Input Description: {input_description}
Output Description: {output_description}

CRITICAL: Generate ONLY a function, no imports outside the function. Follow this EXACT pattern:

```python
def {agent_name}_agent(state):
    \"\"\"
    {description}
    \"\"\"
    import sys
    import os
    from datetime import datetime
    
    # MANDATORY: Add path for imports
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # MANDATORY: Import required tools (if any)
    {tool_imports}
    
    # MANDATORY: Initialize state components
    if 'results' not in state:
        state['results'] = {{}}
    if 'errors' not in state:
        state['errors'] = []
    if 'execution_path' not in state:
        state['execution_path'] = []
    
    try:
        start_time = datetime.now()
        
        # MANDATORY: Universal input extraction
        input_data = None
        
        # Priority 1: Check current_data
        current_data = state.get('current_data')
        if current_data is not None:
            if isinstance(current_data, str):
                input_data = current_data
            elif isinstance(current_data, dict):
                for key in ['text', 'data', 'content', 'value', 'result']:
                    if key in current_data:
                        input_data = current_data[key]
                        break
                if input_data is None:
                    input_data = current_data
            else:
                input_data = str(current_data)
        
        # Priority 2: Check previous results
        if input_data is None and 'results' in state:
            for result in reversed(list(state['results'].values())):
                if isinstance(result, dict) and 'data' in result:
                    input_data = result['data']
                    break
        
        # Priority 3: Check root state
        if input_data is None:
            for key in ['text', 'data', 'input', 'request']:
                if key in state and state[key]:
                    input_data = state[key]
                    break
        
        # AGENT LOGIC: Process input_data using tools
        {agent_logic}
        
        # Calculate execution time
        execution_time = (datetime.now() - start_time).total_seconds()
        
        # MANDATORY: Standard output envelope
        result = {{
            "status": "success",
            "data": processed_data,
            "metadata": {{
                "agent": "{agent_name}",
                "execution_time": execution_time,
                "tools_used": {tools},
                "warnings": []
            }}
        }}
        
        # MANDATORY: Update state
        state['results']['{agent_name}'] = result
        state['current_data'] = result['data']
        state['execution_path'].append('{agent_name}')
        
    except Exception as e:
        import traceback
        error_detail = {{
            "agent": "{agent_name}",
            "error": str(e),
            "traceback": traceback.format_exc(),
            "timestamp": datetime.now().isoformat()
        }}
        state['errors'].append(error_detail)
        
        state['results']['{agent_name}'] = {{
            "status": "error",
            "data": None,
            "metadata": {{
                "agent": "{agent_name}",
                "execution_time": 0,
                "error": str(e)
            }}
        }}
    
    return state
Make the agent logic simple but functional. Keep between {min_lines}-{max_lines} lines total.
"""

# =============================================================================
# TOOL GENERATION PROMPTS
# =============================================================================

CLAUDE_TOOL_GENERATION_PROMPT = """Create a PURE Python function following our standards.

Tool Name: {tool_name}
Purpose: {description}
Input: {input_description}
Output: {output_description}

MANDATORY TOOL STRUCTURE:
```python
def {tool_name}(input_data=None):
    \"\"\"
    {description}
    
    Args:
        input_data: {input_description}
    
    Returns:
        {output_description}
    \"\"\"
    # Required imports
    {imports}
    
    # MANDATORY: Handle None input
    if input_data is None:
        return {default_return}
    
    # MANDATORY: Type flexibility
    try:
        # Handle different input types
        if isinstance(input_data, str):
            data = input_data
        elif isinstance(input_data, dict):
            # Extract from common keys
            data = None
            for key in ['text', 'data', 'value', 'content']:
                if key in input_data:
                    data = input_data[key]
                    break
            if data is None:
                data = str(input_data)
        elif isinstance(input_data, (list, tuple)):
            data = input_data
        elif isinstance(input_data, (int, float)):
            data = input_data
        else:
            # Convert to string as fallback
            try:
                data = str(input_data)
            except:
                return {default_return}
        
        # TOOL LOGIC HERE
        {tool_logic}
        
        return result
        
    except Exception as e:
        # NEVER raise exceptions, always return default
        return {default_return}
```

Requirements:
1. MUST be a pure function (no side effects)
2. MUST handle None and any input type
3. MUST NOT raise exceptions
4. MUST return consistent type
5. Keep between {min_lines}-{max_lines} lines"""

# =============================================================================
# PREBUILT COMPONENTS
# =============================================================================

PREBUILT_READERS = ["read_text", "read_json", "read_csv", "read_pdf"]

PREBUILT_CONNECTORS = ["jira_reader"]  # Jira-only for POC

# =============================================================================
# UI CONFIGURATION
# =============================================================================

UI_CONFIG = {
    "title": "Agentic Fabric POC",
    "theme": "light",
    "max_file_upload_mb": 10,
    "supported_file_types": ["txt", "pdf", "csv", "json", "xlsx"],
    "show_execution_time": True,
    "show_workflow_viz": True,
    "show_generated_code": False,  # Debug mode only
    "refresh_interval_ms": 500,
}

# =============================================================================
# LOGGING
# =============================================================================

LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "agentic_fabric.log",
    "max_bytes": 10485760,  # 10MB
    "backup_count": 5,
}
