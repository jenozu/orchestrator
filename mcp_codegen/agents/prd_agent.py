"""PRD agent for creating product requirements documents from ideas."""
import json
from typing import Dict, Any
from openai import OpenAI
from mcp_codegen.config import OPENAI_API_KEY, CODE_MODEL


class PRDAgent:
    """Create PRD documents from user ideas."""
    
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
    
    async def create_prd(self, idea: str, output_path: str) -> Dict[str, Any]:
        """Create a PRD document from an idea."""
        # Use LLM to generate structured PRD
        response = self.client.chat.completions.create(
            model=CODE_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert product manager who creates detailed Product Requirements Documents (PRDs).
Write a comprehensive PRD with the following structure:
- Summary: Brief overview
- Goals & Non-Goals: Clear objectives and what's out of scope
- User Stories: 3-5 user stories in "As a... I want... So that..." format
- Requirements: Functional and non-functional requirements
- Milestones: M1 (MVP) and M2 (Polish) with specific deliverables
- Tech Stack: Recommended technologies with rationale
- Success Metrics: Measurable outcomes"""
                },
                {
                    "role": "user",
                    "content": f"Create a PRD for: {idea}"
                }
            ]
        )
        
        prd_content = response.choices[0].message.content
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(prd_content)
        
        return {
            "prd_path": output_path,
            "status": "created",
            "idea": idea,
            "summary": "PRD successfully generated"
        }

