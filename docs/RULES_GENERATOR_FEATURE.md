# Rules and Task Generator Feature

## Overview

The Rules and Task Generator is a powerful feature that automatically generates two critical project files based on structured input from the `IntentParser`:

1. **Project Rules** (`.cursor/rules.md`): A project-specific rules document for AI agents to follow
2. **Master Task List** (`docs/tasks.md`): A sequential, checklist-style task list for project execution

## Architecture

### Flow Diagram

```
User Request
    ↓
IntentParser (parses raw request → structured JSON)
    ↓
RulesGenerator (generates rules.md & tasks.md)
    ↓
PRD Agent (reads rules & tasks, generates PRD)
    ↓
Other Agents (Backend, Frontend, QA, etc.)
```

### Components

#### 1. Rules Generator Agent (`agents/subagents/rules_generator.py`)

**Responsibilities:**
- Receives structured project intent from IntentParser
- Generates project-specific rules using OpenAI API
- Generates master task list using OpenAI API
- Writes both files to designated locations

**System Prompts:**
- **Rules Prompt**: Generates coding standards, security practices, documentation requirements
- **Task List Prompt**: Converts features into sequential, actionable tasks

**Output:**
- `.cursor/rules.md`: Project rules for all agents
- `docs/tasks.md`: Master task checklist

#### 2. Orchestrator Integration (`agents/orchestrator.py`)

**Graph Structure:**
```python
intent_parser -> rules_generator -> prd_agent -> END
```

**State Updates:**
- `rules_generated`: Boolean flag
- `rules_path`: Path to generated rules file
- `task_list_path`: Path to generated task list
- `parsed_intent`: Passed through the chain

#### 3. Agent Prompt Updates

All agent prompts now include a "Project Rules and Task List" section:

**PRD Agent (`agents/prompts/prd.md`):**
- Must read `.cursor/rules.md` before drafting
- Must consult `docs/tasks.md` for task planning
- Must follow project-specific standards

**Backend/Frontend/QA Agents:**
- Must read rules before implementing
- Must identify next uncompleted task from task list
- Must follow coding standards from rules

## Generated Files

### `.cursor/rules.md`

**Content:**
- Coding standards (technology-specific)
- Security best practices
- Documentation requirements
- Quality and testing expectations
- Naming conventions
- Error handling guidelines
- File organization standards

**Example Structure:**
```markdown
# Project Rules

## Coding Standards
- Use TypeScript strict mode
- Follow React best practices
...

## Security
- Sanitize all user inputs
- Use environment variables for secrets
...

## Documentation
- Document all public APIs
- Maintain up-to-date README
...
```

### `docs/tasks.md`

**Content:**
- Sequential task list in Markdown checklist format
- Organized by project phase (Setup → PRD → Backend → Frontend → QA)
- Each task is clear, actionable, and testable

**Example Structure:**
```markdown
# Master Task List

## Setup & Planning
- [ ] Create project structure
- [ ] Set up development environment
- [ ] Draft Product Requirements Document (PRD)

## Backend Development
- [ ] Implement user authentication endpoints
- [ ] Create task CRUD endpoints
- [ ] Set up database schema
...

## Frontend Development
- [ ] Create login/signup components
- [ ] Build task dashboard
...

## Testing & QA
- [ ] Write unit tests for backend
- [ ] Perform end-to-end testing
...
```

## Usage

### Running the Feature

1. **Prepare a user request:**
```python
user_request = """
I need a task management web app with:
- User authentication
- Task CRUD operations
- Task prioritization
Tech stack: React, FastAPI, PostgreSQL
"""
```

2. **Initialize and run orchestrator:**
```python
from agents.orchestrator import Orchestrator

orchestrator = Orchestrator()
orchestrator.build_graph()

result = orchestrator.run_once({
    "raw_user_request": user_request
})
```

3. **Check generated files:**
```python
from pathlib import Path

rules_path = Path(".cursor/rules.md")
tasks_path = Path("docs/tasks.md")

if rules_path.exists():
    print("✅ Rules generated")
    
if tasks_path.exists():
    print("✅ Tasks generated")
```

### Testing

Run the test script:
```bash
python test_rules_generator.py
```

This script will:
- Run the complete workflow
- Display generated content
- Verify files were created
- Show state updates

## Benefits

### 1. **Consistency**
All agents follow the same project-specific rules, ensuring consistent code quality and standards.

### 2. **Alignment**
Agents work sequentially through the same task list, preventing duplication and missed requirements.

### 3. **Automation**
Rules and tasks are generated automatically from user intent, reducing manual configuration.

### 4. **Adaptability**
Each project gets custom rules and tasks based on its specific requirements and technology stack.

### 5. **Traceability**
Clear task list provides visibility into project progress and completion status.

## Configuration

### Model Selection

The Rules Generator uses `gpt-4o-mini` by default. To change the model:

```python
# In agents/subagents/rules_generator.py
response = client.chat.completions.create(
    model="gpt-4o-mini",  # Change to your preferred model
    ...
)
```

### System Prompts

Customize the generation behavior by modifying:
- `RULES_SYSTEM_PROMPT`: Controls rules generation style and content
- `TASK_LIST_SYSTEM_PROMPT`: Controls task list organization and format

### File Paths

Change output locations by modifying paths in `run_task()`:

```python
rules_path = Path(".cursor/rules.md")  # Change rules location
task_list_path = Path("docs/tasks.md")  # Change tasks location
```

## Integration with Other Features

### RAG (Retrieval-Augmented Generation)

Agents use both:
- **Generated rules** (project-specific)
- **Knowledge base** (general patterns and best practices)

This combination ensures both project-specific compliance and industry-standard quality.

### Learning Memory

The Rules Generator integrates with the learning memory system:
- Successful patterns can be captured and reused
- Error fixes are stored and referenced
- Knowledge accumulates across projects

## Troubleshooting

### Issue: Files not generated

**Check:**
1. OpenAI API key is set: `echo $OPENAI_API_KEY`
2. IntentParser succeeded: Check for `parsed_intent` in state
3. Network connectivity to OpenAI API

### Issue: Empty or error content in files

**Check:**
1. OpenAI API response was successful
2. System prompts are properly formatted
3. Parsed intent contains sufficient information

### Issue: Agents not reading rules

**Check:**
1. Agent prompts include "Project Rules and Task List" section
2. Agent implementation calls `Path().exists()` and `open()`
3. File paths are correct relative to working directory

## Future Enhancements

### Planned Features

1. **Dynamic Rule Updates**: Allow rules to evolve during project execution
2. **Task Progress Tracking**: Automatically check off completed tasks
3. **Rule Validation**: Verify agents actually follow generated rules
4. **Multi-Project Rules**: Share common rules across related projects
5. **Custom Templates**: Allow users to provide rule/task templates

### Extension Points

The Rules Generator can be extended to generate:
- `.gitignore` files
- `README.md` templates
- CI/CD configuration
- Docker configurations
- Environment variable templates

## API Reference

### `run_task(inputs: Dict[str, Any]) -> Dict[str, Any]`

**Parameters:**
- `inputs`: State dictionary containing `parsed_intent`

**Returns:**
```python
{
    "rules_generated": bool,
    "rules_path": str,
    "task_list_path": str,
    "parsed_intent": dict,  # Passed through
    "raw_user_request": str  # Passed through
}
```

### `generate_document(system_prompt: str, user_prompt: str) -> str`

**Parameters:**
- `system_prompt`: System instructions for generation
- `user_prompt`: User content to process

**Returns:**
- Generated markdown content as string

## Contributing

When contributing to the Rules Generator:

1. Test with multiple project types (web apps, APIs, CLIs, etc.)
2. Ensure system prompts remain general yet specific
3. Validate generated content is actionable and clear
4. Update agent prompts to use new rule sections
5. Add test cases for edge cases (minimal intent, complex projects)

## License

This feature is part of the Orchestrator project and follows the same license terms.

---

**Last Updated:** November 2025  
**Version:** 1.0.0  
**Maintainer:** Orchestrator Team

