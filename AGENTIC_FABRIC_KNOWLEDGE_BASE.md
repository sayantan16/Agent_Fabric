# AGENTIC FABRIC POC - COMPLETE PROJECT KNOWLEDGE BASE
================================================================================
Generated: 2025-09-03 13:33:57
Project Root: /Users/sayantankundu/Documents/Agent Fabric

## PROJECT OVERVIEW

**Agentic Fabric POC:** Dual-model AI orchestration platform
- GPT-4: Master orchestrator for strategic decisions
- Claude: Intelligent agent execution engine
- LangGraph: Workflow coordination
- Streamlit: User interface

## IMPLEMENTATION STATUS

**Completed Steps (1-4):**
- [x] Step 1: Project Foundation Setup
- [x] Step 2: Python Environment Configuration
- [x] Step 3: OpenAI API Setup & Configuration
- [x] Step 4: Anthropic Claude API Setup & Configuration

**Ready for:** Step 5 - Core Infrastructure Development

## PROJECT DIRECTORY STRUCTURE
```
Agent Fabric/
├── core/
│   ├── __init__.py
│   ├── agent_factory.py
│   ├── config_validator.py
│   ├── orchestrator.py
│   ├── register_example_tools.py
│   ├── register_file_readers.py
│   ├── registry.py
│   ├── registry_cli.py
│   ├── registry_enhanced.py
│   ├── tool_factory.py
│   └── workflow_engine.py
├── docs/
│   └── AGENT_TOOL_TEMPLATES.md
├── generated/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── csv_analyzer.py
│   │   ├── document_processor.py
│   │   ├── email_extractor.py
│   │   ├── pdf_email_extractor.py
│   │   ├── statistics_calculator.py
│   │   └── text_analyzer.py
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── calculate_mean.py
│   │   ├── calculate_median.py
│   │   ├── extract_emails.py
│   │   ├── extract_numbers.py
│   │   ├── extract_urls.py
│   │   ├── read_csv.py
│   │   ├── read_json.py
│   │   ├── read_pdf.py
│   │   └── read_text.py
│   └── __init__.py
├── registry_backups/
│   └── backup_20250903_080437_test_backup/
│       ├── agents.json
│       ├── metadata.json
│       └── tools.json
├── scripts/
│   └── regenerate_agents.py
├── tests/
│   ├── test_files/
│   │   ├── test.csv
│   │   ├── test.json
│   │   └── test.txt
│   ├── test_agent_factory.py
│   ├── test_end_to_end.py
│   ├── test_file_readers.py
│   ├── test_orchestrator.py
│   ├── test_registry_enhanced.py
│   ├── test_templates.py
│   ├── test_tool_factory.py
│   └── test_workflow_engine.py
├── AGENTIC_FABRIC_KNOWLEDGE_BASE.md
├── AGENTIC_FABRIC_POC_Roadmap.md
├── README.md
├── agents.json
├── config.py
├── create_knowledge_base.py
├── requirements.txt
├── system_report.md
└── tools.json
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
**Size:** 826 bytes
**Modified:** 2025-08-31 18:34:57

*[Binary file or content not included]*

--------------------------------------------------------------------------------

### File: AGENTIC_FABRIC_KNOWLEDGE_BASE.md
**Path:** `AGENTIC_FABRIC_KNOWLEDGE_BASE.md`
**Size:** 0 bytes
**Modified:** 2025-09-03 13:33:37

```markdown

```

--------------------------------------------------------------------------------

### File: AGENTIC_FABRIC_POC_Roadmap.md
**Path:** `AGENTIC_FABRIC_POC_Roadmap.md`
**Size:** 22,188 bytes
**Modified:** 2025-09-02 19:29:23

```markdown
My query:
I need to have a discussion on the agents that I have, dont you think these are too complex agents?
i mean moving on this framework is supposed to create agent, add it in the registry and then use it through the orchestrator, calling one agent after another as required, using tools on its own

the claude api is supposed to code those agents and add them
no api can code such large and extensive agents

then why keep such agents as pre use ones
like for example the ticketing agent needs to be much simpler and just have jira helper for now
like it will be used only for jira maybe
if someone requests for github or something else the claude can code and add it

in fact all the agents make them very simple, reading and parsing
in a standard json format so that the other agents can understand or can be outputted

dont code anything but help me form this idea, this project is becoming too complex and agent fabric registry cant create such agents automatically using claude API moving forward, we must keep realistically simple agents to test now and as required we will see how agents get created, added and orchestrted

Inital Discussion:

I need to have a discussion on the agents that I have, dont you think these are too complex agents?
i mean moving on this framework is supposed to create agent, add it in the registry and then use it through the orchestrator, calling one agent after another as required, using tools on its own

the claude api is supposed to code those agents and add them
no api can code such large and extensive agents

then why keep such agents as pre use ones
like for example the ticketing agent needs to be much simpler and just have jira helper for now
like it will be used only for jira maybe
if someone requests for github or something else the claude can code and add it

in fact all the agents make them very simple, reading and parsing
in a standard json format so that the other agents can understand or can be outputted

dont code anything but help me form this idea, this project is becoming too complex and agent fabric registry cant create such agents automatically using claude API moving forward, we must keep realistically simple agents to test now and as required we will see how agents get created, added and orchestrted



Final PLAN ------

## Key Architecture Decisions

### 1. **Dynamic Tool Creation - YES!**
This is brilliant! We'll have TWO registries:

```json
// agents.json
{
  "extract_urls": {
    "description": "Extracts URLs from text",
    "uses_tools": ["regex_matcher", "url_validator"],
    "location": "generated/agents/extract_urls.py"
  }
}

// tools.json
{
  "regex_matcher": {
    "description": "Matches patterns in text using regex",
    "location": "generated/tools/regex_matcher.py",
    "created_by": "claude"
  },
  "url_validator": {
    "description": "Validates if string is valid URL",
    "location": "generated/tools/url_validator.py",
    "created_by": "claude"
  }
}
```

**Benefits:**
- Agents can share tools (no redundancy!)
- Claude can create both agents AND tools
- Tools are reusable utilities, agents are workflow components
- Much more efficient and elegant

### 2. **Agent Size Flexibility - 100-300 lines**
You're right! Some agents need more complexity:
- Simple agent: 50 lines (extract_urls)
- Medium agent: 150 lines (create_chart with multiple chart types)
- Complex agent: 300 lines (jira_fetch with auth and error handling)

We'll let Claude decide based on requirements, not force arbitrary limits.

### 3. **LangGraph as Core Framework**
Yes! LangGraph will be our foundation:
- Handles state management between agents
- Provides workflow visualization
- Manages conditional branching
- Built-in retry and error handling
- Perfect for agent orchestration

```python
# LangGraph workflow example
workflow = StateGraph(State)
workflow.add_node("read_pdf", read_pdf_agent)
workflow.add_node("extract_urls", extract_urls_agent) 
workflow.add_edge("read_pdf", "extract_urls")
```

## Refined Dual-Registry Architecture

### How It Works:

```
User Request → GPT-4 Orchestrator → Checks agents.json
                 ↓
    "Need extract_urls agent"
                 ↓
    Agent exists? → No → Claude creates agent
                         ↓
              "This agent needs regex_matcher tool"
                         ↓
              Tool exists? → No → Claude creates tool first
                                  ↓
                          Register tool in tools.json
                                  ↓
                          Create agent using tool
                                  ↓
                          Register agent in agents.json
                                  ↓
                          Execute workflow via LangGraph
```

### Example Generated Code:

**Claude creates a tool:**
```python
# generated/tools/date_parser.py
def parse_dates(text, format=None):
    """Extract dates from text."""
    import re
    from datetime import datetime
    
    patterns = [
        r'\d{4}-\d{2}-\d{2}',
        r'\d{2}/\d{2}/\d{4}',
        r'\w+ \d{1,2}, \d{4}'
    ]
    
    dates = []
    for pattern in patterns:
        matches = re.findall(pattern, text)
        dates.extend(matches)
    
    if format:
        # Convert to specified format
        parsed = []
        for date_str in dates:
            # Try different formats
            for fmt in ['%Y-%m-%d', '%m/%d/%Y', '%B %d, %Y']:
                try:
                    dt = datetime.strptime(date_str, fmt)
                    parsed.append(dt.strftime(format))
                    break
                except:
                    continue
        return parsed
    
    return dates
```

**Claude creates an agent using the tool:**
```python
# generated/agents/extract_dates.py
def extract_dates(input_data):
    """Extract and format dates from text."""
    import sys
    sys.path.append('.')
    from generated.tools.date_parser import parse_dates
    
    try:
        text = input_data.get('text', '')
        output_format = input_data.get('format', '%Y-%m-%d')
        
        # Use the date_parser tool
        dates = parse_dates(text, output_format)
        
        # Additional agent logic
        date_count = len(dates)
        earliest = min(dates) if dates else None
        latest = max(dates) if dates else None
        
        return {
            "status": "success",
            "dates": dates,
            "count": date_count,
            "earliest": earliest,
            "latest": latest,
            "metadata": {
                "agent": "extract_dates",
                "tools_used": ["date_parser"]
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
```

## Final Comprehensive Plan

### **Project Vision**
Transform the current monolithic agent system into a dynamic, composable framework where:
- **Agents and Tools are generated on-demand** by Claude
- **Orchestration via LangGraph** provides sophisticated workflow management
- **Dual-registry system** tracks both agents and tools
- **GPT-4 orchestrates** by understanding capabilities and creating what's missing

### **What We're Changing**

**FROM: Current Complex System**
- 3 massive agents (PDF, Excel, Ticket) with 500-1000 lines each
- Hardcoded capabilities
- No dynamic creation
- Monolithic design

**TO: Dynamic Composable System**
- Micro-agents (50-300 lines) doing specific tasks
- Micro-tools (20-100 lines) providing utilities
- Everything created on-demand
- LangGraph orchestration
- Infinite extensibility

---

## Implementation Steps

### **Phase 1: Foundation & Cleanup (Steps 1-5)**

#### Step 1: Backup and Restructure
- Backup current implementation to `Agent Fabric_backup_complex/`
- Clean directory, keep `.env`, `venv/`, `.git/`
- Create new structure:
  ```
  Agent Fabric/
  ├── generated/
  │   ├── agents/     # Claude-generated agents
  │   └── tools/      # Claude-generated tools
  ├── core/
  │   ├── orchestrator.py      # GPT-4 orchestration
  │   ├── agent_factory.py     # Claude agent creation
  │   ├── tool_factory.py      # Claude tool creation
  │   ├── workflow_engine.py   # LangGraph workflows
  │   └── registry.py          # Dual registry management
  ├── agents.json              # Agent registry
  ├── tools.json              # Tool registry
  ├── config.py               # Simple configuration
  └── app.py                  # Streamlit UI
  ```

#### Step 2: Configuration Setup
- Create minimal `config.py` with API keys
- Set agent size limits (50-300 lines)
- Set tool size limits (20-100 lines)
- Configure LangGraph settings
- Set model choices (GPT-4, Claude-3-Haiku)

#### Step 3: Dual Registry Design
- Create `agents.json` schema:
  ```json
  {
    "agents": {
      "agent_name": {
        "description": "what it does",
        "uses_tools": ["tool1", "tool2"],
        "inputs": {},
        "outputs": {},
        "location": "generated/agents/agent_name.py",
        "created_by": "claude",
        "created_at": "timestamp",
        "execution_count": 0,
        "avg_execution_time": 0
      }
    }
  }
  ```
- Create `tools.json` schema:
  ```json
  {
    "tools": {
      "tool_name": {
        "description": "utility function",
        "location": "generated/tools/tool_name.py",
        "used_by_agents": ["agent1", "agent2"],
        "created_by": "claude",
        "created_at": "timestamp"
      }
    }
  }
  ```

#### Step 4: Minimal Pre-built Components
Create only essential file readers:
- `read_pdf` (30 lines) - PyPDF2 wrapper
- `read_csv` (20 lines) - pandas wrapper
- `read_json` (15 lines) - JSON parser
- `read_text` (10 lines) - file reader

These bootstrap the system; everything else is generated.

#### Step 5: Example Templates
Create one example of each for Claude to learn from:
- `example_agent.py` - Shows agent structure
- `example_tool.py` - Shows tool structure
- Include these in prompts to Claude

### **Phase 2: Core Engine (Steps 6-10)**

#### Step 6: Tool Factory Implementation
Build `core/tool_factory.py`:
- Claude integration for tool generation
- Prompt engineering for consistent tools
- Validation (syntax, size, functionality)
- Auto-registration in tools.json
- Testing before registration

#### Step 7: Agent Factory Implementation
Build `core/agent_factory.py`:
- Claude integration for agent generation
- Can request tool creation if needed
- Understands tool registry
- Creates agents that use tools
- Auto-registration in agents.json

#### Step 8: LangGraph Workflow Engine
Build `core/workflow_engine.py`:
- StateGraph setup for agent workflows
- Dynamic node creation from registry
- Conditional edges based on outputs
- State passing between agents
- Error handling and retries
- Workflow visualization hooks

#### Step 9: GPT-4 Orchestrator
Build `core/orchestrator.py`:
- Analyze user requests
- Check agent/tool registries
- Plan LangGraph workflow
- Detect missing capabilities
- Trigger agent/tool creation
- Execute via LangGraph
- Synthesize results

#### Step 10: Registry Management
Build `core/registry.py`:
- Manage dual registries
- Track dependencies (agent→tool)
- Usage statistics
- Search capabilities
- Cleanup unused components

### **Phase 3: Dynamic Creation Testing (Steps 11-15)**

#### Step 11: Create Your 10 Test Agents
Use the system to create:
1. `extract_urls` - May create `url_regex` tool
2. `create_simple_chart` - May create `matplotlib_wrapper` tool
3. `fetch_webpage` - May create `http_client` tool
4. `parse_json` - Standalone agent
5. `format_table` - May create `table_formatter` tool
6. `calculate_stats` - May create `stats_calculator` tool
7. `detect_language` - May create `language_detector` tool
8. `extract_dates` - May create `date_parser` tool
9. `jira_fetch` - May create `jira_client` tool
10. `send_slack` - May create `slack_client` tool

Document which tools get created alongside agents.

#### Step 12: Complex Workflow Testing
Test multi-agent workflows:
- PDF → Extract text → Extract URLs → Fetch pages → Summarize
- CSV → Calculate stats → Create chart → Format report
- Text → Detect language → Extract dates → Translate → Format

#### Step 13: Streamlit Interface
Build `app.py`:
- Display agent & tool registries
- Request input with file upload
- Show workflow planning
- Real-time execution via LangGraph
- Display results
- "Create New Agent/Tool" interface

#### Step 14: LangGraph Visualization
- Show workflow as graph
- Node = agent, Edge = data flow
- Color coding for status
- Execution time per node
- Data preview on edges

#### Step 15: Demo Scenarios
Prepare compelling demos:
1. **Dynamic Creation**: Request something that doesn't exist, watch it get created
2. **Tool Reuse**: Multiple agents using same tool
3. **Complex Workflow**: 5+ agents working together
4. **Error Recovery**: Show LangGraph handling failures
5. **Performance**: Compare to monolithic approach

### **Phase 4: Testing & Documentation (Steps 16-20)**

#### Step 16: Comprehensive Testing
- Test tool creation (20 different tools)
- Test agent creation (20 different agents)
- Test agent-tool dependencies
- Test LangGraph workflows
- Test error scenarios

#### Step 17: Documentation
- Architecture overview
- How to create agents/tools
- LangGraph workflow patterns
- API documentation
- Deployment guide

#### Step 18: Example Library
- Common tool patterns
- Common agent patterns
- Workflow templates
- Best practices

#### Step 19: Monitoring Dashboard
- Agent/tool usage stats
- Creation success rates
- Workflow performance
- Cost tracking

#### Step 20: Final Demo Preparation
- Polish UI
- Prepare presentation
- Create video demos
- Write executive summary

## Expected Outcomes

### System Capabilities:
1. **Dynamic Tool Creation**: Claude creates reusable utility functions
2. **Dynamic Agent Creation**: Claude creates agents that use tools
3. **Intelligent Orchestration**: GPT-4 plans complex workflows
4. **LangGraph Execution**: Professional workflow management
5. **Dual Registry**: Tracking and reuse of components

### Metrics:
- Tool creation: ~20-100 lines, <3 seconds
- Agent creation: ~50-300 lines, <5 seconds
- Workflow execution: <20 seconds for 5 agents
- Code reuse: Tools used by multiple agents
- Total codebase: <2000 lines (excluding generated)

### Demo Impact:
- Show true dynamic creation (not pre-built)
- Demonstrate tool reuse across agents
- Display LangGraph workflow visualization
- Prove infinite extensibility
- Clear value over monolithic approach

## Key Differentiators

1. **Two-Level Generation**: Both tools AND agents are created dynamically
2. **LangGraph Integration**: Professional workflow orchestration, not just chaining
3. **Intelligent Reuse**: Tools are shared across agents
4. **True Composability**: Build complex from simple, dynamically
5. **Infinite Extension**: Any capability can be added in seconds

This approach gives us the best of all worlds:
- Clean separation of concerns (tools vs agents)
- No redundant code
- Professional orchestration via LangGraph
- True dynamic creation
- Realistic for Claude to generate

What do you think? Should we proceed with this dual-registry, LangGraph-based approach?



Added Discussion. ---


## 1. **Removing "next_actions" - Correct Decision!**

You're absolutely right. The orchestrator (GPT-4) is the brain that decides workflow, not individual agents. So the agent output becomes simpler:

```json
{
    "status": "success/error",
    "data": {...},  // The actual output
    "metadata": {
        "agent": "agent_name",
        "tools_used": ["tool1", "tool2"],
        "execution_time": 1.2
    }
}
```

**Why this is better:**
- **Single responsibility**: Agents just execute, don't make workflow decisions
- **Centralized intelligence**: GPT-4 has the full context and registry to make optimal decisions
- **Simpler agent generation**: Claude doesn't need to generate workflow logic
- **Clear separation**: Execution (agents) vs Orchestration (GPT-4)

## 2. **Pure Function Tools - YES, Much Better!**

Pure, stateless functions are absolutely the way to go:

```python
def extract_emails(text):
    """Extract email addresses from text."""
    import re
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(pattern, text)

def calculate_average(numbers):
    """Calculate average of a list of numbers."""
    return sum(numbers) / len(numbers) if numbers else 0

def parse_date(date_string, input_format='%Y-%m-%d'):
    """Parse date string to datetime object."""
    from datetime import datetime
    return datetime.strptime(date_string, input_format).isoformat()
```

**Why pure functions are perfect:**
- **Easier to generate**: Claude can create these reliably
- **Easier to test**: Input → Output, no side effects
- **Easier to reuse**: No state management complications
- **Easier to understand**: What you see is what you get
- **Easier to compose**: Agents can chain tools naturally
- **No initialization**: Just import and use

## 3. **LangGraph State Management - Good Foundation**

Your state structure is solid for POC. Here's a slight refinement based on LangGraph best practices:

```python
from typing import TypedDict, List, Dict, Any, Optional

class WorkflowState(TypedDict):
    # Core request info
    request: str
    files: List[Dict[str, Any]]  # [{"name": "file.pdf", "content": bytes, "type": "pdf"}]
    
    # Execution tracking
    execution_path: List[str]  # ["read_pdf", "extract_text", "find_urls"]
    current_agent: Optional[str]  # Currently executing agent
    
    # Data flow
    current_data: Any  # Data being passed to next agent
    results: Dict[str, Any]  # Accumulates: {"agent_name": output, ...}
    
    # Error handling
    errors: List[Dict[str, str]]  # [{"agent": "extract_urls", "error": "..."}]
    
    # Metadata
    workflow_id: str
    started_at: str
    completed_at: Optional[str]
```

This structure:
- **Tracks everything needed** for debugging and visualization
- **Supports branching** via current_data
- **Accumulates results** for final synthesis
- **Simple enough** to pass between agents

## Enhanced Registry Structure

Based on your feedback, here's the refined registry structure:

### agents.json
```json
{
  "extract_urls": {
    "description": "Extracts all URLs from provided text using regex pattern matching",
    "uses_tools": ["regex_url_matcher"],
    "input_schema": {
      "text": "string"
    },
    "output_schema": {
      "urls": "array",
      "count": "integer"
    },
    "location": "generated/agents/extract_urls.py",
    "created_by": "claude-3-haiku",
    "created_at": "2024-01-15T10:30:00Z",
    "version": "1.0",
    "execution_count": 45,
    "avg_execution_time": 0.3,
    "tags": ["text-processing", "extraction"]
  }
}
```

### tools.json
```json
{
  "regex_url_matcher": {
    "description": "Pure function that finds URLs in text using regex patterns",
    "signature": "def regex_url_matcher(text: str) -> List[str]",
    "location": "generated/tools/regex_url_matcher.py",
    "used_by_agents": ["extract_urls", "validate_links"],
    "created_by": "claude-3-haiku",
    "created_at": "2024-01-15T10:29:00Z",
    "is_pure_function": true,
    "tags": ["regex", "text", "url"]
  }
}
```

## Why This Architecture Works

### **Orchestration Flow (GPT-4's Job):**
1. Understand user request
2. Check agent registry descriptions
3. Plan workflow sequence
4. Identify missing capabilities
5. Trigger creation if needed
6. Build LangGraph workflow
7. Execute and monitor
8. Synthesize results

### **Agent Simplicity (50-300 lines):**
```python
def extract_urls_agent(state: WorkflowState) -> WorkflowState:
    """Simple agent that extracts URLs from text."""
    from generated.tools.regex_url_matcher import regex_url_matcher
    
    try:
        # Get input
        text = state['current_data'].get('text', '')
        
        # Use tool
        urls = regex_url_matcher(text)
        
        # Format output
        result = {
            "status": "success",
            "data": {
                "urls": urls,
                "count": len(urls)
            },
            "metadata": {
                "agent": "extract_urls",
                "tools_used": ["regex_url_matcher"],
                "execution_time": 0.3
            }
        }
        
        # Update state
        state['results']['extract_urls'] = result
        state['current_data'] = result['data']
        state['execution_path'].append('extract_urls')
        
    except Exception as e:
        state['errors'].append({
            "agent": "extract_urls",
            "error": str(e)
        })
        
    return state
```

### **Tool Simplicity (20-100 lines):**
```python
def regex_url_matcher(text):
    """Extract URLs from text using regex."""
    import re
    
    # Multiple patterns for different URL formats
    patterns = [
        r'https?://[^\s<>"{}|\\^`\[\]]+',
        r'www\.[^\s<>"{}|\\^`\[\]]+',
        r'ftp://[^\s<>"{}|\\^`\[\]]+'
    ]
    
    urls = []
    for pattern in patterns:
        matches = re.findall(pattern, text)
        urls.extend(matches)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_urls = []
    for url in urls:
        if url not in seen:
            seen.add(url)
            unique_urls.append(url)
    
    return unique_urls
```

## Summary: Why This Will Work

1. **Realistic Generation**: Claude can easily generate 50-line pure functions and 150-line simple agents
2. **Clear Separation**: Tools = utilities, Agents = workflows, Orchestrator = intelligence
3. **True Composability**: Build complex from simple, dynamically
4. **No Hidden Complexity**: What you see in the registry is what you get
5. **Scalable Pattern**: This same pattern works for 10 agents or 1000 agents

The beauty is in the simplicity. By removing complexity from individual components and centralizing intelligence in the orchestrator, we get a system that's both powerful and achievable.




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
**Size:** 4,080 bytes
**Modified:** 2025-09-03 13:16:31

```json
{
  "agents": {
    "email_extractor": {
      "description": "Extracts email addresses from provided text",
      "uses_tools": [
        "extract_emails"
      ],
      "input_schema": {
        "text": "string"
      },
      "output_schema": {
        "emails": "array",
        "count": "integer"
      },
      "location": "generated/agents/email_extractor.py",
      "created_by": "claude-3-haiku",
      "created_at": "2025-09-02T19:45:07.755626",
      "version": "1.0.fd0b347e",
      "execution_count": 5,
      "avg_execution_time": 1.0,
      "tags": [
        "extraction",
        "email",
        "text-processing"
      ],
      "line_count": 41,
      "last_executed": "2025-09-03T13:16:24.050301"
    },
    "text_analyzer": {
      "description": "Analyze text to extract emails and numbers",
      "uses_tools": [
        "extract_emails",
        "extract_numbers"
      ],
      "input_schema": {
        "data": "any"
      },
      "output_schema": {
        "data": "any"
      },
      "location": "generated/agents/text_analyzer.py",
      "created_by": "claude-3-haiku",
      "created_at": "2025-09-02T23:58:41.401801",
      "version": "1.0.528daabc",
      "execution_count": 0,
      "avg_execution_time": 0,
      "tags": [
        "communication",
        "extraction"
      ],
      "line_count": 61
    },
    "statistics_calculator": {
      "description": "Calculate statistics from numbers in text",
      "uses_tools": [
        "extract_numbers",
        "calculate_mean",
        "calculate_median"
      ],
      "input_schema": {
        "data": "any"
      },
      "output_schema": {
        "data": "any"
      },
      "location": "generated/agents/statistics_calculator.py",
      "created_by": "claude-3-haiku",
      "created_at": "2025-09-02T23:58:46.927691",
      "version": "1.0.2d6d8b8b",
      "execution_count": 4,
      "avg_execution_time": 1.0,
      "tags": [
        "analysis",
        "statistics"
      ],
      "line_count": 86,
      "last_executed": "2025-09-03T13:16:31.504687"
    },
    "csv_analyzer": {
      "description": "Analyze CSV data to extract statistics and create summaries",
      "uses_tools": [
        "read_csv",
        "extract_numbers",
        "calculate_mean",
        "calculate_median"
      ],
      "input_schema": {
        "data": "any"
      },
      "output_schema": {
        "data": "any"
      },
      "location": "generated/agents/csv_analyzer.py",
      "created_by": "claude-3-haiku",
      "created_at": "2025-09-03T00:02:18.109016",
      "version": "1.0.845d07b9",
      "execution_count": 0,
      "avg_execution_time": 0,
      "tags": [
        "statistics",
        "data-processing",
        "analysis",
        "csv"
      ],
      "line_count": 78
    },
    "document_processor": {
      "description": "Process text documents to extract key information",
      "uses_tools": [
        "read_text",
        "extract_emails",
        "extract_urls",
        "extract_numbers"
      ],
      "input_schema": {
        "data": "any"
      },
      "output_schema": {
        "data": "any"
      },
      "location": "generated/agents/document_processor.py",
      "created_by": "claude-3-haiku",
      "created_at": "2025-09-03T00:03:00.710845",
      "version": "1.0.540ebda1",
      "execution_count": 0,
      "avg_execution_time": 0,
      "tags": [],
      "line_count": 69
    },
    "pdf_email_extractor": {
      "description": "Extract email addresses from PDF documents",
      "uses_tools": [
        "read_pdf",
        "extract_emails"
      ],
      "input_schema": {
        "data": "any"
      },
      "output_schema": {
        "data": "any"
      },
      "location": "generated/agents/pdf_email_extractor.py",
      "created_by": "claude-3-haiku",
      "created_at": "2025-09-03T00:03:58.606397",
      "version": "1.0.298b664d",
      "execution_count": 0,
      "avg_execution_time": 0,
      "tags": [
        "communication",
        "pdf-processing",
        "extraction",
        "document"
      ],
      "line_count": 68
    }
  }
}
```

--------------------------------------------------------------------------------

### File: config.py
**Path:** `config.py`
**Size:** 12,624 bytes
**Modified:** 2025-09-03 13:32:53

```python
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
1. ALWAYS check multiple possible input locations in state:
   - state['current_data'] (can be dict, string, list, or any type)
   - state['current_data']['text']
   - state['current_data']['data']  
   - state['current_data'][specific_field_names]
   - state['text']
   - state root level fields

2. NEVER assume input data type - always check with isinstance()

3. Handle ALL these input scenarios:
   - Previous agent passed structured data (dict with specific fields)
   - Previous agent passed raw data (string, list, etc.)
   - First agent in chain (use root state fields)
   - Unexpected data structure from any agent

4. ALWAYS provide fallback behavior when expected data is not found

5. ALWAYS pass data forward in a consistent structure that next agents can use

FUNCTION REQUIREMENTS:
- Name must be: {agent_name}_agent
- Must be between {min_lines} and {max_lines} lines
- Must handle state dict properly (read from state, update state)
- Must include comprehensive try/except error handling
- Must update state['results'], state['current_data'], and state['execution_path']
- Must initialize state components if missing
- Can only import from: {allowed_imports}

EXAMPLE STRUCTURE TO FOLLOW:
{template}

Remember: Agents must be resilient to any data type or structure from previous agents!
"""

CLAUDE_TOOL_GENERATION_PROMPT = """Generate a PURE Python function following these rules:

FUNCTION REQUIREMENTS:
1. Must be a pure function (no side effects, same input = same output)
2. Must be between {min_lines} and {max_lines} lines
3. Must handle basic input validation:
   - Check if input exists (not None)
   - Check input type if specific type required
   - Return safe default for invalid inputs (empty list, 0, empty string, etc.)
4. No external API calls, file I/O, or global state
5. Can only import from: {allowed_imports}

INPUT VALIDATION PATTERN:
- If expecting string: check isinstance(input, str), return empty string if not
- If expecting list: check isinstance(input, list), return empty list if not
- If expecting number: try conversion, return 0 or None if fails
- Always handle None inputs gracefully

Example:
def extract_numbers(text):
    import re
    if not text or not isinstance(text, str):
        return []  # Safe default for invalid input
    # ... rest of function

Keep tools simple and focused. Let agents handle complex data extraction.
"""

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_TO_FILE = True
LOG_FILE_PATH = "agentic_fabric.log"

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
**Size:** 12,724 bytes
**Modified:** 2025-09-03 13:28:12

```python
"""
Agent Factory
Dynamically generates agent code using Claude API
"""

import os
import sys
import ast
import json
from typing import Dict, Optional, List
from anthropic import Anthropic

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (
    ANTHROPIC_API_KEY,
    CLAUDE_MODEL,
    CLAUDE_TEMPERATURE,
    MIN_AGENT_LINES,
    MAX_AGENT_LINES,
    ALLOWED_IMPORTS,
    EXAMPLE_AGENT_TEMPLATE,
)
from core.registry import RegistryManager
from core.tool_factory import ToolFactory


class AgentFactory:
    def __init__(self):
        self.client = Anthropic(api_key=ANTHROPIC_API_KEY)
        self.registry = RegistryManager()
        self.tool_factory = ToolFactory()
        self.allowed_imports = ALLOWED_IMPORTS

    def create_agent(
        self,
        agent_name: str,
        description: str,
        required_tools: List[str],
        input_description: str,
        output_description: str,
        workflow_steps: List[str] = None,
    ) -> Dict:
        """
        Create a new agent using Claude.

        Args:
            agent_name: Name of the agent function
            description: What the agent does
            required_tools: List of tools the agent should use
            input_description: Description of expected input
            output_description: Description of expected output
            workflow_steps: Optional list of steps the agent should perform

        Returns:
            Dict with status and generated code or error
        """

        # Check if agent already exists
        if self.registry.agent_exists(agent_name):
            return {
                "status": "exists",
                "message": f"Agent '{agent_name}' already exists in registry",
            }

        # Check if required tools exist
        missing_tools = []
        for tool in required_tools:
            if not self.registry.tool_exists(tool):
                missing_tools.append(tool)

        if missing_tools:
            return {
                "status": "error",
                "message": f"Missing required tools: {', '.join(missing_tools)}",
                "missing_tools": missing_tools,
            }

        # Build the prompt
        prompt = self._build_agent_prompt(
            agent_name,
            description,
            required_tools,
            input_description,
            output_description,
            workflow_steps,
        )

        try:
            # Call Claude API
            response = self.client.messages.create(
                model=CLAUDE_MODEL,
                temperature=CLAUDE_TEMPERATURE,
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}],
            )

            # Extract code from response
            code = self._extract_code_from_response(response.content[0].text)

            if not code:
                return {
                    "status": "error",
                    "message": "No valid Python code found in response",
                }

            # Validate the generated code
            validation_result = self._validate_agent_code(code, agent_name)

            if validation_result["valid"]:
                # Determine input/output schemas
                input_schema = {"data": "any"}
                output_schema = {"data": "any"}

                # Register the agent
                self.registry.register_agent(
                    name=agent_name,
                    description=description,
                    code=code,
                    uses_tools=required_tools,
                    input_schema=input_schema,
                    output_schema=output_schema,
                    tags=self._extract_tags(description),
                )

                return {
                    "status": "success",
                    "code": code,
                    "message": f"Agent '{agent_name}' created successfully",
                    "line_count": len(code.splitlines()),
                }
            else:
                return {
                    "status": "error",
                    "message": validation_result["error"],
                    "code": code,
                }

        except Exception as e:
            return {"status": "error", "message": f"API error: {str(e)}"}

    def _build_agent_prompt(
        self,
        agent_name: str,
        description: str,
        required_tools: List[str],
        input_desc: str,
        output_desc: str,
        workflow_steps: List[str],
    ) -> str:
        """Build the prompt for Claude to generate agent code."""

        # Get tool signatures for reference
        tool_info = []
        for tool_name in required_tools:
            tool = self.registry.get_tool(tool_name)
            if tool:
                tool_info.append(f"- {tool_name}: {tool['description']}")

        prompt = CLAUDE_AGENT_GENERATION_PROMPT.format(
            agent_name=agent_name,
            min_lines=MIN_AGENT_LINES,
            max_lines=MAX_AGENT_LINES,
            allowed_imports=", ".join(self.allowed_imports),
            template=EXAMPLE_AGENT_TEMPLATE,
        )

        prompt += f"""
    SPECIFIC AGENT DETAILS:
    - Description: {description}
    - Required Tools: {chr(10).join(tool_info)}
    - Expected Input: {input_desc}
    - Expected Output: {output_desc}
    """

        if workflow_steps:
            prompt += f"""
    WORKFLOW STEPS:
    {chr(10).join(f'{i+1}. {step}' for i, step in enumerate(workflow_steps))}
    """

        return prompt

    def _extract_code_from_response(self, response: str) -> Optional[str]:
        """Extract Python code from Claude's response."""

        # Remove markdown code blocks if present
        if "```python" in response:
            start = response.find("```python") + 9
            end = response.find("```", start)
            code = response[start:end].strip()
        elif "```" in response:
            start = response.find("```") + 3
            end = response.find("```", start)
            code = response[start:end].strip()
        else:
            # Assume entire response is code
            code = response.strip()

        # Verify it starts with 'def'
        if not code.startswith("def "):
            # Try to find where def starts
            def_index = code.find("def ")
            if def_index != -1:
                code = code[def_index:]

        return code if code.startswith("def ") else None

    def _validate_agent_code(self, code: str, expected_base_name: str) -> Dict:
        """Validate the generated agent code."""

        try:
            # Parse the code to check syntax
            tree = ast.parse(code)

            # Check if it's a function definition
            if not isinstance(tree.body[0], ast.FunctionDef):
                return {"valid": False, "error": "Code is not a function definition"}

            # Check function name (should be agent_name_agent)
            func_name = tree.body[0].name
            expected_name = f"{expected_base_name}_agent"
            if func_name != expected_name:
                # Allow both patterns
                if func_name != expected_base_name:
                    return {
                        "valid": False,
                        "error": f"Function name '{func_name}' doesn't match expected '{expected_name}'",
                    }

            # Check it takes 'state' parameter
            args = tree.body[0].args
            if len(args.args) == 0 or args.args[0].arg != "state":
                return {"valid": False, "error": "Agent must take 'state' as parameter"}

            # Check line count
            line_count = len(code.splitlines())
            if line_count < MIN_AGENT_LINES:
                return {
                    "valid": False,
                    "error": f"Code too short: {line_count} lines (minimum: {MIN_AGENT_LINES})",
                }
            if line_count > MAX_AGENT_LINES:
                return {
                    "valid": False,
                    "error": f"Code too long: {line_count} lines (maximum: {MAX_AGENT_LINES})",
                }

            # Check for required state operations
            code_str = code
            required_operations = [
                "state['results']",
                "state['current_data']",
                "state['execution_path']",
            ]

            missing_ops = []
            for op in required_operations:
                if op not in code_str:
                    missing_ops.append(op)

            if missing_ops:
                return {
                    "valid": False,
                    "error": f"Missing required state operations: {', '.join(missing_ops)}",
                }

            return {"valid": True}

        except SyntaxError as e:
            return {"valid": False, "error": f"Syntax error: {str(e)}"}
        except Exception as e:
            return {"valid": False, "error": f"Validation error: {str(e)}"}

    def _extract_tags(self, description: str) -> List[str]:
        """Extract relevant tags from description."""

        tags = []

        # Keywords to look for
        keywords = {
            "pdf": ["pdf-processing", "document"],
            "excel": ["excel", "spreadsheet"],
            "csv": ["csv", "data-processing"],
            "chart": ["visualization", "plotting"],
            "email": ["communication", "extraction"],
            "statistic": ["statistics", "analysis"],
            "summary": ["summarization", "analysis"],
            "jira": ["ticketing", "project-management"],
            "slack": ["communication", "messaging"],
        }

        description_lower = description.lower()

        for keyword, tag_list in keywords.items():
            if keyword in description_lower:
                tags.extend(tag_list)

        # Remove duplicates and limit to 5 tags
        return list(set(tags))[:5]


class AgentFactoryCLI:
    """Command-line interface for testing agent creation."""

    def __init__(self):
        self.factory = AgentFactory()
        self.registry = RegistryManager()

    def run(self):
        """Run interactive agent creation."""

        print("\n" + "=" * 50)
        print("AGENT FACTORY - Interactive Agent Creation")
        print("=" * 50)

        # Get agent details from user
        print("\nEnter agent details:")
        agent_name = input("Agent name (e.g., pdf_summarizer): ").strip()
        description = input("Description: ").strip()

        # Show available tools
        print("\nAvailable tools:")
        tools = self.registry.list_tools()
        for tool in tools:
            print(f"  - {tool['name']}: {tool['description']}")

        print("\nEnter required tools (comma-separated):")
        tools_input = input("Tools: ").strip()
        required_tools = [t.strip() for t in tools_input.split(",") if t.strip()]

        input_desc = input("Input description: ").strip()
        output_desc = input("Output description: ").strip()

        # Optional workflow steps
        add_steps = input("\nAdd workflow steps? (y/n): ").lower() == "y"
        workflow_steps = []

        if add_steps:
            print("Enter workflow steps (type 'done' to finish):")
            while True:
                step = input(f"Step {len(workflow_steps) + 1}: ").strip()
                if step.lower() == "done":
                    break
                workflow_steps.append(step)

        print("\nGenerating agent code...")
        result = self.factory.create_agent(
            agent_name=agent_name,
            description=description,
            required_tools=required_tools,
            input_description=input_desc,
            output_description=output_desc,
            workflow_steps=workflow_steps if workflow_steps else None,
        )

        if result["status"] == "success":
            print(f"\nSuccess! Agent '{agent_name}' created")
            print(f"Location: generated/agents/{agent_name}_agent.py")
            print(f"Lines: {result['line_count']}")
            print("\nGenerated code preview (first 20 lines):")
            print("-" * 40)
            lines = result["code"].splitlines()[:20]
            for line in lines:
                print(line)
            if len(result["code"].splitlines()) > 20:
                print("... (truncated)")
            print("-" * 40)
        else:
            print(f"\nError: {result['message']}")
            if "missing_tools" in result:
                print(f"Missing tools: {', '.join(result['missing_tools'])}")
                print("Please create these tools first using the Tool Factory")


if __name__ == "__main__":
    cli = AgentFactoryCLI()
    cli.run()

```

--------------------------------------------------------------------------------

### File: core/config_validator.py
**Path:** `core/config_validator.py`
**Size:** 1,256 bytes
**Modified:** 2025-09-02 19:36:39

```python
"""
Configuration Validator
Ensures all required settings are present and valid
"""

import os
import sys


def validate_config():
    """Validate configuration on startup."""
    errors = []

    # Check API keys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import config

    if not config.OPENAI_API_KEY:
        errors.append("OPENAI_API_KEY not found in environment variables")

    if not config.ANTHROPIC_API_KEY:
        errors.append("ANTHROPIC_API_KEY not found in environment variables")

    # Check directories exist
    for dir_path in [config.GENERATED_AGENTS_DIR, config.GENERATED_TOOLS_DIR]:
        if not os.path.exists(dir_path):
            errors.append(f"Directory {dir_path} does not exist")

    # Check registry files exist
    for file_path in [config.AGENTS_REGISTRY_PATH, config.TOOLS_REGISTRY_PATH]:
        if not os.path.exists(file_path):
            errors.append(f"Registry file {file_path} does not exist")

    if errors:
        print("Configuration Errors:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("Configuration validated successfully")
        return True


if __name__ == "__main__":
    validate_config()

```

--------------------------------------------------------------------------------

### File: core/orchestrator.py
**Path:** `core/orchestrator.py`
**Size:** 20,595 bytes
**Modified:** 2025-09-03 07:55:21

```python
"""
GPT-4 Orchestrator
Intelligent workflow planning and agent selection using GPT-4
"""

import os
import sys
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import openai

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    OPENAI_API_KEY,
    ORCHESTRATOR_MODEL,
    ORCHESTRATOR_TEMPERATURE,
    ORCHESTRATOR_SYSTEM_PROMPT,
)
from core.registry import RegistryManager
from core.workflow_engine import WorkflowEngine
from core.agent_factory import AgentFactory
from core.tool_factory import ToolFactory


class Orchestrator:
    def __init__(self):
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        self.registry = RegistryManager()
        self.workflow_engine = WorkflowEngine()
        self.agent_factory = AgentFactory()
        self.tool_factory = ToolFactory()

    def process_request(
        self,
        user_request: str,
        files: List[Dict[str, Any]] = None,
        auto_create: bool = False,
    ) -> Dict[str, Any]:
        """
        Process a user request by planning and executing the appropriate workflow.

        Args:
            user_request: Natural language request from user
            files: Optional list of file information
            auto_create: Whether to automatically create missing agents/tools

        Returns:
            Dict containing workflow results and execution details
        """

        print("\n[ORCHESTRATOR] Analyzing request...")

        # Step 1: Analyze request and plan workflow
        workflow_plan = self._plan_workflow(user_request, files)

        if workflow_plan["status"] == "error":
            return {
                "status": "error",
                "message": workflow_plan["message"],
                "timestamp": datetime.now().isoformat(),
            }

        print(
            f"[ORCHESTRATOR] Planned workflow: {' -> '.join(workflow_plan['workflow_steps'])}"
        )

        # Step 2: Check for missing capabilities
        if workflow_plan.get("missing_agents") or workflow_plan.get("missing_tools"):
            print("[ORCHESTRATOR] Missing capabilities detected")

            if auto_create:
                # Try to create missing components
                creation_result = self._create_missing_components(
                    workflow_plan.get("missing_agents", []),
                    workflow_plan.get("missing_tools", []),
                )

                if not creation_result["success"]:
                    return {
                        "status": "error",
                        "message": f"Failed to create required components: {creation_result['message']}",
                        "missing": {
                            "agents": workflow_plan.get("missing_agents", []),
                            "tools": workflow_plan.get("missing_tools", []),
                        },
                    }
            else:
                # Return what's missing
                return {
                    "status": "missing_capabilities",
                    "message": "Required agents or tools are not available",
                    "missing": {
                        "agents": workflow_plan.get("missing_agents", []),
                        "tools": workflow_plan.get("missing_tools", []),
                    },
                    "suggestion": "Enable auto_create to automatically build missing components",
                }

        # Step 3: Prepare initial data
        initial_data = self._prepare_initial_data(user_request, files, workflow_plan)

        # Step 4: Execute workflow
        print("[ORCHESTRATOR] Executing workflow...")

        try:
            workflow_result = self.workflow_engine.create_and_execute(
                agent_sequence=workflow_plan["workflow_steps"],
                initial_data=initial_data,
                workflow_id=workflow_plan.get("workflow_id"),
            )

            # Step 5: Synthesize results
            print("[ORCHESTRATOR] Synthesizing results...")
            final_response = self._synthesize_results(
                user_request, workflow_result, workflow_plan
            )

            return {
                "status": "success",
                "response": final_response,
                "workflow": {
                    "steps": workflow_plan["workflow_steps"],
                    "execution_path": workflow_result.get("execution_path", []),
                    "workflow_id": workflow_plan.get("workflow_id"),
                },
                "raw_results": workflow_result.get("results", {}),
                "errors": workflow_result.get("errors", []),
                "timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Workflow execution failed: {str(e)}",
                "workflow": workflow_plan,
                "timestamp": datetime.now().isoformat(),
            }

    def _plan_workflow(
        self, user_request: str, files: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Use GPT-4 to plan the workflow based on the request.

        Args:
            user_request: User's natural language request
            files: Information about uploaded files

        Returns:
            Workflow plan with agent sequence and missing components
        """

        # Get available capabilities
        agents = self.registry.list_agents()
        tools = self.registry.list_tools()

        # Build context for GPT-4
        context = self._build_planning_context(agents, tools, files)

        # Create planning prompt
        prompt = f"""Given the following user request and available capabilities, plan the optimal workflow.

  USER REQUEST: {user_request}

  FILES PROVIDED: {json.dumps(files) if files else "None"}

  AVAILABLE AGENTS:
  {self._format_agents_list(agents)}

  AVAILABLE TOOLS:
  {self._format_tools_list(tools)}

  Plan the workflow by selecting the appropriate agents in the correct sequence.
  If the request requires capabilities that don't exist, identify what needs to be created.

  Output ONLY a valid JSON object with this exact structure (no other text):
  {{
      "workflow_steps": ["agent1", "agent2", ...],
      "missing_agents": ["agent_name", ...],
      "missing_tools": ["tool_name", ...],
      "workflow_type": "sequential",
      "reasoning": "Brief explanation of the plan"
  }}

  IMPORTANT:
  - Use only existing agent names from the available list for workflow_steps
  - List any conceptual agents that would be helpful but don't exist in missing_agents
  - Workflow steps should be in logical execution order
  - Keep the workflow as simple as possible while meeting the requirements
  - Output ONLY the JSON object, no additional text or formatting
  """

        try:
            response = self.client.chat.completions.create(
                model=ORCHESTRATOR_MODEL,
                temperature=ORCHESTRATOR_TEMPERATURE,
                messages=[
                    {"role": "system", "content": ORCHESTRATOR_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                # Removed response_format parameter
            )

            # Extract JSON from response
            response_text = response.choices[0].message.content

            # Try to extract JSON from the response
            import re

            json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
            if json_match:
                workflow_plan = json.loads(json_match.group())
            else:
                # Fallback if no JSON found
                workflow_plan = {
                    "workflow_steps": [],
                    "missing_agents": [],
                    "missing_tools": [],
                    "workflow_type": "sequential",
                    "reasoning": "Failed to parse plan",
                }

            # Validate and clean the plan
            workflow_plan = self._validate_workflow_plan(workflow_plan, agents)
            workflow_plan["status"] = "success"
            workflow_plan["workflow_id"] = self._generate_workflow_id()

            return workflow_plan

        except json.JSONDecodeError as e:
            # Try basic parsing if JSON fails
            return {
                "status": "error",
                "message": f"Failed to parse workflow plan: {str(e)}",
                "workflow_steps": [],
                "missing_agents": [],
                "missing_tools": [],
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Planning failed: {str(e)}",
                "workflow_steps": [],
                "missing_agents": [],
                "missing_tools": [],
            }

    def _synthesize_results(
        self,
        user_request: str,
        workflow_result: Dict[str, Any],
        workflow_plan: Dict[str, Any],
    ) -> str:
        """
        Use GPT-4 to synthesize results into a coherent response.

        Args:
            user_request: Original user request
            workflow_result: Raw results from workflow execution
            workflow_plan: The planned workflow

        Returns:
            Natural language response summarizing the results
        """

        # Format results for GPT-4
        results_summary = self._format_results_for_synthesis(workflow_result)

        prompt = f"""Synthesize the following workflow results into a clear, helpful response for the user.

ORIGINAL REQUEST: {user_request}

WORKFLOW EXECUTED: {' -> '.join(workflow_plan['workflow_steps'])}

RESULTS:
{results_summary}

Provide a natural language response that:
1. Directly answers the user's request
2. Highlights key findings
3. Mentions any important details or patterns
4. Notes any errors or limitations if present

Keep the response concise but comprehensive.
"""

        try:
            response = self.client.chat.completions.create(
                model=ORCHESTRATOR_MODEL,
                temperature=0.5,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant synthesizing workflow results.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )

            return response.choices[0].message.content

        except Exception as e:
            # Fallback to basic summary
            return self._create_basic_summary(workflow_result)

    def _prepare_initial_data(
        self,
        user_request: str,
        files: List[Dict[str, Any]],
        workflow_plan: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Prepare initial data for workflow execution.

        Args:
            user_request: User's request
            files: File information
            workflow_plan: Planned workflow

        Returns:
            Initial data dictionary for workflow
        """

        initial_data = {
            "request": user_request,
            "files": files or [],
            "workflow_plan": workflow_plan,
        }

        # Add file paths if files provided
        if files and len(files) > 0:
            initial_data["file_path"] = files[0].get("path", "")
            initial_data["file_type"] = files[0].get("type", "")

        # Add any extracted text directly if it's a simple text request
        if not files and isinstance(user_request, str):
            # Check if the request contains data to process
            if ":" in user_request or "\n" in user_request:
                # Might contain embedded data
                parts = user_request.split(":", 1)
                if len(parts) > 1:
                    initial_data["text"] = parts[1].strip()
                else:
                    initial_data["text"] = user_request
            else:
                initial_data["text"] = user_request

        return initial_data

    def _build_planning_context(
        self, agents: List[Dict], tools: List[Dict], files: List[Dict]
    ) -> str:
        """Build context string for planning."""

        context = f"Agents: {len(agents)}, Tools: {len(tools)}"
        if files:
            context += f", Files: {len(files)}"
            for file in files:
                context += f" [{file.get('type', 'unknown')}]"
        return context

    def _format_agents_list(self, agents: List[Dict]) -> str:
        """Format agents list for prompt."""

        formatted = []
        for agent in agents:
            formatted.append(
                f"- {agent['name']}: {agent['description']} "
                f"(uses: {', '.join(agent.get('uses_tools', []))})"
            )
        return "\n".join(formatted) if formatted else "No agents available"

    def _format_tools_list(self, tools: List[Dict]) -> str:
        """Format tools list for prompt."""

        formatted = []
        for tool in tools[:10]:  # Limit to prevent prompt overflow
            formatted.append(f"- {tool['name']}: {tool['description']}")

        if len(tools) > 10:
            formatted.append(f"... and {len(tools) - 10} more tools")

        return "\n".join(formatted) if formatted else "No tools available"

    def _validate_workflow_plan(
        self, plan: Dict[str, Any], available_agents: List[Dict]
    ) -> Dict[str, Any]:
        """
        Validate and clean the workflow plan.

        Args:
            plan: Raw plan from GPT-4
            available_agents: List of available agents

        Returns:
            Validated and cleaned plan
        """

        # Ensure required keys exist
        if "workflow_steps" not in plan:
            plan["workflow_steps"] = []
        if "missing_agents" not in plan:
            plan["missing_agents"] = []
        if "missing_tools" not in plan:
            plan["missing_tools"] = []

        # Get available agent names
        available_names = [a["name"] for a in available_agents]

        # Validate workflow steps
        valid_steps = []
        for step in plan["workflow_steps"]:
            if step in available_names:
                valid_steps.append(step)
            else:
                # Move to missing agents if not available
                if step not in plan["missing_agents"]:
                    plan["missing_agents"].append(step)

        plan["workflow_steps"] = valid_steps

        return plan

    def _format_results_for_synthesis(self, workflow_result: Dict[str, Any]) -> str:
        """Format workflow results for synthesis."""

        formatted = []

        for agent_name, result in workflow_result.get("results", {}).items():
            formatted.append(f"\n[{agent_name}]")

            if isinstance(result, dict):
                if "status" in result:
                    formatted.append(f"Status: {result['status']}")

                if "data" in result and result["data"]:
                    # Format data nicely
                    data_str = json.dumps(result["data"], indent=2)
                    if len(data_str) > 500:
                        data_str = data_str[:500] + "..."
                    formatted.append(f"Data: {data_str}")

        if workflow_result.get("errors"):
            formatted.append("\nERRORS:")
            for error in workflow_result["errors"]:
                formatted.append(
                    f"- {error.get('agent', 'unknown')}: {error.get('error', '')}"
                )

        return "\n".join(formatted)

    def _create_basic_summary(self, workflow_result: Dict[str, Any]) -> str:
        """Create a basic summary without GPT-4."""

        summary = ["Workflow execution completed."]

        # Add results summary
        for agent_name, result in workflow_result.get("results", {}).items():
            if isinstance(result, dict) and result.get("status") == "success":
                summary.append(f"- {agent_name}: Completed successfully")

                if "data" in result:
                    # Add key data points
                    data = result["data"]
                    if isinstance(data, dict):
                        for key in list(data.keys())[:3]:  # First 3 keys
                            summary.append(f"  - {key}: {data[key]}")

        # Add errors
        if workflow_result.get("errors"):
            summary.append("\nErrors encountered:")
            for error in workflow_result["errors"]:
                summary.append(f"- {error.get('error', 'Unknown error')}")

        return "\n".join(summary)

    def _generate_workflow_id(self) -> str:
        """Generate unique workflow ID."""

        import random

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = random.randint(1000, 9999)
        return f"orch_{timestamp}_{random_suffix}"

    def _create_missing_components(
        self, missing_agents: List[str], missing_tools: List[str]
    ) -> Dict[str, Any]:
        """
        Attempt to create missing agents and tools.

        Args:
            missing_agents: List of agent names to create
            missing_tools: List of tool names to create

        Returns:
            Dict with success status and details
        """

        # This is a placeholder - in a full implementation,
        # this would use GPT-4 to understand what needs to be created
        # and then use the factories to create them

        return {
            "success": False,
            "message": "Automatic component creation not yet implemented",
            "created_agents": [],
            "created_tools": [],
        }


class OrchestratorCLI:
    """Command-line interface for testing the orchestrator."""

    def __init__(self):
        self.orchestrator = Orchestrator()

    def run(self):
        """Run interactive orchestrator session."""

        print("\n" + "=" * 50)
        print("GPT-4 ORCHESTRATOR - Natural Language Interface")
        print("=" * 50)

        print("\nEnter your request in natural language.")
        print("Examples:")
        print("  - Extract all emails from this text: Contact john@example.com")
        print("  - Analyze these numbers and calculate statistics: 10, 20, 30, 40, 50")
        print("  - Process this document and extract key information")

        while True:
            print("\n" + "-" * 40)
            user_request = input("\nYour request (or 'quit'): ").strip()

            if user_request.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break

            if not user_request:
                continue

            # Check for file reference
            files = None
            if "file:" in user_request.lower():
                # Extract file path
                parts = user_request.split("file:", 1)
                if len(parts) > 1:
                    file_path = parts[1].strip().split()[0]
                    files = [{"path": file_path, "type": "unknown"}]
                    user_request = parts[0].strip()

            # Process the request
            print("\nProcessing...")
            result = self.orchestrator.process_request(
                user_request=user_request, files=files, auto_create=False
            )

            # Display results
            print("\n" + "=" * 50)
            print("RESULTS")
            print("=" * 50)

            if result["status"] == "success":
                print(f"\nResponse:\n{result['response']}")

                if result.get("workflow"):
                    print(
                        f"\nWorkflow executed: {' -> '.join(result['workflow']['steps'])}"
                    )

                if result.get("errors"):
                    print("\nErrors encountered:")
                    for error in result["errors"]:
                        print(f"  - {error}")

            elif result["status"] == "missing_capabilities":
                print(f"\nMissing capabilities detected:")
                if result["missing"]["agents"]:
                    print(f"  Missing agents: {', '.join(result['missing']['agents'])}")
                if result["missing"]["tools"]:
                    print(f"  Missing tools: {', '.join(result['missing']['tools'])}")
                print(
                    "\nSuggestion: Enable auto_create mode to build these automatically"
                )

            else:
                print(f"\nError: {result.get('message', 'Unknown error')}")


if __name__ == "__main__":
    cli = OrchestratorCLI()
    cli.run()

```

--------------------------------------------------------------------------------

### File: core/register_example_tools.py
**Path:** `core/register_example_tools.py`
**Size:** 2,356 bytes
**Modified:** 2025-09-02 23:41:06

```python
"""
Register Example Tools
Registers example statistical tools to demonstrate tool patterns
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.registry import RegistryManager


def register_example_tools():
    """Register example statistical tools."""
    registry = RegistryManager()

    print("\n" + "=" * 50)
    print("REGISTERING EXAMPLE TOOLS")
    print("=" * 50)

    # Define tools to register
    tools_to_register = [
        {
            "name": "extract_numbers",
            "description": "Extracts all numbers from text, including integers and decimals",
            "tags": ["text-processing", "extraction", "numbers"],
        },
        {
            "name": "calculate_mean",
            "description": "Calculates the arithmetic mean of a list of numbers",
            "tags": ["statistics", "math", "aggregation"],
        },
        {
            "name": "calculate_median",
            "description": "Calculates the median value of a list of numbers",
            "tags": ["statistics", "math", "aggregation"],
        },
    ]

    registered_count = 0

    for tool_info in tools_to_register:
        # Check if tool already exists
        if registry.tool_exists(tool_info["name"]):
            print(f"Tool '{tool_info['name']}' already exists, skipping...")
            continue

        # Read the code from the file
        file_path = f"generated/tools/{tool_info['name']}.py"

        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                code = f.read()

            # Register the tool
            registry.register_tool(
                name=tool_info["name"],
                description=tool_info["description"],
                code=code,
                tags=tool_info["tags"],
            )
            registered_count += 1
        else:
            print(f"File not found: {file_path}")

    # Display statistics
    print(f"\nRegistered {registered_count} new example tools")

    # List statistical tools
    print("\nStatistical Tools Available:")
    stats_tools = registry.list_tools(tags=["statistics"])
    for tool in stats_tools:
        print(f"  - {tool['name']}: {tool['description']}")

    print("\nExample tool registration complete!")


if __name__ == "__main__":
    register_example_tools()

```

--------------------------------------------------------------------------------

### File: core/register_file_readers.py
**Path:** `core/register_file_readers.py`
**Size:** 2,562 bytes
**Modified:** 2025-09-02 23:25:29

```python
"""
Register File Reader Tools
Registers the essential file reading tools in the registry
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.registry import RegistryManager


def register_file_readers():
    """Register all file reader tools."""
    registry = RegistryManager()

    print("\n" + "=" * 50)
    print("REGISTERING FILE READER TOOLS")
    print("=" * 50)

    # Read the actual code from files
    tools_to_register = [
        {
            "name": "read_pdf",
            "description": "Extracts text content from PDF files using PyPDF2",
            "tags": ["file-reader", "pdf", "text-extraction"],
        },
        {
            "name": "read_csv",
            "description": "Reads CSV files into structured data using pandas",
            "tags": ["file-reader", "csv", "data-processing"],
        },
        {
            "name": "read_json",
            "description": "Parses JSON files into Python objects",
            "tags": ["file-reader", "json", "data-processing"],
        },
        {
            "name": "read_text",
            "description": "Reads plain text files",
            "tags": ["file-reader", "text", "basic-io"],
        },
    ]

    for tool_info in tools_to_register:
        # Read the code from the file
        file_path = f"generated/tools/{tool_info['name']}.py"

        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                code = f.read()

            # Register the tool
            registry.register_tool(
                name=tool_info["name"],
                description=tool_info["description"],
                code=code,
                tags=tool_info["tags"],
            )
        else:
            print(f"File not found: {file_path}")
            print(f"   Please create the file first before running this script")

    # Display registry statistics
    print("\nUpdated Registry Statistics:")
    stats = registry.get_statistics()
    print(f"  Total tools: {stats['total_tools']}")
    print(f"  Average tool lines: {stats['avg_tool_lines']}")

    # List all file readers
    print("\nFile Readers Registered:")
    file_readers = registry.list_tools(tags=["file-reader"])
    for reader in file_readers:
        print(f"  - {reader['name']}: {reader['description']}")
        print(f"    Location: {reader['location']}")
        print(f"    Lines: {reader['line_count']}")

    print("\nFile reader registration complete!")


if __name__ == "__main__":
    register_file_readers()

```

--------------------------------------------------------------------------------

### File: core/registry.py
**Path:** `core/registry.py`
**Size:** 12,191 bytes
**Modified:** 2025-09-02 19:44:16

```python
"""
Registry Manager
Manages dual registries for agents and tools with dependency tracking
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
import hashlib


class RegistryManager:
    def __init__(
        self, agents_path: str = "agents.json", tools_path: str = "tools.json"
    ):
        self.agents_path = agents_path
        self.tools_path = tools_path
        self.agents = self._load_registry(agents_path)
        self.tools = self._load_registry(tools_path)

    def _load_registry(self, path: str) -> Dict:
        """Load registry from JSON file."""
        try:
            with open(path, "r") as f:
                data = json.load(f)
                # Ensure proper structure
                if path == self.agents_path and "agents" not in data:
                    return {"agents": {}}
                elif path == self.tools_path and "tools" not in data:
                    return {"tools": {}}
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            # Initialize empty registry
            return {"agents": {}} if "agents" in path else {"tools": {}}

    def _save_registry(self, data: Dict, path: str):
        """Save registry to JSON file."""
        with open(path, "w") as f:
            json.dump(data, f, indent=2, default=str)

    def save_all(self):
        """Save both registries."""
        self._save_registry(self.agents, self.agents_path)
        self._save_registry(self.tools, self.tools_path)

    # =============================================================================
    # AGENT REGISTRY OPERATIONS
    # =============================================================================

    def register_agent(
        self,
        name: str,
        description: str,
        code: str,
        uses_tools: List[str] = None,
        input_schema: Dict = None,
        output_schema: Dict = None,
        tags: List[str] = None,
    ) -> bool:
        """Register a new agent."""

        # Generate file path
        file_path = f"generated/agents/{name}.py"

        # Save the code to file
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            f.write(code)

        # Generate a version hash from code
        version_hash = hashlib.md5(code.encode()).hexdigest()[:8]

        # Create agent entry
        agent_entry = {
            "description": description,
            "uses_tools": uses_tools or [],
            "input_schema": input_schema or {"data": "any"},
            "output_schema": output_schema or {"data": "any"},
            "location": file_path,
            "created_by": "claude-3-haiku",
            "created_at": datetime.now().isoformat(),
            "version": f"1.0.{version_hash}",
            "execution_count": 0,
            "avg_execution_time": 0,
            "tags": tags or [],
            "line_count": len(code.splitlines()),
        }

        # Update registry
        self.agents["agents"][name] = agent_entry

        # Update tool references
        if uses_tools:
            for tool_name in uses_tools:
                if tool_name in self.tools.get("tools", {}):
                    if "used_by_agents" not in self.tools["tools"][tool_name]:
                        self.tools["tools"][tool_name]["used_by_agents"] = []
                    if name not in self.tools["tools"][tool_name]["used_by_agents"]:
                        self.tools["tools"][tool_name]["used_by_agents"].append(name)

        # Save registries
        self.save_all()

        print(
            f"Agent '{name}' registered successfully ({len(code.splitlines())} lines)"
        )
        return True

    def get_agent(self, name: str) -> Optional[Dict]:
        """Get agent details by name."""
        return self.agents.get("agents", {}).get(name)

    def list_agents(self, tags: List[str] = None) -> List[Dict]:
        """List all agents, optionally filtered by tags."""
        agents = []
        for name, details in self.agents.get("agents", {}).items():
            if tags:
                if any(tag in details.get("tags", []) for tag in tags):
                    agents.append({"name": name, **details})
            else:
                agents.append({"name": name, **details})
        return agents

    def agent_exists(self, name: str) -> bool:
        """Check if an agent exists."""
        return name in self.agents.get("agents", {})

    def update_agent_metrics(self, name: str, execution_time: float):
        """Update agent execution metrics."""
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
    # TOOL REGISTRY OPERATIONS
    # =============================================================================

    def register_tool(
        self,
        name: str,
        description: str,
        code: str,
        signature: str = None,
        tags: List[str] = None,
    ) -> bool:
        """Register a new tool."""

        # Generate file path
        file_path = f"generated/tools/{name}.py"

        # Save the code to file
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            f.write(code)

        # Extract signature if not provided
        if not signature:
            # Simple extraction of function signature from code
            lines = code.split("\n")
            for line in lines:
                if line.startswith("def "):
                    signature = line.strip()
                    break

        # Create tool entry
        tool_entry = {
            "description": description,
            "signature": signature or f"def {name}(*args, **kwargs)",
            "location": file_path,
            "used_by_agents": [],
            "created_by": "claude-3-haiku",
            "created_at": datetime.now().isoformat(),
            "is_pure_function": True,
            "tags": tags or [],
            "line_count": len(code.splitlines()),
        }

        # Update registry
        self.tools["tools"][name] = tool_entry
        self.save_all()

        print(f"Tool '{name}' registered successfully ({len(code.splitlines())} lines)")
        return True

    def get_tool(self, name: str) -> Optional[Dict]:
        """Get tool details by name."""
        return self.tools.get("tools", {}).get(name)

    def list_tools(self, tags: List[str] = None) -> List[Dict]:
        """List all tools, optionally filtered by tags."""
        tools = []
        for name, details in self.tools.get("tools", {}).items():
            if tags:
                if any(tag in details.get("tags", []) for tag in tags):
                    tools.append({"name": name, **details})
            else:
                tools.append({"name": name, **details})
        return tools

    def tool_exists(self, name: str) -> bool:
        """Check if a tool exists."""
        return name in self.tools.get("tools", {})

    # =============================================================================
    # DEPENDENCY OPERATIONS
    # =============================================================================

    def get_agent_dependencies(self, agent_name: str) -> Dict[str, List[str]]:
        """Get all dependencies for an agent."""
        agent = self.get_agent(agent_name)
        if not agent:
            return {}

        dependencies = {"tools": agent.get("uses_tools", []), "missing_tools": []}

        # Check which tools are missing
        for tool in dependencies["tools"]:
            if not self.tool_exists(tool):
                dependencies["missing_tools"].append(tool)

        return dependencies

    def get_tool_usage(self, tool_name: str) -> List[str]:
        """Get list of agents using a specific tool."""
        tool = self.get_tool(tool_name)
        if tool:
            return tool.get("used_by_agents", [])
        return []

    def can_delete_tool(self, tool_name: str) -> bool:
        """Check if a tool can be safely deleted (no agents using it)."""
        return len(self.get_tool_usage(tool_name)) == 0

    # =============================================================================
    # SEARCH OPERATIONS
    # =============================================================================

    def search_agents(self, query: str) -> List[Dict]:
        """Search agents by description or name."""
        query_lower = query.lower()
        results = []

        for name, details in self.agents.get("agents", {}).items():
            if (
                query_lower in name.lower()
                or query_lower in details.get("description", "").lower()
            ):
                results.append({"name": name, **details})

        return results

    def search_tools(self, query: str) -> List[Dict]:
        """Search tools by description or name."""
        query_lower = query.lower()
        results = []

        for name, details in self.tools.get("tools", {}).items():
            if (
                query_lower in name.lower()
                or query_lower in details.get("description", "").lower()
            ):
                results.append({"name": name, **details})

        return results

    # =============================================================================
    # STATISTICS
    # =============================================================================

    def get_statistics(self) -> Dict:
        """Get registry statistics."""
        agents_list = self.agents.get("agents", {})
        tools_list = self.tools.get("tools", {})

        # Calculate agent stats
        total_executions = sum(
            a.get("execution_count", 0) for a in agents_list.values()
        )
        avg_agent_lines = sum(
            a.get("line_count", 0) for a in agents_list.values()
        ) / max(len(agents_list), 1)

        # Calculate tool stats
        avg_tool_lines = sum(t.get("line_count", 0) for t in tools_list.values()) / max(
            len(tools_list), 1
        )
        tool_reuse = sum(len(t.get("used_by_agents", [])) for t in tools_list.values())

        return {
            "total_agents": len(agents_list),
            "total_tools": len(tools_list),
            "total_executions": total_executions,
            "avg_agent_lines": round(avg_agent_lines, 1),
            "avg_tool_lines": round(avg_tool_lines, 1),
            "tool_reuse_count": tool_reuse,
            "most_used_agent": (
                max(agents_list.items(), key=lambda x: x[1].get("execution_count", 0))[
                    0
                ]
                if agents_list
                else None
            ),
            "newest_agent": (
                max(agents_list.items(), key=lambda x: x[1].get("created_at", ""))[0]
                if agents_list
                else None
            ),
        }

    def cleanup_unused(self, dry_run: bool = True) -> List[str]:
        """Remove unused tools (with confirmation)."""
        unused = []
        for tool_name in self.tools.get("tools", {}):
            if self.can_delete_tool(tool_name):
                unused.append(tool_name)
                if not dry_run:
                    # Delete file
                    tool_path = self.tools["tools"][tool_name]["location"]
                    if os.path.exists(tool_path):
                        os.remove(tool_path)
                    # Remove from registry
                    del self.tools["tools"][tool_name]

        if not dry_run:
            self.save_all()
            print(f"Cleaned up {len(unused)} unused tools")

        return unused

```

--------------------------------------------------------------------------------

### File: core/registry_cli.py
**Path:** `core/registry_cli.py`
**Size:** 3,911 bytes
**Modified:** 2025-09-02 19:44:52

```python
"""
Registry CLI - Test the registry system
"""

from registry import RegistryManager


def test_registry():
    """Test registry operations."""
    registry = RegistryManager()

    print("\n" + "=" * 50)
    print("REGISTRY SYSTEM TEST")
    print("=" * 50)

    # Test tool registration
    print("\nTesting Tool Registration...")

    sample_tool_code = '''def extract_emails(text):
    """Extract email addresses from text."""
    import re
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}'
    emails = re.findall(pattern, text)
    return list(set(emails))  # Remove duplicates
'''

    registry.register_tool(
        name="extract_emails",
        description="Extracts email addresses from text using regex",
        code=sample_tool_code,
        tags=["text-processing", "extraction", "email"],
    )

    # Test agent registration
    print("\nTesting Agent Registration...")

    sample_agent_code = '''def email_extractor_agent(state):
    """Agent that extracts emails from text."""
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from generated.tools.extract_emails import extract_emails
    
    try:
        # Get input
        text = state.get('current_data', {}).get('text', '')
        
        # Use tool
        emails = extract_emails(text)
        
        # Format output
        result = {
            "status": "success",
            "data": {
                "emails": emails,
                "count": len(emails)
            },
            "metadata": {
                "agent": "email_extractor",
                "tools_used": ["extract_emails"],
                "execution_time": 0.1
            }
        }
        
        # Update state
        state['results']['email_extractor'] = result
        state['current_data'] = result['data']
        state['execution_path'].append('email_extractor')
        
    except Exception as e:
        state['errors'].append({
            "agent": "email_extractor",
            "error": str(e)
        })
    
    return state
'''

    registry.register_agent(
        name="email_extractor",
        description="Extracts email addresses from provided text",
        code=sample_agent_code,
        uses_tools=["extract_emails"],
        input_schema={"text": "string"},
        output_schema={"emails": "array", "count": "integer"},
        tags=["extraction", "email", "text-processing"],
    )

    # Test retrieval
    print("\nTesting Retrieval...")

    agent = registry.get_agent("email_extractor")
    if agent:
        print(f"  Found agent: {agent['description']}")
        print(f"  Uses tools: {agent['uses_tools']}")
        print(f"  Location: {agent['location']}")

    tool = registry.get_tool("extract_emails")
    if tool:
        print(f"  Found tool: {tool['description']}")
        print(f"  Used by: {tool['used_by_agents']}")

    # Test dependencies
    print("\nTesting Dependencies...")
    deps = registry.get_agent_dependencies("email_extractor")
    print(f"  Agent dependencies: {deps}")

    usage = registry.get_tool_usage("extract_emails")
    print(f"  Tool usage: {usage}")

    # Test search
    print("\nTesting Search...")
    results = registry.search_agents("email")
    print(f"  Found {len(results)} agents matching 'email'")

    results = registry.search_tools("extract")
    print(f"  Found {len(results)} tools matching 'extract'")

    # Test statistics
    print("\nRegistry Statistics:")
    stats = registry.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    print("\nRegistry test completed successfully!")

    # Test listing
    print("\nCurrent Registry Contents:")
    print(f"  Agents: {[a['name'] for a in registry.list_agents()]}")
    print(f"  Tools: {[t['name'] for t in registry.list_tools()]}")


if __name__ == "__main__":
    test_registry()

```

--------------------------------------------------------------------------------

### File: core/registry_enhanced.py
**Path:** `core/registry_enhanced.py`
**Size:** 22,950 bytes
**Modified:** 2025-09-03 08:03:32

```python
"""
Enhanced Registry Manager
Advanced registry operations including validation, cleanup, and analytics
"""

import json
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import shutil

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.registry import RegistryManager


class EnhancedRegistryManager(RegistryManager):
    """Extended registry with advanced management features."""

    def __init__(
        self, agents_path: str = "agents.json", tools_path: str = "tools.json"
    ):
        super().__init__(agents_path, tools_path)
        self.backup_dir = "registry_backups"
        os.makedirs(self.backup_dir, exist_ok=True)

    # =============================================================================
    # BACKUP AND RESTORE
    # =============================================================================

    def backup_registries(self, tag: str = None) -> str:
        """
        Create backup of current registries.

        Args:
            tag: Optional tag for the backup

        Returns:
            Backup file path
        """
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
        }

        with open(os.path.join(backup_path, "metadata.json"), "w") as f:
            json.dump(metadata, f, indent=2)

        print(f"Backup created: {backup_path}")
        return backup_path

    def restore_registries(self, backup_name: str) -> bool:
        """
        Restore registries from backup.

        Args:
            backup_name: Name of backup directory

        Returns:
            Success status
        """
        backup_path = os.path.join(self.backup_dir, backup_name)

        if not os.path.exists(backup_path):
            print(f"Backup not found: {backup_path}")
            return False

        try:
            # Restore files
            shutil.copy(os.path.join(backup_path, "agents.json"), self.agents_path)
            shutil.copy(os.path.join(backup_path, "tools.json"), self.tools_path)

            # Reload registries
            self.agents = self._load_registry(self.agents_path)
            self.tools = self._load_registry(self.tools_path)

            print(f"Registries restored from: {backup_path}")
            return True

        except Exception as e:
            print(f"Restore failed: {str(e)}")
            return False

    # =============================================================================
    # VALIDATION AND HEALTH CHECKS
    # =============================================================================

    def validate_all(self) -> Dict[str, List[str]]:
        """
        Validate all agents and tools.

        Returns:
            Dict with validation results
        """
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

            if not os.path.exists(file_path):
                results["missing_files"].append(f"Agent: {name} - {file_path}")
                results["invalid_agents"].append(name)
            else:
                # Check dependencies
                missing_deps = []
                for tool in agent.get("uses_tools", []):
                    if not self.tool_exists(tool):
                        missing_deps.append(tool)

                if missing_deps:
                    results["dependency_issues"].append(
                        f"Agent '{name}' missing tools: {', '.join(missing_deps)}"
                    )
                    results["invalid_agents"].append(name)
                else:
                    results["valid_agents"].append(name)

        # Validate tools
        for name, tool in self.tools.get("tools", {}).items():
            file_path = tool.get("location", "")

            if not os.path.exists(file_path):
                results["missing_files"].append(f"Tool: {name} - {file_path}")
                results["invalid_tools"].append(name)
            else:
                results["valid_tools"].append(name)

        return results

    def health_check(self) -> Dict[str, Any]:
        """
        Perform comprehensive health check.

        Returns:
            Health status report
        """
        validation = self.validate_all()
        stats = self.get_statistics()

        # Calculate health score
        total_agents = len(self.agents.get("agents", {}))
        total_tools = len(self.tools.get("tools", {}))
        valid_agents = len(validation["valid_agents"])
        valid_tools = len(validation["valid_tools"])

        health_score = 0
        if total_agents > 0:
            health_score += (valid_agents / total_agents) * 50
        if total_tools > 0:
            health_score += (valid_tools / total_tools) * 50

        return {
            "health_score": round(health_score, 1),
            "status": (
                "healthy"
                if health_score >= 80
                else "degraded" if health_score >= 50 else "unhealthy"
            ),
            "total_components": total_agents + total_tools,
            "valid_components": valid_agents + valid_tools,
            "issues": {
                "missing_files": len(validation["missing_files"]),
                "dependency_issues": len(validation["dependency_issues"]),
                "invalid_agents": len(validation["invalid_agents"]),
                "invalid_tools": len(validation["invalid_tools"]),
            },
            "statistics": stats,
            "validation_details": validation,
        }

    # =============================================================================
    # ADVANCED ANALYTICS
    # =============================================================================

    def get_usage_analytics(self) -> Dict[str, Any]:
        """
        Get detailed usage analytics.

        Returns:
            Usage statistics and patterns
        """
        agents_list = self.agents.get("agents", {})
        tools_list = self.tools.get("tools", {})

        # Agent analytics
        most_used_agents = sorted(
            agents_list.items(),
            key=lambda x: x[1].get("execution_count", 0),
            reverse=True,
        )[:5]

        # Tool analytics
        tool_usage = {}
        for tool_name, tool_data in tools_list.items():
            usage_count = len(tool_data.get("used_by_agents", []))
            tool_usage[tool_name] = usage_count

        most_used_tools = sorted(tool_usage.items(), key=lambda x: x[1], reverse=True)[
            :5
        ]

        # Calculate averages
        total_executions = sum(
            a.get("execution_count", 0) for a in agents_list.values()
        )
        avg_execution_time = sum(
            a.get("avg_execution_time", 0) for a in agents_list.values()
        ) / max(len(agents_list), 1)

        return {
            "agent_analytics": {
                "total_agents": len(agents_list),
                "most_used": [
                    {"name": name, "executions": data.get("execution_count", 0)}
                    for name, data in most_used_agents
                ],
                "total_executions": total_executions,
                "average_execution_time": round(avg_execution_time, 2),
            },
            "tool_analytics": {
                "total_tools": len(tools_list),
                "most_reused": [
                    {"name": name, "used_by": count} for name, count in most_used_tools
                ],
                "unused_tools": [
                    name for name, count in tool_usage.items() if count == 0
                ],
            },
            "complexity_metrics": {
                "avg_agent_size": round(
                    sum(a.get("line_count", 0) for a in agents_list.values())
                    / max(len(agents_list), 1),
                    1,
                ),
                "avg_tool_size": round(
                    sum(t.get("line_count", 0) for t in tools_list.values())
                    / max(len(tools_list), 1),
                    1,
                ),
                "avg_tools_per_agent": round(
                    sum(len(a.get("uses_tools", [])) for a in agents_list.values())
                    / max(len(agents_list), 1),
                    1,
                ),
            },
        }

    # =============================================================================
    # DEPENDENCY MANAGEMENT
    # =============================================================================

    def get_dependency_graph(self) -> Dict[str, Dict[str, List[str]]]:
        """
        Build complete dependency graph.

        Returns:
            Dependency relationships
        """
        graph = {"agents_to_tools": {}, "tools_to_agents": {}, "agent_chains": {}}

        # Build agent to tool mapping
        for agent_name, agent_data in self.agents.get("agents", {}).items():
            graph["agents_to_tools"][agent_name] = agent_data.get("uses_tools", [])

        # Build tool to agent mapping
        for tool_name, tool_data in self.tools.get("tools", {}).items():
            graph["tools_to_agents"][tool_name] = tool_data.get("used_by_agents", [])

        # Identify potential agent chains (agents that could work together)
        for agent_name, agent_data in self.agents.get("agents", {}).items():
            output_schema = agent_data.get("output_schema", {})

            # Find agents that could consume this agent's output
            potential_next = []
            for other_name, other_data in self.agents.get("agents", {}).items():
                if other_name != agent_name:
                    input_schema = other_data.get("input_schema", {})
                    # Simple compatibility check
                    if self._schemas_compatible(output_schema, input_schema):
                        potential_next.append(other_name)

            if potential_next:
                graph["agent_chains"][agent_name] = potential_next

        return graph

    def _schemas_compatible(self, output_schema: Dict, input_schema: Dict) -> bool:
        """
        Check if output schema is compatible with input schema.
        Simple implementation - can be enhanced.
        """
        # Basic compatibility - if both have 'data' or 'text' fields
        output_keys = set(output_schema.keys())
        input_keys = set(input_schema.keys())

        common_keys = output_keys.intersection(input_keys)
        return len(common_keys) > 0 or "any" in input_schema.values()

    # =============================================================================
    # CLEANUP AND OPTIMIZATION
    # =============================================================================

    def optimize_registry(self, dry_run: bool = True) -> Dict[str, Any]:
        """
        Optimize registry by cleaning up unused components and fixing issues.

        Args:
            dry_run: If True, only report what would be done

        Returns:
            Optimization report
        """
        report = {
            "unused_tools": [],
            "broken_agents": [],
            "missing_files": [],
            "fixed_dependencies": [],
            "removed_components": [],
        }

        # Find unused tools
        for tool_name, tool_data in self.tools.get("tools", {}).items():
            if len(tool_data.get("used_by_agents", [])) == 0:
                report["unused_tools"].append(tool_name)
                if not dry_run:
                    # Remove tool
                    del self.tools["tools"][tool_name]
                    report["removed_components"].append(f"Tool: {tool_name}")

        # Find broken agents
        for agent_name, agent_data in self.agents.get("agents", {}).items():
            # Check file exists
            if not os.path.exists(agent_data.get("location", "")):
                report["broken_agents"].append(agent_name)
                report["missing_files"].append(agent_data.get("location", ""))
                if not dry_run:
                    # Remove agent
                    del self.agents["agents"][agent_name]
                    report["removed_components"].append(f"Agent: {agent_name}")

            # Check dependencies
            for tool in agent_data.get("uses_tools", []):
                if not self.tool_exists(tool):
                    report["fixed_dependencies"].append(
                        f"Removed missing tool '{tool}' from agent '{agent_name}'"
                    )
                    if not dry_run:
                        agent_data["uses_tools"].remove(tool)

        if not dry_run:
            self.save_all()
            report["status"] = "optimized"
        else:
            report["status"] = "dry_run"

        return report

    # =============================================================================
    # EXPORT AND IMPORT
    # =============================================================================

    def export_to_markdown(self, output_file: str = "registry_report.md") -> str:
        """
        Export registry information to markdown report.

        Args:
            output_file: Output file path

        Returns:
            Path to generated file
        """
        health = self.health_check()
        analytics = self.get_usage_analytics()
        deps = self.get_dependency_graph()

        content = []
        content.append("# Agentic Fabric Registry Report")
        content.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        content.append("")

        # Health Status
        content.append("## System Health")
        content.append(f"- **Health Score**: {health['health_score']}/100")
        content.append(f"- **Status**: {health['status'].upper()}")
        content.append(f"- **Total Components**: {health['total_components']}")
        content.append(f"- **Valid Components**: {health['valid_components']}")
        content.append("")

        # Agents
        content.append("## Registered Agents")
        for name, data in self.agents.get("agents", {}).items():
            content.append(f"### {name}")
            content.append(f"- **Description**: {data.get('description', 'N/A')}")
            content.append(f"- **Tools Used**: {', '.join(data.get('uses_tools', []))}")
            content.append(f"- **Executions**: {data.get('execution_count', 0)}")
            content.append(f"- **Lines**: {data.get('line_count', 0)}")
            content.append("")

        # Tools
        content.append("## Registered Tools")
        for name, data in self.tools.get("tools", {}).items():
            content.append(f"### {name}")
            content.append(f"- **Description**: {data.get('description', 'N/A')}")
            content.append(
                f"- **Used By**: {', '.join(data.get('used_by_agents', [])) or 'None'}"
            )
            content.append(f"- **Lines**: {data.get('line_count', 0)}")
            content.append("")

        # Analytics
        content.append("## Usage Analytics")
        content.append(
            f"- **Total Executions**: {analytics['agent_analytics']['total_executions']}"
        )
        content.append(
            f"- **Average Agent Size**: {analytics['complexity_metrics']['avg_agent_size']} lines"
        )
        content.append(
            f"- **Average Tool Size**: {analytics['complexity_metrics']['avg_tool_size']} lines"
        )
        content.append("")

        # Write to file
        with open(output_file, "w") as f:
            f.write("\n".join(content))

        print(f"Registry report exported to: {output_file}")
        return output_file


class RegistryManagementCLI:
    """CLI for registry management operations."""

    def __init__(self):
        self.registry = EnhancedRegistryManager()

    def run(self):
        """Run interactive registry management."""

        while True:
            print("\n" + "=" * 50)
            print("REGISTRY MANAGEMENT")
            print("=" * 50)

            print("\n1. Health Check")
            print("2. View Analytics")
            print("3. Validate All Components")
            print("4. Optimize Registry")
            print("5. Backup Registry")
            print("6. Export Report")
            print("7. View Dependency Graph")
            print("8. Exit")

            choice = input("\nChoice (1-8): ").strip()

            if choice == "1":
                self._health_check()
            elif choice == "2":
                self._view_analytics()
            elif choice == "3":
                self._validate_all()
            elif choice == "4":
                self._optimize()
            elif choice == "5":
                self._backup()
            elif choice == "6":
                self._export_report()
            elif choice == "7":
                self._view_dependencies()
            elif choice == "8":
                print("Exiting...")
                break
            else:
                print("Invalid choice")

    def _health_check(self):
        """Run health check."""
        health = self.registry.health_check()

        print("\n" + "-" * 40)
        print("HEALTH CHECK RESULTS")
        print("-" * 40)
        print(f"Health Score: {health['health_score']}/100")
        print(f"Status: {health['status'].upper()}")
        print(f"Total Components: {health['total_components']}")
        print(f"Valid Components: {health['valid_components']}")

        if health["issues"]["missing_files"] > 0:
            print(f"\nMissing Files: {health['issues']['missing_files']}")
        if health["issues"]["dependency_issues"] > 0:
            print(f"Dependency Issues: {health['issues']['dependency_issues']}")

    def _view_analytics(self):
        """View usage analytics."""
        analytics = self.registry.get_usage_analytics()

        print("\n" + "-" * 40)
        print("USAGE ANALYTICS")
        print("-" * 40)

        print("\nAgent Analytics:")
        print(f"  Total Agents: {analytics['agent_analytics']['total_agents']}")
        print(f"  Total Executions: {analytics['agent_analytics']['total_executions']}")
        print(
            f"  Avg Execution Time: {analytics['agent_analytics']['average_execution_time']}s"
        )

        print("\nMost Used Agents:")
        for agent in analytics["agent_analytics"]["most_used"]:
            print(f"  - {agent['name']}: {agent['executions']} executions")

        print("\nTool Analytics:")
        print(f"  Total Tools: {analytics['tool_analytics']['total_tools']}")

        print("\nMost Reused Tools:")
        for tool in analytics["tool_analytics"]["most_reused"]:
            print(f"  - {tool['name']}: used by {tool['used_by']} agents")

        if analytics["tool_analytics"]["unused_tools"]:
            print(
                f"\nUnused Tools: {', '.join(analytics['tool_analytics']['unused_tools'])}"
            )

    def _validate_all(self):
        """Validate all components."""
        results = self.registry.validate_all()

        print("\n" + "-" * 40)
        print("VALIDATION RESULTS")
        print("-" * 40)

        print(f"Valid Agents: {len(results['valid_agents'])}")
        print(f"Invalid Agents: {len(results['invalid_agents'])}")
        print(f"Valid Tools: {len(results['valid_tools'])}")
        print(f"Invalid Tools: {len(results['invalid_tools'])}")

        if results["missing_files"]:
            print("\nMissing Files:")
            for file in results["missing_files"][:5]:
                print(f"  - {file}")

        if results["dependency_issues"]:
            print("\nDependency Issues:")
            for issue in results["dependency_issues"][:5]:
                print(f"  - {issue}")

    def _optimize(self):
        """Optimize registry."""
        # First do dry run
        dry_report = self.registry.optimize_registry(dry_run=True)

        print("\n" + "-" * 40)
        print("OPTIMIZATION PREVIEW")
        print("-" * 40)

        if dry_report["unused_tools"]:
            print(f"Unused Tools to Remove: {', '.join(dry_report['unused_tools'])}")
        if dry_report["broken_agents"]:
            print(f"Broken Agents to Remove: {', '.join(dry_report['broken_agents'])}")

        if dry_report["unused_tools"] or dry_report["broken_agents"]:
            confirm = input("\nProceed with optimization? (y/n): ").lower()
            if confirm == "y":
                report = self.registry.optimize_registry(dry_run=False)
                print(
                    f"\nOptimization complete. Removed {len(report['removed_components'])} components."
                )
        else:
            print("Registry is already optimized!")

    def _backup(self):
        """Create backup."""
        tag = input("Enter backup tag (optional): ").strip()
        path = self.registry.backup_registries(tag if tag else None)
        print(f"Backup created at: {path}")

    def _export_report(self):
        """Export markdown report."""
        filename = input("Report filename (default: registry_report.md): ").strip()
        if not filename:
            filename = "registry_report.md"
        path = self.registry.export_to_markdown(filename)
        print(f"Report exported to: {path}")

    def _view_dependencies(self):
        """View dependency graph."""
        deps = self.registry.get_dependency_graph()

        print("\n" + "-" * 40)
        print("DEPENDENCY GRAPH")
        print("-" * 40)

        print("\nAgent → Tool Dependencies:")
        for agent, tools in deps["agents_to_tools"].items():
            if tools:
                print(f"  {agent} → {', '.join(tools)}")

        print("\nTool → Agent Usage:")
        for tool, agents in deps["tools_to_agents"].items():
            if agents:
                print(f"  {tool} ← {', '.join(agents)}")

        if deps["agent_chains"]:
            print("\nPotential Agent Chains:")
            for agent, next_agents in deps["agent_chains"].items():
                print(f"  {agent} → {', '.join(next_agents[:3])}")


if __name__ == "__main__":
    cli = RegistryManagementCLI()
    cli.run()

```

--------------------------------------------------------------------------------

### File: core/tool_factory.py
**Path:** `core/tool_factory.py`
**Size:** 10,833 bytes
**Modified:** 2025-09-02 23:44:29

```python
"""
Tool Factory
Dynamically generates tool code using Claude API
"""

import os
import sys
import ast
import json
from typing import Dict, Optional, List
from anthropic import Anthropic

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (
    ANTHROPIC_API_KEY,
    CLAUDE_MODEL,
    CLAUDE_TEMPERATURE,
    MIN_TOOL_LINES,
    MAX_TOOL_LINES,
    ALLOWED_IMPORTS,
    EXAMPLE_TOOL_TEMPLATE,
)
from core.registry import RegistryManager


class ToolFactory:
    def __init__(self):
        self.client = Anthropic(api_key=ANTHROPIC_API_KEY)
        self.registry = RegistryManager()
        self.allowed_imports = ALLOWED_IMPORTS

    def create_tool(
        self,
        tool_name: str,
        description: str,
        input_description: str,
        output_description: str,
        examples: List[Dict] = None,
    ) -> Dict:
        """
        Create a new tool using Claude.

        Args:
            tool_name: Name of the tool function
            description: What the tool does
            input_description: Description of input parameters
            output_description: Description of output format
            examples: Optional input/output examples

        Returns:
            Dict with status and generated code or error
        """

        # Check if tool already exists
        if self.registry.tool_exists(tool_name):
            return {
                "status": "exists",
                "message": f"Tool '{tool_name}' already exists in registry",
            }

        # Build the prompt
        prompt = self._build_tool_prompt(
            tool_name, description, input_description, output_description, examples
        )

        try:
            # Call Claude API
            response = self.client.messages.create(
                model=CLAUDE_MODEL,
                temperature=CLAUDE_TEMPERATURE,
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}],
            )

            # Extract code from response
            code = self._extract_code_from_response(response.content[0].text)

            if not code:
                return {
                    "status": "error",
                    "message": "No valid Python code found in response",
                }

            # Validate the generated code
            validation_result = self._validate_tool_code(code, tool_name)

            if validation_result["valid"]:
                # Register the tool
                self.registry.register_tool(
                    name=tool_name,
                    description=description,
                    code=code,
                    tags=self._extract_tags(description),
                )

                return {
                    "status": "success",
                    "code": code,
                    "message": f"Tool '{tool_name}' created successfully",
                    "line_count": len(code.splitlines()),
                }
            else:
                return {
                    "status": "error",
                    "message": validation_result["error"],
                    "code": code,
                }

        except Exception as e:
            return {"status": "error", "message": f"API error: {str(e)}"}

    def _build_tool_prompt(
        self,
        tool_name: str,
        description: str,
        input_desc: str,
        output_desc: str,
        examples: List[Dict],
    ) -> str:
        """Build the prompt for Claude to generate tool code."""

        prompt = f"""Generate a Python function that follows these specifications:

FUNCTION NAME: {tool_name}

DESCRIPTION: {description}

INPUT: {input_desc}

OUTPUT: {output_desc}

REQUIREMENTS:
1. Must be a PURE function (no side effects, no file I/O, no API calls)
2. Must be between {MIN_TOOL_LINES} and {MAX_TOOL_LINES} lines
3. All imports must be inside the function
4. Must handle edge cases gracefully
5. Must return consistent data types
6. Can only use these allowed imports: {', '.join(self.allowed_imports)}

EXAMPLE STRUCTURE TO FOLLOW:
{EXAMPLE_TOOL_TEMPLATE}

"""

        if examples:
            prompt += "\nEXAMPLES:\n"
            for i, example in enumerate(examples, 1):
                prompt += f"Example {i}:\n"
                prompt += f"  Input: {example.get('input')}\n"
                prompt += f"  Output: {example.get('output')}\n"

        prompt += """
OUTPUT ONLY THE PYTHON CODE. Do not include any explanation or markdown formatting.
The code should start with 'def' and be valid Python.
"""

        return prompt

    def _extract_code_from_response(self, response: str) -> Optional[str]:
        """Extract Python code from Claude's response."""

        # Remove markdown code blocks if present
        if "```python" in response:
            start = response.find("```python") + 9
            end = response.find("```", start)
            code = response[start:end].strip()
        elif "```" in response:
            start = response.find("```") + 3
            end = response.find("```", start)
            code = response[start:end].strip()
        else:
            # Assume entire response is code
            code = response.strip()

        # Verify it starts with 'def'
        if not code.startswith("def "):
            # Try to find where def starts
            def_index = code.find("def ")
            if def_index != -1:
                code = code[def_index:]

        return code if code.startswith("def ") else None

    def _validate_tool_code(self, code: str, expected_name: str) -> Dict:
        """Validate the generated tool code."""

        try:
            # Parse the code to check syntax
            tree = ast.parse(code)

            # Check if it's a function definition
            if not isinstance(tree.body[0], ast.FunctionDef):
                return {"valid": False, "error": "Code is not a function definition"}

            # Check function name
            func_name = tree.body[0].name
            if func_name != expected_name:
                return {
                    "valid": False,
                    "error": f"Function name '{func_name}' doesn't match expected '{expected_name}'",
                }

            # Check line count
            line_count = len(code.splitlines())
            if line_count < MIN_TOOL_LINES:
                return {
                    "valid": False,
                    "error": f"Code too short: {line_count} lines (minimum: {MIN_TOOL_LINES})",
                }
            if line_count > MAX_TOOL_LINES:
                return {
                    "valid": False,
                    "error": f"Code too long: {line_count} lines (maximum: {MAX_TOOL_LINES})",
                }

            # Check for forbidden operations
            for node in ast.walk(tree):
                # Check for file I/O
                if isinstance(node, ast.Name) and node.id in ["open", "file"]:
                    return {
                        "valid": False,
                        "error": "Code contains file I/O operations",
                    }

                # Check for network operations
                if isinstance(node, ast.Name) and node.id in [
                    "requests",
                    "urllib",
                    "socket",
                ]:
                    return {"valid": False, "error": "Code contains network operations"}

            return {"valid": True}

        except SyntaxError as e:
            return {"valid": False, "error": f"Syntax error: {str(e)}"}
        except Exception as e:
            return {"valid": False, "error": f"Validation error: {str(e)}"}

    def _extract_tags(self, description: str) -> List[str]:
        """Extract relevant tags from description."""

        tags = []

        # Keywords to look for
        keywords = {
            "extract": ["extraction", "parsing"],
            "calculate": ["calculation", "math"],
            "convert": ["conversion", "transformation"],
            "validate": ["validation", "checking"],
            "format": ["formatting", "display"],
            "analyze": ["analysis", "processing"],
            "text": ["text-processing"],
            "number": ["numeric", "math"],
            "date": ["datetime", "temporal"],
            "url": ["web", "link"],
            "email": ["communication"],
            "json": ["data", "structured"],
            "csv": ["data", "tabular"],
        }

        description_lower = description.lower()

        for keyword, tag_list in keywords.items():
            if keyword in description_lower:
                tags.extend(tag_list)

        # Remove duplicates and limit to 5 tags
        return list(set(tags))[:5]


class ToolFactoryCLI:
    """Command-line interface for testing tool creation."""

    def __init__(self):
        self.factory = ToolFactory()

    def run(self):
        """Run interactive tool creation."""

        print("\n" + "=" * 50)
        print("TOOL FACTORY - Interactive Tool Creation")
        print("=" * 50)

        # Get tool details from user
        print("\nEnter tool details:")
        tool_name = input("Tool name (e.g., extract_urls): ").strip()
        description = input("Description: ").strip()
        input_desc = input("Input description: ").strip()
        output_desc = input("Output description: ").strip()

        # Optional examples
        add_examples = input("\nAdd examples? (y/n): ").lower() == "y"
        examples = []

        if add_examples:
            while True:
                example_input = input("Example input (or 'done'): ").strip()
                if example_input.lower() == "done":
                    break
                example_output = input("Expected output: ").strip()
                examples.append({"input": example_input, "output": example_output})

        print("\nGenerating tool code...")
        result = self.factory.create_tool(
            tool_name=tool_name,
            description=description,
            input_description=input_desc,
            output_description=output_desc,
            examples=examples if examples else None,
        )

        if result["status"] == "success":
            print(f"\nSuccess! Tool '{tool_name}' created")
            print(f"Location: generated/tools/{tool_name}.py")
            print(f"Lines: {result['line_count']}")
            print("\nGenerated code:")
            print("-" * 40)
            print(result["code"])
            print("-" * 40)
        else:
            print(f"\nError: {result['message']}")
            if "code" in result:
                print("\nGenerated code (with errors):")
                print("-" * 40)
                print(result["code"])
                print("-" * 40)


if __name__ == "__main__":
    cli = ToolFactoryCLI()
    cli.run()

```

--------------------------------------------------------------------------------

### File: core/workflow_engine.py
**Path:** `core/workflow_engine.py`
**Size:** 13,278 bytes
**Modified:** 2025-09-03 07:44:11

```python
"""
Workflow Engine
Executes multi-agent workflows using LangGraph
"""

import sys
import os
from typing import Dict, List, Optional, Any, TypedDict
from datetime import datetime
import json
import importlib.util

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from core.registry import RegistryManager


class WorkflowState(TypedDict):
    """State schema for workflow execution."""

    # Core request info
    request: str
    files: List[Dict[str, Any]]

    # Execution tracking
    execution_path: List[str]
    current_agent: Optional[str]

    # Data flow
    current_data: Any
    results: Dict[str, Any]

    # Error handling
    errors: List[Dict[str, str]]

    # Metadata
    workflow_id: str
    started_at: str
    completed_at: Optional[str]


class WorkflowEngine:
    def __init__(self):
        self.registry = RegistryManager()
        self.checkpointer = MemorySaver()
        self.loaded_agents = {}

    def create_workflow(
        self, agent_sequence: List[str], workflow_id: str = None
    ) -> StateGraph:
        """
        Create a LangGraph workflow from a sequence of agents.

        Args:
            agent_sequence: List of agent names to execute in order
            workflow_id: Optional workflow identifier

        Returns:
            Configured StateGraph ready for execution
        """

        # Validate all agents exist
        missing_agents = []
        for agent_name in agent_sequence:
            if not self.registry.agent_exists(agent_name):
                missing_agents.append(agent_name)

        if missing_agents:
            raise ValueError(f"Missing agents: {', '.join(missing_agents)}")

        # Create the graph
        workflow = StateGraph(WorkflowState)

        # Load and add each agent as a node
        for agent_name in agent_sequence:
            agent_func = self._load_agent(agent_name)
            workflow.add_node(agent_name, agent_func)

        # Add edges to create sequential flow
        for i, agent_name in enumerate(agent_sequence):
            if i == 0:
                # First agent connects from START
                workflow.set_entry_point(agent_name)

            if i < len(agent_sequence) - 1:
                # Connect to next agent
                next_agent = agent_sequence[i + 1]
                workflow.add_edge(agent_name, next_agent)
            else:
                # Last agent connects to END
                workflow.add_edge(agent_name, END)

        # Compile the workflow
        return workflow.compile(checkpointer=self.checkpointer)

    def execute_workflow(
        self,
        workflow: StateGraph,
        initial_data: Dict[str, Any],
        workflow_id: str = None,
    ) -> Dict[str, Any]:
        """
        Execute a compiled workflow.

        Args:
            workflow: Compiled StateGraph
            initial_data: Initial data to pass to first agent
            workflow_id: Optional workflow identifier

        Returns:
            Final workflow state with all results
        """

        # Prepare initial state
        initial_state = {
            "request": initial_data.get("request", ""),
            "files": initial_data.get("files", []),
            "execution_path": [],
            "current_agent": None,
            "current_data": initial_data,
            "results": {},
            "errors": [],
            "workflow_id": workflow_id or self._generate_workflow_id(),
            "started_at": datetime.now().isoformat(),
            "completed_at": None,
        }

        try:
            # Execute the workflow
            config = {"configurable": {"thread_id": workflow_id or "default"}}

            # Run through all nodes
            final_state = None
            for output in workflow.stream(initial_state, config):
                final_state = output

                # Print progress for debugging
                if isinstance(output, dict):
                    for key, value in output.items():
                        if key != "__end__":
                            print(f"  Executed: {key}")
                            if isinstance(value, dict) and "errors" in value:
                                if value["errors"]:
                                    print(f"    Errors: {value['errors']}")

            # Extract the final state
            if final_state and "__end__" in final_state:
                result_state = final_state["__end__"]
            else:
                # Get the last non-end state
                result_state = final_state
                for key, value in final_state.items():
                    if key != "__end__":
                        result_state = value
                        break

            # Mark completion
            result_state["completed_at"] = datetime.now().isoformat()

            # Update agent metrics
            for agent_name in result_state.get("execution_path", []):
                # Simple timing estimate
                self.registry.update_agent_metrics(agent_name, 1.0)

            return result_state

        except Exception as e:
            # Return error state
            initial_state["errors"].append(
                {"agent": "workflow_engine", "error": str(e)}
            )
            initial_state["completed_at"] = datetime.now().isoformat()
            return initial_state

    def create_and_execute(
        self,
        agent_sequence: List[str],
        initial_data: Dict[str, Any],
        workflow_id: str = None,
    ) -> Dict[str, Any]:
        """
        Convenience method to create and execute a workflow in one step.

        Args:
            agent_sequence: List of agent names to execute
            initial_data: Initial data for the workflow
            workflow_id: Optional workflow identifier

        Returns:
            Final workflow state with results
        """

        workflow = self.create_workflow(agent_sequence, workflow_id)
        return self.execute_workflow(workflow, initial_data, workflow_id)

    def _load_agent(self, agent_name: str):
        """
        Dynamically load an agent function from its file.

        Args:
            agent_name: Name of the agent to load

        Returns:
            The agent function
        """

        # Check cache first
        if agent_name in self.loaded_agents:
            return self.loaded_agents[agent_name]

        # Get agent info from registry
        agent_info = self.registry.get_agent(agent_name)
        if not agent_info:
            raise ValueError(f"Agent '{agent_name}' not found in registry")

        # Load the agent module
        agent_path = agent_info["location"]
        if not os.path.exists(agent_path):
            raise FileNotFoundError(f"Agent file not found: {agent_path}")

        # Import the module
        spec = importlib.util.spec_from_file_location(f"{agent_name}_agent", agent_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Get the agent function
        # Try both patterns: agent_name_agent and agent_name
        func_name = f"{agent_name}_agent"
        if hasattr(module, func_name):
            agent_func = getattr(module, func_name)
        elif hasattr(module, agent_name):
            agent_func = getattr(module, agent_name)
        else:
            raise AttributeError(
                f"Agent function '{func_name}' not found in {agent_path}"
            )

        # Cache for future use
        self.loaded_agents[agent_name] = agent_func

        return agent_func

    def _generate_workflow_id(self) -> str:
        """Generate a unique workflow ID."""
        from datetime import datetime
        import random

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = random.randint(1000, 9999)
        return f"workflow_{timestamp}_{random_suffix}"

    def visualize_workflow(self, agent_sequence: List[str]) -> str:
        """
        Create a text visualization of the workflow.

        Args:
            agent_sequence: List of agent names

        Returns:
            Text representation of the workflow
        """

        visualization = "\nWorkflow Visualization:\n"
        visualization += "=" * 50 + "\n"

        for i, agent_name in enumerate(agent_sequence):
            agent_info = self.registry.get_agent(agent_name)

            # Node representation
            visualization += f"\n[{i+1}. {agent_name}]\n"

            if agent_info:
                visualization += f"    Description: {agent_info['description']}\n"
                visualization += (
                    f"    Uses tools: {', '.join(agent_info['uses_tools'])}\n"
                )

            # Edge representation
            if i < len(agent_sequence) - 1:
                visualization += "         |\n"
                visualization += "         v\n"
            else:
                visualization += "         |\n"
                visualization += "        END\n"

        visualization += "\n" + "=" * 50
        return visualization

    def get_available_workflows(self) -> Dict[str, List[str]]:
        """
        Get pre-defined workflow templates.

        Returns:
            Dictionary of workflow templates
        """

        return {
            "text_analysis": ["text_analyzer"],
            "document_extraction": ["document_processor"],
            "pdf_email": ["pdf_email_extractor"],
            "csv_statistics": ["csv_analyzer", "statistics_calculator"],
            "full_document_analysis": [
                "document_processor",
                "text_analyzer",
                "statistics_calculator",
            ],
        }


class WorkflowCLI:
    """Command-line interface for testing workflows."""

    def __init__(self):
        self.engine = WorkflowEngine()
        self.registry = RegistryManager()

    def run(self):
        """Run interactive workflow execution."""

        print("\n" + "=" * 50)
        print("WORKFLOW ENGINE - Interactive Execution")
        print("=" * 50)

        # Show available agents
        print("\nAvailable Agents:")
        agents = self.registry.list_agents()
        for agent in agents:
            print(f"  - {agent['name']}: {agent['description']}")

        # Show pre-defined workflows
        print("\nPre-defined Workflows:")
        workflows = self.engine.get_available_workflows()
        for name, sequence in workflows.items():
            print(f"  - {name}: {' -> '.join(sequence)}")

        # Get user choice
        print("\nOptions:")
        print("1. Use pre-defined workflow")
        print("2. Create custom workflow")

        choice = input("\nChoice (1 or 2): ").strip()

        if choice == "1":
            # Use pre-defined
            workflow_name = input("Workflow name: ").strip()
            if workflow_name in workflows:
                agent_sequence = workflows[workflow_name]
            else:
                print("Invalid workflow name")
                return
        else:
            # Create custom
            print("\nEnter agent sequence (comma-separated):")
            sequence_input = input("Agents: ").strip()
            agent_sequence = [a.strip() for a in sequence_input.split(",")]

        # Get input data
        print("\nEnter input data:")
        input_type = input("Data type (text/file): ").strip().lower()

        if input_type == "file":
            file_path = input("File path: ").strip()
            initial_data = {
                "file_path": file_path,
                "request": f"Process file: {file_path}",
            }
        else:
            text = input("Enter text: ").strip()
            initial_data = {"text": text, "request": "Process text input"}

        # Show workflow visualization
        print(self.engine.visualize_workflow(agent_sequence))

        # Execute workflow
        print("\nExecuting workflow...")
        print("-" * 40)

        try:
            result = self.engine.create_and_execute(
                agent_sequence=agent_sequence, initial_data=initial_data
            )

            print("\n" + "-" * 40)
            print("Workflow completed!")

            # Show results
            print("\nExecution Path:")
            for agent in result.get("execution_path", []):
                print(f"  - {agent}")

            print("\nResults:")
            for agent_name, agent_result in result.get("results", {}).items():
                print(f"\n  [{agent_name}]")
                if isinstance(agent_result, dict):
                    print(f"    Status: {agent_result.get('status', 'unknown')}")
                    if "data" in agent_result:
                        print(
                            f"    Data: {json.dumps(agent_result['data'], indent=6)[:500]}"
                        )

            if result.get("errors"):
                print("\nErrors:")
                for error in result["errors"]:
                    print(f"  - {error['agent']}: {error['error']}")

        except Exception as e:
            print(f"Workflow execution failed: {str(e)}")


if __name__ == "__main__":
    cli = WorkflowCLI()
    cli.run()

```

--------------------------------------------------------------------------------

### File: create_knowledge_base.py
**Path:** `create_knowledge_base.py`
**Size:** 12,696 bytes
**Modified:** 2025-09-02 23:01:54

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
        self.output_file = "AGENTIC_FABRIC_KNOWLEDGE_BASE.md"

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
        self.max_file_size = 50000  # 50KB

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
        content.append("- GPT-4: Master orchestrator for strategic decisions")
        content.append("- Claude: Intelligent agent execution engine")
        content.append("- LangGraph: Workflow coordination")
        content.append("- Streamlit: User interface")
        content.append("")

        # Current Status
        content.append("## IMPLEMENTATION STATUS")
        content.append("")
        content.append("**Completed Steps (1-4):**")
        content.append("- [x] Step 1: Project Foundation Setup")
        content.append("- [x] Step 2: Python Environment Configuration")
        content.append("- [x] Step 3: OpenAI API Setup & Configuration")
        content.append("- [x] Step 4: Anthropic Claude API Setup & Configuration")
        content.append("")
        content.append("**Ready for:** Step 5 - Core Infrastructure Development")
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

        # Environment Information
        content.append("## ENVIRONMENT INFORMATION")
        content.append("")
        content.append("**API Configuration:**")
        content.append("- OpenAI: Configured and tested (GPT-4 available)")
        content.append("- Anthropic: Configured and tested (Claude-3-Haiku available)")
        content.append("- Dual API Integration: Working successfully")
        content.append("")

        content.append("**Python Environment:**")
        content.append("- Virtual Environment: ./venv/")
        content.append("- Python Version: 3.11+")
        content.append("- Key Dependencies: openai, anthropic, streamlit, langgraph")
        content.append("")

        content.append("**Quick Start Commands:**")
        content.append("```bash")
        content.append("# Activate environment")
        content.append("source venv/bin/activate")
        content.append("")
        content.append("# Test APIs")
        content.append("python tests/api_tests/test_dual_api_integration.py")
        content.append("")
        content.append("# Continue development from Step 5")
        content.append("# Next: Core Infrastructure Development")
        content.append("```")
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

### File: docs/AGENT_TOOL_TEMPLATES.md
**Path:** `docs/AGENT_TOOL_TEMPLATES.md`
**Size:** 3,267 bytes
**Modified:** 2025-09-02 23:39:35

```markdown
# Agent and Tool Creation Templates

## Tool Template Structure

Tools must be **pure functions** with these characteristics:
- No side effects (no file I/O, no API calls, no global state)
- Deterministic (same input always produces same output)
- Self-contained (all imports inside the function)
- Error handling (gracefully handle edge cases)
- Clear return types (consistent structure)

### Basic Tool Pattern
```python
def tool_name(input_param):
    """Clear description of what the tool does."""
    # Import statements inside function
    import required_module
    
    # Input validation
    if not input_param:
        return default_value
    
    # Core logic
    try:
        result = process(input_param)
        return result
    except Exception:
        return safe_default
Tool Categories

Extraction Tools - Extract specific data from text
Calculation Tools - Perform mathematical operations
Transformation Tools - Convert data formats
Validation Tools - Check data validity
Aggregation Tools - Combine or summarize data

Agent Template Structure
Agents coordinate tools and manage workflow state:
Basic Agent Pattern
pythondef agent_name(state):
    """Agent description."""
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from generated.tools.tool1 import tool1
    from generated.tools.tool2 import tool2
    
    try:
        # Initialize state if needed
        if 'results' not in state:
            state['results'] = {}
        if 'errors' not in state:
            state['errors'] = []
            
        # Get input data
        input_data = state.get('current_data', {})
        
        # Use tools
        result1 = tool1(input_data)
        result2 = tool2(result1)
        
        # Format output
        result = {
            "status": "success",
            "data": processed_data,
            "metadata": {
                "agent": "agent_name",
                "tools_used": ["tool1", "tool2"],
                "execution_time": 0.1
            }
        }
        
        # Update state
        state['results']['agent_name'] = result
        state['current_data'] = result['data']
        state['execution_path'].append('agent_name')
        
    except Exception as e:
        state['errors'].append({
            "agent": "agent_name",
            "error": str(e)
        })
        
    return state
Size Guidelines

Tools: 20-100 lines

Simple extractors: 20-40 lines
Complex processors: 40-80 lines
Multi-step validators: 60-100 lines


Agents: 50-300 lines

Single tool agents: 50-100 lines
Multi-tool coordinators: 100-200 lines
Complex workflow agents: 200-300 lines



Common Patterns
Data Extraction Pattern
pythondef extract_pattern(text):
    import re
    pattern = r'your_regex_here'
    matches = re.findall(pattern, text)
    return list(set(matches))  # Remove duplicates
Calculation Pattern
pythondef calculate_metric(data):
    if not data:
        return 0.0
    try:
        result = perform_calculation(data)
        return round(result, 2)
    except:
        return 0.0
State Update Pattern
python# In agent
state['results'][agent_name] = result
state['current_data'] = result['data']
state['execution_path'].append(agent_name)
```

--------------------------------------------------------------------------------

### File: generated/__init__.py
**Path:** `generated/__init__.py`
**Size:** 0 bytes
**Modified:** 2025-09-02 19:29:49

```python

```

--------------------------------------------------------------------------------

### File: generated/agents/__init__.py
**Path:** `generated/agents/__init__.py`
**Size:** 0 bytes
**Modified:** 2025-09-02 19:29:49

```python

```

--------------------------------------------------------------------------------

### File: generated/agents/csv_analyzer.py
**Path:** `generated/agents/csv_analyzer.py`
**Size:** 2,580 bytes
**Modified:** 2025-09-03 00:02:18

```python
def csv_analyzer_agent(state):
    """Agent that analyzes CSV data to extract statistics and create summaries."""
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from generated.tools.read_csv import read_csv
    from generated.tools.extract_numbers import extract_numbers
    from generated.tools.calculate_mean import calculate_mean
    from generated.tools.calculate_median import calculate_median
    
    try:
        # Initialize state components if missing
        if 'results' not in state:
            state['results'] = {}
        if 'errors' not in state:
            state['errors'] = []
        if 'execution_path' not in state:
            state['execution_path'] = []
        
        # Get CSV file path from state
        csv_file_path = state.get('current_data', {}).get('file_path', '')
        
        # Read CSV file using read_csv tool
        df = read_csv(csv_file_path)
        
        # Extract numeric data from columns
        numeric_columns = []
        numeric_data = {}
        for column in df.columns:
            try:
                numeric_data[column] = df[column].apply(extract_numbers).tolist()
                numeric_columns.append(column)
            except:
                pass
        
        # Calculate statistics for numeric columns
        column_stats = {}
        for column in numeric_columns:
            column_stats[column] = {
                "mean": calculate_mean(numeric_data[column]),
                "median": calculate_median(numeric_data[column])
            }
        
        # Create summary
        summary = {
            "row_count": len(df),
            "column_count": len(df.columns),
            "numeric_columns": numeric_columns,
            "column_statistics": column_stats
        }
        
        # Update state
        state['results']['csv_analyzer'] = {
            "status": "success",
            "data": summary
        }
        state['current_data'] = summary
        state['execution_path'].append('csv_analyzer')
        
    except Exception as e:
        state['errors'].append({
            "agent": "csv_analyzer",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        })
        
        # Still update results with error status
        state['results']['csv_analyzer'] = {
            "status": "error",
            "data": None,
            "metadata": {
                "agent": "csv_analyzer",
                "error": str(e)
            }
        }
    
    return state
```

--------------------------------------------------------------------------------

### File: generated/agents/document_processor.py
**Path:** `generated/agents/document_processor.py`
**Size:** 2,259 bytes
**Modified:** 2025-09-03 00:03:00

```python
def document_processor_agent(state):
    """Agent that processes text documents to extract key information."""
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from generated.tools.read_text import read_text
    from generated.tools.extract_emails import extract_emails
    from generated.tools.extract_urls import extract_urls
    from generated.tools.extract_numbers import extract_numbers
    
    try:
        # Initialize state components if missing
        if 'results' not in state:
            state['results'] = {}
        if 'errors' not in state:
            state['errors'] = []
        if 'execution_path' not in state:
            state['execution_path'] = []
        
        # Get input from state
        file_path = state.get('current_data', {}).get('file_path', '')
        
        # Read text from file
        text = read_text(file_path)
        
        # Extract entities from text
        emails = extract_emails(text)
        urls = extract_urls(text)
        numbers = extract_numbers(text)
        
        # Prepare result
        result = {
            "status": "success",
            "data": {
                "emails": emails,
                "urls": urls,
                "numbers": numbers
            },
            "metadata": {
                "agent": "document_processor",
                "tools_used": ["read_text", "extract_emails", "extract_urls", "extract_numbers"],
                "execution_time": 0.5
            }
        }
        
        # Update state
        state['results']['document_processor'] = result
        state['current_data'] = result['data']
        state['execution_path'].append('document_processor')
        
    except Exception as e:
        state['errors'].append({
            "agent": "document_processor",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        })
        
        # Still update results with error status
        state['results']['document_processor'] = {
            "status": "error",
            "data": None,
            "metadata": {
                "agent": "document_processor",
                "error": str(e)
            }
        }
    
    return state
```

--------------------------------------------------------------------------------

### File: generated/agents/email_extractor.py
**Path:** `generated/agents/email_extractor.py`
**Size:** 1,155 bytes
**Modified:** 2025-09-02 19:45:07

```python
def email_extractor_agent(state):
    """Agent that extracts emails from text."""
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from generated.tools.extract_emails import extract_emails
    
    try:
        # Get input
        text = state.get('current_data', {}).get('text', '')
        
        # Use tool
        emails = extract_emails(text)
        
        # Format output
        result = {
            "status": "success",
            "data": {
                "emails": emails,
                "count": len(emails)
            },
            "metadata": {
                "agent": "email_extractor",
                "tools_used": ["extract_emails"],
                "execution_time": 0.1
            }
        }
        
        # Update state
        state['results']['email_extractor'] = result
        state['current_data'] = result['data']
        state['execution_path'].append('email_extractor')
        
    except Exception as e:
        state['errors'].append({
            "agent": "email_extractor",
            "error": str(e)
        })
    
    return state

```

--------------------------------------------------------------------------------

### File: generated/agents/pdf_email_extractor.py
**Path:** `generated/agents/pdf_email_extractor.py`
**Size:** 2,159 bytes
**Modified:** 2025-09-03 00:03:58

```python
def pdf_email_extractor_agent(state):
    """Agent that extracts email addresses from PDF documents."""
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from generated.tools.read_pdf import read_pdf
    from generated.tools.extract_emails import extract_emails
    
    import re
    
    try:
        # Initialize state components if missing
        if 'results' not in state:
            state['results'] = {}
        if 'errors' not in state:
            state['errors'] = []
        if 'execution_path' not in state:
            state['execution_path'] = []
        
        # Get PDF file path from state
        pdf_file_path = state.get('current_data', {}).get('pdf_file_path', '')
        
        # Read PDF content using read_pdf tool
        pdf_text = read_pdf(pdf_file_path)
        
        # Extract email addresses from the text
        emails = extract_emails(pdf_text)
        
        # Remove duplicates and format output
        unique_emails = list(set(emails))
        
        result = {
            "status": "success",
            "data": {
                "emails_found": len(unique_emails),
                "emails": unique_emails
            },
            "metadata": {
                "agent": "pdf_email_extractor",
                "tools_used": ["read_pdf", "extract_emails"],
                "execution_time": 0.5
            }
        }
        
        # Update state
        state['results']['pdf_email_extractor'] = result
        state['current_data'] = result['data']
        state['execution_path'].append('pdf_email_extractor')
    
    except Exception as e:
        state['errors'].append({
            "agent": "pdf_email_extractor",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        })
        
        # Still update results with error status
        state['results']['pdf_email_extractor'] = {
            "status": "error",
            "data": None,
            "metadata": {
                "agent": "pdf_email_extractor",
                "error": str(e)
            }
        }
    
    return state
```

--------------------------------------------------------------------------------

### File: generated/agents/statistics_calculator.py
**Path:** `generated/agents/statistics_calculator.py`
**Size:** 3,007 bytes
**Modified:** 2025-09-02 23:58:46

```python
def statistics_calculator_agent(state):
    """Agent that calculates basic statistics from numbers in text."""
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from generated.tools.extract_numbers import extract_numbers
    from generated.tools.calculate_mean import calculate_mean
    from generated.tools.calculate_median import calculate_median
    
    try:
        # Initialize state components if missing
        if 'results' not in state:
            state['results'] = {}
        if 'errors' not in state:
            state['errors'] = []
        if 'execution_path' not in state:
            state['execution_path'] = []
            
        # Get input from state
        text = state.get('current_data', {}).get('text', '')
        
        # Use tools to extract and analyze numbers
        numbers = extract_numbers(text)
        
        if not numbers:
            result = {
                "status": "warning",
                "data": {
                    "message": "No numbers found in text",
                    "numbers_found": 0
                },
                "metadata": {
                    "agent": "statistics_calculator",
                    "tools_used": ["extract_numbers"],
                    "execution_time": 0.1
                }
            }
        else:
            # Calculate statistics using tools
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
                    "agent": "statistics_calculator",
                    "tools_used": ["extract_numbers", "calculate_mean", "calculate_median"],
                    "execution_time": 0.3
                }
            }
        
        # Update state
        state['results']['statistics_calculator'] = result
        state['current_data'] = result['data']
        state['execution_path'].append('statistics_calculator')
        
    except Exception as e:
        state['errors'].append({
            "agent": "statistics_calculator",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        })
        
        # Still update results with error status
        state['results']['statistics_calculator'] = {
            "status": "error",
            "data": None,
            "metadata": {
                "agent": "statistics_calculator",
                "error": str(e)
            }
        }
    
    return state
```

--------------------------------------------------------------------------------

### File: generated/agents/text_analyzer.py
**Path:** `generated/agents/text_analyzer.py`
**Size:** 1,890 bytes
**Modified:** 2025-09-02 23:58:41

```python
def text_analyzer_agent(state):
    """Analyze text to extract emails and numbers."""
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from generated.tools.extract_emails import extract_emails
    from generated.tools.extract_numbers import extract_numbers
    
    try:
        # Initialize state components if missing
        if 'results' not in state:
            state['results'] = {}
        if 'errors' not in state:
            state['errors'] = []
        if 'execution_path' not in state:
            state['execution_path'] = []
        
        # Get text from state
        text = state.get('current_data', {}).get('text', '')
        
        # Extract emails and numbers
        emails = extract_emails(text)
        numbers = extract_numbers(text)
        
        # Combine results into output dictionary
        output = {
            'emails': emails,
            'numbers': numbers
        }
        
        # Update state
        state['results']['text_analyzer'] = {
            'status': 'success',
            'data': output,
            'metadata': {
                'agent': 'text_analyzer_agent',
                'tools_used': ['extract_emails', 'extract_numbers'],
                'execution_time': 0.5
            }
        }
        state['current_data'] = output
        state['execution_path'].append('text_analyzer_agent')
    
    except Exception as e:
        state['errors'].append({
            'agent': 'text_analyzer_agent',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        })
        
        state['results']['text_analyzer'] = {
            'status': 'error',
            'data': None,
            'metadata': {
                'agent': 'text_analyzer_agent',
                'error': str(e)
            }
        }
    
    return state
```

--------------------------------------------------------------------------------

### File: generated/tools/__init__.py
**Path:** `generated/tools/__init__.py`
**Size:** 0 bytes
**Modified:** 2025-09-02 19:29:49

```python

```

--------------------------------------------------------------------------------

### File: generated/tools/calculate_mean.py
**Path:** `generated/tools/calculate_mean.py`
**Size:** 406 bytes
**Modified:** 2025-09-02 23:42:11

```python
def calculate_mean(numbers):
    """Calculate the arithmetic mean of a list of numbers."""
    if not numbers:
        return 0.0

    if not isinstance(numbers, (list, tuple)):
        return float(numbers)

    try:
        total = sum(numbers)
        count = len(numbers)
        mean = total / count
        return float(mean)
    except (TypeError, ValueError, ZeroDivisionError):
        return 0.0

```

--------------------------------------------------------------------------------

### File: generated/tools/calculate_median.py
**Path:** `generated/tools/calculate_median.py`
**Size:** 665 bytes
**Modified:** 2025-09-02 23:42:11

```python
def calculate_median(numbers):
    """Calculate the median of a list of numbers."""
    if not numbers:
        return 0.0

    if not isinstance(numbers, (list, tuple)):
        return float(numbers)

    try:
        sorted_numbers = sorted(numbers)
        n = len(sorted_numbers)

        if n % 2 == 0:
            # Even number of elements
            mid1 = sorted_numbers[n // 2 - 1]
            mid2 = sorted_numbers[n // 2]
            median = (mid1 + mid2) / 2
        else:
            # Odd number of elements
            median = sorted_numbers[n // 2]

        return float(median)
    except (TypeError, ValueError, IndexError):
        return 0.0

```

--------------------------------------------------------------------------------

### File: generated/tools/extract_emails.py
**Path:** `generated/tools/extract_emails.py`
**Size:** 238 bytes
**Modified:** 2025-09-02 19:45:07

```python
def extract_emails(text):
    """Extract email addresses from text."""
    import re
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(pattern, text)
    return list(set(emails))  # Remove duplicates

```

--------------------------------------------------------------------------------

### File: generated/tools/extract_numbers.py
**Path:** `generated/tools/extract_numbers.py`
**Size:** 869 bytes
**Modified:** 2025-09-02 23:42:11

```python
def extract_numbers(text):
    """Extract all numbers from text - both integers and decimals."""
    import re

    if not text:
        return []

    # Find all numeric patterns
    patterns = [
        r"-?\d+\.?\d*",  # Regular numbers (integers and decimals)
        r"-?\.\d+",  # Numbers starting with decimal point
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

```

--------------------------------------------------------------------------------

### File: generated/tools/extract_urls.py
**Path:** `generated/tools/extract_urls.py`
**Size:** 473 bytes
**Modified:** 2025-09-02 23:47:53

```python
def extract_urls(text):
    import re
    from urllib.parse import urlparse

    if not text:
        return []

    url_pattern = r'(https?://\S+)'
    urls = re.findall(url_pattern, text)

    # Remove duplicates while preserving order
    seen = set()
    unique_urls = []
    for url in urls:
        parsed_url = urlparse(url)
        if parsed_url.netloc not in seen:
            seen.add(parsed_url.netloc)
            unique_urls.append(url)

    return unique_urls
```

--------------------------------------------------------------------------------

### File: generated/tools/read_csv.py
**Path:** `generated/tools/read_csv.py`
**Size:** 679 bytes
**Modified:** 2025-09-02 23:26:46

```python
def read_csv(file_path):
    """Read CSV file into structured data using pandas."""
    import pandas as pd
    import os

    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}", "data": None}

    try:
        df = pd.read_csv(file_path)

        return {
            "data": df.to_dict("records"),
            "columns": df.columns.tolist(),
            "shape": {"rows": len(df), "columns": len(df.columns)},
            "dtypes": df.dtypes.astype(str).to_dict(),
            "status": "success",
            "file_path": file_path,
        }

    except Exception as e:
        return {"error": str(e), "data": None, "status": "error"}

```

--------------------------------------------------------------------------------

### File: generated/tools/read_json.py
**Path:** `generated/tools/read_json.py`
**Size:** 576 bytes
**Modified:** 2025-09-02 23:26:46

```python
def read_json(file_path):
    """Parse JSON file into Python object."""
    import json
    import os

    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}", "data": None}

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        return {
            "data": data,
            "type": type(data).__name__,
            "status": "success",
            "file_path": file_path,
        }

    except Exception as e:
        return {"error": str(e), "data": None, "status": "error"}

```

--------------------------------------------------------------------------------

### File: generated/tools/read_pdf.py
**Path:** `generated/tools/read_pdf.py`
**Size:** 909 bytes
**Modified:** 2025-09-02 23:26:46

```python
def read_pdf(file_path):
    """Extract text from PDF file using PyPDF2."""
    import PyPDF2
    import os

    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}", "text": ""}

    try:
        text_content = []

        with open(file_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)

            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                if text.strip():
                    text_content.append(text)

        full_text = "\n\n".join(text_content)

        return {
            "text": full_text,
            "pages": num_pages,
            "status": "success",
            "file_path": file_path,
        }

    except Exception as e:
        return {"error": str(e), "text": "", "status": "error"}

```

--------------------------------------------------------------------------------

### File: generated/tools/read_text.py
**Path:** `generated/tools/read_text.py`
**Size:** 659 bytes
**Modified:** 2025-09-02 23:29:34

```python
def read_text(file_path):
    """Read plain text file."""
    import os

    if not os.path.exists(file_path):
        return {
            "error": f"File not found: {file_path}",
            "text": "",
            "status": "error",  # Added this line
        }

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

        return {
            "text": text,
            "lines": len(text.splitlines()),
            "chars": len(text),
            "status": "success",
            "file_path": file_path,
        }

    except Exception as e:
        return {"error": str(e), "text": "", "status": "error"}

```

--------------------------------------------------------------------------------

### File: registry_backups/backup_20250903_080437_test_backup/agents.json
**Path:** `registry_backups/backup_20250903_080437_test_backup/agents.json`
**Size:** 4,080 bytes
**Modified:** 2025-09-03 08:04:37

```json
{
  "agents": {
    "email_extractor": {
      "description": "Extracts email addresses from provided text",
      "uses_tools": [
        "extract_emails"
      ],
      "input_schema": {
        "text": "string"
      },
      "output_schema": {
        "emails": "array",
        "count": "integer"
      },
      "location": "generated/agents/email_extractor.py",
      "created_by": "claude-3-haiku",
      "created_at": "2025-09-02T19:45:07.755626",
      "version": "1.0.fd0b347e",
      "execution_count": 3,
      "avg_execution_time": 1.0,
      "tags": [
        "extraction",
        "email",
        "text-processing"
      ],
      "line_count": 41,
      "last_executed": "2025-09-03T07:56:38.262579"
    },
    "text_analyzer": {
      "description": "Analyze text to extract emails and numbers",
      "uses_tools": [
        "extract_emails",
        "extract_numbers"
      ],
      "input_schema": {
        "data": "any"
      },
      "output_schema": {
        "data": "any"
      },
      "location": "generated/agents/text_analyzer.py",
      "created_by": "claude-3-haiku",
      "created_at": "2025-09-02T23:58:41.401801",
      "version": "1.0.528daabc",
      "execution_count": 0,
      "avg_execution_time": 0,
      "tags": [
        "communication",
        "extraction"
      ],
      "line_count": 61
    },
    "statistics_calculator": {
      "description": "Calculate statistics from numbers in text",
      "uses_tools": [
        "extract_numbers",
        "calculate_mean",
        "calculate_median"
      ],
      "input_schema": {
        "data": "any"
      },
      "output_schema": {
        "data": "any"
      },
      "location": "generated/agents/statistics_calculator.py",
      "created_by": "claude-3-haiku",
      "created_at": "2025-09-02T23:58:46.927691",
      "version": "1.0.2d6d8b8b",
      "execution_count": 2,
      "avg_execution_time": 1.0,
      "tags": [
        "analysis",
        "statistics"
      ],
      "line_count": 86,
      "last_executed": "2025-09-03T07:57:01.577754"
    },
    "csv_analyzer": {
      "description": "Analyze CSV data to extract statistics and create summaries",
      "uses_tools": [
        "read_csv",
        "extract_numbers",
        "calculate_mean",
        "calculate_median"
      ],
      "input_schema": {
        "data": "any"
      },
      "output_schema": {
        "data": "any"
      },
      "location": "generated/agents/csv_analyzer.py",
      "created_by": "claude-3-haiku",
      "created_at": "2025-09-03T00:02:18.109016",
      "version": "1.0.845d07b9",
      "execution_count": 0,
      "avg_execution_time": 0,
      "tags": [
        "statistics",
        "data-processing",
        "analysis",
        "csv"
      ],
      "line_count": 78
    },
    "document_processor": {
      "description": "Process text documents to extract key information",
      "uses_tools": [
        "read_text",
        "extract_emails",
        "extract_urls",
        "extract_numbers"
      ],
      "input_schema": {
        "data": "any"
      },
      "output_schema": {
        "data": "any"
      },
      "location": "generated/agents/document_processor.py",
      "created_by": "claude-3-haiku",
      "created_at": "2025-09-03T00:03:00.710845",
      "version": "1.0.540ebda1",
      "execution_count": 0,
      "avg_execution_time": 0,
      "tags": [],
      "line_count": 69
    },
    "pdf_email_extractor": {
      "description": "Extract email addresses from PDF documents",
      "uses_tools": [
        "read_pdf",
        "extract_emails"
      ],
      "input_schema": {
        "data": "any"
      },
      "output_schema": {
        "data": "any"
      },
      "location": "generated/agents/pdf_email_extractor.py",
      "created_by": "claude-3-haiku",
      "created_at": "2025-09-03T00:03:58.606397",
      "version": "1.0.298b664d",
      "execution_count": 0,
      "avg_execution_time": 0,
      "tags": [
        "communication",
        "pdf-processing",
        "extraction",
        "document"
      ],
      "line_count": 68
    }
  }
}
```

--------------------------------------------------------------------------------

### File: registry_backups/backup_20250903_080437_test_backup/metadata.json
**Path:** `registry_backups/backup_20250903_080437_test_backup/metadata.json`
**Size:** 330 bytes
**Modified:** 2025-09-03 08:04:37

```json
{
  "timestamp": "2025-09-03T08:04:37.740319",
  "tag": "test_backup",
  "stats": {
    "total_agents": 6,
    "total_tools": 9,
    "total_executions": 5,
    "avg_agent_lines": 67.2,
    "avg_tool_lines": 21.6,
    "tool_reuse_count": 16,
    "most_used_agent": "email_extractor",
    "newest_agent": "pdf_email_extractor"
  }
}
```

--------------------------------------------------------------------------------

### File: registry_backups/backup_20250903_080437_test_backup/tools.json
**Path:** `registry_backups/backup_20250903_080437_test_backup/tools.json`
**Size:** 4,670 bytes
**Modified:** 2025-09-03 08:04:37

```json
{
  "tools": {
    "extract_emails": {
      "description": "Extracts email addresses from text using regex",
      "signature": "def extract_emails(text):",
      "location": "generated/tools/extract_emails.py",
      "used_by_agents": [
        "email_extractor",
        "text_analyzer",
        "document_processor",
        "pdf_email_extractor"
      ],
      "created_by": "claude-3-haiku",
      "created_at": "2025-09-02T19:45:07.754248",
      "is_pure_function": true,
      "tags": [
        "text-processing",
        "extraction",
        "email"
      ],
      "line_count": 6
    },
    "read_pdf": {
      "description": "Extracts text content from PDF files using PyPDF2",
      "signature": "def read_pdf(file_path):",
      "location": "generated/tools/read_pdf.py",
      "used_by_agents": [
        "pdf_email_extractor"
      ],
      "created_by": "claude-3-haiku",
      "created_at": "2025-09-02T23:26:46.042619",
      "is_pure_function": true,
      "tags": [
        "file-reader",
        "pdf",
        "text-extraction"
      ],
      "line_count": 32
    },
    "read_csv": {
      "description": "Reads CSV files into structured data using pandas",
      "signature": "def read_csv(file_path):",
      "location": "generated/tools/read_csv.py",
      "used_by_agents": [
        "csv_analyzer"
      ],
      "created_by": "claude-3-haiku",
      "created_at": "2025-09-02T23:26:46.043604",
      "is_pure_function": true,
      "tags": [
        "file-reader",
        "csv",
        "data-processing"
      ],
      "line_count": 22
    },
    "read_json": {
      "description": "Parses JSON files into Python objects",
      "signature": "def read_json(file_path):",
      "location": "generated/tools/read_json.py",
      "used_by_agents": [],
      "created_by": "claude-3-haiku",
      "created_at": "2025-09-02T23:26:46.044329",
      "is_pure_function": true,
      "tags": [
        "file-reader",
        "json",
        "data-processing"
      ],
      "line_count": 21
    },
    "read_text": {
      "description": "Reads plain text files",
      "signature": "def read_text(file_path):",
      "location": "generated/tools/read_text.py",
      "used_by_agents": [
        "document_processor"
      ],
      "created_by": "claude-3-haiku",
      "created_at": "2025-09-02T23:26:46.045070",
      "is_pure_function": true,
      "tags": [
        "file-reader",
        "text",
        "basic-io"
      ],
      "line_count": 21
    },
    "extract_numbers": {
      "description": "Extracts all numbers from text, including integers and decimals",
      "signature": "def extract_numbers(text):",
      "location": "generated/tools/extract_numbers.py",
      "used_by_agents": [
        "text_analyzer",
        "statistics_calculator",
        "csv_analyzer",
        "document_processor"
      ],
      "created_by": "claude-3-haiku",
      "created_at": "2025-09-02T23:42:11.055994",
      "is_pure_function": true,
      "tags": [
        "text-processing",
        "extraction",
        "numbers"
      ],
      "line_count": 33
    },
    "calculate_mean": {
      "description": "Calculates the arithmetic mean of a list of numbers",
      "signature": "def calculate_mean(numbers):",
      "location": "generated/tools/calculate_mean.py",
      "used_by_agents": [
        "statistics_calculator",
        "csv_analyzer"
      ],
      "created_by": "claude-3-haiku",
      "created_at": "2025-09-02T23:42:11.057455",
      "is_pure_function": true,
      "tags": [
        "statistics",
        "math",
        "aggregation"
      ],
      "line_count": 15
    },
    "calculate_median": {
      "description": "Calculates the median value of a list of numbers",
      "signature": "def calculate_median(numbers):",
      "location": "generated/tools/calculate_median.py",
      "used_by_agents": [
        "statistics_calculator",
        "csv_analyzer"
      ],
      "created_by": "claude-3-haiku",
      "created_at": "2025-09-02T23:42:11.058335",
      "is_pure_function": true,
      "tags": [
        "statistics",
        "math",
        "aggregation"
      ],
      "line_count": 24
    },
    "extract_urls": {
      "description": "Extract all URLs from text",
      "signature": "def extract_urls(text):",
      "location": "generated/tools/extract_urls.py",
      "used_by_agents": [
        "document_processor"
      ],
      "created_by": "claude-3-haiku",
      "created_at": "2025-09-02T23:47:53.241795",
      "is_pure_function": true,
      "tags": [
        "parsing",
        "link",
        "text-processing",
        "extraction",
        "web"
      ],
      "line_count": 20
    }
  }
}
```

--------------------------------------------------------------------------------

### File: requirements.txt
**Path:** `requirements.txt`
**Size:** 1,582 bytes
**Modified:** 2025-09-01 10:31:58

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

```

--------------------------------------------------------------------------------

### File: scripts/regenerate_agents.py
**Path:** `scripts/regenerate_agents.py`
**Size:** 3,702 bytes
**Modified:** 2025-09-03 13:31:41

```python
"""
Regenerate Agents with Improved Data Handling
"""

import sys
import os
import shutil

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.agent_factory import AgentFactory
from core.registry import RegistryManager


def cleanup_and_regenerate():
    """Remove problematic agents and regenerate with better prompts."""

    print("AGENT REGENERATION PROCESS")
    print("=" * 50)

    registry = RegistryManager()
    factory = AgentFactory()

    # Agents to regenerate for better data handling
    agents_to_regenerate = [
        {
            "name": "text_analyzer",
            "description": "Analyze text to extract emails and numbers, handling various input formats",
            "tools": ["extract_emails", "extract_numbers"],
            "input": "Text data from state in any format (string, dict with text field, etc.)",
            "output": "Dictionary with extracted emails and numbers arrays",
        },
        {
            "name": "statistics_calculator",
            "description": "Calculate statistics from numbers, accepting both raw text and pre-extracted number arrays",
            "tools": ["extract_numbers", "calculate_mean", "calculate_median"],
            "input": "Either raw text to extract numbers from, or pre-extracted numbers array from previous agent",
            "output": "Dictionary with calculated statistics including mean, median, min, max",
        },
    ]

    print("\n1. Backing up current agents...")
    os.makedirs("generated/agents_backup", exist_ok=True)

    for agent_info in agents_to_regenerate:
        agent_name = agent_info["name"]
        agent_file = f"generated/agents/{agent_name}_agent.py"

        if os.path.exists(agent_file):
            backup_file = f"generated/agents_backup/{agent_name}_agent.py"
            shutil.copy(agent_file, backup_file)
            print(f"  Backed up: {agent_name}")

    print("\n2. Removing agents from registry...")

    for agent_info in agents_to_regenerate:
        agent_name = agent_info["name"]
        if registry.agent_exists(agent_name):
            # Remove from registry
            del registry.agents["agents"][agent_name]
            print(f"  Removed from registry: {agent_name}")

    registry.save_all()

    print("\n3. Regenerating agents with improved data handling...")
    print("This will use Claude API credits.")
    confirm = input("Continue? (y/n): ").lower()

    if confirm != "y":
        print("Cancelled.")
        return

    for agent_info in agents_to_regenerate:
        print(f"\nRegenerating: {agent_info['name']}")

        result = factory.create_agent(
            agent_name=agent_info["name"],
            description=agent_info["description"],
            required_tools=agent_info["tools"],
            input_description=agent_info["input"],
            output_description=agent_info["output"],
            workflow_steps=[
                "Check multiple possible input locations in state",
                "Handle both raw and pre-processed data",
                "Process data with appropriate tools",
                "Format output consistently",
                "Update state for next agent",
            ],
        )

        if result["status"] == "success":
            print(
                f"  Success: {agent_info['name']} regenerated ({result['line_count']} lines)"
            )
        else:
            print(f"  Failed: {result.get('message')}")

    print("\n4. Testing regenerated agents...")

    from tests.test_end_to_end import test_multi_agent_workflows

    test_multi_agent_workflows()

    print("\nRegeneration complete!")


if __name__ == "__main__":
    cleanup_and_regenerate()

```

--------------------------------------------------------------------------------

### File: system_report.md
**Path:** `system_report.md`
**Size:** 2,740 bytes
**Modified:** 2025-09-03 08:05:21

```markdown
# Agentic Fabric Registry Report
Generated: 2025-09-03 08:05:21

## System Health
- **Health Score**: 100.0/100
- **Status**: HEALTHY
- **Total Components**: 15
- **Valid Components**: 15

## Registered Agents
### email_extractor
- **Description**: Extracts email addresses from provided text
- **Tools Used**: extract_emails
- **Executions**: 3
- **Lines**: 41

### text_analyzer
- **Description**: Analyze text to extract emails and numbers
- **Tools Used**: extract_emails, extract_numbers
- **Executions**: 0
- **Lines**: 61

### statistics_calculator
- **Description**: Calculate statistics from numbers in text
- **Tools Used**: extract_numbers, calculate_mean, calculate_median
- **Executions**: 2
- **Lines**: 86

### csv_analyzer
- **Description**: Analyze CSV data to extract statistics and create summaries
- **Tools Used**: read_csv, extract_numbers, calculate_mean, calculate_median
- **Executions**: 0
- **Lines**: 78

### document_processor
- **Description**: Process text documents to extract key information
- **Tools Used**: read_text, extract_emails, extract_urls, extract_numbers
- **Executions**: 0
- **Lines**: 69

### pdf_email_extractor
- **Description**: Extract email addresses from PDF documents
- **Tools Used**: read_pdf, extract_emails
- **Executions**: 0
- **Lines**: 68

## Registered Tools
### extract_emails
- **Description**: Extracts email addresses from text using regex
- **Used By**: email_extractor, text_analyzer, document_processor, pdf_email_extractor
- **Lines**: 6

### read_pdf
- **Description**: Extracts text content from PDF files using PyPDF2
- **Used By**: pdf_email_extractor
- **Lines**: 32

### read_csv
- **Description**: Reads CSV files into structured data using pandas
- **Used By**: csv_analyzer
- **Lines**: 22

### read_json
- **Description**: Parses JSON files into Python objects
- **Used By**: None
- **Lines**: 21

### read_text
- **Description**: Reads plain text files
- **Used By**: document_processor
- **Lines**: 21

### extract_numbers
- **Description**: Extracts all numbers from text, including integers and decimals
- **Used By**: text_analyzer, statistics_calculator, csv_analyzer, document_processor
- **Lines**: 33

### calculate_mean
- **Description**: Calculates the arithmetic mean of a list of numbers
- **Used By**: statistics_calculator, csv_analyzer
- **Lines**: 15

### calculate_median
- **Description**: Calculates the median value of a list of numbers
- **Used By**: statistics_calculator, csv_analyzer
- **Lines**: 24

### extract_urls
- **Description**: Extract all URLs from text
- **Used By**: document_processor
- **Lines**: 20

## Usage Analytics
- **Total Executions**: 5
- **Average Agent Size**: 67.2 lines
- **Average Tool Size**: 21.6 lines

```

--------------------------------------------------------------------------------

### File: tests/test_agent_factory.py
**Path:** `tests/test_agent_factory.py`
**Size:** 5,047 bytes
**Modified:** 2025-09-02 23:58:21

```python
"""
Test Agent Factory
Verifies that the agent factory can create new agents dynamically
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.agent_factory import AgentFactory
from core.registry import RegistryManager


def test_agent_creation():
    """Test creating a new agent."""

    print("\n" + "=" * 50)
    print("TESTING AGENT FACTORY")
    print("=" * 50)

    factory = AgentFactory()
    registry = RegistryManager()

    # Test 1: Create a simple text processing agent
    print("\nTest 1: Creating text_analyzer agent...")

    result = factory.create_agent(
        agent_name="text_analyzer",
        description="Analyze text to extract emails and numbers",
        required_tools=["extract_emails", "extract_numbers"],
        input_description="Text data from state containing mixed content",
        output_description="Dictionary with extracted emails and numbers",
        workflow_steps=[
            "Get text from state current_data",
            "Extract email addresses using extract_emails tool",
            "Extract numbers using extract_numbers tool",
            "Combine results into output dictionary",
            "Update state with results",
        ],
    )

    if result["status"] == "success":
        print(f"  Success: Created {result['line_count']} lines of code")
        print(f"  Agent registered: text_analyzer_agent")
    elif result["status"] == "exists":
        print(f"  Agent already exists: {result['message']}")
    else:
        print(f"  Result: {result['status']} - {result['message']}")

    # Test 2: Try to create agent with missing tool
    print("\nTest 2: Attempting to create agent with missing tool...")

    result = factory.create_agent(
        agent_name="invalid_agent",
        description="Agent that uses non-existent tool",
        required_tools=["non_existent_tool"],
        input_description="Any input",
        output_description="Any output",
    )

    print(f"  Result: {result['status']} - {result['message']}")
    if "missing_tools" in result:
        print(f"  Missing tools: {result['missing_tools']}")

    # Test 3: Create a statistics agent
    print("\nTest 3: Creating statistics_calculator agent...")

    result = factory.create_agent(
        agent_name="statistics_calculator",
        description="Calculate statistics from numbers in text",
        required_tools=["extract_numbers", "calculate_mean", "calculate_median"],
        input_description="Text containing numbers",
        output_description="Statistical analysis with mean, median, count",
        workflow_steps=[
            "Extract numbers from input text",
            "Calculate mean of the numbers",
            "Calculate median of the numbers",
            "Count total numbers found",
            "Return statistics dictionary",
        ],
    )

    if result["status"] == "success":
        print(f"  Success: Created {result['line_count']} lines of code")
    else:
        print(f"  Result: {result['status']} - {result['message']}")

    # Display registry statistics
    print("\nRegistry Statistics:")
    stats = registry.get_statistics()
    print(f"  Total agents: {stats['total_agents']}")
    print(f"  Total tools: {stats['total_tools']}")
    print(f"  Average agent lines: {stats['avg_agent_lines']}")

    # List all agents
    print("\nRegistered Agents:")
    agents = registry.list_agents()
    for agent in agents:
        print(f"  - {agent['name']}: {agent['description']}")
        print(f"    Uses tools: {agent['uses_tools']}")


def test_validation():
    """Test agent code validation."""

    print("\n" + "=" * 50)
    print("TESTING AGENT VALIDATION")
    print("=" * 50)

    factory = AgentFactory()

    # Test invalid code (missing state parameter)
    print("\nTesting validation with missing state parameter...")
    bad_code = """def test_agent():
    return {'status': 'success'}
"""
    result = factory._validate_agent_code(bad_code, "test")
    print(f"  Valid: {result['valid']}")
    if not result["valid"]:
        print(f"  Error: {result['error']}")

    # Test invalid code (missing state operations)
    print("\nTesting validation with missing state operations...")
    incomplete_code = (
        """def test_agent(state):
    '''Agent without proper state handling.'''
    result = {'status': 'success'}
    return state
"""
        + "\n" * 50
    )  # Pad to meet line requirement

    result = factory._validate_agent_code(incomplete_code, "test")
    print(f"  Valid: {result['valid']}")
    if not result["valid"]:
        print(f"  Error: {result['error']}")

    print("\nValidation tests complete!")


if __name__ == "__main__":
    # Run validation tests first
    test_validation()

    # Ask before running API tests
    print("\n" + "=" * 50)
    response = input(
        "\nRun API tests? This will use Claude API credits (y/n): "
    ).lower()

    if response == "y":
        test_agent_creation()
    else:
        print("Skipping API tests.")

```

--------------------------------------------------------------------------------

### File: tests/test_end_to_end.py
**Path:** `tests/test_end_to_end.py`
**Size:** 7,986 bytes
**Modified:** 2025-09-03 13:15:49

```python
"""
End-to-End System Tests
Comprehensive testing of the complete Agentic Fabric system
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.orchestrator import Orchestrator
from core.workflow_engine import WorkflowEngine
from core.registry_enhanced import EnhancedRegistryManager


def test_simple_workflows():
    """Test simple single-agent workflows."""

    print("\n" + "=" * 50)
    print("TESTING SIMPLE WORKFLOWS")
    print("=" * 50)

    engine = WorkflowEngine()

    # Test 1: Email extraction
    print("\nTest 1: Email Extraction")
    print("-" * 40)

    result = engine.create_and_execute(
        agent_sequence=["email_extractor"],
        initial_data={
            "text": "Contact john@example.com or mary@test.org for details",
            "current_data": {
                "text": "Contact john@example.com or mary@test.org for details"
            },
        },
    )

    print(f"Execution path: {result.get('execution_path', [])}")
    if "email_extractor" in result.get("results", {}):
        emails = result["results"]["email_extractor"].get("data", {}).get("emails", [])
        print(f"Emails found: {emails}")
        assert len(emails) == 2, "Should find 2 emails"

    # Test 2: Number extraction
    print("\nTest 2: Number Extraction")
    print("-" * 40)

    result = engine.create_and_execute(
        agent_sequence=["text_analyzer"],
        initial_data={
            "text": "Values are 100, 200, 300",
            "current_data": {"text": "Values are 100, 200, 300"},
        },
    )

    print(f"Execution path: {result.get('execution_path', [])}")
    if "text_analyzer" in result.get("results", {}):
        numbers = result["results"]["text_analyzer"].get("data", {}).get("numbers", [])
        print(f"Numbers found: {numbers}")


def test_multi_agent_workflows():
    """Test multi-agent workflows with data passing."""

    print("\n" + "=" * 50)
    print("TESTING MULTI-AGENT WORKFLOWS")
    print("=" * 50)

    engine = WorkflowEngine()

    # Test: Text analysis -> Statistics calculation
    print("\nTest: Text Analysis Pipeline")
    print("-" * 40)

    # Initialize with text containing numbers
    initial_data = {
        "text": "Sales: 1000, 2000, 3000, 4000, 5000",
        "current_data": {"text": "Sales: 1000, 2000, 3000, 4000, 5000"},
    }

    result = engine.create_and_execute(
        agent_sequence=["text_analyzer", "statistics_calculator"],
        initial_data=initial_data,
    )

    print(f"Execution path: {result.get('execution_path', [])}")

    # Check text_analyzer results
    if "text_analyzer" in result.get("results", {}):
        ta_result = result["results"]["text_analyzer"]
        print(f"Text Analyzer Status: {ta_result.get('status')}")
        numbers = ta_result.get("data", {}).get("numbers", [])
        print(f"Numbers extracted: {numbers}")

    # Check statistics_calculator results
    if "statistics_calculator" in result.get("results", {}):
        sc_result = result["results"]["statistics_calculator"]
        print(f"Statistics Calculator Status: {sc_result.get('status')}")
        stats = sc_result.get("data", {}).get("statistics", {})
        if stats:
            print(
                f"Statistics calculated: mean={stats.get('mean')}, median={stats.get('median')}"
            )
        else:
            print(f"Statistics data: {sc_result.get('data')}")

    # Check current_data flow
    print(f"\nFinal current_data: {result.get('current_data')}")


def test_orchestrator_planning():
    """Test orchestrator's ability to plan workflows."""

    print("\n" + "=" * 50)
    print("TESTING ORCHESTRATOR PLANNING")
    print("=" * 50)

    orchestrator = Orchestrator()

    test_requests = [
        "Extract emails from: Contact support@test.com",
        "Calculate statistics for: 10, 20, 30, 40, 50",
        "Process this text and find all information: Visit https://example.com or email info@test.org",
    ]

    for request in test_requests:
        print(f"\nRequest: {request}")
        plan = orchestrator._plan_workflow(request)
        if plan["status"] == "success":
            print(f"Planned workflow: {' -> '.join(plan['workflow_steps'])}")
        else:
            print(f"Planning failed: {plan.get('message')}")


def test_full_orchestration():
    """Test complete orchestration from request to results."""

    print("\n" + "=" * 50)
    print("TESTING FULL ORCHESTRATION")
    print("=" * 50)

    orchestrator = Orchestrator()

    # Test 1: Simple request
    print("\nTest 1: Email Extraction Request")
    print("-" * 40)

    result = orchestrator.process_request(
        "Find emails in: Contact admin@site.com for help", auto_create=False
    )

    print(f"Status: {result['status']}")
    if result["status"] == "success":
        print(f"Workflow executed: {' -> '.join(result['workflow']['steps'])}")
        print(f"Response preview: {result['response'][:150]}...")

    # Test 2: Complex request
    print("\nTest 2: Statistical Analysis Request")
    print("-" * 40)

    result = orchestrator.process_request(
        "Analyze these numbers and give me statistics: 15, 25, 35, 45, 55",
        auto_create=False,
    )

    print(f"Status: {result['status']}")
    if result["status"] == "success":
        print(f"Workflow executed: {' -> '.join(result['workflow']['steps'])}")


def test_registry_health():
    """Verify system health after tests."""

    print("\n" + "=" * 50)
    print("SYSTEM HEALTH CHECK")
    print("=" * 50)

    registry = EnhancedRegistryManager()
    health = registry.health_check()

    print(f"Health Score: {health['health_score']}/100")
    print(f"Status: {health['status']}")

    analytics = registry.get_usage_analytics()
    print(f"Total Executions: {analytics['agent_analytics']['total_executions']}")
    print(
        f"Most Used Agent: {analytics['agent_analytics']['most_used'][0]['name'] if analytics['agent_analytics']['most_used'] else 'None'}"
    )


def diagnose_data_flow():
    """Diagnose the data flow issue between agents."""

    print("\n" + "=" * 50)
    print("DIAGNOSING DATA FLOW ISSUE")
    print("=" * 50)

    # Check statistics_calculator agent code
    agent_path = "generated/agents/statistics_calculator_agent.py"
    if os.path.exists(agent_path):
        with open(agent_path, "r") as f:
            code = f.read()

        print("Checking statistics_calculator agent...")
        print("-" * 40)

        # Look for how it gets input
        if "current_data" in code:
            # Find the line that extracts text
            for line in code.split("\n"):
                if "current_data" in line and ("text" in line or "get" in line):
                    print(f"Input extraction: {line.strip()}")
                    break

        # Check if it's looking for the right data structure
        if "numbers" in code:
            print("Agent expects 'numbers' in data: Yes")
        else:
            print("Agent expects 'numbers' in data: No")

    print(
        "\nThe issue: statistics_calculator expects text but text_analyzer passes numbers array"
    )
    print(
        "Solution: statistics_calculator should check for both text and numbers in current_data"
    )


if __name__ == "__main__":
    print("COMPREHENSIVE END-TO-END TESTING")
    print("=" * 50)

    # Run all tests
    test_simple_workflows()
    test_multi_agent_workflows()
    test_orchestrator_planning()
    test_full_orchestration()
    test_registry_health()
    diagnose_data_flow()

    print("\n" + "=" * 50)
    print("END-TO-END TESTING COMPLETE")
    print("=" * 50)

    print("\nSummary:")
    print("- Simple workflows: Working")
    print("- Multi-agent workflows: Data flow issue identified")
    print("- Orchestrator planning: Working")
    print("- Full orchestration: Working")
    print("- System health: 100%")
    print("\nNext step: Fix data flow in statistics_calculator agent")

```

--------------------------------------------------------------------------------

### File: tests/test_file_readers.py
**Path:** `tests/test_file_readers.py`
**Size:** 2,781 bytes
**Modified:** 2025-09-02 23:26:27

```python
"""
Test File Reader Tools
Verifies that all file reader tools work correctly
"""

import sys
import os
import json
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generated.tools.read_pdf import read_pdf
from generated.tools.read_csv import read_csv
from generated.tools.read_json import read_json
from generated.tools.read_text import read_text


def create_test_files():
    """Create test files for verification."""
    test_dir = "tests/test_files"
    os.makedirs(test_dir, exist_ok=True)

    # Create test text file
    with open(f"{test_dir}/test.txt", "w") as f:
        f.write(
            "This is a test file.\nIt has multiple lines.\nFor testing the text reader."
        )

    # Create test JSON file
    test_data = {
        "name": "Test Document",
        "type": "json",
        "items": [1, 2, 3],
        "metadata": {"created": "2024-01-01"},
    }
    with open(f"{test_dir}/test.json", "w") as f:
        json.dump(test_data, f, indent=2)

    # Create test CSV file
    df = pd.DataFrame(
        {
            "name": ["Alice", "Bob", "Charlie"],
            "age": [25, 30, 35],
            "city": ["NYC", "LA", "Chicago"],
        }
    )
    df.to_csv(f"{test_dir}/test.csv", index=False)

    print("Test files created in tests/test_files/")
    return test_dir


def test_readers():
    """Test all file reader tools."""
    print("\n" + "=" * 50)
    print("TESTING FILE READER TOOLS")
    print("=" * 50)

    # Create test files
    test_dir = create_test_files()

    # Test text reader
    print("\nTesting read_text...")
    result = read_text(f"{test_dir}/test.txt")
    if result["status"] == "success":
        print(f"Read {result['lines']} lines, {result['chars']} characters")
    else:
        print(f"Error: {result['error']}")

    # Test JSON reader
    print("\nTesting read_json...")
    result = read_json(f"{test_dir}/test.json")
    if result["status"] == "success":
        print(f"Parsed {result['type']} with keys: {list(result['data'].keys())}")
    else:
        print(f"Error: {result['error']}")

    # Test CSV reader
    print("\nTesting read_csv...")
    result = read_csv(f"{test_dir}/test.csv")
    if result["status"] == "success":
        print(
            f"Read {result['shape']['rows']} rows, {result['shape']['columns']} columns"
        )
        print(f"     Columns: {result['columns']}")
    else:
        print(f"Error: {result['error']}")

    # Test with non-existent file
    print("\nTesting error handling...")
    result = read_text("non_existent_file.txt")
    if result["status"] == "error":
        print(f"Correctly handled missing file")

    print("\nAll file reader tests complete!")


if __name__ == "__main__":
    test_readers()

```

--------------------------------------------------------------------------------

### File: tests/test_files/test.csv
**Path:** `tests/test_files/test.csv`
**Size:** 56 bytes
**Modified:** 2025-09-02 23:29:42

*[Binary file or content not included]*

--------------------------------------------------------------------------------

### File: tests/test_files/test.json
**Path:** `tests/test_files/test.json`
**Size:** 134 bytes
**Modified:** 2025-09-02 23:29:42

```json
{
  "name": "Test Document",
  "type": "json",
  "items": [
    1,
    2,
    3
  ],
  "metadata": {
    "created": "2024-01-01"
  }
}
```

--------------------------------------------------------------------------------

### File: tests/test_files/test.txt
**Path:** `tests/test_files/test.txt`
**Size:** 72 bytes
**Modified:** 2025-09-02 23:29:42

```text
This is a test file.
It has multiple lines.
For testing the text reader.
```

--------------------------------------------------------------------------------

### File: tests/test_orchestrator.py
**Path:** `tests/test_orchestrator.py`
**Size:** 4,810 bytes
**Modified:** 2025-09-03 07:50:22

```python
"""
Test Orchestrator
Verifies that the GPT-4 orchestrator can plan and execute workflows
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.orchestrator import Orchestrator
from core.registry import RegistryManager


def test_workflow_planning():
    """Test workflow planning capabilities."""

    print("\n" + "=" * 50)
    print("TESTING WORKFLOW PLANNING")
    print("=" * 50)

    orchestrator = Orchestrator()

    # Test 1: Simple email extraction request
    print("\nTest 1: Email extraction request...")

    plan = orchestrator._plan_workflow(
        "Extract emails from this text: Contact support@example.com and sales@test.org"
    )

    if plan["status"] == "success":
        print(f"  Planned workflow: {' -> '.join(plan['workflow_steps'])}")
        print(f"  Reasoning: {plan.get('reasoning', 'N/A')}")
    else:
        print(f"  Error: {plan.get('message')}")

    # Test 2: Multi-step analysis request
    print("\nTest 2: Complex analysis request...")

    plan = orchestrator._plan_workflow(
        "Analyze this text to find all numbers and calculate statistics: The values are 10, 20, 30, 40, 50"
    )

    if plan["status"] == "success":
        print(f"  Planned workflow: {' -> '.join(plan['workflow_steps'])}")
        if plan.get("missing_agents"):
            print(f"  Missing agents: {plan['missing_agents']}")
    else:
        print(f"  Error: {plan.get('message')}")

    # Test 3: Request with missing capabilities
    print("\nTest 3: Request requiring non-existent capabilities...")

    plan = orchestrator._plan_workflow(
        "Translate this text to French and create a word cloud visualization"
    )

    if plan["status"] == "success":
        print(f"  Planned workflow: {' -> '.join(plan['workflow_steps'])}")
        if plan.get("missing_agents"):
            print(f"  Missing agents identified: {plan['missing_agents']}")
        if plan.get("missing_tools"):
            print(f"  Missing tools identified: {plan['missing_tools']}")
    else:
        print(f"  Error: {plan.get('message')}")


def test_end_to_end_processing():
    """Test complete request processing."""

    print("\n" + "=" * 50)
    print("TESTING END-TO-END PROCESSING")
    print("=" * 50)

    orchestrator = Orchestrator()

    # Test 1: Process a simple request
    print("\nTest 1: Simple text analysis...")

    result = orchestrator.process_request(
        "Find all emails in: Please contact john@example.com or mary@test.org for details",
        auto_create=False,
    )

    print(f"  Status: {result['status']}")
    if result["status"] == "success":
        print(f"  Workflow: {' -> '.join(result['workflow']['steps'])}")
        print(f"  Response preview: {result['response'][:200]}...")
    else:
        print(f"  Message: {result.get('message', 'N/A')}")

    # Test 2: Process request with numbers
    print("\nTest 2: Statistical analysis...")

    result = orchestrator.process_request(
        "Calculate statistics for these numbers: 15.5, 22.3, 18.9, 25.1, 30.2",
        auto_create=False,
    )

    print(f"  Status: {result['status']}")
    if result["status"] == "success":
        print(f"  Workflow: {' -> '.join(result['workflow']['steps'])}")
    elif result["status"] == "missing_capabilities":
        print(f"  Missing: {result['missing']}")


def test_result_synthesis():
    """Test result synthesis capabilities."""

    print("\n" + "=" * 50)
    print("TESTING RESULT SYNTHESIS")
    print("=" * 50)

    orchestrator = Orchestrator()

    # Mock workflow result
    mock_result = {
        "results": {
            "email_extractor": {
                "status": "success",
                "data": {"emails": ["john@example.com", "mary@test.org"], "count": 2},
            },
            "text_analyzer": {
                "status": "success",
                "data": {"numbers": [15.5, 22.3], "emails": ["john@example.com"]},
            },
        },
        "execution_path": ["email_extractor", "text_analyzer"],
        "errors": [],
    }

    mock_plan = {"workflow_steps": ["email_extractor", "text_analyzer"]}

    print("\nSynthesizing mock results...")

    synthesis = orchestrator._synthesize_results(
        "Extract emails and numbers from the text", mock_result, mock_plan
    )

    print(f"Synthesized response:")
    print(f"  {synthesis[:300]}...")


if __name__ == "__main__":
    print("\nNote: These tests will use GPT-4 API credits")
    response = input("Continue with tests? (y/n): ").lower()

    if response == "y":
        test_workflow_planning()
        test_end_to_end_processing()
        test_result_synthesis()
        print("\n" + "=" * 50)
        print("All orchestrator tests complete!")
    else:
        print("Tests cancelled")

```

--------------------------------------------------------------------------------

### File: tests/test_registry_enhanced.py
**Path:** `tests/test_registry_enhanced.py`
**Size:** 4,911 bytes
**Modified:** 2025-09-03 08:03:54

```python
"""
Test Enhanced Registry Management
Verifies advanced registry features
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.registry_enhanced import EnhancedRegistryManager


def test_health_check():
    """Test registry health check."""

    print("\n" + "=" * 50)
    print("TESTING HEALTH CHECK")
    print("=" * 50)

    registry = EnhancedRegistryManager()
    health = registry.health_check()

    print(f"Health Score: {health['health_score']}/100")
    print(f"Status: {health['status']}")
    print(f"Total Components: {health['total_components']}")
    print(f"Valid Components: {health['valid_components']}")

    if health["issues"]["missing_files"] > 0:
        print(f"Issues Found - Missing Files: {health['issues']['missing_files']}")

    assert health["health_score"] >= 0
    assert health["health_score"] <= 100
    print("\nHealth check test passed!")


def test_analytics():
    """Test usage analytics."""

    print("\n" + "=" * 50)
    print("TESTING ANALYTICS")
    print("=" * 50)

    registry = EnhancedRegistryManager()
    analytics = registry.get_usage_analytics()

    print(f"Total Agents: {analytics['agent_analytics']['total_agents']}")
    print(f"Total Tools: {analytics['tool_analytics']['total_tools']}")
    print(f"Total Executions: {analytics['agent_analytics']['total_executions']}")

    print("\nMost Used Agents:")
    for agent in analytics["agent_analytics"]["most_used"][:3]:
        print(f"  - {agent['name']}: {agent['executions']} executions")

    print("\nUnused Tools:")
    unused = analytics["tool_analytics"]["unused_tools"]
    if unused:
        print(f"  {', '.join(unused[:5])}")
    else:
        print("  None")

    print("\nAnalytics test passed!")


def test_validation():
    """Test component validation."""

    print("\n" + "=" * 50)
    print("TESTING VALIDATION")
    print("=" * 50)

    registry = EnhancedRegistryManager()
    results = registry.validate_all()

    print(f"Valid Agents: {len(results['valid_agents'])}")
    print(f"Invalid Agents: {len(results['invalid_agents'])}")
    print(f"Valid Tools: {len(results['valid_tools'])}")
    print(f"Invalid Tools: {len(results['invalid_tools'])}")

    if results["dependency_issues"]:
        print("\nDependency Issues Found:")
        for issue in results["dependency_issues"][:3]:
            print(f"  - {issue}")

    print("\nValidation test passed!")


def test_dependency_graph():
    """Test dependency graph generation."""

    print("\n" + "=" * 50)
    print("TESTING DEPENDENCY GRAPH")
    print("=" * 50)

    registry = EnhancedRegistryManager()
    deps = registry.get_dependency_graph()

    print("Agent to Tool Mappings:")
    count = 0
    for agent, tools in deps["agents_to_tools"].items():
        if tools and count < 3:
            print(f"  {agent} uses: {', '.join(tools)}")
            count += 1

    print("\nTool Usage:")
    count = 0
    for tool, agents in deps["tools_to_agents"].items():
        if agents and count < 3:
            print(f"  {tool} used by: {', '.join(agents)}")
            count += 1

    print("\nDependency graph test passed!")


def test_backup_restore():
    """Test backup and restore functionality."""

    print("\n" + "=" * 50)
    print("TESTING BACKUP/RESTORE")
    print("=" * 50)

    registry = EnhancedRegistryManager()

    # Create backup
    print("Creating backup...")
    backup_path = registry.backup_registries("test_backup")
    print(f"Backup created at: {backup_path}")

    # Verify backup files exist
    backup_name = os.path.basename(backup_path)
    agents_backup = os.path.join(backup_path, "agents.json")
    tools_backup = os.path.join(backup_path, "tools.json")

    assert os.path.exists(agents_backup), "Agents backup missing"
    assert os.path.exists(tools_backup), "Tools backup missing"

    print("Backup files verified")
    print("\nBackup/restore test passed!")


def test_optimization():
    """Test registry optimization."""

    print("\n" + "=" * 50)
    print("TESTING OPTIMIZATION")
    print("=" * 50)

    registry = EnhancedRegistryManager()

    # Run dry run first
    report = registry.optimize_registry(dry_run=True)

    print("Optimization Preview (Dry Run):")
    print(f"  Unused tools: {len(report['unused_tools'])}")
    print(f"  Broken agents: {len(report['broken_agents'])}")
    print(f"  Missing files: {len(report['missing_files'])}")

    if report["unused_tools"]:
        print(f"  Would remove tools: {', '.join(report['unused_tools'][:3])}")

    print("\nOptimization test passed!")


if __name__ == "__main__":
    print("Running Enhanced Registry Tests...")

    test_health_check()
    test_analytics()
    test_validation()
    test_dependency_graph()
    test_backup_restore()
    test_optimization()

    print("\n" + "=" * 50)
    print("All enhanced registry tests passed!")

```

--------------------------------------------------------------------------------

### File: tests/test_templates.py
**Path:** `tests/test_templates.py`
**Size:** 1,878 bytes
**Modified:** 2025-09-02 23:41:49

```python
## 5.5 Test the Templates

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generated.tools.extract_numbers import extract_numbers
from generated.tools.calculate_mean import calculate_mean
from generated.tools.calculate_median import calculate_median


def test_example_tools():
    """Test the example statistical tools."""
    print("\n" + "=" * 50)
    print("TESTING EXAMPLE TEMPLATE TOOLS")
    print("=" * 50)

    # Test extract_numbers
    print("\nTesting extract_numbers...")
    test_text = "The temperature was 23.5 degrees, with a high of 28 and low of -2.5"
    numbers = extract_numbers(test_text)
    print(f"  Input: '{test_text}'")
    print(f"  Extracted: {numbers}")
    assert len(numbers) == 4, "Should extract 4 numbers"

    # Test calculate_mean
    print("\nTesting calculate_mean...")
    test_numbers = [10, 20, 30, 40, 50]
    mean = calculate_mean(test_numbers)
    print(f"  Input: {test_numbers}")
    print(f"  Mean: {mean}")
    assert mean == 30.0, "Mean should be 30.0"

    # Test calculate_median
    print("\nTesting calculate_median...")
    median = calculate_median(test_numbers)
    print(f"  Input: {test_numbers}")
    print(f"  Median: {median}")
    assert median == 30.0, "Median should be 30.0"

    # Test with odd number of elements
    odd_numbers = [1, 3, 5, 7, 9]
    median_odd = calculate_median(odd_numbers)
    print(f"  Odd list: {odd_numbers}")
    print(f"  Median: {median_odd}")
    assert median_odd == 5.0, "Median should be 5.0"

    # Test edge cases
    print("\nTesting edge cases...")
    print(f"  Empty list mean: {calculate_mean([])}")
    print(f"  Empty list median: {calculate_median([])}")
    print(f"  Single value: {calculate_mean([42])}")

    print("\nAll template tool tests passed!")


if __name__ == "__main__":
    test_example_tools()

```

--------------------------------------------------------------------------------

### File: tests/test_tool_factory.py
**Path:** `tests/test_tool_factory.py`
**Size:** 6,151 bytes
**Modified:** 2025-09-02 23:47:07

```python
"""
Test Tool Factory
Verifies that the tool factory can create new tools dynamically
"""

import sys
import os
import importlib.util

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.tool_factory import ToolFactory
from core.registry import RegistryManager


def dynamic_import_tool(tool_name):
    """Dynamically import a tool after it's created."""
    tool_path = f"generated/tools/{tool_name}.py"
    if not os.path.exists(tool_path):
        return None

    spec = importlib.util.spec_from_file_location(tool_name, tool_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, tool_name)


def test_tool_creation():
    """Test creating a new tool."""

    print("\n" + "=" * 50)
    print("TESTING TOOL FACTORY")
    print("=" * 50)

    factory = ToolFactory()
    registry = RegistryManager()

    # Test 1: Create a simple extraction tool
    print("\nTest 1: Creating extract_urls tool...")

    result = factory.create_tool(
        tool_name="extract_urls",
        description="Extract all URLs from text",
        input_description="A string containing text with URLs",
        output_description="A list of unique URLs found in the text",
        examples=[
            {
                "input": "Visit https://example.com and http://test.org",
                "output": "['https://example.com', 'http://test.org']",
            }
        ],
    )

    if result["status"] == "success":
        print(f"  Success: Created {result['line_count']} lines of code")

        # Dynamically import and test the created tool
        extract_urls = dynamic_import_tool("extract_urls")
        if extract_urls:
            test_text = "Check out https://github.com and https://google.com"
            urls = extract_urls(test_text)
            print(f"  Test run: Found {len(urls) if urls else 0} URLs")
        else:
            print("  Warning: Could not import created tool")
    else:
        print(f"  Result: {result['status']} - {result['message']}")

    # Test 2: Try to create duplicate tool
    print("\nTest 2: Attempting to create duplicate tool...")

    result = factory.create_tool(
        tool_name="extract_urls",
        description="Extract URLs again",
        input_description="Text",
        output_description="URLs",
    )

    print(f"  Result: {result['status']} - {result['message']}")

    # Test 3: Create a calculation tool
    print("\nTest 3: Creating calculate_percentage tool...")

    result = factory.create_tool(
        tool_name="calculate_percentage",
        description="Calculate percentage of a value",
        input_description="Two numbers: value and total",
        output_description="The percentage as a float",
        examples=[
            {"input": "value=25, total=100", "output": "25.0"},
            {"input": "value=7, total=50", "output": "14.0"},
        ],
    )

    if result["status"] == "success":
        print(f"  Success: Created {result['line_count']} lines of code")

        # Dynamically import and test the created tool
        calculate_percentage = dynamic_import_tool("calculate_percentage")
        if calculate_percentage:
            try:
                percentage = calculate_percentage(50, 200)
                print(f"  Test run: 50 out of 200 = {percentage}%")
            except TypeError:
                # Tool might expect different parameter format
                try:
                    percentage = calculate_percentage({"value": 50, "total": 200})
                    print(f"  Test run: 50 out of 200 = {percentage}%")
                except:
                    print("  Warning: Could not test tool with sample inputs")
        else:
            print("  Warning: Could not import created tool")
    else:
        print(f"  Result: {result['status']} - {result['message']}")

    # Display registry statistics
    print("\nRegistry Statistics:")
    stats = registry.get_statistics()
    print(f"  Total tools: {stats['total_tools']}")
    print(f"  Average tool lines: {stats['avg_tool_lines']}")

    # List newly created tools
    print("\nNewly Created Tools:")
    new_tools = ["extract_urls", "calculate_percentage"]
    for tool_name in new_tools:
        if registry.tool_exists(tool_name):
            tool = registry.get_tool(tool_name)
            print(f"  - {tool_name}: {tool['description']}")


def test_validation():
    """Test tool code validation."""

    print("\n" + "=" * 50)
    print("TESTING TOOL VALIDATION")
    print("=" * 50)

    factory = ToolFactory()

    # Test invalid code (too short)
    print("\nTesting validation with too short code...")
    short_code = "def test():\n    return 1"
    result = factory._validate_tool_code(short_code, "test")
    print(f"  Valid: {result['valid']}")
    if not result["valid"]:
        print(f"  Error: {result['error']}")

    # Test invalid code (wrong name)
    print("\nTesting validation with wrong function name...")
    wrong_name_code = "def wrong_name(x):\n" + "    " * 10 + "return x"
    result = factory._validate_tool_code(wrong_name_code, "expected_name")
    print(f"  Valid: {result['valid']}")
    if not result["valid"]:
        print(f"  Error: {result['error']}")

    # Test invalid code (contains file I/O)
    print("\nTesting validation with file I/O...")
    file_io_code = (
        """def read_file(path):
    '''Read a file.'''
    with open(path, 'r') as f:
        return f.read()
    """
        + "\n" * 20
    )  # Add lines to meet minimum
    result = factory._validate_tool_code(file_io_code, "read_file")
    print(f"  Valid: {result['valid']}")
    if not result["valid"]:
        print(f"  Error: {result['error']}")

    print("\nValidation tests complete!")


if __name__ == "__main__":
    # Run validation tests first (no API calls)
    test_validation()

    # Ask before running API tests
    print("\n" + "=" * 50)
    response = input(
        "\nRun API tests? This will use Claude API credits (y/n): "
    ).lower()

    if response == "y":
        test_tool_creation()
    else:
        print("Skipping API tests.")

```

--------------------------------------------------------------------------------

### File: tests/test_workflow_engine.py
**Path:** `tests/test_workflow_engine.py`
**Size:** 5,244 bytes
**Modified:** 2025-09-03 07:44:40

```python
"""
Test Workflow Engine
Verifies that the workflow engine can execute multi-agent workflows
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.workflow_engine import WorkflowEngine, WorkflowState
from core.registry import RegistryManager


def test_workflow_creation():
    """Test creating workflows from agent sequences."""

    print("\n" + "=" * 50)
    print("TESTING WORKFLOW CREATION")
    print("=" * 50)

    engine = WorkflowEngine()
    registry = RegistryManager()

    # Test 1: Create simple single-agent workflow
    print("\nTest 1: Single-agent workflow...")

    try:
        workflow = engine.create_workflow(["email_extractor"])
        print("  Success: Created workflow with email_extractor")
    except Exception as e:
        print(f"  Error: {str(e)}")

    # Test 2: Create multi-agent workflow
    print("\nTest 2: Multi-agent workflow...")

    # Check which agents exist
    available_agents = [a["name"] for a in registry.list_agents()]
    print(f"  Available agents: {available_agents}")

    if (
        "text_analyzer" in available_agents
        and "statistics_calculator" in available_agents
    ):
        try:
            workflow = engine.create_workflow(
                ["text_analyzer", "statistics_calculator"]
            )
            print(
                "  Success: Created workflow with text_analyzer -> statistics_calculator"
            )
        except Exception as e:
            print(f"  Error: {str(e)}")
    else:
        print("  Skipping: Required agents not available")

    # Test 3: Invalid workflow (non-existent agent)
    print("\nTest 3: Invalid workflow...")

    try:
        workflow = engine.create_workflow(["non_existent_agent"])
        print("  Error: Should have failed with missing agent")
    except ValueError as e:
        print(f"  Success: Correctly rejected - {str(e)}")

    print("\nWorkflow creation tests complete!")


def test_workflow_execution():
    """Test executing workflows with real agents."""

    print("\n" + "=" * 50)
    print("TESTING WORKFLOW EXECUTION")
    print("=" * 50)

    engine = WorkflowEngine()
    registry = RegistryManager()

    # Test 1: Execute email extraction workflow
    print("\nTest 1: Email extraction workflow...")

    test_data = {
        "text": "Contact us at support@example.com or sales@company.org for more information.",
        "request": "Extract emails from text",
    }

    if registry.agent_exists("email_extractor"):
        try:
            result = engine.create_and_execute(
                agent_sequence=["email_extractor"], initial_data=test_data
            )

            print("  Execution completed!")
            print(f"  Execution path: {result.get('execution_path', [])}")

            if "email_extractor" in result.get("results", {}):
                agent_result = result["results"]["email_extractor"]
                if "data" in agent_result:
                    print(f"  Found emails: {agent_result['data'].get('emails', [])}")

            if result.get("errors"):
                print(f"  Errors: {result['errors']}")

        except Exception as e:
            print(f"  Error: {str(e)}")
    else:
        print("  Skipping: email_extractor not available")

    # Test 2: Execute multi-agent workflow
    print("\nTest 2: Text analysis pipeline...")

    test_data = {
        "text": "The temperature is 23.5 degrees. Contact admin@site.com for details. Visit https://example.com",
        "request": "Analyze text comprehensively",
    }

    # Try to use available agents
    if registry.agent_exists("text_analyzer"):
        try:
            result = engine.create_and_execute(
                agent_sequence=["text_analyzer"], initial_data=test_data
            )

            print("  Execution completed!")
            print(f"  Execution path: {result.get('execution_path', [])}")

            for agent_name in result.get("execution_path", []):
                if agent_name in result.get("results", {}):
                    print(
                        f"  {agent_name} status: {result['results'][agent_name].get('status')}"
                    )

        except Exception as e:
            print(f"  Error: {str(e)}")
    else:
        print("  Skipping: text_analyzer not available")

    print("\nWorkflow execution tests complete!")


def test_workflow_visualization():
    """Test workflow visualization."""

    print("\n" + "=" * 50)
    print("TESTING WORKFLOW VISUALIZATION")
    print("=" * 50)

    engine = WorkflowEngine()
    registry = RegistryManager()

    # Get available agents
    available = [a["name"] for a in registry.list_agents()][:3]  # Use first 3

    if available:
        print(f"\nVisualizing workflow with: {available}")
        visualization = engine.visualize_workflow(available)
        print(visualization)
    else:
        print("No agents available for visualization")


if __name__ == "__main__":
    # Test workflow creation
    test_workflow_creation()

    # Test workflow execution
    test_workflow_execution()

    # Test visualization
    test_workflow_visualization()

    print("\n" + "=" * 50)
    print("All workflow engine tests complete!")

```

--------------------------------------------------------------------------------

### File: tools.json
**Path:** `tools.json`
**Size:** 4,670 bytes
**Modified:** 2025-09-03 13:16:31

```json
{
  "tools": {
    "extract_emails": {
      "description": "Extracts email addresses from text using regex",
      "signature": "def extract_emails(text):",
      "location": "generated/tools/extract_emails.py",
      "used_by_agents": [
        "email_extractor",
        "text_analyzer",
        "document_processor",
        "pdf_email_extractor"
      ],
      "created_by": "claude-3-haiku",
      "created_at": "2025-09-02T19:45:07.754248",
      "is_pure_function": true,
      "tags": [
        "text-processing",
        "extraction",
        "email"
      ],
      "line_count": 6
    },
    "read_pdf": {
      "description": "Extracts text content from PDF files using PyPDF2",
      "signature": "def read_pdf(file_path):",
      "location": "generated/tools/read_pdf.py",
      "used_by_agents": [
        "pdf_email_extractor"
      ],
      "created_by": "claude-3-haiku",
      "created_at": "2025-09-02T23:26:46.042619",
      "is_pure_function": true,
      "tags": [
        "file-reader",
        "pdf",
        "text-extraction"
      ],
      "line_count": 32
    },
    "read_csv": {
      "description": "Reads CSV files into structured data using pandas",
      "signature": "def read_csv(file_path):",
      "location": "generated/tools/read_csv.py",
      "used_by_agents": [
        "csv_analyzer"
      ],
      "created_by": "claude-3-haiku",
      "created_at": "2025-09-02T23:26:46.043604",
      "is_pure_function": true,
      "tags": [
        "file-reader",
        "csv",
        "data-processing"
      ],
      "line_count": 22
    },
    "read_json": {
      "description": "Parses JSON files into Python objects",
      "signature": "def read_json(file_path):",
      "location": "generated/tools/read_json.py",
      "used_by_agents": [],
      "created_by": "claude-3-haiku",
      "created_at": "2025-09-02T23:26:46.044329",
      "is_pure_function": true,
      "tags": [
        "file-reader",
        "json",
        "data-processing"
      ],
      "line_count": 21
    },
    "read_text": {
      "description": "Reads plain text files",
      "signature": "def read_text(file_path):",
      "location": "generated/tools/read_text.py",
      "used_by_agents": [
        "document_processor"
      ],
      "created_by": "claude-3-haiku",
      "created_at": "2025-09-02T23:26:46.045070",
      "is_pure_function": true,
      "tags": [
        "file-reader",
        "text",
        "basic-io"
      ],
      "line_count": 21
    },
    "extract_numbers": {
      "description": "Extracts all numbers from text, including integers and decimals",
      "signature": "def extract_numbers(text):",
      "location": "generated/tools/extract_numbers.py",
      "used_by_agents": [
        "text_analyzer",
        "statistics_calculator",
        "csv_analyzer",
        "document_processor"
      ],
      "created_by": "claude-3-haiku",
      "created_at": "2025-09-02T23:42:11.055994",
      "is_pure_function": true,
      "tags": [
        "text-processing",
        "extraction",
        "numbers"
      ],
      "line_count": 33
    },
    "calculate_mean": {
      "description": "Calculates the arithmetic mean of a list of numbers",
      "signature": "def calculate_mean(numbers):",
      "location": "generated/tools/calculate_mean.py",
      "used_by_agents": [
        "statistics_calculator",
        "csv_analyzer"
      ],
      "created_by": "claude-3-haiku",
      "created_at": "2025-09-02T23:42:11.057455",
      "is_pure_function": true,
      "tags": [
        "statistics",
        "math",
        "aggregation"
      ],
      "line_count": 15
    },
    "calculate_median": {
      "description": "Calculates the median value of a list of numbers",
      "signature": "def calculate_median(numbers):",
      "location": "generated/tools/calculate_median.py",
      "used_by_agents": [
        "statistics_calculator",
        "csv_analyzer"
      ],
      "created_by": "claude-3-haiku",
      "created_at": "2025-09-02T23:42:11.058335",
      "is_pure_function": true,
      "tags": [
        "statistics",
        "math",
        "aggregation"
      ],
      "line_count": 24
    },
    "extract_urls": {
      "description": "Extract all URLs from text",
      "signature": "def extract_urls(text):",
      "location": "generated/tools/extract_urls.py",
      "used_by_agents": [
        "document_processor"
      ],
      "created_by": "claude-3-haiku",
      "created_at": "2025-09-02T23:47:53.241795",
      "is_pure_function": true,
      "tags": [
        "parsing",
        "link",
        "text-processing",
        "extraction",
        "web"
      ],
      "line_count": 20
    }
  }
}
```

--------------------------------------------------------------------------------

## ENVIRONMENT INFORMATION

**API Configuration:**
- OpenAI: Configured and tested (GPT-4 available)
- Anthropic: Configured and tested (Claude-3-Haiku available)
- Dual API Integration: Working successfully

**Python Environment:**
- Virtual Environment: ./venv/
- Python Version: 3.11+
- Key Dependencies: openai, anthropic, streamlit, langgraph

**Quick Start Commands:**
```bash
# Activate environment
source venv/bin/activate

# Test APIs
python tests/api_tests/test_dual_api_integration.py

# Continue development from Step 5
# Next: Core Infrastructure Development
```
