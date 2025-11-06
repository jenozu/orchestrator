# Unified Implementation Plan: Evolving the Parallel Agent Build System

This plan integrates all previous discussions—the need for a structured input agent (`IntentParser`), the implementation of a domain-specific Knowledge Base (KB) for RAG, and the roadmap for expanding to general-purpose capabilities—into a single, actionable guide for your **Parallel Agent Build System**.

## Phase 1: Foundational Architecture and File Structure

The first step is to establish the necessary file structure to support the new `IntentParser` and the agent-specific Knowledge Base (KB) as outlined in your `knowledgebaseguide.md`.

### 1.1 Knowledge Base Directory Setup

Create the following directory structure under your existing `docs/` folder to house the domain-specific knowledge for each agent.

```
docs/
├── shared/           # Global context for all agents (e.g., coding standards)
├── orchestrator/     # KB for system-level reasoning, memory, and task distribution
├── prd/              # KB for product requirements and templates
├── diagrammer/       # KB for architecture patterns and Mermaid syntax
├── backend/          # KB for API standards, framework guides, and security
├── frontend/         # KB for UI/UX patterns, framework guides, and accessibility
└── qa/               # KB for testing frameworks, patterns, and quality metrics
```

**Action:** Populate these folders with the relevant documentation, templates, and guides you identified in your `knowledgebaseguide.md`.

### 1.2 IntentParser File Setup

Set up the files for the new initial agent.

| File Path | Purpose | Status |
| :--- | :--- | :--- |
| `agents/schema/project_intent_schema.json` | Defines the structured output contract for the `IntentParser`. | **New File** (Content provided in previous discussion) |
| `agents/subagents/intent_parser.py` | Contains the Python logic for the agent, using an LLM with JSON mode. | **New File** (Content provided in previous discussion) |
| `agents/prompts/intent_parser.md` | The mission prompt for the `IntentParser` agent. | **New File** (Content provided in previous discussion) |

## Phase 2: Core Agent Implementation and Orchestrator Update

This phase focuses on integrating the `IntentParser` and updating the Orchestrator to use the new structured input.

### 2.1 Implement the IntentParser Agent

Follow the steps in the `intent_parser_integration_guide.md` to implement the agent's logic and schema.

**Key Action:** Ensure the `run_intent_parser` function successfully takes the `raw_user_request` from the LangGraph state and returns the structured JSON object under the key `parsed_intent`.

### 2.2 Update the Orchestrator (`agents/orchestrator.py`)

The Orchestrator must be modified to:

1.  **Set Entry Point:** Change the graph's entry point to the new `"intent_parser"` node.
2.  **Define Initial State:** Ensure the initial state passed to the graph contains the raw user input under the key `raw_user_request`.
3.  **Update Subagent Inputs:** Modify all subsequent subagents (PRD, Diagrammer, Backend, etc.) to **read their primary instructions from the structured `state['parsed_intent']`** instead of the raw, unstructured user request.

**Example PRD Agent Logic Update:**

```python
# OLD: prd_agent_logic(state['raw_user_request'])
# NEW: prd_agent_logic(state['parsed_intent']['project_description'], state['parsed_intent']['required_features'])
```

## Phase 3: RAG System Integration (Domain-Specific Retrieval)

This phase implements the core concept from your `knowledgebaseguide.md`: providing each agent with its own domain-specific knowledge base.

### 3.1 RAG System Refactoring

Your existing RAG system must be refactored to support **scoped retrieval**.

1.  **Indexing:** When documents are ingested, they must be tagged with their domain (e.g., `prd`, `backend`, `shared`).
2.  **Retrieval Logic:** Create a new utility function, e.g., `retrieve_knowledge(query, agent_domain)`. This function will query the vector store, filtering results to include only documents tagged with the specific `agent_domain` (e.g., `backend`) and the universal `shared` domain.

### 3.2 Agent Prompt Update

Modify the mission prompt for each subagent to explicitly instruct it to use its domain-specific knowledge.

**Example Backend Agent Mission Prompt Update:**

> "You are the Backend Agent. Your task is to scaffold the API endpoints. **Before generating code, you MUST use your RAG tool to retrieve context from the `backend` and `shared` knowledge bases** using the structured requirements provided by the Orchestrator. Adhere strictly to the API standards found in your retrieved context."

### 3.3 Agent Execution Logic Update

The Python code for each subagent (e.g., `agents/subagents/backend.py`) must be updated to include a step where it calls the new scoped retrieval function and injects the retrieved context into the LLM prompt.

```python
# Inside run_backend_agent(inputs):
# 1. Extract structured requirements from inputs
requirements = inputs['parsed_intent']['required_features']
# 2. Retrieve scoped knowledge
context = retrieve_knowledge(requirements, "backend")
# 3. Construct the final prompt
final_prompt = f"Mission: {backend_mission_prompt}\n\nRequirements: {requirements}\n\nKnowledge Context:\n{context}"
# 4. Call the LLM
# ...
```

## Phase 4: Generalist Capabilities Roadmap

To evolve your system into a complete, general-purpose agent, you must integrate the external-facing capabilities discussed previously. These should be implemented as new, high-level **Tools** that the Orchestrator can call.

| Capability | New Tool/Agent | Architectural Requirement |
| :--- | :--- | :--- |
| **Live Web Interaction** | `BrowserTool` | Integration with a headless browser (Playwright/Selenium) to perform live navigation, scraping, and transactional tasks. |
| **Media Generation** | `MediaTool` | API wrappers for image/audio generation services (e.g., DALL-E, Stability AI) to create project assets. |
| **Data Analysis** | `DataAnalysisTool` | A sandboxed Python environment with Pandas/Matplotlib exposed as a tool for ad-hoc data processing and visualization. |
| **Scheduling/Automation** | `SchedulerTool` | Integration with a job scheduler (e.g., Celery Beat, Cron) to enable time-based and recurring task execution. |
| **Professional Output** | `DocumentTool` | Utilities for converting Markdown/HTML into final-form documents (PPTX, PDF) for stakeholders. |

**Action:** Define the function signatures for these new tools and integrate them into your **MCP Tool Configuration** (`.cursor/mcp.json`). The Orchestrator can then be updated to use a **Tool-Calling Router** to decide whether to dispatch to a subagent (for code building) or to one of these new generalist tools (for external tasks).

By following this unified plan, you will successfully transition your system from a specialized code-building engine to a robust, multi-agent intelligence network with domain-specific RAG and a clear path to becoming a complete, general-purpose autonomous agent.
