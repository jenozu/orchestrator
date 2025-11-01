from typing import Dict, Any


def run_task(inputs: Dict[str, Any]) -> Dict[str, Any]:
    summary = inputs.get("summary", "")
    return {
        "doc_path": "docs/prd.md",
        "status": "drafted",
        "summary": summary,
    }

