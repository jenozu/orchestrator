# IntentParser Agent Integration Guide

This guide provides the necessary steps and code to implement the `IntentParser` agent and integrate it into your existing **Parallel Agent Build System**. This agent will translate unstructured user requests into a reliable, structured JSON format, significantly improving the robustness and predictability of your Orchestrator.

## 1. Define the Structured Schema

First, define the JSON schema that the `IntentParser` agent must adhere to. This schema should be saved in a new file, perhaps `agents/schema/project_intent_schema.json`.

**File: `agents/schema/project_intent_schema.json`**

```json
{
  "type": "object",
  "properties": {
    "project_name": {
      "type": "string",
      "description": "A concise, kebab-case name for the project (e.g., 'e-commerce-platform')."
    },
    "project_description": {
      "type": "string",
      "description": "A one-sentence summary of the project's core function."
    },
    "project_type": {
      "type": "string",
      "enum": ["web-app", "api-service", "cli-tool", "library", "data-pipeline"],
      "description": "The primary type of software to be built. Default to 'web-app' if unclear."
    },
    "required_features": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "A list of key features or user stories to be implemented (e.g., 'user authentication', 'CRUD for products', 'payment gateway integration')."
    },
    "technology_stack": {
      "type": "object",
      "properties": {
        "backend": {"type": "string", "description": "Preferred backend framework (e.g., 'FastAPI', 'Node.js/Express'). Infer from context if not explicit."},
        "frontend": {"type": "string", "description": "Preferred frontend framework (e.g., 'React', 'Vue', 'Next.js'). Infer from context if not explicit."},
        "database": {"type": "string", "description": "Preferred database (e.g., 'PostgreSQL', 'MongoDB'). Infer from context if not explicit."}
      },
      "description": "Specific technology choices, if mentioned by the user. Should be an empty object if no technologies are specified."
    },
    "initial_tasks": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "A list of high-level tasks for the Orchestrator to prioritize (e.g., 'Draft PRD', 'Scaffold Backend', 'Create Database Schema'). Default to ['Draft PRD', 'Generate Architecture Diagram']."
    }
  },
  "required": ["project_name", "project_description", "required_features"]
}
```

## 2. Create the IntentParser Agent

Create a new file for the agent logic. This agent will use an LLM with JSON mode or function calling to generate the structured output.

**File: `agents/subagents/intent_parser.py`**

```python
import json
from typing import Dict, Any
from openai import OpenAI # Assuming you use an OpenAI-compatible API

# Load the schema from the file system
try:
    with open("agents/schema/project_intent_schema.json", "r") as f:
        PROJECT_INTENT_SCHEMA = json.load(f)
except FileNotFoundError:
    # Fallback or error handling if schema file is missing
    PROJECT_INTENT_SCHEMA = {} 

# Initialize the LLM client (assuming environment variables are set)
client = OpenAI()

def run_intent_parser(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Translates a raw user request into a structured JSON object 
    based on the PROJECT_INTENT_SCHEMA.
    """
    raw_user_request = inputs.get("raw_user_request", "")
    
    if not raw_user_request:
        return {"parsed_intent": None, "error": "No raw user request provided."}

    system_prompt = (
        "You are the Intent Parser Agent. Your task is to analyze the user's request "
        "for a new software project and translate it into a structured JSON object. "
        "You MUST strictly adhere to the provided JSON schema. Infer missing details "
        "logically (e.g., project_name from description) but do not invent features. "
        "If a technology is not specified, leave the field blank or infer a common default."
    )

    try:
        # Use the LLM's JSON mode feature for reliable structured output
        response = client.chat.completions.create(
            model="gpt-4.1-mini", # Use a reliable model for this critical step
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Translate this project request into JSON: '{raw_user_request}'"}
            ],
            # Pass the schema in the prompt for better adherence, 
            # as the response_format only guarantees JSON, not schema adherence.
            # For true schema enforcement, use the function calling API if available.
            # For simplicity here, we rely on the prompt and JSON mode.
            extra_body={"schema": PROJECT_INTENT_SCHEMA} 
        )
        
        # The response content is a JSON string
        json_string = response.choices[0].message.content
        parsed_intent = json.loads(json_string)
        
        # The output state will now contain the structured intent
        return {"parsed_intent": parsed_intent, "raw_user_request": raw_user_request}

    except Exception as e:
        print(f"IntentParser Error: {e}")
        return {"parsed_intent": None, "error": str(e)}

# Note: In a real LangGraph setup, this function would be the node's executor.
```

## 3. Update the Orchestrator (LangGraph)

You need to modify your main orchestrator file (`agents/orchestrator.py`) to add the `IntentParser` as the very first node in your graph.

**File: `agents/orchestrator.py` (Conceptual Changes)**

```python
# ... existing imports ...
from langgraph.graph import StateGraph, END
from agents.subagents.intent_parser import run_intent_parser
from agents.subagents.prd import run_prd_agent
# ... other subagent imports ...

# Define the state (your existing state object)
class AgentState(TypedDict):
    raw_user_request: str
    parsed_intent: Dict[str, Any]
    # ... existing state fields (e.g., prd_summary, architecture_diagram, etc.) ...

class Orchestrator:
    def __init__(self):
        # ...
        pass

    def build_graph(self):
        # 1. Initialize the graph with the state
        graph = StateGraph(AgentState)

        # 2. Add the new IntentParser node
        graph.add_node("intent_parser", run_intent_parser)
        
        # 3. Add existing subagent nodes
        graph.add_node("prd_agent", run_prd_agent)
        # ... add other subagent nodes (diagrammer, backend, etc.) ...

        # 4. Set the entry point to the new IntentParser
        graph.set_entry_point("intent_parser")

        # 5. Define the first transition
        # The intent_parser always transitions to the prd_agent (or a router)
        graph.add_edge("intent_parser", "prd_agent") 
        
        # 6. Modify the PRD Agent's input logic
        # The PRD Agent must now read from `state['parsed_intent']` instead of `state['raw_user_request']`
        
        # ... existing transitions for other agents ...

        self.app = graph.compile()

    def run_once(self, initial_state: Dict[str, Any]):
        # The initial state must now contain the raw user request
        # Example: {"raw_user_request": "Build a simple e-commerce site with user auth and a product catalog using FastAPI and React."}
        return self.app.invoke(initial_state)

# ...
```

## 4. Sample Mission Prompt (`agents/prompts/intent_parser.md`)

While the LLM's JSON mode is powerful, a clear prompt is still essential for quality.

**File: `agents/prompts/intent_parser.md`**

```markdown
# Intent Parser Agent Mission

You are a highly precise, structured data translator. Your mission is to take a user's natural language request for a software project and convert it into a JSON object that strictly conforms to the provided schema.

**Instructions:**
1.  **Strict Adherence:** Your output MUST be a valid JSON object. Do not include any other text, markdown, or commentary.
2.  **Inference:** If the user does not explicitly state a `project_name`, infer a concise, kebab-case name from the description.
3.  **Features:** Extract all core functionalities and user stories into the `required_features` array.
4.  **Technology:** If the user mentions specific frameworks (e.g., "React," "Django," "PostgreSQL"), populate the `technology_stack` object. If not mentioned, leave the sub-fields blank or infer a common default based on the `project_type`.
5.  **Initial Tasks:** Default the `initial_tasks` to `["Draft PRD", "Generate Architecture Diagram"]` unless the user specifies a different starting point.

**Example Input:**
"I need a new social media app called 'Connectify' that lets users post photos and follow each other. It should use Node.js for the backend and Vue.js for the frontend."

**Example Output (Conceptual):**
```json
{
  "project_name": "connectify",
  "project_description": "A social media application for photo sharing and user following.",
  "project_type": "web-app",
  "required_features": [
    "user registration and login",
    "user profile management",
    "photo posting and viewing",
    "follow/unfollow functionality"
  ],
  "technology_stack": {
    "backend": "Node.js",
    "frontend": "Vue.js",
    "database": "PostgreSQL"
  },
  "initial_tasks": ["Draft PRD", "Generate Architecture Diagram"]
}
```

By following these steps, you will have successfully implemented a robust `IntentParser` that dramatically improves the reliability of your entire agent system.
