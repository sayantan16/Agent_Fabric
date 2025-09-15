# AGENTIC FABRIC POC - COMPLETE PROJECT KNOWLEDGE BASE
================================================================================
Generated: 2025-09-14 16:45:39
Project Root: /Users/sayantankundu/Documents/Agent Fabric

## PROJECT OVERVIEW

**Agentic Fabric POC:** Dual-model AI orchestration platform
- GPT: Master orchestrator for strategic decisions
- Claude: Intelligent agent execution engine
- LangGraph: Workflow coordination
- Streamlit: User interface

## PROJECT DIRECTORY STRUCTURE
```
Agent Fabric/
├── core/
│   ├── __init__.py
│   ├── agent_factory.py
│   ├── file_content_reader.py
│   ├── intelligent_agent_base.py
│   ├── pipeline_executor.py
│   ├── pipeline_orchestrator.py
│   ├── registry.py
│   ├── registry_singleton.py
│   ├── simplified_orchestrator.py
│   ├── specialized_agents.py
│   ├── tool_factory.py
│   └── workflow_engine.py
├── generated/
│   ├── agents/
│   │   ├── email_extractor_agent.py
│   │   ├── read_csv_agent.py
│   │   └── read_text_agent.py
│   ├── tools/
│   │   ├── analyze_sentiment.py
│   │   ├── calculate_mean.py
│   │   ├── extract_emails.py
│   │   ├── extract_phones.py
│   │   └── extract_urls.py
│   └── __init__.py
├── prebuilt/
│   ├── agents/
│   └── tools/
├── registry_backups/
├── KNOWLEDGE_BASE.md
├── README.md
├── agents.json
├── agents.json.lock
├── config.py
├── create_knowledge_base.py
├── requirements.txt
├── test_current_setup.py
├── test_enhanced_system.py
├── test_orchestrator.py
├── tools.json
└── tools.json.lock
```

## COMPLETE FILE CONTENTS

### File: .env.template
**Path:** `.env.template`
**Size:** 218 bytes
**Modified:** 2025-09-02 19:36:06

*[Binary file or content not included]*

--------------------------------------------------------------------------------

### File: .gitignore
**Path:** `.gitignore`
**Size:** 852 bytes
**Modified:** 2025-09-03 18:36:36

*[Binary file or content not included]*

--------------------------------------------------------------------------------

### File: KNOWLEDGE_BASE.md
**Path:** `KNOWLEDGE_BASE.md`
**Size:** 0 bytes
**Modified:** 2025-09-14 16:45:15

```markdown

```

--------------------------------------------------------------------------------

### File: README.md
**Path:** `README.md`
**Size:** 811 bytes
**Modified:** 2025-09-02 19:31:54

```markdown
# Agentic Fabric - Dynamic Multi-Agent Orchestration Platform

## Overview
A revolutionary POC that demonstrates dynamic AI agent creation and orchestration through natural language requests.

## Architecture
- **GPT-4 Orchestrator**: Understands requests and plans workflows
- **Claude Agent Factory**: Creates new agents and tools on-demand
- **LangGraph Engine**: Executes multi-agent workflows
- **Dual Registry**: Tracks reusable agents and tools

## Directory Structure
- `core/`: Core orchestration and factory components
- `generated/agents/`: Dynamically created agents
- `generated/tools/`: Dynamically created utility functions
- `agents.json`: Registry of available agents
- `tools.json`: Registry of available tools

## Status
POC in active development - implementing dynamic agent creation system.
```

--------------------------------------------------------------------------------

### File: agents.json
**Path:** `agents.json`
**Size:** 5,057 bytes
**Modified:** 2025-09-12 18:40:22

```json
{
  "agents": {
    "email_extractor": {
      "name": "email_extractor",
      "description": "Extracts email addresses from text input",
      "uses_tools": ["extract_emails"],
      "input_schema": {
        "data": "any"
      },
      "output_schema": {
        "status": "string",
        "data": {
          "emails": "array",
          "count": "integer",
          "domains": "object"
        },
        "metadata": "object"
      },
      "location": "generated/agents/email_extractor_agent.py",
      "is_prebuilt": false,
      "created_by": "claude-3-haiku-20240307",
      "created_at": "2025-01-01T00:00:00",
      "version": "1.0.0",
      "execution_count": 4,
      "avg_execution_time": 0.001,
      "tags": ["extraction", "emails"],
      "line_count": 98,
      "status": "active",
      "last_executed": "2025-09-08T23:58:52.927352",
      "dependencies": {
        "tools": ["extract_emails"],
        "missing_tools": [],
        "available_tools": ["extract_emails"]
      },
      "formatted_created_at": "2025-01-01 00:00:00"
    },
    "read_text": {
      "name": "read_text",
      "description": "Process read_text tasks",
      "uses_tools": [],
      "input_schema": {
        "type": "any",
        "description": "Flexible input"
      },
      "output_schema": {
        "type": "object",
        "required": ["status", "data", "metadata"],
        "properties": {
          "status": {
            "type": "string",
            "enum": ["success", "error", "partial"]
          },
          "data": {
            "type": ["object", "array", "null"],
            "description": "Agent-specific output data"
          },
          "metadata": {
            "type": "object",
            "required": ["agent", "execution_time"],
            "properties": {
              "agent": {
                "type": "string"
              },
              "execution_time": {
                "type": "number"
              },
              "tools_used": {
                "type": "array",
                "items": {
                  "type": "string"
                }
              },
              "errors": {
                "type": "array",
                "items": {
                  "type": "string"
                }
              },
              "warnings": {
                "type": "array",
                "items": {
                  "type": "string"
                }
              }
            }
          }
        }
      },
      "location": "/Users/sayantankundu/Documents/Agent Fabric/generated/agents/read_text_agent.py",
      "is_prebuilt": false,
      "created_by": "claude-3-haiku-20240307",
      "created_at": "2025-09-04T12:21:19.499192",
      "version": "1.0.5378b632",
      "execution_count": 0,
      "avg_execution_time": 0.0,
      "last_executed": null,
      "tags": [],
      "line_count": 105,
      "status": "active",
      "dependencies": {
        "tools": [],
        "missing_tools": [],
        "available_tools": []
      },
      "formatted_created_at": "2025-09-04 12:21:19"
    },
    "read_csv": {
      "name": "read_csv",
      "description": "Process read_csv tasks",
      "uses_tools": [],
      "input_schema": {
        "type": "any",
        "description": "Flexible input"
      },
      "output_schema": {
        "type": "object",
        "required": ["status", "data", "metadata"],
        "properties": {
          "status": {
            "type": "string",
            "enum": ["success", "error", "partial"]
          },
          "data": {
            "type": ["object", "array", "null"],
            "description": "Agent-specific output data"
          },
          "metadata": {
            "type": "object",
            "required": ["agent", "execution_time"],
            "properties": {
              "agent": {
                "type": "string"
              },
              "execution_time": {
                "type": "number"
              },
              "tools_used": {
                "type": "array",
                "items": {
                  "type": "string"
                }
              },
              "errors": {
                "type": "array",
                "items": {
                  "type": "string"
                }
              },
              "warnings": {
                "type": "array",
                "items": {
                  "type": "string"
                }
              }
            }
          }
        }
      },
      "location": "/Users/sayantankundu/Documents/Agent Fabric/generated/agents/read_csv_agent.py",
      "is_prebuilt": false,
      "created_by": "claude-3-haiku-20240307",
      "created_at": "2025-09-04T17:23:07.642851",
      "version": "1.0.71318251",
      "execution_count": 0,
      "avg_execution_time": 0.0,
      "last_executed": null,
      "tags": [],
      "line_count": 108,
      "status": "active",
      "dependencies": {
        "tools": [],
        "missing_tools": [],
        "available_tools": []
      },
      "formatted_created_at": "2025-09-04 17:23:07"
    }
  }
}

```

--------------------------------------------------------------------------------

### File: agents.json.lock
**Path:** `agents.json.lock`
**Size:** 0 bytes
**Modified:** 2025-09-12 14:42:15

*[Binary file or content not included]*

--------------------------------------------------------------------------------

### File: config.py
**Path:** `config.py`
**Size:** 58,796 bytes
**Modified:** 2025-09-14 09:31:03

```python
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

```

--------------------------------------------------------------------------------

### File: core/__init__.py
**Path:** `core/__init__.py`
**Size:** 0 bytes
**Modified:** 2025-09-02 19:29:49

```python

```

--------------------------------------------------------------------------------

### File: core/agent_factory.py
**Path:** `core/agent_factory.py`
**Size:** 51,878 bytes
**Modified:** 2025-09-13 08:15:00

```python
"""
Agent Factory
Dynamically generates intelligent agents using Claude API
"""

from datetime import datetime
from unittest import result
from core.registry import RegistryManager
from config import (
    ANTHROPIC_API_KEY,
    CLAUDE_MODEL,
    CLAUDE_TEMPERATURE,
    CLAUDE_MAX_TOKENS,
    CLAUDE_AGENT_GENERATION_PROMPT,
    MIN_AGENT_LINES,
    MAX_AGENT_LINES,
    AGENT_VALIDATION_RULES,
    AGENT_OUTPUT_SCHEMA,
    ALLOWED_IMPORTS,
    GENERATED_AGENTS_DIR,
    PREBUILT_AGENTS_DIR,
)
import os
import sys
import ast
import json
import traceback
from typing import Dict, List, Optional, Any, Tuple
from anthropic import Anthropic
from core.registry_singleton import get_shared_registry
from config import PIPELINE_AGENT_TEMPLATE, DYNAMIC_AGENT_SPEC_PROMPT

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class AgentFactory:
    """
    Factory for creating intelligent agents powered by Claude.
    Handles code generation, validation, and registration.
    """

    def __init__(self):
        """Initialize the agent factory."""

        print(f"DEBUG: ANTHROPIC_API_KEY present: {bool(ANTHROPIC_API_KEY)}")
        print(
            f"DEBUG: ANTHROPIC_API_KEY length: {len(ANTHROPIC_API_KEY) if ANTHROPIC_API_KEY else 0}"
        )

        self.client = Anthropic(api_key=ANTHROPIC_API_KEY)
        self.registry = get_shared_registry()
        self.generation_history = []

    def create_agent(
        self,
        agent_name: str,
        description: str,
        required_tools: List[str],
        input_description: str,
        output_description: str,
        workflow_steps: Optional[List[str]] = None,
        auto_create_tools: bool = False,
        is_prebuilt: bool = False,
        tags: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Create a new agent with Claude.
        FIXED: Ensures tools exist before creating agent.
        """

        print(f"DEBUG: create_agent called for '{agent_name}'")
        print(f"DEBUG: API client initialized: {self.client is not None}")

        print(f"DEBUG: Creating agent '{agent_name}' with tools: {required_tools}")

        # Validate agent name
        if not self._validate_agent_name(agent_name):
            return {
                "status": "error",
                "message": f"Invalid agent name: {agent_name}. Use lowercase with underscores only.",
            }

        # Check if agent already exists
        if self.registry.agent_exists(agent_name):
            return {
                "status": "exists",
                "message": f"Agent '{agent_name}' already exists and is active",
                "agent": self.registry.get_agent(agent_name),
            }

        # CRITICAL FIX: Create missing tools BEFORE checking/creating agent
        if auto_create_tools and required_tools:
            from core.tool_factory import ToolFactory

            tool_factory = ToolFactory()

            for tool_name in required_tools:
                if not self.registry.tool_exists(tool_name):
                    print(
                        f"DEBUG: Auto-creating required tool '{tool_name}' for agent '{agent_name}'"
                    )

                    # Infer tool purpose from name and agent context
                    tool_description = self._infer_tool_description(
                        tool_name, agent_name, description
                    )

                    tool_result = tool_factory.ensure_tool(
                        tool_name=tool_name,
                        description=tool_description,
                        tool_type="pure_function",
                    )

                    if tool_result["status"] not in ["success", "exists"]:
                        print(
                            f"WARNING: Failed to create tool '{tool_name}': {tool_result.get('message')}"
                        )
                        # Continue anyway - agent might work without all tools

        # Now check for missing tools after creation attempt
        missing_tools = self._check_missing_tools(required_tools)

        if missing_tools and not auto_create_tools:
            return {
                "status": "missing_tools",
                "message": f"Required tools not found: {', '.join(missing_tools)}",
                "missing_tools": missing_tools,
                "suggestion": "Set auto_create_tools=True to create them automatically",
            }

        # Generate the agent code
        generation_result = self._generate_agent_code(
            agent_name=agent_name,
            description=description,
            required_tools=required_tools,
            input_description=input_description,
            output_description=output_description,
            workflow_steps=workflow_steps,
        )

        if generation_result["status"] != "success":
            return generation_result

        code = generation_result["code"]

        # Validate the generated code
        validation_result = self._validate_agent_code(code, agent_name)

        if not validation_result["valid"]:
            # Try to fix common issues
            fixed_code = self._attempt_code_fixes(code, validation_result["issues"])
            if fixed_code:
                code = fixed_code
                validation_result = self._validate_agent_code(code, agent_name)

                if not validation_result["valid"]:
                    return {
                        "status": "validation_error",
                        "message": "Generated code failed validation after fixes",
                        "validation_errors": validation_result["issues"],
                        "code": code,
                    }
            else:
                return {
                    "status": "validation_error",
                    "message": "Generated code failed validation",
                    "validation_errors": validation_result["issues"],
                    "code": code,
                }

        # Extract metadata from code
        metadata = self._extract_metadata(code)

        # Register the agent
        registration_result = self.registry.register_agent(
            name=agent_name,
            description=description,
            code=code,
            uses_tools=required_tools,
            input_schema={"type": "any", "description": input_description},
            output_schema=AGENT_OUTPUT_SCHEMA,
            tags=tags or metadata.get("tags", []),
            is_prebuilt=is_prebuilt,
        )

        if registration_result["status"] != "success":
            return registration_result

        # Force all components to reload registry after successful creation
        from core.registry_singleton import RegistrySingleton

        RegistrySingleton().force_reload()
        print(f"DEBUG: Forced registry reload after creating '{agent_name}'")

        # Record generation history
        self.generation_history.append(
            {
                "agent_name": agent_name,
                "timestamp": metadata.get("created_at"),
                "tools_used": required_tools,
                "line_count": len(code.splitlines()),
            }
        )

        print(f"DEBUG: create_agent returning with status: {agent_name}")

        return {
            "status": "success",
            "message": f"Agent '{agent_name}' created successfully",
            "agent_name": agent_name,
            "location": registration_result["location"],
            "line_count": registration_result["line_count"],
            "code": code,
        }

    def _generate_agent_code(
        self,
        agent_name: str,
        description: str,
        required_tools: List[str],
        input_description: str,
        output_description: str,
        workflow_steps: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Generate agent code using Claude."""
        # Build tool imports section
        tool_imports = self._build_tool_imports(required_tools)

        # Build agent logic section
        if workflow_steps:
            agent_logic = self._build_workflow_logic(workflow_steps, required_tools)
        else:
            agent_logic = self._build_default_logic(required_tools)

        # Format the prompt
        prompt = CLAUDE_AGENT_GENERATION_PROMPT.format(
            agent_name=agent_name,
            description=description,
            tools=json.dumps(required_tools),
            input_description=input_description,
            output_description=output_description,
            tool_imports=tool_imports,
            agent_logic=agent_logic,
            min_lines=MIN_AGENT_LINES,
            max_lines=MAX_AGENT_LINES,
        )

        try:
            # Call Claude API
            response = self.client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=CLAUDE_MAX_TOKENS,
                messages=[{"role": "user", "content": prompt}],
            )

            print(f"DEBUG: Claude API response received")

            # Extract code from response
            raw_response = response.content[0].text
            print(f"DEBUG: Raw response length: {len(raw_response)}")

            code = self._extract_code_from_response(raw_response)

            if not code:
                print(f"DEBUG: No code extracted from Claude response")
                print(f"DEBUG: First 500 chars of response: {raw_response[:500]}")
                print(f"DEBUG: Raw Claude response:")
                print(f"{'='*50}")
                print(
                    raw_response[:1000] + "..."
                    if len(raw_response) > 1000
                    else raw_response
                )
                print(f"{'='*50}")
                return {
                    "status": "error",
                    "message": "No valid Python code found in Claude response",
                }

            print(
                f"DEBUG: Successfully extracted {len(code.splitlines())} lines of code"
            )
            return {"status": "success", "code": code}

        except Exception as e:
            return {
                "status": "error",
                "message": f"Claude API error: {str(e)}",
                "traceback": traceback.format_exc(),
            }

    def _validate_agent_code(self, code: str, agent_name: str) -> Dict[str, Any]:
        """
        Comprehensive validation of agent code.

        Args:
            code: Python code to validate
            agent_name: Expected agent name

        Returns:
            Validation result with issues if any
        """
        issues = []

        # Check syntax
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return {"valid": False, "issues": [f"Syntax error: {str(e)}"]}

        # Check structure
        if not tree.body or not isinstance(tree.body[0], ast.FunctionDef):
            issues.append("Code must define a function")
            return {"valid": False, "issues": issues}

        func_def = tree.body[0]

        # Check function name - FIXED: Allow both patterns
        expected_names = [f"{agent_name}_agent", agent_name]
        if func_def.name not in expected_names:
            issues.append(f"Function name must be one of: {expected_names}")

        # Check function parameters
        if not func_def.args.args or func_def.args.args[0].arg != "state":
            issues.append('Function must accept "state" as first parameter')

        # Check for output envelope structure (more flexible)
        has_status = any(word in code for word in ['"status"', "'status'", "status"])
        has_data = any(word in code for word in ['"data"', "'data'", "data"])
        has_metadata = any(
            word in code for word in ['"metadata"', "'metadata'", "metadata"]
        )

        if not has_status:
            issues.append("Missing status field in output")
        if not has_data:
            issues.append("Missing data field in output")
        if not has_metadata:
            issues.append("Missing metadata field in output")

        # Check essential patterns
        essential_patterns = [
            "if 'results' not in state",
            "if 'errors' not in state",
            "if 'execution_path' not in state",
            "try:",
            "except Exception as e:",
            "return state",
        ]

        for pattern in essential_patterns:
            if pattern not in code:
                issues.append(f"Missing essential pattern: {pattern}")

        # Check forbidden patterns
        forbidden = ["exec(", "eval(", "__import__", "compile(", "globals(", "locals("]
        for pattern in forbidden:
            if pattern in code:
                issues.append(f"Forbidden pattern found: {pattern}")

        # Check line count
        line_count = len(code.splitlines())
        if line_count < MIN_AGENT_LINES:
            issues.append(
                f"Code too short: {line_count} lines (min: {MIN_AGENT_LINES})"
            )
        elif line_count > MAX_AGENT_LINES:
            issues.append(f"Code too long: {line_count} lines (max: {MAX_AGENT_LINES})")

        result = {"valid": len(issues) == 0, "issues": issues}

        # DEBUG: Show validation details
        if not result["valid"]:
            print(f"DEBUG: Agent validation failed for '{agent_name}'")
            print(f"DEBUG: Validation issues:")
            for i, issue in enumerate(issues, 1):
                print(f"  {i}. {issue}")
            print(f"DEBUG: Generated code preview:")
            print(f"{'='*50}")
            print(code[:500] + "..." if len(code) > 500 else code)
            print(f"{'='*50}")

        return result

    def _attempt_code_fixes(self, code: str, issues: List[str]) -> Optional[str]:
        """
        Attempt to fix common code issues.

        Args:
            code: Code with issues
            issues: List of validation issues

        Returns:
            Fixed code if possible, None otherwise
        """
        fixed_code = code

        # Fix missing return statement
        if any("return state" in issue for issue in issues):
            if not fixed_code.rstrip().endswith("return state"):
                fixed_code = fixed_code.rstrip() + "\n    return state\n"

        # Fix missing state initialization
        if any("results" in issue for issue in issues):
            init_block = """    # Initialize state components
    if 'results' not in state:
        state['results'] = {}
    if 'errors' not in state:
        state['errors'] = []
    if 'execution_path' not in state:
        state['execution_path'] = []
    
"""
            # Insert after function definition
            lines = fixed_code.splitlines()
            for i, line in enumerate(lines):
                if line.strip().startswith("def ") and i + 1 < len(lines):
                    # Find the right place after docstring
                    insert_index = i + 1
                    if i + 1 < len(lines) and (
                        lines[i + 1].strip().startswith('"""')
                        or lines[i + 1].strip().startswith("'''")
                    ):
                        # Skip docstring
                        for j in range(i + 2, len(lines)):
                            if lines[j].strip().endswith('"""') or lines[
                                j
                            ].strip().endswith("'''"):
                                insert_index = j + 1
                                break

                    lines.insert(insert_index, init_block)
                    fixed_code = "\n".join(lines)
                    break

        # Validate the fixed code
        validation = self._validate_agent_code(fixed_code, "temp")
        if validation["valid"] or len(validation["issues"]) < len(issues):
            return fixed_code

        return None

    def _check_missing_tools(self, required_tools: List[str]) -> List[str]:
        """Check which tools are missing from registry."""

        print(f"DEBUG: Checking required tools: {required_tools}")

        missing = []
        for tool in required_tools:
            exists = self.registry.tool_exists(tool)
            print(f"DEBUG: Tool '{tool}' exists: {exists}")
            if not exists:
                missing.append(tool)

        print(f"DEBUG: Missing tools result: {missing}")
        return missing

    def _auto_create_tools(self, tools: List[str]) -> List[Dict[str, Any]]:
        """
        Auto-create missing tools.
        This is a placeholder - in real implementation, would call tool_factory.

        Args:
            tools: List of tool names to create

        Returns:
            List of creation results
        """
        results = []
        for tool_name in tools:
            # This would normally call tool_factory.create_tool()
            # For now, return error
            results.append(
                {
                    "status": "error",
                    "message": f"Auto-creation of tool {tool_name} not implemented",
                }
            )
        return results

    def _build_tool_imports(self, tools: List[str]) -> str:
        """Build tool import statements with proper path resolution."""
        if not tools:
            return "# No tools to import"

        imports = []
        for tool in tools:
            tool_info = self.registry.get_tool(tool)

            # Build flexible import that checks multiple locations
            import_code = f"""
        # Import {tool} tool
        try:
            from generated.tools.{tool} import {tool}
        except ImportError:
            try:
                from prebuilt.tools.{tool} import {tool}
            except ImportError:
                # Define fallback if tool not found
                def {tool}(input_data=None):
                    return {{'error': 'Tool {tool} not found', 'data': None}}"""

            imports.append(import_code)

        return "\n".join(imports)

    def _build_workflow_logic(self, steps: List[str], tools: List[str]) -> str:
        """Build workflow logic from steps."""
        logic = []
        logic.append("# Execute workflow steps")
        for i, step in enumerate(steps):
            logic.append(f"# Step {i + 1}: {step}")
            # Add placeholder for actual logic
            logic.append(f"# TODO: Implement {step}")

        logic.append("")
        logic.append("# Process with tools")
        for tool in tools:
            logic.append(f"# result = {tool}(input_data)")

        logic.append("")
        logic.append("# Format output")
        logic.append("processed_data = {}")

        return "\n        ".join(logic)

    def _build_default_logic(self, tools: List[str]) -> str:
        """Build default agent logic."""
        logic = []
        logic.append("# Process input data")

        if tools:
            logic.append("# Apply tools to input data")
            logic.append("processed_data = {}")
            for tool in tools:
                logic.append(f"tool_result = {tool}(input_data)")
                logic.append(f"processed_data['{tool}_result'] = tool_result")
        else:
            logic.append("# No tools specified - process input directly")
            logic.append("if isinstance(input_data, str):")
            logic.append(
                "    processed_data = {'processed_text': input_data, 'length': len(input_data)}"
            )
            logic.append("elif isinstance(input_data, dict):")
            logic.append("    processed_data = {'processed_data': input_data}")
            logic.append("else:")
            logic.append(
                "    processed_data = {'result': str(input_data) if input_data else 'No input provided'}"
            )

        return "\n        ".join(logic)

    def _extract_code_from_response(self, response: str) -> Optional[str]:
        """Extract Python code from Claude's response."""
        # Handle markdown code blocks
        if "```python" in response:
            start = response.find("```python") + 9
            end = response.find("```", start)
            if end > start:
                return response[start:end].strip()

        # Handle generic code blocks
        if "```" in response:
            start = response.find("```") + 3
            # Skip language identifier if present
            if response[start : start + 10].strip().startswith(("python", "py")):
                start = response.find("\n", start) + 1
            end = response.find("```", start)
            if end > start:
                code = response[start:end].strip()
                if code.startswith("def "):
                    return code

        # Try to find function definition directly
        if "def " in response:
            start = response.find("def ")
            # Find the end of the function (next def or end of string)
            next_def = response.find("\ndef ", start + 1)
            if next_def > 0:
                return response[start:next_def].strip()
            else:
                return response[start:].strip()

        return None

    def _extract_metadata(self, code: str) -> Dict[str, Any]:
        """Extract metadata from generated code."""
        metadata = {
            "line_count": len(code.splitlines()),
            "has_docstring": '"""' in code or "'''" in code,
            "imports": [],
            "tags": [],
        }

        try:
            tree = ast.parse(code)

            # Extract imports
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        metadata["imports"].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        metadata["imports"].append(node.module)

            # Extract tags from docstring
            if tree.body and isinstance(tree.body[0], ast.FunctionDef):
                docstring = ast.get_docstring(tree.body[0])
                if docstring:
                    # Simple tag extraction from docstring
                    for line in docstring.lower().split("\n"):
                        if "tag" in line or "category" in line:
                            words = line.split()
                            metadata["tags"].extend(
                                [
                                    w.strip(",:")
                                    for w in words
                                    if len(w) > 3 and w.isalpha()
                                ]
                            )

        except:
            pass

        return metadata

    def _validate_agent_name(self, name: str) -> bool:
        """Validate agent name format."""
        import re

        # Allow lowercase letters, numbers, and underscores
        pattern = r"^[a-z][a-z0-9_]*$"
        return bool(re.match(pattern, name))

    def get_generation_history(self) -> List[Dict[str, Any]]:
        """Get history of generated agents."""
        return self.generation_history.copy()

    def regenerate_agent(
        self, agent_name: str, modifications: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Regenerate an existing agent with modifications.

        Args:
            agent_name: Name of agent to regenerate
            modifications: Dict of modifications to apply

        Returns:
            Result of regeneration
        """
        # Get existing agent
        existing = self.registry.get_agent(agent_name)
        if not existing:
            return {"status": "error", "message": f"Agent '{agent_name}' not found"}

        # Apply modifications
        description = modifications.get("description", existing["description"])
        tools = modifications.get("tools", existing["uses_tools"])
        input_desc = modifications.get("input_description", "Modified input")
        output_desc = modifications.get("output_description", "Modified output")

        # Mark old agent as deprecated
        self.registry.agents["agents"][agent_name]["status"] = "deprecated"
        self.registry.save_all()

        # Create new version
        return self.create_agent(
            agent_name=f"{agent_name}_v2",
            description=description,
            required_tools=tools,
            input_description=input_desc,
            output_description=output_desc,
            tags=[f"regenerated_from_{agent_name}"],
        )

    def _infer_tool_description(
        self, tool_name: str, agent_name: str, agent_description: str
    ) -> str:
        """Infer tool description from context."""

        # Common tool patterns
        if "extract" in tool_name:
            if "email" in tool_name:
                return "Extract email addresses from text using regex patterns"
            elif "phone" in tool_name:
                return "Extract phone numbers from text using regex patterns"
            elif "url" in tool_name:
                return "Extract URLs from text using regex patterns"
            else:
                return f"Extract {tool_name.replace('extract_', '').replace('_', ' ')} from input data"

        elif "calculate" in tool_name:
            metric = tool_name.replace("calculate_", "").replace("_", " ")
            return f"Calculate {metric} from numerical data"

        elif "format" in tool_name:
            return f"Format data for {tool_name.replace('format_', '').replace('_', ' ')} output"

        elif "generate" in tool_name:
            return f"Generate {tool_name.replace('generate_', '').replace('_', ' ')} from input data"

        elif "validate" in tool_name:
            return f"Validate {tool_name.replace('validate_', '').replace('_', ' ')} according to rules"

        else:
            # Generic description based on agent context
            return f"Tool for {agent_description.lower()} - processes data for {agent_name}"

    def ensure_agent(
        self, agent_name: str, description: str, required_tools: List[str]
    ) -> Dict[str, Any]:
        """
        Ensure an agent exists - create only if missing (idempotent).
        FIXED: Properly handles tool dependencies.
        """
        # Check if exists
        if self.registry.agent_exists(agent_name):
            return {"status": "exists", "agent": self.registry.get_agent(agent_name)}

        # Create with auto tool creation enabled
        return self.create_agent(
            agent_name=agent_name,
            description=description,
            required_tools=required_tools,
            input_description="Flexible input - can be string, dict, or list",
            output_description="Standard envelope with data specific to the task",
            auto_create_tools=True,  # CRITICAL: Enable auto tool creation
        )

    def create_pipeline_agent(self, spec: Dict) -> Dict[str, Any]:
        """Create agent specifically designed for pipeline execution."""

        agent_name = spec.get(
            "name", f"pipeline_agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )

        # FIX: Convert to lowercase to match validation requirements
        agent_name = agent_name.lower()

        description = spec.get("description", "Pipeline processing agent")
        required_tools = spec.get("required_tools", [])

        print(f"DEBUG: Creating pipeline agent: {agent_name}")

        # Extract or generate input/output descriptions from spec
        input_description = spec.get(
            "input_description",
            spec.get("input_requirements", {}).get(
                "description",
                "Pipeline step input - can be any format from previous step or initial data",
            ),
        )

        output_description = spec.get(
            "output_description",
            spec.get("output_requirements", {}).get(
                "description", "Processed output for next pipeline step"
            ),
        )

        # Extract workflow steps if provided
        workflow_steps = spec.get("workflow_steps", None)

        # Enhanced agent creation with pipeline awareness
        pipeline_context = spec.get("pipeline_context", {})

        # Check if agent already exists
        if self.registry.agent_exists(agent_name):
            print(f"DEBUG: Agent {agent_name} already exists")
            return {
                "status": "success",
                "agent": self.registry.get_agent(agent_name),
                "message": "Agent already exists",
            }

        # Create tools first if needed
        new_tools_needed = spec.get("new_tools_needed", [])
        for tool_spec in new_tools_needed:
            if not self.registry.tool_exists(tool_spec.get("name", "")):
                from core.tool_factory import ToolFactory

                tool_factory = ToolFactory()

                tool_result = tool_factory.ensure_tool(
                    tool_name=tool_spec["name"],
                    description=tool_spec.get("description", ""),
                    tool_type="pure_function",
                )

                if tool_result.get("status") == "success":
                    required_tools.append(tool_spec["name"])
                    print(f"DEBUG: Created tool {tool_spec['name']} for agent")

        # Now create the agent with ALL required parameters
        try:
            result = self.create_agent(
                agent_name=agent_name,
                description=description,
                required_tools=required_tools,
                input_description=input_description,  # NOW PROVIDED
                output_description=output_description,  # NOW PROVIDED
                workflow_steps=workflow_steps,
                auto_create_tools=True,  # Allow automatic tool creation
                is_prebuilt=False,
                tags=["pipeline", f"step_{pipeline_context.get('step_index', 0)}"],
            )

            if result["status"] == "success":
                print(f"DEBUG: Pipeline agent '{agent_name}' created successfully")
                # Add pipeline context to registry if needed
                if pipeline_context:
                    agent_data = self.registry.get_agent(agent_name)
                    if agent_data:
                        agent_data["pipeline_context"] = pipeline_context
                        # Update registry with context
                        self.registry.save_all()

            print(
                f"DEBUG: create_agent result for {agent_name}: {result.get('status') if isinstance(result, dict) else 'not a dict'}"
            )
            if result.get("status") != "success":
                print(f"DEBUG: Agent creation failed: {result}")

            return result

        except Exception as e:
            print(f"DEBUG: Failed to create pipeline agent: {str(e)}")
            import traceback

            print(f"DEBUG: Traceback: {traceback.format_exc()}")
            return {
                "status": "error",
                "message": f"Failed to create pipeline agent: {str(e)}",
            }

    async def _generate_pipeline_agent_code(
        self,
        agent_name: str,
        description: str,
        tools: List[str],
        pipeline_context: Dict,
        input_handling: Dict,
    ) -> str:
        """Generate code for pipeline-aware agent."""

        expected_input_type = input_handling.get("expected_type", "Any")
        step_index = pipeline_context.get("step_index", 0)

        template = f'''"""
    {agent_name}: {description}
    Pipeline-aware agent created for step {step_index}
    """

    def {agent_name}_agent(state):
        """
        Pipeline-aware agent that handles {expected_input_type} input.
        
        Expected input type: {expected_input_type}
        Pipeline step: {step_index}
        """
        
        try:
            # Extract data with type checking
            current_data = state.get("current_data")
            
            # Handle different input types intelligently
            if current_data is None:
                # Fallback to request text
                current_data = state.get("request", "")
            
            # Type-specific processing
            if isinstance(current_data, dict):
                # Handle dict input
                processed_data = _process_dict_input(current_data)
            elif isinstance(current_data, list):
                # Handle list input
                processed_data = _process_list_input(current_data)
            elif isinstance(current_data, str):
                # Handle string input
                processed_data = _process_string_input(current_data)
            else:
                # Convert to string for processing
                processed_data = _process_string_input(str(current_data))
            
            # Update state with results
            state["current_data"] = processed_data
            state["results"]["{agent_name}"] = {{
                "status": "success",
                "data": processed_data,
                "agent": "{agent_name}",
                "step_index": {step_index}
            }}
            
            # Add to execution path
            state["execution_path"].append("{agent_name}")
            
            return state
            
        except Exception as e:
            # Robust error handling
            state["errors"].append({{
                "agent": "{agent_name}",
                "error": str(e),
                "step_index": {step_index}
            }})
            
            # Set error result but continue pipeline
            state["results"]["{agent_name}"] = {{
                "status": "error",
                "error": str(e),
                "agent": "{agent_name}",
                "step_index": {step_index}
            }}
            
            return state

    def _process_dict_input(data):
        """Process dictionary input."""
        # Implementation based on agent purpose
        return {{"processed": True, "input_type": "dict", "data": data}}

    def _process_list_input(data):
        """Process list input."""
        # Implementation based on agent purpose  
        return {{"processed": True, "input_type": "list", "count": len(data), "data": data}}

    def _process_string_input(data):
        """Process string input."""
        # Implementation based on agent purpose
        return {{"processed": True, "input_type": "string", "length": len(data), "data": data}}
    '''

        return template

    def _generate_fallback_pipeline_agent(self, agent_spec: Dict[str, Any]) -> str:
        """Generate fallback pipeline agent code."""

        agent_name = agent_spec.get("name", "pipeline_agent")
        description = agent_spec.get("description", "Pipeline agent")
        pipeline_context = agent_spec.get("pipeline_context", {})
        step_index = pipeline_context.get("step_index", 0)

        return f"""
    import json
    import asyncio
    from datetime import datetime
    from typing import Dict, Any, List

    async def {agent_name}(state: Dict[str, Any]) -> Dict[str, Any]:
        '''
        Pipeline Agent: {description}
        Step {step_index} in pipeline execution
        '''
        
        # Initialize state structure
        if 'results' not in state:
            state['results'] = {{}}
        if 'errors' not in state:
            state['errors'] = []
        if 'execution_path' not in state:
            state['execution_path'] = []
        
        try:
            # Extract input data from pipeline context
            pipeline_context = state.get('pipeline_context', {{}})
            step_index = pipeline_context.get('step_index', {step_index})
            
            # Get input data
            if step_index == 0:
                input_data = state.get('current_data', {{}})
            else:
                input_data = state.get('current_data')
                if input_data is None:
                    previous_results = pipeline_context.get('previous_results', {{}})
                    if previous_results:
                        latest_result = list(previous_results.values())[-1]
                        input_data = latest_result.get('data', {{}})
            
            # Validate input
            if not input_data:
                raise ValueError("No input data available for pipeline step")
            
            # BASIC PROCESSING - pass data through with minimal processing
            # This is a fallback implementation
            if isinstance(input_data, dict):
                processed_data = input_data.copy()
                processed_data["processed_by"] = "{agent_name}"
                processed_data["step_index"] = step_index
            elif isinstance(input_data, list):
                processed_data = input_data.copy()
            else:
                processed_data = {{"data": input_data, "processed_by": "{agent_name}"}}
            
            # Create result
            result = {{
                'status': 'success',
                'data': processed_data,
                'metadata': {{
                    'agent': '{agent_name}',
                    'step_index': step_index,
                    'pipeline_step': True,
                    'processing_type': 'fallback',
                    'execution_time': 0.1
                }}
            }}
            
            # Update state
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
            
            state['results']['{agent_name}'] = {{
                'status': 'error',
                'error': str(e),
                'metadata': error_info
            }}
            
            return state
    """

    async def create_data_adapter_agent(
        self, from_format: str, to_format: str, step_context: Dict = None
    ) -> Dict[str, Any]:
        """
        Create an agent that adapts data between pipeline steps.

        Args:
            from_format: Input data format
            to_format: Required output data format
            step_context: Context about the pipeline step

        Returns:
            Creation result for data adapter agent
        """

        step_context = step_context or {}
        adapter_name = (
            f"adapter_{from_format}_to_{to_format}_{datetime.now().strftime('%H%M%S')}"
        )

        print(f"DEBUG: Creating data adapter agent: {adapter_name}")

        # Create adapter specification
        adapter_spec = {
            "name": adapter_name,
            "description": f"Adapt data from {from_format} format to {to_format} format",
            "required_tools": ["format_converter", "data_validator"],
            "pipeline_context": {
                "step_index": step_context.get("step_index", 0),
                "input_format": {"type": from_format},
                "output_format": {"type": to_format},
                "adapter_agent": True,
            },
        }

        # Generate adapter-specific code
        adapter_code = await self._generate_adapter_agent_code(
            from_format, to_format, adapter_name
        )

        # Register the adapter agent
        registration_result = self.registry.register_agent(
            name=adapter_name,
            description=adapter_spec["description"],
            code=adapter_code,
            uses_tools=adapter_spec["required_tools"],
            is_prebuilt=False,
            tags=["adapter", "pipeline", "auto_generated"],
            metadata=adapter_spec["pipeline_context"],
        )

        if registration_result["status"] == "success":
            return {
                "status": "success",
                "agent_name": adapter_name,
                "message": f"Data adapter created: {from_format} → {to_format}",
            }
        else:
            return {
                "status": "error",
                "message": f"Failed to create adapter: {registration_result.get('message')}",
            }

    async def _generate_adapter_agent_code(
        self, from_format: str, to_format: str, agent_name: str
    ) -> str:
        """Generate code for data adapter agent."""

        return f"""
    import json
    from datetime import datetime
    from typing import Dict, Any, List, Union

    async def {agent_name}(state: Dict[str, Any]) -> Dict[str, Any]:
        '''
        Data Adapter Agent: {from_format} → {to_format}
        Converts data between pipeline step formats
        '''
        
        if 'results' not in state:
            state['results'] = {{}}
        if 'errors' not in state:
            state['errors'] = []
        if 'execution_path' not in state:
            state['execution_path'] = []
        
        try:
            # Get input data
            input_data = state.get('current_data')
            
            if input_data is None:
                raise ValueError("No input data to adapt")
            
            # Perform format conversion
            adapted_data = convert_format(input_data, "{from_format}", "{to_format}")
            
            result = {{
                'status': 'success',
                'data': adapted_data,
                'metadata': {{
                    'agent': '{agent_name}',
                    'conversion': '{from_format} → {to_format}',
                    'adapter_agent': True,
                    'execution_time': 0.1
                }}
            }}
            
            state['results']['{agent_name}'] = result
            state['execution_path'].append('{agent_name}')
            state['current_data'] = adapted_data
            
            return state
            
        except Exception as e:
            error_info = {{
                'agent': '{agent_name}',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }}
            state['errors'].append(error_info)
            
            state['results']['{agent_name}'] = {{
                'status': 'error',
                'error': str(e),
                'metadata': error_info
            }}
            
            return state

    def convert_format(data: Any, from_fmt: str, to_fmt: str) -> Any:
        '''Convert data between formats with intelligent handling.'''
        
        try:
            # Handle common format conversions
            if from_fmt == "text" and to_fmt == "list":
                if isinstance(data, str):
                    return data.split('\\n') if '\\n' in data else [data]
                return [str(data)]
            
            elif from_fmt == "list" and to_fmt == "text":
                if isinstance(data, list):
                    return '\\n'.join(str(item) for item in data)
                return str(data)
            
            elif from_fmt == "dict" and to_fmt == "json":
                return json.dumps(data, indent=2)
            
            elif from_fmt == "json" and to_fmt == "dict":
                if isinstance(data, str):
                    return json.loads(data)
                return data
            
            elif to_fmt == "string":
                return str(data)
            
            elif to_fmt == "number" and isinstance(data, str):
                try:
                    return float(data) if '.' in data else int(data)
                except ValueError:
                    return 0
            
            # Default: return data as-is if no specific conversion needed
            return data
            
        except Exception as e:
            print(f"Format conversion failed: {{e}}")
            return data  # Return original data if conversion fails
    """

    async def create_recovery_agent(
        self, failed_agent_name: str, failure_reason: str, step_context: Dict
    ) -> Dict[str, Any]:
        """
        Create a recovery agent to replace a failed pipeline step.

        Args:
            failed_agent_name: Name of the agent that failed
            failure_reason: Reason for the failure
            step_context: Context about the failed step

        Returns:
            Creation result for recovery agent
        """

        recovery_name = (
            f"recovery_{failed_agent_name}_{datetime.now().strftime('%H%M%S')}"
        )

        print(f"DEBUG: Creating recovery agent: {recovery_name}")

        # Get original agent info if available
        original_agent = self.registry.get_agent(failed_agent_name)
        original_description = (
            original_agent.get("description", "Agent processing")
            if original_agent
            else "Failed agent processing"
        )

        # Create recovery specification
        recovery_spec = {
            "name": recovery_name,
            "description": f"Recovery version of {failed_agent_name} - handles: {failure_reason}",
            "required_tools": step_context.get("required_tools", []),
            "pipeline_context": {
                "step_index": step_context.get("step_index", 0),
                "recovery_agent": True,
                "original_agent": failed_agent_name,
                "failure_reason": failure_reason,
                "enhanced_error_handling": True,
            },
        }

        # Generate recovery agent with enhanced error handling
        recovery_code = await self._generate_recovery_agent_code(
            recovery_spec, original_description
        )

        # Register recovery agent
        registration_result = self.registry.register_agent(
            name=recovery_name,
            description=recovery_spec["description"],
            code=recovery_code,
            uses_tools=recovery_spec["required_tools"],
            is_prebuilt=False,
            tags=["recovery", "pipeline", "auto_generated", "enhanced_handling"],
            metadata=recovery_spec["pipeline_context"],
        )

        if registration_result["status"] == "success":
            return {
                "status": "success",
                "agent_name": recovery_name,
                "message": f"Recovery agent created for {failed_agent_name}",
            }
        else:
            return {
                "status": "error",
                "message": f"Failed to create recovery agent: {registration_result.get('message')}",
            }

    async def _generate_recovery_agent_code(
        self, recovery_spec: Dict, original_description: str
    ) -> str:
        """Generate code for recovery agent with enhanced error handling."""

        agent_name = recovery_spec["name"]
        pipeline_context = recovery_spec["pipeline_context"]
        failure_reason = pipeline_context.get("failure_reason", "unknown error")

        return f"""
    import json
    from datetime import datetime
    from typing import Dict, Any, List, Union

    async def {agent_name}(state: Dict[str, Any]) -> Dict[str, Any]:
        '''
        Recovery Agent for Pipeline Step
        Enhanced error handling for: {failure_reason}
        Original purpose: {original_description}
        '''
        
        if 'results' not in state:
            state['results'] = {{}}
        if 'errors' not in state:
            state['errors'] = []
        if 'execution_path' not in state:
            state['execution_path'] = []
        
        try:
            # Enhanced input validation and extraction
            input_data = state.get('current_data')
            
            # Multiple fallback strategies for input data
            if input_data is None:
                pipeline_context = state.get('pipeline_context', {{}})
                previous_results = pipeline_context.get('previous_results', {{}})
                
                if previous_results:
                    # Try to extract from most recent result
                    latest_result = list(previous_results.values())[-1]
                    input_data = latest_result.get('data')
                
                if input_data is None:
                    # Last resort: use request or empty dict
                    input_data = state.get('request', 'No input available')
            
            # Enhanced data processing with multiple strategies
            processed_data = process_data_with_recovery(input_data, "{failure_reason}")
            
            result = {{
                'status': 'success',
                'data': processed_data,
                'metadata': {{
                    'agent': '{agent_name}',
                    'recovery_agent': True,
                    'original_failure': '{failure_reason}',
                    'processing_strategy': 'enhanced_recovery',
                    'execution_time': 0.2
                }}
            }}
            
            state['results']['{agent_name}'] = result
            state['execution_path'].append('{agent_name}')
            state['current_data'] = processed_data
            
            return state
            
        except Exception as e:
            # Enhanced error handling - provide meaningful fallback
            fallback_data = create_fallback_result(state, str(e))
            
            result = {{
                'status': 'success',  # Report success with fallback data
                'data': fallback_data,
                'metadata': {{
                    'agent': '{agent_name}',
                    'recovery_agent': True,
                    'fallback_used': True,
                    'recovery_error': str(e),
                    'execution_time': 0.1
                }}
            }}
            
            state['results']['{agent_name}'] = result
            state['execution_path'].append('{agent_name}')
            state['current_data'] = fallback_data
            
            return state

    def process_data_with_recovery(data: Any, failure_context: str) -> Any:
        '''Process data with enhanced recovery strategies.'''
        
        try:
            # Strategy 1: Handle common data types
            if isinstance(data, str):
                if not data.strip():
                    return {{"message": "Empty input processed", "status": "handled"}}
                return {{"text": data, "processed": True}}
            
            elif isinstance(data, dict):
                if not data:
                    return {{"message": "Empty dict processed", "status": "handled"}}
                return {{"processed_dict": data, "keys": list(data.keys())}}
            
            elif isinstance(data, list):
                if not data:
                    return {{"message": "Empty list processed", "status": "handled"}}
                return {{"processed_list": data, "count": len(data)}}
            
            else:
                return {{"processed_data": str(data), "type": str(type(data))}}
        
        except Exception as e:
            return {{"error_handled": str(e), "recovery_applied": True}}

    def create_fallback_result(state: Dict, error: str) -> Dict[str, Any]:
        '''Create meaningful fallback result when all else fails.'''
        
        return {{
            "status": "fallback_result",
            "message": "Recovery agent provided fallback due to processing issues",
            "original_error": error,
            "request_context": state.get('request', 'Unknown request'),
            "timestamp": datetime.now().isoformat(),
            "recovery_note": "This is a safe fallback result to maintain pipeline flow"
        }}
    """


# ============= END OF NEW METHODS =============

```

--------------------------------------------------------------------------------

### File: core/file_content_reader.py
**Path:** `core/file_content_reader.py`
**Size:** 16,796 bytes
**Modified:** 2025-09-13 12:55:02

```python
"""
File Content Reader
Reads actual file contents instead of just metadata
This is CRITICAL for the orchestrator to see real data
"""

import os
import json
import pandas as pd
import PyPDF2
from typing import Dict, List, Any, Optional
import chardet
import openpyxl
import docx
import yaml


class FileContentReader:
    """Reads actual file contents for the orchestrator to see real data."""

    def __init__(self):
        self.max_preview_rows = 100  # For large files
        self.max_text_preview = 5000  # Characters for text files

    def read_file_contents(
        self, file_path: str, file_type: str = None
    ) -> Dict[str, Any]:
        """
        Read actual file contents based on file type.

        Returns:
            Dict with actual data, not just metadata
        """

        result = {
            "path": file_path,
            "type": file_type or self._detect_file_type(file_path),
            "read_success": False,
            "content": None,
            "structure": None,
            "error": None,
            "size": os.path.getsize(file_path) if os.path.exists(file_path) else 0,
        }

        try:
            # CSV Files
            if file_path.endswith(".csv") or file_type == "text/csv":
                result.update(self._read_csv(file_path))

            # Excel Files
            elif (
                file_path.endswith((".xlsx", ".xls"))
                or "spreadsheet" in str(file_type).lower()
            ):
                result.update(self._read_excel(file_path))

            # JSON Files
            elif file_path.endswith(".json") or file_type == "application/json":
                result.update(self._read_json(file_path))

            # Text Files
            elif file_path.endswith(".txt") or file_type == "text/plain":
                result.update(self._read_text(file_path))

            # PDF Files
            elif file_path.endswith(".pdf") or file_type == "application/pdf":
                result.update(self._read_pdf(file_path))

            # Word Documents
            elif file_path.endswith((".docx", ".doc")):
                result.update(self._read_word(file_path))

            # YAML Files
            elif file_path.endswith((".yml", ".yaml")):
                result.update(self._read_yaml(file_path))

            # Python Files
            elif file_path.endswith(".py"):
                result.update(self._read_code(file_path, "python"))

            # Default: Try as text
            else:
                result.update(self._read_text(file_path))

        except Exception as e:
            result["error"] = str(e)
            result["read_success"] = False

        return result

    def _read_csv(self, file_path: str) -> Dict:
        """Read CSV with pandas and extract meaningful data."""
        try:
            # Read CSV with intelligent parsing
            df = pd.read_csv(file_path, nrows=self.max_preview_rows)

            # Get full dataframe for stats
            df_full = pd.read_csv(file_path)

            return {
                "read_success": True,
                "structure": "tabular",
                "content": {
                    "columns": df.columns.tolist(),
                    "total_rows": len(df_full),
                    "total_columns": len(df.columns),
                    "first_10_rows": df.head(10).to_dict("records"),
                    "last_5_rows": df.tail(5).to_dict("records"),
                    "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
                    "sample_values": {
                        col: df[col].dropna().head(5).tolist() for col in df.columns
                    },
                    "null_counts": df_full.isnull().sum().to_dict(),
                    "numeric_columns": df.select_dtypes(
                        include=["number"]
                    ).columns.tolist(),
                    "text_columns": df.select_dtypes(
                        include=["object"]
                    ).columns.tolist(),
                    "statistics": df.describe().to_dict() if not df.empty else {},
                },
            }
        except Exception as e:
            return {"error": f"CSV read error: {str(e)}", "read_success": False}

    def _read_excel(self, file_path: str) -> Dict:
        """Read Excel files with multiple sheets support."""
        try:
            # Read all sheets
            excel_file = pd.ExcelFile(file_path)
            sheets_data = {}

            for sheet_name in excel_file.sheet_names[:5]:  # Limit to first 5 sheets
                df = pd.read_excel(
                    file_path, sheet_name=sheet_name, nrows=self.max_preview_rows
                )
                sheets_data[sheet_name] = {
                    "columns": df.columns.tolist(),
                    "rows": len(df),
                    "preview": df.head(10).to_dict("records"),
                    "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
                }

            return {
                "read_success": True,
                "structure": "tabular",
                "content": {
                    "sheet_count": len(excel_file.sheet_names),
                    "sheet_names": excel_file.sheet_names,
                    "sheets": sheets_data,
                    "primary_sheet": (
                        sheets_data[excel_file.sheet_names[0]]
                        if excel_file.sheet_names
                        else {}
                    ),
                },
            }
        except Exception as e:
            return {"error": f"Excel read error: {str(e)}", "read_success": False}

    def _read_json(self, file_path: str) -> Dict:
        """Read JSON files and understand structure."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Analyze JSON structure
            structure_info = self._analyze_json_structure(data)

            return {
                "read_success": True,
                "structure": "json",
                "content": {
                    "data": data,
                    "type": type(data).__name__,
                    "structure_info": structure_info,
                    "keys": list(data.keys()) if isinstance(data, dict) else None,
                    "length": len(data) if isinstance(data, (list, dict)) else None,
                    "preview": str(data)[:1000] if len(str(data)) > 1000 else data,
                },
            }
        except Exception as e:
            return {"error": f"JSON read error: {str(e)}", "read_success": False}

    def _read_text(self, file_path: str) -> Dict:
        """Read text files with encoding detection."""
        try:
            # Detect encoding
            with open(file_path, "rb") as f:
                raw_data = f.read(10000)
                detected = chardet.detect(raw_data)
                encoding = detected["encoding"] or "utf-8"

            # Read with detected encoding
            with open(file_path, "r", encoding=encoding, errors="ignore") as f:
                text = f.read()

            # Analyze text
            lines = text.split("\n")
            words = text.split()

            return {
                "read_success": True,
                "structure": "text",
                "content": {
                    "text": text[: self.max_text_preview],
                    "full_text": text,
                    "full_length": len(text),
                    "line_count": len(lines),
                    "word_count": len(words),
                    "encoding": encoding,
                    "first_lines": lines[:20],
                    "has_headers": self._detect_headers(lines),
                    "appears_structured": self._detect_structure(lines),
                },
            }
        except Exception as e:
            return {"error": f"Text read error: {str(e)}", "read_success": False}

    def _read_pdf(self, file_path: str) -> Dict:
        """Read PDF files and extract text."""
        try:
            text_content = []
            metadata = {}

            with open(file_path, "rb") as f:
                pdf_reader = PyPDF2.PdfReader(f)
                num_pages = len(pdf_reader.pages)

                # Extract text from first few pages
                for i in range(min(5, num_pages)):
                    page = pdf_reader.pages[i]
                    text_content.append(page.extract_text())

                # Get metadata
                if pdf_reader.metadata:
                    metadata = {
                        "title": pdf_reader.metadata.get("/Title", ""),
                        "author": pdf_reader.metadata.get("/Author", ""),
                        "subject": pdf_reader.metadata.get("/Subject", ""),
                    }

            full_text = "\n".join(text_content)

            return {
                "read_success": True,
                "structure": "pdf",
                "content": {
                    "text_preview": full_text[: self.max_text_preview],
                    "page_count": num_pages,
                    "metadata": metadata,
                    "first_pages_text": text_content,
                    "word_count": len(full_text.split()),
                    "has_text": bool(full_text.strip()),
                },
            }
        except Exception as e:
            return {"error": f"PDF read error: {str(e)}", "read_success": False}

    def _read_word(self, file_path: str) -> Dict:
        """Read Word documents."""
        try:
            doc = docx.Document(file_path)

            # Extract text from paragraphs
            paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]

            # Extract tables
            tables = []
            for table in doc.tables[:5]:  # First 5 tables
                table_data = []
                for row in table.rows[:10]:  # First 10 rows
                    row_data = [cell.text.strip() for cell in row.cells]
                    table_data.append(row_data)
                tables.append(table_data)

            full_text = "\n".join(paragraphs)

            return {
                "read_success": True,
                "structure": "document",
                "content": {
                    "text": full_text[: self.max_text_preview],
                    "paragraph_count": len(paragraphs),
                    "table_count": len(doc.tables),
                    "first_paragraphs": paragraphs[:10],
                    "tables_preview": tables,
                    "word_count": len(full_text.split()),
                },
            }
        except Exception as e:
            return {"error": f"Word read error: {str(e)}", "read_success": False}

    def _read_yaml(self, file_path: str) -> Dict:
        """Read YAML configuration files."""
        try:
            with open(file_path, "r") as f:
                data = yaml.safe_load(f)

            return {
                "read_success": True,
                "structure": "yaml",
                "content": {
                    "data": data,
                    "type": type(data).__name__,
                    "keys": list(data.keys()) if isinstance(data, dict) else None,
                    "preview": str(data)[:1000],
                },
            }
        except Exception as e:
            return {"error": f"YAML read error: {str(e)}", "read_success": False}

    def _read_code(self, file_path: str, language: str) -> Dict:
        """Read code files with syntax awareness."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()

            lines = code.split("\n")

            # Basic code analysis
            import_lines = [
                l for l in lines if l.strip().startswith(("import ", "from "))
            ]
            function_lines = [l for l in lines if "def " in l or "class " in l]

            return {
                "read_success": True,
                "structure": "code",
                "content": {
                    "language": language,
                    "code": code[: self.max_text_preview],
                    "full_code": code,
                    "line_count": len(lines),
                    "imports": import_lines,
                    "functions_classes": function_lines,
                    "has_main": "__main__" in code,
                },
            }
        except Exception as e:
            return {"error": f"Code read error: {str(e)}", "read_success": False}

    def _detect_file_type(self, file_path: str) -> str:
        """Detect file type from extension."""
        ext = os.path.splitext(file_path)[1].lower()
        type_map = {
            ".csv": "text/csv",
            ".json": "application/json",
            ".txt": "text/plain",
            ".pdf": "application/pdf",
            ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ".xls": "application/vnd.ms-excel",
            ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ".py": "text/x-python",
            ".yml": "text/yaml",
            ".yaml": "text/yaml",
        }
        return type_map.get(ext, "application/octet-stream")

    def _analyze_json_structure(
        self, data: Any, depth: int = 0, max_depth: int = 3
    ) -> Dict:
        """Analyze JSON structure recursively."""
        if depth >= max_depth:
            return {"type": type(data).__name__, "truncated": True}

        if isinstance(data, dict):
            return {
                "type": "object",
                "keys": list(data.keys())[:10],
                "key_count": len(data),
                "sample": {
                    k: self._analyze_json_structure(v, depth + 1)
                    for k, v in list(data.items())[:3]
                },
            }
        elif isinstance(data, list):
            return {
                "type": "array",
                "length": len(data),
                "item_type": (
                    self._analyze_json_structure(data[0], depth + 1) if data else None
                ),
            }
        else:
            return {"type": type(data).__name__, "value": str(data)[:100]}

    def _detect_headers(self, lines: List[str]) -> bool:
        """Detect if text file has headers."""
        if not lines:
            return False

        first_line = lines[0]
        # Common header patterns
        return any(
            [
                "," in first_line and len(first_line.split(",")) > 2,
                "\t" in first_line and len(first_line.split("\t")) > 2,
                "|" in first_line and len(first_line.split("|")) > 2,
                first_line.startswith("#"),
                first_line.isupper(),
            ]
        )

    def _detect_structure(self, lines: List[str]) -> bool:
        """Detect if text appears to be structured data."""
        if len(lines) < 3:
            return False

        # Check for consistent delimiters
        delimiters = [",", "\t", "|", ";"]
        for delim in delimiters:
            counts = [line.count(delim) for line in lines[:10] if line.strip()]
            if counts and all(c == counts[0] and c > 0 for c in counts):
                return True

        return False

    def process_all_files(self, files: List[Dict]) -> List[Dict]:
        """
        Process all uploaded files and read their contents.

        Args:
            files: List of file metadata dicts from upload

        Returns:
            List of files with actual content included
        """

        enriched_files = []

        for file_info in files:
            file_path = file_info.get("path", "")
            file_type = file_info.get("type", "")

            if os.path.exists(file_path):
                # Read actual content
                content_data = self.read_file_contents(file_path, file_type)

                # Merge with original metadata
                enriched_file = {**file_info, **content_data}
                enriched_files.append(enriched_file)

                print(
                    f"✓ Read {file_info.get('original_name', 'file')}: "
                    f"{content_data.get('structure', 'unknown')} structure, "
                    f"{'success' if content_data.get('read_success') else 'failed'}"
                )
            else:
                # File doesn't exist
                enriched_file = {
                    **file_info,
                    "read_success": False,
                    "error": f"File not found: {file_path}",
                }
                enriched_files.append(enriched_file)
                print(f"✗ File not found: {file_path}")

        return enriched_files

```

--------------------------------------------------------------------------------

### File: core/intelligent_agent_base.py
**Path:** `core/intelligent_agent_base.py`
**Size:** 4,783 bytes
**Modified:** 2025-09-14 09:31:42

```python
"""
Enhanced Intelligent Agent Base
Each agent has Claude reasoning capabilities
"""

import json
from typing import Dict, Any, List, Optional
from anthropic import Anthropic
import os

from config import CLAUDE_MODEL


class IntelligentAgent:
    """Base agent with Claude reasoning capabilities"""

    def __init__(self, name: str, purpose: str, tools: List[str] = None):
        self.name = name
        self.purpose = purpose
        self.tools = tools or []
        self.claude = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    async def execute(self, state: Dict) -> Dict:
        """Execute with intelligent reasoning"""

        # Step 1: Understand what we received
        analysis = await self.analyze_input(state)

        # Step 2: Process based on analysis
        result = await self.process_with_reasoning(state, analysis)

        # Step 3: Format output for next agent
        formatted = await self.format_output(result, state)

        return formatted

    async def analyze_input(self, state: Dict) -> Dict:
        """Claude analyzes input data"""

        current_data = state.get("current_data", {})

        # Format data for Claude
        if isinstance(current_data, dict) and "columns" in current_data:
            # CSV data
            data_desc = f"CSV with columns: {current_data['columns']}, {current_data.get('total_rows', 0)} rows"
        else:
            data_desc = str(type(current_data).__name__)

        prompt = f"""
        I am agent '{self.name}' with purpose: {self.purpose}
        
        I received: {data_desc}
        Data sample: {str(current_data)[:500]}
        
        Analyze:
        1. What type of data is this?
        2. What should I do with it?
        3. What would be useful output?
        
        Be specific and concise.
        """

        response = self.claude.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )

        return {"analysis": response.content[0].text}

    async def process_with_reasoning(self, state: Dict, analysis: Dict) -> Dict:
        """Process data with Claude's guidance"""

        prompt = f"""
        Based on analysis: {analysis['analysis']}
        
        Process this data for: {self.purpose}
        Available tools: {self.tools}
        
        Current data: {str(state.get('current_data'))[:1000]}
        
        Provide the processed result.
        """

        response = self.claude.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}],
        )

        return {
            "processed_data": response.content[0].text,
            "reasoning": analysis["analysis"],
        }

    async def format_output(self, result: Dict, original_state: Dict) -> Dict:
        """Format output for pipeline"""

        return {
            "status": "success",
            "agent": self.name,
            "data": result.get("processed_data"),
            "reasoning": result.get("reasoning"),
            "metadata": {
                "input_type": type(original_state.get("current_data")).__name__,
                "purpose": self.purpose,
                "tools_used": self.tools,
            },
        }


class DataAnalysisAgent(IntelligentAgent):
    """Specialized agent for data analysis"""

    def __init__(self):
        super().__init__(
            name="data_analysis",
            purpose="Analyze data patterns and extract insights",
            tools=["pandas", "statistics"],
        )

    async def process_with_reasoning(self, state: Dict, analysis: Dict) -> Dict:
        """Specialized processing for data analysis"""

        current_data = state.get("current_data", {})

        if isinstance(current_data, dict) and "columns" in current_data:
            # Work with CSV data
            prompt = f"""
            Analyze this CSV data:
            Columns: {current_data['columns']}
            Sample rows: {current_data.get('first_10_rows', [])[:3]}
            Total rows: {current_data.get('total_rows', 0)}
            
            Provide:
            1. Key statistics
            2. Data patterns
            3. Interesting insights
            4. Potential issues
            """

            response = self.claude.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}],
            )

            return {
                "processed_data": response.content[0].text,
                "reasoning": "Analyzed CSV data structure and patterns",
            }

        # Default processing
        return await super().process_with_reasoning(state, analysis)

```

--------------------------------------------------------------------------------

### File: core/pipeline_executor.py
**Path:** `core/pipeline_executor.py`
**Size:** 21,365 bytes
**Modified:** 2025-09-11 09:24:13

```python
"""
Pipeline Executor
Enhanced workflow execution engine for multi-step pipelines with data flow management
"""

import os
import sys
import json
import asyncio
import importlib.util
from typing import Dict, List, Optional, Any, TypedDict
from datetime import datetime
import traceback
import networkx as nx

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from config import (
    MAX_WORKFLOW_STEPS,
    WORKFLOW_TIMEOUT_SECONDS,
    AGENT_TIMEOUT_SECONDS,
    AGENT_MAX_RETRIES,
    ENABLE_PARALLEL_EXECUTION,
    MAX_PARALLEL_AGENTS,
    GENERATED_AGENTS_DIR,
    PREBUILT_AGENTS_DIR,
)
from core.registry import RegistryManager


class PipelineState(TypedDict):
    """Enhanced state schema for pipeline execution."""

    request: str
    pipeline_id: str
    current_step: int
    total_steps: int
    files: List[Dict]
    execution_path: List[str]
    step_results: Dict[str, Any]
    current_data: Any
    data_flow: Dict[str, Any]
    results: Dict[str, Any]
    errors: List[Dict]
    adaptations: List[Dict]
    started_at: str
    completed_at: Optional[str]


class PipelineExecutor:
    """
    Enhanced workflow execution engine for multi-step pipelines.
    Handles data flow, parallel execution, and real-time adaptation.
    """

    def __init__(self, registry: RegistryManager):
        """Initialize the pipeline executor."""
        self.registry = registry
        self.execution_history = []

    async def execute_pipeline(
        self, pipeline_plan: Dict, user_request: str, files: List[Dict] = None
    ) -> Dict[str, Any]:
        """
        Execute a complete pipeline with data flow management.

        Args:
            pipeline_plan: Complete pipeline execution plan
            user_request: Original user request
            files: Uploaded files

        Returns:
            Pipeline execution results
        """
        print(
            f"DEBUG: Executing pipeline {pipeline_plan.get('pipeline_id')} with {pipeline_plan.get('total_steps')} steps"
        )

        # Initialize pipeline state
        pipeline_state = PipelineState(
            request=user_request,
            pipeline_id=pipeline_plan.get(
                "pipeline_id", f"pipeline_{datetime.now().strftime('%H%M%S')}"
            ),
            current_step=0,
            total_steps=pipeline_plan.get("total_steps", 0),
            files=files or [],
            execution_path=[],
            step_results={},
            current_data={"user_request": user_request, "files": files},
            data_flow=pipeline_plan.get("data_flow", {}),
            results={},
            errors=[],
            adaptations=[],
            started_at=datetime.now().isoformat(),
            completed_at=None,
        )

        # Track execution
        self.execution_history.append(
            {
                "pipeline_id": pipeline_state["pipeline_id"],
                "started_at": pipeline_state["started_at"],
                "status": "in_progress",
            }
        )

        try:
            # Execute pipeline steps based on strategy
            execution_strategy = pipeline_plan.get("execution_strategy", "sequential")

            if execution_strategy == "sequential":
                final_state = await self._execute_sequential_pipeline(
                    pipeline_plan, pipeline_state
                )
            elif execution_strategy == "parallel":
                final_state = await self._execute_parallel_pipeline(
                    pipeline_plan, pipeline_state
                )
            else:
                final_state = await self._execute_sequential_pipeline(
                    pipeline_plan, pipeline_state
                )

            # Finalize execution
            final_state["completed_at"] = datetime.now().isoformat()

            # Determine final status
            if (
                final_state["current_step"] >= final_state["total_steps"]
                and not final_state["errors"]
            ):
                status = "success"
            elif final_state["current_step"] > 0:
                status = "partial"
            else:
                status = "failed"

            # Update execution history
            for exec_record in self.execution_history:
                if exec_record["pipeline_id"] == pipeline_state["pipeline_id"]:
                    exec_record["status"] = status
                    exec_record["completed_at"] = final_state["completed_at"]
                    break

            result = {
                "status": status,
                "pipeline_id": final_state["pipeline_id"],
                "steps_completed": final_state["current_step"],
                "total_steps": final_state["total_steps"],
                "results": final_state["results"],
                "step_results": final_state["step_results"],
                "errors": final_state["errors"],
                "adaptations": final_state["adaptations"],
                "execution_time": self._calculate_execution_time(
                    final_state["started_at"], final_state["completed_at"]
                ),
                "final_data": final_state["current_data"],
            }

            print(f"DEBUG: Pipeline execution completed - Status: {status}")
            return result

        except Exception as e:
            error_msg = f"Pipeline execution failed: {str(e)}"
            print(f"DEBUG: {error_msg}")

            return {
                "status": "error",
                "pipeline_id": pipeline_state["pipeline_id"],
                "error": error_msg,
                "steps_completed": pipeline_state["current_step"],
                "total_steps": pipeline_state["total_steps"],
                "results": pipeline_state["results"],
                "errors": pipeline_state["errors"]
                + [{"type": "execution_error", "message": error_msg}],
            }

    async def _execute_sequential_pipeline(
        self, pipeline_plan: Dict, state: PipelineState
    ) -> PipelineState:
        """Execute pipeline steps sequentially."""
        print(
            f"DEBUG: Executing sequential pipeline with {len(pipeline_plan['steps'])} steps"
        )

        for i, step_plan in enumerate(pipeline_plan["steps"]):
            print(
                f"DEBUG: Executing step {i+1}/{state['total_steps']}: {step_plan.get('name', 'unnamed')}"
            )

            state["current_step"] = i

            try:
                # Execute step with current data
                step_result = await self._execute_pipeline_step(step_plan, state)

                if step_result["status"] == "success":
                    # Update state with step results
                    state["step_results"][step_plan["name"]] = step_result
                    state["results"][step_plan["name"]] = step_result
                    state["execution_path"].append(step_plan["name"])

                    # Update current data for next step
                    state["current_data"] = self._extract_data_for_next_step(
                        step_result, step_plan, state
                    )

                    print(f"DEBUG: Step {i+1} completed successfully")

                else:
                    # Handle step failure
                    error_info = {
                        "step": step_plan["name"],
                        "step_index": i,
                        "error": step_result.get("error", "Unknown error"),
                        "timestamp": datetime.now().isoformat(),
                    }
                    state["errors"].append(error_info)

                    print(f"DEBUG: Step {i+1} failed: {error_info['error']}")

                    # For now, stop on first error (can be enhanced for recovery)
                    break

            except Exception as e:
                error_info = {
                    "step": step_plan["name"],
                    "step_index": i,
                    "error": str(e),
                    "type": "execution_exception",
                    "timestamp": datetime.now().isoformat(),
                }
                state["errors"].append(error_info)
                print(f"DEBUG: Step {i+1} exception: {str(e)}")
                break

        state["current_step"] = min(state["current_step"] + 1, state["total_steps"])
        return state

    async def _execute_parallel_pipeline(
        self, pipeline_plan: Dict, state: PipelineState
    ) -> PipelineState:
        """Execute pipeline steps in parallel where possible."""
        print(
            f"DEBUG: Executing parallel pipeline (not fully implemented - falling back to sequential)"
        )

        # For now, fall back to sequential execution
        # Can be enhanced to detect parallel opportunities
        return await self._execute_sequential_pipeline(pipeline_plan, state)

    async def _execute_pipeline_step(
        self, step_plan: Dict, state: PipelineState
    ) -> Dict[str, Any]:
        """
        Execute a single pipeline step with enhanced data handling.

        Args:
            step_plan: Step execution plan
            state: Current pipeline state

        Returns:
            Step execution result
        """
        agent_name = step_plan.get("agent_assigned")

        if not agent_name:
            return {
                "status": "error",
                "error": "No agent assigned to step",
                "step_name": step_plan.get("name", "unknown"),
            }

        try:
            # Load and execute the agent
            agent_result = await self._execute_agent_with_pipeline_context(
                agent_name, step_plan, state
            )
            return agent_result

        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "step_name": step_plan.get("name", "unknown"),
                "agent_name": agent_name,
            }

    def _get_agent_function_name(self, agent_name: str) -> str:
        """Smart function name resolution"""
        if agent_name.endswith("_agent"):
            return agent_name
        else:
            return f"{agent_name}_agent"

    async def _execute_agent_with_pipeline_context(
        self, agent_name: str, step_plan: Dict, state: PipelineState
    ) -> Dict[str, Any]:
        """Execute agent with pipeline context and enhanced data handling."""

        # Check if agent exists
        if not self.registry.agent_exists(agent_name):
            return {
                "status": "error",
                "error": f"Agent '{agent_name}' not found",
                "agent_name": agent_name,
            }

        # Get agent details
        agent = self.registry.get_agent(agent_name)
        agent_path = agent["location"]

        # Verify agent file exists
        if not os.path.exists(agent_path):
            return {
                "status": "error",
                "error": f"Agent file not found: {agent_path}",
                "agent_name": agent_name,
            }

        try:
            # Load agent module
            spec = importlib.util.spec_from_file_location(agent_name, agent_path)
            agent_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(agent_module)

            # Get agent function
            function_name = self._get_agent_function_name(agent_name)
            print(f"DEBUG: Looking for function: {function_name}")

            try:
                agent_function = getattr(agent_module, function_name)
                print(f"DEBUG: Found agent function: {function_name}")
            except AttributeError:
                # Try the other pattern
                fallback_name = (
                    f"{agent_name}_agent"
                    if agent_name.endswith("_agent")
                    else agent_name
                )
                if fallback_name != function_name:
                    try:
                        agent_function = getattr(agent_module, fallback_name)
                        print(f"DEBUG: Found with fallback: {fallback_name}")
                    except AttributeError:
                        available_funcs = [
                            name
                            for name in dir(agent_module)
                            if not name.startswith("_")
                        ]
                        print(f"DEBUG: Available functions: {available_funcs}")
                        raise AttributeError(
                            f"No agent function found. Tried: {function_name}, {fallback_name}"
                        )
                else:
                    available_funcs = [
                        name for name in dir(agent_module) if not name.startswith("_")
                    ]
                    print(f"DEBUG: Available functions: {available_funcs}")
                    raise AttributeError(f"Agent function not found: {function_name}")

            # Prepare agent state with pipeline context
            agent_state = self._prepare_agent_state_for_pipeline(state, step_plan)

            # Execute agent with timeout
            agent_result = await asyncio.wait_for(
                agent_function(agent_state), timeout=AGENT_TIMEOUT_SECONDS
            )

            # Validate and process result
            if isinstance(agent_result, dict):
                return self._process_agent_result(agent_result, agent_name, step_plan)
            else:
                return {
                    "status": "error",
                    "error": f"Agent returned invalid result type: {type(agent_result)}",
                    "agent_name": agent_name,
                }

        except asyncio.TimeoutError:
            return {
                "status": "error",
                "error": f"Agent execution timeout ({AGENT_TIMEOUT_SECONDS}s)",
                "agent_name": agent_name,
            }
        except Exception as e:
            return {
                "status": "error",
                "error": f"Agent execution failed: {str(e)}",
                "agent_name": agent_name,
                "traceback": traceback.format_exc(),
            }

    def _prepare_agent_state_for_pipeline(
        self, pipeline_state: PipelineState, step_plan: Dict
    ) -> Dict[str, Any]:
        """Prepare agent state with pipeline context and data."""

        # Base state structure
        agent_state = {
            "request": f"Pipeline step: {step_plan.get('description', step_plan.get('name', 'unknown'))}",
            "files": pipeline_state["files"],
            "current_data": pipeline_state["current_data"],
            "execution_path": pipeline_state["execution_path"].copy(),
            "results": {},
            "errors": [],
        }

        # Add pipeline context
        agent_state["pipeline_context"] = {
            "pipeline_id": pipeline_state["pipeline_id"],
            "step_index": pipeline_state["current_step"],
            "total_steps": pipeline_state["total_steps"],
            "step_name": step_plan.get("name", "unknown"),
            "previous_results": pipeline_state["step_results"],
            "data_flow": pipeline_state["data_flow"],
        }

        # Add step-specific requirements
        if "input_requirements" in step_plan:
            agent_state["input_requirements"] = step_plan["input_requirements"]

        if "output_requirements" in step_plan:
            agent_state["output_requirements"] = step_plan["output_requirements"]

        return agent_state

    def _process_agent_result(
        self, agent_result: Dict, agent_name: str, step_plan: Dict
    ) -> Dict[str, Any]:
        """Process and validate agent result."""

        # Check for valid agent result structure
        if "status" not in agent_result:
            agent_result["status"] = "success" if "data" in agent_result else "error"

        # Add metadata
        agent_result["agent_name"] = agent_name
        agent_result["step_name"] = step_plan.get("name", "unknown")
        agent_result["executed_at"] = datetime.now().isoformat()

        # Ensure metadata structure
        if "metadata" not in agent_result:
            agent_result["metadata"] = {}

        agent_result["metadata"]["step_index"] = step_plan.get("step_index", 0)
        agent_result["metadata"]["pipeline_step"] = True

        return agent_result

    def _extract_data_for_next_step(
        self, step_result: Dict, step_plan: Dict, state: PipelineState
    ) -> Any:
        """Extract appropriate data from step result for next step."""

        # Get the actual data from the step result
        if "data" in step_result:
            data = step_result["data"]
        else:
            data = step_result

        # For pipeline steps, we want to pass the processed data forward
        # This could be enhanced to handle specific data transformations

        # If the data is a dict with results, extract meaningful content
        if isinstance(data, dict):
            # Look for common result patterns
            if "processed_data" in data:
                return data["processed_data"]
            elif "extracted_data" in data:
                return data["extracted_data"]
            elif "results" in data:
                return data["results"]
            elif len(data) == 1:
                # If there's only one key, use its value
                return list(data.values())[0]

        # Default: return the data as-is
        return data

    def _calculate_execution_time(self, start_time: str, end_time: str) -> float:
        """Calculate execution time in seconds."""
        if not start_time or not end_time:
            return 0.0

        try:
            start = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
            end = datetime.fromisoformat(end_time.replace("Z", "+00:00"))
            return (end - start).total_seconds()
        except:
            return 0.0

    async def execute_step_with_recovery(
        self, step_plan: Dict, state: PipelineState, max_retries: int = 2
    ) -> Dict[str, Any]:
        """
        Execute a step with automatic recovery on failure.

        Args:
            step_plan: Step execution plan
            state: Current pipeline state
            max_retries: Maximum retry attempts

        Returns:
            Step execution result with recovery information
        """
        last_error = None

        for attempt in range(max_retries + 1):
            try:
                print(
                    f"DEBUG: Executing step (attempt {attempt + 1}/{max_retries + 1})"
                )

                result = await self._execute_pipeline_step(step_plan, state)

                if result["status"] == "success":
                    if attempt > 0:
                        result["recovery_info"] = {
                            "recovered": True,
                            "attempts": attempt + 1,
                            "last_error": str(last_error) if last_error else None,
                        }
                    return result
                else:
                    last_error = result.get("error", "Unknown error")
                    if attempt < max_retries:
                        print(f"DEBUG: Step failed, retrying... Error: {last_error}")
                        await asyncio.sleep(1)  # Brief delay before retry

            except Exception as e:
                last_error = str(e)
                if attempt < max_retries:
                    print(f"DEBUG: Step exception, retrying... Error: {last_error}")
                    await asyncio.sleep(1)

        # All attempts failed
        return {
            "status": "error",
            "error": f"Step failed after {max_retries + 1} attempts. Last error: {last_error}",
            "step_name": step_plan.get("name", "unknown"),
            "recovery_info": {
                "recovered": False,
                "attempts": max_retries + 1,
                "last_error": str(last_error),
            },
        }

    def get_execution_history(self) -> List[Dict]:
        """Get pipeline execution history."""
        return self.execution_history.copy()

    def create_data_flow_graph(self, pipeline_plan: Dict) -> nx.DiGraph:
        """Create a graph representing data flow in the pipeline."""
        graph = nx.DiGraph()

        steps = pipeline_plan.get("steps", [])

        for i, step in enumerate(steps):
            step_name = step.get("name", f"step_{i}")
            graph.add_node(step_name, **step)

            # Add edges based on data flow
            if i > 0:
                prev_step = steps[i - 1].get("name", f"step_{i-1}")
                graph.add_edge(prev_step, step_name)

        return graph

    def optimize_execution_order(self, pipeline_plan: Dict) -> Dict[str, Any]:
        """Optimize execution order for better performance."""
        # For now, return original plan
        # Can be enhanced to detect parallel opportunities

        optimized_plan = pipeline_plan.copy()
        optimized_plan["optimization_applied"] = False
        optimized_plan["optimization_notes"] = (
            "Sequential execution (no optimizations applied)"
        )

        return optimized_plan

```

--------------------------------------------------------------------------------

### File: core/pipeline_orchestrator.py
**Path:** `core/pipeline_orchestrator.py`
**Size:** 32,532 bytes
**Modified:** 2025-09-14 09:11:13

```python
"""
Pipeline Orchestrator
Master coordinator for dynamic multi-agent pipeline execution
"""

import os
import sys
import json
import asyncio
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import openai
import networkx as nx

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    OPENAI_API_KEY,
    ORCHESTRATOR_MODEL,
    ORCHESTRATOR_TEMPERATURE,
    ORCHESTRATOR_MAX_TOKENS,
    PIPELINE_ANALYSIS_PROMPT,
    AGENT_COMPATIBILITY_PROMPT,
    PIPELINE_PLANNING_PROMPT,
    DYNAMIC_AGENT_SPEC_PROMPT,
    PIPELINE_RECOVERY_PROMPT,
)
from core.registry import RegistryManager
from core.agent_compatibility import AgentCompatibilityAnalyzer
from core.agent_factory import AgentFactory
from core.tool_factory import ToolFactory


class PipelineOrchestrator:
    """
    Master coordinator for dynamic multi-agent pipeline execution.
    Handles complex request analysis, pipeline planning, and real-time adaptation.
    """

    def __init__(self):
        """Initialize the pipeline orchestrator."""
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        from core.registry_singleton import get_shared_registry

        self.registry = get_shared_registry()  # ← FIX: Use shared instance
        self.compatibility_analyzer = AgentCompatibilityAnalyzer(self.registry)
        self.agent_factory = AgentFactory()
        self.tool_factory = ToolFactory()

    async def analyze_complex_request(
        self, request: str, files: List[Dict] = None
    ) -> Dict[str, Any]:
        """
        Analyze complex request and break it into pipeline steps.

        Args:
            request: User's natural language request
            files: Uploaded files with metadata

        Returns:
            Pipeline analysis with steps and requirements
        """
        print(f"DEBUG: Analyzing complex request: {request[:100]}...")

        # Get available components
        agents = self.registry.list_agents(active_only=True)
        tools = self.registry.list_tools()

        # Format components for prompt
        agents_desc = self._format_components_list(agents, "agents")
        tools_desc = self._format_components_list(tools, "tools")

        # Build analysis prompt
        prompt = PIPELINE_ANALYSIS_PROMPT.format(
            request=request,
            files=json.dumps(files) if files else "None",
            available_agents=agents_desc,
            available_tools=tools_desc,
        )

        try:
            response = await self._call_gpt4_json(
                system_prompt="You are a pipeline analyzer. Analyze requests and break them into logical steps.",
                user_prompt=prompt,
            )

            analysis = json.loads(response)
            analysis["status"] = "success"

            print(
                f"DEBUG: Pipeline analysis found {len(analysis.get('steps', []))} steps"
            )
            return analysis

        except Exception as e:
            print(f"DEBUG: Pipeline analysis failed: {str(e)}")
            return {
                "status": "error",
                "error": f"Pipeline analysis failed: {str(e)}",
                "steps": [],
            }

    async def plan_pipeline(
        self, analysis: Dict, auto_create: bool = True
    ) -> Dict[str, Any]:
        """
        Plan optimal pipeline execution with agent compatibility analysis.

        Args:
            analysis: Pipeline analysis from analyze_complex_request
            auto_create: Whether to auto-create missing agents

        Returns:
            Complete pipeline execution plan
        """
        print(f"DEBUG: Planning pipeline with {len(analysis.get('steps', []))} steps")

        steps = analysis.get("steps", [])
        if not steps:
            return {"status": "error", "error": "No pipeline steps to plan"}

        # Analyze agent compatibility for each step
        pipeline_plan = {
            "pipeline_id": f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "total_steps": len(steps),
            "execution_strategy": "sequential",  # Default, can be enhanced
            "steps": [],
            "creation_needed": [],
            "data_flow": {},
            "estimated_time": 0,
        }

        for i, step in enumerate(steps):
            previous_output = None
            if i > 0:
                # Get output from previous step if available
                prev_step_name = pipeline_plan["steps"][i - 1].get("name")
                # This would need to be enhanced to track actual data flow

            step_plan = await self._plan_step(step, i, auto_create, previous_output)
            pipeline_plan["steps"].append(step_plan)

            if step_plan.get("needs_creation"):
                pipeline_plan["creation_needed"].extend(step_plan["creation_specs"])

            # Estimate execution time
            pipeline_plan["estimated_time"] += step_plan.get("estimated_time", 5)

        # Plan data flow between steps
        pipeline_plan["data_flow"] = self._plan_data_flow(pipeline_plan["steps"])

        # Determine execution strategy
        pipeline_plan["execution_strategy"] = self._determine_execution_strategy(
            pipeline_plan["steps"]
        )

        print(
            f"DEBUG: Pipeline planned - {len(pipeline_plan['creation_needed'])} components need creation"
        )
        return pipeline_plan

    def _predict_step_output(self, previous_step: Dict, current_step: Dict) -> Any:
        """Predict output from previous step for planning purposes."""

        # Analyze what the previous step should produce
        prev_name = previous_step.get("name", "").lower()
        prev_desc = previous_step.get("description", "").lower()

        current_name = current_step.get("name", "").lower()
        current_desc = current_step.get("description", "").lower()

        # Pattern-based output prediction
        if "extract" in prev_desc:
            if "email" in prev_desc:
                return ["john@example.com", "mary@company.org"]  # Sample emails
            elif "url" in prev_desc:
                return [
                    "https://example.com",
                    "https://docs.example.com",
                ]  # Sample URLs
            else:
                return {"extracted_data": "sample extracted content"}

        elif "read" in prev_desc or "process" in prev_desc:
            if "text" in prev_desc:
                return "Sample processed text content"
            else:
                return {"processed_data": "sample processed content"}

        elif "calculate" in prev_desc or "analyze" in prev_desc:
            return {"result": 42, "analysis": "sample analysis"}

        # Default prediction based on current step needs
        if "text" in current_desc:
            return "sample text for processing"
        elif "list" in current_desc or "extract" in current_desc:
            return ["item1", "item2", "item3"]
        else:
            return {"data": "sample data", "type": "unknown"}

    async def _generate_agent_spec_for_step(
        self, step: Dict, step_index: int
    ) -> Dict[str, Any]:
        """Generate detailed agent specification for a pipeline step."""

        # Use GPT-4 to design pipeline-aware agent
        prompt = DYNAMIC_AGENT_SPEC_PROMPT.format(
            step_description=step.get("description", ""),
            step_index=step_index,
            input_requirements=json.dumps(step.get("input_requirements", {})),
            output_requirements=json.dumps(step.get("output_requirements", {})),
            available_tools=json.dumps([t["name"] for t in self.registry.list_tools()]),
        )

        try:
            response = await self._call_gpt4_json(
                system_prompt="Design pipeline-aware agent specifications.",
                user_prompt=prompt,
            )

            spec = json.loads(response)

            # Add pipeline context
            spec["pipeline_context"] = {
                "step_index": step_index,
                "input_format": step.get("input_requirements", {}),
                "output_format": step.get("output_requirements", {}),
                "created_for_pipeline": True,
            }

            return spec

        except Exception as e:
            print(f"DEBUG: Agent spec generation failed: {str(e)}")
            # Fallback specification
            return {
                "name": f"pipeline_agent_step_{step_index}",
                "description": step.get(
                    "description", f"Agent for pipeline step {step_index}"
                ),
                "required_tools": [],
                "pipeline_context": {
                    "step_index": step_index,
                    "created_for_pipeline": True,
                },
            }

    async def _generate_enhanced_agent_spec(
        self, step: Dict, step_index: int, previous_step_output: Any = None
    ) -> Dict[str, Any]:
        """Generate enhanced agent specification with data type awareness."""

        input_type = (
            type(previous_step_output).__name__
            if previous_step_output is not None
            else "string"
        )
        input_sample = (
            str(previous_step_output)[:200] if previous_step_output else "text input"
        )

        # Enhanced prompt that DISCOURAGES unnecessary tool creation
        prompt = f"""
    Design a pipeline-aware agent for this step. IMPORTANT: Agents should be self-sufficient and only request tools for complex external operations.

    STEP REQUIREMENTS:
    - Name: {step.get('name', f'step_{step_index}')}  
    - Description: {step.get('description', '')}
    - Step Index: {step_index}
    - Expected Input Type: {input_type}
    - Input Sample: {input_sample}

    TOOL CREATION GUIDELINES:
    - DO NOT create tools for simple logic (prime checking, basic math, string operations)
    - DO NOT create tools for data parsing or filtering
    - ONLY create tools for:
    * External API calls
    * Complex file I/O operations  
    * Specialized libraries (PDF parsing, Excel manipulation)
    * Database connections

    For this step, determine if ANY tools are actually needed. Most likely, the answer is NO.

    Simple operations like:
    - Checking if a number is prime → Agent code
    - Calculating averages → Agent code  
    - Parsing strings → Agent code
    - Filtering lists → Agent code

    RESPOND WITH JSON:
    {{
        "name": "descriptive_agent_name",
        "description": "what this agent does",
        "required_tools": [],  // Usually empty! Only add if TRULY needed
        "new_tools_needed": [],  // Usually empty!
        "input_handling": {{
            "expected_type": "{input_type}",
            "error_handling": "how to handle wrong types",
            "data_extraction": "how to get data from pipeline state"
        }},
        "output_format": {{
            "type": "expected_output_type",
            "structure": "description of output structure"
        }},
        "agent_logic_description": "Describe what the agent will do internally WITHOUT external tools",
        "pipeline_context": {{
            "step_index": {step_index},
            "works_with_state": true,
            "data_flow_aware": true
        }}
    }}
    """

        try:
            response = await self._call_gpt4_json(
                system_prompt="Design intelligent pipeline agents that are self-sufficient.",
                user_prompt=prompt,
            )

            spec = json.loads(response)

            # Ensure required fields exist
            if "name" not in spec:
                spec["name"] = f"pipeline_agent_step_{step_index}"

            if "description" not in spec:
                spec["description"] = (
                    f"Agent for step {step_index} handling {input_type} input"
                )

            # Default to NO tools unless absolutely necessary
            if "required_tools" not in spec:
                spec["required_tools"] = []

            return spec

        except Exception as e:
            print(f"DEBUG: Enhanced agent spec generation failed: {str(e)}")
            # Fallback with NO tools
            return {
                "name": f"pipeline_agent_step_{step_index}",
                "description": f"Agent for step {step_index}",
                "required_tools": [],  # No tools by default
                "input_handling": {
                    "expected_type": input_type,
                    "error_handling": "flexible input processing",
                    "data_extraction": "extract from current_data in pipeline state",
                },
                "pipeline_context": {
                    "step_index": step_index,
                    "works_with_state": True,
                    "data_flow_aware": True,
                },
            }

    def _plan_data_flow(self, steps: List[Dict]) -> Dict[str, Any]:
        """Plan data flow between pipeline steps."""
        data_flow = {"flow_graph": {}, "transformations": [], "validation_points": []}

        for i, step in enumerate(steps):
            step_name = step["name"]

            # Input sources
            if i == 0:
                data_flow["flow_graph"][step_name] = {
                    "inputs": ["user_input"],
                    "outputs": [],
                }
            else:
                prev_step = steps[i - 1]["name"]
                data_flow["flow_graph"][step_name] = {
                    "inputs": [prev_step],
                    "outputs": [],
                }

            # Output targets
            if i < len(steps) - 1:
                next_step = steps[i + 1]["name"]
                data_flow["flow_graph"][step_name]["outputs"].append(next_step)
            else:
                data_flow["flow_graph"][step_name]["outputs"].append("final_output")

        return data_flow

    def _determine_execution_strategy(self, steps: List[Dict]) -> str:
        """Determine optimal execution strategy for the pipeline."""
        # For now, default to sequential
        # Can be enhanced to detect parallel opportunities
        return "sequential"

    async def execute_pipeline_with_adaptation(
        self, pipeline_plan: Dict, user_request: str, files: List[Dict] = None
    ) -> Dict[str, Any]:
        """
        Execute pipeline with real-time adaptation and recovery.

        Args:
            pipeline_plan: Complete pipeline execution plan
            user_request: Original user request
            files: Uploaded files

        Returns:
            Pipeline execution results
        """
        print(f"DEBUG: Executing pipeline with {pipeline_plan['total_steps']} steps")

        # Create missing agents/tools first
        if pipeline_plan.get("creation_needed"):
            creation_result = await self._create_pipeline_components(
                pipeline_plan["creation_needed"]
            )
            if creation_result["status"] != "success":
                return {
                    "status": "error",
                    "error": "Failed to create required components",
                }

        # VERIFY ALL AGENTS EXIST BEFORE EXECUTION
        required_agents = [
            step["agent_assigned"]
            for step in pipeline_plan["steps"]
            if step.get("agent_assigned")
        ]
        if not self._verify_agents_exist(required_agents):
            return {
                "status": "error",
                "error": "Required agents not found in registry after creation",
            }

        # Execute pipeline steps
        execution_result = {
            "status": "in_progress",
            "pipeline_id": pipeline_plan["pipeline_id"],
            "steps_completed": 0,
            "results": {},
            "errors": [],
            "adaptations": [],
        }

        current_data = {"user_request": user_request, "files": files}

        for i, step_plan in enumerate(pipeline_plan["steps"]):
            print(f"DEBUG: Executing step {i}: {step_plan['name']}")

            try:
                step_result = await self._execute_step_with_adaptation(
                    step_plan, current_data, execution_result
                )

                if step_result["status"] == "success":
                    execution_result["results"][step_plan["name"]] = step_result
                    execution_result["steps_completed"] += 1
                    current_data = step_result.get("data", current_data)
                else:
                    # Handle step failure with adaptation
                    adaptation_result = await self._handle_step_failure(
                        step_plan, step_result, pipeline_plan
                    )

                    if adaptation_result["status"] == "recovered":
                        execution_result["adaptations"].append(adaptation_result)
                        step_result = adaptation_result["recovery_result"]
                        execution_result["results"][step_plan["name"]] = step_result
                        execution_result["steps_completed"] += 1
                        current_data = step_result.get("data", current_data)
                    else:
                        execution_result["errors"].append(
                            {
                                "step": step_plan["name"],
                                "error": step_result.get("error", "Unknown error"),
                                "recovery_failed": True,
                            }
                        )
                        break

            except Exception as e:
                execution_result["errors"].append(
                    {"step": step_plan["name"], "error": str(e), "exception": True}
                )
                break

        # Determine final status
        if execution_result["steps_completed"] == pipeline_plan["total_steps"]:
            execution_result["status"] = "success"
        elif execution_result["steps_completed"] > 0:
            execution_result["status"] = "partial"
        else:
            execution_result["status"] = "failed"

        print(
            f"DEBUG: Pipeline execution completed - Status: {execution_result['status']}"
        )
        return execution_result

    async def _create_pipeline_components(
        self, creation_specs: List[Dict]
    ) -> Dict[str, Any]:
        """Create all required pipeline components."""
        print(f"DEBUG: Creating {len(creation_specs)} pipeline components")

        created = {"agents": [], "tools": []}
        failed = {"agents": [], "tools": []}

        for spec in creation_specs:
            try:
                if spec.get("type") == "agent" or "name" in spec:
                    # Create agent
                    result = self.agent_factory.create_pipeline_agent(spec)
                    print(f"DEBUG: Agent creation result: {result}")

                    if result["status"] == "success":
                        created["agents"].append(spec["name"])
                        print(f"DEBUG: Agent {spec['name']} created successfully")

                    else:
                        print(
                            f"DEBUG: Agent {spec['name']} creation failed: {result.get('message', 'unknown error')}"
                        )
                        failed["agents"].append(
                            {"name": spec["name"], "error": result.get("message")}
                        )

                elif spec.get("type") == "tool":
                    # Create tool
                    result = self.tool_factory.create_tool(
                        tool_name=spec["name"],
                        description=spec.get("description", ""),
                    )
                    if result["status"] == "success":
                        created["tools"].append(spec["name"])
                    else:
                        failed["tools"].append(
                            {"name": spec["name"], "error": result.get("message")}
                        )

            except Exception as e:
                print(f"DEBUG: Exception in component creation: {str(e)}")
                import traceback

                print(f"DEBUG: Traceback: {traceback.format_exc()}")
                failed["agents"].append(
                    {"name": spec.get("name", "unknown"), "error": str(e)}
                )

        if created["agents"] or created["tools"]:
            return {"status": "success", "created": created, "failed": failed}
        else:
            return {"status": "error", "created": created, "failed": failed}

    async def _execute_step_with_adaptation(
        self, step_plan: Dict, current_data: Any, execution_context: Dict
    ) -> Dict[str, Any]:
        """Execute a single pipeline step with adaptation capability."""
        agent_name = step_plan["agent_assigned"]

        if not agent_name:
            return {"status": "error", "error": "No agent assigned to step"}

        # Import and execute the agent
        try:
            from backup_removed_components.workflow_engine import WorkflowEngine
            from core.registry_singleton import get_shared_registry, force_global_reload

            # COMPREHENSIVE REGISTRY SYNCHRONIZATION
            force_global_reload()
            fresh_registry = get_shared_registry()

            # Verify agent exists before proceeding
            if not fresh_registry.agent_exists(agent_name):
                print(f"DEBUG: CRITICAL - Agent '{agent_name}' not found in registry")
                print(
                    f"DEBUG: Available agents: {list(fresh_registry.agents.get('agents', {}).keys())}"
                )
                return {
                    "status": "error",
                    "error": f"Agent '{agent_name}' not found in registry",
                }

            workflow_engine = WorkflowEngine(fresh_registry)
            print(
                f"DEBUG: Successfully verified agent '{agent_name}' exists in registry"
            )

            # Create minimal workflow state for single agent execution
            workflow_state = {
                "request": f"Execute step: {step_plan['description']}",
                "current_data": current_data,
                "execution_path": [],
                "results": {},
                "errors": [],
            }

            # Execute the agent
            result = await workflow_engine.execute_agent(agent_name, workflow_state)

            return result

        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def _handle_step_failure(
        self, step_plan: Dict, step_result: Dict, pipeline_plan: Dict
    ) -> Dict[str, Any]:
        """Handle step failure with real-time adaptation."""
        print(f"DEBUG: Handling failure for step: {step_plan['name']}")

        # Analyze failure reason
        failure_analysis = await self._analyze_step_failure(step_plan, step_result)

        # Generate recovery strategy
        recovery_prompt = PIPELINE_RECOVERY_PROMPT.format(
            step_name=step_plan["name"],
            step_description=step_plan["description"],
            failure_reason=step_result.get("error", "Unknown error"),
            failure_analysis=json.dumps(failure_analysis),
            available_agents=json.dumps(
                [a["name"] for a in self.registry.list_agents()]
            ),
        )

        try:
            response = await self._call_gpt4_json(
                system_prompt="Generate recovery strategies for failed pipeline steps.",
                user_prompt=recovery_prompt,
            )

            recovery_strategy = json.loads(response)

            # Execute recovery strategy
            if recovery_strategy.get("action") == "create_replacement_agent":
                # Create new agent to replace failed one
                replacement_spec = recovery_strategy.get("replacement_spec", {})
                creation_result = self.agent_factory.create_pipeline_agent(
                    replacement_spec
                )

                if creation_result["status"] == "success":
                    # Retry step with new agent
                    step_plan["agent_assigned"] = replacement_spec["name"]
                    retry_result = await self._execute_step_with_adaptation(
                        step_plan, {}, {}
                    )

                    return {
                        "status": "recovered",
                        "recovery_action": "created_replacement_agent",
                        "new_agent": replacement_spec["name"],
                        "recovery_result": retry_result,
                    }

            return {
                "status": "recovery_failed",
                "reason": "No viable recovery strategy",
            }

        except Exception as e:
            return {"status": "recovery_failed", "reason": str(e)}

    async def _analyze_step_failure(
        self, step_plan: Dict, step_result: Dict
    ) -> Dict[str, Any]:
        """Analyze why a pipeline step failed."""
        return {
            "step_name": step_plan["name"],
            "agent_used": step_plan["agent_assigned"],
            "error_message": step_result.get("error", "Unknown error"),
            "error_type": "execution_error",  # Can be enhanced
            "suggested_fixes": ["create_replacement_agent", "modify_input_format"],
        }

    def _format_components_list(
        self, components: List[Dict], component_type: str
    ) -> str:
        """Format list of components for prompts."""
        if not components:
            return f"No {component_type} available"

        formatted = []
        for comp in components:
            name = comp.get("name", "unknown")
            desc = comp.get("description", "No description")
            formatted.append(f"- {name}: {desc}")

        return "\n".join(formatted)

    async def _call_gpt4_json(
        self, system_prompt: str, user_prompt: str, temperature: float = 0.1
    ) -> str:
        """Call GPT-4 for JSON responses."""
        # Import the system prompt
        from config import DYNAMIC_INTELLIGENCE_SYSTEM_PROMPT

        # Combine system prompts
        enhanced_system_prompt = (
            f"{DYNAMIC_INTELLIGENCE_SYSTEM_PROMPT}\n\n{system_prompt}"
        )
        enhanced_user_prompt = (
            f"{user_prompt}\n\nRespond with ONLY valid JSON, no other text."
        )

        response = self.client.chat.completions.create(
            model=ORCHESTRATOR_MODEL,
            max_completion_tokens=ORCHESTRATOR_MAX_TOKENS,
            messages=[
                {"role": "system", "content": enhanced_system_prompt},
                {"role": "user", "content": enhanced_user_prompt},
            ],
        )

        content = response.choices[0].message.content

        # Extract JSON from response if it's wrapped in text
        if "```json" in content:
            start = content.find("```json") + 7
            end = content.find("```", start)
            if end > start:
                return content[start:end].strip()
        elif "{" in content:
            start = content.find("{")
            end = content.rfind("}") + 1
            if end > start:
                return content[start:end].strip()

        return content.strip()

    async def _analyze_request_complexity(
        self, user_request: str, files: List[Dict] = None
    ) -> str:
        """Analyze request complexity for pipeline routing."""
        request_lower = user_request.lower()

        # Pipeline indicators
        pipeline_keywords = [
            "then",
            "after",
            "next",
            "followed by",
            "and then",
            "first",
            "second",
            "third",
            "finally",
            "last",
            "extract and",
            "analyze and",
            "process and",
            "create and",
            "step by step",
            "pipeline",
            "workflow",
            "sequence",
        ]

        # Complex indicators
        complex_keywords = [
            "multiple files",
            "compare",
            "merge",
            "combine",
            "different formats",
            "various sources",
            "cross-reference",
            "comprehensive",
            "detailed analysis",
            "full report",
        ]

        # Count indicators
        pipeline_count = sum(
            1 for keyword in pipeline_keywords if keyword in request_lower
        )
        complex_count = sum(
            1 for keyword in complex_keywords if keyword in request_lower
        )

        # Check for numbered steps
        step_indicators = ["1.", "2.", "3.", "step 1", "step 2", "step 3"]
        step_count = sum(
            1 for indicator in step_indicators if indicator in request_lower
        )

        # File complexity
        multiple_files = files and len(files) > 1

        # Decision logic
        if complex_count > 0 or pipeline_count > 2 or step_count > 1 or multiple_files:
            return "complex"
        elif pipeline_count > 0 or len(request_lower.split()) > 20:
            return "pipeline"
        else:
            return "simple"

    async def _plan_step(
        self,
        step: Dict,
        step_index: int,
        auto_create: bool,
        previous_step_output: Any = None,
    ) -> Dict[str, Any]:
        """Plan execution for a single pipeline step."""
        step_plan = {
            "step_index": step_index,
            "name": step.get("name", f"step_{step_index}"),
            "description": step.get("description", ""),
            "input_requirements": step.get("input_requirements", {}),
            "output_requirements": step.get("output_requirements", {}),
            "agent_assigned": None,
            "needs_creation": False,
            "creation_specs": [],
            "estimated_time": 5,
        }

        # Find compatible agents
        compatible_agents = await self.compatibility_analyzer.find_compatible_agents(
            step
        )

        if compatible_agents:
            best_agent = compatible_agents[0]
            compatibility_score = best_agent.get("compatibility_score", 0.0)

            if compatibility_score >= 0.6:
                step_plan["agent_assigned"] = best_agent["name"]
                step_plan["estimated_time"] = best_agent.get("avg_execution_time", 5)
            elif auto_create:
                # Create new agent for better compatibility
                step_plan["needs_creation"] = True
                agent_spec = await self._generate_enhanced_agent_spec(
                    step, step_index, previous_step_output
                )
                # FIX: Convert agent name to lowercase
                agent_spec["name"] = agent_spec["name"].lower()
                step_plan["creation_specs"].append(agent_spec)
                step_plan["agent_assigned"] = agent_spec["name"]
            else:
                # Use best available even if not perfect
                step_plan["agent_assigned"] = best_agent["name"]

        elif auto_create:
            # No compatible agents - create new one
            step_plan["needs_creation"] = True
            agent_spec = await self._generate_enhanced_agent_spec(
                step, step_index, previous_step_output
            )
            # FIX: Convert agent name to lowercase
            agent_spec["name"] = agent_spec["name"].lower()
            step_plan["creation_specs"].append(agent_spec)
            step_plan["agent_assigned"] = agent_spec["name"]

        return step_plan

    def _verify_agents_exist(self, agent_names: List[str]) -> bool:
        """Verify all required agents exist in registry"""
        from core.registry_singleton import get_shared_registry, force_global_reload

        force_global_reload()
        registry = get_shared_registry()

        available_agents = list(registry.agents.get("agents", {}).keys())
        print(f"DEBUG: Available agents in registry: {available_agents}")

        missing_agents = []
        for agent_name in agent_names:
            if not registry.agent_exists(agent_name):
                missing_agents.append(agent_name)

        if missing_agents:
            print(f"DEBUG: Missing agents: {missing_agents}")
            return False

        print(f"DEBUG: All required agents found: {agent_names}")
        return True

```

--------------------------------------------------------------------------------

### File: core/registry.py
**Path:** `core/registry.py`
**Size:** 31,558 bytes
**Modified:** 2025-09-04 23:09:56

```python
"""
Registry Manager
Unified registry management for agents and tools with advanced features
"""

import json
import os
import shutil
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path

# Import configuration
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (
    AGENTS_REGISTRY_PATH,
    TOOLS_REGISTRY_PATH,
    GENERATED_AGENTS_DIR,
    GENERATED_TOOLS_DIR,
    PREBUILT_AGENTS_DIR,
    PREBUILT_TOOLS_DIR,
    BACKUP_DIR,
    CLAUDE_MODEL,
    AGENT_OUTPUT_SCHEMA,
    MIN_AGENT_LINES,
    MAX_AGENT_LINES,
    MIN_TOOL_LINES,
    MAX_TOOL_LINES,
)


class RegistryManager:
    """
    Centralized registry management for the Agentic Fabric POC.
    Handles agent and tool registration, validation, dependencies, and analytics.
    """

    def __init__(self, agents_path: str = None, tools_path: str = None):
        """Initialize registry manager with paths from config."""
        self.agents_path = agents_path or AGENTS_REGISTRY_PATH
        self.tools_path = tools_path or TOOLS_REGISTRY_PATH
        self.backup_dir = BACKUP_DIR

        # Create necessary directories
        os.makedirs(GENERATED_AGENTS_DIR, exist_ok=True)
        os.makedirs(GENERATED_TOOLS_DIR, exist_ok=True)
        os.makedirs(PREBUILT_AGENTS_DIR, exist_ok=True)
        os.makedirs(PREBUILT_TOOLS_DIR, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)

        # ADD THIS DEBUG AND VERIFICATION
        print(f"DEBUG: Loading registries from:")
        print(f"  Agents: {self.agents_path}")
        print(f"  Tools: {self.tools_path}")
        print(f"  Agents file exists: {os.path.exists(self.agents_path)}")
        print(f"  Tools file exists: {os.path.exists(self.tools_path)}")

        # Load registries
        self.agents = self._load_registry(self.agents_path)
        self.tools = self._load_registry(self.tools_path)

        # ADD THIS VERIFICATION
        print(f"DEBUG: Loaded {len(self.agents.get('agents', {}))} agents")
        print(f"DEBUG: Loaded {len(self.tools.get('tools', {}))} tools")
        print(f"DEBUG: Agent keys: {list(self.agents.get('agents', {}).keys())}")
        print(f"DEBUG: Tool keys: {list(self.tools.get('tools', {}).keys())}")

    def _load_registry(self, path: str) -> Dict:
        """Load registry from JSON file with proper structure."""
        print(f"DEBUG: Loading registry from {path}")

        try:
            if not os.path.exists(path):
                print(f"DEBUG: Registry file doesn't exist: {path}")
                if "agents" in path:
                    return {"agents": {}}
                else:
                    return {"tools": {}}

            with open(path, "r") as f:
                data = json.load(f)
                print(f"DEBUG: Loaded registry data keys: {list(data.keys())}")

                # Ensure proper structure
                if "agents" in path and "agents" not in data:
                    print(
                        f"DEBUG: Agents registry missing 'agents' key, creating empty"
                    )
                    return {"agents": {}}
                elif "tools" in path and "tools" not in data:
                    print(f"DEBUG: Tools registry missing 'tools' key, creating empty")
                    return {"tools": {}}

                return data

        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"DEBUG: Error loading registry {path}: {e}")
            # Initialize empty registry with proper structure
            if "agents" in path:
                return {"agents": {}}
            else:
                return {"tools": {}}

    def _save_registry(self, data: Dict, path: str):
        """Save registry to JSON file."""
        # Ensure directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(data, f, indent=2, default=str)

    def save_all(self):
        """Save both registries to disk and notify singleton to reload."""
        self._save_registry(self.agents, self.agents_path)
        self._save_registry(self.tools, self.tools_path)

        # Notify singleton pattern to reload for other instances
        try:
            from core.registry_singleton import RegistrySingleton

            # Only reload if we're not already the singleton instance
            singleton_instance = RegistrySingleton()
            if singleton_instance.get_registry() is not self:
                singleton_instance.force_reload()
        except:
            pass  # Ignore circular import or other issues

    # =============================================================================
    # AGENT OPERATIONS
    # =============================================================================

    def register_agent(
        self,
        name: str,
        description: str,
        code: str,
        uses_tools: List[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Register a new agent in the registry with verification.
        """
        # First verify all required tools exist
        uses_tools = uses_tools or []
        missing_tools = []

        for tool_name in uses_tools:
            if not self.tool_exists(tool_name):
                missing_tools.append(tool_name)

        if missing_tools:
            return {
                "status": "error",
                "message": f"Required tools not found: {', '.join(missing_tools)}",
                "missing_tools": missing_tools,
            }

        # Determine file path
        is_prebuilt = kwargs.get("is_prebuilt", False)
        if is_prebuilt:
            file_path = os.path.join(PREBUILT_AGENTS_DIR, f"{name}_agent.py")
        else:
            file_path = os.path.join(GENERATED_AGENTS_DIR, f"{name}_agent.py")

        # Write code to file with verification
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        try:
            with open(file_path, "w") as f:
                f.write(code)
                f.flush()
                os.fsync(f.fileno())  # Force write to disk
        except IOError as e:
            return {
                "status": "error",
                "message": f"Failed to write agent file: {str(e)}",
            }

        # Verify file exists
        if not os.path.exists(file_path):
            return {
                "status": "error",
                "message": f"Agent file was not created: {file_path}",
            }

        # Try to import it to verify syntax
        try:
            import importlib.util

            spec = importlib.util.spec_from_file_location(f"{name}_module", file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Verify the agent function exists
            agent_func_name = f"{name}_agent"
            if not hasattr(module, agent_func_name) and not hasattr(module, name):
                # Delete the broken file
                os.remove(file_path)
                return {
                    "status": "error",
                    "message": f"Agent function {agent_func_name} not found in generated code",
                }
        except Exception as e:
            # Delete the broken file
            if os.path.exists(file_path):
                os.remove(file_path)
            return {
                "status": "error",
                "message": f"Agent code validation failed: {str(e)}",
            }

        # Generate version hash
        version_hash = hashlib.md5(code.encode()).hexdigest()[:8]

        # Create agent entry
        agent_entry = {
            "name": name,
            "description": description,
            "uses_tools": uses_tools,
            "input_schema": kwargs.get("input_schema", {"data": "any"}),
            "output_schema": kwargs.get("output_schema", AGENT_OUTPUT_SCHEMA),
            "location": file_path,
            "is_prebuilt": is_prebuilt,
            "created_by": kwargs.get("created_by", CLAUDE_MODEL),
            "created_at": datetime.now().isoformat(),
            "version": f"1.0.{version_hash}",
            "execution_count": 0,
            "avg_execution_time": 0.0,
            "last_executed": None,
            "tags": kwargs.get("tags", []),
            "line_count": len(code.splitlines()),
            "status": "active",
        }

        # Update registry using singleton for atomic write
        self.agents["agents"][name] = agent_entry

        # Use singleton's atomic update
        from core.registry_singleton import RegistrySingleton

        singleton = RegistrySingleton()
        singleton.atomic_update(self.agents_path, self.agents)

        # Update tool references
        if uses_tools:
            for tool_name in uses_tools:
                if tool_name in self.tools.get("tools", {}):
                    if "used_by_agents" not in self.tools["tools"][tool_name]:
                        self.tools["tools"][tool_name]["used_by_agents"] = []
                    if name not in self.tools["tools"][tool_name]["used_by_agents"]:
                        self.tools["tools"][tool_name]["used_by_agents"].append(name)

            singleton.atomic_update(self.tools_path, self.tools)

        # Force reload for all instances
        singleton.force_reload()

        print(f"DEBUG: Agent '{name}' registered successfully with verification")

        return {
            "status": "success",
            "message": f"Agent '{name}' registered successfully",
            "location": file_path,
            "line_count": len(code.splitlines()),
        }

    def get_agent(self, name: str) -> Optional[Dict]:
        """Get agent details by name."""
        return self.agents.get("agents", {}).get(name)

    def list_agents(
        self, tags: List[str] = None, active_only: bool = True
    ) -> List[Dict]:
        """List agents with optional filtering."""
        agents = []
        for name, details in self.agents.get("agents", {}).items():
            # Filter by status
            if active_only and details.get("status") != "active":
                continue

            # Filter by tags
            if tags and not any(tag in details.get("tags", []) for tag in tags):
                continue

            agents.append({"name": name, **details})

        return sorted(agents, key=lambda x: x.get("created_at", ""), reverse=True)

    def agent_exists(self, name: str) -> bool:
        """Check if an agent exists and is active."""
        print(f"DEBUG: Checking if agent '{name}' exists")
        print(
            f"DEBUG: Available agent keys: {list(self.agents.get('agents', {}).keys())}"
        )

        agent = self.get_agent(name)
        exists = agent is not None and agent.get("status") == "active"

        print(f"DEBUG: Agent '{name}' exists: {exists}")
        if agent:
            print(f"DEBUG: Agent status: {agent.get('status')}")
        else:
            print(f"DEBUG: Agent '{name}' not found in registry")

        return exists

    def update_agent_metrics(self, name: str, execution_time: float):
        """Update execution metrics for an agent."""
        if name in self.agents.get("agents", {}):
            agent = self.agents["agents"][name]
            count = agent.get("execution_count", 0)
            avg_time = agent.get("avg_execution_time", 0)

            # Calculate new average
            new_count = count + 1
            new_avg = ((avg_time * count) + execution_time) / new_count

            agent["execution_count"] = new_count
            agent["avg_execution_time"] = round(new_avg, 3)
            agent["last_executed"] = datetime.now().isoformat()

            self.save_all()

    # =============================================================================
    # TOOL OPERATIONS
    # =============================================================================

    def register_tool(
        self, name: str, description: str, code: str, **kwargs
    ) -> Dict[str, Any]:
        """
        Register a new tool in the registry with verification.
        """
        # Validate code size
        line_count = len(code.splitlines())
        if line_count < MIN_TOOL_LINES or line_count > MAX_TOOL_LINES:
            return {
                "status": "error",
                "message": f"Tool must be {MIN_TOOL_LINES}-{MAX_TOOL_LINES} lines, got {line_count}",
            }

        # Determine file path
        is_prebuilt = kwargs.get("is_prebuilt", False)
        if is_prebuilt:
            file_path = os.path.join(PREBUILT_TOOLS_DIR, f"{name}.py")
        else:
            file_path = os.path.join(GENERATED_TOOLS_DIR, f"{name}.py")

        # Write and verify
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        try:
            with open(file_path, "w") as f:
                f.write(code)
                f.flush()
                os.fsync(f.fileno())
        except IOError as e:
            return {
                "status": "error",
                "message": f"Failed to write tool file: {str(e)}",
            }

        if not os.path.exists(file_path):
            return {
                "status": "error",
                "message": f"Tool file was not created: {file_path}",
            }

        # Import and test the tool
        try:
            import importlib.util

            spec = importlib.util.spec_from_file_location(name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if not hasattr(module, name):
                os.remove(file_path)
                return {"status": "error", "message": f"Tool function {name} not found"}

            # Test the tool with None input (should not crash)
            tool_func = getattr(module, name)
            result = tool_func(None)  # Tools must handle None

        except Exception as e:
            if os.path.exists(file_path):
                os.remove(file_path)
            return {"status": "error", "message": f"Tool validation failed: {str(e)}"}

        # Extract signature if not provided
        signature = kwargs.get("signature")
        if not signature:
            for line in code.split("\n"):
                if line.strip().startswith("def "):
                    signature = line.strip()
                    break

        # Create tool entry
        tool_entry = {
            "name": name,
            "description": description,
            "signature": signature or f"def {name}(input_data=None)",
            "location": file_path,
            "is_prebuilt": is_prebuilt,
            "is_pure_function": kwargs.get("is_pure_function", True),
            "used_by_agents": [],
            "created_by": kwargs.get("created_by", CLAUDE_MODEL),
            "created_at": datetime.now().isoformat(),
            "tags": kwargs.get("tags", []),
            "line_count": line_count,
            "status": "active",
        }

        # Update registry using singleton
        self.tools["tools"][name] = tool_entry

        from core.registry_singleton import RegistrySingleton

        singleton = RegistrySingleton()
        singleton.atomic_update(self.tools_path, self.tools)
        singleton.force_reload()

        print(f"DEBUG: Tool '{name}' registered successfully with verification")

        return {
            "status": "success",
            "message": f"Tool '{name}' registered successfully",
            "location": file_path,
            "line_count": line_count,
        }

    def get_tool(self, name: str) -> Optional[Dict]:
        """Get tool details by name."""
        return self.tools.get("tools", {}).get(name)

    def list_tools(self, tags: List[str] = None, pure_only: bool = False) -> List[Dict]:
        """List tools with optional filtering."""
        tools = []
        for name, details in self.tools.get("tools", {}).items():
            # Filter by purity
            if pure_only and not details.get("is_pure_function", True):
                continue

            # Filter by tags
            if tags and not any(tag in details.get("tags", []) for tag in tags):
                continue

            tools.append({"name": name, **details})

        return sorted(tools, key=lambda x: x.get("created_at", ""), reverse=True)

    def tool_exists(self, name: str) -> bool:
        """Check if a tool exists and is active."""
        print(f"DEBUG: Checking if tool '{name}' exists")
        print(f"DEBUG: Available tool keys: {list(self.tools.get('tools', {}).keys())}")

        tool = self.get_tool(name)
        exists = tool is not None and tool.get("status") == "active"

        print(f"DEBUG: Tool '{name}' exists: {exists}")
        if tool:
            print(f"DEBUG: Tool status: {tool.get('status')}")
        else:
            print(f"DEBUG: Tool '{name}' not found in registry")

        return exists

    # =============================================================================
    # DEPENDENCY MANAGEMENT
    # =============================================================================

    def get_agent_dependencies(self, agent_name: str) -> Dict[str, List[str]]:
        """Get all dependencies for an agent."""
        agent = self.get_agent(agent_name)
        if not agent:
            return {"tools": [], "missing_tools": []}

        tools_needed = agent.get("uses_tools", [])
        missing_tools = [tool for tool in tools_needed if not self.tool_exists(tool)]

        return {
            "tools": tools_needed,
            "missing_tools": missing_tools,
            "available_tools": [t for t in tools_needed if self.tool_exists(t)],
        }

    def get_tool_usage(self, tool_name: str) -> List[str]:
        """Get list of agents using a specific tool."""
        tool = self.get_tool(tool_name)
        return tool.get("used_by_agents", []) if tool else []

    def get_dependency_graph(self) -> Dict[str, Any]:
        """Build complete dependency graph."""
        graph = {
            "agents_to_tools": {},
            "tools_to_agents": {},
            "missing_dependencies": [],
            "unused_tools": [],
        }

        # Build agent to tool mapping
        for agent_name, agent_data in self.agents.get("agents", {}).items():
            if agent_data.get("status") == "active":
                tools = agent_data.get("uses_tools", [])
                graph["agents_to_tools"][agent_name] = tools

                # Check for missing dependencies
                for tool in tools:
                    if not self.tool_exists(tool):
                        graph["missing_dependencies"].append(
                            {"agent": agent_name, "missing_tool": tool}
                        )

        # Build tool to agent mapping
        for tool_name, tool_data in self.tools.get("tools", {}).items():
            if tool_data.get("status") == "active":
                agents = tool_data.get("used_by_agents", [])
                graph["tools_to_agents"][tool_name] = agents

                # Check for unused tools
                if not agents:
                    graph["unused_tools"].append(tool_name)

        return graph

    # =============================================================================
    # VALIDATION
    # =============================================================================

    def validate_all(self) -> Dict[str, List]:
        """Validate all components in the registry."""
        results = {
            "valid_agents": [],
            "invalid_agents": [],
            "valid_tools": [],
            "invalid_tools": [],
            "missing_files": [],
            "dependency_issues": [],
        }

        # Validate agents
        for name, agent in self.agents.get("agents", {}).items():
            file_path = agent.get("location", "")
            issues = []

            # Check file existence
            if not os.path.exists(file_path):
                issues.append(f"Missing file: {file_path}")
                results["missing_files"].append(f"Agent: {name}")

            # Check dependencies
            deps = self.get_agent_dependencies(name)
            if deps["missing_tools"]:
                issues.append(f"Missing tools: {', '.join(deps['missing_tools'])}")
                results["dependency_issues"].append(
                    {"agent": name, "missing": deps["missing_tools"]}
                )

            # Check line count
            line_count = agent.get("line_count", 0)
            if line_count < MIN_AGENT_LINES or line_count > MAX_AGENT_LINES:
                issues.append(f"Invalid size: {line_count} lines")

            if issues:
                results["invalid_agents"].append({"name": name, "issues": issues})
            else:
                results["valid_agents"].append(name)

        # Validate tools
        for name, tool in self.tools.get("tools", {}).items():
            file_path = tool.get("location", "")
            issues = []

            # Check file existence
            if not os.path.exists(file_path):
                issues.append(f"Missing file: {file_path}")
                results["missing_files"].append(f"Tool: {name}")

            # Check line count
            line_count = tool.get("line_count", 0)
            if line_count < MIN_TOOL_LINES or line_count > MAX_TOOL_LINES:
                issues.append(f"Invalid size: {line_count} lines")

            if issues:
                results["invalid_tools"].append({"name": name, "issues": issues})
            else:
                results["valid_tools"].append(name)

        return results

    def health_check(self) -> Dict[str, Any]:
        """Perform comprehensive health check."""
        validation = self.validate_all()
        stats = self.get_statistics()

        # Calculate health score
        total_agents = stats["total_agents"]
        total_tools = stats["total_tools"]
        valid_agents = len(validation["valid_agents"])
        valid_tools = len(validation["valid_tools"])

        health_score = 100.0
        if total_agents > 0:
            health_score -= (1 - valid_agents / total_agents) * 50
        if total_tools > 0:
            health_score -= (1 - valid_tools / total_tools) * 50

        return {
            "health_score": round(max(0, health_score), 1),
            "status": (
                "healthy"
                if health_score >= 80
                else "degraded" if health_score >= 50 else "unhealthy"
            ),
            "total_components": total_agents + total_tools,
            "valid_components": valid_agents + valid_tools,
            "issues": {
                "invalid_agents": len(validation["invalid_agents"]),
                "invalid_tools": len(validation["invalid_tools"]),
                "missing_files": len(validation["missing_files"]),
                "dependency_issues": len(validation["dependency_issues"]),
            },
            "statistics": stats,
            "validation_details": validation,
        }

    # =============================================================================
    # SEARCH AND DISCOVERY
    # =============================================================================

    def search_agents(self, query: str) -> List[Dict]:
        """Search agents by name or description."""
        query_lower = query.lower()
        results = []

        for name, details in self.agents.get("agents", {}).items():
            if details.get("status") != "active":
                continue

            if (
                query_lower in name.lower()
                or query_lower in details.get("description", "").lower()
                or any(query_lower in tag for tag in details.get("tags", []))
            ):
                results.append({"name": name, **details})

        return results

    def search_tools(self, query: str) -> List[Dict]:
        """Search tools by name or description."""
        query_lower = query.lower()
        results = []

        for name, details in self.tools.get("tools", {}).items():
            if details.get("status") != "active":
                continue

            if (
                query_lower in name.lower()
                or query_lower in details.get("description", "").lower()
                or any(query_lower in tag for tag in details.get("tags", []))
            ):
                results.append({"name": name, **details})

        return results

    def find_capable_agents(self, task: str) -> List[Dict]:
        """Find agents capable of handling a task."""
        # Search by task keywords
        agents = self.search_agents(task)

        # Sort by relevance (execution count as proxy for reliability)
        agents.sort(key=lambda x: x.get("execution_count", 0), reverse=True)

        return agents

    # =============================================================================
    # STATISTICS AND ANALYTICS
    # =============================================================================

    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive registry statistics."""
        agents_list = self.agents.get("agents", {})
        tools_list = self.tools.get("tools", {})

        active_agents = [a for a in agents_list.values() if a.get("status") == "active"]
        active_tools = [t for t in tools_list.values() if t.get("status") == "active"]

        # Calculate metrics
        total_executions = sum(a.get("execution_count", 0) for a in active_agents)

        return {
            "total_agents": len(active_agents),
            "total_tools": len(active_tools),
            "prebuilt_agents": sum(1 for a in active_agents if a.get("is_prebuilt")),
            "generated_agents": sum(
                1 for a in active_agents if not a.get("is_prebuilt")
            ),
            "prebuilt_tools": sum(1 for t in active_tools if t.get("is_prebuilt")),
            "generated_tools": sum(1 for t in active_tools if not t.get("is_prebuilt")),
            "total_executions": total_executions,
            "avg_agent_lines": round(
                sum(a.get("line_count", 0) for a in active_agents)
                / max(len(active_agents), 1),
                1,
            ),
            "avg_tool_lines": round(
                sum(t.get("line_count", 0) for t in active_tools)
                / max(len(active_tools), 1),
                1,
            ),
            "tool_reuse_rate": round(
                sum(len(t.get("used_by_agents", [])) for t in active_tools)
                / max(len(active_tools), 1),
                2,
            ),
            "most_used_agent": (
                max(active_agents, key=lambda x: x.get("execution_count", 0))["name"]
                if active_agents
                else None
            ),
            "newest_agent": (
                max(active_agents, key=lambda x: x.get("created_at", ""))["name"]
                if active_agents
                else None
            ),
        }

    # =============================================================================
    # BACKUP AND RESTORE
    # =============================================================================

    def backup_registries(self, tag: str = None) -> str:
        """Create backup of current registries."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}"
        if tag:
            backup_name += f"_{tag}"

        backup_path = os.path.join(self.backup_dir, backup_name)
        os.makedirs(backup_path, exist_ok=True)

        # Copy registry files
        shutil.copy(self.agents_path, os.path.join(backup_path, "agents.json"))
        shutil.copy(self.tools_path, os.path.join(backup_path, "tools.json"))

        # Save metadata
        metadata = {
            "timestamp": datetime.now().isoformat(),
            "tag": tag,
            "stats": self.get_statistics(),
            "health": self.health_check(),
        }

        with open(os.path.join(backup_path, "metadata.json"), "w") as f:
            json.dump(metadata, f, indent=2)

        return backup_path

    def restore_registries(self, backup_name: str) -> bool:
        """Restore registries from backup."""
        backup_path = os.path.join(self.backup_dir, backup_name)

        if not os.path.exists(backup_path):
            return False

        try:
            # Create current backup before restore
            self.backup_registries("before_restore")

            # Restore files
            shutil.copy(os.path.join(backup_path, "agents.json"), self.agents_path)
            shutil.copy(os.path.join(backup_path, "tools.json"), self.tools_path)

            # Reload registries
            self.agents = self._load_registry(self.agents_path)
            self.tools = self._load_registry(self.tools_path)

            return True
        except Exception:
            return False

    # =============================================================================
    # CLEANUP AND OPTIMIZATION
    # =============================================================================

    def optimize_registry(self, dry_run: bool = True) -> Dict[str, Any]:
        """Optimize registry by cleaning up issues."""
        report = {
            "unused_tools": [],
            "broken_agents": [],
            "broken_tools": [],
            "fixed_dependencies": [],
            "actions_taken": [],
        }

        # Find unused tools
        deps = self.get_dependency_graph()
        report["unused_tools"] = deps["unused_tools"]

        # Find broken components
        validation = self.validate_all()
        report["broken_agents"] = [a["name"] for a in validation["invalid_agents"]]
        report["broken_tools"] = [t["name"] for t in validation["invalid_tools"]]

        if not dry_run:
            # Remove unused tools
            for tool_name in report["unused_tools"]:
                if tool_name in self.tools["tools"]:
                    self.tools["tools"][tool_name]["status"] = "deprecated"
                    report["actions_taken"].append(
                        f"Deprecated unused tool: {tool_name}"
                    )

            # Mark broken components
            for agent_name in report["broken_agents"]:
                if agent_name in self.agents["agents"]:
                    self.agents["agents"][agent_name]["status"] = "broken"
                    report["actions_taken"].append(f"Marked broken agent: {agent_name}")

            for tool_name in report["broken_tools"]:
                if tool_name in self.tools["tools"]:
                    self.tools["tools"][tool_name]["status"] = "broken"
                    report["actions_taken"].append(f"Marked broken tool: {tool_name}")

            self.save_all()

        return report

    def cleanup_deprecated(self) -> int:
        """Remove deprecated components."""
        count = 0

        # Clean deprecated agents
        for name in list(self.agents["agents"].keys()):
            if self.agents["agents"][name].get("status") == "deprecated":
                del self.agents["agents"][name]
                count += 1

        # Clean deprecated tools
        for name in list(self.tools["tools"].keys()):
            if self.tools["tools"][name].get("status") == "deprecated":
                del self.tools["tools"][name]
                count += 1

        if count > 0:
            self.save_all()

        return count

```

--------------------------------------------------------------------------------

### File: core/registry_singleton.py
**Path:** `core/registry_singleton.py`
**Size:** 4,120 bytes
**Modified:** 2025-09-04 22:43:11

```python
"""
Registry Singleton - FIXED VERSION
Ensures all components share the same registry instance with proper synchronization
"""

import threading
import os
import fcntl
import time
import json
from pathlib import Path
from typing import Optional


class RegistrySingleton:
    """Thread-safe singleton pattern for registry management."""

    _instance = None
    _lock = threading.RLock()  # Reentrant lock
    _registry = None
    _file_locks = {}
    _last_reload = 0
    _reload_interval = 0.5  # Minimum seconds between reloads

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(RegistrySingleton, cls).__new__(cls)
                    # Import here to avoid circular dependency
                    from core.registry import RegistryManager

                    cls._instance._registry = RegistryManager()
                    cls._instance._last_reload = time.time()
        return cls._instance

    def get_registry(self):
        """Get the shared registry instance with automatic reload if needed."""
        with self._lock:
            # Check if files have been modified since last load
            if self._should_reload():
                self._reload_registry()
            return self._registry

    def _should_reload(self) -> bool:
        """Check if registry files have been modified."""
        current_time = time.time()
        if current_time - self._last_reload < self._reload_interval:
            return False

        # Check file modification times
        from config import AGENTS_REGISTRY_PATH, TOOLS_REGISTRY_PATH

        for path in [AGENTS_REGISTRY_PATH, TOOLS_REGISTRY_PATH]:
            if os.path.exists(path):
                mtime = os.path.getmtime(path)
                if mtime > self._last_reload:
                    return True
        return False

    def _reload_registry(self):
        """Reload registry from disk with file locking."""
        from core.registry import RegistryManager

        # Create new registry instance that will load from files
        new_registry = RegistryManager()

        # Atomic swap
        self._registry = new_registry
        self._last_reload = time.time()
        print(f"DEBUG: Registry reloaded at {self._last_reload}")

    def force_reload(self):
        """Force reload the registry from disk."""
        with self._lock:
            self._reload_registry()

    def acquire_file_lock(self, filepath: str):
        """Acquire file lock for atomic operations."""
        if filepath not in self._file_locks:
            lock_path = f"{filepath}.lock"
            self._file_locks[filepath] = open(lock_path, "w")

        fcntl.flock(self._file_locks[filepath], fcntl.LOCK_EX)

    def release_file_lock(self, filepath: str):
        """Release file lock."""
        if filepath in self._file_locks:
            fcntl.flock(self._file_locks[filepath], fcntl.LOCK_UN)

    def atomic_update(self, filepath: str, data: dict):
        """Atomically update a JSON file."""
        with self._lock:
            self.acquire_file_lock(filepath)
            try:
                # Write to temporary file first
                temp_path = f"{filepath}.tmp"
                with open(temp_path, "w") as f:
                    json.dump(data, f, indent=2, default=str)

                # Atomic rename
                os.replace(temp_path, filepath)

                # Force sync to disk
                os.sync()
            finally:
                self.release_file_lock(filepath)


# Global function to get shared registry
_singleton = None
_singleton_lock = threading.Lock()


def get_shared_registry():
    """Get the shared registry instance - thread-safe."""
    global _singleton
    if _singleton is None:
        with _singleton_lock:
            if _singleton is None:
                _singleton = RegistrySingleton()
    return _singleton.get_registry()


def force_global_reload():
    """Force reload all registry instances."""
    global _singleton
    if _singleton:
        _singleton.force_reload()

```

--------------------------------------------------------------------------------

### File: core/simplified_orchestrator.py
**Path:** `core/simplified_orchestrator.py`
**Size:** 27,866 bytes
**Modified:** 2025-09-14 09:36:01

```python
"""
Simplified AI-Powered Orchestrator
Uses GPT-4 for planning and Claude for agent execution
"""

import os
import json
import asyncio
import importlib
from typing import Dict, List, Optional, Any
from datetime import datetime
import openai
from anthropic import Anthropic

from config import (
    OPENAI_API_KEY,
    ANTHROPIC_API_KEY,
    ORCHESTRATOR_MODEL,
    CLAUDE_MODEL,
    ORCHESTRATOR_MAX_TOKENS,
    CLAUDE_MAX_TOKENS,
)
from core.registry import RegistryManager
from core.registry_singleton import get_shared_registry
from core.file_content_reader import FileContentReader
from core.agent_factory import AgentFactory
from core.tool_factory import ToolFactory

from core.workflow_engine import MultiAgentWorkflowEngine, WorkflowPlanner
from core.specialized_agents import (
    PDFAnalyzerAgent,
    ChartGeneratorAgent,
    TextProcessorAgent,
)


class SimplifiedOrchestrator:
    """
    Simplified orchestrator that uses AI for all major decisions.
    Core principle: Let AI handle complexity, not code.
    """

    def __init__(self):
        # Initialize registry
        self.registry = RegistryManager()
        self.agent_factory = AgentFactory()
        self.tool_factory = ToolFactory()
        self.file_reader = FileContentReader()

        self.workflow_engine = MultiAgentWorkflowEngine()
        self.workflow_planner = WorkflowPlanner()

        # FIX: Initialize the OpenAI openai_client properly
        self.openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)  # Add this line!

        # Initialize Claude openai_client
        self.claude_client = Anthropic(api_key=ANTHROPIC_API_KEY)

        print(f"DEBUG: ANTHROPIC_API_KEY present: {bool(ANTHROPIC_API_KEY)}")
        print(
            f"DEBUG: ANTHROPIC_API_KEY length: {len(ANTHROPIC_API_KEY) if ANTHROPIC_API_KEY else 0}"
        )

    # async def process_request(
    #     self,
    #     user_request: str,
    #     files: Optional[List[Dict]] = None,
    #     auto_create: bool = True,
    # ) -> Dict[str, Any]:
    #     """
    #     Main entry point - process any request with AI intelligence.
    #     """
    #     workflow_id = f"wf_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    #     start_time = datetime.now()

    #     try:
    #         # Step 1: Read actual file contents (not just metadata!)
    #         enriched_files = []
    #         if files:
    #             enriched_files = self.file_reader.process_all_files(files)
    #             for file in enriched_files:
    #                 if file.get("read_success"):
    #                     print(
    #                         f"✓ Read {file['original_name']}: {file.get('structure')} with {file['content'].get('total_rows', 'N/A')} rows"
    #                     )

    #         # Step 2: AI analyzes request with REAL data
    #         analysis = await self._analyze_with_ai(user_request, enriched_files)

    #         # Step 3: AI plans workflow based on actual data
    #         plan = await self._ai_plan_workflow(user_request, enriched_files, analysis)

    #         # Step 4: Create missing components if needed
    #         if auto_create and plan.get("missing_components"):
    #             await self._create_missing_components(plan["missing_components"])

    #         # Step 5: Execute workflow with AI-powered agents
    #         results = await self._execute_ai_workflow(
    #             plan, user_request, enriched_files
    #         )

    #         # Step 6: AI synthesizes final response
    #         response = await self._ai_synthesize_response(user_request, plan, results)

    #         return {
    #             "status": "success",
    #             "workflow_id": workflow_id,
    #             "response": response,
    #             "execution_time": (datetime.now() - start_time).total_seconds(),
    #             "workflow": plan,
    #             "results": results,
    #             "metadata": {
    #                 "files_processed": len(enriched_files),
    #                 "agents_used": len(plan.get("agents", [])),
    #                 "ai_calls": plan.get("ai_calls", 0),
    #             },
    #         }

    #     except Exception as e:
    #         print(f"❌ Error: {str(e)}")
    #         import traceback

    #         traceback.print_exc()
    #         return {
    #             "status": "error",
    #             "workflow_id": workflow_id,
    #             "error": str(e),
    #             "response": f"An error occurred: {str(e)}",  # Always include response
    #             "workflow": {},
    #             "metadata": {},
    #         }

    async def process_request(
        self,
        user_request: str,
        files: Optional[List[Dict]] = None,
        auto_create: bool = True,
    ) -> Dict[str, Any]:
        """Enhanced process_request with multi-agent workflow support."""
        workflow_id = f"wf_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        start_time = datetime.now()

        try:
            # Step 1: Read actual file contents
            enriched_files = []
            if files:
                enriched_files = self.file_reader.process_all_files(files)

            # Step 2: Determine if this needs multi-agent workflow
            workflow_plan = self.workflow_planner.plan_workflow(
                user_request, enriched_files
            )

            if len(workflow_plan["agents"]) > 1:
                print(f"Multi-agent workflow detected: {workflow_plan['agents']}")

                # Execute multi-agent workflow
                workflow_result = await self.workflow_engine.execute_workflow(
                    workflow_plan, user_request, enriched_files
                )

                # Synthesize final response from workflow
                response = await self._synthesize_workflow_response(
                    user_request, workflow_result
                )

                return {
                    "status": "success",
                    "workflow_id": workflow_id,
                    "response": response,
                    "execution_time": (datetime.now() - start_time).total_seconds(),
                    "workflow": workflow_plan,
                    "results": workflow_result.get("results", {}),
                    "workflow_summary": workflow_result.get("summary", ""),
                    "metadata": {
                        "workflow_type": "multi_agent",
                        "agents_used": len(workflow_plan["agents"]),
                        "execution_strategy": workflow_plan.get(
                            "execution_strategy", "sequential"
                        ),
                    },
                }

            elif workflow_plan["agents"]:
                # Single specialized agent
                agent_name = workflow_plan["agents"][0]
                print(f"Single specialized agent workflow: {agent_name}")

                result = await self._execute_specialized_agent(
                    agent_name, user_request, enriched_files
                )

                return {
                    "status": "success",
                    "workflow_id": workflow_id,
                    "response": result.get("response", ""),
                    "execution_time": (datetime.now() - start_time).total_seconds(),
                    "workflow": workflow_plan,
                    "results": {agent_name: result},
                    "metadata": {
                        "workflow_type": "single_agent_specialized",
                        "agent_used": agent_name,
                    },
                }
            else:
                # Fall back to original simple processing
                return await self._process_simple_request(
                    user_request, enriched_files, workflow_id, start_time
                )

        except Exception as e:
            print(f"Error: {str(e)}")
            import traceback

            traceback.print_exc()
            return {
                "status": "error",
                "workflow_id": workflow_id,
                "error": str(e),
                "response": f"An error occurred: {str(e)}",
                "workflow": {},
                "metadata": {},
            }

    async def _analyze_with_ai(self, request: str, files: List[Dict]) -> Dict:
        """Use GPT-4 to analyze request with ACTUAL DATA - works with ANY file type."""

        # Build context with whatever data we have
        context_parts = [f"User request: {request}"]

        if files:
            for file in files:
                if file.get("read_success"):
                    context_parts.append(
                        f"\nFile: {file['original_name']} (Type: {file['structure']})"
                    )

                    # Let GPT-4 see the actual content based on file type
                    content = file.get("content", {})

                    if file["structure"] == "tabular":
                        # CSV/Excel - show columns and sample data
                        context_parts.append(f"Columns: {content.get('columns', [])}")
                        context_parts.append(
                            f"Sample data: {content.get('first_10_rows', [])[:3]}"
                        )

                    elif file["structure"] == "text":
                        # Text/PDF/Word - show actual text
                        context_parts.append(
                            f"Text content: {content.get('text', '')[:1000]}"
                        )

                    elif file["structure"] == "json":
                        # JSON - show structure and data
                        context_parts.append(
                            f"JSON data: {json.dumps(content.get('data', {}), indent=2)[:1000]}"
                        )

                    elif file["structure"] == "yaml":
                        # YAML - show parsed data
                        context_parts.append(
                            f"YAML data: {json.dumps(content.get('data', {}), indent=2)[:1000]}"
                        )

                    else:
                        # Unknown type - show what we have
                        context_parts.append(f"Content: {str(content)[:1000]}")

        # Let GPT-4 figure out what to do with ANY data type
        prompt = f"""
        {chr(10).join(context_parts)}
        
        Available agents: {list(self.registry.agents['agents'].keys())}
        
        YOU CAN SEE THE ACTUAL DATA ABOVE. Based on what you see:
        1. What type of data is this?
        2. What does the user want to do with it?
        3. What specific processing is needed?
        4. Which agents should handle this?
        
        If it's CSV data with sales, actually look at the values and answer the question.
        If it's text, analyze the actual text content.
        If it's JSON, understand the structure and process accordingly.
        
        Be specific based on the ACTUAL DATA you can see, not generic descriptions.
        
        Return JSON with your analysis and plan.
        """

        response = self.openai_client.chat.completions.create(
            model=ORCHESTRATOR_MODEL,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )

        return json.loads(response.choices[0].message.content)

    async def _ai_plan_workflow(
        self, request: str, files: List[Dict], analysis: Dict
    ) -> Dict:
        """
        GPT-4 plans workflow with knowledge of actual data structure.
        """
        available_agents = self.registry.list_agents()
        available_tools = self.registry.list_tools()

        prompt = f"""
        Create a workflow plan based on ACTUAL data structure:
        
        REQUEST: {request}
        
        ANALYSIS: {json.dumps(analysis, indent=2)}
        
        AVAILABLE AGENTS: {[a['name'] for a in available_agents]}
        AVAILABLE TOOLS: {[t['name'] for t in available_tools]}
        
        Return JSON with:
        {{
            "agents": ["agent1", "agent2"],
            "missing_components": {{"agents": [], "tools": []}},
            "execution_strategy": "sequential",
            "data_flow": {{"step1": "description", "step2": "description"}},
            "expected_output": "description"
        }}
        
        IMPORTANT: You can see the actual data columns and structure. Plan based on what's really there.
        """

        response = self.openai_client.chat.completions.create(
            model=ORCHESTRATOR_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_completion_tokens=ORCHESTRATOR_MAX_TOKENS,
            response_format={"type": "json_object"},
        )

        plan = json.loads(response.choices[0].message.content)
        plan["ai_calls"] = 2  # Track AI usage
        return plan

    async def _create_missing_components(self, missing: Dict):
        """
        Create missing agents/tools using AI.
        """
        # Create tools first (agents depend on them)
        for tool_name in missing.get("tools", []):
            print(f"Creating tool: {tool_name}")
            self.tool_factory.ensure_tool(tool_name, f"Tool for {tool_name}")

        # Create agents
        for agent_name in missing.get("agents", []):
            print(f"Creating agent: {agent_name}")
            self.agent_factory.ensure_agent(agent_name, f"Agent for {agent_name}")

    async def _execute_ai_workflow(
        self, plan: Dict, request: str, files: List[Dict]
    ) -> Dict:
        """Execute workflow with actual data - ANY file type."""

        results = {}

        # FIXED: Handle the case when there are no files properly
        if files and files[0].get("read_success"):
            # We have actual file data
            actual_data = files[0]["content"]  # The ACTUAL content
            data_type = files[0]["structure"]
        else:
            # No files - use the request as text data
            actual_data = request
            data_type = "text"  # Treat request as text to be processed

        for agent_name in plan.get("agents", []):
            print(f"Executing Agent: {agent_name}")

            # Let Claude work with the actual data
            agent_prompt = f"""
            You are the '{agent_name}' agent.
            
            Original request: {request}
            Data type: {data_type}
            
            ACTUAL DATA TO PROCESS:
            {self._format_data_for_prompt(actual_data, data_type)}
            
            INSTRUCTIONS:
            - Work with the ACTUAL data above
            - If it's a question like "What is 2+2?", calculate and provide the answer
            - If it's CSV data, analyze the real values
            - If it's text, process the actual text
            - If it's JSON, work with the real structure
            - Provide specific answers based on what you see
            - Don't just describe what you would do - DO IT
            
            For example:
            - If asked "What is 2+2?", answer "4"
            - If asked for highest sales region, tell me which region and the value
            - If asked to extract emails, show the actual emails you found
            - If asked to summarize, provide the actual summary
            """

            response = self.claude_client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=CLAUDE_MAX_TOKENS,
                messages=[{"role": "user", "content": agent_prompt}],
            )

            results[agent_name] = response.content[0].text

        return results

    def _format_data_for_prompt(self, data: Any, data_type: str) -> str:
        """Format ANY data type for AI prompt - FIXED VERSION."""

        try:
            if data_type == "tabular":
                # CSV/Excel data
                if isinstance(data, dict):
                    output = f"Columns: {data.get('columns', [])}\n"
                    output += f"Total rows: {data.get('total_rows', 0)}\n"
                    output += (
                        f"Data:\n{json.dumps(data.get('first_10_rows', []), indent=2)}"
                    )
                    return output[:2000]
                else:
                    return f"Tabular data (non-dict): {str(data)[:2000]}"

            elif data_type == "text":
                # Text content - handle both dict and string
                if isinstance(data, dict):
                    return str(data.get("text", data))[:2000]
                else:
                    # If it's already a string, use it directly
                    return str(data)[:2000]

            elif data_type in ["json", "yaml"]:
                # Structured data
                if isinstance(data, dict):
                    return json.dumps(data.get("data", data), indent=2)[:2000]
                else:
                    return (
                        json.dumps(data, indent=2)[:2000] if data else str(data)[:2000]
                    )

            # Default - safely convert to string
            return str(data)[:2000]

        except Exception as e:
            print(f"DEBUG: Error formatting data: {e}")
            return f"Data formatting error: {str(data)[:500]}"

    async def _ai_synthesize_response(
        self, request: str, plan: Dict, results: Dict
    ) -> str:
        """
        GPT-4 creates final user-friendly response.
        FIXED: Handle string results from Claude agents properly.
        """

        # FIXED: Handle both string and dict results properly
        formatted_results = {}
        for k, v in results.items():
            if isinstance(v, dict):
                # If result is a dict, try to get 'output' or use the whole dict
                formatted_results[k] = str(v.get("output", v))[:500]
            elif isinstance(v, str):
                # If result is a string (which it is from Claude), use it directly
                formatted_results[k] = v[:500]
            else:
                # For any other type, convert to string
                formatted_results[k] = str(v)[:500]

        prompt = f"""
        Create a natural response for the user:
        
        ORIGINAL REQUEST: {request}
        
        WORKFLOW EXECUTED: {plan.get('agents', [])}
        
        RESULTS: {json.dumps(formatted_results, indent=2)}
        
        Synthesize a clear, helpful response that directly answers the user's request.
        Include specific details from the results.
        Be conversational and helpful.
        """

        response = self.openai_client.chat.completions.create(
            model=ORCHESTRATOR_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_completion_tokens=ORCHESTRATOR_MAX_TOKENS,
        )

        return response.choices[0].message.content

    # async def _execute_specialized_agent(
    #     self, agent_name: str, request: str, files: List[Dict]
    # ) -> Dict:
    #     """Execute a specialized agent directly."""

    #     # Get the specialized agent
    #     agent = self.workflow_engine.agents.get(agent_name)
    #     if not agent:
    #         return {"status": "error", "error": f"Agent {agent_name} not found"}

    #     # Execute with file data
    #     file_data = files[0] if files and files[0].get("read_success") else None
    #     result = await agent.execute(request, file_data)

    #     # Generate response
    #     if result.get("status") == "success":
    #         data = result.get("data", {})
    #         response_parts = []

    #         if agent_name == "pdf_analyzer":
    #             response_parts.append("PDF Analysis Complete:")
    #             if data.get("summary"):
    #                 response_parts.append(f"Summary: {data['summary']}")
    #             if data.get("key_points"):
    #                 response_parts.append(
    #                     f"Key Points: {', '.join(data['key_points'][:3])}"
    #                 )

    #         elif agent_name == "text_processor":
    #             response_parts.append("Text Processing Complete:")
    #             if data.get("processed_text"):
    #                 response_parts.append(f"Result: {data['processed_text'][:200]}...")
    #             if data.get("sentiment"):
    #                 response_parts.append(f"Sentiment: {data['sentiment']}")

    #         elif agent_name == "chart_generator":
    #             response_parts.append("Chart Generation Complete:")
    #             if data.get("chart_type"):
    #                 response_parts.append(f"Generated {data['chart_type']} chart")

    #         response = (
    #             " | ".join(response_parts)
    #             if response_parts
    #             else "Processing completed successfully."
    #         )
    #     else:
    #         response = f"Processing failed: {result.get('error', 'Unknown error')}"

    #     return {"response": response, **result}

    async def _execute_specialized_agent(
        self, agent_name: str, request: str, files: List[Dict]
    ) -> Dict:
        """Execute a specialized agent directly - FIXED VERSION."""

        # Get the specialized agent
        agent = self.workflow_engine.agents.get(agent_name)
        if not agent:
            return {"status": "error", "error": f"Agent {agent_name} not found"}

        # Prepare file data
        file_data = files[0] if files and files[0].get("read_success") else None

        # FIXED: Check if this is a new specialized agent or old IntelligentAgent
        if hasattr(agent, "execute") and agent_name in [
            "pdf_analyzer",
            "text_processor",
            "chart_generator",
        ]:
            # New specialized agents - use keyword arguments
            result = await agent.execute(
                request=request, file_data=file_data, context=None
            )
        else:
            # Old IntelligentAgent - use state format
            state = {
                "current_data": file_data,
                "request": request,
                "results": {},
                "errors": [],
                "execution_path": [],
            }
            result = await agent.execute(state)

        # Generate response (rest stays the same)
        if result.get("status") == "success":
            data = result.get("data", {})
            response_parts = []

            if agent_name == "pdf_analyzer":
                response_parts.append("PDF Analysis Complete:")
                if data.get("summary"):
                    response_parts.append(f"Summary: {data['summary']}")
                if data.get("key_points"):
                    response_parts.append(
                        f"Key Points: {', '.join(data['key_points'][:3])}"
                    )

            elif agent_name == "text_processor":
                response_parts.append("Text Processing Complete:")
                if data.get("processed_text"):
                    response_parts.append(f"Result: {data['processed_text'][:200]}...")
                if data.get("sentiment"):
                    response_parts.append(f"Sentiment: {data['sentiment']}")

            elif agent_name == "chart_generator":
                response_parts.append("Chart Generation Complete:")
                if data.get("chart_type"):
                    response_parts.append(f"Generated {data['chart_type']} chart")

            elif agent_name == "data_analyzer":
                response_parts.append("Data Analysis Complete:")
                if isinstance(data, dict) and data.get("processed_data"):
                    response_parts.append(
                        f"Analysis: {str(data['processed_data'])[:100]}..."
                    )

            response = (
                " | ".join(response_parts)
                if response_parts
                else "Processing completed successfully."
            )
        else:
            response = f"Processing failed: {result.get('error', 'Unknown error')}"

        return {"response": response, **result}

    async def _process_simple_request(
        self,
        user_request: str,
        enriched_files: List[Dict],
        workflow_id: str,
        start_time,
    ) -> Dict:
        """Process simple requests using the original logic."""

        # Use original logic for simple cases
        analysis = await self._analyze_with_ai(user_request, enriched_files)
        plan = await self._ai_plan_workflow(user_request, enriched_files, analysis)
        results = await self._execute_ai_workflow(plan, user_request, enriched_files)
        response = await self._ai_synthesize_response(user_request, plan, results)

        return {
            "status": "success",
            "workflow_id": workflow_id,
            "response": response,
            "execution_time": (datetime.now() - start_time).total_seconds(),
            "workflow": plan,
            "results": results,
            "metadata": {
                "workflow_type": "simple",
                "files_processed": len(enriched_files),
                "agents_used": len(plan.get("agents", [])),
            },
        }

    async def _synthesize_workflow_response(
        self, request: str, workflow_result: Dict
    ) -> str:
        """Synthesize final response from multi-agent workflow results - FIXED VERSION."""

        if workflow_result.get("status") == "error":
            return f"Workflow failed: {workflow_result.get('error', 'Unknown error')}"

        results = workflow_result.get("results", {})
        workflow_summary = workflow_result.get("summary", "")

        # Build comprehensive response
        response_parts = ["Multi-agent workflow completed successfully."]

        if workflow_summary:
            response_parts.append(workflow_summary)

        # FIXED: Add specific results from each agent with proper type checking
        for agent_name, result in results.items():
            if isinstance(result, dict) and result.get("status") == "success":
                data = result.get("data", {})

                if agent_name == "pdf_analyzer":
                    if isinstance(data, dict) and data.get("specific_answer"):
                        response_parts.append(
                            f"📄 PDF Analysis: {data['specific_answer']}"
                        )
                    elif isinstance(data, dict) and data.get("summary"):
                        response_parts.append(
                            f"📄 PDF Analysis: {data['summary'][:100]}..."
                        )

                elif agent_name == "text_processor":
                    if isinstance(data, dict) and data.get("processed_text"):
                        response_parts.append(
                            f"📝 Text Processing: {data['processed_text'][:150]}..."
                        )
                    elif isinstance(data, str):
                        response_parts.append(f"📝 Text Processing: {data[:150]}...")

                elif agent_name == "chart_generator":
                    response_parts.append("📊 Chart generated successfully")
                    if isinstance(data, dict) and data.get("chart_type"):
                        response_parts.append(f"Chart type: {data['chart_type']}")

                elif agent_name == "data_analyzer":
                    response_parts.append("📈 Data analysis completed with insights")
                    if isinstance(data, dict) and data.get("analysis"):
                        response_parts.append(f"Key findings available")

            elif isinstance(result, str):
                # Handle cases where result is a string directly
                response_parts.append(f"• {agent_name}: {result[:100]}...")

        return (
            " | ".join(response_parts) if len(response_parts) > 1 else response_parts[0]
        )

```

--------------------------------------------------------------------------------

### File: core/specialized_agents.py
**Path:** `core/specialized_agents.py`
**Size:** 15,567 bytes
**Modified:** 2025-09-14 09:02:21

```python
"""
PDF Analyzer Agent - Intelligent PDF processing with Claude reasoning
Location: core/specialized_agents.py
"""

import os
import json
import PyPDF2
import pdfplumber
from typing import Dict, Any, List
from anthropic import Anthropic
from config import CLAUDE_MODEL, CLAUDE_MAX_TOKENS, ANTHROPIC_API_KEY


class PDFAnalyzerAgent:
    """Intelligent PDF analysis agent powered by Claude."""

    def __init__(self):
        self.name = "pdf_analyzer"
        self.description = (
            "Analyzes PDF documents with intelligent text extraction and reasoning"
        )
        self.claude = Anthropic(api_key=ANTHROPIC_API_KEY)

    async def execute(
        self, request: str, file_data: Dict = None, context: Dict = None
    ) -> Dict:
        """Execute PDF analysis with Claude reasoning."""

        try:
            # Step 1: Extract PDF content intelligently
            if file_data and file_data.get("structure") == "pdf":
                pdf_content = file_data.get("content", {})
                text_content = pdf_content.get("first_pages_text", [])
                full_text = "\n".join(text_content)

                # If text is empty, try alternative extraction
                if not full_text.strip():
                    file_path = file_data.get("path")
                    if file_path and os.path.exists(file_path):
                        full_text = await self._extract_text_advanced(file_path)

            else:
                return {
                    "status": "error",
                    "error": "No PDF data provided",
                    "data": None,
                }

            # Step 2: Claude analyzes the extracted content
            analysis = await self._analyze_with_claude(request, full_text, context)

            # Step 3: Structure the response
            return {
                "status": "success",
                "data": {
                    "analysis": analysis,
                    "text_extracted": len(full_text),
                    "pages_processed": len(text_content),
                    "summary": analysis.get("summary", ""),
                    "key_points": analysis.get("key_points", []),
                    "insights": analysis.get("insights", []),
                },
                "metadata": {
                    "agent": self.name,
                    "processing_type": "pdf_analysis",
                    "claude_model": CLAUDE_MODEL,
                },
            }

        except Exception as e:
            return {"status": "error", "error": str(e), "data": None}

    async def _extract_text_advanced(self, pdf_path: str) -> str:
        """Advanced PDF text extraction using pdfplumber."""
        try:
            text_parts = []
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages[:10]:  # First 10 pages
                    text = page.extract_text()
                    if text:
                        text_parts.append(text)
            return "\n".join(text_parts)
        except Exception as e:
            print(f"PDF extraction error: {e}")
            return ""

    async def _analyze_with_claude(
        self, request: str, pdf_text: str, context: Dict = None
    ) -> Dict:
        """Use Claude to intelligently analyze PDF content."""

        prompt = f"""
        You are an intelligent PDF analyzer. The user wants: "{request}"
        
        PDF Content (first {len(pdf_text)} characters):
        {pdf_text[:4000]}
        
        Context: {json.dumps(context, indent=2) if context else "None"}
        
        Based on the PDF content above, provide a comprehensive analysis that addresses the user's request:
        
        1. **Summary**: Key overview of the document
        2. **Key Points**: Important findings or information points
        3. **Insights**: Analytical insights based on the content
        4. **Specific Answer**: Direct response to the user's question
        5. **Recommendations**: Actionable recommendations if applicable
        
        If the user asks for specific information (like dates, names, financial figures), extract and highlight those precisely.
        
        Respond in JSON format:
        {{
            "summary": "comprehensive summary",
            "key_points": ["point 1", "point 2", "point 3"],
            "insights": ["insight 1", "insight 2"],
            "specific_answer": "direct answer to user request",
            "recommendations": ["recommendation 1", "recommendation 2"],
            "extracted_data": {{
                "dates": ["any dates found"],
                "names": ["any names found"], 
                "financial_figures": ["any money amounts found"],
                "other_important_data": ["other relevant data"]
            }}
        }}
        """

        response = self.claude.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=CLAUDE_MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}],
        )

        try:
            return json.loads(response.content[0].text)
        except json.JSONDecodeError:
            return {
                "summary": response.content[0].text,
                "key_points": [],
                "insights": [],
                "specific_answer": response.content[0].text,
            }


class ChartGeneratorAgent:
    """Intelligent chart generation agent powered by Claude."""

    def __init__(self):
        self.name = "chart_generator"
        self.description = (
            "Generates charts and visualizations from data using intelligent analysis"
        )
        self.claude = Anthropic(api_key=ANTHROPIC_API_KEY)

    async def execute(
        self, request: str, file_data: Dict = None, context: Dict = None
    ) -> Dict:
        """Execute chart generation with Claude reasoning."""

        try:
            # Step 1: Analyze data for visualization
            data_analysis = await self._analyze_data_for_charts(
                request, file_data, context
            )

            # Step 2: Generate chart code with Claude
            chart_code = await self._generate_chart_code(request, data_analysis)

            # Step 3: Execute chart generation
            chart_result = await self._execute_chart_generation(chart_code, file_data)

            return {
                "status": "success",
                "data": {
                    "chart_type": chart_result.get("chart_type"),
                    "chart_path": chart_result.get("chart_path"),
                    "chart_data": chart_result.get("chart_data"),
                    "analysis": data_analysis,
                    "recommendations": chart_result.get("recommendations", []),
                },
                "metadata": {
                    "agent": self.name,
                    "processing_type": "chart_generation",
                    "claude_model": CLAUDE_MODEL,
                },
            }

        except Exception as e:
            return {"status": "error", "error": str(e), "data": None}

    async def _analyze_data_for_charts(
        self, request: str, file_data: Dict, context: Dict
    ) -> Dict:
        """Claude analyzes data to determine best chart type."""

        # Extract data description
        if file_data and file_data.get("structure") == "tabular":
            data_desc = f"Columns: {file_data['content'].get('columns', [])}\n"
            data_desc += (
                f"Sample data: {file_data['content'].get('first_10_rows', [])[:3]}"
            )
        else:
            data_desc = str(file_data)[:1000] if file_data else "No data provided"

        prompt = f"""
        Analyze this data for chart generation:
        
        User Request: {request}
        Data: {data_desc}
        Context: {context}
        
        Determine:
        1. Best chart type (bar, line, pie, scatter, histogram, etc.)
        2. X and Y axis data
        3. Grouping/categorization needed
        4. Chart title and labels
        5. Color scheme recommendations
        
        Respond in JSON:
        {{
            "recommended_chart_type": "bar|line|pie|scatter|histogram|other",
            "x_axis": "column name or data source",
            "y_axis": "column name or data source", 
            "grouping": "grouping column if needed",
            "title": "suggested chart title",
            "x_label": "X axis label",
            "y_label": "Y axis label",
            "color_scheme": "recommended colors",
            "insights": ["what the chart should show"]
        }}
        """

        response = self.claude.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}],
        )

        try:
            return json.loads(response.content[0].text)
        except:
            return {"recommended_chart_type": "bar", "title": "Data Visualization"}

    async def _generate_chart_code(self, request: str, analysis: Dict) -> str:
        """Claude generates matplotlib/seaborn code for the chart."""

        prompt = f"""
        Generate Python code to create a chart based on this analysis:
        
        Request: {request}
        Analysis: {json.dumps(analysis, indent=2)}
        
        Generate complete Python code using matplotlib/seaborn that:
        1. Creates the recommended chart type
        2. Handles the data properly
        3. Adds appropriate labels and title
        4. Saves the chart as a PNG file
        5. Returns the chart data and path
        
        Use this template structure:
        
        ```python
        import matplotlib.pyplot as plt
        import seaborn as sns
        import pandas as pd
        import os
        
        def generate_chart(data):
            # Your chart generation code here
            # Return dict with chart_path, chart_type, etc.
            pass
        ```
        
        Respond with ONLY the Python code, no explanations.
        """

        response = self.claude.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}],
        )

        return response.content[0].text

    async def _execute_chart_generation(self, chart_code: str, file_data: Dict) -> Dict:
        """Execute the generated chart code."""
        try:
            # Extract data for chart
            if file_data and file_data.get("structure") == "tabular":
                import pandas as pd

                data = pd.DataFrame(file_data["content"].get("first_10_rows", []))
            else:
                data = None

            # Execute chart code (simplified for POC)
            return {
                "chart_type": "bar",
                "chart_path": "generated_chart.png",
                "chart_data": "Chart generated successfully",
                "recommendations": ["Chart shows data trends clearly"],
            }

        except Exception as e:
            return {"error": str(e)}


class TextProcessorAgent:
    """Intelligent text processing agent powered by Claude."""

    def __init__(self):
        self.name = "text_processor"
        self.description = "Processes and analyzes text with advanced NLP capabilities"
        self.claude = Anthropic(api_key=ANTHROPIC_API_KEY)

    async def execute(
        self, request: str, file_data: Dict = None, context: Dict = None
    ) -> Dict:
        """Execute text processing with Claude reasoning."""

        try:
            # Step 1: Extract text content
            if file_data:
                if file_data.get("structure") == "text":
                    text_content = file_data["content"].get("text", "")
                elif file_data.get("structure") == "pdf":
                    text_content = "\n".join(
                        file_data["content"].get("first_pages_text", [])
                    )
                else:
                    text_content = str(file_data.get("content", ""))
            else:
                # Extract text from the request itself
                text_content = request

            # Step 2: Claude processes the text
            processing_result = await self._process_with_claude(
                request, text_content, context
            )

            # Step 3: Structure response
            return {
                "status": "success",
                "data": {
                    "processed_text": processing_result.get("processed_result"),
                    "analysis": processing_result.get("analysis", {}),
                    "extracted_entities": processing_result.get("entities", []),
                    "sentiment": processing_result.get("sentiment", "neutral"),
                    "key_phrases": processing_result.get("key_phrases", []),
                    "summary": processing_result.get("summary", ""),
                },
                "metadata": {
                    "agent": self.name,
                    "text_length": len(text_content),
                    "processing_type": "text_analysis",
                    "claude_model": CLAUDE_MODEL,
                },
            }

        except Exception as e:
            return {"status": "error", "error": str(e), "data": None}

    async def _process_with_claude(
        self, request: str, text_content: str, context: Dict
    ) -> Dict:
        """Use Claude for intelligent text processing."""

        prompt = f"""
        You are an intelligent text processor. The user wants: "{request}"
        
        Text to process:
        {text_content[:3000]}
        
        Context: {json.dumps(context, indent=2) if context else "None"}
        
        Based on the request, perform the appropriate text processing:
        
        If the request involves:
        - **Extraction**: Extract emails, phone numbers, names, dates, etc.
        - **Analysis**: Analyze sentiment, themes, topics, etc.
        - **Transformation**: Summarize, rewrite, format, etc.
        - **Classification**: Categorize or classify the text
        - **Comparison**: Compare with other text or criteria
        
        Provide comprehensive results in JSON format:
        {{
            "processed_result": "main result addressing the user's request",
            "analysis": {{
                "text_type": "email|article|document|social_media|other",
                "main_topics": ["topic1", "topic2"],
                "complexity": "simple|medium|complex",
                "tone": "formal|informal|neutral"
            }},
            "entities": {{
                "emails": ["extracted emails"],
                "phones": ["extracted phone numbers"],
                "names": ["extracted names"],
                "dates": ["extracted dates"],
                "locations": ["extracted locations"]
            }},
            "sentiment": "positive|negative|neutral",
            "key_phrases": ["important phrase 1", "important phrase 2"],
            "summary": "brief summary of the text",
            "insights": ["insight 1", "insight 2"]
        }}
        """

        response = self.claude.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=CLAUDE_MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}],
        )

        try:
            return json.loads(response.content[0].text)
        except json.JSONDecodeError:
            return {
                "processed_result": response.content[0].text,
                "analysis": {},
                "entities": [],
                "sentiment": "neutral",
            }

```

--------------------------------------------------------------------------------

### File: core/tool_factory.py
**Path:** `core/tool_factory.py`
**Size:** 50,873 bytes
**Modified:** 2025-09-10 21:56:33

```python
"""
Tool Factory
Dynamically generates pure function tools using Claude API
"""

import os
import sys
import ast
import json
import traceback
from typing import Dict, List, Optional, Any
from anthropic import Anthropic

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    ANTHROPIC_API_KEY,
    CLAUDE_MODEL,
    CLAUDE_TEMPERATURE,
    CLAUDE_MAX_TOKENS,
    CLAUDE_TOOL_GENERATION_PROMPT,
    MIN_TOOL_LINES,
    MAX_TOOL_LINES,
    TOOL_VALIDATION_RULES,
    ALLOWED_IMPORTS,
    GENERATED_TOOLS_DIR,
    PREBUILT_TOOLS_DIR,
)
from core.registry import RegistryManager
from core.registry_singleton import get_shared_registry


class ToolFactory:
    """
    Factory for creating pure function tools using Claude.
    Ensures all tools are stateless and handle inputs gracefully.
    """

    def __init__(self):
        """Initialize the tool factory."""
        self.client = Anthropic(api_key=ANTHROPIC_API_KEY)
        self.registry = get_shared_registry()
        self.generation_history = []

    def create_tool(
        self,
        tool_name: str,
        description: str,
        input_description: str,
        output_description: str,
        examples: Optional[List[Dict[str, Any]]] = None,
        default_return: Any = None,
        is_prebuilt: bool = False,
        is_pure_function: bool = True,
        tags: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Create a new tool using Claude.

        Args:
            tool_name: Unique identifier for the tool
            description: Clear description of tool's purpose
            input_description: Expected input format/type
            output_description: Expected output format/type
            examples: Optional input/output examples
            default_return: Default value to return on error
            is_prebuilt: Whether this is a prebuilt tool
            is_pure_function: Whether tool has no side effects
            tags: Optional categorization tags

        Returns:
            Result dictionary with status and details
        """

        print(f"DEBUG: Creating tool '{tool_name}'")

        # Validate tool name
        if not self._validate_tool_name(tool_name):
            return {
                "status": "error",
                "message": f"Invalid tool name: {tool_name}. Use lowercase with underscores only.",
            }

        # Check if tool already exists
        if self.registry.tool_exists(tool_name):
            print(f"DEBUG: Tool '{tool_name}' already exists")
            return {
                "status": "exists",
                "message": f"Tool '{tool_name}' already exists and is active",
                "tool": self.registry.get_tool(tool_name),
            }

        # Determine default return value
        if default_return is None:
            default_return = self._infer_default_return(output_description)

        # Generate the tool code
        generation_result = self._generate_tool_code(
            tool_name=tool_name,
            description=description,
            input_description=input_description,
            output_description=output_description,
            examples=examples,
            default_return=default_return,
        )

        if generation_result["status"] != "success":
            return generation_result

        code = generation_result["code"]

        # Validate the generated code
        validation_result = self._validate_tool_code(
            code=code, tool_name=tool_name, is_pure_function=is_pure_function
        )

        if not validation_result["valid"]:
            # Try to fix common issues
            fixed_code = self._attempt_code_fixes(code, validation_result["issues"])
            if fixed_code:
                code = fixed_code
                validation_result = self._validate_tool_code(
                    code, tool_name, is_pure_function
                )

                if not validation_result["valid"]:
                    return {
                        "status": "validation_error",
                        "message": "Generated code failed validation after fixes",
                        "validation_errors": validation_result["issues"],
                        "code": code,
                    }
            else:
                return {
                    "status": "validation_error",
                    "message": "Generated code failed validation",
                    "validation_errors": validation_result["issues"],
                    "code": code,
                }

        # Extract function signature
        signature = self._extract_signature(code)

        # Register the tool
        registration_result = self.registry.register_tool(
            name=tool_name,
            description=description,
            code=code,
            signature=signature,
            tags=tags or self._extract_tags_from_description(description),
            is_prebuilt=is_prebuilt,
            is_pure_function=is_pure_function,
        )

        if registration_result["status"] != "success":
            return registration_result

        # Force all components to reload registry after successful creation
        from core.registry_singleton import RegistrySingleton

        RegistrySingleton().force_reload()
        print(f"DEBUG: Forced registry reload after creating '{tool_name}'")

        # Record generation history
        self.generation_history.append(
            {
                "tool_name": tool_name,
                "timestamp": registration_result.get("created_at"),
                "line_count": len(code.splitlines()),
                "is_pure": is_pure_function,
            }
        )

        # Test the tool with examples if provided
        if examples:
            test_results = self._test_tool_with_examples(tool_name, examples)
            registration_result["test_results"] = test_results

        return {
            "status": "success",
            "message": f"Tool '{tool_name}' created successfully",
            "tool_name": tool_name,
            "location": registration_result["location"],
            "line_count": registration_result["line_count"],
            "signature": signature,
            "code": code,
        }

    def _generate_tool_code(
        self,
        tool_name: str,
        description: str,
        input_description: str,
        output_description: str,
        examples: Optional[List[Dict[str, Any]]],
        default_return: Any,
    ) -> Dict[str, Any]:
        """Generate tool code using Claude."""
        # Determine imports needed
        imports = self._determine_imports(
            description, input_description, output_description
        )

        # Build tool logic hints
        tool_logic = self._build_tool_logic_hints(description, examples)

        # Format the prompt
        prompt = CLAUDE_TOOL_GENERATION_PROMPT.format(
            tool_name=tool_name,
            description=description,
            input_description=input_description,
            output_description=output_description,
            imports="\n    ".join(imports),
            tool_logic=tool_logic,
            default_return=repr(default_return),
            min_lines=MIN_TOOL_LINES,
            max_lines=MAX_TOOL_LINES,
        )

        # Add examples to prompt if provided
        if examples:
            examples_text = "\n\nExamples:\n"
            for i, example in enumerate(examples, 1):
                examples_text += f"Input: {example.get('input')}\n"
                examples_text += f"Expected Output: {example.get('output')}\n\n"
            prompt += examples_text

        try:
            # Call Claude API
            response = self.client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=CLAUDE_MAX_TOKENS,
                messages=[{"role": "user", "content": prompt}],
            )

            # Extract code from response
            code = self._extract_code_from_response(response.content[0].text)

            if not code:
                return {
                    "status": "error",
                    "message": "No valid Python code found in Claude response",
                }

            return {"status": "success", "code": code}

        except Exception as e:
            return {
                "status": "error",
                "message": f"Claude API error: {str(e)}",
                "traceback": traceback.format_exc(),
            }

    def _validate_tool_code(
        self, code: str, tool_name: str, is_pure_function: bool = True
    ) -> Dict[str, Any]:
        """
        Comprehensive validation of tool code.

        Args:
            code: Python code to validate
            tool_name: Expected tool name
            is_pure_function: Whether tool should be pure

        Returns:
            Validation result with issues if any
        """
        issues = []

        # Check syntax
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return {"valid": False, "issues": [f"Syntax error: {str(e)}"]}

        # Check structure
        if not tree.body or not isinstance(tree.body[0], ast.FunctionDef):
            issues.append("Code must define a function")
            return {"valid": False, "issues": issues}

        func_def = tree.body[0]

        # Check function name
        if func_def.name != tool_name:
            issues.append(f"Function name must be: {tool_name}")

        # Check function has parameter
        if len(func_def.args.args) == 0:
            issues.append("Function must accept at least one parameter")

        # Check for default parameter handling
        first_param = func_def.args.args[0].arg if func_def.args.args else None
        if first_param and f"if {first_param} is None:" not in code:
            issues.append("Function must handle None input")

        # Check required patterns
        for pattern in TOOL_VALIDATION_RULES["required_patterns"]:
            if pattern and pattern not in code:
                issues.append(f"Missing required pattern: {pattern}")

        # Check forbidden patterns for pure functions
        if is_pure_function:
            forbidden = TOOL_VALIDATION_RULES["forbidden_patterns"]
            for pattern in forbidden:
                if pattern and pattern in code:
                    # Special handling for conditional patterns
                    if 'if "connector"' in pattern:
                        # Skip this check for connectors
                        continue
                    issues.append(f"Forbidden pattern for pure function: {pattern}")

        # Check imports
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module = alias.name.split(".")[0]
                    if module not in ALLOWED_IMPORTS:
                        issues.append(f"Forbidden import: {alias.name}")
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    module = node.module.split(".")[0]
                    if module not in ALLOWED_IMPORTS:
                        issues.append(f"Forbidden import from: {node.module}")

        # Check line count
        line_count = len(code.splitlines())
        if line_count < MIN_TOOL_LINES:
            issues.append(f"Code too short: {line_count} lines (min: {MIN_TOOL_LINES})")
        elif line_count > MAX_TOOL_LINES:
            issues.append(f"Code too long: {line_count} lines (max: {MAX_TOOL_LINES})")

        # Check for return statement
        has_return = any(isinstance(node, ast.Return) for node in ast.walk(func_def))
        if not has_return:
            issues.append("Function must have return statement")

        # Check for exception handling
        has_try = any(isinstance(node, ast.Try) for node in ast.walk(func_def))
        if not has_try:
            issues.append("Function must have try-except block for error handling")

        # Check no exceptions are raised
        for node in ast.walk(func_def):
            if isinstance(node, ast.Raise):
                issues.append("Function must not raise exceptions")

        return {"valid": len(issues) == 0, "issues": issues}

    def _attempt_code_fixes(self, code: str, issues: List[str]) -> Optional[str]:
        """
        Attempt to fix common code issues.

        Args:
            code: Code with issues
            issues: List of validation issues

        Returns:
            Fixed code if possible, None otherwise
        """
        fixed_code = code

        # Fix missing None handling
        if any("None input" in issue for issue in issues):
            lines = fixed_code.splitlines()
            for i, line in enumerate(lines):
                if line.strip().startswith("def ") and i + 1 < len(lines):
                    # Find first line after docstring
                    insert_index = i + 1
                    # Skip docstring if present
                    if i + 1 < len(lines) and (
                        lines[i + 1].strip().startswith('"""')
                        or lines[i + 1].strip().startswith("'''")
                    ):
                        for j in range(i + 2, len(lines)):
                            if lines[j].strip().endswith('"""') or lines[
                                j
                            ].strip().endswith("'''"):
                                insert_index = j + 1
                                break

                    # Insert None check
                    param_name = "input_data"  # Default assumption
                    if "(" in line and ")" in line:
                        params = line[line.find("(") + 1 : line.find(")")].strip()
                        if params and "=" in params:
                            param_name = params.split("=")[0].strip()
                        elif params:
                            param_name = params.split(",")[0].strip()

                    none_check = f"""    if {param_name} is None:
        return None
    """
                    lines.insert(insert_index, none_check)
                    fixed_code = "\n".join(lines)
                    break

        # Fix missing try-except
        if any("try-except" in issue for issue in issues):
            if "try:" not in fixed_code:
                lines = fixed_code.splitlines()
                # Wrap main logic in try-except
                indent_level = 4  # Assuming standard function indentation
                wrapped_lines = []
                in_function = False
                function_start = 0

                for i, line in enumerate(lines):
                    if line.strip().startswith("def "):
                        in_function = True
                        function_start = i
                        wrapped_lines.append(line)
                    elif (
                        in_function
                        and i > function_start
                        and line.strip()
                        and not line.strip().startswith("#")
                    ):
                        # Start wrapping from here
                        wrapped_lines.append("    try:")
                        for j in range(i, len(lines)):
                            wrapped_lines.append("    " + lines[j])
                        wrapped_lines.append("    except Exception:")
                        wrapped_lines.append("        return None")
                        break
                    else:
                        wrapped_lines.append(line)

                fixed_code = "\n".join(wrapped_lines)

        return fixed_code if fixed_code != code else None

    def _extract_code_from_response(self, response: str) -> Optional[str]:
        """Extract Python code from Claude's response."""
        # Handle markdown code blocks
        if "```python" in response:
            start = response.find("```python") + 9
            end = response.find("```", start)
            if end > start:
                return response[start:end].strip()

        # Handle generic code blocks
        if "```" in response:
            start = response.find("```") + 3
            # Skip language identifier if present
            if response[start : start + 10].strip().startswith(("python", "py")):
                start = response.find("\n", start) + 1
            end = response.find("```", start)
            if end > start:
                code = response[start:end].strip()
                if code.startswith("def "):
                    return code

        # Try to find function definition directly
        if "def " in response:
            start = response.find("def ")
            # Find the end of the function
            lines = response[start:].split("\n")
            function_lines = []
            indent_level = None

            for line in lines:
                if line.strip().startswith("def "):
                    function_lines.append(line)
                    indent_level = len(line) - len(line.lstrip())
                elif indent_level is not None:
                    current_indent = len(line) - len(line.lstrip())
                    if (
                        line.strip()
                        and current_indent <= indent_level
                        and not line.strip().startswith("#")
                    ):
                        break
                    function_lines.append(line)

            return "\n".join(function_lines).strip()

        return None

    def _extract_signature(self, code: str) -> str:
        """Extract function signature from code."""
        for line in code.split("\n"):
            if line.strip().startswith("def "):
                return line.strip().rstrip(":")
        return "def unknown()"

    def _infer_default_return(self, output_description: str) -> Any:
        """Infer appropriate default return value from output description."""
        output_lower = output_description.lower()

        if "list" in output_lower or "array" in output_lower:
            return []
        elif (
            "dict" in output_lower or "object" in output_lower or "json" in output_lower
        ):
            return {}
        elif (
            "string" in output_lower or "text" in output_lower or "str" in output_lower
        ):
            return ""
        elif (
            "number" in output_lower or "int" in output_lower or "float" in output_lower
        ):
            return 0
        elif "bool" in output_lower or "boolean" in output_lower:
            return False
        elif "none" in output_lower or "null" in output_lower:
            return None
        else:
            return None

    def _determine_imports(
        self, description: str, input_desc: str, output_desc: str
    ) -> List[str]:
        """Determine likely imports needed based on descriptions."""
        imports = []
        all_text = f"{description} {input_desc} {output_desc}".lower()

        if "regex" in all_text or "pattern" in all_text or "extract" in all_text:
            imports.append("import re")
        if "json" in all_text:
            imports.append("import json")
        if "date" in all_text or "time" in all_text:
            imports.append("from datetime import datetime")
        if "math" in all_text or "calculate" in all_text or "statistics" in all_text:
            imports.append("import math")
        if "random" in all_text:
            imports.append("import random")
        if "url" in all_text or "parse" in all_text:
            imports.append("from urllib.parse import urlparse")

        return imports if imports else ["# No specific imports needed"]

    def _build_tool_logic_hints(
        self, description: str, examples: Optional[List[Dict]]
    ) -> str:
        """Build hints for tool logic based on description and examples."""
        hints = []
        desc_lower = description.lower()

        if "extract" in desc_lower:
            hints.append("# Extract relevant data from input")
            hints.append("# Use pattern matching or parsing")
        elif "calculate" in desc_lower or "compute" in desc_lower:
            hints.append("# Perform calculations on input data")
            hints.append("# Handle numeric operations safely")
        elif "validate" in desc_lower or "check" in desc_lower:
            hints.append("# Validate input against criteria")
            hints.append("# Return validation result")
        elif "convert" in desc_lower or "transform" in desc_lower:
            hints.append("# Transform input to desired format")
            hints.append("# Handle type conversions safely")
        elif "filter" in desc_lower or "select" in desc_lower:
            hints.append("# Filter data based on criteria")
            hints.append("# Return filtered results")
        else:
            hints.append("# Process input data")
            hints.append("# Return processed result")

        if examples:
            hints.append("# Match example input/output patterns")

        return "\n        ".join(hints)

    def _extract_tags_from_description(self, description: str) -> List[str]:
        """Extract relevant tags from description."""
        tags = []
        keywords = {
            "extract": "extraction",
            "calculate": "calculation",
            "validate": "validation",
            "convert": "conversion",
            "parse": "parsing",
            "filter": "filtering",
            "transform": "transformation",
            "analyze": "analysis",
            "process": "processing",
            "format": "formatting",
        }

        desc_lower = description.lower()
        for keyword, tag in keywords.items():
            if keyword in desc_lower:
                tags.append(tag)

        return tags[:5]  # Limit to 5 tags

    def _validate_tool_name(self, name: str) -> bool:
        """Validate tool name format."""
        import re

        # Allow lowercase letters, numbers, and underscores
        pattern = r"^[a-z][a-z0-9_]*$"
        return bool(re.match(pattern, name))

    def _test_tool_with_examples(
        self, tool_name: str, examples: List[Dict]
    ) -> List[Dict]:
        """
        Test generated tool with provided examples.

        Args:
            tool_name: Name of tool to test
            examples: List of input/output examples

        Returns:
            List of test results
        """
        results = []
        tool_info = self.registry.get_tool(tool_name)

        if not tool_info:
            return [{"status": "error", "message": "Tool not found in registry"}]

        # Import the tool dynamically
        try:
            import importlib.util

            spec = importlib.util.spec_from_file_location(
                tool_name, tool_info["location"]
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            tool_func = getattr(module, tool_name)
        except Exception as e:
            return [{"status": "error", "message": f"Failed to import tool: {str(e)}"}]

        # Test each example
        for i, example in enumerate(examples):
            try:
                input_data = example.get("input")
                expected_output = example.get("output")
                actual_output = tool_func(input_data)

                # Check if output matches
                if actual_output == expected_output:
                    results.append(
                        {
                            "example": i + 1,
                            "status": "passed",
                            "input": input_data,
                            "output": actual_output,
                        }
                    )
                else:
                    results.append(
                        {
                            "example": i + 1,
                            "status": "failed",
                            "input": input_data,
                            "expected": expected_output,
                            "actual": actual_output,
                        }
                    )
            except Exception as e:
                results.append(
                    {
                        "example": i + 1,
                        "status": "error",
                        "input": input_data,
                        "error": str(e),
                    }
                )

        return results

    def get_generation_history(self) -> List[Dict[str, Any]]:
        """Get history of generated tools."""
        return self.generation_history.copy()

    def create_connector_tool(
        self,
        tool_name: str,
        service: str,
        operations: List[str],
        auth_type: str = "api_key",
    ) -> Dict[str, Any]:
        """
        Create a connector tool for external services.

        Args:
            tool_name: Name for the connector tool
            service: Service to connect to (e.g., 'jira')
            operations: List of operations to support
            auth_type: Authentication type required

        Returns:
            Result of connector creation
        """
        # Special handling for connector tools
        description = (
            f'Connector for {service} with operations: {", ".join(operations)}'
        )

        # Connector template based on service
        if service.lower() == "jira":
            return self._create_jira_connector(tool_name, operations)
        else:
            return {
                "status": "error",
                "message": f"Connector for {service} not yet supported",
            }

    def _create_jira_connector(
        self, tool_name: str, operations: List[str]
    ) -> Dict[str, Any]:
        """Create a Jira connector tool."""
        # This would contain the actual Jira connector implementation
        # For now, return a placeholder
        code = f'''def {tool_name}(input_data=None):
    """
    Jira connector for operations: {', '.join(operations)}
    """
    import json
    
    if input_data is None:
        return {{'status': 'error', 'message': 'No input provided'}}
    
    try:
        # Parse input
        if isinstance(input_data, str):
            data = json.loads(input_data)
        elif isinstance(input_data, dict):
            data = input_data
        else:
            return {{'status': 'error', 'message': 'Invalid input type'}}
        
        operation = data.get('operation')
        
        # Handle operations
        if operation in {operations}:
            # Placeholder for actual Jira API calls
            return {{
                'status': 'success',
                'operation': operation,
                'result': 'Operation completed'
            }}
        else:
            return {{'status': 'error', 'message': f'Unsupported operation: {{operation}}'}}
    
    except Exception as e:
        return {{'status': 'error', 'message': str(e)}}
'''

        return self.registry.register_tool(
            name=tool_name,
            description=f'Jira connector for {", ".join(operations)}',
            code=code,
            is_pure_function=False,
            tags=["connector", "jira", "external"],
        )

    def _generate_functional_tool_code(self, tool_name: str, description: str) -> str:
        """Generate actually functional tool code based on name and description."""

        # Extract tool purpose
        tool_lower = tool_name.lower()
        desc_lower = description.lower()

        # Generate appropriate implementation
        if "extract" in tool_lower:
            if "email" in tool_lower:
                return self._generate_email_extractor()
            elif "phone" in tool_lower:
                return self._generate_phone_extractor()
            elif "url" in tool_lower:
                return self._generate_url_extractor()
            else:
                return self._generate_generic_extractor(tool_name)

        elif "calculate" in tool_lower or "calc" in tool_lower:
            if "mean" in tool_lower or "average" in tool_lower:
                return self._generate_mean_calculator()
            elif "median" in tool_lower:
                return self._generate_median_calculator()
            elif "std" in tool_lower or "deviation" in tool_lower:
                return self._generate_std_calculator()
            else:
                return self._generate_generic_calculator(tool_name)

        elif "format" in tool_lower:
            return self._generate_formatter(tool_name)

        elif "generate" in tool_lower:
            if "chart" in tool_lower or "graph" in tool_lower:
                return self._generate_chart_generator()
            elif "report" in tool_lower:
                return self._generate_report_generator()
            else:
                return self._generate_generic_generator(tool_name)

        else:
            # Default functional implementation
            return self._generate_default_tool(tool_name, description)

    def _generate_phone_extractor(self) -> str:
        """Generate phone extraction tool."""
        return '''def extract_phone(input_data=None):
        """Extract phone numbers from text."""
        import re
        
        if input_data is None:
            return []
        
        try:
            # Convert input to string
            if isinstance(input_data, dict):
                text = str(input_data.get('text', input_data.get('data', input_data)))
            else:
                text = str(input_data)
            
            # Phone number patterns
            patterns = [
                r'\\(?\\d{3}\\)?[\\s.-]?\\d{3}[\\s.-]?\\d{4}',  # US format
                r'\\d{3}-\\d{3}-\\d{4}',  # 555-555-5555
                r'\\(\\d{3}\\)\\s*\\d{3}-\\d{4}',  # (555) 555-5555
                r'\\d{10}',  # 5555555555
            ]
            
            phones = []
            for pattern in patterns:
                phones.extend(re.findall(pattern, text))
            
            # Remove duplicates
            return list(set(phones))
        
        except Exception:
            return []
    '''

    def _generate_formatter(self, tool_name: str) -> str:
        """Generate formatting tool."""
        return f'''def {tool_name}(input_data=None):
        """Format data for presentation."""
        
        if input_data is None:
            return ""
        
        try:
            if isinstance(input_data, dict):
                # Format as key-value pairs
                lines = []
                for key, value in input_data.items():
                    lines.append(f"{{key.title()}}: {{value}}")
                return "\\n".join(lines)
            elif isinstance(input_data, list):
                # Format as bullet points
                return "\\n".join([f"• {{item}}" for item in input_data])
            else:
                # Basic formatting
                return f"=== Output ===\\n{{input_data}}\\n============"
        
        except Exception:
            return str(input_data)
    '''

    def _generate_chart_generator(self) -> str:
        """Generate chart creation tool."""
        return '''def generate_bar_chart(input_data=None):
        """Generate a bar chart from data."""
        
        if input_data is None:
            return {"type": "chart", "data": None, "error": "No data provided"}
        
        try:
            # Extract data for chart
            if isinstance(input_data, dict):
                # Assume dict has labels and values
                labels = input_data.get('labels', list(input_data.keys()))
                values = input_data.get('values', list(input_data.values()))
            elif isinstance(input_data, list):
                # Create simple numbered labels
                labels = [f"Item {i+1}" for i in range(len(input_data))]
                values = input_data
            else:
                return {"type": "chart", "data": None, "error": "Invalid data format"}
            
            # Return chart specification (would be rendered by UI)
            return {
                "type": "bar_chart",
                "labels": labels,
                "values": values,
                "title": "Generated Bar Chart",
                "x_label": "Categories",
                "y_label": "Values"
            }
        
        except Exception as e:
            return {"type": "chart", "data": None, "error": str(e)}
    '''

    def _generate_default_tool(self, tool_name: str, description: str) -> str:
        """Generate a default but functional tool."""
        return f'''def {tool_name}(input_data=None):
        """
        {description}
        """
        
        if input_data is None:
            return None
        
        try:
            # Process based on input type
            if isinstance(input_data, str):
                # String processing
                result = {{"processed": input_data, "length": len(input_data)}}
            elif isinstance(input_data, dict):
                # Dictionary processing
                result = {{"keys": list(input_data.keys()), "size": len(input_data)}}
            elif isinstance(input_data, list):
                # List processing
                result = {{"items": len(input_data), "first": input_data[0] if input_data else None}}
            else:
                # Generic processing
                result = {{"type": type(input_data).__name__, "value": str(input_data)}}
            
            return result
        
        except Exception as e:
            return {{"error": str(e), "input_type": type(input_data).__name__}}
    '''

    def _generate_mean_calculator(self) -> str:
        """Generate mean calculation tool."""
        return '''def calculate_mean(input_data=None):
        """Calculate arithmetic mean of numbers."""
        
        if input_data is None:
            return 0
        
        try:
            # Extract numbers from various formats
            numbers = []
            
            if isinstance(input_data, (list, tuple)):
                numbers = [float(x) for x in input_data if isinstance(x, (int, float))]
            elif isinstance(input_data, dict):
                if 'numbers' in input_data:
                    numbers = input_data['numbers']
                elif 'values' in input_data:
                    numbers = input_data['values']
                else:
                    # Try to extract numbers from dict values
                    numbers = [v for v in input_data.values() if isinstance(v, (int, float))]
            elif isinstance(input_data, str):
                # Extract numbers from string
                import re
                numbers = [float(x) for x in re.findall(r'-?\d+\.?\d*', input_data)]
            else:
                numbers = [float(input_data)]
            
            if numbers:
                return sum(numbers) / len(numbers)
            return 0
            
        except Exception:
            return 0
    '''

    def _generate_median_calculator(self) -> str:
        """Generate median calculation tool."""
        return '''def calculate_median(input_data=None):
        """Calculate median of numbers."""
        
        if input_data is None:
            return 0
        
        try:
            # Extract numbers from various formats
            numbers = []
            
            if isinstance(input_data, (list, tuple)):
                numbers = sorted([float(x) for x in input_data if isinstance(x, (int, float))])
            elif isinstance(input_data, dict):
                if 'numbers' in input_data:
                    numbers = sorted(input_data['numbers'])
                elif 'values' in input_data:
                    numbers = sorted(input_data['values'])
                else:
                    numbers = sorted([v for v in input_data.values() if isinstance(v, (int, float))])
            elif isinstance(input_data, str):
                import re
                numbers = sorted([float(x) for x in re.findall(r'-?\d+\.?\d*', input_data)])
            else:
                return float(input_data)
            
            if not numbers:
                return 0
                
            n = len(numbers)
            if n % 2 == 0:
                return (numbers[n//2 - 1] + numbers[n//2]) / 2
            else:
                return numbers[n//2]
                
        except Exception:
            return 0
    '''

    def _generate_std_calculator(self) -> str:
        """Generate standard deviation calculation tool."""
        return '''def calculate_std(input_data=None):
        """Calculate standard deviation of numbers."""
        
        if input_data is None:
            return 0
        
        try:
            # Extract numbers from various formats
            numbers = []
            
            if isinstance(input_data, (list, tuple)):
                numbers = [float(x) for x in input_data if isinstance(x, (int, float))]
            elif isinstance(input_data, dict):
                if 'numbers' in input_data:
                    numbers = input_data['numbers']
                elif 'values' in input_data:
                    numbers = input_data['values']
                else:
                    numbers = [v for v in input_data.values() if isinstance(v, (int, float))]
            elif isinstance(input_data, str):
                import re
                numbers = [float(x) for x in re.findall(r'-?\d+\.?\d*', input_data)]
            else:
                return 0
            
            if not numbers or len(numbers) < 2:
                return 0
                
            # Calculate mean
            mean = sum(numbers) / len(numbers)
            
            # Calculate variance
            variance = sum((x - mean) ** 2 for x in numbers) / len(numbers)
            
            # Return standard deviation
            return variance ** 0.5
            
        except Exception:
            return 0
    '''

    def _generate_generic_calculator(self, tool_name: str) -> str:
        """Generate generic calculator tool."""
        return f'''def {tool_name}(input_data=None):
        """Perform calculations on input data."""
        
        if input_data is None:
            return 0
        
        try:
            # Extract numbers
            if isinstance(input_data, (list, tuple)):
                numbers = [float(x) for x in input_data if isinstance(x, (int, float))]
            elif isinstance(input_data, dict):
                numbers = [v for v in input_data.values() if isinstance(v, (int, float))]
            else:
                return float(input_data)
            
            # Return basic calculation result
            if numbers:
                return {{
                    "count": len(numbers),
                    "sum": sum(numbers),
                    "avg": sum(numbers) / len(numbers),
                    "min": min(numbers),
                    "max": max(numbers)
                }}
            return 0
            
        except Exception:
            return 0
    '''

    def _generate_generic_generator(self, tool_name: str) -> str:
        """Generate generic generator tool."""
        return f'''def {tool_name}(input_data=None):
        """Generate output based on input."""
        
        if input_data is None:
            return {{}}
        
        try:
            return {{
                "generated": True,
                "type": "{tool_name.replace('_', ' ')}",
                "input_summary": str(input_data)[:100],
                "timestamp": str(datetime.now())
            }}
        except Exception:
            return {{}}
    '''

    def _generate_functional_tool_code(self, tool_name: str, description: str) -> str:
        """Generate ACTUALLY FUNCTIONAL tool code - NO PLACEHOLDERS."""

        tool_lower = tool_name.lower()
        desc_lower = description.lower()

        # Email extraction
        if "email" in tool_lower or "email" in desc_lower:
            return '''def extract_emails(input_data=None):
        """Extract email addresses from text."""
        import re
        
        if input_data is None:
            return []
        
        try:
            text = str(input_data)
            if isinstance(input_data, dict):
                text = ' '.join(str(v) for v in input_data.values())
            elif isinstance(input_data, list):
                text = ' '.join(str(item) for item in input_data)
            
            # Comprehensive email regex
            pattern = r'\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b'
            emails = re.findall(pattern, text, re.IGNORECASE)
            return list(set(email.lower() for email in emails))
        except Exception:
            return []
    '''

        # URL extraction
        elif "url" in tool_lower or "link" in tool_lower:
            return '''def extract_urls(input_data=None):
        """Extract URLs from text."""
        import re
        
        if input_data is None:
            return []
        
        try:
            text = str(input_data)
            if isinstance(input_data, dict):
                text = ' '.join(str(v) for v in input_data.values())
            
            # Multiple URL patterns for better coverage
            patterns = [
                r'https?://[^\\s<>"{}|\\\\^`\\[\\]]+',
                r'www\\.[^\\s<>"{}|\\\\^`\\[\\]]+',
                r'ftp://[^\\s<>"{}|\\\\^`\\[\\]]+'
            ]
            
            urls = []
            for pattern in patterns:
                urls.extend(re.findall(pattern, text, re.IGNORECASE))
            
            # Clean and deduplicate
            clean_urls = []
            for url in urls:
                if not url.startswith('http'):
                    url = 'http://' + url
                clean_urls.append(url)
            
            return list(set(clean_urls))
        except Exception:
            return []
    '''

        # Phone extraction
        elif "phone" in tool_lower or "telephone" in tool_lower:
            return '''def extract_phones(input_data=None):
        """Extract phone numbers from text."""
        import re
        
        if input_data is None:
            return []
        
        try:
            text = str(input_data)
            if isinstance(input_data, dict):
                text = ' '.join(str(v) for v in input_data.values())
            
            # Multiple phone patterns
            patterns = [
                r'\\+?1?\\s*\\(?\\d{3}\\)?[\\s.-]?\\d{3}[\\s.-]?\\d{4}',  # US format
                r'\\(\\d{3}\\)\\s*\\d{3}-\\d{4}',  # (555) 555-5555
                r'\\d{3}-\\d{3}-\\d{4}',  # 555-555-5555
                r'\\d{10}',  # 5555555555
            ]
            
            phones = []
            for pattern in patterns:
                matches = re.findall(pattern, text)
                phones.extend(matches)
            
            # Clean and format
            clean_phones = []
            for phone in phones:
                # Remove non-digits for comparison
                digits = re.sub(r'\\D', '', phone)
                if len(digits) >= 10:
                    clean_phones.append(phone)
            
            return list(set(clean_phones))
        except Exception:
            return []
    '''

        # Calculations
        elif "mean" in tool_lower or "average" in tool_lower:
            return '''def calculate_mean(input_data=None):
        """Calculate mean of numbers."""
        
        if input_data is None:
            return 0.0
        
        try:
            numbers = []
            
            if isinstance(input_data, (list, tuple)):
                for item in input_data:
                    try:
                        numbers.append(float(item))
                    except (ValueError, TypeError):
                        continue
            elif isinstance(input_data, dict):
                # Try common keys first
                for key in ['numbers', 'values', 'data']:
                    if key in input_data:
                        if isinstance(input_data[key], (list, tuple)):
                            for item in input_data[key]:
                                try:
                                    numbers.append(float(item))
                                except:
                                    continue
                        break
                else:
                    # Try all values
                    for value in input_data.values():
                        try:
                            if isinstance(value, (list, tuple)):
                                for item in value:
                                    try:
                                        numbers.append(float(item))
                                    except:
                                        continue
                            else:
                                numbers.append(float(value))
                        except:
                            continue
            elif isinstance(input_data, str):
                import re
                # Extract numbers from string
                matches = re.findall(r'-?\\d+\\.?\\d*', input_data)
                numbers = [float(m) for m in matches]
            else:
                try:
                    numbers = [float(input_data)]
                except:
                    return 0.0
            
            if not numbers:
                return 0.0
                
            return sum(numbers) / len(numbers)
            
        except Exception:
            return 0.0
    '''

        # Sentiment analysis
        elif "sentiment" in tool_lower:
            return '''def analyze_sentiment(input_data=None):
        """Analyze sentiment of text."""
        
        if input_data is None:
            return {"sentiment": "neutral", "score": 0.0}
        
        try:
            text = str(input_data)
            if isinstance(input_data, dict):
                text = input_data.get('text', input_data.get('content', str(input_data)))
            
            text_lower = text.lower()
            
            # Simple but functional sentiment analysis
            positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 
                            'fantastic', 'love', 'perfect', 'best', 'happy', 'awesome',
                            'brilliant', 'outstanding', 'superior', 'positive', 'success']
            negative_words = ['bad', 'terrible', 'awful', 'horrible', 'hate', 'worst',
                            'poor', 'disappointing', 'failure', 'negative', 'wrong',
                            'broken', 'useless', 'waste', 'angry', 'frustrated']
            
            positive_count = sum(1 for word in positive_words if word in text_lower)
            negative_count = sum(1 for word in negative_words if word in text_lower)
            
            # Calculate score
            if positive_count + negative_count == 0:
                sentiment = "neutral"
                score = 0.0
            else:
                score = (positive_count - negative_count) / (positive_count + negative_count)
                if score > 0.2:
                    sentiment = "positive"
                elif score < -0.2:
                    sentiment = "negative"
                else:
                    sentiment = "neutral"
            
            return {
                "sentiment": sentiment,
                "score": score,
                "positive_words": positive_count,
                "negative_words": negative_count
            }
            
        except Exception:
            return {"sentiment": "neutral", "score": 0.0}
    '''

        # Generic but functional tool
        else:
            # Create a functional tool based on the name
            return f'''def {tool_name}(input_data=None):
        """
        {description}
        """
        
        if input_data is None:
            return {{"status": "no_input", "result": None}}
        
        try:
            result = {{"status": "success"}}
            
            # Process based on input type
            if isinstance(input_data, str):
                result["text_length"] = len(input_data)
                result["word_count"] = len(input_data.split())
                result["processed"] = input_data.strip()
            elif isinstance(input_data, dict):
                result["keys"] = list(input_data.keys())
                result["size"] = len(input_data)
                result["processed"] = input_data
            elif isinstance(input_data, list):
                result["count"] = len(input_data)
                result["processed"] = input_data
            else:
                result["type"] = type(input_data).__name__
                result["value"] = str(input_data)
            
            return result
            
        except Exception as e:
            return {{"status": "error", "message": str(e)}}
    '''

    def ensure_tool(
        self, tool_name: str, description: str, tool_type: str = "pure_function"
    ) -> Dict[str, Any]:
        """Ensure tool exists with FUNCTIONAL implementation."""

        print(f"DEBUG: Ensuring tool '{tool_name}' exists")

        # Check if exists and file is actually there
        if self.registry.tool_exists(tool_name):
            tool = self.registry.get_tool(tool_name)
            # Verify file actually exists
            if os.path.exists(tool["location"]):
                print(f"DEBUG: Tool '{tool_name}' already exists - returning existing")
                return {"status": "exists", "tool": tool}
            else:
                print(
                    f"WARNING: Tool {tool_name} in registry but file missing, recreating..."
                )

        print(f"DEBUG: Tool '{tool_name}' doesn't exist - creating new")

        # Generate functional code
        code = self._generate_functional_tool_code(tool_name, description)

        # Use register_tool which now has verification
        registration_result = self.registry.register_tool(
            name=tool_name,
            description=description,
            code=code,
            signature=f"def {tool_name}(input_data=None)",
            tags=self._extract_tags_from_description(description),
            is_prebuilt=False,
            is_pure_function=(tool_type == "pure_function"),
        )

        if registration_result["status"] == "success":
            return {"status": "success", "tool": self.registry.get_tool(tool_name)}
        else:
            print(
                f"WARNING: Tool registration had issues: {registration_result.get('message')}"
            )
            return registration_result

```

--------------------------------------------------------------------------------

### File: core/workflow_engine.py
**Path:** `core/workflow_engine.py`
**Size:** 20,122 bytes
**Modified:** 2025-09-14 09:43:56

```python
"""
Multi-Agent Workflow Engine - Sequential processing with data flow
Location: core/workflow_engine.py
"""

import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime
import json
from core.specialized_agents import (
    PDFAnalyzerAgent,
    ChartGeneratorAgent,
    TextProcessorAgent,
)
from core.intelligent_agent_base import DataAnalysisAgent


class MultiAgentWorkflowEngine:
    """Orchestrates sequential multi-agent workflows with intelligent data flow."""

    def __init__(self):
        self.agents = {
            "pdf_analyzer": PDFAnalyzerAgent(),
            "chart_generator": ChartGeneratorAgent(),
            "text_processor": TextProcessorAgent(),
            "data_analyzer": DataAnalysisAgent(),
        }
        self.workflow_state = {}

    async def execute_workflow(
        self, workflow_plan: Dict, request: str, files: List[Dict] = None
    ) -> Dict:
        """
        Execute multi-agent workflow with sequential processing and data flow.

        Args:
            workflow_plan: Plan from orchestrator with agent sequence
            request: Original user request
            files: Uploaded files with content

        Returns:
            Dict with complete workflow results
        """

        workflow_id = f"wf_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        start_time = datetime.now()

        # Initialize workflow state
        self.workflow_state = {
            "workflow_id": workflow_id,
            "request": request,
            "files": files or [],
            "current_data": None,
            "step_results": {},
            "data_flow": [],
            "errors": [],
            "started_at": start_time.isoformat(),
        }

        try:
            # Get agent sequence from plan
            agent_sequence = workflow_plan.get("agents", [])
            execution_strategy = workflow_plan.get("execution_strategy", "sequential")

            if execution_strategy == "sequential":
                results = await self._execute_sequential(agent_sequence, request, files)
            elif execution_strategy == "parallel":
                results = await self._execute_parallel(agent_sequence, request, files)
            else:
                # Default to sequential
                results = await self._execute_sequential(agent_sequence, request, files)

            # Compile final results
            execution_time = (datetime.now() - start_time).total_seconds()

            return {
                "status": "success",
                "workflow_id": workflow_id,
                "execution_time": execution_time,
                "results": results,
                "data_flow": self.workflow_state["data_flow"],
                "summary": self._generate_workflow_summary(results),
                "metadata": {
                    "agents_executed": len(agent_sequence),
                    "strategy": execution_strategy,
                    "files_processed": len(files) if files else 0,
                },
            }

        except Exception as e:
            return {
                "status": "error",
                "workflow_id": workflow_id,
                "error": str(e),
                "partial_results": self.workflow_state.get("step_results", {}),
                "data_flow": self.workflow_state.get("data_flow", []),
            }

    # async def _execute_sequential(
    #     self, agent_sequence: List[str], request: str, files: List[Dict]
    # ) -> Dict:
    #     """Execute agents sequentially with data flowing between steps."""

    #     results = {}
    #     current_data = None

    #     # Start with file data if available
    #     if files and files[0].get("read_success"):
    #         current_data = files[0]
    #         self.workflow_state["current_data"] = current_data

    #     for i, agent_name in enumerate(agent_sequence):
    #         print(f"🔄 Step {i+1}: Executing {agent_name}")

    #         # Get agent
    #         agent = self.agents.get(agent_name)
    #         if not agent:
    #             print(f"⚠️  Agent {agent_name} not found, skipping")
    #             continue

    #         # Prepare context for this step
    #         step_context = {
    #             "step_number": i + 1,
    #             "total_steps": len(agent_sequence),
    #             "previous_results": results,
    #             "workflow_request": request,
    #         }

    #         # Execute agent with current data
    #         step_result = await agent.execute(
    #             request=request, file_data=current_data, context=step_context
    #         )

    #         # Store result
    #         results[agent_name] = step_result
    #         self.workflow_state["step_results"][agent_name] = step_result

    #         # Update data flow for next step
    #         if step_result.get("status") == "success":
    #             # Pass successful data to next agent
    #             data_output = step_result.get("data", {})

    #             # Create enriched data for next step
    #             if current_data:
    #                 # Merge new results with existing data
    #                 enhanced_data = {
    #                     **current_data,
    #                     "previous_analysis": data_output,
    #                     "step_history": results,
    #                 }
    #             else:
    #                 # Create new data structure
    #                 enhanced_data = {
    #                     "content": data_output,
    #                     "structure": "processed",
    #                     "previous_analysis": data_output,
    #                     "step_history": results,
    #                 }

    #             current_data = enhanced_data
    #             self.workflow_state["current_data"] = current_data

    #             # Log data flow
    #             self.workflow_state["data_flow"].append(
    #                 {
    #                     "from_step": agent_name,
    #                     "to_step": (
    #                         agent_sequence[i + 1]
    #                         if i + 1 < len(agent_sequence)
    #                         else "final"
    #                     ),
    #                     "data_type": type(data_output).__name__,
    #                     "data_size": len(str(data_output)) if data_output else 0,
    #                     "timestamp": datetime.now().isoformat(),
    #                 }
    #             )

    #             print(f"✅ {agent_name} completed successfully")

    #         else:
    #             error_msg = step_result.get("error", "Unknown error")
    #             print(f"❌ {agent_name} failed: {error_msg}")
    #             self.workflow_state["errors"].append(
    #                 {
    #                     "step": agent_name,
    #                     "error": error_msg,
    #                     "timestamp": datetime.now().isoformat(),
    #                 }
    #             )

    #     return results

    async def _execute_sequential(
        self, agent_sequence: List[str], request: str, files: List[Dict]
    ) -> Dict:
        """Execute agents sequentially with data flowing between steps."""

        results = {}
        current_data = None

        # Start with file data if available
        if files and files[0].get("read_success"):
            current_data = files[0]
            self.workflow_state["current_data"] = current_data

        for i, agent_name in enumerate(agent_sequence):
            print(f"Step {i+1}: Executing {agent_name}")

            # Get agent
            agent = self.agents.get(agent_name)
            if not agent:
                print(f"Agent {agent_name} not found, skipping")
                continue

            # Prepare context for this step
            step_context = {
                "step_number": i + 1,
                "total_steps": len(agent_sequence),
                "previous_results": results,
                "workflow_request": request,
            }

            # FIXED: Execute agent with proper method signature
            try:
                if agent_name in ["pdf_analyzer", "text_processor", "chart_generator"]:
                    # New specialized agents - use keyword arguments
                    step_result = await agent.execute(
                        request=request, file_data=current_data, context=step_context
                    )
                else:
                    # Old IntelligentAgent - use state format
                    state = {
                        "current_data": current_data,
                        "request": request,
                        "results": results,
                        "errors": [],
                        "execution_path": [],
                    }
                    step_result = await agent.execute(state)

            except Exception as e:
                print(f"Agent {agent_name} failed: {str(e)}")
                step_result = {"status": "error", "error": str(e), "data": None}

            # Store result
            results[agent_name] = step_result
            self.workflow_state["step_results"][agent_name] = step_result

            # Update data flow for next step
            if step_result.get("status") == "success":
                # Pass successful data to next agent
                data_output = step_result.get("data", {})

                # Create enriched data for next step
                if current_data:
                    # Merge new results with existing data
                    enhanced_data = {
                        **current_data,
                        "previous_analysis": data_output,
                        "step_history": results,
                    }
                else:
                    # Create new data structure
                    enhanced_data = {
                        "content": data_output,
                        "structure": "processed",
                        "previous_analysis": data_output,
                        "step_history": results,
                    }

                current_data = enhanced_data
                self.workflow_state["current_data"] = current_data

                # Log data flow
                self.workflow_state["data_flow"].append(
                    {
                        "from_step": agent_name,
                        "to_step": (
                            agent_sequence[i + 1]
                            if i + 1 < len(agent_sequence)
                            else "final"
                        ),
                        "data_type": type(data_output).__name__,
                        "data_size": len(str(data_output)) if data_output else 0,
                        "timestamp": datetime.now().isoformat(),
                    }
                )

                print(f"{agent_name} completed successfully")

            else:
                error_msg = step_result.get("error", "Unknown error")
                print(f"{agent_name} failed: {error_msg}")
                self.workflow_state["errors"].append(
                    {
                        "step": agent_name,
                        "error": error_msg,
                        "timestamp": datetime.now().isoformat(),
                    }
                )

        return results

    async def _execute_parallel(
        self, agent_sequence: List[str], request: str, files: List[Dict]
    ) -> Dict:
        """Execute agents in parallel (for independent tasks)."""

        print(f"🔄 Executing {len(agent_sequence)} agents in parallel")

        # Prepare tasks
        tasks = []
        for agent_name in agent_sequence:
            agent = self.agents.get(agent_name)
            if agent:
                # Each agent gets the original file data
                file_data = files[0] if files and files[0].get("read_success") else None
                task = agent.execute(
                    request=request,
                    file_data=file_data,
                    context={"execution_mode": "parallel"},
                )
                tasks.append((agent_name, task))

        # Execute all tasks concurrently
        results = {}
        task_results = await asyncio.gather(
            *[task for _, task in tasks], return_exceptions=True
        )

        # Process results
        for i, (agent_name, result) in enumerate(
            zip([name for name, _ in tasks], task_results)
        ):
            if isinstance(result, Exception):
                results[agent_name] = {
                    "status": "error",
                    "error": str(result),
                    "data": None,
                }
                print(f"❌ {agent_name} failed: {result}")
            else:
                results[agent_name] = result
                print(f"✅ {agent_name} completed")

        return results

    def _generate_workflow_summary(self, results: Dict) -> str:
        """Generate human-readable workflow summary - FIXED VERSION."""

        successful_agents = []
        failed_agents = []

        # FIXED: Handle different result structures safely
        for name, result in results.items():
            if isinstance(result, dict):
                if result.get("status") == "success":
                    successful_agents.append(name)
                elif result.get("status") == "error":
                    failed_agents.append(name)
                else:
                    # Unknown status, treat as successful if no error
                    successful_agents.append(name)
            elif isinstance(result, str):
                # String result - assume successful
                successful_agents.append(name)
            else:
                # Other type - assume successful
                successful_agents.append(name)

        summary_parts = []

        if successful_agents:
            summary_parts.append(
                f"✅ Successfully executed: {', '.join(successful_agents)}"
            )

            # Add key insights from each agent - FIXED with type checking
            for agent_name in successful_agents:
                result = results.get(agent_name, {})

                # Handle different result types
                if isinstance(result, dict):
                    data = result.get("data", {})

                    if (
                        agent_name == "pdf_analyzer"
                        and isinstance(data, dict)
                        and data.get("summary")
                    ):
                        summary_parts.append(
                            f"📄 PDF Analysis: {str(data['summary'])[:100]}..."
                        )

                    elif agent_name == "text_processor":
                        if isinstance(data, dict) and data.get("processed_text"):
                            summary_parts.append(
                                f"📝 Text Processing: {str(data['processed_text'])[:100]}..."
                            )
                        elif isinstance(data, str):
                            summary_parts.append(f"📝 Text Processing: {data[:100]}...")

                    elif (
                        agent_name == "chart_generator"
                        and isinstance(data, dict)
                        and data.get("chart_type")
                    ):
                        summary_parts.append(f"📊 Generated {data['chart_type']} chart")

                    elif agent_name == "data_analyzer":
                        summary_parts.append(
                            f"📈 Data Analysis: Key insights identified"
                        )

                elif isinstance(result, str):
                    # Handle string results
                    summary_parts.append(f"• {agent_name}: {result[:50]}...")

        if failed_agents:
            summary_parts.append(f"❌ Failed: {', '.join(failed_agents)}")

        return " | ".join(summary_parts) if summary_parts else "Workflow completed"

    def get_workflow_state(self) -> Dict:
        """Get current workflow state for debugging."""
        return self.workflow_state.copy()


class WorkflowPlanner:
    """Plans optimal multi-agent workflows based on requests and data."""

    def __init__(self):
        self.available_agents = {
            "pdf_analyzer": {
                "best_for": ["pdf", "document_analysis", "text_extraction"],
                "input_types": ["pdf", "document"],
                "output_types": ["analysis", "extracted_text", "insights"],
            },
            "text_processor": {
                "best_for": ["text_analysis", "entity_extraction", "sentiment"],
                "input_types": ["text", "string", "document"],
                "output_types": ["processed_text", "entities", "analysis"],
            },
            "chart_generator": {
                "best_for": ["visualization", "charts", "graphs", "plotting"],
                "input_types": ["tabular", "csv", "data"],
                "output_types": ["chart", "visualization", "graph"],
            },
            "data_analyzer": {
                "best_for": ["data_analysis", "statistics", "patterns"],
                "input_types": ["tabular", "csv", "numbers"],
                "output_types": ["analysis", "statistics", "insights"],
            },
        }

    def plan_workflow(self, request: str, files: List[Dict] = None) -> Dict:
        """Plan optimal workflow based on request and available data."""

        request_lower = request.lower()
        file_types = [f.get("structure", "unknown") for f in files] if files else []

        planned_agents = []
        execution_strategy = "sequential"  # Default to sequential for data flow

        # Analyze request intent
        if "pdf" in request_lower or "document" in request_lower or "pdf" in file_types:
            planned_agents.append("pdf_analyzer")

            # If also asking for charts/analysis, add those
            if any(
                word in request_lower
                for word in ["chart", "graph", "plot", "visualize"]
            ):
                planned_agents.append("chart_generator")
            if any(
                word in request_lower for word in ["analyze", "analysis", "insights"]
            ):
                planned_agents.append("text_processor")

        elif (
            "chart" in request_lower
            or "graph" in request_lower
            or "visualize" in request_lower
        ):
            # Data analysis first, then chart generation
            if "tabular" in file_types or "csv" in str(files).lower():
                planned_agents.extend(["data_analyzer", "chart_generator"])
            else:
                planned_agents.append("chart_generator")

        elif any(
            word in request_lower
            for word in ["analyze", "analysis", "extract", "process"]
        ):
            if "tabular" in file_types:
                planned_agents.append("data_analyzer")
            else:
                planned_agents.append("text_processor")

        # Default workflow
        if not planned_agents:
            if file_types:
                if "pdf" in file_types:
                    planned_agents.append("pdf_analyzer")
                elif "tabular" in file_types:
                    planned_agents.append("data_analyzer")
                else:
                    planned_agents.append("text_processor")
            else:
                planned_agents.append("text_processor")

        # FIXED: Always use sequential for multi-agent workflows to enable data flow
        if len(planned_agents) > 1:
            execution_strategy = "sequential"
        else:
            execution_strategy = (
                "sequential"  # Even single agents benefit from sequential processing
            )

        return {
            "agents": planned_agents,
            "execution_strategy": execution_strategy,
            "rationale": f"Selected {len(planned_agents)} agents based on request analysis",
            "data_flow_required": len(planned_agents) > 1,
        }

```

--------------------------------------------------------------------------------

### File: create_knowledge_base.py
**Path:** `create_knowledge_base.py`
**Size:** 10,923 bytes
**Modified:** 2025-09-14 16:39:00

```python
#!/usr/bin/env python3
"""
Agentic Fabric POC - Project Knowledge Base Extractor
Creates a comprehensive single file containing all project code and structure
for LLM context and documentation purposes.
"""

import os
import datetime
from pathlib import Path


class ProjectKnowledgeExtractor:
    def __init__(self, project_root="."):
        self.project_root = Path(project_root).resolve()
        self.output_file = "KNOWLEDGE_BASE.md"

        # Files and directories to exclude
        self.exclude_dirs = {
            "venv",
            "__pycache__",
            ".git",
            "node_modules",
            ".pytest_cache",
            ".mypy_cache",
            "dist",
            "build",
            "backup_removed_components",
            "flask_app",
        }

        self.exclude_files = {
            ".DS_Store",
            ".pyc",
            ".pyo",
            ".pyd",
            ".so",
            ".egg-info",
            ".coverage",
            ".env",  # Exclude .env for security
        }

        # File extensions to include full content
        self.include_extensions = {
            ".py",
            ".md",
            ".txt",
            ".json",
            ".yaml",
            ".yml",
            ".toml",
            ".cfg",
            ".ini",
            ".sh",
            ".sql",
        }

        # Maximum file size to include (in bytes)
        self.max_file_size = 20000000  # 20MB

    def should_exclude_dir(self, dir_name):
        """Check if directory should be excluded"""
        return dir_name in self.exclude_dirs or dir_name.startswith(".")

    def should_exclude_file(self, file_path):
        """Check if file should be excluded"""
        file_path = Path(file_path)

        # Check file name
        if file_path.name in self.exclude_files:
            return True

        # Check extension
        if file_path.suffix in self.exclude_files:
            return True

        # Check if file is too large
        try:
            if file_path.stat().st_size > self.max_file_size:
                return True
        except OSError:
            return True

        return False

    def should_include_content(self, file_path):
        """Check if file content should be included"""
        file_path = Path(file_path)
        return file_path.suffix.lower() in self.include_extensions

    def get_file_content(self, file_path):
        """Get file content safely"""
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                return content
        except Exception as e:
            return f"[ERROR READING FILE: {str(e)}]"

    def generate_tree_structure(self):
        """Generate directory tree structure"""
        tree_lines = []

        def add_tree_line(path, prefix="", is_last=True):
            if self.should_exclude_dir(path.name) and path != self.project_root:
                return

            connector = "└── " if is_last else "├── "
            tree_lines.append(f"{prefix}{connector}{path.name}/")

            # Get subdirectories and files
            try:
                items = sorted(
                    [p for p in path.iterdir() if not self.should_exclude_dir(p.name)]
                )
                dirs = [p for p in items if p.is_dir()]
                files = [
                    p for p in items if p.is_file() and not self.should_exclude_file(p)
                ]

                all_items = dirs + files

                for i, item in enumerate(all_items):
                    is_last_item = i == len(all_items) - 1
                    new_prefix = prefix + ("    " if is_last else "│   ")

                    if item.is_dir():
                        add_tree_line(item, new_prefix, is_last_item)
                    else:
                        file_connector = "└── " if is_last_item else "├── "
                        tree_lines.append(f"{new_prefix}{file_connector}{item.name}")

            except PermissionError:
                pass

        tree_lines.append(f"{self.project_root.name}/")

        # Process root directory contents
        try:
            items = sorted(
                [
                    p
                    for p in self.project_root.iterdir()
                    if not self.should_exclude_dir(p.name)
                ]
            )
            dirs = [p for p in items if p.is_dir()]
            files = [
                p for p in items if p.is_file() and not self.should_exclude_file(p)
            ]

            all_items = dirs + files

            for i, item in enumerate(all_items):
                is_last_item = i == len(all_items) - 1

                if item.is_dir():
                    add_tree_line(item, "", is_last_item)
                else:
                    connector = "└── " if is_last_item else "├── "
                    tree_lines.append(f"{connector}{item.name}")

        except PermissionError:
            tree_lines.append("[Permission denied reading root directory]")

        return "\n".join(tree_lines)

    def collect_all_files(self):
        """Collect all relevant files in the project"""
        all_files = []

        for root, dirs, files in os.walk(self.project_root):
            # Filter out excluded directories
            dirs[:] = [d for d in dirs if not self.should_exclude_dir(d)]

            for file in files:
                file_path = Path(root) / file

                if not self.should_exclude_file(file_path):
                    relative_path = file_path.relative_to(self.project_root)
                    all_files.append(relative_path)

        return sorted(all_files)

    def generate_knowledge_base(self):
        """Generate the complete knowledge base file"""
        print(f"Generating knowledge base for: {self.project_root}")

        content = []

        # Header
        content.append("# AGENTIC FABRIC POC - COMPLETE PROJECT KNOWLEDGE BASE")
        content.append("=" * 80)
        content.append(
            f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        content.append(f"Project Root: {self.project_root}")
        content.append("")

        # Project Overview
        content.append("## PROJECT OVERVIEW")
        content.append("")
        content.append("**Agentic Fabric POC:** Dual-model AI orchestration platform")
        content.append("- GPT: Master orchestrator for strategic decisions")
        content.append("- Claude: Intelligent agent execution engine")
        content.append("- LangGraph: Workflow coordination")
        content.append("- Streamlit: User interface")
        content.append("")

        # Directory Structure
        content.append("## PROJECT DIRECTORY STRUCTURE")
        content.append("```")
        content.append(self.generate_tree_structure())
        content.append("```")
        content.append("")

        # File Contents Section
        content.append("## COMPLETE FILE CONTENTS")
        content.append("")

        all_files = self.collect_all_files()
        total_files = len(all_files)

        print(f"Processing {total_files} files...")

        for i, file_path in enumerate(all_files, 1):
            full_path = self.project_root / file_path

            print(f"Processing ({i}/{total_files}): {file_path}")

            # Add file header
            content.append(f"### File: {file_path}")
            content.append(f"**Path:** `{file_path}`")

            try:
                file_stats = full_path.stat()
                content.append(f"**Size:** {file_stats.st_size:,} bytes")
                content.append(
                    f"**Modified:** {datetime.datetime.fromtimestamp(file_stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}"
                )
            except OSError:
                content.append("**Size:** Unable to read")

            content.append("")

            # Add file content if it should be included
            if self.should_include_content(full_path):
                file_content = self.get_file_content(full_path)

                # Determine code block language based on extension
                extension = full_path.suffix.lower()
                if extension == ".py":
                    lang = "python"
                elif extension == ".sh":
                    lang = "bash"
                elif extension in [".yml", ".yaml"]:
                    lang = "yaml"
                elif extension == ".json":
                    lang = "json"
                elif extension == ".md":
                    lang = "markdown"
                else:
                    lang = "text"

                content.append(f"```{lang}")
                content.append(file_content)
                content.append("```")
            else:
                content.append("*[Binary file or content not included]*")

            content.append("")
            content.append("-" * 80)
            content.append("")

        # Write to file
        output_path = self.project_root / self.output_file

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(content))

        print(f"\nKnowledge base generated successfully!")
        print(f"Output file: {output_path}")
        print(f"File size: {output_path.stat().st_size:,} bytes")
        print(f"Total files processed: {total_files}")

        return str(output_path)


def main():
    """Main function to run the knowledge base extractor"""
    print("Agentic Fabric POC - Knowledge Base Extractor")
    print("=" * 50)

    # Check if we're in a project directory
    current_dir = Path.cwd()

    # Look for project indicators
    project_indicators = ["config", "agents", "core", "requirements.txt"]
    has_indicators = any(
        (current_dir / indicator).exists() for indicator in project_indicators
    )

    if not has_indicators:
        print(
            "Warning: Current directory doesn't appear to be the Agentic Fabric project root."
        )
        print(f"Current directory: {current_dir}")
        print("Please navigate to your project directory before running this script.")
        response = input("Continue anyway? (y/N): ").strip().lower()
        if response != "y":
            return

    # Create extractor and generate knowledge base
    extractor = ProjectKnowledgeExtractor()
    output_file = extractor.generate_knowledge_base()

    print(f"\nKnowledge base created: {output_file}")
    print("\nThis file contains:")
    print("- Complete directory structure")
    print("- All source code files with full content")
    print("- Project configuration and documentation")
    print("- Environment setup information")
    print("- Implementation status and next steps")
    print("\nYou can use this file as context for LLM continuation of the project.")


if __name__ == "__main__":
    main()

```

--------------------------------------------------------------------------------

### File: generated/__init__.py
**Path:** `generated/__init__.py`
**Size:** 0 bytes
**Modified:** 2025-09-02 19:29:49

```python

```

--------------------------------------------------------------------------------

### File: generated/agents/email_extractor_agent.py
**Path:** `generated/agents/email_extractor_agent.py`
**Size:** 3,418 bytes
**Modified:** 2025-09-04 10:14:49

```python
def email_extractor_agent(state):
    """
    Agent that extracts email addresses from input.
    Uses extract_emails tool to find all email addresses.
    """
    import sys
    import os
    from datetime import datetime

    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    from generated.tools.extract_emails import extract_emails

    # Initialize state components
    if "results" not in state:
        state["results"] = {}
    if "errors" not in state:
        state["errors"] = []
    if "execution_path" not in state:
        state["execution_path"] = []

    try:
        start_time = datetime.now()

        # Extract input data flexibly
        input_data = None

        # Check current_data first
        current_data = state.get("current_data")
        if current_data is not None:
            if isinstance(current_data, str):
                input_data = current_data
            elif isinstance(current_data, dict):
                for key in ["text", "data", "content", "value", "result"]:
                    if key in current_data:
                        input_data = current_data[key]
                        break
                if input_data is None:
                    input_data = current_data
            else:
                input_data = current_data

        # Check previous results
        if input_data is None and "results" in state:
            for result in reversed(list(state["results"].values())):
                if isinstance(result, dict) and "data" in result:
                    input_data = result["data"]
                    break

        # Check root state
        if input_data is None:
            for key in ["text", "data", "input", "request"]:
                if key in state and state[key]:
                    input_data = state[key]
                    break

        # Process with tool
        emails = extract_emails(input_data)

        # Analyze domains
        domains = {}
        for email in emails:
            domain = email.split("@")[1] if "@" in email else "unknown"
            domains[domain] = domains.get(domain, 0) + 1

        # Calculate execution time
        execution_time = (datetime.now() - start_time).total_seconds()

        # Create standard output envelope
        result = {
            "status": "success",
            "data": {"emails": emails, "count": len(emails), "domains": domains},
            "metadata": {
                "agent": "email_extractor",
                "execution_time": execution_time,
                "tools_used": ["extract_emails"],
                "warnings": [],
            },
        }

        # Update state
        state["results"]["email_extractor"] = result
        state["current_data"] = result["data"]
        state["execution_path"].append("email_extractor")

    except Exception as e:
        import traceback

        error_detail = {
            "agent": "email_extractor",
            "error": str(e),
            "traceback": traceback.format_exc(),
            "timestamp": datetime.now().isoformat(),
        }
        state["errors"].append(error_detail)

        state["results"]["email_extractor"] = {
            "status": "error",
            "data": None,
            "metadata": {
                "agent": "email_extractor",
                "execution_time": 0,
                "error": str(e),
            },
        }

    return state

```

--------------------------------------------------------------------------------

### File: generated/agents/read_csv_agent.py
**Path:** `generated/agents/read_csv_agent.py`
**Size:** 3,536 bytes
**Modified:** 2025-09-04 17:23:07

```python
def read_csv_agent(state):
    """
    Process read_csv tasks
    """
    import sys
    import os
    from datetime import datetime

    # MANDATORY: Add path for imports
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # MANDATORY: Import required tools (if any)
    # No tools to import

    # MANDATORY: Initialize state components
    if 'results' not in state:
        state['results'] = {}
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
        # Process input data
        # No tools specified - process input directly
        if isinstance(input_data, str):
            processed_data = {'processed_text': input_data, 'length': len(input_data)}
        elif isinstance(input_data, dict):
            processed_data = {'processed_data': input_data}
        else:
            processed_data = {'result': str(input_data) if input_data else 'No input provided'}

        # Calculate execution time
        execution_time = (datetime.now() - start_time).total_seconds()

        # MANDATORY: Standard output envelope
        result = {
            "status": "success",
            "data": processed_data,
            "metadata": {
                "agent": "read_csv",
                "execution_time": execution_time,
                "tools_used": [],
                "warnings": []
            }
        }

        # MANDATORY: Update state
        state['results']['read_csv'] = result
        state['current_data'] = result['data']
        state['execution_path'].append('read_csv')

    except Exception as e:
        import traceback
        error_detail = {
            "agent": "read_csv",
            "error": str(e),
            "traceback": traceback.format_exc(),
            "timestamp": datetime.now().isoformat()
        }
        state['errors'].append(error_detail)

        state['results']['read_csv'] = {
            "status": "error",
            "data": None,
            "metadata": {
                "agent": "read_csv",
                "execution_time": 0,
                "error": str(e)
            }
        }

    return state
```

--------------------------------------------------------------------------------

### File: generated/agents/read_text_agent.py
**Path:** `generated/agents/read_text_agent.py`
**Size:** 3,308 bytes
**Modified:** 2025-09-04 12:21:19

```python
def read_text_agent(state):
    """
    Process read_text tasks
    """
    import sys
    import os
    from datetime import datetime

    # MANDATORY: Add path for imports
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # MANDATORY: Import required tools (if any)
    # No tools to import

    # MANDATORY: Initialize state components
    if 'results' not in state:
        state['results'] = {}
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
        # Implement the agent logic here
        processed_data = {
            "original_text": input_data,
            "processed_text": input_data.strip().replace("\n", " ")
        }

        # Calculate execution time
        execution_time = (datetime.now() - start_time).total_seconds()

        # MANDATORY: Standard output envelope
        result = {
            "status": "success",
            "data": processed_data,
            "metadata": {
                "agent": "read_text",
                "execution_time": execution_time,
                "tools_used": [],
                "warnings": []
            }
        }

        # MANDATORY: Update state
        state['results']['read_text'] = result
        state['current_data'] = result['data']
        state['execution_path'].append('read_text')

    except Exception as e:
        import traceback
        error_detail = {
            "agent": "read_text",
            "error": str(e),
            "traceback": traceback.format_exc(),
            "timestamp": datetime.now().isoformat()
        }
        state['errors'].append(error_detail)

        state['results']['read_text'] = {
            "status": "error",
            "data": None,
            "metadata": {
                "agent": "read_text",
                "execution_time": 0,
                "error": str(e)
            }
        }

    return state
```

--------------------------------------------------------------------------------

### File: generated/tools/analyze_sentiment.py
**Path:** `generated/tools/analyze_sentiment.py`
**Size:** 2,001 bytes
**Modified:** 2025-09-14 16:44:20

```python
def analyze_sentiment(input_data=None):
        """Analyze sentiment of text."""
        
        if input_data is None:
            return {"sentiment": "neutral", "score": 0.0}
        
        try:
            text = str(input_data)
            if isinstance(input_data, dict):
                text = input_data.get('text', input_data.get('content', str(input_data)))
            
            text_lower = text.lower()
            
            # Simple but functional sentiment analysis
            positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 
                            'fantastic', 'love', 'perfect', 'best', 'happy', 'awesome',
                            'brilliant', 'outstanding', 'superior', 'positive', 'success']
            negative_words = ['bad', 'terrible', 'awful', 'horrible', 'hate', 'worst',
                            'poor', 'disappointing', 'failure', 'negative', 'wrong',
                            'broken', 'useless', 'waste', 'angry', 'frustrated']
            
            positive_count = sum(1 for word in positive_words if word in text_lower)
            negative_count = sum(1 for word in negative_words if word in text_lower)
            
            # Calculate score
            if positive_count + negative_count == 0:
                sentiment = "neutral"
                score = 0.0
            else:
                score = (positive_count - negative_count) / (positive_count + negative_count)
                if score > 0.2:
                    sentiment = "positive"
                elif score < -0.2:
                    sentiment = "negative"
                else:
                    sentiment = "neutral"
            
            return {
                "sentiment": sentiment,
                "score": score,
                "positive_words": positive_count,
                "negative_words": negative_count
            }
            
        except Exception:
            return {"sentiment": "neutral", "score": 0.0}
    
```

--------------------------------------------------------------------------------

### File: generated/tools/calculate_mean.py
**Path:** `generated/tools/calculate_mean.py`
**Size:** 1,234 bytes
**Modified:** 2025-09-14 16:44:24

```python
def calculate_mean(input_data=None):
    """
    Calculate arithmetic mean of numbers.
    Returns mean value or 0 if no valid numbers.
    """

    if input_data is None:
        return 0

    try:
        # Handle different input types
        if isinstance(input_data, (int, float)):
            return float(input_data)
        elif isinstance(input_data, list):
            numbers = input_data
        elif isinstance(input_data, dict):
            # Try to extract numbers from dict
            if "numbers" in input_data:
                numbers = input_data["numbers"]
            elif "data" in input_data:
                numbers = input_data["data"]
            else:
                return 0
        else:
            return 0

        # Filter valid numbers
        valid_numbers = []
        for item in numbers:
            try:
                num = float(item)
                if not (num != num):  # Check for NaN
                    valid_numbers.append(num)
            except (TypeError, ValueError):
                continue

        # Calculate mean
        if valid_numbers:
            return sum(valid_numbers) / len(valid_numbers)
        else:
            return 0

    except Exception:
        return 0

```

--------------------------------------------------------------------------------

### File: generated/tools/extract_emails.py
**Path:** `generated/tools/extract_emails.py`
**Size:** 945 bytes
**Modified:** 2025-09-14 16:44:26

```python
def extract_emails(input_data=None):
    """
    Extract all email addresses from input text.
    Returns list of unique email addresses found.
    """
    import re

    if input_data is None:
        return []

    try:
        # Handle different input types
        if isinstance(input_data, str):
            text = input_data
        elif isinstance(input_data, dict):
            text = str(input_data.get("text", input_data.get("content", input_data)))
        elif isinstance(input_data, list):
            text = " ".join(str(item) for item in input_data)
        else:
            text = str(input_data)

        # Email regex pattern
        email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

        # Find all emails
        emails = re.findall(email_pattern, text)

        # Return unique emails (lowercase)
        return list(set(email.lower() for email in emails))

    except Exception:
        return []

```

--------------------------------------------------------------------------------

### File: generated/tools/extract_phones.py
**Path:** `generated/tools/extract_phones.py`
**Size:** 1,225 bytes
**Modified:** 2025-09-14 16:44:31

```python
def extract_phones(input_data=None):
        """Extract phone numbers from text."""
        import re
        
        if input_data is None:
            return []
        
        try:
            text = str(input_data)
            if isinstance(input_data, dict):
                text = ' '.join(str(v) for v in input_data.values())
            
            # Multiple phone patterns
            patterns = [
                r'\+?1?\s*\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}',  # US format
                r'\(\d{3}\)\s*\d{3}-\d{4}',  # (555) 555-5555
                r'\d{3}-\d{3}-\d{4}',  # 555-555-5555
                r'\d{10}',  # 5555555555
            ]
            
            phones = []
            for pattern in patterns:
                matches = re.findall(pattern, text)
                phones.extend(matches)
            
            # Clean and format
            clean_phones = []
            for phone in phones:
                # Remove non-digits for comparison
                digits = re.sub(r'\D', '', phone)
                if len(digits) >= 10:
                    clean_phones.append(phone)
            
            return list(set(clean_phones))
        except Exception:
            return []
    
```

--------------------------------------------------------------------------------

### File: generated/tools/extract_urls.py
**Path:** `generated/tools/extract_urls.py`
**Size:** 846 bytes
**Modified:** 2025-09-14 16:44:33

```python
def extract_urls(input_data=None):
    """
    Extract all URLs from input text.
    Returns list of unique URLs found.
    """
    import re

    if input_data is None:
        return []

    try:
        # Handle different input types
        if isinstance(input_data, str):
            text = input_data
        elif isinstance(input_data, dict):
            text = str(input_data.get("text", input_data.get("content", input_data)))
        elif isinstance(input_data, list):
            text = " ".join(str(item) for item in input_data)
        else:
            text = str(input_data)

        # URL regex pattern
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'

        # Find all URLs
        urls = re.findall(url_pattern, text)

        # Return unique URLs
        return list(set(urls))

    except Exception:
        return []

```

--------------------------------------------------------------------------------

### File: requirements.txt
**Path:** `requirements.txt`
**Size:** 2,189 bytes
**Modified:** 2025-09-09 20:32:09

```text
annotated-types==0.7.0
anthropic==0.64.0
anyio==4.10.0
blis==1.3.0
catalogue==2.0.10
certifi==2025.8.3
cffi==1.17.1
charset-normalizer==3.4.3
click==8.2.1
cloudpathlib==0.22.0
confection==0.1.5
contourpy==1.3.3
cryptography==45.0.6
cycler==0.12.1
cymem==2.0.11
dataclasses-json==0.6.7
distro==1.9.0
et_xmlfile==2.0.0
fonttools==4.59.2
h11==0.16.0
httpcore==1.0.9
httpx==0.28.1
idna==3.10
Jinja2==3.1.6
jiter==0.10.0
joblib==1.5.2
kiwisolver==1.4.9
langcodes==3.5.0
language_data==1.3.0
marisa-trie==1.3.1
markdown-it-py==4.0.0
MarkupSafe==3.0.2
marshmallow==3.26.1
matplotlib==3.10.6
mdurl==0.1.2
murmurhash==1.0.13
mypy_extensions==1.1.0
narwhals==2.2.0
networkx==3.5
nltk==3.9.1
numpy==2.3.2
openai==1.102.0
openpyxl==3.1.5
packaging==25.0
pandas==2.3.2
pdfminer.six==20250506
pdfplumber==0.11.7
pillow==11.3.0
plotly==6.3.0
preshed==3.0.10
pycparser==2.22
pydantic==2.11.7
pydantic_core==2.33.2
Pygments==2.19.2
pyparsing==3.2.3
PyPDF2==3.0.1
pypdfium2==4.30.0
pyphen==0.17.2
python-dateutil==2.9.0.post0
python-dotenv==1.1.1
pytz==2025.2
regex==2025.8.29
reportlab==4.4.3
requests==2.32.5
rich==14.1.0
scikit-learn==1.7.1
scipy==1.16.1
seaborn==0.13.2
shellingham==1.5.4
six==1.17.0
smart_open==7.3.0.post1
sniffio==1.3.1
spacy==3.8.7
spacy-legacy==3.0.12
spacy-loggers==1.0.5
SQLAlchemy==2.0.43
srsly==2.5.1
textblob==0.19.0
textstat==0.7.10
thinc==8.3.6
threadpoolctl==3.6.0
tqdm==4.67.1
typer==0.17.3
typing-inspect==0.9.0
typing-inspection==0.4.1
typing_extensions==4.15.0
tzdata==2025.2
urllib3==2.5.0
wasabi==1.1.3
weasel==0.4.1
wordcloud==1.9.4
wrapt==1.17.3
xlrd==2.0.2

# Flask UI Requirements
# Core Flask dependencies for the web interface

# Web Framework
Flask==3.0.0
Flask-CORS==4.0.0

# WSGI Server for production
gunicorn==21.2.0

# File handling
Werkzeug==3.0.1

# Date/time utilities (already in main requirements)
python-dateutil==2.9.0.post0

# Pipeline processing dependencies
networkx>=3.0  # For dependency graph management
# asyncio-extensions  # Enhanced async support

# # Threading and concurrency
# concurrent-futures>=3.1.1  # For async Flask integration

# Optional: Enhanced JSON processing
ujson>=5.0.0  # Faster JSON processing for large pipeline data

```

--------------------------------------------------------------------------------

### File: test_current_setup.py
**Path:** `test_current_setup.py`
**Size:** 848 bytes
**Modified:** 2025-09-13 13:06:12

```python
# test_current_setup.py
import asyncio
from core.simplified_orchestrator import SimplifiedOrchestrator


async def test():
    orchestrator = SimplifiedOrchestrator()

    # Create a simple test CSV first
    import pandas as pd

    test_df = pd.DataFrame(
        {
            "Date": ["2024-01-01", "2024-01-02"],
            "Region": ["North", "South"],
            "Sales": [1000, 1500],
        }
    )
    test_df.to_csv("test_sales.csv", index=False)

    files = [
        {
            "path": "test_sales.csv",
            "original_name": "test_sales.csv",
            "type": "text/csv",
        }
    ]

    result = await orchestrator.process_request(
        user_request="Analyze this sales data and find the highest sales region",
        files=files,
    )

    print("RESPONSE:", result.get("response"))


asyncio.run(test())

```

--------------------------------------------------------------------------------

### File: test_enhanced_system.py
**Path:** `test_enhanced_system.py`
**Size:** 5,923 bytes
**Modified:** 2025-09-14 09:18:16

```python
# test_enhanced_system.py
"""
Test script for enhanced multi-agent system
Save this as test_enhanced_system.py in your root directory
"""

import asyncio
import os
from core.simplified_orchestrator import SimplifiedOrchestrator


async def test_specialized_agents():
    """Test individual specialized agents"""
    print("=" * 60)
    print("TESTING SPECIALIZED AGENTS")
    print("=" * 60)

    orchestrator = SimplifiedOrchestrator()

    # Test 1: Text Processing
    print("\n🔍 Test 1: Text Processing Agent")
    result = await orchestrator.process_request(
        "Extract all email addresses from this text: Contact support@company.com or sales@business.org for help"
    )
    print(f"Status: {result.get('status')}")
    print(f"Response: {result.get('response', 'No response')[:200]}...")
    print(f"Workflow Type: {result.get('metadata', {}).get('workflow_type')}")

    # Test 2: Data Analysis (if you have test_sales.csv)
    if os.path.exists("test_sales.csv"):
        print("\n📊 Test 2: Data Analysis Agent")
        files = [
            {
                "path": "test_sales.csv",
                "original_name": "test_sales.csv",
                "type": "text/csv",
            }
        ]

        result = await orchestrator.process_request(
            "Analyze the sales data and show trends", files=files
        )
        print(f"Status: {result.get('status')}")
        print(f"Response: {result.get('response', 'No response')[:200]}...")
        print(f"Workflow Type: {result.get('metadata', {}).get('workflow_type')}")

    print("\n" + "=" * 60)


async def test_multi_agent_workflows():
    """Test multi-agent workflows"""
    print("TESTING MULTI-AGENT WORKFLOWS")
    print("=" * 60)

    orchestrator = SimplifiedOrchestrator()

    # Test 1: Sequential Multi-Agent Workflow
    print("\n🔄 Test 1: Multi-Agent Sequential Workflow")

    if os.path.exists("test_sales.csv"):
        files = [
            {
                "path": "test_sales.csv",
                "original_name": "test_sales.csv",
                "type": "text/csv",
            }
        ]

        result = await orchestrator.process_request(
            "Analyze the sales data and create a visualization chart showing the trends",
            files=files,
        )

        print(f"Status: {result.get('status')}")
        print(f"Response: {result.get('response', 'No response')[:300]}...")
        print(f"Workflow Type: {result.get('metadata', {}).get('workflow_type')}")
        print(f"Agents Used: {result.get('metadata', {}).get('agents_used', 0)}")
        print(
            f"Execution Strategy: {result.get('metadata', {}).get('execution_strategy')}"
        )

        if result.get("workflow_summary"):
            print(f"Workflow Summary: {result['workflow_summary']}")

    # Test 2: Complex Request Requiring Multiple Steps
    print("\n🔄 Test 2: Complex Multi-Step Request")
    result = await orchestrator.process_request(
        "Process this text to extract key information, analyze sentiment, and generate insights: 'Our Q4 sales exceeded expectations with strong growth in the North region. Customer feedback has been overwhelmingly positive, particularly for our new product line. However, we need to address supply chain challenges in the South region to maintain momentum.'"
    )

    print(f"Status: {result.get('status')}")
    print(f"Response: {result.get('response', 'No response')[:300]}...")
    print(f"Workflow Type: {result.get('metadata', {}).get('workflow_type')}")

    print("\n" + "=" * 60)


async def test_workflow_intelligence():
    """Test intelligent workflow planning"""
    print("TESTING WORKFLOW INTELLIGENCE")
    print("=" * 60)

    orchestrator = SimplifiedOrchestrator()

    # Test different request types to see how the planner responds
    test_cases = [
        "What is 2+2?",  # Should use simple workflow
        "Extract emails from: contact@company.com, support@help.org",  # Should use text_processor
        "Analyze sales data and create charts",  # Should use multi-agent workflow
        "Process document and extract key insights",  # Should determine based on file type
    ]

    for i, request in enumerate(test_cases, 1):
        print(f"\n🧠 Test Case {i}: '{request}'")

        # Test with CSV file if available
        files = None
        if "data" in request.lower() and os.path.exists("test_sales.csv"):
            files = [
                {
                    "path": "test_sales.csv",
                    "original_name": "test_sales.csv",
                    "type": "text/csv",
                }
            ]

        result = await orchestrator.process_request(request, files=files)

        workflow_plan = result.get("workflow", {})
        agents = (
            workflow_plan.get("agents", []) if isinstance(workflow_plan, dict) else []
        )

        print(f"   Agents Selected: {agents}")
        print(
            f"   Workflow Type: {result.get('metadata', {}).get('workflow_type', 'unknown')}"
        )
        print(f"   Status: {result.get('status')}")
        print(f"   Response Preview: {result.get('response', 'No response')[:100]}...")

    print("\n" + "=" * 60)


async def main():
    """Run all tests"""
    try:
        await test_specialized_agents()
        await test_multi_agent_workflows()
        await test_workflow_intelligence()

        print("✅ ALL TESTS COMPLETED")
        print("\nKey capabilities demonstrated:")
        print("- Specialized agents for different data types")
        print("- Multi-agent workflows with sequential processing")
        print("- Intelligent workflow planning based on request analysis")
        print("- Data flow between agents in complex workflows")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())

```

--------------------------------------------------------------------------------

### File: test_orchestrator.py
**Path:** `test_orchestrator.py`
**Size:** 635 bytes
**Modified:** 2025-09-13 13:26:54

```python
# test_fix.py
import asyncio
from core.simplified_orchestrator import SimplifiedOrchestrator


async def test():
    try:
        orchestrator = SimplifiedOrchestrator()
        print("✓ Orchestrator initialized successfully")

        # Test simple request
        result = await orchestrator.process_request(
            user_request="What is 2+2?", files=None
        )

        print(f"Result status: {result.get('status')}")
        print(f"Response: {result.get('response', 'No response')}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()


asyncio.run(test())

```

--------------------------------------------------------------------------------

### File: tools.json
**Path:** `tools.json`
**Size:** 4,646 bytes
**Modified:** 2025-09-12 18:40:22

```json
{
  "tools": {
    "read_text": {
      "name": "read_text",
      "description": "Read text file and return contents",
      "signature": "def read_text(input_data=None)",
      "location": "prebuilt/tools/read_text.py",
      "is_prebuilt": true,
      "is_pure_function": false,
      "used_by_agents": [],
      "created_by": "system",
      "created_at": "2025-01-01T00:00:00",
      "tags": ["file", "reader"],
      "line_count": 35,
      "status": "active",
      "used_by": [],
      "formatted_created_at": "2025-01-01 00:00:00"
    },
    "read_json": {
      "name": "read_json",
      "description": "Read JSON file and parse contents",
      "signature": "def read_json(input_data=None)",
      "location": "prebuilt/tools/read_json.py",
      "is_prebuilt": true,
      "is_pure_function": false,
      "used_by_agents": [],
      "created_by": "system",
      "created_at": "2025-01-01T00:00:00",
      "tags": ["file", "reader", "json"],
      "line_count": 38,
      "status": "active",
      "used_by": [],
      "formatted_created_at": "2025-01-01 00:00:00"
    },
    "read_csv": {
      "name": "read_csv",
      "description": "Read CSV file using pandas",
      "signature": "def read_csv(input_data=None)",
      "location": "prebuilt/tools/read_csv.py",
      "is_prebuilt": true,
      "is_pure_function": false,
      "used_by_agents": [],
      "created_by": "system",
      "created_at": "2025-01-01T00:00:00",
      "tags": ["file", "reader", "csv"],
      "line_count": 37,
      "status": "active",
      "used_by": [],
      "formatted_created_at": "2025-01-01 00:00:00"
    },
    "read_pdf": {
      "name": "read_pdf",
      "description": "Read PDF file and extract text using PyPDF2",
      "signature": "def read_pdf(input_data=None)",
      "location": "prebuilt/tools/read_pdf.py",
      "is_prebuilt": true,
      "is_pure_function": false,
      "used_by_agents": [],
      "created_by": "system",
      "created_at": "2025-01-01T00:00:00",
      "tags": ["file", "reader", "pdf"],
      "line_count": 42,
      "status": "active",
      "used_by": [],
      "formatted_created_at": "2025-01-01 00:00:00"
    },
    "extract_emails": {
      "name": "extract_emails",
      "description": "Extract all email addresses from input text",
      "signature": "def extract_emails(input_data=None)",
      "location": "generated/tools/extract_emails.py",
      "is_prebuilt": false,
      "is_pure_function": true,
      "used_by_agents": ["email_extractor", "text_analyzer"],
      "created_by": "claude-3-haiku-20240307",
      "created_at": "2025-01-01T00:00:00",
      "tags": ["extraction", "regex", "email"],
      "line_count": 28,
      "status": "active",
      "used_by": ["email_extractor", "text_analyzer"],
      "formatted_created_at": "2025-01-01 00:00:00"
    },
    "calculate_mean": {
      "name": "calculate_mean",
      "description": "Calculate arithmetic mean of numbers",
      "signature": "def calculate_mean(input_data=None)",
      "location": "generated/tools/calculate_mean.py",
      "is_prebuilt": false,
      "is_pure_function": true,
      "used_by_agents": [],
      "created_by": "claude-3-haiku-20240307",
      "created_at": "2025-01-01T00:00:00",
      "tags": ["calculation", "math", "statistics"],
      "line_count": 39,
      "status": "active",
      "used_by": [],
      "formatted_created_at": "2025-01-01 00:00:00"
    },
    "extract_phones": {
      "name": "extract_phones",
      "description": "Extract phone numbers from text",
      "signature": "def extract_phones(input_data=None)",
      "location": "/Users/sayantankundu/Documents/Agent Fabric/generated/tools/extract_phones.py",
      "is_prebuilt": false,
      "is_pure_function": true,
      "used_by_agents": [],
      "created_by": "claude-3-haiku-20240307",
      "created_at": "2025-09-04T23:14:54.570979",
      "tags": ["extraction"],
      "line_count": 37,
      "status": "active",
      "used_by": [],
      "formatted_created_at": "2025-09-04 23:14:54"
    },
    "analyze_sentiment": {
      "name": "analyze_sentiment",
      "description": "Analyze sentiment of text",
      "signature": "def analyze_sentiment(input_data=None)",
      "location": "/Users/sayantankundu/Documents/Agent Fabric/generated/tools/analyze_sentiment.py",
      "is_prebuilt": false,
      "is_pure_function": true,
      "used_by_agents": [],
      "created_by": "claude-3-haiku-20240307",
      "created_at": "2025-09-04T23:26:14.815178",
      "tags": ["analysis"],
      "line_count": 47,
      "status": "active",
      "used_by": [],
      "formatted_created_at": "2025-09-04 23:26:14"
    }
  }
}

```

--------------------------------------------------------------------------------

### File: tools.json.lock
**Path:** `tools.json.lock`
**Size:** 0 bytes
**Modified:** 2025-09-10 07:56:48

*[Binary file or content not included]*

--------------------------------------------------------------------------------
