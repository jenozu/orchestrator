# Rules Generator - Quick Start Guide

## 🚀 Quick Start (2 Minutes)

### 1. Install Dependencies
```bash
pip install openai langgraph
```

### 2. Set API Key
```bash
# Windows PowerShell
$env:OPENAI_API_KEY="your-api-key-here"

# Linux/Mac
export OPENAI_API_KEY="your-api-key-here"
```

### 3. Run Test
```bash
python test_rules_generator.py
```

### 4. Check Results
```bash
# View generated rules
cat .cursor/rules.md

# View generated tasks
cat docs/tasks.md
```

## 📝 Usage Example

```python
from agents.orchestrator import Orchestrator

# Create orchestrator
orchestrator = Orchestrator()
orchestrator.build_graph()

# Run with your project request
result = orchestrator.run_once({
    "raw_user_request": """
    Build a REST API for a blog with:
    - User authentication
    - Post CRUD operations
    - Comments system
    Tech: FastAPI, PostgreSQL
    """
})

# Check results
print(f"✅ Rules generated: {result['rules_generated']}")
print(f"📁 Rules file: {result['rules_path']}")
print(f"📁 Tasks file: {result['task_list_path']}")
```

## 🎯 What It Does

### Input
```
User Request: "Build a task management app with React and FastAPI"
```

### Output

#### `.cursor/rules.md`
```markdown
# Project Rules

## Coding Standards
- Use TypeScript strict mode for React
- Follow PEP 8 for Python code
- Use async/await for all API calls

## Security
- Validate all user inputs
- Use JWT for authentication
- Sanitize database queries

## Testing
- 80% code coverage minimum
- Write unit tests for all API endpoints
- End-to-end tests for critical flows
```

#### `docs/tasks.md`
```markdown
# Master Task List

## Setup
- [ ] Initialize project structure
- [ ] Set up development environment
- [ ] Configure database

## Backend
- [ ] Implement authentication endpoints
- [ ] Create task CRUD API
- [ ] Add database migrations

## Frontend
- [ ] Create authentication UI
- [ ] Build task dashboard
- [ ] Implement task forms

## Testing
- [ ] Write backend tests
- [ ] Write frontend tests
- [ ] Perform integration testing
```

## 🔍 Workflow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Your Request │ →→→ │ Intent Parse │ →→→ │ Rules & Tasks│
└──────────────┘     └──────────────┘     │  Generated   │
                                           └──────────────┘
                                                  ↓↓↓
                                           ┌──────────────┐
                                           │  All Agents  │
                                           │ Follow Rules │
                                           └──────────────┘
```

## ✅ Verify It's Working

After running the test script, you should see:

1. **Console Output**:
   ```
   ✅ Workflow completed successfully!
   ✅ .cursor/rules.md created successfully!
   ✅ docs/tasks.md created successfully!
   ```

2. **Generated Files**:
   - `.cursor/rules.md` exists and contains project-specific rules
   - `docs/tasks.md` exists and contains a sequential task list

3. **State Updates**:
   ```json
   {
     "rules_generated": true,
     "rules_path": ".cursor/rules.md",
     "task_list_path": "docs/tasks.md",
     "rules_loaded": true,
     "tasks_loaded": true
   }
   ```

## 🐛 Troubleshooting

### Problem: API Key Error
```
Error: Authentication error
```
**Solution**: Set your OpenAI API key:
```bash
export OPENAI_API_KEY="sk-..."
```

### Problem: Files Not Generated
```
Error: rules_generated: false
```
**Solution**: Check that IntentParser succeeded:
```python
result = orchestrator.run_once({"raw_user_request": "..."})
print(result.get("parsed_intent"))  # Should not be None
```

### Problem: Empty Files
**Solution**: Check OpenAI API connection:
```bash
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

## 📚 Learn More

- **Full Documentation**: `docs/RULES_GENERATOR_FEATURE.md`
- **Implementation Details**: `RULES_GENERATOR_IMPLEMENTATION_SUMMARY.md`
- **Integration Guide**: `misc/Rules and Task Generator Integration Guide`

## 🎓 Advanced Usage

### Custom Rules Template
```python
# Modify agents/subagents/rules_generator.py
RULES_SYSTEM_PROMPT = """
Your custom prompt here...
Include specific guidelines for:
- Code formatting
- Git workflow
- Review process
"""
```

### Custom Task Organization
```python
# Modify agents/subagents/rules_generator.py
TASK_LIST_SYSTEM_PROMPT = """
Your custom prompt here...
Organize tasks by:
- Priority level
- Complexity
- Dependencies
"""
```

### Change Output Paths
```python
# In agents/subagents/rules_generator.py
rules_path = Path("custom/path/rules.md")
task_list_path = Path("custom/path/tasks.md")
```

## 💡 Tips

1. **Be Specific**: More detailed requests = better rules and tasks
   ```
   ❌ "Build a web app"
   ✅ "Build a blog with React, FastAPI, user auth, and comments"
   ```

2. **Include Tech Stack**: Helps generate relevant coding standards
   ```
   ✅ "Tech stack: React, TypeScript, FastAPI, PostgreSQL"
   ```

3. **Mention Requirements**: Include security, performance, or other concerns
   ```
   ✅ "Must be secure, scalable, and accessible"
   ```

## 🎉 Success!

You now have:
- ✅ Automatic rules generation
- ✅ Automatic task planning
- ✅ All agents following consistent standards
- ✅ Clear project roadmap

Happy building! 🚀

---

**Need Help?** Check the troubleshooting section or review the full documentation.

