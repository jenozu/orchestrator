# Agent Basics

## Agent Architecture

Agents are autonomous components that:
1. Receive structured input from Orchestrator
2. Retrieve domain-specific knowledge via RAG
3. Process tasks using LLM
4. Return structured outputs

## Agent Types

- **IntentParser**: Parses user requests into structured JSON
- **PRD Agent**: Drafts product requirements
- **Diagrammer Agent**: Creates architecture diagrams
- **Backend Agent**: Scaffolds backend code
- **Frontend Agent**: Scaffolds frontend code
- **QA Agent**: Validates deliverables

## Agent Lifecycle

1. Receive state from Orchestrator
2. Extract requirements from `parsed_intent`
3. Retrieve knowledge from domain KB
4. Execute task (generate code, create PRD, etc.)
5. Return results to state

## Best Practices

- Always use `parsed_intent` for structured requirements
- Retrieve knowledge before processing
- Log important decisions
- Return clear status and error messages

