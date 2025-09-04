# Agent Fabric — Design Doc And Roadmap

## 1) Problem Statement

Your current agent set feels too complex and monolithic. The vision is an **agent fabric** where agents are created on demand by an LLM (e.g., Claude) and registered automatically. Today’s large, pre-baked agents make that unrealistic: no API can reliably generate, maintain, and safely extend 500–1000 line agents end‑to‑end.

**We need a simpler, composable pattern** that the agent fabric can genuinely automate:

* Keep agents **narrow** (single responsibility).
* Push reusable logic into **pure tools** (stateless functions).
* Let an **Orchestrator LLM** plan and sequence agents dynamically.
* Persist capabilities in **lightweight registries** (agents.json, tools.json).

---

## 2) Goals & Non‑Goals

### Goals

* **Minimal Viable Agents (MVAs):** Agents do one thing well (read/parse/extract/format).
* **Pure Tools:** Small, stateless utilities that agents import and compose.
* **Dual Registry:** Track agents and tools separately for maximum reuse.
* **On‑Demand Generation:** If a capability is missing, let the LLM generate it and register it.
* **Standard I/O Contracts:** Every agent speaks a simple JSON envelope so outputs are chainable.
* **LangGraph Orchestration:** Use LangGraph for state, branching, retries, and visualization.

### Non‑Goals (for now)

* Building rich, domain‑heavy agents (e.g., fully featured “ticketing platform” agent).
* Supporting many vendors at once. Start with **one** (e.g., Jira) and add others on demand.
* Long‑lived agent state. Prefer stateless execution; keep state in the workflow engine.

---

## 3) Design Principles

1. **Small Pieces, Loosely Joined:** Agents are \~50–300 LOC; tools are \~20–100 LOC.
2. **Single Responsibility:** Each agent/tool does one thing; composition yields power.
3. **Stateless & Deterministic:** Tools must be pure; agents minimize side effects.
4. **Centralized Intelligence:** Only the Orchestrator decides workflow (no `next_actions` in agents).
5. **Explicit Contracts:** Uniform JSON I/O so components can plug together safely.
6. **Generate Late:** Prefer generating new agents/tools when (and only when) needed.

---

## 4) High‑Level Architecture

```
User Request → Orchestrator LLM → agents.json / tools.json (capability lookup)
                              ↘ missing? → Codegen (LLM) → Tool/Agent Factory → Registry update
                                           ↘ tests/validation → (accept or reject)
Then: Orchestrator builds a LangGraph workflow → Execute → Collect results → Respond
```

**Why this works:** The Orchestrator plans; registries declare what exists; factories generate the smallest new pieces required; LangGraph executes robustly.

---

## 4a) End‑to‑End Flow (Request → Registries → Codegen → LangGraph)

### Plain‑language Summary

1. **User asks for something.**
2. **Orchestrator** (LLM) translates that ask into needed capabilities.
3. It **checks the registries** to see what agents/tools already exist.
4. If something is **missing**, it asks the **factories** to generate the smallest new pieces (tools first, then agents).
5. New code is **validated & registered**.
6. Orchestrator **builds a workflow** (LangGraph) from the available agents.
7. LangGraph **executes** the workflow and returns results.
8. Orchestrator **synthesizes** the final answer.

### Step‑by‑Step (mirrors your sketch)

1. **User Request** → goes to **GPT‑4 Orchestrator**.
2. Orchestrator **parses intent** and identifies required agent(s): e.g., `extract_urls`.
3. **Lookup** `agents.json` → “Does `extract_urls` exist?”

   * **If yes:** continue to step 7.
   * **If no:** derive dependencies → e.g., needs `regex_matcher` tool.
4. **Lookup** `tools.json` → “Does `regex_matcher` exist?”

   * **If yes:** proceed.
   * **If no:** **Tool Factory** generates `regex_matcher` → validate → **register** in `tools.json`.
5. **Agent Factory** generates `extract_urls` that **imports** `regex_matcher` → validate → **register** in `agents.json`.
6. (Optional) **Smoke tests** run with tiny fixtures to ensure agent+tool behave as expected.
7. Orchestrator **builds LangGraph workflow** (nodes=agents, edges=data handoff).
8. **Execute** workflow via LangGraph with retries, capture timings and outputs.
9. **Collect** standard envelopes from each node, update run logs and metrics.
10. **Synthesize & return** final result to the user.

### Swimlane (conceptual)

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

* **Idempotent creation:** `ensure(name)` checks the registry and reuses existing code.
* **Smallest diff:** Only missing **tools first**, then the **agents** that import them.
* **Uniform contracts:** Every agent returns the standard JSON envelope; tools are pure functions.
* **Safety gates:** Code runs through validation (imports allow‑list, purity/unit tests, size budgets).
* **Observability:** Each step logs timings, creation events, and registry updates.

### Concrete Example (your `extract_urls` case)

* Request: “Find links in this PDF.”
* Orchestrator maps to `read_pdf` → `extract_urls`.
* `extract_urls` depends on `regex_matcher`.
* If `regex_matcher` absent → Tool Factory creates it → register in `tools.json`.
* If `extract_urls` absent → Agent Factory creates it importing `regex_matcher` → register in `agents.json`.
* Orchestrator builds graph: `read_pdf` → `extract_urls` → (optional) `fetch_webpage` → `summarize`.
* Run in LangGraph; return normalized JSON with URLs + counts; orchestrator formats the final answer.

---

## 5) Core Components

### 5.1 Orchestrator LLM

* Parses the user request, maps to available capabilities.
* If capability is missing, triggers codegen via factories.
* Builds the workflow (nodes=agents; edges=data flow) and executes via LangGraph.
* Aggregates outputs and formats the final response.

### 5.2 Dual Registry (files)

* **agents.json** — responsibilities, tool deps, input/output schemas, location, metadata.
* **tools.json** — signatures of pure utilities, locations, metadata, usage.

### 5.3 Tool Factory (codegen + validation)

* Given a spec/signature, requests the LLM to generate a **pure function** tool.
* Validates: lint, import safety, unit tests for sample cases, purity checks (no I/O unless declared).
* On success: writes file, updates tools.json.

### 5.4 Agent Factory (codegen + validation)

* Given an intent and required tools, asks the LLM to generate a **small agent** that imports tools.
* Validates: schema conformance, envelope format, unit tests with fixtures.
* On success: writes file, updates agents.json.

### 5.5 Workflow Engine (LangGraph)

* Maintains **workflow state**, retries, error edges, and conditional branching.
* Records execution path and per‑node timings.
* Exposes a visualization hook for debugging.

### 5.6 Minimal Pre‑built Components

* **Readers:** pdf/csv/json/text (thin wrappers only).
* **Connectors:** single vendor to start (e.g., Jira). Others are generated later.
* **Auth helpers:** scoped and explicit; no hidden side effects.

---

## 6) Contracts (No `next_actions`)

### 6.1 Standard Agent Output Envelope

```json
{
  "status": "success" | "error",
  "data": { /* agent-specific payload */ },
  "metadata": {
    "agent": "string",
    "tools_used": ["string"],
    "execution_time": 0.0,
    "version": "semver"
  }
}
```

### 6.2 Tool Signature Guidelines

* All tools are **pure**: input args → return value; no global state; no network unless declared connector.
* Prefer explicit, typed arguments; avoid implicit environment reads.
* Return simple Python/JSON‑serializable types.

### 6.3 Workflow State (conceptual)

* `request`: original user ask
* `files`: descriptors for uploaded inputs
* `execution_path`: ordered list of agent names
* `current_data`: the data passed to the next node
* `results`: map of agent → output envelope
* `errors`: list of {agent, message}
* `started_at/completed_at`: timestamps

---

## 7) Registries (Schemas)

### 7.1 agents.json (logical schema)

```json
{
  "<agent_name>": {
    "description": "what it does",
    "uses_tools": ["tool_a", "tool_b"],
    "input_schema": { /* JSON schema-ish */ },
    "output_schema": { /* JSON schema-ish */ },
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

### 7.2 tools.json (logical schema)

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

**Scope now:** Jira‑only helper (read/parse/query).
**Non‑goals now:** GitHub, ServiceNow, etc. If requested, the Orchestrator triggers generation of a new adapter/agent.

**Inputs:** project key, filters (assignee, status, date range), fields
**Output:** standard envelope with a normalized JSON array of tickets
**Tools:** `jira_client` (connector), `field_normalizer` (pure local tool)
**Notes:** no workflow smarts; no side effects beyond declared Jira calls.

---

## 9) Security, Safety, and Governance

* **Sandbox codegen:** execute generated code in a restricted environment.
* **Allow‑list imports:** only standard libs + approved SDKs.
* **Secret handling:** explicit credential objects; never read env vars implicitly.
* **Network egress:** only via declared connectors; block raw sockets for tools.
* **Review gates:** automated tests + lightweight human review for new connectors.

---

## 10) Observability & Ops

* **Run logs:** per agent start/stop, inputs (redacted), sizes, durations.
* **Metrics:** execution counts, p50/p95 latency per agent, codegen success rate, registry growth.
* **Tracing:** workflow graph with node/edge timings.
* **Cost:** token and API call accounting per run.

---

## 11) Versioning & Change Management

* **Semver:** bump minor for non‑breaking enhancements; major for breaking schema changes.
* **Immutability:** keep old versions in registry until workflows migrate.
* **Deprecation:** mark old entries; Orchestrator prefers latest non‑deprecated.

---

## 12) Roadmap

**P0 (this week):**

* Stand up registries; implement minimal readers + one connector (Jira).
* Implement factories with basic validation; generate 3–5 tiny tools + 3 tiny agents.
* Orchestrate one end‑to‑end demo workflow in LangGraph.

**P1:**

* Harden validation (purity checks, allow‑list, unit tests).
* Add visualization, metrics, and a simple UI for registry browsing and run history.
* Add on‑demand connector generation path (e.g., GitHub) behind a review gate.

**P2:**

* Policy‑driven governance (who can approve new connectors).
* Caching and memoization for heavy tools.
* Multi‑tenant credentials and role‑based data access.

---

## 13) Risks & Mitigations

* **Risk:** LLM over‑generates complex code.
  **Mitigation:** strict size/time budgets; factories reject oversized outputs.
* **Risk:** Silent side effects in generated tools.
  **Mitigation:** purity tests; deny network/disk unless declared connector.
* **Risk:** Registry drift and dead entries.
  **Mitigation:** usage tracking; prune unused entries on schedule.
* **Risk:** Vendor lock‑in at connector layer.
  **Mitigation:** narrow adapter interfaces; test harnesses per vendor.

---

## 14) Success Criteria

* 80%+ of new capabilities added via **generated** tools/agents under size limits.
* Median time to add a new utility/tool: **< 5 minutes** including validation.
* Stable P95 workflow latency for a 5‑node graph: **< 20 seconds**.
* Zero policy violations (no undeclared network I/O) in CI over 30 days.

---

## 15) Appendix: Sample Registry Entries

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

### TL;DR

* Keep **agents tiny** and **tools pure**.
* Use **registries** to declare capabilities.
* Let the **Orchestrator** plan and **LangGraph** execute.
* Start with **Jira‑only ticketing**, grow on demand via codegen.

## Implementation Plan — Detailed Steps (1–20)

> Keep this section intact as your actionable, step‑by‑step checklist. It complements (not replaces) the Roadmap.

### Phase 1: Foundation & Cleanup (Steps 1–5)

**Step 1 — Backup and Restructure**

* Snapshot the current repo to `Agent_Fabric_backup_complex/`.
* Preserve `.env`, `venv/`, `.git/`.
* Create the lean structure:

  ```
  Agent_Fabric/
  ├── generated/
  │   ├── agents/           # LLM‑generated agents (tiny, single‑purpose)
  │   └── tools/            # LLM‑generated pure tools
  ├── core/
  │   ├── orchestrator.py   # Orchestrates workflows (LLM planning)
  │   ├── agent_factory.py  # Agent codegen + validation + registration
  │   ├── tool_factory.py   # Tool codegen + validation + registration
  │   ├── workflow_engine.py# LangGraph execution + state
  │   └── registry.py       # Read/write agents.json & tools.json
  ├── agents.json           # Agent registry (capabilities)
  ├── tools.json            # Tool registry (utilities)
  ├── config.py             # Keys, model choices, size budgets
  └── app.py                # (Optional) Streamlit UI for demos
  ```

**Step 2 — Configuration Setup**

* Add model IDs, API keys, and **size budgets**: agents (50–300 LOC), tools (20–100 LOC).
* Turn on LangGraph settings (retries, timeouts).
* Enable import allow‑list and network policy (connectors only).

**Step 3 — Dual Registry Design**

* Define minimal JSON schemas:

  * `agents.json`: description, `uses_tools`, input/output schemas, location, created\_by/at, version, usage metrics.
  * `tools.json`: description, `signature`, location, `is_pure_function`, used\_by, created\_by/at.
* Implement `core/registry.py` helpers: load/save, search, dependency map, pruning markers.

**Step 4 — Minimal Pre‑built Components**

* Readers: `read_pdf`, `read_csv`, `read_json`, `read_text` (thin wrappers only).
* One connector to start (e.g., **Jira**). Others are generated on demand.
* Auth helpers are explicit, scoped, and testable.

**Step 5 — Seed Templates**

* `example_tool.py`: shows a pure function (args → return).
* `example_agent.py`: shows agent envelope & calling a tool.
* Store short, commented templates to guide LLM codegen prompts.

---

### Phase 2: Core Engine (Steps 6–10)

**Step 6 — Tool Factory Implementation**

* Prompt engineering for pure, stateless utilities with explicit signatures.
* Static checks: imports allow‑list, no filesystem, no sockets unless connector.
* Unit tests: sample I/O; purity checks (same input → same output).
* On success: write to `generated/tools/…`, update `tools.json`.

**Step 7 — Agent Factory Implementation**

* Given an intent and required tools, ask LLM to produce a small agent that **only**:

  * Validates inputs per schema.
  * Imports approved tools.
  * Returns the standard JSON **envelope** (`status/data/metadata`).
* Tests: schema conformance, happy‑path I/O, error path.
* On success: write to `generated/agents/…`, update `agents.json`.

**Step 8 — LangGraph Workflow Engine**

* Build StateGraph with: `request`, `files`, `execution_path`, `current_data`, `results`, `errors`.
* Add retries/backoff, error edges, and timing capture per node.
* Provide a visualization hook (graph JSON) for the UI.

**Step 9 — Orchestrator (LLM Planning)**

* Parse the user ask → capability lookup in registries.
* If missing, trigger Tool/Agent Factory in the **smallest** increments.
* Assemble the workflow (nodes = agents; edges = data handoff).
* Execute via LangGraph, then synthesize the final output.

**Step 10 — Registry Management**

* Track agent→tool dependencies, execution counts, avg latency.
* Provide pruning for unused/generated‑but‑never‑called entries.
* Support versioning and deprecation flags.

---

### Phase 3: Dynamic Creation Testing (Steps 11–15)

**Step 11 — Create 10 Test Agents**

1. `extract_urls` (may create `url_regex` tool)
2. `create_simple_chart` (may create `matplotlib_wrapper`)
3. `fetch_webpage` (may create `http_client`)
4. `parse_json` (standalone)
5. `format_table` (may create `table_formatter`)
6. `calculate_stats` (may create `stats_calculator`)
7. `detect_language` (may create `language_detector`)
8. `extract_dates` (may create `date_parser`)
9. `jira_fetch` (may create `jira_client`)
10. `send_slack` (may create `slack_client`)

**Step 12 — Complex Workflow Testing**

* PDF → Extract text → Extract URLs → Fetch pages → Summarize.
* CSV → Calculate stats → Create chart → Format report.
* Text → Detect language → Extract dates → Translate → Format.

**Step 13 — Streamlit Interface (Optional but useful)**

* Browse registries; upload inputs; preview planned workflow; run and view results.
* Show real‑time node execution and timings.

**Step 14 — LangGraph Visualization**

* Render nodes/edges, color by status; tooltips for timings and data size previews.

**Step 15 — Demo Scenarios**

* Dynamic creation (capability missing → codegen → run).
* Tool reuse across multiple agents.
* 5+ node workflow with retries.
* Failure handling demo.
* Latency comparison vs monolithic.

---

### Phase 4: Testing & Documentation (Steps 16–20)

**Step 16 — Comprehensive Testing**

* 20 tools + 20 agents: creation, validation, registry linking, deprecation flow.
* Connector tests with mock servers for Jira.
* Negative tests: blocked imports, network without connector, schema mismatch.

**Step 17 — Documentation**

* Architecture, registries, factories, LangGraph patterns.
* Codegen prompts (do/don’t), size budgets, purity rules.
* Deployment guide and security policy.

**Step 18 — Example Library**

* Common tool patterns (regex/date/normalization).
* Common agent patterns (extract/transform/format).
* Workflow templates (PDF→URLs→fetch→summarize, CSV→stats→chart→report).

**Step 19 — Monitoring Dashboard**

* Usage stats per agent/tool, codegen success rates, workflow p50/p95, cost tracking.
