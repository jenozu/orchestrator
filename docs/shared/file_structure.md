# File Structure Guidelines

## Project Organization

```
orchestrator/
├── agents/              # Agent implementations
│   ├── subagents/      # Individual agent logic
│   ├── prompts/        # Agent mission prompts
│   └── schema/         # Data schemas
├── docs/               # Documentation
│   ├── <agent>/        # Agent-specific KB
│   └── shared/         # Shared knowledge
├── mcp_codegen/        # MCP server code
└── tests/              # Test files
```

## Code Organization

- One class/function per logical concept
- Group related functionality together
- Separate concerns (business logic, data access, presentation)

## Documentation

- Keep README files up to date
- Document public APIs
- Include examples in docstrings

