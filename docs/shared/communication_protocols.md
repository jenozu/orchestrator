# Inter-Agent Communication Protocols

## State Management

Agents communicate through the LangGraph state dictionary:

- `raw_user_request`: Original user input
- `parsed_intent`: Structured intent from IntentParser
- `parsed_intent.project_description`: Project description
- `parsed_intent.required_features`: List of required features

## Data Flow

1. IntentParser processes `raw_user_request` → creates `parsed_intent`
2. Subsequent agents read from `parsed_intent` for structured requirements
3. Agents write results to state for next agents
4. Each agent adds its output with a unique key

## Error Handling

- Return error messages in state if agent fails
- Include `status` and `error` keys in agent outputs
- Log errors for debugging but return gracefully

## Output Format

All agents should return dictionaries with:
- `status`: Task completion status
- Relevant output data
- `knowledge_retrieved`: Boolean indicating if RAG was used
- `context_length`: Length of retrieved context

