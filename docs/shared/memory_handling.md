# Memory Handling Between Agents

## State Passing

Agents pass data through the LangGraph state dictionary. Key principles:

1. **Structured Input**: Use `parsed_intent` from IntentParser
2. **Additive Updates**: Agents add to state, don't replace
3. **Namespacing**: Use clear keys (e.g., `prd_output`, `backend_output`)

## Memory Keys

- `raw_user_request`: Original input
- `parsed_intent`: Structured intent
- `<agent>_output`: Agent-specific results
- `learning_memory`: Persistent knowledge storage

## RAG Context

- Each agent retrieves its domain-specific knowledge
- Knowledge is not stored in state (retrieved on-demand)
- Shared knowledge base accessible to all agents

## Learning Memory

The system maintains learning memory for:
- Error solutions
- Successful patterns
- Agent context history

Accessed through `LearningMemory` class, not state dictionary.

