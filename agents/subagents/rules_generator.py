from dotenv import load_dotenv
load_dotenv()

import json
from typing import Dict, Any
from pathlib import Path
from openai import OpenAI

# Initialize the LLM client (assuming environment variables are set)
client = OpenAI()

# System prompt for generating the rules file
RULES_SYSTEM_PROMPT = """
You are the Project Rules Generator. Your task is to create a high-level, project-specific rules document for a team of AI agents. 
The rules must be derived from the provided project intent and cover general areas like coding standards, security, and documentation.
The output MUST be a clean Markdown document.

Guidelines for generating rules:
- Include coding standards relevant to the project's technology stack
- Define security best practices appropriate for the project type
- Specify documentation requirements
- Set quality and testing expectations
- Define naming conventions and file organization standards
- Include error handling and logging requirements
- Be specific to the project's needs but keep rules concise and actionable
"""

# System prompt for generating the master task list
TASK_LIST_SYSTEM_PROMPT = """
You are the Master Task List Generator. Your task is to take the structured project intent and convert the 'required_features' into a sequential, step-by-step master task list.
The list must be formatted as a Markdown checklist, with each item representing a high-level task for the agents to complete.
The list should be organized logically (e.g., Setup -> PRD -> Backend -> Frontend -> QA).
The output MUST be a clean Markdown document.

Guidelines for generating the task list:
- Start with setup and planning tasks (PRD, architecture diagrams)
- Group related features together
- Order tasks by dependencies (e.g., backend before frontend)
- Include testing and QA tasks
- Each task should be clear, actionable, and testable
- Use checkbox format: - [ ] Task description
- Include estimated complexity if relevant
"""

def generate_document(system_prompt: str, user_prompt: str) -> str:
    """Helper function to call the OpenAI API with a specific prompt."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Use a reliable model for content generation
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating document: {e}"

def run_task(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates the project rules and master task list files based on parsed intent.
    """
    parsed_intent = inputs.get("parsed_intent")
    
    if not parsed_intent:
        return {"rules_generated": False, "error": "No parsed intent found."}

    # Convert the structured intent back to a string for the LLM prompt
    intent_str = json.dumps(parsed_intent, indent=2)
    
    # --- 1. Generate Project Rules ---
    rules_content = generate_document(
        RULES_SYSTEM_PROMPT,
        f"Generate project rules for the following intent:\n\n{intent_str}"
    )
    
    # Write the rules file to the designated location
    rules_path = Path(".cursor/rules.md")
    rules_path.parent.mkdir(parents=True, exist_ok=True)
    with open(rules_path, "w", encoding="utf-8") as f:
        f.write(rules_content)
    
    # --- 2. Generate Master Task List ---
    task_list_content = generate_document(
        TASK_LIST_SYSTEM_PROMPT,
        f"Generate a sequential master task list (Markdown checklist) for the following project intent:\n\n{intent_str}"
    )
    
    # Write the task list file to the designated location
    task_list_path = Path("docs/tasks.md")
    task_list_path.parent.mkdir(parents=True, exist_ok=True)
    with open(task_list_path, "w", encoding="utf-8") as f:
        f.write(task_list_content)

    # Return the paths of the generated files to the LangGraph state
    return {
        "rules_generated": True,
        "rules_path": str(rules_path),
        "task_list_path": str(task_list_path),
        "parsed_intent": parsed_intent,  # Pass through for next agent
        "raw_user_request": inputs.get("raw_user_request", "")  # Pass through
    }

# Note: The existing 'docs/tasks.md' file will be overwritten with the new, dynamic list.

