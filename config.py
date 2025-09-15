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
CLAUDE_MODEL = "claude-sonnet-4-20250514"  # Fast and efficient for agents
# claude-3-haiku-20240307
CLAUDE_TEMPERATURE = 0.1  # Very low for consistent code generation
CLAUDE_MAX_TOKENS = 4000

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
# DYNAMIC INTELLIGENCE SYSTEM PROMPT
# =============================================================================

DYNAMIC_INTELLIGENCE_SYSTEM_PROMPT = """You are an adaptive AI that NEVER uses hardcoded patterns or predefined solutions. Your core principle is DYNAMIC REASONING.

FUNDAMENTAL RULES:
1. ANALYZE FIRST: Always understand the specific request before acting
2. REASON DYNAMICALLY: Never apply template solutions or hardcoded patterns  
3. THINK CONTEXTUALLY: Every situation is unique and requires unique analysis
4. GENERATE APPROPRIATELY: Create solutions that fit the exact requirements
5. ADAPT CONTINUOUSLY: Adjust your approach based on the specific context

FORBIDDEN BEHAVIORS:
- Using predefined examples (prime numbers, email extraction, etc.)
- Applying template patterns without analysis
- Assuming request types based on keywords
- Generating generic or boilerplate responses
- Hardcoding any logic, functions, or structures

REQUIRED BEHAVIORS:
- Analyze the specific request context deeply
- Understand the exact data types and transformations needed
- Reason about optimal approaches for THIS specific case
- Generate solutions that are purpose-built for the requirements
- Think step-by-step about what is actually needed

Always think: "How do I solve THIS specific problem intelligently?"
Never think: "Which template pattern matches this request?"
"""

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

AGENT_SELF_SUFFICIENCY_RULES = {
    "implement_own_logic": True,
    "minimize_tool_dependencies": True,
    "tool_creation_threshold": "high",  # Only create tools for complex operations
    "prefer_inline_implementation": True,
}

# Tool creation criteria
TOOL_CREATION_CRITERIA = {
    "required_for": [
        "external_api_calls",
        "database_connections",
        "specialized_file_formats",  # PDF, Excel
        "network_operations",
        "complex_libraries",  # numpy, pandas operations
    ],
    "not_required_for": [
        "basic_math",
        "string_operations",
        "list_filtering",
        "simple_calculations",
        "pattern_matching",
        "data_parsing",
    ],
}

Available agents and their capabilities will be provided. Use exact agent names from the registry."""

ORCHESTRATOR_PLANNING_PROMPT = """You are a workflow orchestrator planning optimal execution for a user request.

REQUEST: {request}
ANALYSIS: {analysis}
AVAILABLE AGENTS: {available_agents}
AVAILABLE TOOLS: {available_tools}

ORCHESTRATION INTELLIGENCE:

1. **STRATEGIC PLANNING**: How to accomplish the user's goal most effectively
2. **RESOURCE ALLOCATION**: Best use of existing capabilities
3. **DEPENDENCY MANAGEMENT**: Handling interdependencies intelligently
4. **OPTIMIZATION**: Fastest, most reliable execution path
5. **RISK MITIGATION**: Handling potential failures

PLANNING FRAMEWORK:

1. **GOAL ANALYSIS**: What does success look like for this request?
2. **CAPABILITY MAPPING**: How do available agents map to requirements?
3. **GAP ANALYSIS**: What capabilities are missing?
4. **EXECUTION DESIGN**: What's the optimal execution strategy?
5. **CONTINGENCY PLANNING**: What if things go wrong?

RESPOND WITH JSON:
{{
    "workflow_strategy": {{
        "approach": "single_agent|sequential_pipeline|parallel_execution|hybrid_strategy",
        "rationale": "why this approach is optimal for this specific request",
        "complexity_assessment": "simple|moderate|complex|enterprise",
        "confidence_level": 0.85
    }},
    "execution_plan": {{
        "total_steps": 3,
        "execution_pattern": "linear|branching|converging|iterative",
        "estimated_duration": 25,
        "resource_intensity": "low|medium|high",
        "optimization_strategy": "speed|accuracy|reliability|cost"
    }},
    "agent_assignments": [
        {{
            "step_index": 0,
            "assigned_agent": "existing_agent_name|null",
            "assignment_confidence": 0.9,
            "assignment_rationale": "why this agent fits this step",
            "modification_needed": "none|minor|major",
            "fallback_options": ["alternative_agent_1", "create_new"]
        }}
    ],
    "capability_gaps": {{
        "missing_agents": [
            {{
                "purpose": "what this missing agent should do",
                "priority": "critical|high|medium|low",
                "complexity": "simple|moderate|complex",
                "creation_estimate": "time to create"
            }}
        ],
        "missing_tools": [
            {{
                "purpose": "what this missing tool should do",
                "priority": "critical|high|medium|low",
                "complexity": "simple|moderate|complex"
            }}
        ],
        "creation_order": ["component_1", "component_2"]
    }},
    "data_flow_design": {{
        "flow_pattern": "description of how data moves through the workflow",
        "transformation_points": ["where data format changes"],
        "validation_checkpoints": ["where to validate data"],
        "state_management": "how to maintain state across steps"
    }},
    "risk_assessment": {{
        "potential_failure_points": ["step or component that might fail"],
        "mitigation_strategies": ["how to handle failures"],
        "recovery_options": ["fallback approaches"],
        "success_probability": 0.8
    }},
    "optimization_opportunities": {{
        "parallelization": ["steps that can run in parallel"],
        "caching": ["data that can be cached"],
        "shortcuts": ["optimizations for common cases"],
        "performance_bottlenecks": ["potential slow points"]
    }}
}}

PLAN FOR THIS SPECIFIC REQUEST - avoid generic templated responses."""


# ORCHESTRATOR_ANALYSIS_PROMPT = """You are an intelligent request analyzer. Your job is to deeply understand what the user wants to accomplish and provide strategic guidance for execution.

# USER REQUEST: "{request}"
# UPLOADED FILES: {files}
# SYSTEM CONTEXT: {context}

# AVAILABLE CAPABILITIES:
# Agents: {available_agents}
# Tools: {available_tools}

# ANALYSIS FRAMEWORK:

# 1. **INTENT ANALYSIS**:
#    - What is the user's primary goal?
#    - What type of outcome do they expect?
#    - What domain does this request belong to? (mathematical, textual, analytical, creative, technical, etc.)

# 2. **REQUIREMENT DECOMPOSITION**:
#    - What are the atomic operations needed?
#    - What data transformations are required?
#    - What dependencies exist between operations?
#    - What input/output formats are involved?

# 3. **COMPLEXITY ASSESSMENT**:
#    - Single-step: One clear operation
#    - Multi-step: Sequential operations with data flow
#    - Complex: Multiple interdependent operations with branching logic

# 4. **CAPABILITY MATCHING**:
#    - Which existing agents can handle parts of this request?
#    - What capabilities are missing?
#    - How well do available tools support the required operations?

# 5. **EXECUTION STRATEGY**:
#    - Sequential: Steps must happen in order
#    - Parallel: Independent operations can run simultaneously
#    - Conditional: Logic branches based on intermediate results

# RESPOND WITH JSON:
# {{
#     "intent_analysis": {{
#         "primary_goal": "concise description of what user wants to achieve",
#         "expected_outcome_type": "data|analysis|visualization|document|calculation|extraction",
#         "domain": "mathematical|textual|analytical|creative|technical|mixed",
#         "user_expertise_level": "beginner|intermediate|advanced|technical"
#     }},
#     "requirements": {{
#         "atomic_operations": ["operation1", "operation2", "operation3"],
#         "data_transformations": ["input_type → intermediate_type → output_type"],
#         "dependencies": [["op1_before_op2"], ["op2_before_op3"]],
#         "input_formats": ["format1", "format2"],
#         "output_format": "expected_final_format"
#     }},
#     "complexity": {{
#         "level": "single|multi|complex",
#         "estimated_steps": 3,
#         "parallel_opportunities": ["op1_and_op2_parallel"],
#         "critical_dependencies": ["op3_needs_op1_and_op2"]
#     }},
#     "capability_assessment": {{
#         "existing_coverage": 0.7,
#         "missing_capabilities": ["specific_capability_1", "specific_capability_2"],
#         "tool_gaps": ["missing_tool_type"],
#         "agent_gaps": ["missing_agent_capability"]
#     }},
#     "execution_strategy": {{
#         "approach": "sequential|parallel|conditional",
#         "rationale": "why this approach is optimal",
#         "estimated_time": 25,
#         "confidence": 0.85
#     }}
# }}

# CRITICAL: Focus on understanding the ACTUAL REQUEST, not matching to predefined patterns. Every request is unique."""

ORCHESTRATOR_ANALYSIS_PROMPT = """You are an intelligent orchestrator that plans workflows.

USER REQUEST: {request}

FILE DATA AVAILABLE:
{files}

IMPORTANT: You can now see the actual structure of uploaded files:
- For CSV files, you see the exact column names, data types, and sample values
- Plan your workflow based on the ACTUAL data structure, not assumptions
- Select agents that can work with these specific columns and data types

Available agents: {agents}

Create a workflow plan that processes the actual data you can see.
"""

ORCHESTRATOR_SYNTHESIS_PROMPT = """You are a results synthesizer creating a natural, helpful response based on workflow execution.

USER'S REQUEST: "{request}"
WORKFLOW EXECUTION RESULTS: {results}
EXECUTION ERRORS: {errors}
WORKFLOW METADATA: {{
    "execution_time": "{execution_time}s",
    "agents_used": {agents_used},
    "workflow_type": "{workflow_type}"
}}

SYNTHESIS INTELLIGENCE:

1. **RESULT ANALYSIS**: What was actually accomplished?
2. **USER ALIGNMENT**: How well do results match user expectations?
3. **QUALITY ASSESSMENT**: Are the results complete and accurate?
4. **PRESENTATION OPTIMIZATION**: How to present results most effectively?
5. **VALUE COMMUNICATION**: What value was delivered to the user?

RESPONSE FRAMEWORK:

1. **DIRECT ANSWER**: Address what the user specifically asked for
2. **RESULT PRESENTATION**: Show the actual data/findings clearly
3. **PROCESS TRANSPARENCY**: Explain how results were obtained
4. **QUALITY INDICATORS**: Indicate reliability and completeness
5. **ACTIONABLE INSIGHTS**: Provide relevant next steps or interpretations

SYNTHESIS RULES:
- ONLY use data that was actually returned by agents
- NEVER invent or assume data that wasn't generated
- BE SPECIFIC about what was found vs. what was requested
- PRESENT results in the format most useful to the user
- ACKNOWLEDGE limitations or partial results honestly
- PROVIDE download links for generated files using: [Download Filename](/api/download/filename)

RESPONSE STRUCTURE:
Based on the actual results, determine the most appropriate response format:

For DATA EXTRACTION tasks:
- Show what was found with specific counts/values
- Indicate completeness of extraction
- Highlight any patterns or notable findings

For CALCULATION tasks:
- Present the computed values clearly
- Show intermediate steps if helpful
- Explain the methodology used

For ANALYSIS tasks:
- Summarize key findings and insights
- Present supporting data
- Indicate confidence levels

For PROCESSING tasks:
- Describe what was processed
- Show transformation results
- Indicate any quality issues

For FILE GENERATION tasks:
- Provide download links
- Describe file contents
- Explain how to use the files

ADAPT YOUR RESPONSE to match what was actually accomplished and what the user needs to know.

Create a natural, conversational response that directly addresses the user's request based on the actual execution results."""

# =============================================================================
# AGENT GENERATION PROMPTS
# =============================================================================

CLAUDE_AGENT_GENERATION_PROMPT = """You are an expert Python developer creating an intelligent agent for a multi-agent pipeline system.

AGENT SPECIFICATION:
- Name: {agent_name}
- Purpose: {description}
- Tools Available: {tools}
- Input Description: {input_description}
- Output Description: {output_description}

DYNAMIC LOGIC GENERATION INSTRUCTIONS:

1. **ANALYZE THE PURPOSE**: Read the agent description carefully and understand what specific operation it needs to perform.

2. **UNDERSTAND DATA FLOW**: 
   - Input: What type of data will this agent receive? (numbers, text, lists, dicts, files, etc.)
   - Processing: What transformation/analysis should be applied?
   - Output: What format should the result be in?

3. **IMPLEMENT APPROPRIATE LOGIC**:
   - For mathematical operations: Implement the specific calculation or analysis needed
   - For text processing: Implement parsing, extraction, or transformation logic  
   - For data analysis: Implement filtering, aggregation, or statistical operations
   - For file processing: Implement reading, parsing, or data extraction
   - For validation: Implement checking, verification, or quality assessment

4. **HANDLE MULTIPLE INPUT FORMATS**: The agent should intelligently handle different input types:
   - Raw strings (extract relevant data)
   - Lists/arrays (process elements)
   - Dictionaries (extract from various keys)
   - Results from previous pipeline steps

5. **GENERATE FLEXIBLE OUTPUT**: Create output that can be consumed by next pipeline step or as final result.

AGENT STRUCTURE TEMPLATE:
```python
def {agent_name}_agent(state):
    \"\"\"
    {description}
    
    Dynamically handles: {input_description}
    Produces: {output_description}
    \"\"\"
    import sys
    import os
    import re
    import json
    from datetime import datetime
    from typing import List, Dict, Any, Union
    
    # Add project path
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Import tools only if needed
    {tool_imports}
    
    # Initialize state
    if 'results' not in state:
        state['results'] = {{}}
    if 'errors' not in state:
        state['errors'] = []
    if 'execution_path' not in state:
        state['execution_path'] = []
    
    try:
        start_time = datetime.now()
        
        # INTELLIGENT INPUT EXTRACTION
        # Extract data from multiple possible sources in state
        input_data = None
        
        # Priority order for data extraction
        for key in ['extracted_data', 'current_data', 'data', 'input', 'request']:
            if key in state and state[key] is not None:
                input_data = state[key]
                break
        
        # If still no data, try to extract from nested structures
        if input_data is None:
            for key in ['results', 'context', 'files']:
                if key in state and state[key]:
                    input_data = state[key]
                    break
        
        # DYNAMIC LOGIC IMPLEMENTATION
        # Analyze the agent's purpose and implement appropriate logic
        
        # [THIS IS WHERE YOU ANALYZE THE DESCRIPTION AND IMPLEMENT THE RIGHT LOGIC]
        # Based on the description: "{description}"
        # Based on expected input: "{input_description}"  
        # Based on expected output: "{output_description}"
        
        # IMPLEMENT YOUR LOGIC HERE:
        # - If the purpose involves mathematical operations, implement those calculations
        # - If it involves text processing, implement parsing/extraction/analysis
        # - If it involves data filtering, implement filtering logic
        # - If it involves validation, implement checking logic
        # - If it involves transformation, implement conversion logic
        
        processed_data = {{}}  # Replace with actual implementation
        
        # STRUCTURED OUTPUT
        result = {{
            'status': 'success',
            'data': processed_data,
            'metadata': {{
                'agent': '{agent_name}',
                'execution_time': (datetime.now() - start_time).total_seconds(),
                'input_type': type(input_data).__name__,
                'output_type': type(processed_data).__name__,
                'tools_used': {tools}
            }}
        }}
        
        # Update pipeline state
        state['results']['{agent_name}'] = result
        state['current_data'] = processed_data
        state['execution_path'].append('{agent_name}')
        
        return state
        
    except Exception as e:
        import traceback
        error_info = {{
            'agent': '{agent_name}',
            'error': str(e),
            'traceback': traceback.format_exc()
        }}
        
        state['errors'].append(error_info)
        state['results']['{agent_name}'] = {{
            'status': 'error',
            'error': str(e),
            'metadata': error_info
        }}
        
        return state

CRITICAL: 

NEVER use locals(), globals(), exec(), eval(), or other introspection functions.
Use simple variable assignments and try/except for error handling instead.

CRITICAL REQUIREMENTS:

NO HARDCODED LOGIC - Analyze the description and implement appropriate logic dynamically
FLEXIBLE INPUT HANDLING - Handle various data types and sources intelligently
PURPOSE-DRIVEN IMPLEMENTATION - The logic should match exactly what the description asks for
ROBUST ERROR HANDLING - Handle edge cases and unexpected input gracefully
PIPELINE COMPATIBILITY - Ensure output can flow to next step or serve as final result

ANALYSIS PATTERNS:

If description mentions "find/extract/identify" → Implement search/filtering logic
If description mentions "calculate/compute/analyze" → Implement mathematical/statistical logic
If description mentions "transform/convert/format" → Implement data transformation logic
If description mentions "validate/check/verify" → Implement validation logic
If description mentions "parse/read/process" → Implement parsing/processing logic

Generate the complete, working agent that intelligently implements the required functionality based on the purpose description.
"""

# =============================================================================
# TOOL GENERATION PROMPTS
# =============================================================================

CLAUDE_TOOL_GENERATION_PROMPT = """Create a WORKING Python function that actually performs the described task.

Tool Name: {tool_name}
Purpose: {description}
Input: {input_description}
Output: {output_description}

CRITICAL: This must be a REAL IMPLEMENTATION, not a placeholder!

Based on the tool name and purpose, implement the ACTUAL logic:

- If it's "prime_checker": Actually check if numbers are prime using mathematical logic
- If it's "parse_and_filter_primes": Actually parse input and filter for prime numbers
- If it's "calculate_std": Actually calculate standard deviation using the statistics module
- If it's any calculation: Use proper mathematical formulas
- If it's extraction: Use proper regex or parsing logic
- If it's transformation: Actually transform the data

EXAMPLE of a GOOD implementation for prime checking:
```python
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True
```

Generate the COMPLETE WORKING function:

```python
def {tool_name}(input_data=None):
    \"\"\"
    {description}
    \"\"\"
    
    if input_data is None:
        # Return appropriate default for this specific tool
        {default_return}
    
    try:
        # Extract data from various input formats
        if isinstance(input_data, str):
            # Parse string input appropriately for this tool's purpose
            # For numbers: extract numeric values
            # For text: process as needed
            pass
        elif isinstance(input_data, dict):
            # Extract from common dictionary keys
            data = input_data.get('data', input_data.get('numbers', input_data.get('text', input_data)))
        elif isinstance(input_data, (list, tuple)):
            data = input_data
        else:
            data = input_data
        
        # IMPLEMENT THE ACTUAL TOOL LOGIC HERE
        # This is where you write the REAL implementation
        # Not placeholders or generic code
        
        # Return the actual result
        return result
        
    except Exception as e:
        # Return safe default on error
        {default_return}
```

Requirements:
1. MUST implement the actual functionality described
2. MUST handle different input formats intelligently
3. MUST NOT be a placeholder or generic template
4. MUST use appropriate Python libraries (math, statistics, re, etc.)
5. MUST return meaningful results

DO NOT create generic templates. Create REAL, WORKING implementations!
"""


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
# PIPELINE ORCHESTRATION PROMPTS
# =============================================================================

PIPELINE_ANALYSIS_PROMPT = """You are a pipeline architect. Break down the request into logical, executable steps that can be orchestrated intelligently.

REQUEST ANALYSIS: {request}
FILES CONTEXT: {files}
CAPABILITIES: 
- Agents: {available_agents}  
- Tools: {available_tools}

PIPELINE DESIGN PRINCIPLES:

1. **STEP IDENTIFICATION**: Each step should be atomic and well-defined
2. **DATA FLOW DESIGN**: Clear input/output specifications for each step
3. **DEPENDENCY MAPPING**: Understanding what depends on what
4. **CAPABILITY MATCHING**: Using existing components when possible
5. **GAP IDENTIFICATION**: Knowing what needs to be created

STEP DESIGN FRAMEWORK:
For each step, define:
- **Purpose**: What this step accomplishes
- **Input Contract**: Exactly what data format it expects
- **Output Contract**: Exactly what data format it produces  
- **Processing Logic**: What transformation/analysis occurs
- **Error Scenarios**: What can go wrong and how to handle it

RESPOND WITH JSON:
{{
    "pipeline_metadata": {{
        "pipeline_type": "sequential|parallel|conditional|hybrid",
        "complexity_level": "simple|moderate|complex|enterprise",
        "estimated_duration": 45,
        "resource_requirements": "low|medium|high"
    }},
    "steps": [
        {{
            "step_id": "step_1", 
            "name": "Descriptive_Step_Name",
            "purpose": "What this step accomplishes",
            "input_contract": {{
                "data_type": "string|number|array|object|file",
                "format": "specific format description",
                "source": "user_input|previous_step|file_upload",
                "validation_rules": ["rule1", "rule2"]
            }},
            "output_contract": {{
                "data_type": "string|number|array|object",
                "format": "specific format description", 
                "destination": "next_step|final_output",
                "structure": "detailed structure description"
            }},
            "processing_requirements": {{
                "operation_type": "extraction|calculation|transformation|analysis|validation",
                "complexity": "simple|moderate|complex",
                "special_handling": ["edge_case_1", "edge_case_2"]
            }},
            "dependencies": ["step_id_that_must_complete_first"],
            "estimated_time": 8
        }}
    ],
    "data_flow": {{
        "flow_pattern": "linear|branching|converging|circular",
        "data_transformations": [
            {{
                "from_step": "step_1",
                "to_step": "step_2", 
                "transformation": "how data changes between steps"
            }}
        ],
        "validation_points": ["where to validate data integrity"]
    }},
    "execution_strategy": {{
        "primary_approach": "sequential|parallel|hybrid",
        "optimization_opportunities": ["where parallelism is possible"],
        "critical_path": ["steps that determine total execution time"],
        "fallback_strategies": ["what to do if steps fail"]
    }},
    "component_requirements": {{
        "existing_agents_usable": ["agent_name_1", "agent_name_2"],
        "new_agents_needed": [
            {{
                "purpose": "what this new agent should do",
                "input_type": "expected input format",
                "output_type": "expected output format",
                "complexity": "simple|moderate|complex"
            }}
        ],
        "tools_needed": ["tool_type_1", "tool_type_2"],
        "creation_priority": "high|medium|low"
    }}
}}

FOCUS: Design based on the ACTUAL request requirements, not template patterns."""

AGENT_COMPATIBILITY_PROMPT = """Analyze compatibility between a pipeline step and existing agents.

STEP REQUIREMENTS:
{step_requirements}

AVAILABLE AGENTS:
{available_agents}

COMPATIBILITY ANALYSIS:
For each agent, analyze:
1. Capability match - Can it perform the required task?
2. Input compatibility - Can it handle the expected input format?
3. Output compatibility - Does it produce the required output format?  
4. Tool availability - Does it have the necessary tools?

ANALYSIS RULES:
1. Score 0.9-1.0: Agent is SPECIFICALLY designed for this exact task (has right tools, clear use case match)
2. Score 0.6-0.8: Agent has SOME relevant capabilities but needs adaptation  
3. Score 0.3-0.5: Agent MIGHT work with major modifications
4. Score 0.0-0.2: Agent is NOT suitable at all

CRITICAL: If an agent description mentions "generic" or "general" - be VERY skeptical. Generic agents should only get high scores if they have the EXACT tools needed.

OUTPUT FORMAT - Respond with valid JSON:
{{
    "compatible_agents": [
        {{
            "agent_name": "exact_agent_name",
            "compatibility_score": 0.85,
            "strengths": ["handles text input", "produces structured output"],
            "limitations": ["may need additional tools"],
            "required_modifications": []
        }}
    ],
    "best_match": {{
        "agent_name": "best_agent_name",
        "score": 0.92,
        "ready_to_use": true
    }},
    "missing_capabilities": [
        "specific capability not available in any agent"
    ],
    "recommendation": "use_existing|create_new|modify_existing"
}}"""

PIPELINE_PLANNING_PROMPT = """Plan optimal execution for this multi-step pipeline.

PIPELINE ANALYSIS:
{pipeline_analysis}

STEP COMPATIBILITY:
{step_compatibility}

PLANNING INSTRUCTIONS:
1. For each step, assign the best available agent or specify creation needs
2. Plan execution order (sequential/parallel/conditional)
3. Define data flow between steps
4. Identify components that need to be created
5. Estimate total execution time

OUTPUT FORMAT - Respond with valid JSON:
{{
    "pipeline_id": "pipeline_timestamp",
    "execution_strategy": "sequential|parallel|hybrid",
    "total_estimated_time": 25,
    "steps": [
        {{
            "step_index": 0,
            "name": "step_name",
            "agent_assigned": "existing_agent_name|null", 
            "needs_creation": false,
            "creation_priority": "high|medium|low",
            "dependencies": [],
            "estimated_time": 8
        }}
    ],
    "creation_needed": [
        {{
            "type": "agent",
            "name": "new_agent_name",
            "purpose": "what it should do",
            "priority": "high|medium|low",
            "for_step": "step_name"
        }}
    ],
    "data_flow_plan": {{
        "step_0": {{ "outputs_to": ["step_1"], "format": "processed_text" }},
        "step_1": {{ "inputs_from": ["step_0"], "outputs_to": ["step_2"] }}
    }},
    "optimization_opportunities": [],
    "risks": []
}}"""

DYNAMIC_AGENT_SPEC_PROMPT = """You are an agent architect designing a component for a specific pipeline step.

STEP CONTEXT:
- Description: {step_description}
- Step Index: {step_index}
- Input Requirements: {input_requirements}
- Output Requirements: {output_requirements}
- Available Tools: {available_tools}

AGENT DESIGN PRINCIPLES:

1. **PURPOSE CLARITY**: Agent should have one clear, well-defined responsibility
2. **INPUT INTELLIGENCE**: Handle various input formats gracefully
3. **OUTPUT CONSISTENCY**: Produce predictable, well-structured output
4. **ERROR RESILIENCE**: Handle edge cases and failures gracefully
5. **PIPELINE AWARENESS**: Understand its role in the larger workflow

DESIGN ANALYSIS:
1. What specific capability does this step require?
2. What are the possible input variations?
3. What processing logic is needed?
4. What output format serves the next step best?
5. What error scenarios need handling?

RESPOND WITH JSON:
{{
    "agent_specification": {{
        "name": "descriptive_agent_name_for_purpose",
        "description": "clear description of what this agent does",
        "responsibility": "single, well-defined responsibility",
        "specialization": "what makes this agent unique/specialized"
    }},
    "input_handling": {{
        "primary_input_type": "expected main input format",
        "alternative_input_types": ["other formats it should handle"],
        "input_validation": ["validation rules for input"],
        "input_extraction_logic": "how to extract data from various sources",
        "edge_cases": ["empty input", "wrong format", "missing data"]
    }},
    "processing_specification": {{
        "core_logic_type": "mathematical|textual|analytical|transformational|validation",
        "algorithm_approach": "description of processing approach",
        "complexity_level": "simple|moderate|complex",
        "performance_requirements": "fast|moderate|thorough",
        "external_dependencies": ["tools or libraries needed"]
    }},
    "output_specification": {{
        "output_format": "structured description of output",
        "data_structure": "detailed structure specification",
        "metadata_requirements": ["what metadata to include"],
        "success_indicators": ["how to know processing succeeded"],
        "error_format": "how to format error responses"
    }},
    "implementation_guidance": {{
        "key_algorithms": ["algorithms or approaches to implement"],
        "data_flow_patterns": ["how data moves through the agent"],
        "optimization_opportunities": ["where to optimize performance"],
        "testing_scenarios": ["scenarios to test during development"]
    }},
    "pipeline_integration": {{
        "upstream_dependencies": ["what this agent expects from previous steps"],
        "downstream_requirements": ["what next steps need from this agent"],
        "state_management": ["how to update pipeline state"],
        "error_propagation": ["how to handle and report errors"]
    }},
    "quality_requirements": {{
        "reliability_level": "high|medium|basic",
        "performance_target": "execution time expectations", 
        "accuracy_requirements": "precision/accuracy needs",
        "robustness_level": "error handling sophistication needed"
    }}
}}

DESIGN FOR THE SPECIFIC REQUIREMENTS - don't use generic templates."""

PIPELINE_RECOVERY_PROMPT = """Generate recovery strategy for failed pipeline step.

FAILED STEP: {step_name}
STEP DESCRIPTION: {step_description}
FAILURE REASON: {failure_reason}
FAILURE ANALYSIS: {failure_analysis}
AVAILABLE AGENTS: {available_agents}

RECOVERY ANALYSIS:
1. Analyze why the step failed
2. Determine if it's recoverable with existing agents
3. Decide if new agent creation is needed
4. Plan data preprocessing if needed
5. Consider fallback strategies

OUTPUT FORMAT - Respond with valid JSON:
{{
    "recovery_assessment": {{
        "failure_type": "agent_error|data_issue|format_mismatch|timeout",
        "severity": "low|medium|high|critical",
        "recoverable": true,
        "estimated_recovery_time": 15
    }},
    "recommended_action": "retry|create_replacement|modify_data|skip_with_fallback",
    "action_details": {{
        "retry": {{ "max_attempts": 2, "modifications": [] }},
        "create_replacement": {{
            "agent_spec": {{
                "name": "replacement_agent_name",
                "description": "improved version that handles the failure case",
                "special_handling": ["edge case 1", "edge case 2"]
            }}
        }},
        "modify_data": {{
            "preprocessing_steps": ["clean data", "validate format"],
            "transformation_needed": "description of transformation"
        }},
        "skip_with_fallback": {{
            "fallback_data": "safe default result",
            "impact_assessment": "how this affects downstream steps"
        }}
    }},
    "confidence": 0.80,
    "alternative_strategies": []
}}"""

WORKFLOW_ADAPTATION_PROMPT = """Plan intelligent adaptation for workflow issues.

DETECTED ISSUES: {issues}
PIPELINE STATE: {pipeline_state}
STEP RESULT: {step_result}

ADAPTATION PLANNING:
1. Analyze the impact of detected issues
2. Determine the best adaptation strategy
3. Plan specific actions to resolve issues
4. Consider downstream effects
5. Minimize disruption to overall pipeline

OUTPUT FORMAT - Respond with valid JSON:
{{
    "adaptation_priority": "low|medium|high|critical",
    "recommended_action": "create_replacement_agent|modify_existing_agent|retry_with_preprocessing|skip_step_with_fallback",
    "action_rationale": "detailed explanation of why this action is best",
    "implementation_plan": {{
        "immediate_actions": ["action1", "action2"],
        "resource_requirements": ["new agent", "preprocessing tool"],
        "estimated_time": 10,
        "success_probability": 0.85
    }},
    "replacement_spec": {{
        "name": "adapted_agent_name",
        "description": "agent designed to handle the specific issues",
        "improvements": ["handles edge case X", "better error handling"],
        "tools": ["tool1", "tool2"]
    }},
    "preprocessing_spec": {{
        "name": "preprocessor_name", 
        "purpose": "prepare data to avoid issues",
        "transformations": ["clean nulls", "normalize format"]
    }},
    "fallback_data": {{
        "safe_default": "reasonable default result",
        "metadata": {{ "fallback_reason": "adaptation strategy" }}
    }},
    "monitoring_adjustments": [
        "watch for similar issues in future steps"
    ]
}}"""


# =============================================================================
# PIPELINE AGENT GENERATION TEMPLATES
# =============================================================================

PIPELINE_AGENT_TEMPLATE = """Create a pipeline-aware agent for step execution.

Agent Name: {agent_name}
Pipeline Context: Step {step_index} of {total_steps}
Input From: {input_source} → {input_format}
Output To: {output_target} → {output_format}
Purpose: {purpose}
Required Tools: {tools}

PIPELINE AGENT STRUCTURE:
The agent must be intelligent about pipeline data flow and format compatibility.

```python
async def {agent_name}(state):
    '''
    Pipeline Step {step_index}: {purpose}
    Input: {input_format} from {input_source}
    Output: {output_format} for {output_target}
    '''
    
    # Initialize results structure
    if 'results' not in state:
        state['results'] = {{}}
    if 'errors' not in state:
        state['errors'] = []
    if 'execution_path' not in state:
        state['execution_path'] = []
    
    try:
        # SMART INPUT EXTRACTION from pipeline state
        pipeline_context = state.get('pipeline_context', {{}})
        step_index = pipeline_context.get('step_index', {step_index})
        
        # Extract input data based on pipeline context
        if step_index == 0:
            # First step - get data from user input
            input_data = state.get('current_data', {{}})
        else:
            # Later step - get data from previous step results
            input_data = state.get('current_data')
            if input_data is None:
                previous_results = pipeline_context.get('previous_results', {{}})
                if previous_results:
                    # Get the most recent result
                    latest_result = list(previous_results.values())[-1]
                    input_data = latest_result.get('data', {{}})
        
        # Validate input format
        if not input_data:
            raise ValueError("No input data available for pipeline step")
        
        # CORE PROCESSING LOGIC with tools
        # [Agent-specific processing logic will be generated here]
        processed_data = input_data  # Placeholder for actual processing
        
        # SMART OUTPUT FORMATTING for next step
        result = {{
            'status': 'success',
            'data': processed_data,
            'metadata': {{
                'agent': '{agent_name}',
                'step_index': step_index,
                'pipeline_step': True,
                'input_format': '{input_format}',
                'output_format': '{output_format}',
                'execution_time': 0.0  # Will be calculated
            }}
        }}
        
        # Update pipeline state
        state['results']['{agent_name}'] = result
        state['execution_path'].append('{agent_name}')
        state['current_data'] = processed_data
        
        return state
        
    except Exception as e:
        error_info = {{
            'agent': '{agent_name}',
            'step_index': step_index,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }}
        state['errors'].append(error_info)
        
        # Return error state but don't break pipeline
        state['results']['{agent_name}'] = {{
            'status': 'error', 
            'error': str(e),
            'metadata': error_info
        }}
        
        return state
```

CRITICAL REQUIREMENTS:
1. Handle pipeline data flow intelligently
2. Extract input from correct pipeline context
3. Format output for next step compatibility
4. Include comprehensive error handling
5. Update pipeline state correctly
6. Be robust to different input scenarios"""

# Add to config.py
AGENT_SELF_SUFFICIENCY_RULES = {
    "implement_own_logic": True,
    "minimize_tool_dependencies": True,
    "tool_creation_threshold": "high",  # Only create tools for complex operations
    "prefer_inline_implementation": True,
}

# Tool creation criteria
TOOL_CREATION_CRITERIA = {
    "required_for": [
        "external_api_calls",
        "database_connections",
        "specialized_file_formats",  # PDF, Excel
        "network_operations",
        "complex_libraries",  # numpy, pandas operations
    ],
    "not_required_for": [
        "basic_math",
        "string_operations",
        "list_filtering",
        "simple_calculations",
        "pattern_matching",
        "data_parsing",
    ],
}

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

# Validation Settings
REQUIRE_TOOL_TESTS = True  # Tools must pass basic tests
REQUIRE_AGENT_TESTS = True  # Agents must pass basic tests


# ADD THESE FINAL CONFIGURATIONS to config.py at the end:

# =============================================================================
# PIPELINE EXECUTION CONSTRAINTS
# =============================================================================

# Pipeline-specific constraints
MAX_PIPELINE_STEPS = 10  # Maximum steps in a pipeline
PIPELINE_TIMEOUT_SECONDS = 120  # Total pipeline timeout
STEP_TIMEOUT_SECONDS = 30  # Individual step timeout
MAX_PIPELINE_RETRIES = 3  # Maximum retry attempts for failed pipelines

# Pipeline intelligence settings
ENABLE_PIPELINE_ADAPTATION = True  # Enable real-time adaptation
ENABLE_PIPELINE_MONITORING = True  # Enable step monitoring
PIPELINE_PERFORMANCE_THRESHOLD = 0.8  # Performance threshold for adaptation

# Data flow settings
MAX_DATA_FLOW_DEPTH = 5  # Maximum data transformation depth
ENABLE_DATA_VALIDATION = True  # Validate data between steps
AUTO_FORMAT_CONVERSION = True  # Automatically convert data formats

# =============================================================================
# COMPONENT CREATION SETTINGS
# =============================================================================

# Pipeline agent creation
PIPELINE_AGENT_PREFIX = "pipeline_"  # Prefix for pipeline agents
ADAPTER_AGENT_PREFIX = "adapter_"  # Prefix for data adapter agents
RECOVERY_AGENT_PREFIX = "recovery_"  # Prefix for recovery agents

# Dynamic creation limits
MAX_AGENTS_PER_PIPELINE = 8  # Maximum agents created per pipeline
MAX_TOOLS_PER_PIPELINE = 12  # Maximum tools created per pipeline
AGENT_CREATION_TIMEOUT = 30  # Timeout for agent creation

# =============================================================================
# MONITORING AND ANALYTICS
# =============================================================================

# Performance monitoring
MONITOR_EXECUTION_TIMES = True  # Track execution times
MONITOR_SUCCESS_RATES = True  # Track success rates
MONITOR_RESOURCE_USAGE = True  # Track resource usage

# Analytics retention
ANALYTICS_RETENTION_DAYS = 30  # Days to retain analytics data
MAX_WORKFLOW_HISTORY = 1000  # Maximum workflows in history
CLEANUP_INTERVAL_HOURS = 24  # Hours between cleanup runs

# =============================================================================
# ERROR HANDLING AND RECOVERY
# =============================================================================

# Recovery strategies
ENABLE_AUTO_RECOVERY = True  # Enable automatic recovery
MAX_RECOVERY_ATTEMPTS = 2  # Maximum recovery attempts per step
RECOVERY_TIMEOUT_SECONDS = 20  # Timeout for recovery operations

# Fallback behaviors
ENABLE_GRACEFUL_DEGRADATION = True  # Enable graceful failure handling
PROVIDE_PARTIAL_RESULTS = True  # Provide partial results on failure
FALLBACK_TO_SIMPLE_MODE = True  # Fallback to simple processing

# =============================================================================
# DEBUGGING AND DEVELOPMENT
# =============================================================================

# Pipeline debugging
DEBUG_PIPELINE_EXECUTION = True  # Enable pipeline execution debugging
LOG_PIPELINE_STATE_CHANGES = True  # Log state changes
SAVE_PIPELINE_ARTIFACTS = False  # Save intermediate artifacts (dev only)

# Performance profiling
ENABLE_PERFORMANCE_PROFILING = False  # Enable detailed performance profiling
PROFILE_AGENT_EXECUTION = False  # Profile individual agent execution
PROFILE_DATA_FLOW = False  # Profile data flow between steps

# =============================================================================
# PIPELINE PROMPT TEMPLATES (CONTINUED)
# =============================================================================

# Additional prompt for edge cases
PIPELINE_EDGE_CASE_PROMPT = """Handle edge cases in pipeline execution.

EDGE CASE DETECTED: {edge_case_type}
CURRENT STATE: {current_state}
ERROR CONTEXT: {error_context}

EDGE CASE HANDLING:
1. Analyze the specific edge case type
2. Determine if recovery is possible
3. Plan appropriate handling strategy
4. Ensure pipeline flow continues

COMMON EDGE CASES:
- Empty or null input data
- Unexpected data formats
- Missing required fields
- Tool execution failures
- Timeout scenarios

OUTPUT FORMAT - Respond with valid JSON:
{{
    "edge_case_analysis": {{
        "type": "data_format|missing_data|tool_failure|timeout|unknown",
        "severity": "low|medium|high|critical",
        "recoverable": true,
        "handling_strategy": "retry|fallback|skip|create_alternative"
    }},
    "recommended_action": {{
        "action_type": "immediate|delayed|manual_intervention",
        "description": "specific action to take",
        "estimated_time": 10,
        "success_probability": 0.75
    }},
    "fallback_options": [
        {{
            "option": "provide_default_data",
            "description": "use safe default values",
            "impact": "minimal|moderate|significant"
        }}
    ],
    "prevention_suggestions": [
        "add input validation",
        "improve error handling"
    ]
}}"""

# Template for data format issues
DATA_FORMAT_RESOLUTION_PROMPT = """Resolve data format compatibility issues in pipeline.

FORMAT MISMATCH: {format_issue}
SOURCE FORMAT: {source_format}
TARGET FORMAT: {target_format}
DATA SAMPLE: {data_sample}

RESOLUTION INSTRUCTIONS:
1. Analyze the format mismatch
2. Determine conversion strategy
3. Plan data transformation steps
4. Ensure no data loss

OUTPUT FORMAT - Respond with valid JSON:
{{
    "conversion_strategy": {{
        "strategy_type": "direct_conversion|multi_step|custom_adapter",
        "complexity": "simple|moderate|complex",
        "data_loss_risk": "none|minimal|moderate|high"
    }},
    "transformation_steps": [
        {{
            "step": 1,
            "operation": "validate_input",
            "description": "check input data validity"
        }},
        {{
            "step": 2,
            "operation": "convert_format",
            "description": "perform actual conversion"
        }}
    ],
    "adapter_spec": {{
        "name": "format_adapter_name",
        "description": "converts {source_format} to {target_format}",
        "tools_needed": ["converter_tool", "validator_tool"]
    }},
    "validation_checks": [
        "verify_data_integrity",
        "check_required_fields"
    ]
}}"""

# =============================================================================
# SYSTEM INTEGRATION SETTINGS
# =============================================================================

# Flask integration
FLASK_PIPELINE_ROUTES = True  # Enable pipeline-specific routes
FLASK_ASYNC_SUPPORT = True  # Enable async route support
FLASK_WEBSOCKET_SUPPORT = False  # WebSocket support (future feature)

# API versioning
API_VERSION = "v1"  # Current API version
SUPPORT_LEGACY_API = True  # Support legacy endpoints
API_DEPRECATION_WARNINGS = True  # Show deprecation warnings

# Security settings
PIPELINE_EXECUTION_SANDBOXING = False  # Sandbox pipeline execution (future)
VALIDATE_GENERATED_CODE = True  # Validate generated agent code
LIMIT_RESOURCE_USAGE = True  # Limit resource usage per pipeline

# =============================================================================
# FEATURE FLAGS
# =============================================================================

# Pipeline features
ENABLE_PARALLEL_PIPELINES = False  # Parallel pipeline execution (future)
ENABLE_CONDITIONAL_PIPELINES = False  # Conditional branching (future)
ENABLE_LOOP_PIPELINES = False  # Loop constructs (future)

# Advanced features
ENABLE_PIPELINE_TEMPLATES = False  # Pipeline templates (future)
ENABLE_PIPELINE_SCHEDULING = False  # Scheduled pipelines (future)
ENABLE_PIPELINE_VERSIONING = False  # Pipeline versioning (future)

# Experimental features
EXPERIMENTAL_AI_PLANNING = True  # Advanced AI-driven planning
EXPERIMENTAL_AUTO_OPTIMIZATION = False  # Automatic pipeline optimization
EXPERIMENTAL_PREDICTIVE_SCALING = False  # Predictive resource scaling

# =============================================================================
# DOCUMENTATION AND HELP
# =============================================================================

# Help text for pipeline features
PIPELINE_HELP_TEXT = """
Pipeline Processing Help:

SIMPLE REQUESTS: Single-step processing
- "Extract emails from this text"
- "Analyze this CSV file"

PIPELINE REQUESTS: Multi-step processing  
- "Extract emails from this document, then count unique domains"
- "Read this CSV, calculate statistics, then create a chart"

COMPLEX REQUESTS: Advanced multi-step with adaptation
- "Compare data from multiple files and generate a comprehensive report"
- "Process these documents, extract key information, and create a presentation"

FEATURES:
✓ Automatic pipeline detection
✓ Dynamic agent creation
✓ Real-time adaptation
✓ Intelligent error recovery
✓ Performance monitoring

For more help, visit: /help/pipelines
"""

# Error messages
PIPELINE_ERROR_MESSAGES = {
    "analysis_failed": "Failed to analyze your request. Please try rephrasing or simplifying.",
    "planning_failed": "Could not plan pipeline execution. The request may be too complex.",
    "execution_failed": "Pipeline execution encountered issues. Check error details.",
    "timeout": "Pipeline execution timed out. Consider breaking into smaller requests.",
    "resource_limit": "Resource limits exceeded. Please reduce request complexity.",
    "component_creation_failed": "Failed to create required components. Check system status.",
}

# Success messages
PIPELINE_SUCCESS_MESSAGES = {
    "completed": "Pipeline completed successfully!",
    "partial": "Pipeline completed with partial results.",
    "adapted": "Pipeline completed with intelligent adaptations.",
    "recovered": "Pipeline recovered from issues and completed.",
    "optimized": "Pipeline execution was optimized for better performance.",
}
# =============================================================================
