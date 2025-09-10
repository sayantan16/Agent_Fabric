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
**Results Found:**
[List actual extracted data clearly based on what agents returned]

**Issues (if any):**
[List specific problems, empty results, or missing data based on actual agent outputs]

**Generated Files (if any):**
[Download Filename](/api/download/filename) - Description from agent metadata

**Process Summary:**
Used [actual_agent_names] agents | Execution time: [actual_time]s

IMPORTANT RULES:
- Never invent data that wasn't returned by agents
- Never assume what results mean without looking at actual values
- If results are missing or empty, explain this honestly
- Always base your response on the actual execution results provided
- For generated files, use the exact filename and path provided by agents
- Be conversational but factually accurate to the agent outputs
- Show the specific data values that were extracted, not generic descriptions
- If an agent returned empty arrays or null values, state this clearly
- Match your response format to what the user actually requested (extraction, analysis, calculation, etc.)

SITUATIONAL HANDLING GUIDELINES:
- **Complete Success**: When all agents returned expected data, show all results clearly and concisely
- **Partial Success**: When some agents succeeded and others failed, clearly separate what worked from what didn't
- **Extraction Tasks**: Show exactly what was found vs what was requested, include counts and specific values
- **Calculation Tasks**: Show the actual computed values, intermediate steps if relevant, and final answers
- **Analysis Tasks**: Present the actual analysis results, insights, and any generated reports or summaries
- **File Processing**: If files were processed, show what was extracted/analyzed and any generated outputs
- **Empty Results**: When agents return empty arrays, null values, or zero counts, explain this clearly without apologizing
- **Error Recovery**: If agents failed but pipeline continued, explain what was attempted and what succeeded
- **Multi-Step Workflows**: Trace the data flow between steps, showing how results from one agent fed into the next
- **Data Transformation**: When agents transform data between steps, show both input and output formats clearly
- **Quality Assessment**: If results seem incomplete or unexpected, note this based on the actual data returned
- **Performance Reporting**: Include actual execution times and which specific agents contributed to each result

CRITICAL: Your response must be based ONLY on the actual agent execution data provided in the results section. Handle each pipeline outcome based on what actually happened, not what should have happened.
"""

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
# PIPELINE ORCHESTRATION PROMPTS
# =============================================================================

PIPELINE_ANALYSIS_PROMPT = """Analyze this complex request and break it into a logical pipeline of steps.

REQUEST: {request}
FILES: {files}

AVAILABLE AGENTS:
{available_agents}

AVAILABLE TOOLS:
{available_tools}

ANALYSIS INSTRUCTIONS:
1. Identify the main goal and break it into sequential steps
2. For each step, determine what processing is needed
3. Define input/output requirements for each step
4. Consider data flow between steps
5. Identify any parallel processing opportunities

IMPORTANT: Look at each agent's ACTUAL capabilities:
- What tools they use
- What they're designed for
- Their input/output types

Create steps that match EXISTING agent capabilities. Don't assume agents can do things they're not designed for.

For each step, specify:
- EXACT agent requirements
- Required tools
- Input/output data types
- Why this specific capability is needed


OUTPUT FORMAT - Respond with valid JSON:
{{
    "analysis_type": "pipeline",
    "complexity": "simple|moderate|complex",
    "total_steps": 3,
    "execution_strategy": "sequential|parallel|hybrid",
    "steps": [
        {{
            "name": "step_1_descriptive_name",
            "description": "What this step accomplishes",
            "input_requirements": {{
                "type": "text|data|file|array",
                "format": "specific format expected",
                "source": "user_input|previous_step|file"
            }},
            "output_requirements": {{
                "type": "text|data|file|array", 
                "format": "specific format produced",
                "destination": "next_step|final_output"
            }},
            "required_capabilities": ["extraction", "analysis", "transformation"],
            "estimated_time": 5
        }}
    ],
    "data_flow": {{
        "linear": true,
        "parallel_opportunities": [],
        "dependencies": []
    }},
    "confidence": 0.85
}}

IMPORTANT:
- Each step should have clear input/output requirements
- Consider how data flows from one step to the next
- Be specific about what processing each step needs
- Identify opportunities for parallel execution"""

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

DYNAMIC_AGENT_SPEC_PROMPT = """Design a pipeline-aware agent for this specific step.

STEP DESCRIPTION: {step_description}
STEP INDEX: {step_index}
INPUT REQUIREMENTS: {input_requirements}
OUTPUT REQUIREMENTS: {output_requirements}
AVAILABLE TOOLS: {available_tools}

AGENT DESIGN INSTRUCTIONS:
1. Create an agent specifically for this pipeline step
2. Ensure it handles the exact input format from previous step
3. Ensure it produces the exact output format for next step
4. Include appropriate error handling and edge cases
5. Make it robust and reliable

OUTPUT FORMAT - Respond with valid JSON:
{{
    "name": "pipeline_step_{step_index}_descriptive_name",
    "description": "Detailed description of what this agent does",
    "input_specification": {{
        "expected_format": "exact format this agent expects",
        "validation_rules": ["rule1", "rule2"],
        "edge_cases": ["case1", "case2"]
    }},
    "output_specification": {{
        "output_format": "exact format this agent produces", 
        "data_structure": "detailed structure description",
        "success_indicators": ["indicator1", "indicator2"]
    }},
    "required_tools": ["tool1", "tool2"],
    "processing_steps": [
        "step 1: validate input",
        "step 2: process data", 
        "step 3: format output"
    ],
    "error_handling": [
        "invalid input format",
        "processing failures",
        "empty results"
    ],
    "performance_target": {{
        "max_execution_time": 10,
        "memory_usage": "low|medium|high"
    }}
}}"""

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
