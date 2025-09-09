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

# Output Directory for Generated Files
OUTPUT_FOLDER = os.path.join(PROJECT_ROOT, "flask_app", "outputs")

# Ensure output directory exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

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
        # ADD THIS NEW FIELD:
        "generated_files": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string"},
                    "path": {"type": "string"},
                    "type": {"type": "string"},
                    "description": {"type": "string"},
                    "size": {"type": "number"},
                },
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

ORCHESTRATOR_PLANNING_PROMPT = """You are planning a workflow for this user request.

REQUEST: {request}
ANALYSIS: {analysis}

AVAILABLE AGENTS:
{available_agents}

AVAILABLE TOOLS:
{available_tools}

PLANNING INSTRUCTIONS:
1. Identify what the user wants to accomplish
2. Find existing agents that can handle the task
3. Plan execution order (sequential/parallel/conditional)
4. Only suggest creating new agents if existing ones truly cannot handle the task
5. Be flexible - agents often have broader capabilities than their names suggest

OUTPUT FORMAT - Respond with valid JSON:
{{
    "workflow_id": "wf_{timestamp}",
    "workflow_type": "sequential|parallel|conditional", 
    "reasoning": "Brief explanation of your plan",
    "agents_needed": ["exact_agent_names_from_available_list"],
    "missing_capabilities": {{
        "agents": [
            {{
                "name": "agent_name",
                "purpose": "what it should do",
                "required_tools": ["tool1", "tool2"]
            }}
        ],
        "tools": [
            {{
                "name": "tool_name", 
                "purpose": "what it should do"
            }}
        ]
    }},
    "confidence": 0.0-1.0
}}

IMPORTANT: 
- Use exact agent names from the available list
- Don't assume rigid naming patterns 
- Prefer existing agents over creating new ones
- If no existing agents match, describe what needs to be created"""


ORCHESTRATOR_ANALYSIS_PROMPT = """Analyze this user request to understand intent, requirements, and execution strategy:

REQUEST: {request}
FILES: {files}
CONTEXT: {context}

AVAILABLE AGENTS (use exact names):
{available_agents}

AVAILABLE TOOLS:
{available_tools}

Perform systematic analysis:

1. CORE INTENT: What does the user want to accomplish?
2. TASK CLASSIFICATION: What type of operation is this? (analysis, extraction, calculation, processing, etc.)
3. DATA REQUIREMENTS: What kind of data does this task need? (numbers, text, files, structured data, etc.)
4. PROCESSING COMPLEXITY: Is this a single-step or multi-step operation?
5. CAPABILITY MATCHING: Which available agents can handle this type of task?
6. CAPABILITY GAPS: What specific capabilities are missing and need to be created?
7. EXECUTION STRATEGY: Should this be sequential, parallel, or conditional execution?

IMPORTANT GUIDELINES:
- Focus on WHAT needs to be done, not HOW to extract data (DataProcessor handles extraction)
- Be specific about agent names and their actual capabilities
- Consider the user's expertise level and adjust complexity accordingly
- Think about error scenarios and edge cases
- Identify if the request is ambiguous and needs clarification

ANALYSIS EXAMPLES:

Request: "Find prime numbers in: 43, 17, 89, 56"
→ Intent: Mathematical analysis - prime number identification
→ Task Type: Numerical computation
→ Data Requirements: Array of integers
→ Complexity: Single-step operation
→ Available Capability: None (need prime_checker)
→ Strategy: Sequential execution with new agent

Request: "Extract emails and count words in this document"
→ Intent: Multi-step text analysis
→ Task Type: Text extraction + counting
→ Data Requirements: Text document content
→ Complexity: Multi-step operation  
→ Available Capability: email_extractor + word_counter
→ Strategy: Parallel execution of existing agents

Request: "Analyze this CSV and create a report"
→ Intent: Data analysis with visualization
→ Task Type: Data processing + report generation
→ Data Requirements: Structured tabular data
→ Complexity: Multi-step pipeline
→ Available Capability: Partial (may need data analyzer + report generator)
→ Strategy: Sequential pipeline with possible new agent creation

Be thorough but concise. Focus on strategic understanding rather than data parsing."""

ORCHESTRATOR_SYNTHESIS_PROMPT = """Create a natural, helpful response based on the workflow execution results.

USER'S ORIGINAL REQUEST: {request}
ACTUAL AGENT EXECUTION RESULTS: {results}
WORKFLOW ERRORS: {errors}

CRITICAL INSTRUCTIONS:
1. **ONLY use the data that agents actually returned** - Do not make assumptions
2. **Read the agent results carefully** - Look at the actual data structures and values
3. **Address what the user specifically asked for** - Don't default to generic patterns
4. **If agents returned empty/null/zero results, say so** - Don't make up data
5. **Include processing attribution** - Show which agents contributed to the answer
6. **If files were generated, provide download links** - Use the exact format: [Download Filename](/api/download/filename)

RESPONSE STRUCTURE:
[Direct answer based on actual agent data]

[If files were generated, add download section:]
**Generated Files:**
- [Download Report](/api/download/filename.pdf) - Description

*Processed using [actual_agent_names] | Execution time: [actual_time]*

IMPORTANT RULES:
- Never invent data that wasn't returned by agents
- Never assume what results mean without looking at actual values
- If results are missing or empty, explain this honestly
- Always base your response on the actual execution results provided
- For generated files, use the exact filename and path provided by agents
- Be conversational but factually accurate to the agent outputs"""

# =============================================================================
# AGENT GENERATION PROMPTS
# =============================================================================

CLAUDE_AGENT_GENERATION_PROMPT = """Create a SMART Python agent that handles input intelligently.

Agent Name: {agent_name}
Purpose: {description}
Required Tools: {tools}

CRITICAL: The agent must be smart about input data extraction and formatting.

SMART INPUT HANDLING PATTERN:
```python
def {agent_name}_agent(state):
    \"\"\"
    {description}
    \"\"\"
    import sys
    import os
    from datetime import datetime
    
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Initialize state
    if 'results' not in state:
        state['results'] = {{}}
    if 'errors' not in state:
        state['errors'] = []
    if 'execution_path' not in state:
        state['execution_path'] = []
    
    try:
        start_time = datetime.now()
        
        # SMART DATA EXTRACTION - Try multiple sources in priority order
        target_data = None
        
        # Priority 1: Use extracted data if available (from intelligent processing)
        if 'extracted_data' in state and state['extracted_data'] is not None:
            target_data = state['extracted_data']
            print(f"DEBUG: Using extracted data: {{target_data}}")
        
        # Priority 2: Use current_data
        elif 'current_data' in state and state['current_data'] is not None:
            target_data = state['current_data']
        
        # Priority 3: Parse from raw request if needed
        else:
            raw_request = state.get('request', state.get('text', ''))
            target_data = raw_request
        
        # SMART PROCESSING - Agent reasons about the input and processes accordingly
        
        # For {agent_name}, implement intelligent processing here
        {agent_logic}
        
        result = {{
            "status": "success",
            "data": processed_data,
            "metadata": {{
                "agent": "{agent_name}",
                "execution_time": (datetime.now() - start_time).total_seconds(),
                "tools_used": {tools},
                "input_data_type": str(type(target_data).__name__)
            }}
        }}
        
        state['results']['{agent_name}'] = result
        state['current_data'] = processed_data
        state['execution_path'].append('{agent_name}')
        
    except Exception as e:
        import traceback
        state['errors'].append({{
            "agent": "{agent_name}",
            "error": str(e),
            "traceback": traceback.format_exc()
        }})
        state['results']['{agent_name}'] = {{
            "status": "error",
            "data": None,
            "metadata": {{"agent": "{agent_name}", "error": str(e)}}
        }}
    
    return state
Make the agent SMART about handling different input types. For prime checking:

If input is a list of numbers → check each number
If input is a string with numbers → extract numbers then check
If input is a single number → check that number

Don't hardcode expectations - make agents adaptive!"""

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
                data = input_data.get('text', input_data.get('data', input_data.get('content', str(input_data))))
            elif isinstance(input_data, (list, tuple)):
                data = input_data
            elif isinstance(input_data, (int, float)):
                data = input_data
            else:
                data = str(input_data)
            
            # TOOL LOGIC HERE - Implement actual functionality
            # Even if it's a simple placeholder, make it functional
            result = {default_return}
            
            # Add basic implementation based on tool name
            if "format" in "{tool_name}":
                result = f"Formatted: {{data}}"
            elif "generate" in "{tool_name}":
                result = f"Generated output for: {{data}}"
            elif "extract" in "{tool_name}":
                result = []
            elif "calculate" in "{tool_name}":
                result = 0
            else:
                result = data
            
            return result
            
        except Exception as e:
            # NEVER raise exceptions, always return default
            return {default_return}
    Requirements:

    MUST be a pure function (no side effects)
    MUST handle None and any input type
    MUST NOT raise exceptions
    MUST return consistent type
    MUST have at least basic functionality
    Keep between {min_lines}-{max_lines} lines"""


DEPENDENCY_ANALYSIS_PROMPT = """
Analyze this request and identify all required capabilities.
Break down the request into atomic operations.

For each capability, specify:
1. The agent needed to perform it
2. The tools that agent would require
3. Input/output data types
4. Dependencies on other capabilities

Request: {request}

Return a structured analysis with:
- List of capabilities
- Dependency relationships
- Suggested execution order
"""

TOOL_GENERATION_PROMPT_ENHANCED = """
You are an expert Python developer creating a tool function.

Tool: {tool_name}
Purpose: {description}
Context: This tool will be used by {used_by_agents}

Create a WORKING implementation that:
1. Actually performs the described function (not a placeholder)
2. Handles edge cases gracefully
3. Returns consistent, predictable output
4. Uses appropriate Python libraries

Examples of good implementations:
- Use 're' module for pattern matching
- Use 'statistics' module for calculations
- Use 'json' module for data formatting
- Use list comprehensions for filtering

The function MUST work correctly when called.
Do not create placeholder or mock implementations.

Return only the Python code.
"""

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


# Registry Settings
REGISTRY_LOCK_TIMEOUT = 5.0  # Seconds to wait for lock
REGISTRY_SYNC_INTERVAL = 0.5  # Minimum seconds between reloads

# Quality Gates
ENFORCE_TOOL_QUALITY = True  # Reject placeholder tools
ENFORCE_AGENT_QUALITY = True  # Reject non-functional agents
TEST_GENERATED_CODE = True  # Test code before registration

# # Model Settings - Upgrade for better quality
# ORCHESTRATOR_MODEL = "gpt-4"  # Upgrade from o3-mini for better planning
# CLAUDE_MODEL = "claude-3-sonnet-20240229"  # Upgrade from haiku for better code

# Validation Settings
REQUIRE_TOOL_TESTS = True  # Tools must pass basic tests
REQUIRE_AGENT_TESTS = True  # Agents must pass basic tests
