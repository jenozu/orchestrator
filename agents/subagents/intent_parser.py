import json
from pathlib import Path
from typing import Dict, Any
from openai import OpenAI  # Assuming you use an OpenAI-compatible API

# Load the schema from the file system
# Handle different working directories by searching for the project root
schema_path = None
for base in [Path.cwd(), Path(__file__).parent.parent.parent]:
    candidate = base / "agents" / "schema" / "project_intent_schema.json"
    if candidate.exists():
        schema_path = candidate
        break

try:
    if schema_path:
        with open(schema_path, "r") as f:
            PROJECT_INTENT_SCHEMA = json.load(f)
    else:
        PROJECT_INTENT_SCHEMA = {}
except (FileNotFoundError, json.JSONDecodeError):
    # Fallback or error handling if schema file is missing
    PROJECT_INTENT_SCHEMA = {}

# LLM client will be initialized lazily in run_task if available


def run_task(inputs: Dict[str, Any]) -> Dict[str, Any]:
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
        # Initialize LLM client lazily (only when needed)
        client = OpenAI()
        
        # Use the LLM's JSON mode feature for reliable structured output
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Use a reliable model for this critical step
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

