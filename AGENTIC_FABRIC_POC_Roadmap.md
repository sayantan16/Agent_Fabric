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
