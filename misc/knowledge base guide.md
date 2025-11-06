# Comprehensive Knowledge Base Sources for Each Agent

Based on each agent's specific function, here are the best sources of documentation and information to maximize their performance:

## 1. PRD Agent (Product Requirements Documents)

**Primary Function**: Draft clear, actionable product requirements and MVP summaries

### Best Documentation Sources:

**Product Management Resources:**
- **Lean Canvas & Business Model Canvas templates** - Helps structure problem/solution fit
- **User Story formats** (As a [user], I want [goal], so that [benefit])
- **Acceptance criteria templates** (Given/When/Then format)
- **PRD templates from top companies** (Google, Amazon, Atlassian PRD formats)

**Specific Documents to Ingest:**
- Sample PRDs for similar products/features
- Product requirement checklists
- Feature prioritization frameworks (MoSCoW, RICE)
- Scope definition guidelines
- Technical feasibility assessment templates
- Success metrics and KPI definitions
- User persona templates

**Recommended Sources:**
- Product School PRD templates
- Atlassian's product requirements documentation
- Pragmatic Institute resources
- Your own completed, successful PRDs
- docs/prd.md (your template)
- docs/tasks.md (task breakdown structure)

---

## 2. Diagrammer Agent (Architecture Diagrams)

**Primary Function**: Create clear Mermaid architecture and system design diagrams

### Best Documentation Sources:

**Architecture Patterns:**
- **Mermaid syntax documentation** (official Mermaid.js docs)
- **System design patterns** (Microservices, MVC, MVVM, Event-Driven, etc.)
- **Cloud architecture diagrams** (AWS, Azure, GCP reference architectures)
- **Database design patterns** (Relational, NoSQL, graph database schemas)

**Specific Documents to Ingest:**
- Complete Mermaid diagram examples (flowcharts, sequence diagrams, ER diagrams, class diagrams)
- Your existing architecture diagrams (docs/architecture.mmd)
- System boundary definitions
- Component interaction patterns
- Data flow diagram examples
- Infrastructure as code diagrams
- Network topology diagrams

**Recommended Sources:**
- Mermaid official documentation (https://mermaid.js.org/)
- C4 Model documentation (Context, Container, Component, Code)
- Martin Fowler's architecture patterns
- System Design Primer on GitHub
- Your approved architecture reviews

---

## 3. Backend Agent (Server-Side Development)

**Primary Function**: Scaffold and modify backend endpoints, business logic, and data layers

### Best Documentation Sources:

**Framework-Specific Documentation:**
- **API design standards** (REST, GraphQL best practices)
- **Framework documentation** (Flask, FastAPI, Django, Express.js - whatever you use)
- **Database patterns** (ORM usage, query optimization, migrations)
- **Authentication/Authorization** (JWT, OAuth2, session management)

**Specific Documents to Ingest:**
- Your successful endpoint implementations
- API versioning strategies
- Error handling patterns
- Middleware examples
- Database schema definitions
- Service layer patterns
- Dependency injection examples
- Configuration management patterns
- Environment variable standards

**Recommended Sources:**
- Official framework documentation
- GitHub repos with 10k+ stars using your stack
- Your .cursor/rules.md (coding standards)
- OpenAPI/Swagger specification examples
- Twelve-Factor App methodology
- API security best practices (OWASP)
- Your existing backend codebase patterns

---

## 4. Frontend Agent (UI/UX Components)

**Primary Function**: Build and modify user interface components and client-side logic

### Best Documentation Sources:

**Framework & Library Documentation:**
- **Component library documentation** (Material-UI, Ant Design, Tailwind, Bootstrap)
- **Framework guides** (React, Vue, Angular - whatever you use)
- **State management patterns** (Redux, Zustand, Context API, Pinia)
- **Accessibility standards** (WCAG guidelines, ARIA patterns)

**Specific Documents to Ingest:**
- Your successful component implementations
- Component composition patterns
- Form validation patterns
- Routing configurations
- API integration patterns (fetch, axios, React Query)
- Error boundary implementations
- Loading state patterns
- Responsive design breakpoints
- CSS/Styling conventions (CSS modules, styled-components, Tailwind patterns)

**Recommended Sources:**
- Official framework documentation
- Component library storybooks
- Your design system documentation
- Accessibility guidelines (a11y project)
- Performance optimization guides (Core Web Vitals)
- Your .cursor/rules.md (frontend standards)
- Popular GitHub repos showcasing best practices

---

## 5. Parser Agent (Requirement Extraction)

**Primary Function**: Convert unstructured text into structured JSON requirements

### Best Documentation Sources:

**Data Extraction Patterns:**
- **JSON schema definitions** (JSON Schema specification)
- **NLP extraction patterns** (entity recognition, relationship extraction)
- **Requirement parsing examples** (text → structured data transformations)
- **Output format specifications** (your desired JSON structure)

**Specific Documents to Ingest:**
- RAG_MCP_GUIDE.md (configuration for document-to-code extraction)
- Input/output example pairs (unstructured text → resulting JSON)
- Feature extraction rules
- Dependency identification patterns
- Tech stack inference rules
- Ambiguity resolution guidelines
- Validation rules for extracted data
- Edge case handling examples

**Recommended Sources:**
- JSON Schema documentation
- Your requirement templates
- Examples of well-structured vs. poorly-structured requirements
- Natural language processing guides for entity extraction
- Your existing parsed requirement examples

---

## 6. Code Agent (General Code Generation)

**Primary Function**: Generate complete project code using requirements and patterns

### Best Documentation Sources:

**Code Generation Patterns:**
- **Project scaffolding templates** (cookiecutter templates, yeoman generators)
- **Boilerplate code** (starter templates for your tech stack)
- **Code organization patterns** (folder structure, module organization)
- **Best practices guides** (language-specific idioms)

**Specific Documents to Ingest:**
- Your complete, working project examples
- File structure conventions
- Naming conventions (files, functions, variables, classes)
- Import/export patterns
- Configuration file templates (package.json, requirements.txt, etc.)
- Docker/containerization templates
- CI/CD pipeline configurations
- Documentation generation patterns (docstrings, JSDoc)

**Recommended Sources:**
- GitHub "awesome" lists for your stack
- Official language style guides (PEP 8 for Python, Airbnb for JavaScript)
- Your .cursor/rules.md
- Project structure best practices
- Design pattern implementations (Gang of Four patterns)

---

## 7. Debug Agent (Error Analysis & Fixing)

**Primary Function**: Analyze errors, classify them, and propose fixes using learned solutions

### Best Documentation Sources:

**Error Resolution Patterns:**
- **Common error messages** and their solutions
- **Stack trace interpretation guides**
- **Debugging methodologies** (rubber duck debugging, binary search debugging)
- **Error classification taxonomies** (syntax, runtime, logical, configuration)

**Specific Documents to Ingest:**
- **Automatically saved**: Successful fix solutions (the agent learns from these)
- Common error patterns by framework/language
- Dependency conflict resolution guides
- Environment configuration issues
- Version compatibility matrices
- Memory leak debugging patterns
- Performance profiling guides
- Security vulnerability fixes
- Stack Overflow top answers for common errors

**Recommended Sources:**
- docs/LEARNING_MEMORY_GUIDE.md (implementation details)
- Error logs from your CI/CD pipeline
- GitHub issue resolutions from popular repos
- Official troubleshooting guides for your stack
- Common gotchas documentation
- Migration guides (when upgrading versions)

---

## 8. QA Agent (Testing & Quality Assurance)

**Primary Function**: Perform quality checks, write tests, and validate code quality

### Best Documentation Sources:

**Testing Frameworks & Patterns:**
- **Testing framework documentation** (pytest, Jest, Mocha, JUnit)
- **Test pattern guides** (unit, integration, e2e testing strategies)
- **Code coverage standards**
- **Quality metrics** (cyclomatic complexity, maintainability index)

**Specific Documents to Ingest:**
- Your existing test files (tests/test_sanity.py)
- Test naming conventions
- Mock/stub patterns
- Fixture setup patterns
- Assertion best practices
- CI/CD workflow definitions (.github/workflows/ci.yml)
- Code review checklists
- Definition of Done criteria
- Performance testing patterns
- Security testing guidelines

**Recommended Sources:**
- Testing library documentation
- Test pyramid concepts
- Behavior-Driven Development (BDD) examples
- Testing best practices (AAA pattern: Arrange, Act, Assert)
- Code quality tool configurations (ESLint, Pylint, SonarQube)
- Your quality gates and acceptance criteria

---

## Universal Sources for All Agents

These should be ingested for the entire knowledge base:

### Project-Specific:
1. **.cursor/rules.md** - Your project coding standards and guidelines
2. **README.md** - Project overview and conventions
3. **CONTRIBUTING.md** - Development workflow and standards
4. **Your git commit history** - Successful implementations and evolution

### Industry Standards:
5. **SOLID principles** documentation
6. **DRY (Don't Repeat Yourself)** examples
7. **KISS (Keep It Simple, Stupid)** guidelines
8. **Security best practices** (OWASP Top 10)
9. **Performance optimization** guides
10. **Code review best practices**

---

## Implementation Priority

### Phase 1 (Immediate Impact):
1. Your existing successful code (highest relevance)
2. Project-specific standards (.cursor/rules.md)
3. Framework official documentation

### Phase 2 (Quality Enhancement):
4. Curated GitHub examples
5. Design pattern implementations
6. Testing patterns

### Phase 3 (Continuous Improvement):
7. Learned solutions (automatic from Debug Agent)
8. Project evolution documentation
9. Team retrospective insights

---

## Ingestion Script Structure

When creating your ingestion pipeline, organize by agent specialty:

```
knowledge_base/
├── prd_agent/
│   ├── templates/
│   ├── examples/
│   └── guidelines/
├── backend_agent/
│   ├── api_patterns/
│   ├── database_patterns/
│   └── security_patterns/
├── frontend_agent/
│   ├── component_patterns/
│   ├── state_management/
│   └── styling_patterns/
├── debug_agent/
│   ├── common_errors/
│   └── learned_solutions/ (auto-populated)
└── shared/
    ├── coding_standards/
    └── best_practices/
```

This organizational structure will help you maintain and update the knowledge base as your project evolves and the agents learn from successful executions.

Perfect question — this is **exactly** the kind of thinking that turns your Orchestrator system into a real *multi-agent intelligence network*.

Let’s go step-by-step so you can design a **Knowledge Base (KB)** architecture that each agent can tap into for its own domain expertise.

---

## 🧠 OVERVIEW: What the KB Is For

Each agent should have its own **domain-specific knowledge base**, containing the *minimal but most powerful context* it needs to perform autonomously and accurately — without bloating memory or slowing reasoning.

You can think of it as:

```
docs/
├─ shared/        → global guides (coding, formatting, workflow)
├─ prd/           → product management & requirements
├─ diagrammer/    → systems design & architecture
├─ backend/       → API, database, Python, FastAPI, etc.
├─ frontend/      → React, Tailwind, UX standards
├─ qa/            → testing, verification, coverage
└─ orchestrator/  → reasoning, coordination, memory
```

Each folder = 1 agent’s KB
Each agent’s prompt = a **mission** + “You may consult docs in `/docs/<agent>/` and `/docs/shared/`.”

---

## 🧩 1. Orchestrator Agent KB

**Purpose:** System-level reasoning, memory, and task distribution.

| Category                          | Source                                                                                                                                                                                                   | Why                                                           |
| --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| **Architecture reasoning**        | `docs/architecture.mmd` + [LangChain docs: Agents, Tools, Memory](https://python.langchain.com/docs/modules/agents/)                                                                                     | Helps orchestrator know how to compose agents into workflows. |
| **Prompt design best practices**  | [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering), [Anthropic Prompting Principles](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering) | Improves dispatching quality and clarity in task creation.    |
| **Memory & context strategies**   | `docs/LEARNING_MEMORY_GUIDE.md`, [LangGraph docs](https://python.langchain.com/docs/langgraph)                                                                                                           | Teaches orchestration of persistent context between agents.   |
| **Agent governance & evaluation** | `docs/agent_governance.md` (create if missing)                                                                                                                                                           | Keeps Orchestrator’s coordination structured and auditable.   |

**Add to KB:**
`docs/orchestrator/agent_basics.md`, `docs/orchestrator/prompt_structure.md`, and external links on orchestration theory (LangGraph, CrewAI, AutoGPT papers).

---

## 📄 2. PRD Agent KB

**Purpose:** Convert abstract ideas into clear product requirements.

| Category             | Source                                                                                                                                                                                                                    | Why                                             |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| **Templates**        | `docs/prd.md`, example PRDs from your previous projects                                                                                                                                                                   | Keeps outputs structured & consistent.          |
| **Best practices**   | [Atlassian Product Requirements Docs](https://www.atlassian.com/agile/product-management/requirements), [Google Design Docs Guide](https://github.com/google/eng-practices/blob/master/review/development/design-docs.md) | Shows what good PRDs look like.                 |
| **Product thinking** | [Reforge articles on product strategy](https://www.reforge.com/blog), [Intercom’s blog](https://www.intercom.com/blog/product-management/)                                                                                | Improves decision rationale and prioritization. |

**Add to KB:**
`docs/prd/examples/` folder with 2–3 exemplary PRDs (e.g., “Create Wave Picking Dashboard”, “RF Scanner App”)
Include a one-pager on “How to define scope, constraints, and metrics.”

---

## 🧭 3. Diagrammer Agent KB

**Purpose:** Translate PRD and architecture into visual, logical diagrams.

| Category                  | Source                                                                                   | Why                                                                    |
| ------------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| **Diagram standards**     | [Mermaid official docs](https://mermaid.js.org/syntax/flowchart.html)                    | Enables precise diagram generation syntax.                             |
| **Architecture patterns** | [Software Architecture Patterns (Martin Fowler)](https://martinfowler.com/architecture/) | Helps diagram high-quality modular systems.                            |
| **Examples**              | `docs/architecture.mmd`, plus any `.mmd` diagrams from other repos                       | Builds a visual “vocabulary” for common components (backend, API, DB). |

**Add to KB:**
`docs/diagrammer/mermaid_templates.md` (e.g., flowchart, class, sequence, component diagrams).
`docs/diagrammer/common_patterns.md` (e.g., microservices, REST, event-driven).

---

## ⚙️ 4. Backend Agent KB

**Purpose:** Implement logic, APIs, and integration based on PRD.

| Category                | Source                                                                                                                                                                                       | Why                                       |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| **Your coding stack**   | `/agents/subagents/backend.py`, plus any `/src/` code it touches                                                                                                                             | Serves as example structure.              |
| **Framework guides**    | [FastAPI Docs](https://fastapi.tiangolo.com/), [SQLAlchemy](https://docs.sqlalchemy.org/), [pandas](https://pandas.pydata.org/docs/), [requests](https://requests.readthedocs.io/en/latest/) | These are your most-used backend tools.   |
| **Testing & structure** | [12-Factor App Principles](https://12factor.net/), [Python Project Structure](https://docs.python-guide.org/writing/structure/)                                                              | Reinforces best-practice backend layouts. |
| **Security / Env**      | `.env.template` + [OWASP API Security Top 10](https://owasp.org/API-Security/)                                                                                                               | Protects keys & secrets.                  |

**Add to KB:**
`docs/backend/api_standards.md`, `docs/backend/error_handling.md`, `docs/backend/examples/`.

---

## 🎨 5. Frontend Agent KB

**Purpose:** Generate clean, consistent UI/UX components.

| Category                 | Source                                                                                                                                           | Why                          |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------- |
| **Framework docs**       | [React Docs](https://react.dev/), [TailwindCSS](https://tailwindcss.com/docs/), [Shadcn UI](https://ui.shadcn.com/docs)                          | Aligns code with your stack. |
| **UI system reference**  | `.cursor/rules.md` and `/frontend/` code samples                                                                                                 | Maintains style consistency. |
| **UX design principles** | [Nielsen Norman Group](https://www.nngroup.com/articles/ten-usability-heuristics/), [Google Material Design Guidelines](https://m3.material.io/) | Encourages good UX logic.    |

**Add to KB:**
`docs/frontend/component_patterns.md`, `docs/frontend/interaction_rules.md`, and screenshots or mockups (optional).

---

## 🧪 6. QA Agent KB

**Purpose:** Validate all deliverables against PRD and system expectations.

| Category                | Source                                                                              | Why                                    |
| ----------------------- | ----------------------------------------------------------------------------------- | -------------------------------------- |
| **Internal guides**     | `docs/TESTING_GUIDE.md`, `docs/VERIFICATION.md`                                     | Define testing structure and coverage. |
| **Framework docs**      | [pytest](https://docs.pytest.org/), [Playwright](https://playwright.dev/docs/intro) | Tools for automated testing.           |
| **Acceptance criteria** | PRDs + feature specs                                                                | Ensures alignment with requirements.   |

**Add to KB:**
`docs/qa/test_cases_examples.md` and `docs/qa/checklists.md` (integration, regression, UI).

---

## 🪄 Implementation Options

You can give each agent an **RAG (Retrieval-Augmented Generation)** source:

* Store Markdown docs in `docs/<agent>/`
* Use local embeddings (e.g., with `chromadb`, `faiss`, or LangChain’s `VectorStore`)
* When an agent runs, it loads its relevant docs as context snippets
* Or store as structured “memory entries” (short paragraphs with metadata: source, tags, last_updated)

Example for PRD agent:

```python
agent_knowledge = KnowledgeBase(folder="docs/prd/")
context = agent_knowledge.retrieve("drafting metrics section")
prompt = f"{mission_prompt}\n\nRelevant context:\n{context}"
```

---

## 🔄 7. Shared Knowledge Base (Global Context)

All agents should also have read-access to a `docs/shared/` folder with:

* `cursor_rules.md` (code conventions)
* `naming_conventions.md`
* `file_structure.md`
* `communication_protocols.md`
* `memory_handling.md` (how to pass state between agents)

---

## ✅ Summary

| Agent            | Knowledge Focus                 | Key Docs / Sources                     |
| ---------------- | ------------------------------- | -------------------------------------- |
| **Orchestrator** | Coordination, reasoning, memory | LangChain/Graph docs, memory guide     |
| **PRD**          | Product writing, user stories   | Atlassian, Google design docs          |
| **Diagrammer**   | System architecture             | Mermaid docs, patterns                 |
| **Backend**      | API, data, logic                | FastAPI, SQLAlchemy, OWASP             |
| **Frontend**     | UI/UX components                | React, Tailwind, shadcn                |
| **QA**           | Testing & validation            | pytest, Playwright, verification guide |

---

Perfect question — this is **exactly** the kind of thinking that turns your Orchestrator system into a real *multi-agent intelligence network*.

Let’s go step-by-step so you can design a **Knowledge Base (KB)** architecture that each agent can tap into for its own domain expertise.

---

## 🧠 OVERVIEW: What the KB Is For

Each agent should have its own **domain-specific knowledge base**, containing the *minimal but most powerful context* it needs to perform autonomously and accurately — without bloating memory or slowing reasoning.

You can think of it as:

```
docs/
├─ shared/        → global guides (coding, formatting, workflow)
├─ prd/           → product management & requirements
├─ diagrammer/    → systems design & architecture
├─ backend/       → API, database, Python, FastAPI, etc.
├─ frontend/      → React, Tailwind, UX standards
├─ qa/            → testing, verification, coverage
└─ orchestrator/  → reasoning, coordination, memory
```

Each folder = 1 agent’s KB
Each agent’s prompt = a **mission** + “You may consult docs in `/docs/<agent>/` and `/docs/shared/`.”

---

## 🧩 1. Orchestrator Agent KB

**Purpose:** System-level reasoning, memory, and task distribution.

| Category                          | Source                                                                                                                                                                                                   | Why                                                           |
| --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| **Architecture reasoning**        | `docs/architecture.mmd` + [LangChain docs: Agents, Tools, Memory](https://python.langchain.com/docs/modules/agents/)                                                                                     | Helps orchestrator know how to compose agents into workflows. |
| **Prompt design best practices**  | [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering), [Anthropic Prompting Principles](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering) | Improves dispatching quality and clarity in task creation.    |
| **Memory & context strategies**   | `docs/LEARNING_MEMORY_GUIDE.md`, [LangGraph docs](https://python.langchain.com/docs/langgraph)                                                                                                           | Teaches orchestration of persistent context between agents.   |
| **Agent governance & evaluation** | `docs/agent_governance.md` (create if missing)                                                                                                                                                           | Keeps Orchestrator’s coordination structured and auditable.   |

**Add to KB:**
`docs/orchestrator/agent_basics.md`, `docs/orchestrator/prompt_structure.md`, and external links on orchestration theory (LangGraph, CrewAI, AutoGPT papers).

---

## 📄 2. PRD Agent KB

**Purpose:** Convert abstract ideas into clear product requirements.

| Category             | Source                                                                                                                                                                                                                    | Why                                             |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| **Templates**        | `docs/prd.md`, example PRDs from your previous projects                                                                                                                                                                   | Keeps outputs structured & consistent.          |
| **Best practices**   | [Atlassian Product Requirements Docs](https://www.atlassian.com/agile/product-management/requirements), [Google Design Docs Guide](https://github.com/google/eng-practices/blob/master/review/development/design-docs.md) | Shows what good PRDs look like.                 |
| **Product thinking** | [Reforge articles on product strategy](https://www.reforge.com/blog), [Intercom’s blog](https://www.intercom.com/blog/product-management/)                                                                                | Improves decision rationale and prioritization. |

**Add to KB:**
`docs/prd/examples/` folder with 2–3 exemplary PRDs (e.g., “Create Wave Picking Dashboard”, “RF Scanner App”)
Include a one-pager on “How to define scope, constraints, and metrics.”

---

## 🧭 3. Diagrammer Agent KB

**Purpose:** Translate PRD and architecture into visual, logical diagrams.

| Category                  | Source                                                                                   | Why                                                                    |
| ------------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| **Diagram standards**     | [Mermaid official docs](https://mermaid.js.org/syntax/flowchart.html)                    | Enables precise diagram generation syntax.                             |
| **Architecture patterns** | [Software Architecture Patterns (Martin Fowler)](https://martinfowler.com/architecture/) | Helps diagram high-quality modular systems.                            |
| **Examples**              | `docs/architecture.mmd`, plus any `.mmd` diagrams from other repos                       | Builds a visual “vocabulary” for common components (backend, API, DB). |

**Add to KB:**
`docs/diagrammer/mermaid_templates.md` (e.g., flowchart, class, sequence, component diagrams).
`docs/diagrammer/common_patterns.md` (e.g., microservices, REST, event-driven).

---

## ⚙️ 4. Backend Agent KB

**Purpose:** Implement logic, APIs, and integration based on PRD.

| Category                | Source                                                                                                                                                                                       | Why                                       |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| **Your coding stack**   | `/agents/subagents/backend.py`, plus any `/src/` code it touches                                                                                                                             | Serves as example structure.              |
| **Framework guides**    | [FastAPI Docs](https://fastapi.tiangolo.com/), [SQLAlchemy](https://docs.sqlalchemy.org/), [pandas](https://pandas.pydata.org/docs/), [requests](https://requests.readthedocs.io/en/latest/) | These are your most-used backend tools.   |
| **Testing & structure** | [12-Factor App Principles](https://12factor.net/), [Python Project Structure](https://docs.python-guide.org/writing/structure/)                                                              | Reinforces best-practice backend layouts. |
| **Security / Env**      | `.env.template` + [OWASP API Security Top 10](https://owasp.org/API-Security/)                                                                                                               | Protects keys & secrets.                  |

**Add to KB:**
`docs/backend/api_standards.md`, `docs/backend/error_handling.md`, `docs/backend/examples/`.

---

## 🎨 5. Frontend Agent KB

**Purpose:** Generate clean, consistent UI/UX components.

| Category                 | Source                                                                                                                                           | Why                          |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------- |
| **Framework docs**       | [React Docs](https://react.dev/), [TailwindCSS](https://tailwindcss.com/docs/), [Shadcn UI](https://ui.shadcn.com/docs)                          | Aligns code with your stack. |
| **UI system reference**  | `.cursor/rules.md` and `/frontend/` code samples                                                                                                 | Maintains style consistency. |
| **UX design principles** | [Nielsen Norman Group](https://www.nngroup.com/articles/ten-usability-heuristics/), [Google Material Design Guidelines](https://m3.material.io/) | Encourages good UX logic.    |

**Add to KB:**
`docs/frontend/component_patterns.md`, `docs/frontend/interaction_rules.md`, and screenshots or mockups (optional).

---

## 🧪 6. QA Agent KB

**Purpose:** Validate all deliverables against PRD and system expectations.

| Category                | Source                                                                              | Why                                    |
| ----------------------- | ----------------------------------------------------------------------------------- | -------------------------------------- |
| **Internal guides**     | `docs/TESTING_GUIDE.md`, `docs/VERIFICATION.md`                                     | Define testing structure and coverage. |
| **Framework docs**      | [pytest](https://docs.pytest.org/), [Playwright](https://playwright.dev/docs/intro) | Tools for automated testing.           |
| **Acceptance criteria** | PRDs + feature specs                                                                | Ensures alignment with requirements.   |

**Add to KB:**
`docs/qa/test_cases_examples.md` and `docs/qa/checklists.md` (integration, regression, UI).

---

## 🪄 Implementation Options

You can give each agent an **RAG (Retrieval-Augmented Generation)** source:

* Store Markdown docs in `docs/<agent>/`
* Use local embeddings (e.g., with `chromadb`, `faiss`, or LangChain’s `VectorStore`)
* When an agent runs, it loads its relevant docs as context snippets
* Or store as structured “memory entries” (short paragraphs with metadata: source, tags, last_updated)

Example for PRD agent:

```python
agent_knowledge = KnowledgeBase(folder="docs/prd/")
context = agent_knowledge.retrieve("drafting metrics section")
prompt = f"{mission_prompt}\n\nRelevant context:\n{context}"
```

---

## 🔄 7. Shared Knowledge Base (Global Context)

All agents should also have read-access to a `docs/shared/` folder with:

* `cursor_rules.md` (code conventions)
* `naming_conventions.md`
* `file_structure.md`
* `communication_protocols.md`
* `memory_handling.md` (how to pass state between agents)

---

## ✅ Summary

| Agent            | Knowledge Focus                 | Key Docs / Sources                     |
| ---------------- | ------------------------------- | -------------------------------------- |
| **Orchestrator** | Coordination, reasoning, memory | LangChain/Graph docs, memory guide     |
| **PRD**          | Product writing, user stories   | Atlassian, Google design docs          |
| **Diagrammer**   | System architecture             | Mermaid docs, patterns                 |
| **Backend**      | API, data, logic                | FastAPI, SQLAlchemy, OWASP             |
| **Frontend**     | UI/UX components                | React, Tailwind, shadcn                |
| **QA**           | Testing & validation            | pytest, Playwright, verification guide |

---

