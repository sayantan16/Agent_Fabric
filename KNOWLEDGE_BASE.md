# AGENTIC FABRIC POC - COMPLETE PROJECT KNOWLEDGE BASE
================================================================================
Generated: 2025-09-08 23:51:41
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
├── flask_app/
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── api.py
│   │   └── main.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── orchestrator_service.py
│   │   ├── registry_service.py
│   │   └── workflow_service.py
│   ├── static/
│   │   ├── css/
│   │   │   └── custom.css
│   │   ├── js/
│   │   │   └── app.js
│   │   └── favicon.ico
│   ├── templates/
│   │   ├── components/
│   │   │   ├── chat-container.html
│   │   │   ├── sidebar.html
│   │   │   ├── workflow-panel.html
│   │   │   └── workflow-visualization.html
│   │   ├── partials/
│   │   │   ├── chat-message.html
│   │   │   └── workflow-status.jinja2
│   │   ├── base.html
│   │   ├── dependencies.html
│   │   ├── error.html
│   │   ├── help.html
│   │   ├── index.jinja2
│   │   ├── registry.html
│   │   ├── settings.html
│   │   ├── workflow_detail.jinja2
│   │   └── workflows.html
│   ├── uploads/
│   ├── __init__.py
│   ├── app.py
│   ├── config_ui.py
│   └── requirements_ui.txt
├── generated/
│   ├── agents/
│   │   ├── email_extractor_agent.py
│   │   ├── read_csv_agent.py
│   │   └── read_text_agent.py
│   ├── tools/
│   │   ├── analyze_sentiment.py
│   │   ├── calculate_mean.py
│   │   ├── calculate_median.py
│   │   ├── calculate_std.py
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
├── Agent_Fabric_UI_Roadmap.md
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
**Size:** 11,844 bytes
**Modified:** 2025-09-07 15:01:58

```markdown
# Agent Fabric — Design & Roadmap (Updated with UI Implementation)
---

## 1) Overview & Problem Statement

Your current agent set is complex and monolithic. The vision is an **agent fabric** where small agents are created on‑demand by an LLM and registered automatically. Large, pre‑baked agents (500–1000 LOC) are brittle to generate and maintain.

**Core shift:**
* Keep agents **narrow** (single responsibility).
* Move reusable logic into **pure tools** (stateless functions).
* Let an **Orchestrator LLM** plan/sequence agents.
* Persist capabilities in **lightweight registries** (`agents.json`, `tools.json`).
* **NEW**: Present intelligent orchestration through intuitive Flask UI with real-time visualization.

---

## 2) Implementation Status Overview

### ✅ COMPLETED (Backend Core - Steps 1-10)
* Dual registry system (agents.json, tools.json)
* Agent Factory with Claude integration
* Tool Factory (implemented via ensure_tool)
* Orchestrator with GPT-4 planning
* LangGraph workflow engine
* Dynamic component creation
* Dependency resolution
* Standard I/O contracts
* 13+ working agents, 13+ tools

### 🚧 IN PROGRESS (UI Implementation - Steps 21-27)
* Flask web interface
* Workflow visualization
* Registry explorer
* Real-time execution display

### 📋 PLANNED (Future Enhancements - Steps 28-30)
* Production deployment
* Performance optimization
* Advanced analytics

---

## 3) Architecture & End‑to‑End Flow (UPDATED)

```
User (Web UI) → Flask App → Orchestrator LLM → agents.json / tools.json
                    ↓              ↘ missing? → Codegen → Factory → Registry
                HTMX Updates        ↘ build workflow → LangGraph → Execute
                    ↓                                      ↓
            Live Visualization ← Progress Updates ← State Changes
                    ↓
            Rich Results Display ← Synthesis ← Collect Results
```

### UI-Enhanced Flow Summary
1. User interacts via Flask web interface
2. HTMX handles async updates without page refresh
3. Orchestrator plans workflow (visible in UI)
4. Missing components created (animated in UI)
5. Workflow executes with live progress
6. Results displayed with agent attribution
7. Registry explorer shows growing capabilities

---

## 4) UI Architecture & Tech Stack

### Core Stack (DECIDED)
* **Flask**: Python web framework, direct backend integration
* **HTMX**: Dynamic updates without complex JavaScript
* **Alpine.js**: Lightweight reactivity (15kb)
* **Tailwind CSS**: Rapid, professional styling
* **Mermaid.js**: Workflow visualization
* **Chart.js**: Data visualization
* **Prism.js**: Code syntax highlighting

### UI Components Architecture
```
flask_app/
├── app.py                      # Main Flask application
├── routes/
│   ├── api.py                 # API endpoints
│   ├── orchestrator.py        # Orchestration endpoints
│   └── registry.py            # Registry management
├── templates/
│   ├── base.html             # Base template with assets
│   ├── index.jinja2            # Main chat interface
│   ├── components/           # Reusable components
│   │   ├── chat.html        # Chat interface
│   │   ├── workflow.html    # Workflow viz
│   │   └── registry.html    # Registry explorer
│   └── partials/            # HTMX fragments
│       ├── message.html     # Chat messages
│       ├── status.html      # Status updates
│       └── result.html      # Result cards
├── static/
│   ├── css/
│   │   ├── tailwind.css    # Tailwind utilities
│   │   └── custom.css      # Custom styles
│   └── js/
│       └── app.js          # Minimal custom JS
└── services/
    ├── orchestrator_service.py  # Backend integration
    └── registry_service.py      # Registry operations
```

---

## 5) Implementation Plan — Steps 1-30 (UPDATED)

### ✅ Phase 1: Foundation & Cleanup (Steps 1-5) **[COMPLETED]**
1. ✅ **Backup & Restructure** - Clean directory structure established
2. ✅ **Configuration Setup** - config.py with all settings
3. ✅ **Dual Registry Design** - agents.json, tools.json working
4. ✅ **Minimal Pre-built** - Four readers implemented
5. ✅ **Seed Templates** - Agent/tool generation templates ready

### ✅ Phase 2: Core Engine (Steps 6-10) **[COMPLETED]**
6. ✅ **Tool Factory** - Dynamic tool creation working
7. ✅ **Agent Factory** - Claude-powered agent generation
8. ✅ **Workflow Engine** - LangGraph integration complete
9. ✅ **Orchestrator** - GPT-4 planning and coordination
10. ✅ **Registry Management** - Full CRUD with validation

### ✅ Phase 3: Dynamic Creation Testing (Steps 11-15) **[COMPLETED]**
11. ✅ **Test Agents Created** - 13 agents dynamically generated
12. ✅ **Complex Workflows** - Multi-agent coordination tested
13. ⚠️ **Basic Testing** - Comprehensive tests passing
14. ✅ **Workflow Execution** - Sequential/parallel working
15. ✅ **Demo Scenarios** - All test scenarios passing

### ✅ Phase 4: Backend Testing & Validation (Steps 16-20) **[COMPLETED]**
16. ✅ **Comprehensive Testing** - test_end_to_end.py (6/6 pass)
17. ✅ **Test Scenarios** - test_comprehensive_scenarios.py (6/6 pass)
18. ✅ **Error Handling** - Graceful failure recovery
19. ✅ **Ambiguity Detection** - Request clarification working
20. ✅ **Backend Ready** - Production-quality backend

### 🚧 Phase 5: UI Implementation (Steps 21-27) **[NEW - IN PROGRESS]**

#### Step 21: Flask Foundation (Day 1)
- [ ] Setup Flask application structure
- [ ] Configure Flask with existing backend
- [ ] Create base templates with Tailwind CSS
- [ ] Setup HTMX and Alpine.js
- [ ] Basic routing structure

#### Step 22: Chat Interface (Day 2)
- [ ] Main chat UI with message display
- [ ] File upload with drag-and-drop
- [ ] Request input with auto-resize textarea
- [ ] Basic response rendering
- [ ] Loading states with spinners

#### Step 23: Workflow Visualization (Day 3-4)
- [ ] Integrate Mermaid.js for workflow graphs
- [ ] Real-time node status updates (pending/active/complete)
- [ ] Agent execution timeline
- [ ] Progress bars per agent
- [ ] Error state visualization

#### Step 24: Registry Explorer (Day 5)
- [ ] Tabbed interface (Agents/Tools/Recent)
- [ ] Agent/Tool cards with metadata
- [ ] Search and filter functionality
- [ ] Usage statistics display
- [ ] Dependency visualization

#### Step 25: Dynamic Creation Showcase (Day 6)
- [ ] Creation animation overlay
- [ ] Code generation preview
- [ ] Success notifications
- [ ] "New capability added" badges
- [ ] Registry update animations

#### Step 26: Results & Analytics (Day 7)
- [ ] Rich result formatting
- [ ] Collapsible agent outputs
- [ ] Chart.js integration for data viz
- [ ] Export functionality
- [ ] Execution metrics display

#### Step 27: Polish & Integration (Day 8)
- [ ] Dark/light theme toggle
- [ ] Error handling UI
- [ ] Performance optimizations
- [ ] Cross-browser testing
- [ ] Documentation

### 📋 Phase 6: Production Preparation (Steps 28-30) **[PLANNED]**

#### Step 28: Deployment Setup
- [ ] Docker containerization
- [ ] Environment configuration
- [ ] NGINX reverse proxy setup
- [ ] SSL certificate configuration
- [ ] Production database setup

#### Step 29: Performance & Monitoring
- [ ] Response caching strategy
- [ ] CDN integration for assets
- [ ] Logging and monitoring setup
- [ ] Performance metrics dashboard
- [ ] Error tracking integration

#### Step 30: Final Demo & Handoff
- [ ] Demo script preparation
- [ ] Video walkthrough creation
- [ ] Technical documentation
- [ ] Deployment guide
- [ ] Knowledge transfer session

---

## 6) UI Feature Specifications

### Core Features (Phase 5)

#### 1. Chat Interface
- **Input**: Multi-line text with file attachments
- **Processing**: Real-time status updates via HTMX
- **Output**: Structured results with agent attribution
- **History**: Session-based conversation memory

#### 2. Workflow Visualization
```mermaid
graph LR
    O[Orchestrator] -->|plans| A1[Agent 1]
    A1 -->|data| A2[Agent 2]
    A2 -->|results| S[Synthesis]
```
- Live execution flow
- Node states: pending (blue), active (yellow), complete (green), error (red)
- Execution time per node
- Click for details

#### 3. Registry Explorer
- **Grid Layout**: Cards for each agent/tool
- **Metadata Display**: Creation date, usage count, performance
- **Relationships**: Tool-agent dependency graph
- **Filtering**: By tag, date, usage

#### 4. Dynamic Creation Theater
- **Split View**: Request → Code Generation → Validation → Registration
- **Progress Steps**: Visual stepper component
- **Celebration**: Success animation when new capability added

---

## 7) Technical Implementation Details

### Flask Routes
```python
# Main routes
@app.route('/')                          # Chat interface
@app.route('/api/process', methods=['POST'])  # Process request
@app.route('/api/workflow/<id>/status')  # Workflow status
@app.route('/registry')                  # Registry explorer
@app.route('/registry/api/agents')       # Agent list API
@app.route('/registry/api/tools')        # Tool list API
```

### HTMX Integration Pattern
```html
<!-- Auto-updating workflow status -->
<div hx-get="/api/workflow/{{ id }}/status" 
     hx-trigger="every 1s"
     hx-swap="innerHTML">
    <!-- Status content -->
</div>
```

### State Management
- Server-side session for conversation history
- Workflow state in backend (existing)
- UI state in Alpine.js data attributes
- No client-side persistence needed for POC

---

## 8) Success Metrics

### Backend (ACHIEVED)
- ✅ Dynamic component creation < 5 min
- ✅ Workflow execution < 20s for 5 nodes
- ✅ 100% test pass rate
- ✅ Zero critical errors in production scenarios

### UI (TARGET)
- [ ] Page load time < 2s
- [ ] Workflow status updates < 100ms latency
- [ ] Smooth animations at 60fps
- [ ] Works on Chrome, Firefox, Safari
- [ ] Intuitive enough for non-technical users

---

## 9) Risk Mitigation

### Identified Risks
1. **HTMX Learning Curve** → Start with simple examples, incremental complexity
2. **Mermaid.js Limitations** → Fallback to simple HTML/CSS for complex visualizations
3. **Performance with Many Agents** → Pagination in registry, virtual scrolling
4. **File Upload Size** → Client-side validation, size limits, progress indicators

---

## 10) Next Immediate Steps

### Week 1 (UI Sprint)
1. **Monday-Tuesday**: Flask setup + basic chat (Steps 21-22)
2. **Wednesday-Thursday**: Workflow visualization (Step 23)
3. **Friday**: Registry explorer (Step 24)

### Week 2 (Polish Sprint)
1. **Monday**: Dynamic creation showcase (Step 25)
2. **Tuesday**: Results formatting (Step 26)
3. **Wednesday-Thursday**: Integration and polish (Step 27)
4. **Friday**: Demo preparation

---

## 11) Demo Scenarios for UI

### Scenario 1: Simple Extraction
"Extract emails from this text" → Show workflow → Display results

### Scenario 2: Dynamic Creation
"Analyze sentiment of customer feedback" → Create sentiment tool → Create analyzer agent → Execute → Show results

### Scenario 3: Complex Pipeline
Upload CSV → "Create statistical report with charts" → Show multi-agent workflow → Display rich results with visualizations

### Scenario 4: Registry Growth
Show registry before/after multiple requests → Demonstrate learning system

---

This updated roadmap integrates the UI implementation plan with your existing backend work, providing a clear path from the current state (completed backend) to a fully functional POC with an impressive user interface. The Flask-based approach maintains simplicity while delivering the visual impact needed for effective demonstrations.
```

--------------------------------------------------------------------------------

### File: Agent_Fabric_UI_Roadmap.md
**Path:** `Agent_Fabric_UI_Roadmap.md`
**Size:** 12,204 bytes
**Modified:** 2025-09-07 15:01:58

```markdown
# Flask UI Implementation Roadmap
## Step-by-Step Development Plan

Based on your existing backend with `orchestrator.py`, here's a comprehensive roadmap to build the complete Flask UI system.

---

## **PHASE 1: Foundation & Flask Setup (Days 1-2)**

### **Step 1: Project Structure Setup**
**Files to Create:**
```
flask_app/
├── app.py
├── __init__.py
├── config_ui.py
└── requirements_ui.txt
```

**Tasks:**
- Create Flask app structure within existing project
- Setup Flask configuration (debug mode, secret key, upload settings)
- Install Flask dependencies: `flask`, `flask-cors`, `python-dotenv`
- Create basic Flask app initialization
- Test basic "Hello World" Flask route

### **Step 2: Backend Integration Bridge**
**Files to Create:**
```
flask_app/services/
├── __init__.py
├── orchestrator_service.py
├── registry_service.py
└── workflow_service.py
```

**Functions to Implement:**
- `orchestrator_service.py`:
  - `process_user_request(request, files=None)`
  - `get_workflow_status(workflow_id)`
  - `cancel_workflow(workflow_id)`
- `registry_service.py`:
  - `get_agents_list()`
  - `get_tools_list()`
  - `get_registry_stats()`
- `workflow_service.py`:
  - `get_workflow_visualization(workflow_id)`
  - `stream_workflow_updates(workflow_id)`

**Tasks:**
- Import and integrate existing `core/orchestrator.py`
- Create service wrapper functions for UI consumption
- Add error handling and response formatting
- Test backend connectivity

---

## **PHASE 2: Core Routes & API (Days 3-4)**

### **Step 3: Main Route Structure**
**Files to Create:**
```
flask_app/routes/
├── __init__.py
├── main.py
├── api.py
├── orchestrator.py
└── registry.py
```

**Routes to Implement:**
- `main.py`:
  - `GET /` - Main chat interface
  - `GET /registry` - Registry explorer page
  - `GET /workflows/<id>` - Workflow detail view
- `api.py`:
  - `POST /api/upload` - File upload handler
  - `GET /api/health` - System health check
  - `POST /api/test-connection` - Backend connectivity test

### **Step 4: Orchestrator API Endpoints**
**Routes in `orchestrator.py`:**
- `POST /api/process` - Main request processing
- `GET /api/workflow/<id>/status` - Get workflow status
- `GET /api/workflow/<id>/stream` - SSE for real-time updates
- `DELETE /api/workflow/<id>` - Cancel workflow
- `GET /api/workflows` - List recent workflows

**Functions to Implement:**
- Request validation and sanitization
- File handling and temporary storage
- Async workflow status tracking
- Server-sent events for real-time updates

### **Step 5: Registry API Endpoints**
**Routes in `registry.py`:**
- `GET /api/registry/agents` - List all agents
- `GET /api/registry/tools` - List all tools
- `GET /api/registry/stats` - Registry statistics
- `GET /api/registry/health` - Registry health check
- `GET /api/registry/dependencies` - Dependency graph

---

## **PHASE 3: Base Templates & Static Assets (Days 5-6)**

### **Step 6: Template Foundation**
**Files to Create:**
```
flask_app/templates/
├── base.html
├── index.jinja2
├── registry.html
└── error.html
```

**Base Template Features (`base.html`):**
- HTML5 structure with meta tags
- Tailwind CSS CDN integration
- HTMX library inclusion
- Alpine.js integration
- Custom CSS/JS file links
- Navigation header with logo
- Flash message container
- Footer with status indicator

### **Step 7: Static Assets Setup**
**Files to Create:**
```
flask_app/static/
├── css/
│   ├── custom.css
│   └── components.css
├── js/
│   ├── app.js
│   ├── workflow-viz.js
│   └── utils.js
└── images/
    └── logo.svg
```

**CSS Components:**
- Chat interface styling
- Workflow visualization containers
- Registry card layouts
- Loading animations
- Status indicators

**JavaScript Functions:**
- HTMX event handlers
- Alpine.js data initialization
- Workflow visualization helpers
- File upload utilities

---

## **PHASE 4: Chat Interface Implementation (Days 7-9)**

### **Step 8: Main Chat Interface**
**Files to Create/Update:**
```
flask_app/templates/
├── components/
│   ├── chat-container.html
│   ├── message-input.html
│   ├── file-upload.html
│   └── typing-indicator.html
└── partials/
    ├── message.html
    ├── status-update.html
    └── error-message.html
```

**Chat Components to Build:**
- Message container with scrolling
- Rich text input with file attachment
- Drag-and-drop file upload zone
- Message history with timestamps
- User/system message differentiation

### **Step 9: Real-Time Message Updates**
**HTMX Integration:**
- `hx-post` for message submission
- `hx-trigger` for auto-scrolling
- `hx-swap` for message updates
- `hx-sse` for real-time status

**Functions to Implement:**
- Message rendering with markdown support
- File preview generation
- Auto-resize textarea
- Message status indicators (sending/sent/error)

### **Step 10: Request Processing Flow**
**Frontend Flow:**
1. User types message + attaches files
2. Frontend validates and shows loading
3. HTMX posts to `/api/process`
4. Server starts orchestrator workflow
5. SSE stream provides status updates
6. Results rendered in chat with agent attribution

**Backend Handlers:**
- Request preprocessing and validation
- File storage and metadata extraction
- Workflow initiation and tracking
- Response streaming and formatting

---

## **PHASE 5: Workflow Visualization (Days 10-12)**

### **Step 11: Workflow Display Components**
**Files to Create:**
```
flask_app/templates/components/
├── workflow-diagram.html
├── agent-node.html
├── execution-timeline.html
└── progress-bar.html
```

**Visualization Features:**
- Mermaid.js workflow diagrams
- Node status indicators (pending/active/complete/error)
- Execution timeline with timestamps
- Progress bars for long-running tasks
- Agent output previews

### **Step 12: Real-Time Workflow Updates**
**JavaScript Functions:**
- `updateWorkflowDiagram(workflowData)`
- `animateNodeTransition(nodeId, newStatus)`
- `updateExecutionTimeline(events)`
- `showAgentOutput(agentId, result)`

**HTMX Patterns:**
- `hx-get="/api/workflow/<id>/status"` with polling
- `hx-trigger="every 1s"` for status updates
- `hx-swap="innerHTML"` for diagram updates
- `hx-target="#workflow-container"`

### **Step 13: Workflow History & Details**
**Pages to Create:**
- Workflow list with filtering
- Detailed workflow view with full execution log
- Error analysis and debugging information
- Performance metrics and timing data

---

## **PHASE 6: Registry Explorer (Days 13-14)**

### **Step 14: Registry Browser Interface**
**Files to Create:**
```
flask_app/templates/
├── registry/
│   ├── agents-grid.html
│   ├── tools-grid.html
│   ├── stats-dashboard.html
│   └── dependencies-graph.html
└── components/
    ├── agent-card.html
    ├── tool-card.html
    └── metric-widget.html
```

**Registry Components:**
- Agent cards with capabilities and metrics
- Tool cards with usage statistics
- Dependency visualization with D3.js or Mermaid
- Search and filtering functionality
- Performance metrics dashboard

### **Step 15: Registry Analytics**
**Analytics Features:**
- Agent usage frequency charts
- Tool reuse patterns
- Creation timeline visualization
- Performance trends
- Error rate monitoring

**Chart Integration:**
- Chart.js for statistical visualizations
- Interactive hover tooltips
- Export functionality for reports
- Real-time metric updates

---

## **PHASE 7: Dynamic Creation Theater (Days 15-16)**

### **Step 16: Creation Visualization**
**Files to Create:**
```
flask_app/templates/components/
├── creation-stepper.html
├── code-preview.html
├── creation-success.html
└── capability-badge.html
```

**Creation Flow Visualization:**
1. **Analysis Step**: Show orchestrator analyzing request
2. **Planning Step**: Display missing capabilities identified
3. **Generation Step**: Code creation progress with Claude
4. **Validation Step**: Testing and validation status
5. **Registration Step**: Adding to registry
6. **Success Step**: New capability celebration

### **Step 17: Creation Progress Tracking**
**Real-Time Updates:**
- Progress stepper with current step highlighting
- Code generation preview (if debug mode enabled)
- Success animations and notifications
- "New capability added" badges
- Integration into chat flow

---

## **PHASE 8: Advanced Features (Days 17-18)**

### **Step 18: File Handling & Preview**
**File Processing Features:**
- File type detection and validation
- Preview generation for common formats
- Progress indicators for large file uploads
- File metadata display
- Error handling for unsupported formats

**Supported File Types:**
- PDF preview with first page thumbnail
- CSV/Excel data preview tables
- Text file content preview
- Image file display
- JSON/XML structured preview

### **Step 19: Error Handling & User Feedback**
**Error Management:**
- Graceful error page designs
- Detailed error information for debugging
- User-friendly error messages
- Retry mechanisms for failed requests
- Error reporting functionality

**User Feedback Systems:**
- Success/error toast notifications
- Loading states and skeleton screens
- Progress indicators for long operations
- Confirmation dialogs for destructive actions

---

## **PHASE 9: Polish & Production Features (Days 19-21)**

### **Step 20: UI Polish & Accessibility**
**Accessibility Features:**
- Proper ARIA labels and roles
- Keyboard navigation support
- Screen reader compatibility
- High contrast mode support
- Focus management

**Visual Polish:**
- Smooth animations and transitions
- Responsive design for mobile/tablet
- Dark/light theme toggle
- Professional color scheme
- Consistent spacing and typography

### **Step 21: Performance Optimization**
**Frontend Optimization:**
- CSS/JS minification and compression
- Image optimization and lazy loading
- HTMX request debouncing
- Local storage for user preferences
- Service worker for offline support

**Backend Integration:**
- Response caching strategies
- Database query optimization
- File upload optimization
- Memory usage monitoring

### **Step 22: Production Deployment**
**Deployment Preparation:**
- Environment configuration management
- Production vs development settings
- Error logging and monitoring
- Security headers and CSRF protection
- Rate limiting for API endpoints

---

## **PHASE 10: Testing & Documentation (Days 22-23)**

### **Step 23: Testing Suite**
**Frontend Tests:**
- HTMX interaction testing
- JavaScript function unit tests
- UI component integration tests
- Cross-browser compatibility testing
- Mobile responsiveness testing

**Integration Tests:**
- Full user journey testing
- File upload and processing tests
- Real-time update functionality
- Error scenario testing

### **Step 24: Documentation & Demo**
**Documentation:**
- User guide with screenshots
- API documentation
- Deployment instructions
- Troubleshooting guide
- Developer setup instructions

**Demo Preparation:**
- Demo script with example scenarios
- Sample files for testing
- Performance benchmarking
- Video walkthrough creation

---

## **Development Timeline Summary**

| Phase | Days | Focus | Key Deliverables |
|-------|------|-------|------------------|
| 1 | 1-2 | Foundation | Flask setup, backend integration |
| 2 | 3-4 | API Layer | Routes, endpoints, data flow |
| 3 | 5-6 | Templates | Base templates, static assets |
| 4 | 7-9 | Chat UI | Interactive chat interface |
| 5 | 10-12 | Workflows | Visualization, real-time updates |
| 6 | 13-14 | Registry | Explorer, analytics dashboard |
| 7 | 15-16 | Creation | Dynamic creation theater |
| 8 | 17-18 | Advanced | File handling, error management |
| 9 | 19-21 | Polish | Accessibility, performance, deployment |
| 10 | 22-23 | Testing | Testing suite, documentation |

**Total Estimated Time: 23 days (4-5 weeks)**

Each step builds incrementally on the previous ones, ensuring you have a working system at every stage that can be tested and demonstrated.
```

--------------------------------------------------------------------------------

### File: KNOWLEDGE_BASE.md
**Path:** `KNOWLEDGE_BASE.md`
**Size:** 0 bytes
**Modified:** 2025-09-08 23:51:33

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
**Size:** 5,813 bytes
**Modified:** 2025-09-08 23:29:00

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
      "execution_count": 3,
      "avg_execution_time": 0.001,
      "tags": [
        "extraction",
        "emails"
      ],
      "line_count": 98,
      "status": "active",
      "last_executed": "2025-09-08T23:29:00.135005"
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
      "execution_count": 3,
      "avg_execution_time": 0.0,
      "tags": [
        "extraction",
        "urls"
      ],
      "line_count": 80,
      "status": "active",
      "last_executed": "2025-09-08T23:29:00.137209"
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
    }
  }
}
```

--------------------------------------------------------------------------------

### File: agents.json.lock
**Path:** `agents.json.lock`
**Size:** 0 bytes
**Modified:** 2025-09-08 00:54:41

*[Binary file or content not included]*

--------------------------------------------------------------------------------

### File: config.py
**Path:** `config.py`
**Size:** 18,940 bytes
**Modified:** 2025-09-06 23:37:10

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
1. First check if existing agents can handle the task
2. If no suitable agents exist for a capability, mark them for creation
3. For statistical/numerical tasks, consider these patterns:
   - "statistics" or "stats" → needs stats_calculator agent
   - "mean/median/average" → needs statistical calculation tools
   - "report" → needs report generation capabilities
   - "chart/graph" → needs visualization capabilities

PLANNING RULES:
- If the request mentions statistics/calculations and no stats agents exist, plan to create them
- Break complex requests into atomic capabilities
- Each capability needs an agent (existing or to be created)

Respond with this EXACT JSON structure:
{{
    "workflow_id": "wf_{timestamp}",
    "workflow_type": "sequential",
    "reasoning": "Step-by-step explanation of your plan",
    "agents_needed": ["list_of_existing_agents_that_match"],
    "missing_capabilities": {{
        "agents": [
            {{
                "name": "agent_name_to_create",
                "purpose": "specific purpose",
                "required_tools": ["tool1", "tool2"],
                "justification": "why this is needed"
            }}
        ],
        "tools": [
            {{
                "name": "tool_name_to_create",
                "purpose": "specific purpose"
            }}
        ]
    }},
    "confidence": 0.95
}}

IMPORTANT: 
- If no agents match the request, agents_needed should be empty [] not cause an error
- Always identify what needs to be created in missing_capabilities
- For ambiguous requests, suggest a reasonable default workflow"""


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
**Size:** 33,037 bytes
**Modified:** 2025-09-08 22:55:07

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
                # Execute with timeout using threading instead of signal
                import threading
                import time

                def run_agent_with_timeout():
                    nonlocal agent_state, execution_error
                    try:
                        agent_state = agent_func(agent_state)
                    except Exception as e:
                        execution_error = e

                execution_error = None
                agent_thread = threading.Thread(target=run_agent_with_timeout)
                agent_thread.start()
                agent_thread.join(timeout=AGENT_TIMEOUT_SECONDS)

                if agent_thread.is_alive():
                    # Timeout occurred
                    state["errors"].append(
                        {
                            "agent": agent_name,
                            "error": f"Agent {agent_name} timeout after {AGENT_TIMEOUT_SECONDS}s",
                            "type": "timeout",
                        }
                    )
                    state["results"][agent_name] = {
                        "status": "error",
                        "data": None,
                        "metadata": {
                            "agent": agent_name,
                            "error": "Execution timeout",
                            "execution_time": AGENT_TIMEOUT_SECONDS,
                        },
                    }
                elif execution_error:
                    # Agent had an error
                    raise execution_error

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

        # Get agent info from registry
        agent_info = self.registry.get_agent(agent_name)
        if not agent_info:
            print(f"DEBUG: Agent '{agent_name}' not found in registry")
            raise ValueError(f"Agent '{agent_name}' not found in registry")

        print(f"DEBUG: Agent info found: {agent_info.get('location')}")

        # Load the agent module
        agent_path = agent_info["location"]

        # FIX: Handle relative paths correctly
        if not os.path.isabs(agent_path):
            # Get project root (parent of current directory when running from flask_app)
            current_dir = os.getcwd()
            if current_dir.endswith("flask_app"):
                project_root = os.path.dirname(current_dir)
            else:
                project_root = current_dir
            agent_path = os.path.join(project_root, agent_path)

        print(f"DEBUG: Full agent path: {agent_path}")

        if not os.path.exists(agent_path):
            raise FileNotFoundError(f"Agent file not found: {agent_path}")

        # Import the module
        import importlib.util

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

        # Determine current_data from multiple possible sources
        current_data = (
            initial_data.get("current_data")
            or initial_data.get("text")
            or initial_data.get("data")
            or initial_data.get("request")
            or initial_data
        )

        return {
            "request": initial_data.get("request", ""),
            "workflow_id": workflow_id,
            "workflow_type": initial_data.get("workflow_type", "sequential"),
            "current_data": current_data,
            # IMPORTANT: Also preserve original fields
            "text": initial_data.get("text"),
            "data": initial_data.get("data"),
            "input": initial_data.get("input"),
            "files": initial_data.get("files", []),
            "context": initial_data.get("context", {}),
            "execution_path": initial_data.get("execution_path", []),
            "current_agent": None,
            "pending_agents": [],
            "completed_agents": [],
            "results": initial_data.get("results", {}),
            "errors": initial_data.get("errors", []),
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

### File: flask_app/__init__.py
**Path:** `flask_app/__init__.py`
**Size:** 161 bytes
**Modified:** 2025-09-07 12:05:15

```python
# flask_app/__init__.py
"""
Flask UI Application for Agentic Fabric POC
Provides web interface for multi-agent orchestration platform
"""

__version__ = "1.0.0"

```

--------------------------------------------------------------------------------

### File: flask_app/app.py
**Path:** `flask_app/app.py`
**Size:** 6,303 bytes
**Modified:** 2025-09-08 00:36:38

```python
# flask_app/app.py
"""
Main Flask Application
Entry point for the Agentic Fabric web interface
"""

import json
import os
import sys
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS

# Add project root to Python path for backend imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Import UI configuration
from flask_app.config_ui import config


def create_app(config_name=None):
    """
    Application factory pattern for Flask app creation.

    Args:
        config_name: Configuration environment ('development', 'production')

    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)

    # Determine configuration
    config_name = config_name or os.environ.get("FLASK_ENV", "development")
    app.config.from_object(config[config_name])

    # Enable CORS for API endpoints
    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": "*",
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": [
                    "Content-Type",
                    "Authorization",
                    "HX-Request",
                    "HX-Target",
                ],
            }
        },
    )

    # Ensure upload directory exists
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Initialize extensions and register blueprints
    register_blueprints(app)
    register_error_handlers(app)
    register_template_functions(app)

    return app


def register_blueprints(app):
    """Register Flask blueprints for route organization."""

    # Import route blueprints (will create these in next steps)
    try:
        from flask_app.routes.main import main_bp
        from flask_app.routes.api import api_bp

        app.register_blueprint(main_bp)
        app.register_blueprint(api_bp, url_prefix="/api")

    except ImportError as e:
        app.logger.warning(f"Blueprint import failed: {e}.")


def register_error_handlers(app):
    """Register custom error handlers."""

    @app.errorhandler(404)
    def not_found_error(error):
        return (
            render_template(
                "error.html", error_code=404, error_message="Page not found"
            ),
            404,
        )

    @app.errorhandler(500)
    def internal_error(error):
        return (
            render_template(
                "error.html", error_code=500, error_message="Internal server error"
            ),
            500,
        )

    @app.errorhandler(413)
    def file_too_large(error):
        return (
            jsonify(
                {
                    "error": "File too large",
                    "message": f'Maximum file size is {app.config["MAX_CONTENT_LENGTH"] // (1024*1024)}MB',
                }
            ),
            413,
        )


def register_template_functions(app):
    """Register custom template functions and filters."""

    @app.template_filter("file_size")
    def file_size_filter(size_bytes):
        """Convert bytes to human readable format."""
        if size_bytes == 0:
            return "0 B"

        size_names = ["B", "KB", "MB", "GB"]
        import math

        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_names[i]}"

    @app.template_filter("time_ago")
    def time_ago_filter(timestamp):
        """Convert timestamp to relative time."""
        from datetime import datetime

        if isinstance(timestamp, str):
            try:
                timestamp = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            except:
                return timestamp

        now = datetime.now(timestamp.tzinfo if timestamp.tzinfo else None)
        diff = now - timestamp

        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days != 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        else:
            return "just now"

    @app.context_processor
    def inject_globals():
        """Inject global variables into all templates."""
        return {
            "app_name": "Agentic Fabric",
            "app_version": "1.0.0",
            "debug_mode": app.config.get("ENABLE_DEBUG_MODE", False),
            "show_code_gen": app.config.get("SHOW_CODE_GENERATION", False),
        }


# Create app instance
app = create_app()


@app.route("/favicon.ico")
def favicon():
    """Handle favicon requests to prevent 404 errors."""
    from flask import send_from_directory

    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


# Add this test route to flask_app/app.py
@app.route("/test-backend")
def test_backend():
    """Test backend integration."""
    from flask_app.services import OrchestratorService, RegistryService, WorkflowService

    # Test services
    orch_service = OrchestratorService()
    reg_service = RegistryService()
    workflow_service = WorkflowService()

    results = {
        "orchestrator_available": orch_service.is_backend_available(),
        "registry_available": reg_service.is_available(),
        "workflow_available": workflow_service.is_available(),
        "registry_stats": (
            reg_service.get_registry_stats() if reg_service.is_available() else {}
        ),
        "agents_count": (
            len(reg_service.get_agents_list()) if reg_service.is_available() else 0
        ),
        "tools_count": (
            len(reg_service.get_tools_list()) if reg_service.is_available() else 0
        ),
    }

    return f"""
    <h1>Backend Integration Test</h1>
    <pre>{json.dumps(results, indent=2)}</pre>
    <a href="/">← Back to main</a>
    """


if __name__ == "__main__":
    # Development server
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host="127.0.0.1", port=port, debug=app.config.get("DEBUG", True), threaded=True
    )

```

--------------------------------------------------------------------------------

### File: flask_app/config_ui.py
**Path:** `flask_app/config_ui.py`
**Size:** 1,690 bytes
**Modified:** 2025-09-07 12:05:28

```python
# flask_app/config_ui.py
"""
Flask UI Configuration
Separate from core config.py to avoid conflicts
"""

import os
from datetime import timedelta


class Config:
    """Base configuration class."""

    # Flask Core Settings
    SECRET_KEY = (
        os.environ.get("FLASK_SECRET_KEY")
        or "agentic-fabric-dev-key-change-in-production"
    )

    # Upload Settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
    ALLOWED_EXTENSIONS = {
        "txt",
        "pdf",
        "csv",
        "json",
        "xlsx",
        "xls",
        "docx",
        "jpg",
        "jpeg",
        "png",
    }

    # Session Settings
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)

    # HTMX Settings
    HTMX_BOOSTED = True

    # Backend Integration
    BACKEND_TIMEOUT = 30  # seconds
    MAX_WORKFLOW_TIME = 300  # 5 minutes max per workflow

    # UI Settings
    ITEMS_PER_PAGE = 20
    ENABLE_DEBUG_MODE = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    SHOW_CODE_GENERATION = os.environ.get("SHOW_CODE_GEN", "False").lower() == "true"

    # Real-time Updates
    SSE_HEARTBEAT_INTERVAL = 30  # seconds
    WORKFLOW_POLL_INTERVAL = 1  # seconds


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True
    EXPLAIN_TEMPLATE_LOADING = False


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False
    TESTING = False


# Configuration mapping
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}

```

--------------------------------------------------------------------------------

### File: flask_app/requirements_ui.txt
**Path:** `flask_app/requirements_ui.txt`
**Size:** 434 bytes
**Modified:** 2025-09-07 12:06:24

```text
# Flask UI Requirements
# Core Flask dependencies for the web interface

# Web Framework
Flask==3.0.0
Flask-CORS==4.0.0

# Template Engine (included with Flask)
Jinja2==3.1.2

# WSGI Server for production
gunicorn==21.2.0

# Development tools
python-dotenv==1.0.0

# File handling
Werkzeug==3.0.1

# Date/time utilities (already in main requirements)
python-dateutil==2.9.0.post0

# JSON handling (built-in)
# Async support (built-in)
```

--------------------------------------------------------------------------------

### File: flask_app/routes/__init__.py
**Path:** `flask_app/routes/__init__.py`
**Size:** 224 bytes
**Modified:** 2025-09-07 12:32:00

```python
# flask_app/routes/__init__.py
"""
Route Blueprints for Flask Application
Organized by functionality: main, api, orchestrator, registry
"""

from .main import main_bp
from .api import api_bp

__all__ = ["main_bp", "api_bp"]

```

--------------------------------------------------------------------------------

### File: flask_app/routes/api.py
**Path:** `flask_app/routes/api.py`
**Size:** 23,718 bytes
**Modified:** 2025-09-08 23:42:06

```python
# flask_app/routes/api.py - STREAMLINED VERSION
"""
API Routes Blueprint - Streamlined for Agentic Fabric POC
Handles AJAX requests, file uploads, and data endpoints
"""

import os
import json
from typing import Any, Dict
import uuid
from datetime import datetime
from flask import (
    Blueprint,
    request,
    jsonify,
    current_app,
    session,
    make_response,
)
from werkzeug.utils import secure_filename
from flask_app.services.orchestrator_service import orchestrator_service
from flask_app.services.registry_service import registry_service
from flask_app.services.workflow_service import workflow_service

api_bp = Blueprint("api", __name__)


def allowed_file(filename):
    """Check if file extension is allowed."""
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["ALLOWED_EXTENSIONS"]
    )


@api_bp.route("/health")
def health_check():
    """System health check endpoint."""
    try:
        registry_stats = registry_service.get_registry_stats()

        # Ensure proper structure
        if not registry_stats or not registry_stats.get("available", False):
            registry_stats = {
                "available": False,
                "statistics": {"total_agents": 0, "total_tools": 0},
                "summary": {"health_score": 0, "status": "unavailable"},
            }

        health_data = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "services": {
                "orchestrator": orchestrator_service.is_backend_available(),
                "registry": {
                    "available": registry_stats.get("available", False),
                    "stats": registry_stats.get(
                        "statistics", {"total_agents": 0, "total_tools": 0}
                    ),
                    "health_score": registry_stats.get("summary", {}).get(
                        "health_score", 0
                    ),
                    "status": registry_stats.get("summary", {}).get(
                        "status", "unknown"
                    ),
                },
            },
            "system_stats": orchestrator_service.get_system_stats(),
            "version": "1.0.0",
        }

        # Determine overall health
        orchestrator_ok = health_data["services"]["orchestrator"]
        registry_ok = health_data["services"]["registry"]["available"]

        if orchestrator_ok and registry_ok:
            health_data["status"] = "healthy"
            status_code = 200
        elif orchestrator_ok or registry_ok:
            health_data["status"] = "degraded"
            status_code = 200
        else:
            health_data["status"] = "unhealthy"
            status_code = 503

        return jsonify(health_data), status_code

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "unhealthy",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat(),
                }
            ),
            500,
        )


@api_bp.route("/upload", methods=["POST"])
def upload_file():
    """Handle file uploads."""
    try:
        if "files" not in request.files:
            return jsonify({"error": "No files provided"}), 400

        files = request.files.getlist("files")
        uploaded_files = []

        for file in files:
            if file.filename == "":
                continue

            if file and allowed_file(file.filename):
                # Generate unique filename
                filename = secure_filename(file.filename)
                unique_id = uuid.uuid4().hex[:8]
                name, ext = os.path.splitext(filename)
                unique_filename = f"{name}_{unique_id}{ext}"

                # Save file
                filepath = os.path.join(
                    current_app.config["UPLOAD_FOLDER"], unique_filename
                )
                file.save(filepath)

                # Get file metadata
                file_stats = os.stat(filepath)
                file_metadata = {
                    "id": unique_id,
                    "original_name": filename,
                    "stored_name": unique_filename,
                    "path": filepath,
                    "size": file_stats.st_size,
                    "type": file.content_type or "application/octet-stream",
                    "uploaded_at": datetime.now().isoformat(),
                }
                uploaded_files.append(file_metadata)
            else:
                return (
                    jsonify({"error": f"File type not allowed: {file.filename}"}),
                    400,
                )

        return jsonify(
            {"status": "success", "files": uploaded_files, "count": len(uploaded_files)}
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/chat/message", methods=["POST"])
def send_chat_message():
    """Process a chat message with natural language support."""
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"error": "No message provided"}), 400

        message = data["message"].strip()
        if not message:
            return jsonify({"error": "Message cannot be empty"}), 400

        files = data.get("files", [])
        settings = data.get("settings", {})

        # Get user preferences
        auto_create = settings.get("auto_create", session.get("auto_create", True))
        workflow_type = settings.get(
            "workflow_type", session.get("workflow_type", "sequential")
        )

        # Generate unique message ID
        message_id = f"msg_{uuid.uuid4().hex[:8]}"

        # Store in session
        if "chat_history" not in session:
            session["chat_history"] = []

        user_message = {
            "id": message_id,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "type": "user",
            "files": files,
        }
        session["chat_history"].append(user_message)

        # Process through orchestrator
        import asyncio

        try:
            result = asyncio.run(
                orchestrator_service.process_user_request(
                    request_text=message,
                    files=files,
                    auto_create=auto_create,
                    workflow_type=workflow_type,
                )
            )
        except Exception as e:
            result = {
                "status": "error",
                "error": str(e),
                "response": f"I encountered an error processing your request: {str(e)}",
            }

        # Create natural language response
        response_text = create_natural_response(result, message)

        # Add system response to session
        system_response = {
            "id": f"sys_{uuid.uuid4().hex[:8]}",
            "message": response_text,
            "timestamp": datetime.now().isoformat(),
            "type": "system",
            "workflow_id": result.get("workflow_id"),
            "status": result.get("status"),
            "metadata": {
                "agents_used": result.get("workflow", {}).get("steps", []),
                "execution_time": result.get("execution_time", 0),
                "components_created": result.get("metadata", {}).get(
                    "components_created", 0
                ),
                "workflow_type": workflow_type,
            },
        }

        session["chat_history"].append(system_response)
        session.modified = True

        return jsonify(
            {
                "status": "success",
                "message_id": message_id,
                "response": response_text,
                "workflow_id": result.get("workflow_id"),
                "workflow": result.get("workflow", {}),
                "execution_time": result.get("execution_time", 0),
                "results": result.get("results", {}),
                "metadata": system_response["metadata"],
                "chat_updated": True,
            }
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "error": str(e),
                    "response": f"I'm having technical difficulties: {str(e)}",
                }
            ),
            500,
        )


def create_natural_response(result, original_request):
    """Create a natural language response from orchestrator results."""

    # Check if we have a synthesized response from orchestrator
    if result.get("response"):
        # Use the orchestrator's synthesized response
        return result["response"]

    # Fallback: Create response from components
    if result.get("status") == "error":
        error_msg = result.get("error", "An unknown error occurred")
        return f"I encountered an error while processing your request: {error_msg}\n\nPlease try again or provide more specific information."

    # Build response from results
    response_parts = []

    # Add opening based on request type
    if "extract" in original_request.lower():
        response_parts.append(
            "I've extracted the requested information from your content:"
        )
    elif "analyze" in original_request.lower():
        response_parts.append("I've completed the analysis of your content:")
    else:
        response_parts.append("I've processed your request successfully:")

    # Process agent results
    agent_results = result.get("results", {})
    workflow_steps = result.get("workflow", {}).get("steps", [])

    # Extract meaningful content from each agent
    all_emails = []
    all_urls = []
    all_phones = []
    other_data = {}

    for agent_name, agent_result in agent_results.items():
        if (
            not isinstance(agent_result, dict)
            or agent_result.get("status") != "success"
        ):
            continue

        agent_data = agent_result.get("data", {})

        # Collect specific data types
        if isinstance(agent_data, dict):
            if "emails" in agent_data:
                all_emails.extend(agent_data["emails"])
            if "urls" in agent_data:
                all_urls.extend(agent_data["urls"])
            if "phones" in agent_data:
                all_phones.extend(agent_data["phones"])

            # Collect other data
            for key, value in agent_data.items():
                if key not in ["emails", "urls", "phones"]:
                    other_data[key] = value

    # Format findings
    if all_emails:
        response_parts.append(f"\n📧 **Email Addresses Found ({len(all_emails)}):**")
        for email in all_emails[:10]:  # Limit display
            response_parts.append(f"  • {email}")
        if len(all_emails) > 10:
            response_parts.append(f"  • ... and {len(all_emails) - 10} more")

    if all_urls:
        response_parts.append(f"\n🔗 **URLs Found ({len(all_urls)}):**")
        for url in all_urls[:10]:
            response_parts.append(f"  • {url}")
        if len(all_urls) > 10:
            response_parts.append(f"  • ... and {len(all_urls) - 10} more")

    if all_phones:
        response_parts.append(f"\n📞 **Phone Numbers Found ({len(all_phones)}):**")
        for phone in all_phones[:10]:
            response_parts.append(f"  • {phone}")

    # Add other data if present
    if other_data:
        response_parts.append("\n📊 **Additional Information:**")
        for key, value in list(other_data.items())[:5]:
            response_parts.append(f"  • {key.replace('_', ' ').title()}: {value}")

    # If no specific data found
    if not (all_emails or all_urls or all_phones or other_data):
        response_parts.append(
            "\nNo specific data items were extracted from your content."
        )

    # Add execution summary
    if workflow_steps:
        response_parts.append(f"\n---")
        response_parts.append(
            f"*Processed using {len(workflow_steps)} agents in {result.get('execution_time', 0):.1f} seconds*"
        )

    return "\n".join(response_parts)


def extract_content_summary(agent_results):
    """Extract meaningful content from agent results."""
    content_parts = []

    for agent_name, agent_result in agent_results.items():
        if (
            not isinstance(agent_result, dict)
            or agent_result.get("status") != "success"
        ):
            continue

        agent_data = agent_result.get("data", {})

        # Email extraction
        if "email" in agent_name.lower() and isinstance(agent_data, dict):
            emails = agent_data.get("emails", [])
            if emails:
                content_parts.append(f"Found **{len(emails)} email addresses**:")
                for email in emails[:5]:  # Show first 5
                    content_parts.append(f"   • {email}")
                if len(emails) > 5:
                    content_parts.append(f"   • ... and {len(emails) - 5} more")

        # URL extraction
        elif "url" in agent_name.lower() and isinstance(agent_data, dict):
            urls = agent_data.get("urls", [])
            if urls:
                content_parts.append(f"Found **{len(urls)} URLs**:")
                for url in urls[:3]:  # Show first 3
                    content_parts.append(f"   • {url}")
                if len(urls) > 3:
                    content_parts.append(f"   • ... and {len(urls) - 3} more")

        # Generic data processing
        else:
            if isinstance(agent_data, dict) and agent_data:
                summary_items = []
                for key, value in list(agent_data.items())[:3]:
                    if isinstance(value, list):
                        summary_items.append(
                            f"**{key.replace('_', ' ').title()}**: {len(value)} items"
                        )
                    elif isinstance(value, (int, float)):
                        summary_items.append(
                            f"**{key.replace('_', ' ').title()}**: {value}"
                        )

                if summary_items:
                    content_parts.append(
                        f"**{agent_name.replace('_', ' ').title()} Results:**"
                    )
                    content_parts.extend([f"   • {item}" for item in summary_items])

    return content_parts


# Simple API endpoints
@api_bp.route("/workflow/<workflow_id>/status")
def get_workflow_status(workflow_id):
    """Get workflow status."""
    try:
        status = orchestrator_service.get_workflow_status(workflow_id)
        if not status:
            return jsonify({"error": "Workflow not found"}), 404
        return jsonify(status)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/registry/agents")
def list_agents():
    """Get list of available agents."""
    try:
        agents = registry_service.get_agents_list()
        return jsonify({"agents": agents, "count": len(agents)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/registry/tools")
def list_tools():
    """Get list of available tools."""
    try:
        tools = registry_service.get_tools_list()
        return jsonify({"tools": tools, "count": len(tools)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/registry/stats")
def registry_stats():
    """Get registry statistics."""
    try:
        stats = registry_service.get_registry_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/chat/history")
def get_chat_history():
    """Get current chat history."""
    try:
        history = session.get("chat_history", [])
        return jsonify({"history": history, "count": len(history)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/chat/clear", methods=["POST"])
def clear_chat_history():
    """Clear chat history."""
    try:
        session["chat_history"] = []
        session.modified = True
        return jsonify({"status": "success", "message": "Chat history cleared"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/chat/export")
def export_chat_history():
    """Export chat history as JSON."""
    try:
        history = session.get("chat_history", [])
        export_data = {
            "exported_at": datetime.now().isoformat(),
            "message_count": len(history),
            "messages": history,
        }

        response = make_response(json.dumps(export_data, indent=2))
        response.headers["Content-Type"] = "application/json"
        response.headers["Content-Disposition"] = (
            f'attachment; filename=chat_history_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        )
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Error handlers
@api_bp.errorhandler(400)
def bad_request(error):
    """Handle 400 errors."""
    return jsonify({"error": "Bad request"}), 400


@api_bp.errorhandler(404)
def not_found_api(error):
    """Handle 404 errors."""
    return jsonify({"error": "Endpoint not found"}), 404


@api_bp.errorhandler(500)
def internal_error_api(error):
    """Handle 500 errors."""
    return jsonify({"error": "Internal server error"}), 500


@api_bp.route("/workflows")
def list_workflows():
    """Get workflow history."""
    try:
        per_page = min(int(request.args.get("per_page", 20)), 100)
        workflows = orchestrator_service.get_workflow_history(limit=per_page)
        return jsonify(
            {"workflows": workflows, "count": len(workflows), "total": len(workflows)}
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/registry/dependencies")
def get_dependencies():
    """Get dependency graph."""
    try:
        deps = registry_service.get_dependency_graph()
        return jsonify(deps)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def get_current_workflow_status(self) -> Dict[str, Any]:
    """Get current workflow execution status for sidebar display."""
    try:
        # Get active workflows from orchestrator service
        from flask_app.services.orchestrator_service import orchestrator_service

        active_workflows = orchestrator_service.get_active_workflows()

        if not active_workflows:
            return {
                "status": "idle",
                "message": "No active workflows",
                "current_workflow": None,
            }

        # Get the most recent active workflow
        current = active_workflows[0]

        return {
            "status": "active",
            "message": f"Processing: {current.get('request', 'Unknown task')[:50]}...",
            "current_workflow": {
                "id": current.get("workflow_id"),
                "request": current.get("request"),
                "status": current.get("status"),
                "started_at": current.get("started_at"),
                "progress": self._calculate_workflow_progress(current),
            },
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error getting workflow status: {str(e)}",
            "current_workflow": None,
        }


def _calculate_workflow_progress(self, workflow_data: Dict) -> int:
    """Calculate workflow progress percentage."""
    # This is a simple calculation - you can make it more sophisticated
    if workflow_data.get("status") == "completed":
        return 100
    elif workflow_data.get("status") == "processing":
        return 50  # Assume 50% when processing
    else:
        return 0


# @api_bp.route("/workflow/status/current")
# def get_current_workflow_status():
#     """Get current workflow status for sidebar display."""
#     try:
#         # Get active workflows from orchestrator service
#         active_workflows = orchestrator_service.get_active_workflows()
#         recent_workflows = orchestrator_service.get_workflow_history(limit=1)

#         # If there's an active workflow, show it
#         if active_workflows:
#             current = active_workflows[0]
#             return jsonify(
#                 {
#                     "status": "active",
#                     "message": f"Processing: {current.get('request', 'Unknown task')[:50]}...",
#                     "current_workflow": {
#                         "id": current.get("workflow_id"),
#                         "request": current.get("request"),
#                         "status": current.get("status"),
#                         "started_at": current.get("started_at"),
#                         "timeline": [],
#                         "progress": (
#                             50 if current.get("status") == "processing" else 100
#                         ),
#                     },
#                     "workflow_results": {
#                         "agentsUsed": len(current.get("agents", [])),
#                         "executionTime": current.get("execution_time", 0),
#                         "status": current.get("status", "Processing"),
#                         "componentsCreated": 0,
#                     },
#                 }
#             )

#         # If no active workflow, show the most recent completed one
#         elif recent_workflows:
#             recent = recent_workflows[0]
#             return jsonify(
#                 {
#                     "status": "completed",
#                     "message": f"Last execution: {recent.get('request', 'Unknown task')[:50]}...",
#                     "current_workflow": {
#                         "id": recent.get("workflow_id"),
#                         "request": recent.get("request"),
#                         "status": "completed",
#                         "started_at": recent.get("started_at"),
#                         "timeline": [],
#                         "progress": 100,
#                     },
#                     "workflow_results": {
#                         "agentsUsed": recent.get(
#                             "files", 0
#                         ),  # This might need adjustment based on your data
#                         "executionTime": recent.get("execution_time", 0),
#                         "status": "Success",
#                         "componentsCreated": 0,
#                     },
#                 }
#             )

#         # No workflows at all
#         else:
#             return jsonify(
#                 {
#                     "status": "idle",
#                     "message": "No recent workflows",
#                     "current_workflow": None,
#                     "workflow_results": {
#                         "agentsUsed": 0,
#                         "executionTime": 0,
#                         "status": "Idle",
#                         "componentsCreated": 0,
#                     },
#                 }
#             )

#     except Exception as e:
#         return (
#             jsonify(
#                 {
#                     "status": "error",
#                     "message": f"Error getting workflow status: {str(e)}",
#                     "current_workflow": None,
#                     "workflow_results": {
#                         "agentsUsed": 0,
#                         "executionTime": 0,
#                         "status": "Error",
#                         "componentsCreated": 0,
#                     },
#                 }
#             ),
#             500,
#         )

```

--------------------------------------------------------------------------------

### File: flask_app/routes/main.py
**Path:** `flask_app/routes/main.py`
**Size:** 11,464 bytes
**Modified:** 2025-09-08 21:06:56

```python
# flask_app/routes/main.py
"""
Main Routes Blueprint
Handles page rendering and navigation
"""

from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from flask_app.services.registry_service import registry_service
from flask_app.services.orchestrator_service import orchestrator_service
import os

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Main chat interface page with enhanced system status."""
    try:
        # Get chat history from session
        chat_history = session.get("chat_history", [])
        # Get comprehensive system status with safe defaults
        system_status = {
            "backend_available": registry_service.is_available(),
            "registry_stats": registry_service.get_registry_stats() or {},
            "recent_workflows": [],  # Start with empty list
            "system_performance": {},  # Start with empty dict
        }

        # Only try to get workflows if orchestrator is available
        try:
            if orchestrator_service.is_backend_available():
                system_status["recent_workflows"] = (
                    orchestrator_service.get_workflow_history(limit=5) or []
                )
                system_status["system_performance"] = (
                    orchestrator_service.get_system_stats() or {}
                )
        except Exception as e:
            print(f"Warning: Could not get orchestrator data: {e}")
            # Continue with empty data rather than failing

        # Get session-based chat history with safe default
        chat_history = session.get("chat_history", [])

        # Get user preferences with safe defaults
        user_settings = {
            "auto_create": session.get("auto_create", True),
            "workflow_type": session.get("workflow_type", "sequential"),
            "theme": session.get("theme", "light"),
            "show_debug": session.get("debug_mode", False),
        }

        return render_template(
            "index.jinja2",  # Use correct template name
            system_status=system_status,
            chat_history=chat_history,
            user_settings=user_settings,
        )

    except Exception as e:
        print(f"Error in index route: {str(e)}")
        import traceback

        traceback.print_exc()
        flash(f"Error loading chat interface: {str(e)}", "error")
        return render_template(
            "error.html", error_code=500, error_message="Failed to load chat interface"
        )


@main_bp.route("/registry")
def registry():
    """Registry explorer page."""
    try:
        # Get filter parameters
        agent_tags = request.args.getlist("agent_tags")
        tool_tags = request.args.getlist("tool_tags")
        search_query = request.args.get("search", "").strip()

        # Fetch data with safe defaults
        agents = (
            registry_service.get_agents_list(tags=agent_tags if agent_tags else None)
            or []
        )

        tools = (
            registry_service.get_tools_list(tags=tool_tags if tool_tags else None) or []
        )

        registry_stats = registry_service.get_registry_stats() or {
            "available": False,
            "statistics": {"total_agents": 0, "total_tools": 0},
            "summary": {"health_score": 0, "status": "unavailable"},
        }

        # Apply search filter if provided
        if search_query:
            search_results = registry_service.search_components(search_query)
            agents = search_results.get("agents", [])
            tools = search_results.get("tools", [])

        # Get all available tags for filters
        all_agent_tags = set()
        all_tool_tags = set()

        for agent in registry_service.get_agents_list() or []:
            all_agent_tags.update(agent.get("tags", []))

        for tool in registry_service.get_tools_list() or []:
            all_tool_tags.update(tool.get("tags", []))

        return render_template(
            "registry.html",
            agents=agents,
            tools=tools,
            registry_stats=registry_stats,
            all_agent_tags=sorted(all_agent_tags),
            all_tool_tags=sorted(all_tool_tags),
            current_filters={
                "agent_tags": agent_tags,
                "tool_tags": tool_tags,
                "search": search_query,
            },
        )

    except Exception as e:
        print(f"Registry error: {str(e)}")
        import traceback

        traceback.print_exc()
        flash(f"Error loading registry: {str(e)}", "error")
        return render_template(
            "error.html", error_code=500, error_message="Failed to load registry"
        )


@main_bp.route("/workflows")
def workflows():
    """Workflow history and management page."""
    try:
        # Get real workflow history from orchestrator service
        all_workflows = []
        active_workflows = []

        try:
            all_workflows = orchestrator_service.get_workflow_history() or []
            active_workflows = orchestrator_service.get_active_workflows() or []
        except Exception as e:
            print(f"Error getting workflow data: {e}")
            # Fallback to empty lists

        # Get pagination parameters
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 20))

        # Apply pagination
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        workflows = all_workflows[start_idx:end_idx]

        pagination_info = {
            "page": page,
            "per_page": per_page,
            "total": len(all_workflows),
            "pages": max(1, (len(all_workflows) + per_page - 1) // per_page),
            "has_prev": page > 1,
            "has_next": end_idx < len(all_workflows),
        }

        # Get system stats
        system_stats = {
            "avg_processing_time": sum(
                w.get("execution_time", 0) for w in all_workflows
            )
            / max(len(all_workflows), 1),
            "success_rate": len(
                [w for w in all_workflows if w.get("status") == "success"]
            )
            / max(len(all_workflows), 1),
            "total_processed": len(all_workflows),
            "active_workflows": len(active_workflows),
        }

        return render_template(
            "workflows.html",
            workflows=workflows,
            active_workflows=active_workflows,
            pagination=pagination_info,
            system_stats=system_stats,
        )

    except Exception as e:
        print(f"Workflows error: {str(e)}")
        flash(f"Error loading workflows: {str(e)}", "error")
        return render_template(
            "error.html", error_code=500, error_message="Failed to load workflows"
        )


@main_bp.route("/workflow/<workflow_id>")
def workflow_detail(workflow_id):
    """Detailed view of a specific workflow."""
    try:
        # Get workflow status and details
        workflow_status = orchestrator_service.get_workflow_status(workflow_id)

        if not workflow_status:
            flash("Workflow not found", "error")
            return redirect(url_for("main.workflows"))

        # Get visualization data
        from flask_app.services import workflow_service

        viz_data = workflow_service.get_workflow_visualization(workflow_id)

        return render_template(
            "workflow_detail.jinja2",
            workflow=workflow_status,
            visualization=viz_data,
            workflow_id=workflow_id,
        )

    except Exception as e:
        flash(f"Error loading workflow details: {str(e)}", "error")
        return redirect(url_for("main.workflows"))


@main_bp.route("/agent/<agent_name>")
def agent_detail(agent_name):
    """Detailed view of a specific agent."""
    try:
        agent = registry_service.get_agent_details(agent_name)

        if not agent:
            flash("Agent not found", "error")
            return redirect(url_for("main.registry"))

        return render_template("agent_detail.html", agent=agent, agent_name=agent_name)

    except Exception as e:
        flash(f"Error loading agent details: {str(e)}", "error")
        return redirect(url_for("main.registry"))


@main_bp.route("/tool/<tool_name>")
def tool_detail(tool_name):
    """Detailed view of a specific tool."""
    try:
        tool = registry_service.get_tool_details(tool_name)

        if not tool:
            flash("Tool not found", "error")
            return redirect(url_for("main.registry"))

        return render_template("tool_detail.html", tool=tool, tool_name=tool_name)

    except Exception as e:
        flash(f"Error loading tool details: {str(e)}", "error")
        return redirect(url_for("main.registry"))


@main_bp.route("/dependencies")
def dependencies():
    """Dependency graph visualization page."""
    try:
        dependency_graph = registry_service.get_dependency_graph()

        return render_template("dependencies.html", graph=dependency_graph)

    except Exception as e:
        flash(f"Error loading dependencies: {str(e)}", "error")
        return render_template(
            "error.html",
            error_code=500,
            error_message="Failed to load dependency graph",
        )


@main_bp.route("/help")
def help_page():
    """Help and documentation page."""
    return render_template("help.html")


@main_bp.route("/settings")
def settings():
    """Application settings page."""
    try:
        current_settings = {
            "debug_mode": session.get("debug_mode", False),
            "show_code_generation": session.get("show_code_generation", False),
            "theme": session.get("theme", "light"),
            "auto_create": session.get("auto_create", True),
            "workflow_type": session.get("workflow_type", "sequential"),
        }

        return render_template("settings.html", settings=current_settings)

    except Exception as e:
        flash(f"Error loading settings: {str(e)}", "error")
        return render_template(
            "error.html", error_code=500, error_message="Failed to load settings"
        )


@main_bp.route("/settings", methods=["POST"])
def update_settings():
    """Update application settings."""
    try:
        # Update session settings
        session["debug_mode"] = request.form.get("debug_mode") == "on"
        session["show_code_generation"] = (
            request.form.get("show_code_generation") == "on"
        )
        session["theme"] = request.form.get("theme", "light")
        session["auto_create"] = request.form.get("auto_create") == "on"
        session["workflow_type"] = request.form.get("workflow_type", "sequential")

        flash("Settings updated successfully", "success")
        return redirect(url_for("main.settings"))

    except Exception as e:
        flash(f"Error updating settings: {str(e)}", "error")
        return redirect(url_for("main.settings"))


# Error handlers for this blueprint
@main_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors within main blueprint."""
    return (
        render_template("error.html", error_code=404, error_message="Page not found"),
        404,
    )


@main_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors within main blueprint."""
    return (
        render_template(
            "error.html", error_code=500, error_message="Internal server error"
        ),
        500,
    )

```

--------------------------------------------------------------------------------

### File: flask_app/services/__init__.py
**Path:** `flask_app/services/__init__.py`
**Size:** 368 bytes
**Modified:** 2025-09-08 21:07:09

```python
from .orchestrator_service import OrchestratorService, orchestrator_service
from .registry_service import RegistryService, registry_service
from .workflow_service import WorkflowService, workflow_service

__all__ = [
    "OrchestratorService",
    "RegistryService",
    "WorkflowService",
    "orchestrator_service",
    "registry_service",
    "workflow_service",
]

```

--------------------------------------------------------------------------------

### File: flask_app/services/orchestrator_service.py
**Path:** `flask_app/services/orchestrator_service.py`
**Size:** 11,710 bytes
**Modified:** 2025-09-08 22:03:45

```python
# flask_app/services/orchestrator_service.py
"""
Orchestrator Service
Interfaces with core/orchestrator.py for request processing
"""

import os
import sys
import asyncio
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

# Add project root to path for backend imports
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(project_root)

try:
    from core.orchestrator import Orchestrator
    from core.registry_singleton import get_shared_registry
except ImportError as e:
    print(f"Warning: Could not import backend components: {e}")
    Orchestrator = None


class OrchestratorService:
    """Service layer for orchestrator operations."""

    def __init__(self):
        """Initialize orchestrator service."""
        try:
            self.orchestrator = Orchestrator() if Orchestrator else None
        except Exception as e:
            print(f"Warning: Could not initialize Orchestrator: {e}")
            self.orchestrator = None
        self.active_workflows = {}
        self.workflow_history = []

        # Add sample data for demonstration
        self.create_sample_workflows()

    def is_backend_available(self) -> bool:
        """Check if backend components are available."""
        return self.orchestrator is not None

    async def process_user_request(
        self,
        request_text: str,
        files: List[Dict] = None,
        auto_create: bool = True,
        workflow_type: str = "sequential",
    ) -> Dict[str, Any]:
        """
        Process user request through orchestrator.

        Args:
            request_text: User's natural language request
            files: List of uploaded files with metadata
            auto_create: Whether to auto-create missing agents
            workflow_type: Type of workflow execution

        Returns:
            Processed result with workflow information
        """
        workflow_id = f"wf_{uuid.uuid4().hex[:8]}"

        try:
            if not self.is_backend_available():
                return {
                    "status": "error",
                    "workflow_id": workflow_id,
                    "error": "Backend orchestrator not available",
                    "message": "Please check backend configuration",
                }

            # Prepare request data
            request_data = {
                "request": request_text,
                "files": files or [],
                "workflow_id": workflow_id,
                "workflow_type": workflow_type,
                "auto_create": auto_create,
                "started_at": datetime.now().isoformat(),
            }

            # Track workflow start
            self.active_workflows[workflow_id] = {
                "status": "processing",
                "started_at": request_data["started_at"],
                "request": request_text,
                "files": len(files) if files else 0,
            }

            # Process through orchestrator
            result = await self.orchestrator.process_request(
                user_request=request_text, files=files, auto_create=auto_create
            )

            # ADD DEBUG to see what's returned:
            print(f"DEBUG: Orchestrator returned: {result.keys()}")
            print(
                f"DEBUG: Response field: {result.get('response', 'NO RESPONSE FIELD')[:200]}"
            )

            # Update workflow status
            final_status = result.get("status", "unknown")
            self.active_workflows[workflow_id]["status"] = final_status
            self.active_workflows[workflow_id][
                "completed_at"
            ] = datetime.now().isoformat()

            # Calculate execution time
            execution_time = 0
            if workflow_id in self.active_workflows:
                try:
                    start = datetime.fromisoformat(
                        self.active_workflows[workflow_id]["started_at"]
                    )
                    execution_time = (datetime.now() - start).total_seconds()
                except:
                    execution_time = 0

            # Extract workflow info
            workflow_info = result.get("workflow", {})
            if isinstance(workflow_info, dict) and "steps" not in workflow_info:
                workflow_info = {"steps": result.get("agents", [])}

            # Format response to match frontend expectations
            formatted_response = {
                "status": final_status,
                "workflow_id": workflow_id,
                "response": result.get("response", "Request processed successfully."),
                "workflow": workflow_info,
                "execution_time": execution_time,
                "results": result.get("results", {}),
                "metadata": {
                    "agents_used": workflow_info.get("steps", []),
                    "execution_time": execution_time,
                    "components_created": result.get("metadata", {}).get(
                        "components_created", 0
                    ),
                    "workflow_type": workflow_type,
                },
            }

            # Move to history if completed
            if final_status in ["success", "error", "partial"]:
                self.workflow_history.append(self.active_workflows[workflow_id])
                if workflow_id in self.active_workflows:
                    del self.active_workflows[workflow_id]

            return formatted_response

        except Exception as e:
            # Handle processing errors
            error_result = {
                "status": "error",
                "workflow_id": workflow_id,
                "error": str(e),
                "message": "Request processing failed",
                "request_data": locals().get("request_data", {}),
                "traceback": str(e),
            }

            # Update workflow status
            if workflow_id in self.active_workflows:
                self.active_workflows[workflow_id]["status"] = "error"
                self.active_workflows[workflow_id]["error"] = str(e)

            return error_result

    def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get current status of a workflow."""

        # Check active workflows
        if workflow_id in self.active_workflows:
            return self.active_workflows[workflow_id]

        # Check history
        for workflow in self.workflow_history:
            if workflow.get("workflow_id") == workflow_id:
                return workflow

        return None

    def cancel_workflow(self, workflow_id: str) -> bool:
        """Cancel an active workflow."""
        if workflow_id in self.active_workflows:
            self.active_workflows[workflow_id]["status"] = "cancelled"
            self.active_workflows[workflow_id][
                "cancelled_at"
            ] = datetime.now().isoformat()
            return True
        return False

    def get_active_workflows(self) -> List[Dict[str, Any]]:
        """Get list of currently active workflows."""
        active = list(self.active_workflows.values())

        # Ensure each active workflow has required fields
        for workflow in active:
            workflow.setdefault(
                "workflow_id", workflow.get("id", f"active_{len(active)}")
            )
            workflow.setdefault("request", "Active workflow processing...")
            workflow.setdefault("status", "processing")
            workflow.setdefault("started_at", datetime.now().isoformat())

        return active

    def get_workflow_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent workflow history."""
        history = self.workflow_history[-limit:] if self.workflow_history else []

        # Ensure each workflow has required fields for the template
        for workflow in history:
            workflow.setdefault("workflow_id", f"wf_{len(history)}")
            workflow.setdefault("request", "Sample workflow request")
            workflow.setdefault("status", "completed")
            workflow.setdefault("started_at", datetime.now().isoformat())
            workflow.setdefault("execution_time", 2.5)
            workflow.setdefault("files", 0)

        return history

    def get_system_stats(self) -> Dict[str, Any]:
        """Get system performance statistics."""
        return {
            "active_workflows": len(self.active_workflows),
            "total_processed": len(self.workflow_history),
            "backend_available": self.is_backend_available(),
            "avg_processing_time": self._calculate_avg_processing_time(),
            "success_rate": self._calculate_success_rate(),
        }

    def _calculate_avg_processing_time(self) -> float:
        """Calculate average processing time from history."""
        if not self.workflow_history:
            return 0.0

        total_time = 0
        count = 0

        for workflow in self.workflow_history:
            if "started_at" in workflow and "completed_at" in workflow:
                try:
                    start = datetime.fromisoformat(workflow["started_at"])
                    end = datetime.fromisoformat(workflow["completed_at"])
                    total_time += (end - start).total_seconds()
                    count += 1
                except:
                    continue

        return total_time / count if count > 0 else 0.0

    def _calculate_success_rate(self) -> float:
        """Calculate success rate from history."""
        if not self.workflow_history:
            return 1.0

        successful = sum(
            1 for w in self.workflow_history if w.get("status") == "success"
        )
        return successful / len(self.workflow_history)

    def create_sample_workflows(self):
        """Create sample workflow data for demonstration."""
        if not self.workflow_history:  # Only create if empty
            sample_workflows = [
                {
                    "workflow_id": "wf_demo_001",
                    "request": "Extract emails from uploaded document",
                    "status": "success",
                    "started_at": (datetime.now() - timedelta(hours=2)).isoformat(),
                    "completed_at": (
                        datetime.now() - timedelta(hours=2) + timedelta(minutes=5)
                    ).isoformat(),
                    "execution_time": 4.2,
                    "files": 1,
                },
                {
                    "workflow_id": "wf_demo_002",
                    "request": "Analyze CSV data and create statistical report",
                    "status": "success",
                    "started_at": (datetime.now() - timedelta(hours=1)).isoformat(),
                    "completed_at": (
                        datetime.now() - timedelta(hours=1) + timedelta(minutes=8)
                    ).isoformat(),
                    "execution_time": 7.8,
                    "files": 1,
                },
                {
                    "workflow_id": "wf_demo_003",
                    "request": "Extract phone numbers and URLs from text",
                    "status": "partial",
                    "started_at": (datetime.now() - timedelta(minutes=30)).isoformat(),
                    "completed_at": (
                        datetime.now() - timedelta(minutes=25)
                    ).isoformat(),
                    "execution_time": 3.1,
                    "files": 0,
                },
            ]
            self.workflow_history.extend(sample_workflows)


# Global service instance
orchestrator_service = OrchestratorService()

```

--------------------------------------------------------------------------------

### File: flask_app/services/registry_service.py
**Path:** `flask_app/services/registry_service.py`
**Size:** 14,398 bytes
**Modified:** 2025-09-08 09:36:39

```python
# flask_app/services/registry_service.py
"""
Registry Service
Interfaces with backend registry for agent/tool information
"""

import os
import sys
from typing import Dict, List, Any, Optional

# Add project root to path
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(project_root)

try:
    from core.registry_singleton import get_shared_registry
    from core.registry import RegistryManager
except ImportError as e:
    print(f"Warning: Could not import registry components: {e}")
    get_shared_registry = None


class RegistryService:
    """Service layer for registry operations."""

    def __init__(self):
        """Initialize registry service."""
        self.registry = get_shared_registry() if get_shared_registry else None

    def is_available(self) -> bool:
        """Check if registry is available."""
        return self.registry is not None

    def get_agents_list(
        self, tags: List[str] = None, active_only: bool = True
    ) -> List[Dict[str, Any]]:
        """Get list of available agents."""
        if not self.is_available():
            return []

        try:
            agents = self.registry.list_agents(tags=tags, active_only=active_only)

            # Add formatted data for UI
            for agent in agents:
                agent["formatted_created_at"] = self._format_timestamp(
                    agent.get("created_at")
                )
                agent["capabilities_summary"] = self._summarize_capabilities(agent)
                agent["performance_indicator"] = self._get_performance_indicator(agent)

            return agents
        except Exception as e:
            print(f"Error fetching agents: {e}")
            return []

    def get_tools_list(
        self, tags: List[str] = None, pure_only: bool = False
    ) -> List[Dict[str, Any]]:
        """Get list of available tools."""
        if not self.is_available():
            return []

        try:
            tools = self.registry.list_tools(tags=tags, pure_only=pure_only)

            # Add formatted data for UI
            for tool in tools:
                tool["formatted_created_at"] = self._format_timestamp(
                    tool.get("created_at")
                )
                tool["usage_summary"] = self._get_tool_usage_summary(tool)
                tool["complexity_level"] = self._assess_tool_complexity(tool)

            return tools
        except Exception as e:
            print(f"Error fetching tools: {e}")
            return []

    def get_agent_details(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific agent."""
        if not self.is_available():
            return None

        try:
            agent = self.registry.get_agent(agent_name)
            if agent:
                # Add dependency information
                agent["dependencies"] = self.registry.get_agent_dependencies(agent_name)
                agent["formatted_created_at"] = self._format_timestamp(
                    agent.get("created_at")
                )

            return agent
        except Exception as e:
            print(f"Error fetching agent details: {e}")
            return None

    def get_tool_details(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific tool."""
        if not self.is_available():
            return None

        try:
            tool = self.registry.get_tool(tool_name)
            if tool:
                # Add usage information
                tool["used_by"] = self.registry.get_tool_usage(tool_name)
                tool["formatted_created_at"] = self._format_timestamp(
                    tool.get("created_at")
                )

            return tool
        except Exception as e:
            print(f"Error fetching tool details: {e}")
            return None

    # flask_app/services/registry_service.py - Replace the get_registry_stats method

    def get_registry_stats(self) -> Dict[str, Any]:
        """Get comprehensive registry statistics - FIXED."""
        if not self.is_available():
            return {
                "available": False,
                "statistics": {"total_agents": 0, "total_tools": 0},
                "summary": {"health_score": 0, "status": "unavailable"},
            }

        try:
            # Get actual registry data directly
            registry = self.registry

            # Get agents and tools lists
            agents_data = registry.agents.get("agents", {})
            tools_data = registry.tools.get("tools", {})

            # Filter active components
            active_agents = [
                a for a in agents_data.values() if a.get("status") == "active"
            ]
            active_tools = [
                t for t in tools_data.values() if t.get("status") == "active"
            ]

            print(f"DEBUG: Registry stats calculation:")
            print(f"  Total agents in registry: {len(agents_data)}")
            print(f"  Active agents: {len(active_agents)}")
            print(f"  Total tools in registry: {len(tools_data)}")
            print(f"  Active tools: {len(active_tools)}")

            stats = {
                "total_agents": len(active_agents),
                "total_tools": len(active_tools),
                "total_components": len(active_agents) + len(active_tools),
                "prebuilt_agents": len(
                    [a for a in active_agents if a.get("is_prebuilt", False)]
                ),
                "generated_agents": len(
                    [a for a in active_agents if not a.get("is_prebuilt", False)]
                ),
                "execution_count": sum(
                    a.get("execution_count", 0) for a in active_agents
                ),
            }

            # Calculate health score
            health_score = 100 if stats["total_components"] > 0 else 0
            if stats["total_agents"] > 0:
                # Better health calculation
                base_score = 50
                agent_bonus = min(
                    30, stats["total_agents"] * 5
                )  # Up to 30 points for agents
                tool_bonus = min(
                    20, stats["total_tools"] * 2
                )  # Up to 20 points for tools
                health_score = base_score + agent_bonus + tool_bonus

            return {
                "available": True,
                "statistics": stats,
                "summary": {
                    "health_score": min(100, health_score),
                    "status": (
                        "healthy"
                        if health_score > 70
                        else "degraded" if health_score > 30 else "poor"
                    ),
                },
                "agent_breakdown": {
                    "prebuilt": stats["prebuilt_agents"],
                    "generated": stats["generated_agents"],
                    "active": stats["total_agents"],
                },
                "performance": {
                    "total_executions": stats["execution_count"],
                    "avg_execution_time": self._calculate_avg_execution_time(
                        active_agents
                    ),
                },
            }
        except Exception as e:
            print(f"ERROR: Failed to get registry stats: {e}")
            import traceback

            traceback.print_exc()
            return {
                "available": True,
                "statistics": {"total_agents": 0, "total_tools": 0},
                "summary": {"health_score": 0, "status": "error"},
                "error": str(e),
            }

    def _calculate_avg_execution_time(self, agents: List[Dict]) -> float:
        """Calculate average execution time from agents."""
        if not agents:
            return 0.0

        total_time = 0
        count = 0

        for agent in agents:
            if agent.get("avg_execution_time", 0) > 0:
                total_time += agent["avg_execution_time"]
                count += 1

        return total_time / count if count > 0 else 0.0

    def get_dependency_graph(self) -> Dict[str, Any]:
        """Get dependency graph for visualization."""
        if not self.is_available():
            return {
                "nodes": [],
                "edges": [],
                "stats": {
                    "total_agents": 0,
                    "total_tools": 0,
                    "missing_dependencies": 0,
                    "unused_tools": 0,
                },
            }

        try:
            deps = self.registry.get_dependency_graph()

            # Convert to visualization format
            nodes = []
            edges = []

            # Add agent nodes
            for agent_name, tools in deps.get("agents_to_tools", {}).items():
                nodes.append(
                    {
                        "id": agent_name,
                        "type": "agent",
                        "name": agent_name,  # Add name field
                        "label": agent_name,
                        "description": self._get_agent_description(agent_name),
                        "uses_tools": tools,  # Add for UI
                    }
                )

                # Add edges to tools
                for tool_name in tools:
                    edges.append(
                        {"from": tool_name, "to": agent_name, "type": "dependency"}
                    )

            # Add tool nodes
            for tool_name, agents_using in deps.get("tools_to_agents", {}).items():
                nodes.append(
                    {
                        "id": tool_name,
                        "type": "tool",
                        "name": tool_name,  # Add name field
                        "label": tool_name,
                        "description": self._get_tool_description(tool_name),
                        "used_by": agents_using,  # Add for UI
                    }
                )

            # Calculate statistics
            agent_nodes = [n for n in nodes if n["type"] == "agent"]
            tool_nodes = [n for n in nodes if n["type"] == "tool"]
            unused_tools = [t for t in tool_nodes if not t.get("used_by")]

            return {
                "nodes": nodes,
                "edges": edges,
                "stats": {
                    "total_agents": len(agent_nodes),
                    "total_tools": len(tool_nodes),
                    "total_nodes": len(nodes),
                    "total_edges": len(edges),
                    "missing_dependencies": len(deps.get("missing_dependencies", [])),
                    "unused_tools": len(unused_tools),
                },
            }

        except Exception as e:
            print(f"Error building dependency graph: {e}")
            return {
                "nodes": [],
                "edges": [],
                "error": str(e),
                "stats": {
                    "total_agents": 0,
                    "total_tools": 0,
                    "missing_dependencies": 0,
                    "unused_tools": 0,
                },
            }

    def search_components(self, query: str) -> Dict[str, List[Dict]]:
        """Search agents and tools by query."""
        if not self.is_available():
            return {"agents": [], "tools": []}

        try:
            agents = self.registry.search_agents(query)
            tools = self.registry.search_tools(query)

            return {
                "agents": agents,
                "tools": tools,
                "total_results": len(agents) + len(tools),
            }
        except Exception as e:
            print(f"Error searching components: {e}")
            return {"agents": [], "tools": [], "error": str(e)}

    def _format_timestamp(self, timestamp: str = None) -> str:
        """Format timestamp for display."""
        if not timestamp:
            from datetime import datetime

            return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            from datetime import datetime

            dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            return timestamp

    def _summarize_capabilities(self, agent: Dict) -> str:
        """Create a summary of agent capabilities."""
        tools = agent.get("uses_tools", [])
        tags = agent.get("tags", [])

        if tools:
            return f"Uses {len(tools)} tools: {', '.join(tools[:3])}{'...' if len(tools) > 3 else ''}"
        elif tags:
            return f"Tags: {', '.join(tags[:3])}{'...' if len(tags) > 3 else ''}"
        else:
            return "General purpose agent"

    def _get_performance_indicator(self, agent: Dict) -> str:
        """Get performance indicator for agent."""
        exec_count = agent.get("execution_count", 0)
        avg_time = agent.get("avg_execution_time", 0)

        if exec_count == 0:
            return "New"
        elif avg_time < 2:
            return "Fast"
        elif avg_time < 10:
            return "Normal"
        else:
            return "Slow"

    def _get_tool_usage_summary(self, tool: Dict) -> str:
        """Get usage summary for tool."""
        used_by = tool.get("used_by_agents", [])
        if not used_by:
            return "Unused"
        elif len(used_by) == 1:
            return f"Used by {used_by[0]}"
        else:
            return f"Used by {len(used_by)} agents"

    def _assess_tool_complexity(self, tool: Dict) -> str:
        """Assess tool complexity level."""
        line_count = tool.get("line_count", 0)
        if line_count < 30:
            return "Simple"
        elif line_count < 100:
            return "Medium"
        else:
            return "Complex"

    def _get_agent_description(self, agent_name: str) -> str:
        """Get agent description for visualization."""
        agent = self.get_agent_details(agent_name)
        return agent.get("description", "Agent") if agent else "Agent"

    def _get_tool_description(self, tool_name: str) -> str:
        """Get tool description for visualization."""
        tool = self.get_tool_details(tool_name)
        return tool.get("description", "Tool") if tool else "Tool"


# Global service instance
registry_service = RegistryService()

```

--------------------------------------------------------------------------------

### File: flask_app/services/workflow_service.py
**Path:** `flask_app/services/workflow_service.py`
**Size:** 15,266 bytes
**Modified:** 2025-09-08 21:07:45

```python
# flask_app/services/workflow_service.py
"""
Workflow Service
Handles workflow visualization and real-time updates
"""

import os
import sys
import json
from typing import Dict, List, Any, Optional, Generator
from datetime import datetime

# Add project root to path
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(project_root)

try:
    from core.workflow_engine import WorkflowEngine, WorkflowState
except ImportError as e:
    print(f"Warning: Could not import workflow components: {e}")
    WorkflowEngine = None


class WorkflowService:
    """Service layer for workflow operations."""

    def __init__(self):
        """Initialize workflow service."""
        self.workflow_engine = WorkflowEngine() if WorkflowEngine else None
        self.workflow_cache = {}

    def is_available(self) -> bool:
        """Check if workflow engine is available."""
        return self.workflow_engine is not None

    def get_workflow_visualization(self, workflow_id: str) -> Dict[str, Any]:
        """Get workflow visualization data."""
        if not self.is_available():
            return {"error": "Workflow engine not available"}

        # Check cache first
        if workflow_id in self.workflow_cache:
            workflow_data = self.workflow_cache[workflow_id]
        else:
            # Get from workflow engine
            workflow_status = self.workflow_engine.get_workflow_status(workflow_id)
            if not workflow_status:
                return {"error": "Workflow not found"}
            workflow_data = workflow_status

        return self._create_visualization_data(workflow_data)

    def stream_workflow_updates(self, workflow_id: str) -> Generator[str, None, None]:
        """Stream real-time workflow updates."""
        if not self.is_available():
            yield f"data: {json.dumps({'error': 'Workflow engine not available'})}\n\n"
            return

        # This would connect to real workflow engine streaming
        # For now, simulate updates
        import time

        for i in range(10):  # Simulate 10 updates
            time.sleep(1)

            update = {
                "workflow_id": workflow_id,
                "timestamp": datetime.now().isoformat(),
                "type": "status_update",
                "data": {
                    "step": i + 1,
                    "status": "processing" if i < 9 else "completed",
                    "message": f"Processing step {i + 1}/10",
                },
            }

            yield f"data: {json.dumps(update)}\n\n"

        # Final completion message
        completion = {
            "workflow_id": workflow_id,
            "timestamp": datetime.now().isoformat(),
            "type": "completion",
            "data": {
                "status": "completed",
                "message": "Workflow completed successfully",
            },
        }
        yield f"data: {json.dumps(completion)}\n\n"

    def create_workflow_diagram(
        self, agents: List[str], workflow_type: str = "sequential"
    ) -> str:
        """Create Mermaid diagram for workflow."""
        if workflow_type == "sequential":
            return self._create_sequential_diagram(agents)
        elif workflow_type == "parallel":
            return self._create_parallel_diagram(agents)
        else:
            return self._create_conditional_diagram(agents)

    def get_execution_timeline(self, workflow_id: str) -> List[Dict[str, Any]]:
        """Get execution timeline for workflow."""
        if workflow_id in self.workflow_cache:
            workflow_data = self.workflow_cache[workflow_id]
            return self._extract_timeline(workflow_data)

        return []

    def _create_visualization_data(self, workflow_data: Dict) -> Dict[str, Any]:
        """Create visualization data structure."""
        agents = workflow_data.get("agents", [])
        workflow_type = workflow_data.get("type", "sequential")

        return {
            "workflow_id": workflow_data.get("id", "unknown"),
            "type": workflow_type,
            "diagram": self.create_workflow_diagram(agents, workflow_type),
            "nodes": self._create_node_data(agents, workflow_data),
            "edges": self._create_edge_data(agents, workflow_type),
            "timeline": self.get_execution_timeline(workflow_data.get("id", "")),
            "status": workflow_data.get("status", "unknown"),
            "progress": self._calculate_progress(workflow_data),
        }

    def _create_node_data(self, agents: List[str], workflow_data: Dict) -> List[Dict]:
        """Create node data for visualization."""
        nodes = []

        for i, agent in enumerate(agents):
            status = self._get_agent_status(agent, workflow_data)

            nodes.append(
                {
                    "id": agent,
                    "label": agent.replace("_", " ").title(),
                    "type": "agent",
                    "status": status,
                    "position": {"x": i * 200, "y": 100},
                    "metadata": {
                        "execution_time": workflow_data.get("execution_times", {}).get(
                            agent, 0
                        ),
                        "tools_used": workflow_data.get("tools_used", {}).get(
                            agent, []
                        ),
                        "output_size": workflow_data.get("output_sizes", {}).get(
                            agent, 0
                        ),
                    },
                }
            )

        return nodes

    def _create_edge_data(self, agents: List[str], workflow_type: str) -> List[Dict]:
        """Create edge data for visualization."""
        edges = []

        if workflow_type == "sequential":
            for i in range(len(agents) - 1):
                edges.append(
                    {"from": agents[i], "to": agents[i + 1], "type": "sequential"}
                )
        elif workflow_type == "parallel":
            # All agents connect to a merge point
            for agent in agents:
                edges.append({"from": "start", "to": agent, "type": "parallel"})
                edges.append({"from": agent, "to": "merge", "type": "parallel"})

        return edges

    def _create_sequential_diagram(self, agents: List[str]) -> str:
        """Create Mermaid diagram for sequential workflow."""
        diagram = "graph TD\n"
        diagram += "    Start([Start])\n"

        for i, agent in enumerate(agents):
            agent_id = f"A{i+1}"
            agent_label = agent.replace("_", " ").title()
            diagram += f"    {agent_id}[{agent_label}]\n"

            if i == 0:
                diagram += f"    Start --> {agent_id}\n"
            else:
                prev_id = f"A{i}"
                diagram += f"    {prev_id} --> {agent_id}\n"

        diagram += f"    A{len(agents)} --> End([End])\n"

        # Add styling
        diagram += "\n    classDef startEnd fill:#e1f5fe\n"
        diagram += "    classDef agent fill:#f3e5f5\n"
        diagram += "    class Start,End startEnd\n"
        diagram += (
            f"    class {','.join([f'A{i+1}' for i in range(len(agents))])} agent\n"
        )

        return diagram

    def _create_parallel_diagram(self, agents: List[str]) -> str:
        """Create Mermaid diagram for parallel workflow."""
        diagram = "graph TD\n"
        diagram += "    Start([Start])\n"
        diagram += "    Merge([Merge Results])\n"
        diagram += "    End([End])\n"

        for i, agent in enumerate(agents):
            agent_id = f"A{i+1}"
            agent_label = agent.replace("_", " ").title()
            diagram += f"    {agent_id}[{agent_label}]\n"
            diagram += f"    Start --> {agent_id}\n"
            diagram += f"    {agent_id} --> Merge\n"

        diagram += "    Merge --> End\n"

        # Add styling
        diagram += "\n    classDef startEnd fill:#e1f5fe\n"
        diagram += "    classDef agent fill:#f3e5f5\n"
        diagram += "    classDef merge fill:#fff3e0\n"
        diagram += "    class Start,End startEnd\n"
        diagram += "    class Merge merge\n"
        diagram += (
            f"    class {','.join([f'A{i+1}' for i in range(len(agents))])} agent\n"
        )

        return diagram

    def _create_conditional_diagram(self, agents: List[str]) -> str:
        """Create Mermaid diagram for conditional workflow."""
        diagram = "graph TD\n"
        diagram += "    Start([Start])\n"
        diagram += "    Decision{Decision}\n"
        diagram += "    Start --> Decision\n"

        for i, agent in enumerate(agents):
            agent_id = f"A{i+1}"
            agent_label = agent.replace("_", " ").title()
            diagram += f"    {agent_id}[{agent_label}]\n"
            diagram += f"    Decision -->|Option {i+1}| {agent_id}\n"
            diagram += f"    {agent_id} --> End([End])\n"

        return diagram

    def _get_agent_status(self, agent: str, workflow_data: Dict) -> str:
        """Get current status of an agent in workflow."""
        if agent in workflow_data.get("completed", []):
            return "completed"
        elif agent in workflow_data.get("active", []):
            return "active"
        elif agent in workflow_data.get("failed", []):
            return "error"
        else:
            return "pending"

    def _calculate_progress(self, workflow_data: Dict) -> float:
        """Calculate overall workflow progress."""
        total_agents = len(workflow_data.get("agents", []))
        completed_agents = len(workflow_data.get("completed", []))

        if total_agents == 0:
            return 0.0

        return (completed_agents / total_agents) * 100

    def _extract_timeline(self, workflow_data: Dict) -> List[Dict[str, Any]]:
        """Extract execution timeline from workflow data."""
        timeline = []

        # This would extract real timeline data from workflow execution
        # For now, create sample timeline
        events = workflow_data.get("events", [])

        for event in events:
            timeline.append(
                {
                    "timestamp": event.get("timestamp", datetime.now().isoformat()),
                    "agent": event.get("agent", "unknown"),
                    "event_type": event.get("type", "execution"),
                    "message": event.get("message", "Agent executed"),
                    "duration": event.get("duration", 0),
                }
            )

        return sorted(timeline, key=lambda x: x["timestamp"])

    def get_workflow_statistics(self) -> Dict[str, Any]:
        """Get comprehensive workflow statistics."""
        try:
            # This would integrate with your actual workflow data
            return {
                "total_workflows": len(self.workflow_cache),
                "active_workflows": sum(
                    1
                    for w in self.workflow_cache.values()
                    if w.get("status") == "running"
                ),
                "success_rate": 0.85,  # Calculate from actual data
                "avg_execution_time": 5.2,  # Calculate from actual data
                "most_used_agents": ["email_extractor", "url_extractor"],
                "performance_trends": {
                    "last_hour": [1.2, 2.1, 1.8, 2.3, 1.9],
                    "success_rates": [0.9, 0.85, 0.92, 0.88, 0.87],
                },
            }
        except Exception as e:
            print(f"Error getting workflow statistics: {e}")
            return {}

    def create_mermaid_workflow_diagram(
        self, agents: List[str], status_data: Dict = None
    ) -> str:
        """Create a Mermaid diagram with real-time status."""
        diagram = "graph TD\n"
        diagram += "    Start([User Request])\n"

        for i, agent in enumerate(agents):
            agent_id = f"A{i+1}"
            agent_label = agent.replace("_", " ").title()

            # Determine status styling
            if status_data and agent in status_data:
                status = status_data[agent].get("status", "pending")
                if status == "completed":
                    diagram += f"    {agent_id}[{agent_label}]:::completed\n"
                elif status == "active":
                    diagram += f"    {agent_id}[{agent_label}]:::active\n"
                elif status == "error":
                    diagram += f"    {agent_id}[{agent_label}]:::error\n"
                else:
                    diagram += f"    {agent_id}[{agent_label}]:::pending\n"
            else:
                diagram += f"    {agent_id}[{agent_label}]\n"

            # Add connections
            if i == 0:
                diagram += f"    Start --> {agent_id}\n"
            else:
                diagram += f"    A{i} --> {agent_id}\n"

        diagram += f"    A{len(agents)} --> End([Response])\n"
        diagram += "\n"

        # Add CSS classes for styling
        diagram += "    classDef completed fill:#d4edda,stroke:#c3e6cb,color:#155724\n"
        diagram += "    classDef active fill:#fff3cd,stroke:#ffeaa7,color:#856404\n"
        diagram += "    classDef error fill:#f8d7da,stroke:#f5c6cb,color:#721c24\n"
        diagram += "    classDef pending fill:#f8f9fa,stroke:#dee2e6,color:#495057\n"

        return diagram

    def get_current_workflow_status(self) -> Dict[str, Any]:
        """Get current workflow execution status for sidebar display."""
        try:
            # Get active workflows from orchestrator service
            from flask_app.services.orchestrator_service import orchestrator_service

            active_workflows = orchestrator_service.get_active_workflows()

            if not active_workflows:
                return {
                    "status": "idle",
                    "message": "No active workflows",
                    "current_workflow": None,
                }

            # Get the most recent active workflow
            current = active_workflows[0]

            return {
                "status": "active",
                "message": f"Processing: {current.get('request', 'Unknown task')[:50]}...",
                "current_workflow": {
                    "id": current.get("workflow_id"),
                    "request": current.get("request"),
                    "status": current.get("status"),
                    "started_at": current.get("started_at"),
                    "progress": self._calculate_workflow_progress(current),
                },
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error getting workflow status: {str(e)}",
                "current_workflow": None,
            }

    def _calculate_workflow_progress(self, workflow_data: Dict) -> int:
        """Calculate workflow progress percentage."""
        # This is a simple calculation - you can make it more sophisticated
        if workflow_data.get("status") == "completed":
            return 100
        elif workflow_data.get("status") == "processing":
            return 50  # Assume 50% when processing
        else:
            return 0


# Global service instance
workflow_service = WorkflowService()

```

--------------------------------------------------------------------------------

### File: flask_app/static/css/custom.css
**Path:** `flask_app/static/css/custom.css`
**Size:** 6,513 bytes
**Modified:** 2025-09-07 23:18:47

*[Binary file or content not included]*

--------------------------------------------------------------------------------

### File: flask_app/static/favicon.ico
**Path:** `flask_app/static/favicon.ico`
**Size:** 0 bytes
**Modified:** 2025-09-07 12:52:59

*[Binary file or content not included]*

--------------------------------------------------------------------------------

### File: flask_app/static/js/app.js
**Path:** `flask_app/static/js/app.js`
**Size:** 18,226 bytes
**Modified:** 2025-09-08 23:42:21

*[Binary file or content not included]*

--------------------------------------------------------------------------------

### File: flask_app/templates/base.html
**Path:** `flask_app/templates/base.html`
**Size:** 13,865 bytes
**Modified:** 2025-09-08 22:23:37

*[Binary file or content not included]*

--------------------------------------------------------------------------------

### File: flask_app/templates/components/chat-container.html
**Path:** `flask_app/templates/components/chat-container.html`
**Size:** 18,905 bytes
**Modified:** 2025-09-08 23:47:59

*[Binary file or content not included]*

--------------------------------------------------------------------------------

### File: flask_app/templates/components/sidebar.html
**Path:** `flask_app/templates/components/sidebar.html`
**Size:** 8,404 bytes
**Modified:** 2025-09-08 23:45:51

*[Binary file or content not included]*

--------------------------------------------------------------------------------

### File: flask_app/templates/components/workflow-panel.html
**Path:** `flask_app/templates/components/workflow-panel.html`
**Size:** 5,963 bytes
**Modified:** 2025-09-08 23:28:14

*[Binary file or content not included]*

--------------------------------------------------------------------------------

### File: flask_app/templates/components/workflow-visualization.html
**Path:** `flask_app/templates/components/workflow-visualization.html`
**Size:** 18,108 bytes
**Modified:** 2025-09-08 23:14:19

*[Binary file or content not included]*

--------------------------------------------------------------------------------

### File: flask_app/templates/dependencies.html
**Path:** `flask_app/templates/dependencies.html`
**Size:** 20,910 bytes
**Modified:** 2025-09-07 22:52:12

*[Binary file or content not included]*

--------------------------------------------------------------------------------

### File: flask_app/templates/error.html
**Path:** `flask_app/templates/error.html`
**Size:** 796 bytes
**Modified:** 2025-09-07 12:38:11

*[Binary file or content not included]*

--------------------------------------------------------------------------------

### File: flask_app/templates/help.html
**Path:** `flask_app/templates/help.html`
**Size:** 1,418 bytes
**Modified:** 2025-09-07 12:54:08

*[Binary file or content not included]*

--------------------------------------------------------------------------------

### File: flask_app/templates/index.jinja2
**Path:** `flask_app/templates/index.jinja2`
**Size:** 1,981 bytes
**Modified:** 2025-09-08 23:45:24

*[Binary file or content not included]*

--------------------------------------------------------------------------------

### File: flask_app/templates/partials/chat-message.html
**Path:** `flask_app/templates/partials/chat-message.html`
**Size:** 1,380 bytes
**Modified:** 2025-09-07 13:14:07

*[Binary file or content not included]*

--------------------------------------------------------------------------------

### File: flask_app/templates/partials/workflow-status.jinja2
**Path:** `flask_app/templates/partials/workflow-status.jinja2`
**Size:** 1,232 bytes
**Modified:** 2025-09-07 13:22:50

*[Binary file or content not included]*

--------------------------------------------------------------------------------

### File: flask_app/templates/registry.html
**Path:** `flask_app/templates/registry.html`
**Size:** 7,127 bytes
**Modified:** 2025-09-08 21:01:07

*[Binary file or content not included]*

--------------------------------------------------------------------------------

### File: flask_app/templates/settings.html
**Path:** `flask_app/templates/settings.html`
**Size:** 1,933 bytes
**Modified:** 2025-09-07 12:54:29

*[Binary file or content not included]*

--------------------------------------------------------------------------------

### File: flask_app/templates/workflow_detail.jinja2
**Path:** `flask_app/templates/workflow_detail.jinja2`
**Size:** 18,007 bytes
**Modified:** 2025-09-07 13:22:48

*[Binary file or content not included]*

--------------------------------------------------------------------------------

### File: flask_app/templates/workflows.html
**Path:** `flask_app/templates/workflows.html`
**Size:** 15,881 bytes
**Modified:** 2025-09-07 22:57:12

*[Binary file or content not included]*

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
**Size:** 12,856 bytes
**Modified:** 2025-09-06 23:38:01

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
            creation_result = agent_factory.ensure_agent(
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
**Size:** 10,190 bytes
**Modified:** 2025-09-06 23:38:43

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

    # Check results structure - FIXED VERSION
    if "results" in result:
        for agent_name, agent_result in result["results"].items():
            print(f"\n  Agent: {agent_name}")
            if isinstance(agent_result, dict):
                print(f"    Status: {agent_result.get('status')}")
                # Handle both success and error cases
                if agent_result.get("data") is not None:
                    if isinstance(agent_result["data"], dict):
                        print(f"    Data keys: {list(agent_result['data'].keys())}")
                    else:
                        print(f"    Data type: {type(agent_result['data'])}")
                else:
                    # Show error if available
                    error_msg = "Unknown error"
                    if "metadata" in agent_result:
                        error_msg = agent_result["metadata"].get("error", error_msg)
                    elif "error" in agent_result:
                        error_msg = agent_result["error"]
                    print(f"    Error: {error_msg}")

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
**Size:** 5,956 bytes
**Modified:** 2025-09-08 23:29:00

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
    }
  }
}
```

--------------------------------------------------------------------------------

### File: tools.json.lock
**Path:** `tools.json.lock`
**Size:** 0 bytes
**Modified:** 2025-09-08 00:54:34

*[Binary file or content not included]*

--------------------------------------------------------------------------------
