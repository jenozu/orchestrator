from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

# Import RAG retrieval utility
try:
    from agents.rag_retrieval import retrieve_knowledge
    RAG_AVAILABLE = True
except ImportError:
    RAG_AVAILABLE = False
    logger.warning("RAG retrieval not available. Frontend agent will work without knowledge base context.")


def run_task(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Run frontend agent task with domain-specific knowledge retrieval.
    
    This agent scaffolds UI components using:
    - Structured requirements from parsed_intent
    - Domain-specific knowledge from the frontend KB
    - Shared knowledge base context
    """
    # 1. Extract structured requirements from parsed_intent
    parsed_intent = inputs.get('parsed_intent', {})
    project_description = parsed_intent.get('project_description', '')
    required_features = parsed_intent.get('required_features', [])
    
    # If parsed_intent not available, fall back to raw_user_request
    if not parsed_intent and 'raw_user_request' in inputs:
        raw_request = inputs['raw_user_request']
        logger.warning("parsed_intent not available. Using raw_user_request as fallback.")
        project_description = raw_request
        required_features = []
    
    # 2. Retrieve scoped knowledge from frontend KB
    knowledge_context = ""
    if RAG_AVAILABLE:
        try:
            # Construct query for UI components and patterns
            query = f"React components for {project_description}"
            if required_features:
                query += f" with features: {', '.join(required_features[:3])}"
            
            knowledge_context = retrieve_knowledge(
                query=query,
                agent_domain="frontend",
                top_k=5
            )
            
            if knowledge_context:
                logger.info("Retrieved frontend knowledge context for scaffolding")
            else:
                logger.info("No frontend knowledge context retrieved (KB may be empty)")
        except Exception as e:
            logger.error(f"Failed to retrieve frontend knowledge: {e}")
    
    # 3. Construct the UI (currently placeholder, but now has access to knowledge_context)
    # In a full implementation, this would:
    # - Load the frontend mission prompt
    # - Combine: mission_prompt + requirements + knowledge_context
    # - Call LLM to generate components
    # - Return the generated component code
    
    return {
        "status": "scaffolded",
        "notes": "Frontend components to be defined in subsequent tasks.",
        "knowledge_retrieved": bool(knowledge_context),
        "context_length": len(knowledge_context) if knowledge_context else 0,
    }

