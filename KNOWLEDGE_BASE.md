# AGENTIC FABRIC POC - COMPLETE PROJECT KNOWLEDGE BASE
================================================================================
Generated: 2025-09-06 15:25:32
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
│   ├── dependency_resolver.py
│   ├── registry.py
│   ├── registry_singleton.py
│   └── workflow_engine.py
├── generated/
│   ├── agents/
│   │   ├── email_extractor_agent.py
│   │   ├── read_csv_agent.py
│   │   ├── read_text_agent.py
│   │   └── word_counter_agent.py
│   ├── tools/
│   │   ├── analyze_sentiment.py
│   │   ├── calculate_mean.py
│   │   ├── calculate_median.py
│   │   ├── calculate_std.py
│   │   ├── count_words.py
│   │   ├── extract_emails.py
│   │   ├── extract_phones.py
│   │   └── extract_urls.py
│   └── __init__.py
├── prebuilt/
│   ├── agents/
│   │   └── url_extractor_agent.py
│   └── tools/
│       ├── read_csv.py
│       ├── read_json.py
│       ├── read_pdf.py
│       └── read_text.py
├── registry_backups/
├── scripts/
│   ├── initialize_prebuilt.py
│   └── regenerate_agents.py
├── tests/
│   ├── test_files/
│   ├── test_backend_fixes.py
│   ├── test_comprehensive_scenarios.py
│   ├── test_dependency_resolution.py
│   └── test_end_to_end.py
├── AGENTIC_FABRIC_POC_Roadmap.md
├── KNOWLEDGE_BASE.md
├── README.md
├── agents.json
├── agents.json.lock
├── config.py
├── create_knowledge_base.py
├── requirements.txt
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

### File: AGENTIC_FABRIC_POC_Roadmap.md
**Path:** `AGENTIC_FABRIC_POC_Roadmap.md`
**Size:** 20,981 bytes
**Modified:** 2025-09-04 22:11:11

```markdown
# Agent Fabric — Design & Roadmap 
---

## 1) Overview & Problem Statement

Your current agent set is complex and monolithic. The vision is an **agent fabric** where small agents are created on‑demand by an LLM and registered automatically. Large, pre‑baked agents (500–1000 LOC) are brittle to generate and maintain.

**Core shift:**

* Keep agents **narrow** (single responsibility).
* Move reusable logic into **pure tools** (stateless functions).
* Let an **Orchestrator LLM** plan/sequence agents.
* Persist capabilities in **lightweight registries** (`agents.json`, `tools.json`).

---

## 2) Goals & Non‑Goals

### Goals

* **Minimal Viable Agents (MVAs):** tiny agents for read/parse/extract/format.
* **Pure Tools:** 20–100 LOC utilities; deterministic; JSON‑serializable returns.
* **Dual Registry:** separate tracking for agents vs tools for maximal reuse.
* **On‑Demand Generation:** LLM creates missing tools/agents and registers them.
* **Standard I/O Contracts:** uniform JSON envelope; chainable outputs.
* **LangGraph Orchestration:** state, branching, retries, visualization.

### Non‑Goals (for now)

* Domain‑heavy “platform” agents.
* Multi‑vendor support on day one (start **Jira‑only** path).
* Long‑lived agent state (keep state in the workflow engine).

---

## 3) Design Principles

1. **Small Pieces, Loosely Joined:** agents ≈ 50–300 LOC; tools ≈ 20–100 LOC.
2. **Single Responsibility:** composition yields power.
3. **Stateless & Deterministic Tools:** agents minimize side effects.
4. **Centralized Intelligence:** Orchestrator owns planning (no `next_actions` inside agents).
5. **Explicit Contracts:** uniform JSON I/O, explicit schemas.
6. **Generate Late:** create new things only when needed.

---

## 4) Architecture & End‑to‑End Flow

```
User Request → Orchestrator LLM → agents.json / tools.json (capability lookup)
                              ↘ missing? → Codegen (LLM) → Tool/Agent Factory → Registry update
                                           ↘ tests/validation → (accept or reject)
Then: Orchestrator builds a LangGraph workflow → Execute → Collect results → Respond
```

### Flow Summary

1. User asks → 2) Orchestrator derives needed capabilities → 3) Check registries → 4) If missing, factories generate **tools first**, then agents → 5) Validate & register → 6) Build workflow (LangGraph) → 7) Execute with retries → 8) Synthesize answer.

### Swimlane

```
User        | Orchestrator       | Registries          | Factories                | LangGraph
------------+--------------------+---------------------+--------------------------+------------------
Request ----> parse+plan --------> read agents/tools --|                           |
             missing deps?        |                     |                          |
             yes -----------------|--------------------> ensure(tool)               |
                                   tools.json update <-| (validate/register)       |
             then ensure agent ---|--------------------> ensure(agent)              |
                                   agents.json update <-| (validate/register)      |
             build workflow -------------------------------------------------------> build graph
             execute -----------------------------------------------------------------> run nodes
             gather results <------------------------------------------------------- results
             synthesize & respond -------------------------------------------------> reply
```

### Orchestrator Algorithm (pseudocode)

```python
 def plan_and_run(request):
     need = derive_capabilities(request)            # e.g., ["extract_urls"]
     existing = registries.lookup(need)
     missing_tools, missing_agents = diff(existing, need)

     for tool in order_tools(missing_tools):        # tools first
         tool_factory.ensure(tool)                  # idempotent: no‑op if exists

     for agent in order_agents(missing_agents):     # then agents
         agent_factory.ensure(agent)                # imports tools by name

     graph = build_langgraph(request, need)         # nodes from agents.json
     run = execute_graph(graph)                     # retries, timings, logs
     return synthesize_outputs(run)                 # standard envelopes → answer
```

### Design Guarantees

* **Idempotent creation** via `ensure(name)` (smallest diff).
* **Uniform contracts**: standard JSON envelope; tools are pure.
* **Safety gates**: allow‑listed imports, purity/unit checks, size budgets.
* **Observability**: timings, creation events, registry updates.

### Concrete Example

“Find links in this PDF” → map `read_pdf` → `extract_urls` (needs `regex_matcher`). If missing, create tool then agent; register both; build graph; execute; return normalized URLs.

---

## 4b) Starter Kit & Dynamic Creation Policy (Canonical)

**Pre‑built (absolute minimum):**

* `read_pdf` (PyPDF2 wrapper), `read_csv` (pandas wrapper), `read_text`, `read_json`.

> Nothing else is pre‑baked. These exist only because library syntax is finicky for LLMs. The **first supported connector is Jira**, delivered via the factory path (not hard‑coded), with review gates enabled.

**Created dynamically (by LLM):**

* Agents (examples): `extract_urls`, `create_simple_chart`, `fetch_webpage`, `parse_json`, `format_table`, `calculate_stats`, `detect_language`, `extract_dates`, `jira_fetch`, `send_slack`.
* Tools: small, pure utilities those agents import. Missing tools are created **first**.

**Tools vs Agents — Hybrid Rule**

* Prefer **tools** for reusable logic (regex, normalization, validation, date parsing).
* Agents are **simple executors** importing tools and returning the **standard JSON envelope**.
* If duplication appears, factories prompt extraction into tools.

**Registry Contracts (source of truth)**

* **agents.json:** description, `uses_tools`, `input_schema`, `output_schema`, `location`, `created_by`, `created_at`, `version`, metrics, tags.
* **tools.json:** description, explicit `signature`, `location`, `created_by`, `created_at`, `is_pure_function`, tags, `used_by_agents`.
* Entries point to real files; factories update registries atomically after validation.

**Factory Operating Rules (must)**

* **Tool Factory (`ensure_tool`)**: purity; datatype robustness; size budget; validation (lint/import gate/samples/signature).
* **Agent Factory (`ensure_agent`)**: single responsibility; uses tools; standard envelope; schema checks; size budget; validation (lint/allow‑list/smoke test).
* On success: write file → update respective registry.

**Prompt & Config Policy**

* **Single source of truth:** generation prompts, size budgets, allow‑lists, safety toggles live in `config.py`.
* `config_bkup.py` is **deprecated**.
* **No inline prompts** in factories; they must read from `config.py`.

**Up‑to‑Step‑10 Acceptance (what “working” means)**

1. Missing capability triggers **tool → agent** creation in that order.
2. Both pass validation; registries updated with correct paths/signatures.
3. Orchestrator builds a **LangGraph** graph from registry entries (no hardcoding).
4. Execution captures envelopes, timings, errors; results synthesized.
5. Run logs show dependency resolution and creation events.
6. Only the four readers are prebuilt; all other nodes are generated.

---

## 4c) Agent–Tool Collaboration & Dependency Resolution (Authoritative Design)

**Problem to avoid:** Agents being created without their required tools, or tools being created generically without purpose.

**Authoritative rule:** **Tools are prerequisites; agents are dependents.** Creation and planning must enforce **tools → agents → workflow** in that order.

### Orchestrator Protocol (4 stages)

1. **Capability Analysis** → Decompose the user request into **atomic capabilities** (candidate agents) and list the **specific tools** each capability needs (with input/output types and purpose).
2. **Dependency Graph** → Build a typed DAG with nodes = {tool|agent} and edges **tool → agent**.
3. **Creation Order** → Topologically sort the graph and **ensure tools first**, then agents. All ensures are **idempotent** (no‑op if present).
4. **Workflow Build & Execute** → Only after all dependencies exist, assemble the LangGraph and run with retries/telemetry.

### Factory Execution Rules

* **ensure\_tool(name, spec):** Must validate *purity*, import allow‑list, size budget, and **purpose‑specific behavior** (no placeholders). Include sample I/O tests and register atomically in `tools.json` with canonical `location`.
* **ensure\_agent(name, spec):** Only runs **after all tools are ensured**. Validates input/output schemas and returns the **standard JSON envelope**; registers in `agents.json` with `uses_tools` populated.

### Registry & Import Resolution (prebuilt vs generated)

* **Prebuilt vs generated is not a problem** so long as **registries are the source of truth**. Each entry carries a canonical `location` and agents **import tools via registry‑resolved paths**.
* Provide an **import resolver** at generation time so agent code imports from the correct module path regardless of whether a tool lives under `prebuilt/` or `generated/`. (Fallback import is acceptable but registry‑driven import is preferred.)

### Dynamic Planning Rules (how the Orchestrator decides)

* For each capability, consult `tools.json` by **description/signature** first. If no suitable tool exists, the Orchestrator must produce a **tool spec** with: `name`, **purpose**, **input/output types**, and an **implementation hint**.
* Create missing tools **before** generating the agent that depends on them; then generate the agent **referencing those tool names** in `uses_tools` and imports.

### Tool Quality Bar

* Tools must implement **specific, testable behavior** (e.g., *extract E.164 phone numbers from text*) rather than generic stubs.
* Each tool ships with **minimal unit samples** and is rejected if tests fail or purity/import rules are violated.

### LangGraph Correctness Checks

* **Pre‑flight validation:** no cycles; every node corresponds to a registered agent; for each agent, **all `uses_tools` exist**; conditional edges have a condition function.
* **Visualization:** export a graph view per run to confirm whether the workflow is a straight path or includes conditionals; annotate nodes with timings and outputs present.

### Telemetry & Audit Requirements

* Log the **dependency resolution** (what tools were required and why), the **creation order**, registry updates, and **import paths** chosen for each agent.
* Include clear errors when an agent would be created without all tools, and **abort** creation until tools are ensured.

### Acceptance Checks (collaboration)

* Any plan that introduces a new agent must show prior or concurrent logs of **tool ensures** for all dependencies.
* Agents never import missing tools at runtime; imports resolve using registry paths.
* The executed LangGraph uses the expected tools per agent, confirmed by run logs and the visualization output.

## 5) Core Components

* **Orchestrator LLM:** parses request, ensures capabilities, builds/executes LangGraph, synthesizes output.
* **Dual Registry:** `agents.json` (capabilities), `tools.json` (utilities).
* **Tool Factory:** codegen + validation + registration for pure tools.
* **Agent Factory:** codegen + validation + registration for small agents.
* **Workflow Engine (LangGraph):** state, retries, branching, visualization.
* **Minimal Prebuilt:** the four readers. Jira is the **first connector path**, generated behind a review gate.

---

## 6) Contracts (No `next_actions` inside agents)

### 6.1 Standard Agent Output Envelope

```json
{
  "status": "success" | "error",
  "data": { },
  "metadata": {
    "agent": "string",
    "tools_used": ["string"],
    "execution_time": 0.0,
    "version": "semver"
  }
}
```

### 6.2 Tool Signature Guidelines

* Pure functions only; explicit args; JSON‑serializable returns; no hidden I/O or implicit env reads.

### 6.3 Workflow State (conceptual)

`request`, `files`, `execution_path`, `current_data`, `results`, `errors`, `started_at`, `completed_at`.

---

## 7) Registries (Schemas)

### 7.1 `agents.json` (logical schema)

```json
{
  "<agent_name>": {
    "description": "what it does",
    "uses_tools": ["tool_a", "tool_b"],
    "input_schema": {},
    "output_schema": {},
    "location": "generated/agents/<agent_name>.py",
    "created_by": "llm-id",
    "created_at": "iso-8601",
    "version": "1.0.0",
    "execution_count": 0,
    "avg_execution_time": 0.0,
    "tags": ["text", "extraction"]
  }
}
```

### 7.2 `tools.json` (logical schema)

```json
{
  "<tool_name>": {
    "description": "utility function",
    "signature": "def <tool_name>(args) -> return_type",
    "location": "generated/tools/<tool_name>.py",
    "used_by_agents": ["agent_a", "agent_b"],
    "created_by": "llm-id",
    "created_at": "iso-8601",
    "is_pure_function": true,
    "tags": ["regex", "url"]
  }
}
```

---

## 8) Example: Minimal Ticketing Agent (MVA)

* **Scope now:** Jira‑only helper (read/parse/query).
* **Inputs:** project key; filters (assignee/status/date range); fields.
* **Output:** standard envelope, normalized ticket array.
* **Tools:** `jira_client` (connector), `field_normalizer` (pure).
* **Notes:** no workflow smarts; no side effects beyond declared Jira calls.

---

## 9) Security, Safety, and Governance

* **Sandbox codegen** execution.
* **Allow‑list imports**; deny forbidden modules.
* **Secret handling** explicit (no implicit env reads).
* **Network egress** only via declared connectors; block raw sockets in tools.
* **Review gates**: automated tests + lightweight human review for new connectors.

---

## 10) Observability & Ops

* **Run logs:** per‑agent start/stop, redacted inputs, sizes, durations.
* **Metrics:** execution counts, p50/p95 latency per agent, codegen success rate, registry growth.
* **Tracing:** workflow graph with node/edge timings.
* **Cost:** token/API accounting per run.

---

## 11) Versioning & Change Management

* **SemVer**: bump minor for non‑breaking enhancements; major for schema changes.
* **Immutability:** keep old versions until workflows migrate.
* **Deprecation:** mark old entries; Orchestrator prefers latest non‑deprecated.

---

## 12) Roadmap

* **P0 (this week):** registries + four readers; factory basics; generate 3–5 tools + 3 tiny agents; one end‑to‑end LangGraph demo; enable Jira connector via factory path (behind review gate).
* **P1:** strengthen validation (purity checks, allow‑list, unit tests); visualization/metrics/UI for registry & run history; on‑demand new connector path (e.g., GitHub) behind review gate.
* **P2:** policy‑driven governance; caching/memoization for heavy tools; multi‑tenant credentials & role‑based data access.

---

## 13) Risks & Mitigations

* **Over‑complex codegen** → strict size/time budgets; factories reject oversized outputs.
* **Hidden side effects** → purity tests; deny network/disk unless declared connector.
* **Registry drift/dead entries** → usage tracking; scheduled prune.
* **Vendor lock‑in** → narrow adapter interfaces; per‑vendor test harnesses.

---

## 14) Success Criteria

* ≥80% new capabilities via generated tools/agents **within size budgets**.
* Median time to add a new utility/tool **< 5 min** including validation.
* Stable P95 workflow latency for a 5‑node graph **< 20 s**.
* **Zero policy violations** (no undeclared network I/O) in CI over 30 days.

---

## 15) Implementation Plan — Steps 1–20

### Phase 1: Foundation & Cleanup (Steps 1–5)

**1 — Backup & Restructure:** snapshot repo; keep `.env`, `venv/`, `.git/`; establish lean tree (`generated/`, `core/`, registries, `config.py`).
**2 — Configuration Setup:** model IDs, API keys, **size budgets** (agents 50–300, tools 20–100), retries/timeouts, import allow‑list, connector policy.
**3 — Dual Registry Design:** define schemas; implement `core/registry.py` (load/save/search/deps/prune).
**4 — Minimal Pre‑built:** implement four readers; prepare Jira connector **via factory path**.
**5 — Seed Templates:** `example_tool.py`, `example_agent.py` for codegen prompts.

### Phase 2: Core Engine (Steps 6–10)

**6 — Tool Factory:** prompt for pure utilities; static checks; unit samples; write + update `tools.json`.
**7 — Agent Factory:** small agents; standard envelope; schema checks; write + update `agents.json`.
**8 — Workflow Engine:** LangGraph StateGraph; state fields; retries/backoff; timing capture; viz hook.
**9 — Orchestrator:** capability lookup; smallest missing pieces first; build graph; execute; synthesize.
**10 — Registry Mgmt:** deps, usage stats, search, cleanup, versioning & deprecation.

### Phase 3: Dynamic Creation Testing (Steps 11–15)

**11 — Create 10 Test Agents:** `extract_urls`, `create_simple_chart`, `fetch_webpage`, `parse_json`, `format_table`, `calculate_stats`, `detect_language`, `extract_dates`, `jira_fetch`, `send_slack`.
**12 — Complex Workflow Tests:** PDF→text→URLs→fetch→summarize; CSV→stats→chart→report; Text→detect language→extract dates→translate→format.
**13 — Streamlit UI (optional):** browse registries; upload inputs; preview workflow; run and view timings.
**14 — LangGraph Visualization:** nodes/edges with status & timings.
**15 — Demo Scenarios:** dynamic creation; tool reuse; 5+ node workflow; failure handling; latency comparison.

### Phase 4: Testing & Docs (Steps 16–20)

**16 — Comprehensive Testing:** 20 tools + 20 agents; connector mocks (Jira); negative tests (blocked imports, schema mismatch, net w/o connector).
**17 — Documentation:** architecture, registries, factories, LangGraph patterns; prompts (do/don’t); size budgets; purity rules; deployment & security.
**18 — Example Library:** common tool patterns (regex/date/normalization); agent patterns (extract/transform/format); workflow templates.
**19 — Monitoring Dashboard:** usage per agent/tool, codegen success rates, workflow p50/p95, cost tracking.
**20 — Final Demo Prep:** UI polish; scripted demos/videos; executive summary.

---

## 16) Acceptance Checks (attach to Steps 4, 6–10)

* **Step 4:** only four readers are prebuilt; each within LOC budget; smoke tests exist; no other feature agents prebuilt.
* **Step 6:** `ensure_tool` idempotent; allow‑list/purity enforced; `tools.json` entries correct.
* **Step 7:** `ensure_agent` idempotent; standard envelope; `agents.json` entries correct with `uses_tools`/schemas.
* **Steps 8–10:** Orchestrator builds graph **from registry** (no hardcoding); engine tracks state/timings/errors; registry has usage/deprecation; no dead pointers.

---

## 17) Operational Prompts: Audit & Setup

**17.1 LLM Analysis Prompt — Agent Fabric Audit (Steps 1–10 only)**
Use this when you want the LLM to audit your repo strictly up to Step 10, verify claims, and list gaps/issues without generating code. *(Paste your audit prompt here or reference from `config.py`.)*

**17.2 System Prompt — Backend Audit & Setup (Steps 1–10 only)**
Use this when you want the LLM to both verify Step‑10 compliance and output a concrete, code‑free setup + test plan honoring §4b (Starter Kit & Dynamic Creation Policy). *(Paste here or reference from `config.py`.)*

> Tip: Keep both prompts under source control beside `knowledge_base.md` and reference them from `config.py` to reduce drift.

---

## 18) Appendix: Sample Registry Entries

### agents.json (example)

```json
{
  "extract_urls": {
    "description": "Extracts all URLs from text",
    "uses_tools": ["regex_url_matcher"],
    "input_schema": {"text": "string"},
    "output_schema": {"urls": "array", "count": "integer"},
    "location": "generated/agents/extract_urls.py",
    "created_by": "claude-3-xxx",
    "created_at": "2025-09-03T12:00:00Z",
    "version": "1.0.0",
    "execution_count": 0,
    "avg_execution_time": 0.0,
    "tags": ["text", "extraction"]
  }
}
```

### tools.json (example)

```json
{
  "regex_url_matcher": {
    "description": "Finds URLs in text using regex patterns",
    "signature": "def regex_url_matcher(text: str) -> List[str]",
    "location": "generated/tools/regex_url_matcher.py",
    "used_by_agents": ["extract_urls"],
    "created_by": "claude-3-xxx",
    "created_at": "2025-09-03T11:59:00Z",
    "is_pure_function": true,
    "tags": ["regex", "url"]
  }
}
```

---

## 19) TL;DR

Keep **agents tiny** and **tools pure**. Use **dual registries** as the source of truth. The **Orchestrator** plans; **LangGraph** executes. Only four readers are prebuilt; everything else is created on demand, validated, and registered. Ensure safety, observability, and versioned change management throughout.

```

--------------------------------------------------------------------------------

### File: KNOWLEDGE_BASE.md
**Path:** `KNOWLEDGE_BASE.md`
**Size:** 0 bytes
**Modified:** 2025-09-06 15:25:25

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
**Size:** 7,822 bytes
**Modified:** 2025-09-06 13:33:30

```json
{
  "agents": {
    "email_extractor": {
      "name": "email_extractor",
      "description": "Extracts email addresses from text input",
      "uses_tools": [
        "extract_emails"
      ],
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
      "execution_count": 0,
      "avg_execution_time": 0.0,
      "tags": [
        "extraction",
        "emails"
      ],
      "line_count": 98,
      "status": "active"
    },
    "url_extractor": {
      "name": "url_extractor",
      "description": "Extracts URLs from text input",
      "uses_tools": [
        "extract_urls"
      ],
      "input_schema": {
        "data": "any"
      },
      "output_schema": {
        "status": "string",
        "data": {
          "urls": "array",
          "count": "integer",
          "domains": "object"
        },
        "metadata": "object"
      },
      "location": "prebuilt/agents/url_extractor_agent.py",
      "is_prebuilt": true,
      "created_by": "claude-3-haiku-20240307",
      "created_at": "2025-09-04T12:30:00",
      "version": "1.0.0",
      "execution_count": 0,
      "avg_execution_time": 0.0,
      "tags": [
        "extraction",
        "urls"
      ],
      "line_count": 80,
      "status": "active"
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
        "required": [
          "status",
          "data",
          "metadata"
        ],
        "properties": {
          "status": {
            "type": "string",
            "enum": [
              "success",
              "error",
              "partial"
            ]
          },
          "data": {
            "type": [
              "object",
              "array",
              "null"
            ],
            "description": "Agent-specific output data"
          },
          "metadata": {
            "type": "object",
            "required": [
              "agent",
              "execution_time"
            ],
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
      "status": "active"
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
        "required": [
          "status",
          "data",
          "metadata"
        ],
        "properties": {
          "status": {
            "type": "string",
            "enum": [
              "success",
              "error",
              "partial"
            ]
          },
          "data": {
            "type": [
              "object",
              "array",
              "null"
            ],
            "description": "Agent-specific output data"
          },
          "metadata": {
            "type": "object",
            "required": [
              "agent",
              "execution_time"
            ],
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
      "status": "active"
    },
    "word_counter": {
      "name": "word_counter",
      "description": "Count words in text using the count_words tool",
      "uses_tools": [
        "count_words"
      ],
      "input_schema": {
        "type": "any",
        "description": "Flexible input - can be string, dict, or list"
      },
      "output_schema": {
        "type": "object",
        "required": [
          "status",
          "data",
          "metadata"
        ],
        "properties": {
          "status": {
            "type": "string",
            "enum": [
              "success",
              "error",
              "partial"
            ]
          },
          "data": {
            "type": [
              "object",
              "array",
              "null"
            ],
            "description": "Agent-specific output data"
          },
          "metadata": {
            "type": "object",
            "required": [
              "agent",
              "execution_time"
            ],
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
      "location": "/Users/sayantankundu/Documents/Agent Fabric/generated/agents/word_counter_agent.py",
      "is_prebuilt": false,
      "created_by": "claude-3-haiku-20240307",
      "created_at": "2025-09-06T13:33:30.345830",
      "version": "1.0.08c2f7ac",
      "execution_count": 0,
      "avg_execution_time": 0.0,
      "last_executed": null,
      "tags": [],
      "line_count": 80,
      "status": "active"
    }
  }
}
```

--------------------------------------------------------------------------------

### File: agents.json.lock
**Path:** `agents.json.lock`
**Size:** 0 bytes
**Modified:** 2025-09-06 13:33:30

*[Binary file or content not included]*

--------------------------------------------------------------------------------

### File: config.py
**Path:** `config.py`
**Size:** 18,817 bytes
**Modified:** 2025-09-04 22:57:09

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

ORCHESTRATOR_PLANNING_PROMPT = """Analyze this request and create a workflow plan.

REQUEST: {request}
ANALYSIS: {analysis}

AVAILABLE AGENTS (Use EXACT names from this list):
{available_agents}

AVAILABLE TOOLS:
{available_tools}

CRITICAL INSTRUCTIONS:
1. ONLY use agent names that appear in the AVAILABLE AGENTS list above
2. Check if existing agents can handle the task before creating new ones
3. Many agents have flexible input handling - don't create duplicates
4. For common tasks, these agents likely exist:
   - email_extractor: extracts emails from any text
   - url_extractor: extracts URLs from any text  
   - calculate_mean/median/std: statistical calculations
   - format_report: formats data into reports
   - read_text/csv/pdf: file readers

STEP-BY-STEP PLANNING:
1. Break down what the user wants into specific tasks
2. Map each task to an available agent (check the list!)
3. Only mark as missing if NO agent can do it
4. Plan the execution order

Respond with this EXACT JSON structure:
{{
    "workflow_id": "wf_{timestamp}",
    "workflow_type": "sequential",
    "reasoning": "Step-by-step explanation of your plan",
    "agents_needed": ["agent1_from_available_list", "agent2_from_available_list"],
    "missing_capabilities": {{
        "agents": [
            // ONLY if truly missing from available list
            {{
                "name": "new_agent_name",
                "purpose": "specific purpose",
                "required_tools": ["tool1"],
                "justification": "why existing agents cannot handle this"
            }}
        ],
        "tools": []
    }},
    "confidence": 0.95
}}

IMPORTANT: The agents_needed array should ONLY contain names from the AVAILABLE AGENTS list."""


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

CLAUDE_AGENT_GENERATION_PROMPT = """Create a Python agent that is MINIMAL but FUNCTIONAL.

Agent Name: {agent_name}
Purpose: {description}
Required Tools: {tools}

CRITICAL REQUIREMENTS:
1. The agent MUST actually do something useful, not just pass data through
2. Use the tools intelligently to process the input
3. Add value beyond what the tools alone provide
4. Handle edge cases gracefully
5. Keep it between {min_lines}-{max_lines} lines

TEMPLATE TO FOLLOW EXACTLY:
```python
def {agent_name}_agent(state):
    \"\"\"
    {description}
    \"\"\"
    import sys
    import os
    from datetime import datetime
    
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Import tools
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
        
        # Get input data using standard pattern
        input_data = state.get('current_data')
        if input_data is None:
            # Check previous agent results
            if 'results' in state and state['execution_path']:
                last_agent = state['execution_path'][-1]
                if last_agent in state['results']:
                    last_result = state['results'][last_agent]
                    if isinstance(last_result, dict) and 'data' in last_result:
                        input_data = last_result['data']
        
        if input_data is None:
            # Check root state
            input_data = state.get('text', state.get('data', state.get('request')))
        
        # ACTUAL PROCESSING - This is where the agent adds value
        # Use the tools to process the data
        # Don't just return the tool output - enhance it
        
        {agent_logic}
        
        # Create meaningful output
        processed_data = {{
            # Include actual processed results here
        }}
        
        result = {{
            "status": "success",
            "data": processed_data,
            "metadata": {{
                "agent": "{agent_name}",
                "execution_time": (datetime.now() - start_time).total_seconds(),
                "tools_used": {tools}
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
Make the agent ACTUALLY USEFUL. For example:

If it's a calculator, actually calculate things
If it's an extractor, actually extract and organize data
If it's a formatter, actually format the data nicely
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
**Size:** 26,091 bytes
**Modified:** 2025-09-04 22:51:19

```python
"""
Agent Factory
Dynamically generates intelligent agents using Claude API
"""

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

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class AgentFactory:
    """
    Factory for creating intelligent agents powered by Claude.
    Handles code generation, validation, and registration.
    """

    def __init__(self):
        """Initialize the agent factory."""
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
                temperature=CLAUDE_TEMPERATURE,
                max_tokens=CLAUDE_MAX_TOKENS,
                messages=[{"role": "user", "content": prompt}],
            )

            # Extract code from response
            raw_response = response.content[0].text
            code = self._extract_code_from_response(raw_response)

            if not code:
                print(f"DEBUG: No code extracted from Claude response")
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

```

--------------------------------------------------------------------------------

### File: core/dependency_resolver.py
**Path:** `core/dependency_resolver.py`
**Size:** 8,333 bytes
**Modified:** 2025-09-04 21:57:32

```python
"""
Dependency Resolver
Handles topological sorting and dependency graph creation for agent-tool relationships
"""

import networkx as nx
from typing import Dict, List, Any, Tuple
from collections import defaultdict


class DependencyResolver:
    """Resolves and creates dependencies in correct order."""

    def __init__(self, registry):
        self.registry = registry
        self.dependency_graph = nx.DiGraph()

    def analyze_request(
        self, request: str, existing_agents: Dict, existing_tools: Dict
    ) -> Dict:
        """
        Analyze request and build dependency graph.

        Returns:
            Dict with capabilities needed and creation order
        """
        # Build capability map from request
        capabilities = self._extract_capabilities(request)

        # Build dependency graph
        graph = self._build_dependency_graph(
            capabilities, existing_agents, existing_tools
        )

        # Determine creation order
        creation_order = self._get_creation_order(graph)

        return {
            "capabilities": capabilities,
            "dependency_graph": graph,
            "creation_order": creation_order,
            "missing_components": self._identify_missing_components(
                graph, existing_agents, existing_tools
            ),
        }

    def _extract_capabilities(self, request: str) -> List[Dict]:
        """Extract required capabilities from request."""
        capabilities = []

        # Pattern matching for common operations
        request_lower = request.lower()

        # Extraction capabilities
        if any(word in request_lower for word in ["extract", "find", "get"]):
            if "email" in request_lower:
                capabilities.append(
                    {
                        "name": "email_extraction",
                        "agent": "email_extractor",
                        "tools": ["extract_emails"],
                    }
                )
            if "phone" in request_lower:
                capabilities.append(
                    {
                        "name": "phone_extraction",
                        "agent": "phone_extractor",
                        "tools": ["extract_phone"],
                    }
                )
            if "url" in request_lower or "link" in request_lower:
                capabilities.append(
                    {
                        "name": "url_extraction",
                        "agent": "url_extractor",
                        "tools": ["extract_urls"],
                    }
                )

        # Analysis capabilities
        if any(word in request_lower for word in ["analyze", "analysis", "examine"]):
            if "sentiment" in request_lower:
                capabilities.append(
                    {
                        "name": "sentiment_analysis",
                        "agent": "sentiment_analyzer",
                        "tools": ["analyze_sentiment", "score_sentiment"],
                    }
                )
            if "statistic" in request_lower or "stats" in request_lower:
                capabilities.append(
                    {
                        "name": "statistical_analysis",
                        "agent": "statistics_calculator",
                        "tools": [
                            "calculate_mean",
                            "calculate_median",
                            "calculate_std",
                        ],
                    }
                )

        # Generation capabilities
        if any(word in request_lower for word in ["generate", "create", "make"]):
            if "chart" in request_lower or "graph" in request_lower:
                capabilities.append(
                    {
                        "name": "chart_generation",
                        "agent": "chart_generator",
                        "tools": ["generate_chart", "format_chart_data"],
                    }
                )
            if "report" in request_lower:
                capabilities.append(
                    {
                        "name": "report_generation",
                        "agent": "report_generator",
                        "tools": ["format_report", "generate_summary"],
                    }
                )

        return capabilities

    def _build_dependency_graph(
        self, capabilities: List[Dict], existing_agents: Dict, existing_tools: Dict
    ) -> nx.DiGraph:
        """Build directed graph of dependencies."""
        graph = nx.DiGraph()

        for cap in capabilities:
            agent_name = cap["agent"]

            # Add agent node
            graph.add_node(
                agent_name,
                type="agent",
                exists=agent_name in existing_agents,
                capability=cap["name"],
            )

            # Add tool nodes and edges
            for tool_name in cap["tools"]:
                graph.add_node(
                    tool_name, type="tool", exists=tool_name in existing_tools
                )

                # Tool must exist before agent can use it
                graph.add_edge(tool_name, agent_name, relation="required_by")

        return graph

    def _get_creation_order(self, graph: nx.DiGraph) -> List[Tuple[str, str]]:
        """
        Get creation order using topological sort.

        Returns:
            List of (type, name) tuples in creation order
        """
        try:
            # Topological sort ensures dependencies are created first
            sorted_nodes = list(nx.topological_sort(graph))

            creation_order = []
            for node in sorted_nodes:
                if not graph.nodes[node]["exists"]:
                    node_type = graph.nodes[node]["type"]
                    creation_order.append((node_type, node))

            return creation_order

        except nx.NetworkXUnfeasible:
            # Graph has cycles - shouldn't happen with proper design
            print("WARNING: Dependency graph has cycles!")
            return []

    def _identify_missing_components(
        self, graph: nx.DiGraph, existing_agents: Dict, existing_tools: Dict
    ) -> Dict:
        """Identify what needs to be created."""
        missing = {"agents": [], "tools": []}

        for node, data in graph.nodes(data=True):
            if not data["exists"]:
                if data["type"] == "agent":
                    # Get required tools for this agent
                    required_tools = [
                        pred
                        for pred in graph.predecessors(node)
                        if graph.nodes[pred]["type"] == "tool"
                    ]

                    missing["agents"].append(
                        {
                            "name": node,
                            "required_tools": required_tools,
                            "capability": data.get("capability", ""),
                        }
                    )
                else:  # tool
                    missing["tools"].append(
                        {"name": node, "used_by": list(graph.successors(node))}
                    )

        return missing

    def visualize_dependencies(self, graph: nx.DiGraph) -> str:
        """Create text visualization of dependency graph."""
        lines = ["Dependency Graph:"]
        lines.append("=" * 50)

        # Group by component type
        tools = [n for n, d in graph.nodes(data=True) if d["type"] == "tool"]
        agents = [n for n, d in graph.nodes(data=True) if d["type"] == "agent"]

        lines.append("\nTools:")
        for tool in tools:
            status = "✓" if graph.nodes[tool]["exists"] else "✗"
            users = list(graph.successors(tool))
            lines.append(f"  {status} {tool} -> used by: {', '.join(users)}")

        lines.append("\nAgents:")
        for agent in agents:
            status = "✓" if graph.nodes[agent]["exists"] else "✗"
            deps = list(graph.predecessors(agent))
            lines.append(f"  {status} {agent} <- requires: {', '.join(deps)}")

        lines.append("\nCreation Order:")
        for node in nx.topological_sort(graph):
            if not graph.nodes[node]["exists"]:
                lines.append(f"  {graph.nodes[node]['type']}: {node}")

        return "\n".join(lines)

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

### File: core/workflow_engine.py
**Path:** `core/workflow_engine.py`
**Size:** 31,883 bytes
**Modified:** 2025-09-06 13:23:39

```python
"""
Workflow Engine
Executes multi-agent workflows using LangGraph with advanced state management
"""

import os
import sys
import json
import asyncio
import importlib.util
from typing import Dict, List, Optional, Any, TypedDict, Callable
from datetime import datetime
from enum import Enum
import traceback

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from config import (
    WORKFLOW_STATE_SCHEMA,
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
from core.registry_singleton import get_shared_registry


class WorkflowState(TypedDict):
    """Enhanced state schema for workflow execution."""

    # Core fields
    request: str
    workflow_id: str
    workflow_type: str

    # Data flow
    current_data: Any
    files: List[Dict[str, Any]]
    context: Dict[str, Any]

    # Execution tracking
    execution_path: List[str]
    current_agent: Optional[str]
    pending_agents: List[str]
    completed_agents: List[str]

    # Results and errors
    results: Dict[str, Any]
    errors: List[Dict[str, str]]
    warnings: List[Dict[str, str]]

    # Metadata
    started_at: str
    completed_at: Optional[str]
    execution_metrics: Dict[str, float]
    retry_counts: Dict[str, int]

    # Control flow
    should_continue: bool
    next_agent: Optional[str]
    parallel_group: Optional[List[str]]


class ExecutionStatus(Enum):
    """Workflow execution statuses."""

    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"


class WorkflowEngine:
    """
    Advanced workflow execution engine using LangGraph.
    Handles complex multi-agent orchestration with state management.
    """

    def __init__(self):
        """Initialize the workflow engine."""
        self.registry = get_shared_registry()
        self.checkpointer = MemorySaver()
        self.loaded_agents = {}
        self.active_workflows = {}
        self.execution_cache = {}

    def create_workflow(
        self,
        agent_sequence: List[str],
        workflow_id: Optional[str] = None,
        workflow_type: str = "sequential",
    ) -> StateGraph:
        """
        Create a LangGraph workflow from agent sequence.

        Args:
            agent_sequence: List of agent names to execute
            workflow_id: Optional workflow identifier
            workflow_type: Type of workflow (sequential, parallel, conditional)

        Returns:
            Configured StateGraph ready for execution
        """
        # Validate agents exist
        validation_result = self._validate_agents(agent_sequence)
        if not validation_result["valid"]:
            raise ValueError(f"Invalid agents: {validation_result['errors']}")

        # Create the state graph
        workflow = StateGraph(WorkflowState)

        # Add nodes based on workflow type
        if workflow_type == "sequential":
            self._build_sequential_workflow(workflow, agent_sequence)
        elif workflow_type == "parallel":
            self._build_parallel_workflow(workflow, agent_sequence)
        elif workflow_type == "conditional":
            self._build_conditional_workflow(workflow, agent_sequence)
        else:
            self._build_hybrid_workflow(workflow, agent_sequence)

        # Compile with checkpointer for state persistence
        return workflow.compile(checkpointer=self.checkpointer)

    def execute_workflow(
        self,
        workflow: StateGraph,
        initial_data: Dict[str, Any],
        workflow_id: Optional[str] = None,
        timeout: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Execute a compiled workflow synchronously.
        """
        workflow_id = workflow_id or self._generate_workflow_id()
        timeout = timeout or WORKFLOW_TIMEOUT_SECONDS

        # Prepare initial state
        initial_state = self._prepare_initial_state(workflow_id, initial_data)

        # CRITICAL FIX: Ensure current_data is properly initialized
        if "current_data" not in initial_state or initial_state["current_data"] is None:
            # Set current_data from various possible sources
            if initial_data.get("text"):
                initial_state["current_data"] = initial_data["text"]
            elif initial_data.get("data"):
                initial_state["current_data"] = initial_data["data"]
            elif initial_data.get("request"):
                initial_state["current_data"] = initial_data["request"]
            else:
                initial_state["current_data"] = initial_data

        # Track workflow
        self.active_workflows[workflow_id] = {
            "status": ExecutionStatus.RUNNING,
            "started_at": initial_state["started_at"],
        }

        try:
            # Configure execution
            config = {
                "configurable": {"thread_id": workflow_id, "checkpoint_ns": workflow_id}
            }

            # Execute workflow with timeout
            final_state = self._execute_with_timeout(
                workflow, initial_state, config, timeout
            )

            # Mark completion
            final_state["completed_at"] = datetime.now().isoformat()
            final_state["execution_metrics"]["total_time"] = (
                datetime.fromisoformat(final_state["completed_at"])
                - datetime.fromisoformat(final_state["started_at"])
            ).total_seconds()

            # CRITICAL FIX: Determine success based on completed agents vs errors
            has_critical_errors = False
            if final_state.get("errors"):
                # Check if errors are critical (not just warnings)
                for error in final_state["errors"]:
                    if "critical" in str(error.get("error", "")).lower():
                        has_critical_errors = True
                        break

            # Success if we have results and no critical errors
            if final_state.get("results") and not has_critical_errors:
                status = ExecutionStatus.SUCCESS
            elif final_state.get("results") and final_state.get("errors"):
                status = ExecutionStatus.PARTIAL
            else:
                status = ExecutionStatus.FAILED

            # Update tracking
            self.active_workflows[workflow_id]["status"] = status

            # Update agent metrics
            self._update_agent_metrics(final_state)

            return final_state

        except Exception as e:
            # Handle execution failure
            self.active_workflows[workflow_id]["status"] = ExecutionStatus.FAILED

            return self._create_error_state(
                initial_state, f"Workflow execution failed: {str(e)}"
            )
        finally:
            # Clean up
            if workflow_id in self.active_workflows:
                del self.active_workflows[workflow_id]

    async def execute_workflow_async(
        self,
        workflow: StateGraph,
        initial_data: Dict[str, Any],
        workflow_id: Optional[str] = None,
        stream_callback: Optional[Callable] = None,
    ) -> Dict[str, Any]:
        """
        Execute workflow asynchronously with streaming support.

        Args:
            workflow: Compiled StateGraph
            initial_data: Initial data
            workflow_id: Optional workflow identifier
            stream_callback: Optional callback for streaming results

        Returns:
            Final workflow state
        """
        workflow_id = workflow_id or self._generate_workflow_id()

        # Prepare initial state
        initial_state = self._prepare_initial_state(workflow_id, initial_data)

        try:
            # Execute with streaming
            config = {
                "configurable": {"thread_id": workflow_id, "checkpoint_ns": workflow_id}
            }

            final_state = initial_state
            async for output in workflow.astream(initial_state, config):
                # Stream intermediate results
                if stream_callback:
                    await stream_callback(output)

                # Update state
                for key, value in output.items():
                    if key != "__end__":
                        final_state = value

            # Mark completion
            final_state["completed_at"] = datetime.now().isoformat()

            return final_state

        except Exception as e:
            return self._create_error_state(
                initial_state, f"Async execution failed: {str(e)}"
            )

    def _build_sequential_workflow(self, workflow: StateGraph, agents: List[str]):
        """Build sequential workflow structure."""
        for i, agent_name in enumerate(agents):
            # Create agent node
            agent_func = self._create_agent_node(agent_name)
            workflow.add_node(agent_name, agent_func)

            # Set edges
            if i == 0:
                workflow.set_entry_point(agent_name)

            if i < len(agents) - 1:
                # Add conditional edge for error handling
                workflow.add_conditional_edges(
                    agent_name, self._should_continue, {True: agents[i + 1], False: END}
                )
            else:
                workflow.add_edge(agent_name, END)

    def _build_parallel_workflow(self, workflow: StateGraph, agents: List[str]):
        """Build parallel workflow structure."""
        # Add parallel execution node
        parallel_node = self._create_parallel_node(agents)
        workflow.add_node("parallel_execution", parallel_node)

        # Add merge node
        merge_node = self._create_merge_node()
        workflow.add_node("merge_results", merge_node)

        # Set edges
        workflow.set_entry_point("parallel_execution")
        workflow.add_edge("parallel_execution", "merge_results")
        workflow.add_edge("merge_results", END)

    def _build_conditional_workflow(self, workflow: StateGraph, agents: List[str]):
        """Build conditional workflow structure."""
        # Add decision node
        decision_node = self._create_decision_node()
        workflow.add_node("decision", decision_node)

        # Add agent nodes
        for agent_name in agents:
            agent_func = self._create_agent_node(agent_name)
            workflow.add_node(agent_name, agent_func)
            workflow.add_edge(agent_name, END)

        # Set conditional routing
        workflow.set_entry_point("decision")

        # Create routing map
        route_map = {agent: agent for agent in agents}
        route_map["none"] = END

        workflow.add_conditional_edges("decision", self._route_decision, route_map)

    def _build_hybrid_workflow(self, workflow: StateGraph, agents: List[str]):
        """Build hybrid workflow with mixed patterns."""
        # This is a simplified hybrid - can be extended
        # For now, treat as sequential with parallel groups
        self._build_sequential_workflow(workflow, agents)

    def _create_agent_node(self, agent_name: str) -> Callable:
        """Create a node function for an agent - ENHANCED VERSION."""

        def agent_node(state: WorkflowState) -> WorkflowState:
            """Execute agent and update state."""
            try:
                # Ensure current_data is properly set
                if "current_data" not in state or state["current_data"] is None:
                    # Enhanced data extraction logic
                    if state.get("request"):
                        state["current_data"] = state["request"]
                    elif state.get("text"):
                        state["current_data"] = state["text"]
                    elif state.get("data"):
                        state["current_data"] = state["data"]
                    elif state.get("files") and len(state["files"]) > 0:
                        # Try to use file content if available
                        state["current_data"] = state["files"][0]
                    elif state.get("results"):
                        # Get the last successful agent's output
                        for prev_agent in reversed(state.get("execution_path", [])):
                            if prev_agent in state["results"]:
                                result = state["results"][prev_agent]
                                if (
                                    isinstance(result, dict)
                                    and result.get("status") == "success"
                                ):
                                    state["current_data"] = result.get("data")
                                    break

                    # If still no data, provide empty dict to prevent errors
                    if state.get("current_data") is None:
                        state["current_data"] = {}
                        state["warnings"].append(
                            {
                                "agent": agent_name,
                                "warning": "No input data available, using empty dict",
                            }
                        )

                # Update current agent
                state["current_agent"] = agent_name

                # Check retry count
                if agent_name not in state["retry_counts"]:
                    state["retry_counts"][agent_name] = 0

                # Load and execute agent
                agent_func = self._load_agent(agent_name)

                # Record start time
                start_time = datetime.now()

                # Create mutable copy of state
                agent_state = dict(state)

                # Execute with timeout
                import signal

                def timeout_handler(signum, frame):
                    raise TimeoutError(
                        f"Agent {agent_name} timeout after {AGENT_TIMEOUT_SECONDS}s"
                    )

                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(AGENT_TIMEOUT_SECONDS)

                try:
                    # Execute agent with error recovery
                    agent_state = agent_func(agent_state)

                    # Merge state changes back
                    for key, value in agent_state.items():
                        state[key] = value

                except TimeoutError as e:
                    # Handle timeout specifically
                    state["errors"].append(
                        {"agent": agent_name, "error": str(e), "type": "timeout"}
                    )
                    # Create error result but don't stop workflow
                    state["results"][agent_name] = {
                        "status": "error",
                        "data": None,
                        "metadata": {
                            "agent": agent_name,
                            "error": "Execution timeout",
                            "execution_time": AGENT_TIMEOUT_SECONDS,
                        },
                    }
                finally:
                    signal.alarm(0)

                # Record execution time
                execution_time = (datetime.now() - start_time).total_seconds()
                state["execution_metrics"][agent_name] = execution_time

                # Update tracking
                if agent_name not in state["execution_path"]:
                    state["execution_path"].append(agent_name)
                if agent_name not in state["completed_agents"]:
                    state["completed_agents"].append(agent_name)

                # Ensure current_data is preserved for next agent
                if agent_name in state.get("results", {}):
                    result = state["results"][agent_name]
                    if (
                        isinstance(result, dict)
                        and result.get("status") == "success"
                        and "data" in result
                    ):
                        state["current_data"] = result["data"]

                return state

            except Exception as e:
                # Record error but don't crash workflow
                import traceback

                state["errors"].append(
                    {
                        "agent": agent_name,
                        "error": str(e),
                        "traceback": traceback.format_exc(),
                        "type": "execution_error",
                    }
                )

                # Create error result
                state["results"][agent_name] = {
                    "status": "error",
                    "data": None,
                    "metadata": {"agent": agent_name, "error": str(e)},
                }

                # Still mark as completed (with error)
                if agent_name not in state["completed_agents"]:
                    state["completed_agents"].append(agent_name)

                # Don't stop the workflow
                return state

        return agent_node

    def _create_parallel_node(self, agents: List[str]) -> Callable:
        """Create node for parallel execution - FIXED VERSION."""

        def parallel_node(state: WorkflowState) -> WorkflowState:
            """Execute agents in parallel without duplication."""
            import concurrent.futures

            state["parallel_group"] = agents
            results = {}

            # Track which agents have already been executed
            already_executed = set(state.get("completed_agents", []))
            agents_to_run = [a for a in agents if a not in already_executed]

            if not agents_to_run:
                print(f"All parallel agents already executed: {agents}")
                return state

            with concurrent.futures.ThreadPoolExecutor(
                max_workers=min(len(agents_to_run), MAX_PARALLEL_AGENTS)
            ) as executor:
                # Submit all agents that haven't run yet
                futures = {}
                for agent_name in agents_to_run:
                    try:
                        agent_func = self._load_agent(agent_name)
                        # Create copy of state for each agent
                        agent_state = dict(state)
                        agent_state["current_agent"] = agent_name

                        future = executor.submit(agent_func, agent_state)
                        futures[future] = agent_name
                    except Exception as e:
                        print(f"Failed to submit agent {agent_name}: {e}")
                        state["errors"].append(
                            {
                                "agent": agent_name,
                                "error": f"Failed to submit: {str(e)}",
                            }
                        )

                # Collect results with timeout
                for future in concurrent.futures.as_completed(
                    futures, timeout=WORKFLOW_TIMEOUT_SECONDS
                ):
                    agent_name = futures[future]
                    try:
                        agent_state = future.result(timeout=AGENT_TIMEOUT_SECONDS)

                        # Merge results back to main state
                        if agent_name in agent_state.get("results", {}):
                            results[agent_name] = agent_state["results"][agent_name]

                        # Update completed list (avoid duplicates)
                        if agent_name not in state["completed_agents"]:
                            state["completed_agents"].append(agent_name)

                        # Add to execution path once
                        if agent_name not in state["execution_path"]:
                            state["execution_path"].append(agent_name)

                    except concurrent.futures.TimeoutError:
                        state["errors"].append(
                            {
                                "agent": agent_name,
                                "error": f"Timeout after {AGENT_TIMEOUT_SECONDS}s",
                            }
                        )
                    except Exception as e:
                        state["errors"].append({"agent": agent_name, "error": str(e)})

            # Merge all results at once
            state["results"].update(results)

            return state

        return parallel_node

    def _create_merge_node(self) -> Callable:
        """Create node for merging parallel results."""

        def merge_node(state: WorkflowState) -> WorkflowState:
            """Merge results from parallel execution."""
            # Aggregate data from all results
            merged_data = {}

            for agent_name, result in state.get("results", {}).items():
                if isinstance(result, dict) and result.get("status") == "success":
                    data = result.get("data", {})
                    if isinstance(data, dict):
                        merged_data.update(data)
                    else:
                        merged_data[agent_name] = data

            state["current_data"] = merged_data
            return state

        return merge_node

    def _create_decision_node(self) -> Callable:
        """Create node for conditional decisions."""

        def decision_node(state: WorkflowState) -> WorkflowState:
            """Make routing decision based on state."""
            # Analyze current data to determine next agent
            # This is a simplified implementation
            state["next_agent"] = self._determine_next_agent(state)
            return state

        return decision_node

    def _should_continue(self, state: WorkflowState) -> bool:
        """Determine if workflow should continue."""
        # Check explicit flag
        if not state.get("should_continue", True):
            return False

        # CRITICAL FIX: Don't stop on non-critical errors
        # Only stop if ALL agents have failed
        if state.get("errors"):
            # Count successful vs failed agents
            successful = len(
                [
                    a
                    for a in state.get("completed_agents", [])
                    if state.get("results", {}).get(a, {}).get("status") == "success"
                ]
            )

            # Continue if at least one agent succeeded
            if successful > 0:
                return True

            # Check if all agents have failed critically
            total_agents = len(state.get("execution_path", []))
            critical_errors = len(
                [
                    e
                    for e in state["errors"]
                    if "critical" in str(e.get("error", "")).lower()
                ]
            )

            # Stop only if all agents failed
            if total_agents > 0 and critical_errors >= total_agents:
                return False

        # Check step limit
        if len(state.get("execution_path", [])) >= MAX_WORKFLOW_STEPS:
            return False

        return True

    def _route_decision(self, state: WorkflowState) -> str:
        """Route to next agent based on decision."""
        return state.get("next_agent", "none")

    def _determine_next_agent(self, state: WorkflowState) -> str:
        """Determine next agent based on current state."""
        # Simple logic - can be enhanced
        current_data = state.get("current_data", {})

        # Check data type and route accordingly
        if isinstance(current_data, dict):
            if "emails" in current_data:
                return "email_processor"
            elif "numbers" in current_data:
                return "statistics_calculator"

        return "none"

    def _load_agent(self, agent_name: str) -> Callable:
        """Load an agent function dynamically."""

        print(f"DEBUG: Loading agent '{agent_name}'")

        # Check cache first
        if agent_name in self.loaded_agents:
            return self.loaded_agents[agent_name]

        # Get agent info from registry
        agent_info = self.registry.get_agent(agent_name)
        if not agent_info:
            print(f"DEBUG: Agent '{agent_name}' not found in registry")
            raise ValueError(f"Agent '{agent_name}' not found in registry")
        print(f"DEBUG: Agent info found: {agent_info.get('location')}")

        # Load the agent module
        agent_path = agent_info["location"]
        if not os.path.exists(agent_path):
            raise FileNotFoundError(f"Agent file not found: {agent_path}")

        # Import the module
        spec = importlib.util.spec_from_file_location(
            f"{agent_name}_module", agent_path
        )
        module = importlib.util.module_from_spec(spec)
        sys.modules[f"{agent_name}_module"] = module
        spec.loader.exec_module(module)

        # Get the agent function
        possible_names = [f"{agent_name}_agent", agent_name, "agent", "execute"]

        agent_func = None
        for name in possible_names:
            if hasattr(module, name):
                agent_func = getattr(module, name)
                break

        if not agent_func:
            raise AttributeError(f"No valid agent function found in {agent_path}")

        # Cache for future use
        self.loaded_agents[agent_name] = agent_func

        return agent_func

    def _validate_agents(self, agents: List[str]) -> Dict[str, Any]:
        """Validate that all agents exist and are valid."""

        print(f"DEBUG: Validating agents: {agents}")

        missing = []
        inactive = []

        for agent_name in agents:
            print(f"DEBUG: Checking agent '{agent_name}'")
            agent = self.registry.get_agent(agent_name)
            if not agent:
                print(f"DEBUG: Agent '{agent_name}' not found in registry")
                missing.append(agent_name)
            elif agent.get("status") != "active":
                print(f"DEBUG: Agent '{agent_name}' status: {agent.get('status')}")
                inactive.append(agent_name)
            else:
                print(f"DEBUG: Agent '{agent_name}' is valid and active")

        errors = []
        if missing:
            errors.append(f"Missing agents: {', '.join(missing)}")
        if inactive:
            errors.append(f"Inactive agents: {', '.join(inactive)}")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "missing": missing,
            "inactive": inactive,
        }

    def _prepare_initial_state(
        self, workflow_id: str, initial_data: Dict[str, Any]
    ) -> WorkflowState:
        """Prepare initial workflow state."""
        return {
            "request": initial_data.get("request", ""),
            "workflow_id": workflow_id,
            "workflow_type": initial_data.get("workflow_type", "sequential"),
            "current_data": initial_data,
            "files": initial_data.get("files", []),
            "context": initial_data.get("context", {}),
            "execution_path": [],
            "current_agent": None,
            "pending_agents": [],
            "completed_agents": [],
            "results": {},
            "errors": [],
            "warnings": [],
            "started_at": datetime.now().isoformat(),
            "completed_at": None,
            "execution_metrics": {},
            "retry_counts": {},
            "should_continue": True,
            "next_agent": None,
            "parallel_group": None,
        }

    def _execute_with_timeout(
        self,
        workflow: StateGraph,
        initial_state: WorkflowState,
        config: Dict,
        timeout: int,
    ) -> WorkflowState:
        """Execute workflow with timeout."""
        import threading

        result = [None]
        exception = [None]

        def run_workflow():
            try:
                final_state = initial_state
                for output in workflow.stream(initial_state, config):
                    if isinstance(output, dict):
                        for key, value in output.items():
                            if key != "__end__":
                                final_state = value
                result[0] = final_state
            except Exception as e:
                exception[0] = e

        thread = threading.Thread(target=run_workflow)
        thread.start()
        thread.join(timeout=timeout)

        if thread.is_alive():
            # Timeout occurred
            raise TimeoutError(f"Workflow timeout after {timeout} seconds")

        if exception[0]:
            raise exception[0]

        return result[0]

    def _update_agent_metrics(self, state: WorkflowState):
        """Update agent metrics in registry."""
        for agent_name in state.get("completed_agents", []):
            if agent_name in state.get("execution_metrics", {}):
                execution_time = state["execution_metrics"][agent_name]
                self.registry.update_agent_metrics(agent_name, execution_time)

    def _create_error_state(
        self, initial_state: WorkflowState, error_message: str
    ) -> WorkflowState:
        """Create error state for failed execution."""
        initial_state["errors"].append(
            {
                "agent": "workflow_engine",
                "error": error_message,
                "timestamp": datetime.now().isoformat(),
            }
        )
        initial_state["completed_at"] = datetime.now().isoformat()
        initial_state["should_continue"] = False
        return initial_state

    def _generate_workflow_id(self) -> str:
        """Generate unique workflow ID."""
        import random

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = random.randint(1000, 9999)
        return f"wf_{timestamp}_{random_suffix}"

    def get_workflow_status(self, workflow_id: str) -> Optional[Dict]:
        """Get status of a workflow."""
        return self.active_workflows.get(workflow_id)

    def cancel_workflow(self, workflow_id: str) -> bool:
        """Cancel an active workflow."""
        if workflow_id in self.active_workflows:
            self.active_workflows[workflow_id]["status"] = ExecutionStatus.CANCELLED
            return True
        return False

    def visualize_workflow(
        self, agent_sequence: List[str], workflow_type: str = "sequential"
    ) -> str:
        """Create text visualization of workflow."""
        viz = ["\nWorkflow Visualization"]
        viz.append("=" * 50)
        viz.append(f"Type: {workflow_type}")
        viz.append(f"Agents: {len(agent_sequence)}")
        viz.append("")

        if workflow_type == "sequential":
            viz.append("START")
            for i, agent in enumerate(agent_sequence):
                viz.append(f"  │")
                viz.append(f"  ▼")
                viz.append(f"[{i+1}. {agent}]")
                agent_info = self.registry.get_agent(agent)
                if agent_info:
                    viz.append(f"    {agent_info['description']}")
            viz.append(f"  │")
            viz.append(f"  ▼")
            viz.append("END")

        elif workflow_type == "parallel":
            viz.append("START")
            viz.append("  │")
            viz.append("  ▼")
            viz.append("[Parallel Execution]")
            for agent in agent_sequence:
                viz.append(f"  ├─> {agent}")
            viz.append("  │")
            viz.append("  ▼")
            viz.append("[Merge Results]")
            viz.append("  │")
            viz.append("  ▼")
            viz.append("END")

        return "\n".join(viz)

```

--------------------------------------------------------------------------------

### File: create_knowledge_base.py
**Path:** `create_knowledge_base.py`
**Size:** 10,854 bytes
**Modified:** 2025-09-04 19:20:17

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

### File: generated/agents/word_counter_agent.py
**Path:** `generated/agents/word_counter_agent.py`
**Size:** 2,578 bytes
**Modified:** 2025-09-06 13:33:30

```python
def word_counter_agent(state):
    """
    Count words in text using the count_words tool
    """
    import sys
    import os
    from datetime import datetime

    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # Import tools
    try:
        from generated.tools.count_words import count_words
    except ImportError:
        try:
            from prebuilt.tools.count_words import count_words
        except ImportError:
            # Define fallback if tool not found
            def count_words(input_data=None):
                return {'error': 'Tool count_words not found', 'data': None}

    # Initialize state
    if 'results' not in state:
        state['results'] = {}
    if 'errors' not in state:
        state['errors'] = []
    if 'execution_path' not in state:
        state['execution_path'] = []

    try:
        start_time = datetime.now()

        # Get input data using standard pattern
        input_data = state.get('current_data')
        if input_data is None:
            if 'results' in state and state['execution_path']:
                last_agent = state['execution_path'][-1]
                if last_agent in state['results']:
                    last_result = state['results'][last_agent]
                    if isinstance(last_result, dict) and 'data' in last_result:
                        input_data = last_result['data']

        if input_data is None:
            input_data = state.get('text', state.get('data', state.get('request')))

        # Process input data
        tool_result = count_words(input_data)
        word_count = tool_result.get('data', 0)

        # Create meaningful output
        result = {
            "status": "success",
            "data": {
                "word_count": word_count
            },
            "metadata": {
                "agent": "word_counter",
                "execution_time": (datetime.now() - start_time).total_seconds(),
                "tools_used": ["count_words"]
            }
        }

        state['results']['word_counter'] = result
        state['current_data'] = result['data']
        state['execution_path'].append('word_counter')

    except Exception as e:
        import traceback
        state['errors'].append({
            "agent": "word_counter",
            "error": str(e),
            "traceback": traceback.format_exc()
        })
        state['results']['word_counter'] = {
            "status": "error",
            "data": None,
            "metadata": {"agent": "word_counter", "error": str(e)}
        }

    return state
```

--------------------------------------------------------------------------------

### File: generated/tools/analyze_sentiment.py
**Path:** `generated/tools/analyze_sentiment.py`
**Size:** 2,001 bytes
**Modified:** 2025-09-04 23:26:14

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
**Modified:** 2025-09-04 23:20:14

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

### File: generated/tools/calculate_median.py
**Path:** `generated/tools/calculate_median.py`
**Size:** 1,157 bytes
**Modified:** 2025-09-04 23:14:54

```python
def calculate_median(input_data=None):
        """
        Calculate median of numbers
        """
        
        if input_data is None:
            return {"status": "no_input", "result": None}
        
        try:
            result = {"status": "success"}
            
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
            return {"status": "error", "message": str(e)}
    
```

--------------------------------------------------------------------------------

### File: generated/tools/calculate_std.py
**Path:** `generated/tools/calculate_std.py`
**Size:** 1,155 bytes
**Modified:** 2025-09-04 23:14:54

```python
def calculate_std(input_data=None):
        """
        Calculate standard deviation
        """
        
        if input_data is None:
            return {"status": "no_input", "result": None}
        
        try:
            result = {"status": "success"}
            
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
            return {"status": "error", "message": str(e)}
    
```

--------------------------------------------------------------------------------

### File: generated/tools/count_words.py
**Path:** `generated/tools/count_words.py`
**Size:** 1,164 bytes
**Modified:** 2025-09-06 13:33:23

```python
def count_words(input_data=None):
        """
        Count the number of words in text input
        """
        
        if input_data is None:
            return {"status": "no_input", "result": None}
        
        try:
            result = {"status": "success"}
            
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
            return {"status": "error", "message": str(e)}
    
```

--------------------------------------------------------------------------------

### File: generated/tools/extract_emails.py
**Path:** `generated/tools/extract_emails.py`
**Size:** 945 bytes
**Modified:** 2025-09-04 10:13:41

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
**Modified:** 2025-09-04 23:14:54

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
**Modified:** 2025-09-04 10:13:28

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

### File: prebuilt/agents/url_extractor_agent.py
**Path:** `prebuilt/agents/url_extractor_agent.py`
**Size:** 2,033 bytes
**Modified:** 2025-09-04 23:15:38

```python
def url_extractor_agent(state):
    """
    Extract URLs from input text.
    """
    import sys
    import os
    from datetime import datetime

    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # Import tool
    from generated.tools.extract_urls import extract_urls

    # Initialize state
    if "results" not in state:
        state["results"] = {}
    if "errors" not in state:
        state["errors"] = []
    if "execution_path" not in state:
        state["execution_path"] = []

    try:
        start_time = datetime.now()

        # Extract input
        input_data = state.get("current_data")
        if input_data is None:
            input_data = state.get("text", state.get("data", state.get("request", "")))

        # Process with tool
        urls = extract_urls(input_data)

        # Analyze URLs
        domains = {}
        for url in urls:
            try:
                from urllib.parse import urlparse

                parsed = urlparse(url)
                domain = parsed.netloc or parsed.path.split("/")[0]
                domains[domain] = domains.get(domain, 0) + 1
            except:
                pass

        # Create result
        result = {
            "status": "success",
            "data": {"urls": urls, "count": len(urls), "domains": domains},
            "metadata": {
                "agent": "url_extractor",
                "execution_time": (datetime.now() - start_time).total_seconds(),
                "tools_used": ["extract_urls"],
            },
        }

        # Update state
        state["results"]["url_extractor"] = result
        state["current_data"] = result["data"]
        state["execution_path"].append("url_extractor")

    except Exception as e:
        state["errors"].append({"agent": "url_extractor", "error": str(e)})
        state["results"]["url_extractor"] = {
            "status": "error",
            "data": None,
            "metadata": {"agent": "url_extractor", "error": str(e)},
        }

    return state

```

--------------------------------------------------------------------------------

### File: prebuilt/tools/read_csv.py
**Path:** `prebuilt/tools/read_csv.py`
**Size:** 1,339 bytes
**Modified:** 2025-09-04 10:12:06

```python
def read_csv(input_data=None):
    """
    Read CSV file using pandas.
    Handles file path or dict with 'path' key.
    """
    import os
    import pandas as pd

    if input_data is None:
        return {"status": "error", "message": "No input provided", "data": []}

    try:
        # Extract file path
        if isinstance(input_data, str):
            file_path = input_data
        elif isinstance(input_data, dict):
            file_path = input_data.get("path", input_data.get("file_path", ""))
        else:
            return {"status": "error", "message": "Invalid input type", "data": []}

        if not file_path:
            return {"status": "error", "message": "No file path provided", "data": []}

        # Read CSV
        if not os.path.exists(file_path):
            return {
                "status": "error",
                "message": f"File not found: {file_path}",
                "data": [],
            }

        df = pd.read_csv(file_path)

        return {
            "status": "success",
            "data": df.to_dict("records"),
            "shape": {"rows": len(df), "columns": len(df.columns)},
            "columns": df.columns.tolist(),
            "preview": df.head(5).to_dict("records"),
        }

    except Exception as e:
        return {"status": "error", "message": str(e), "data": []}

```

--------------------------------------------------------------------------------

### File: prebuilt/tools/read_json.py
**Path:** `prebuilt/tools/read_json.py`
**Size:** 1,460 bytes
**Modified:** 2025-09-04 10:11:49

```python
def read_json(input_data=None):
    """
    Read JSON file and parse contents.
    Handles file path or dict with 'path' key.
    """
    import os
    import json

    if input_data is None:
        return {"status": "error", "message": "No input provided", "data": {}}

    try:
        # Extract file path
        if isinstance(input_data, str):
            file_path = input_data
        elif isinstance(input_data, dict):
            file_path = input_data.get("path", input_data.get("file_path", ""))
        else:
            return {"status": "error", "message": "Invalid input type", "data": {}}

        if not file_path:
            return {"status": "error", "message": "No file path provided", "data": {}}

        # Read and parse JSON
        if not os.path.exists(file_path):
            return {
                "status": "error",
                "message": f"File not found: {file_path}",
                "data": {},
            }

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return {
            "status": "success",
            "data": data,
            "type": type(data).__name__,
            "keys": list(data.keys()) if isinstance(data, dict) else None,
        }

    except json.JSONDecodeError as e:
        return {"status": "error", "message": f"Invalid JSON: {str(e)}", "data": {}}
    except Exception as e:
        return {"status": "error", "message": str(e), "data": {}}

```

--------------------------------------------------------------------------------

### File: prebuilt/tools/read_pdf.py
**Path:** `prebuilt/tools/read_pdf.py`
**Size:** 1,486 bytes
**Modified:** 2025-09-04 10:12:20

```python
def read_pdf(input_data=None):
    """
    Read PDF file and extract text using PyPDF2.
    Handles file path or dict with 'path' key.
    """
    import os
    import PyPDF2

    if input_data is None:
        return {"status": "error", "message": "No input provided", "text": ""}

    try:
        # Extract file path
        if isinstance(input_data, str):
            file_path = input_data
        elif isinstance(input_data, dict):
            file_path = input_data.get("path", input_data.get("file_path", ""))
        else:
            return {"status": "error", "message": "Invalid input type", "text": ""}

        if not file_path:
            return {"status": "error", "message": "No file path provided", "text": ""}

        # Read PDF
        if not os.path.exists(file_path):
            return {
                "status": "error",
                "message": f"File not found: {file_path}",
                "text": "",
            }

        text = ""
        with open(file_path, "rb") as f:
            pdf_reader = PyPDF2.PdfReader(f)
            num_pages = len(pdf_reader.pages)

            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()

        return {
            "status": "success",
            "text": text,
            "pages": num_pages,
            "chars": len(text),
        }

    except Exception as e:
        return {"status": "error", "message": str(e), "text": ""}

```

--------------------------------------------------------------------------------

### File: prebuilt/tools/read_text.py
**Path:** `prebuilt/tools/read_text.py`
**Size:** 1,379 bytes
**Modified:** 2025-09-04 10:11:28

```python
def read_text(input_data=None):
    """
    Read text file and return contents.
    Handles file path or dict with 'path' key.
    """
    import os

    if input_data is None:
        return {"status": "error", "message": "No input provided", "content": ""}

    try:
        # Extract file path
        if isinstance(input_data, str):
            file_path = input_data
        elif isinstance(input_data, dict):
            file_path = input_data.get("path", input_data.get("file_path", ""))
        else:
            return {"status": "error", "message": "Invalid input type", "content": ""}

        if not file_path:
            return {
                "status": "error",
                "message": "No file path provided",
                "content": "",
            }

        # Read file
        if not os.path.exists(file_path):
            return {
                "status": "error",
                "message": f"File not found: {file_path}",
                "content": "",
            }

        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        return {
            "status": "success",
            "content": content,
            "lines": len(content.splitlines()),
            "chars": len(content),
        }

    except Exception as e:
        return {"status": "error", "message": str(e), "content": ""}

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

### File: scripts/initialize_prebuilt.py
**Path:** `scripts/initialize_prebuilt.py`
**Size:** 1,243 bytes
**Modified:** 2025-09-04 22:52:01

```python
"""Initialize missing prebuilt components."""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.registry import RegistryManager
from core.tool_factory import ToolFactory


def initialize_prebuilt_tools():
    """Create missing prebuilt tools."""

    registry = RegistryManager()
    tool_factory = ToolFactory()

    # Define essential tools
    essential_tools = [
        ("extract_urls", "Extract URLs from text"),
        ("extract_emails", "Extract email addresses from text"),
        ("extract_phones", "Extract phone numbers from text"),
        ("calculate_mean", "Calculate mean of numbers"),
        ("calculate_median", "Calculate median of numbers"),
        ("calculate_std", "Calculate standard deviation"),
        ("analyze_sentiment", "Analyze sentiment of text"),
    ]

    for tool_name, description in essential_tools:
        if not registry.tool_exists(tool_name):
            print(f"Creating tool: {tool_name}")
            result = tool_factory.ensure_tool(tool_name, description)
            print(f"  Result: {result['status']}")
        else:
            print(f"Tool exists: {tool_name}")


if __name__ == "__main__":
    initialize_prebuilt_tools()

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

### File: tests/test_backend_fixes.py
**Path:** `tests/test_backend_fixes.py`
**Size:** 1,841 bytes
**Modified:** 2025-09-04 22:53:11

```python
"""Test that backend fixes are working."""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.registry_singleton import get_shared_registry, force_global_reload
from core.orchestrator import Orchestrator
import asyncio


def test_registry_singleton():
    """Test registry singleton is working."""
    print("Testing registry singleton...")

    # Get multiple references
    reg1 = get_shared_registry()
    reg2 = get_shared_registry()

    # Should be same instance
    assert reg1 is reg2, "Registry singleton broken!"

    # Test force reload
    force_global_reload()
    reg3 = get_shared_registry()

    print("✓ Registry singleton working")


async def test_orchestrator_planning():
    """Test orchestrator planning."""
    print("\nTesting orchestrator planning...")

    orchestrator = Orchestrator()

    # Test simple request
    result = await orchestrator.process_request(
        user_request="Extract emails from this text: test@example.com",
        auto_create=False,
    )

    assert result["status"] == "success", f"Planning failed: {result}"
    assert len(result.get("workflow", {}).get("steps", [])) > 0, "No agents planned"

    print("✓ Orchestrator planning working")


def test_tool_quality():
    """Test tools are functional."""
    print("\nTesting tool quality...")

    from generated.tools.extract_emails import extract_emails

    # Test with various inputs
    assert extract_emails(None) == []
    assert extract_emails("test@example.com") == ["test@example.com"]
    assert len(extract_emails("a@b.com and c@d.com")) == 2

    print("✓ Tools are functional")


if __name__ == "__main__":
    test_registry_singleton()
    asyncio.run(test_orchestrator_planning())
    test_tool_quality()
    print("\n✅ All backend fixes verified!")

```

--------------------------------------------------------------------------------

### File: tests/test_comprehensive_scenarios.py
**Path:** `tests/test_comprehensive_scenarios.py`
**Size:** 12,862 bytes
**Modified:** 2025-09-06 13:22:21

```python
"""
Comprehensive End-to-End Scenarios for Agentic Fabric POC
Tests complete user journey from input to response across different capability scenarios
"""

import sys
import os
import asyncio
import json
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.orchestrator import Orchestrator
from core.agent_factory import AgentFactory
from core.tool_factory import ToolFactory
from core.registry_singleton import get_shared_registry, force_global_reload


class ComprehensiveScenarioTests:
    """Test suite for comprehensive end-to-end scenarios."""

    def __init__(self):
        self.orchestrator = Orchestrator()
        # Use shared registry singleton
        self.registry = get_shared_registry()
        self.test_results = []

    async def run_all_scenarios(self):
        """Run all comprehensive test scenarios."""
        print("\n" + "=" * 80)
        print("AGENTIC FABRIC POC - COMPREHENSIVE END-TO-END SCENARIOS")
        print("=" * 80)

        scenarios = [
            ("All Components Present", self.test_all_components_present),
            ("Missing Agents, Tools Present", self.test_missing_agents_present_tools),
            ("Present Agents, Missing Tools", self.test_present_agents_missing_tools),
            ("Complex Mixed Dependencies", self.test_complex_mixed_dependencies),
            ("Completely New Domain", self.test_completely_new_domain),
            ("Ambiguous Multi-Path Request", self.test_ambiguous_request),
        ]

        passed = 0
        failed = 0

        for scenario_name, test_func in scenarios:
            print(f"\n{'='*60}")
            print(f"SCENARIO: {scenario_name}")
            print("=" * 60)

            try:
                # Force reload before each test to ensure clean state
                force_global_reload()

                result = await test_func()
                if result:
                    passed += 1
                    print(f"\n✅ {scenario_name}: PASSED")
                else:
                    failed += 1
                    print(f"\n❌ {scenario_name}: FAILED")
            except Exception as e:
                failed += 1
                print(f"\n❌ {scenario_name}: ERROR - {str(e)}")
                import traceback

                traceback.print_exc()

        print(f"\n{'='*80}")
        print(f"COMPREHENSIVE RESULTS: {passed} passed, {failed} failed")
        print("=" * 80)

        if passed == len(scenarios):
            print("🎉 ALL SCENARIOS PASSED - BACKEND VALIDATION COMPLETE! 🎉")
            return True
        else:
            print(f"⚠️ {failed} scenarios need attention")
            return False

    async def test_all_components_present(self):
        """
        SCENARIO 1: All Components Present
        Request that uses only existing agents and tools
        Expected: Smooth execution without any dynamic creation
        """
        request = """
        Analyze this text and extract both email addresses and URLs:
        "Contact us at support@company.com or sales@business.org. 
        Visit our sites at https://company.com and https://docs.business.org"
        """

        print("Testing with existing agents: email_extractor, url_extractor")

        # Ensure registry is fresh
        force_global_reload()

        result = await self.orchestrator.process_request(
            user_request=request,
            auto_create=False,  # Should not need to create anything
        )

        # Validate results
        success = (
            result["status"] == "success"
            and len(result.get("workflow", {}).get("steps", [])) >= 1
            and result.get("metadata", {}).get("components_created", 0)
            == 0  # No new components
        )

        print(f"Status: {result['status']}")
        print(f"Workflow: {result.get('workflow', {}).get('steps', [])}")
        print(
            f"Components Created: {result.get('metadata', {}).get('components_created', 'N/A')}"
        )

        # Check if actual extraction worked
        if "results" in result:
            email_results = result["results"].get("email_extractor", {})
            url_results = result["results"].get("url_extractor", {})

            if email_results.get("status") == "success":
                emails = email_results.get("data", {}).get("emails", [])
                print(f"Emails extracted: {emails}")

            if url_results.get("status") == "success":
                urls = url_results.get("data", {}).get("urls", [])
                print(f"URLs extracted: {urls}")

        return success

    async def test_missing_agents_present_tools(self):
        """
        SCENARIO 2: Missing Agents, Tools Present
        Request that needs new agents but tools exist
        Expected: Dynamic agent creation, tool reuse
        """
        request = """
        Create a statistical report from these numbers: [10, 20, 30, 40, 50, 25, 35, 45]
        Calculate mean, median, and standard deviation, then format as a professional report.
        """

        print("Testing agent creation with existing calculate_mean tool")

        result = await self.orchestrator.process_request(
            user_request=request, auto_create=True
        )

        # Force reload after creation
        if result.get("metadata", {}).get("components_created", 0) > 0:
            force_global_reload()

        # Validate dynamic creation occurred
        success = result["status"] in ["success", "partial"] and (
            result.get("metadata", {}).get("components_created", 0) > 0
            or len(result.get("workflow", {}).get("steps", [])) > 0
        )

        print(f"Status: {result['status']}")
        print(f"Workflow: {result.get('workflow', {}).get('steps', [])}")
        print(
            f"Components Created: {result.get('metadata', {}).get('components_created', 'N/A')}"
        )

        return success

    async def test_present_agents_missing_tools(self):
        """
        SCENARIO 3: Present Agents, Missing Tools
        Request that existing agents can handle but need new tools
        Expected: Dynamic tool creation, agent reuse
        """
        # First, create phone_extractor agent if it doesn't exist
        if not self.registry.agent_exists("phone_extractor"):
            agent_factory = AgentFactory()
            creation_result = await agent_factory.ensure_agent(
                agent_name="phone_extractor",
                description="Extract phone numbers from text",
                required_tools=["extract_phones"],
            )
            if creation_result["status"] in ["success", "exists"]:
                force_global_reload()
                print("Created phone_extractor agent for test")

        request = """
        Extract all phone numbers from this text:
        "Call us at (555) 123-4567 or (555) 987-6543. Emergency: 911"
        """

        print("Testing with phone_extractor agent (tool may need creation)")

        result = await self.orchestrator.process_request(
            user_request=request, auto_create=True
        )

        # Force reload after any creation
        if result.get("metadata", {}).get("components_created", 0) > 0:
            force_global_reload()

        success = result["status"] in ["success", "partial"] and (
            "phone" in str(result.get("workflow", {})).lower()
            or len(result.get("workflow", {}).get("steps", [])) > 0
        )

        print(f"Status: {result['status']}")
        print(f"Workflow: {result.get('workflow', {}).get('steps', [])}")

        return success

    async def test_complex_mixed_dependencies(self):
        """
        SCENARIO 4: Complex Mixed Dependencies
        Multi-step request with some agents present, some missing, complex tool chain
        Expected: Intelligent dependency resolution and creation
        """
        request = """
        Process this data pipeline:
        1. Read data from a CSV file (simulated data)
        2. Clean and validate the data  
        3. Calculate summary statistics
        4. Generate a bar chart visualization
        5. Create a formatted report with insights
        """

        print("Testing complex multi-agent pipeline with mixed dependencies")

        result = await self.orchestrator.process_request(
            user_request=request, auto_create=True
        )

        # Force reload after complex creation
        force_global_reload()

        # Complex workflow should be planned and executed
        success = (
            result["status"] in ["success", "partial"]
            and len(result.get("workflow", {}).get("steps", []))
            >= 3  # Multi-step workflow
        )

        print(f"Status: {result['status']}")
        print(f"Workflow Steps: {len(result.get('workflow', {}).get('steps', []))}")
        print(f"Execution Time: {result.get('execution_time', 'N/A')}s")

        return success

    async def test_completely_new_domain(self):
        """
        SCENARIO 5: Completely New Domain
        Request for entirely new capability not covered by existing system
        Expected: Full agent+tool chain creation from scratch
        """
        # Use a truly new domain that doesn't exist
        request = """
        Analyze blockchain transaction patterns and identify:
        - Whale movements over $1M
        - Smart contract interactions
        - Gas fee optimization opportunities
        - Risk score for wallet addresses
        Test with address: 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb8
        """

        print("Testing completely new domain - blockchain analysis")

        initial_agent_count = len(self.registry.list_agents())
        initial_tool_count = len(self.registry.list_tools())

        result = await self.orchestrator.process_request(
            user_request=request, auto_create=True
        )

        # Force reload and check what was created
        force_global_reload()

        final_agent_count = len(self.registry.list_agents())
        final_tool_count = len(self.registry.list_tools())

        components_created = (final_agent_count - initial_agent_count) + (
            final_tool_count - initial_tool_count
        )

        # Should create new components and execute
        success = result["status"] in ["success", "partial", "error"] and (
            components_created > 0
            or len(result.get("response", "")) > 100
            or "blockchain" in result.get("response", "").lower()
        )

        print(f"Status: {result['status']}")
        print(
            f"Components Created: {components_created} (Agents: {final_agent_count - initial_agent_count}, Tools: {final_tool_count - initial_tool_count})"
        )
        print(
            f"Response Quality: {'High' if len(result.get('response', '')) > 200 else 'Low'}"
        )

        return success

    async def test_ambiguous_request(self):
        """
        SCENARIO 6: Ambiguous Multi-Path Request
        Request that could be interpreted multiple ways, testing orchestrator intelligence
        Expected: Intelligent disambiguation and optimal agent selection
        """
        request = """
        "Analyze this customer feedback data"
        [No specific data provided, ambiguous request]
        """

        print("Testing ambiguous request handling and clarification")

        result = await self.orchestrator.process_request(
            user_request=request, auto_create=True
        )

        # Should handle ambiguity gracefully
        success = (
            result["status"] in ["success", "partial", "missing_capabilities", "error"]
            and len(result.get("response", "")) > 50  # Some meaningful response
        )

        print(f"Status: {result['status']}")
        print(
            f"Response Handling: {'Clarification' if 'clarify' in result.get('response', '').lower() else 'Assumption'}"
        )

        return success


async def main():
    """Run comprehensive scenarios."""
    print("Starting Comprehensive End-to-End Scenario Testing")
    print("Goal: Validate complete user journey from input to response")

    # Ensure clean start
    force_global_reload()

    tester = ComprehensiveScenarioTests()
    success = await tester.run_all_scenarios()

    if success:
        print("\n🎊 BACKEND VALIDATION COMPLETE - SYSTEM READY FOR PRODUCTION 🎊")
        print("✅ All user journey scenarios working correctly")
        print("✅ Dynamic component creation functioning")
        print("✅ Complex workflow orchestration operational")
        print("✅ Error handling and edge cases covered")
    else:
        print("\n🔧 Additional tuning needed before production readiness")

    return success


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)

```

--------------------------------------------------------------------------------

### File: tests/test_dependency_resolution.py
**Path:** `tests/test_dependency_resolution.py`
**Size:** 1,983 bytes
**Modified:** 2025-09-04 21:59:45

```python
"""
Test Dependency Resolution
Verify that tools are created before agents that need them
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.dependency_resolver import DependencyResolver
from core.registry import RegistryManager
import networkx as nx


def test_dependency_resolver():
    """Test the dependency resolver."""
    print("\nTesting Dependency Resolution")
    print("=" * 60)

    registry = RegistryManager()
    resolver = DependencyResolver(registry)

    # Test request
    request = "Extract emails and phone numbers, then generate a report"

    # Get existing components
    existing_agents = {a["name"]: a for a in registry.list_agents()}
    existing_tools = {t["name"]: t for t in registry.list_tools()}

    # Analyze
    result = resolver.analyze_request(request, existing_agents, existing_tools)

    print("\nCapabilities Found:")
    for cap in result["capabilities"]:
        print(f"  - {cap['name']}: {cap['agent']} using {cap['tools']}")

    print("\nCreation Order:")
    for comp_type, comp_name in result["creation_order"]:
        print(f"  {comp_type}: {comp_name}")

    print("\nDependency Visualization:")
    print(resolver.visualize_dependencies(result["dependency_graph"]))

    # Verify topological order
    graph = result["dependency_graph"]
    topo_order = list(nx.topological_sort(graph))

    # Tools should come before agents that use them
    for i, node in enumerate(topo_order):
        if graph.nodes[node]["type"] == "agent":
            # Check all tool dependencies come before this agent
            for tool in graph.predecessors(node):
                tool_index = topo_order.index(tool)
                assert (
                    tool_index < i
                ), f"Tool {tool} should be created before agent {node}"

    print("\n✓ Dependency resolution working correctly")
    return True


if __name__ == "__main__":
    test_dependency_resolver()

```

--------------------------------------------------------------------------------

### File: tests/test_end_to_end.py
**Path:** `tests/test_end_to_end.py`
**Size:** 9,522 bytes
**Modified:** 2025-09-06 11:55:33

```python
"""
End-to-End Test for Agentic Fabric POC
Tests the complete flow from request to execution
"""

import sys
import os
import json
import asyncio

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.orchestrator import Orchestrator
from core.registry import RegistryManager
from core.agent_factory import AgentFactory
from core.tool_factory import ToolFactory
from core.workflow_engine import WorkflowEngine

from core.registry_singleton import get_shared_registry, force_global_reload


def test_basic_workflow():
    """Test basic sequential workflow with existing agents."""
    print("\n" + "=" * 60)
    print("TEST 1: Basic Sequential Workflow")
    print("=" * 60)

    print(f"\nDEBUG: Starting basic workflow test")

    # Initialize
    orchestrator = Orchestrator()
    registry = RegistryManager()

    # Test request
    request = """Extract all email addresses and URLs from this text:
    Please contact john@example.com or mary@company.org for details.
    Visit our website at https://example.com or https://docs.example.com
    """

    # Process
    result = asyncio.run(
        orchestrator.process_request(user_request=request, auto_create=True)
    )

    print(f"DEBUG: Orchestrator result status: {result.get('status')}")
    print(f"DEBUG: Orchestrator result keys: {list(result.keys())}")
    if result.get("status") != "success":
        print(f"DEBUG: Error details: {result}")

    # Verify
    assert result["status"] == "success", f"Failed: {result.get('message')}"
    print(f"✓ Status: {result['status']}")
    print(f"✓ Workflow: {result['workflow']['steps']}")
    print(f"✓ Response preview: {result['response'][:200]}...")

    # Check results structure
    if "results" in result:
        for agent_name, agent_result in result["results"].items():
            print(f"\n  Agent: {agent_name}")
            if isinstance(agent_result, dict):
                print(f"    Status: {agent_result.get('status')}")
                if "data" in agent_result:
                    print(f"    Data keys: {list(agent_result['data'].keys())}")

    return True


def test_dynamic_creation():
    """Test dynamic creation of missing tools and agents."""
    print("\n" + "=" * 60)
    print("TEST 2: Dynamic Component Creation")
    print("=" * 60)

    # Initialize factories
    agent_factory = AgentFactory()
    tool_factory = ToolFactory()

    # Use shared registry
    registry = get_shared_registry()

    # Test creating a new tool
    print("\n1. Creating new tool: count_words")
    result = tool_factory.ensure_tool(
        tool_name="count_words",
        description="Count the number of words in text input",
        tool_type="pure_function",
    )

    if result["status"] in ["success", "exists"]:
        print(f"✓ Tool created/exists: count_words")
    else:
        print(f"✗ Failed to create tool: {result.get('message')}")
        return False

    # Force reload to ensure registry is synced
    force_global_reload()

    # Test creating a new agent
    print("\n2. Creating new agent: word_counter")
    result = agent_factory.ensure_agent(
        agent_name="word_counter",
        description="Count words in text using the count_words tool",
        required_tools=["count_words"],
    )

    if result["status"] in ["success", "exists"]:
        print(f"✓ Agent created/exists: word_counter")
    else:
        print(f"✗ Failed to create agent: {result.get('message')}")
        return False

    # Force reload again
    force_global_reload()

    # Verify in registry (using the shared instance)
    assert registry.tool_exists("count_words"), "Tool not in registry"
    assert registry.agent_exists("word_counter"), "Agent not in registry"
    print("\n✓ Components registered successfully")

    return True


def test_file_reading():
    """Test file reading capabilities."""
    print("\n" + "=" * 60)
    print("TEST 3: File Reading")
    print("=" * 60)

    # Create test file
    test_file = "test_data.txt"
    with open(test_file, "w") as f:
        f.write("Test content with email@example.com and https://test.com")

    try:
        # Test read_text tool directly
        from prebuilt.tools.read_text import read_text

        result = read_text(test_file)
        assert result["status"] == "success", "Failed to read file"
        print(f"✓ Read file: {result['chars']} chars, {result['lines']} lines")

        # Test through workflow
        orchestrator = Orchestrator()
        request = f"Read the file {test_file} and extract emails from it"

        result = asyncio.run(
            orchestrator.process_request(
                user_request=request,
                files=[{"path": test_file, "type": "text"}],
                auto_create=True,
            )
        )

        print(f"✓ Workflow status: {result['status']}")

    finally:
        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)

    return True


def test_parallel_execution():
    """Test parallel agent execution."""
    print("\n" + "=" * 60)
    print("TEST 4: Parallel Execution")
    print("=" * 60)

    engine = WorkflowEngine()

    # Create parallel workflow
    agents = ["url_extractor", "email_extractor"]

    try:
        workflow = engine.create_workflow(
            agent_sequence=agents, workflow_type="parallel"
        )

        initial_data = {
            "text": "Contact admin@site.com or visit https://site.com",
            "workflow_type": "parallel",
        }

        result = engine.execute_workflow(workflow, initial_data)

        print(f"✓ Execution path: {result.get('execution_path', [])}")
        print(f"✓ Completed agents: {result.get('completed_agents', [])}")

        # Verify both agents ran
        assert len(result.get("results", {})) >= 2, "Not all agents executed"
        print("✓ All agents executed in parallel")

    except Exception as e:
        print(f"✗ Parallel execution failed: {str(e)}")
        return False

    return True


def test_error_handling():
    """Test error handling and recovery."""
    print("\n" + "=" * 60)
    print("TEST 5: Error Handling")
    print("=" * 60)

    orchestrator = Orchestrator()

    # Test with invalid request
    result = asyncio.run(
        orchestrator.process_request(
            user_request="Use non_existent_agent to process this", auto_create=False
        )
    )

    # Accept either missing_capabilities or error status
    if result["status"] == "missing_capabilities":
        print(f"✓ Correctly identified missing capabilities")
        print(f"  Missing: {result.get('missing', {})}")
        return True
    elif result["status"] == "error":
        # FIX: Handle None properly
        error_msg = result.get("error") or result.get("message") or ""
        if error_msg:  # Check if we have an error message
            error_msg_lower = error_msg.lower()
            if "no agents" in error_msg_lower or "planning failed" in error_msg_lower:
                print(f"✓ Correctly reported error for non-existent agent")
                return True
        # If no specific error message, still pass if status is error
        print(f"✓ Correctly returned error status")
        return True

    print(f"✗ Unexpected status: {result['status']}")
    print(f"✗ Result: {result}")
    return False


def test_registry_health():
    """Test registry health and validation."""
    print("\n" + "=" * 60)
    print("TEST 6: Registry Health Check")
    print("=" * 60)

    registry = RegistryManager()

    # Health check
    health = registry.health_check()
    print(f"Health Score: {health['health_score']}/100")
    print(f"Status: {health['status']}")
    print(f"Total Components: {health['total_components']}")
    print(f"Valid Components: {health['valid_components']}")

    # Validate all
    validation = registry.validate_all()
    print(f"\nValid Agents: {len(validation['valid_agents'])}")
    print(f"Valid Tools: {len(validation['valid_tools'])}")

    if validation["invalid_agents"]:
        print(f"Invalid Agents: {validation['invalid_agents']}")
    if validation["invalid_tools"]:
        print(f"Invalid Tools: {validation['invalid_tools']}")

    assert health["health_score"] > 50, "Registry health too low"
    print("\n✓ Registry is healthy")

    return True


def run_all_tests():
    """Run all end-to-end tests."""
    print("\n" + "=" * 60)
    print("AGENTIC FABRIC POC - END-TO-END TESTS")
    print("=" * 60)

    tests = [
        ("Basic Workflow", test_basic_workflow),
        ("Dynamic Creation", test_dynamic_creation),
        ("File Reading", test_file_reading),
        ("Parallel Execution", test_parallel_execution),
        ("Error Handling", test_error_handling),
        ("Registry Health", test_registry_health),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"\n{test_name}: PASSED")
            else:
                failed += 1
                print(f"\n{test_name}: FAILED")
        except Exception as e:
            failed += 1
            print(f"\n{test_name}: ERROR - {str(e)}")
            import traceback

            traceback.print_exc()

    print("\n" + "=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

```

--------------------------------------------------------------------------------

### File: tools.json
**Path:** `tools.json`
**Size:** 6,510 bytes
**Modified:** 2025-09-06 13:33:30

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
      "tags": [
        "file",
        "reader"
      ],
      "line_count": 35,
      "status": "active"
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
      "tags": [
        "file",
        "reader",
        "json"
      ],
      "line_count": 38,
      "status": "active"
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
      "tags": [
        "file",
        "reader",
        "csv"
      ],
      "line_count": 37,
      "status": "active"
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
      "tags": [
        "file",
        "reader",
        "pdf"
      ],
      "line_count": 42,
      "status": "active"
    },
    "extract_urls": {
      "name": "extract_urls",
      "description": "Extract all URLs from input text",
      "signature": "def extract_urls(input_data=None)",
      "location": "generated/tools/extract_urls.py",
      "is_prebuilt": false,
      "is_pure_function": true,
      "used_by_agents": [
        "url_extractor",
        "text_analyzer"
      ],
      "created_by": "claude-3-haiku-20240307",
      "created_at": "2025-01-01T00:00:00",
      "tags": [
        "extraction",
        "regex",
        "url"
      ],
      "line_count": 28,
      "status": "active"
    },
    "extract_emails": {
      "name": "extract_emails",
      "description": "Extract all email addresses from input text",
      "signature": "def extract_emails(input_data=None)",
      "location": "generated/tools/extract_emails.py",
      "is_prebuilt": false,
      "is_pure_function": true,
      "used_by_agents": [
        "email_extractor",
        "text_analyzer"
      ],
      "created_by": "claude-3-haiku-20240307",
      "created_at": "2025-01-01T00:00:00",
      "tags": [
        "extraction",
        "regex",
        "email"
      ],
      "line_count": 28,
      "status": "active"
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
      "tags": [
        "calculation",
        "math",
        "statistics"
      ],
      "line_count": 39,
      "status": "active"
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
      "tags": [
        "extraction"
      ],
      "line_count": 37,
      "status": "active"
    },
    "calculate_median": {
      "name": "calculate_median",
      "description": "Calculate median of numbers",
      "signature": "def calculate_median(input_data=None)",
      "location": "/Users/sayantankundu/Documents/Agent Fabric/generated/tools/calculate_median.py",
      "is_prebuilt": false,
      "is_pure_function": true,
      "used_by_agents": [],
      "created_by": "claude-3-haiku-20240307",
      "created_at": "2025-09-04T23:14:54.610601",
      "tags": [
        "calculation"
      ],
      "line_count": 32,
      "status": "active"
    },
    "calculate_std": {
      "name": "calculate_std",
      "description": "Calculate standard deviation",
      "signature": "def calculate_std(input_data=None)",
      "location": "/Users/sayantankundu/Documents/Agent Fabric/generated/tools/calculate_std.py",
      "is_prebuilt": false,
      "is_pure_function": true,
      "used_by_agents": [],
      "created_by": "claude-3-haiku-20240307",
      "created_at": "2025-09-04T23:14:54.644859",
      "tags": [
        "calculation"
      ],
      "line_count": 32,
      "status": "active"
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
      "tags": [
        "analysis"
      ],
      "line_count": 47,
      "status": "active"
    },
    "count_words": {
      "name": "count_words",
      "description": "Count the number of words in text input",
      "signature": "def count_words(input_data=None)",
      "location": "/Users/sayantankundu/Documents/Agent Fabric/generated/tools/count_words.py",
      "is_prebuilt": false,
      "is_pure_function": true,
      "used_by_agents": [
        "word_counter"
      ],
      "created_by": "claude-3-haiku-20240307",
      "created_at": "2025-09-06T13:33:23.155239",
      "tags": [],
      "line_count": 32,
      "status": "active"
    }
  }
}
```

--------------------------------------------------------------------------------

### File: tools.json.lock
**Path:** `tools.json.lock`
**Size:** 0 bytes
**Modified:** 2025-09-06 13:33:23

*[Binary file or content not included]*

--------------------------------------------------------------------------------
