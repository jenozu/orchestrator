# How to Use the Codegen MCP Server

## 🚀 Quick Start

After restarting Cursor, your `codegen` MCP server is automatically available. Just ask naturally in Cursor's AI chat!

## 📋 Available Tools

### 1. `create_prd` - Create Product Requirements Document

**What it does**: Generates a comprehensive PRD from a project idea.

**How to use in Cursor**:
```
Use create_prd to create a PRD for a task management app with user authentication
```

**Parameters**:
- `idea` (required): Your project idea/description
- `output_path` (optional): Where to save the PRD (default: `docs/generated_prd.md`)

**Example**:
```
Use create_prd with idea "A social media platform for developers" and output_path "docs/social_prd.md"
```

---

### 2. `parse_prd` - Parse PRD/README into Structured Requirements

**What it does**: Converts a PRD or README file into structured JSON requirements.

**How to use in Cursor**:
```
Use parse_prd to parse docs/prd.md into structured requirements
```

**Parameters**:
- `document_path` (required): Path to the PRD or README file

**Example**:
```
Use parse_prd to parse the document at docs/my_project_prd.md
```

---

### 3. `retrieve_context` - Search Knowledge Base with RAG

**What it does**: Searches your knowledge base for similar code patterns, documentation, or solutions.

**How to use in Cursor**:
```
Use retrieve_context to find FastAPI authentication patterns
```

**Parameters**:
- `query` (required): What you're looking for
- `k` (optional): Number of results (default: 5)

**Example**:
```
Use retrieve_context to search for "React component patterns" with k=10
```

---

### 4. `generate_project` - Generate Complete Project

**What it does**: Generates a complete project structure from structured requirements.

**How to use in Cursor**:
```
Use generate_project to generate a project from the requirements in docs/prd.md
```

**Parameters**:
- `requirements` (required): Structured requirements object (JSON)
- `output_dir` (required): Where to generate the project

**Example**:
```
Use generate_project with requirements from docs/parsed_requirements.json and output_dir "generated_project"
```

---

### 5. `debug_error` - Debug Code with Learning

**What it does**: Analyzes errors and proposes fixes, learning from past solutions.

**How to use in Cursor**:
```
Use debug_error to fix this error: [paste your error message and code]
```

**Parameters**:
- `code` (required): The code that has the error
- `error` (required): The error message
- `context` (optional): Additional context about the error

**Example**:
```
Use debug_error with code "def my_function():\n    return x + 1" and error "NameError: name 'x' is not defined"
```

---

### 6. `search_learned_solutions` - Find Learned Solutions

**What it does**: Searches for previously learned solutions to similar problems.

**How to use in Cursor**:
```
Use search_learned_solutions to find how we've fixed authentication errors before
```

**Parameters**:
- `query` (required): Description of the problem
- `category` (optional): Solution category (default: `error_fixes`)
- `limit` (optional): Number of results (default: 5)

**Example**:
```
Use search_learned_solutions to find solutions for "database connection timeout" with limit=10
```

---

### 7. `get_learning_stats` - Get Learning Statistics

**What it does**: Shows statistics about what the system has learned.

**How to use in Cursor**:
```
Use get_learning_stats to show me what the system has learned about error fixes
```

**Parameters**:
- `category` (optional): Stats category (default: `error_fixes`)

**Example**:
```
Use get_learning_stats to get statistics for category "error_fixes"
```

---

## 🎯 Common Workflows

### Workflow 1: Create a New Project

```
1. Use create_prd to create a PRD for "a todo app with React and FastAPI"
2. Use parse_prd to parse the generated PRD
3. Use generate_project to generate the complete project structure
```

### Workflow 2: Debug and Learn

```
1. Use debug_error to fix an error (system learns from this)
2. Use search_learned_solutions to find similar fixes
3. Use get_learning_stats to see what's been learned
```

### Workflow 3: Find Code Patterns

```
1. Use retrieve_context to find similar patterns
2. Use the results to inform your code generation
3. Use generate_project to create code based on patterns
```

---

## 🔍 How to Verify It's Working

### Option 1: Test in Cursor

1. **Restart Cursor** (if you haven't already)
2. Open AI chat
3. Try: `Use create_prd to create a PRD for a simple blog app`
4. The tool should execute and create a PRD file

### Option 2: Run Test Script

```powershell
python test_mcp_tools.py
```

This will:
- List all available tools
- Test PRD creation
- Test RAG retrieval
- Verify everything is working

---

## 🛠️ Troubleshooting

### Tools Not Appearing in Cursor

1. **Check MCP Configuration**:
   - Verify `C:\Users\andel\.cursor\mcp.json` has the `codegen` section
   - Make sure it points to `scripts/run_mcp_server.py`

2. **Restart Cursor**:
   - Close Cursor completely
   - Reopen it
   - MCP servers load on startup

3. **Check Server Logs**:
   - Look for errors in Cursor's developer console
   - Verify the Python path is correct

### Server Won't Start

1. **Test the script directly**:
   ```powershell
   python scripts/run_mcp_server.py
   ```
   Should initialize without errors

2. **Check .env file**:
   - Make sure `OPENAI_API_KEY` is set in `.env`
   - Verify the file is in the project root

3. **Verify Python path**:
   - The script should automatically add the project root
   - Check that `mcp_codegen` folder exists

---

## 💡 Pro Tips

1. **Be Specific**: The more details you provide, the better the results
   - ✅ "Use create_prd for a task management app with React frontend, FastAPI backend, PostgreSQL database, user authentication, and task prioritization"
   - ❌ "Use create_prd for an app"

2. **Chain Tools**: Use multiple tools together for better results
   - Create PRD → Parse PRD → Generate Project

3. **Use RAG First**: Before generating code, search for similar patterns
   - "Use retrieve_context to find FastAPI authentication examples"

4. **Learn from Errors**: Every time you use `debug_error`, the system learns
   - Future similar errors will be fixed faster

5. **Check Learning Stats**: Periodically check what the system has learned
   - "Use get_learning_stats to see error fix patterns"

---

## 📚 Example Conversations

### Example 1: Starting a New Project

**You**: "I want to build a blog platform. Use create_prd to create a PRD for a blog with user authentication, post creation, and comments."

**Cursor**: [Creates PRD using `create_prd` tool]

**You**: "Now use parse_prd to parse that PRD into structured requirements."

**Cursor**: [Parses PRD using `parse_prd` tool]

**You**: "Use generate_project to generate the complete project structure."

**Cursor**: [Generates project using `generate_project` tool]

### Example 2: Finding Code Patterns

**You**: "Use retrieve_context to find React component patterns for forms."

**Cursor**: [Searches knowledge base and returns relevant patterns]

**You**: "Now use those patterns to help me create a login form component."

**Cursor**: [Uses the retrieved patterns to generate code]

### Example 3: Debugging

**You**: "I'm getting this error: [error message]. Use debug_error to fix it."

**Cursor**: [Analyzes error, proposes fix, and learns from it]

**You**: "Use search_learned_solutions to see if we've fixed similar errors before."

**Cursor**: [Searches learning memory for similar solutions]

---

## 🎉 You're Ready!

Your MCP server is configured and ready to use. Just restart Cursor and start using the tools naturally in your conversations!

For more details, see:
- `MCP_SERVER_SETUP.md` - Complete setup guide
- `QUICK_REFERENCE.md` - Quick command reference
- `test_mcp_tools.py` - Test script

