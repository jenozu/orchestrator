from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

# Import RAG retrieval utility
try:
    from agents.rag_retrieval import retrieve_knowledge
    RAG_AVAILABLE = True
except ImportError:
    RAG_AVAILABLE = False
    logger.warning("RAG retrieval not available. PRD agent will work without knowledge base context.")


def run_task(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Run PRD agent task with domain-specific knowledge retrieval.
    
    This agent drafts PRDs using:
    - Structured requirements from parsed_intent
    - Domain-specific knowledge from the PRD KB
    - Shared knowledge base context
    """
    # 1. Extract structured requirements from parsed_intent
    parsed_intent = inputs.get('parsed_intent', {})
    project_description = parsed_intent.get('project_description', '')
    required_features = parsed_intent.get('required_features', [])
    
    # Fallback to summary if parsed_intent not available
    summary = inputs.get("summary", "")
    if not project_description and summary:
        project_description = summary
    
    # 2. Retrieve scoped knowledge from PRD KB
    knowledge_context = ""
    if RAG_AVAILABLE:
        try:
            # Construct query for PRD templates and best practices
            query = f"PRD template for {project_description}"
            if required_features:
                query += f" with features: {', '.join(required_features[:3])}"
            
            knowledge_context = retrieve_knowledge(
                query=query,
                agent_domain="prd",
                top_k=5
            )
            
            if knowledge_context:
                logger.info("Retrieved PRD knowledge context for drafting")
            else:
                logger.info("No PRD knowledge context retrieved (KB may be empty)")
        except Exception as e:
            logger.error(f"Failed to retrieve PRD knowledge: {e}")
    
    # 3. Construct the PRD (currently placeholder, but now has access to knowledge_context)
    # In a full implementation, this would:
    # - Load the PRD mission prompt
    # - Combine: mission_prompt + requirements + knowledge_context
    # - Call LLM to generate PRD
    # - Write to docs/prd.md
    
    return {
        "doc_path": "docs/prd.md",
        "status": "drafted",
        "summary": summary or project_description,
        "knowledge_retrieved": bool(knowledge_context),
        "context_length": len(knowledge_context) if knowledge_context else 0,
    }

