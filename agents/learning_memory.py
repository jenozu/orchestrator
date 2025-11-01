"""Learning and memory system for persistent agent knowledge."""
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
import json

try:
    from langgraph.store.memory import InMemoryStore
    from langchain.embeddings import init_embeddings
    from langgraph.checkpoint.memory import InMemorySaver
except ImportError:
    # Graceful fallback
    InMemoryStore = object
    InMemorySaver = object
    init_embeddings = lambda x: None


class LearningMemory:
    """Persistent memory with semantic search for agent learning."""
    
    def __init__(self, use_persistent: bool = False, db_uri: Optional[str] = None):
        """Initialize learning memory system.
        
        Args:
            use_persistent: If True, use Postgres instead of in-memory
            db_uri: Database URI for Postgres (if use_persistent)
        """
        if use_persistent and db_uri:
            # Production: Use Postgres
            try:
                from langgraph.checkpoint.postgres import PostgresSaver, PostgresStore
                self.store = PostgresStore.from_conn_string(db_uri)
                self.checkpointer = PostgresSaver.from_conn_string(db_uri)
            except ImportError:
                raise ImportError("Install langgraph-checkpoint-postgres for persistent storage")
        else:
            # Development: Use in-memory
            if InMemoryStore is object:
                self.store = None
                self.checkpointer = None
            else:
                try:
                    # Configure with semantic search if API key available
                    embedding_fn = init_embeddings("openai:text-embedding-3-small")
                    self.store = InMemoryStore(
                        index={
                            "embed": embedding_fn,
                            "dims": 1536,
                            "fields": ["error", "solution", "context", "$"]
                        }
                    )
                except Exception:
                    # Fallback to simple store without embeddings
                    self.store = InMemoryStore()
                
                try:
                    self.checkpointer = InMemorySaver()
                except Exception:
                    self.checkpointer = None
    
    async def learn_from_success(
        self,
        category: str,
        error: str,
        solution: str,
        context: Dict[str, Any],
        success: bool = True
    ) -> str:
        """Store a successful solution for future reference.
        
        Returns:
            Memory ID of stored solution
        """
        if self.store is None:
            return ""
        
        namespace = ("learned_solutions", category)
        memory_id = str(uuid.uuid4())
        
        memory_value = {
            "error": error,
            "solution": solution,
            "context": context,
            "success": success,
            "occurrences": 1,
            "success_count": 1 if success else 0,
            "success_rate": 1.0 if success else 0.0,
            "first_seen": datetime.utcnow().isoformat(),
            "last_updated": datetime.utcnow().isoformat()
        }
        
        await self.store.aput(namespace, memory_id, memory_value)
        return memory_id
    
    async def search_solutions(
        self,
        category: str,
        query: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Search for similar solutions using semantic search.
        
        Returns:
            List of solutions sorted by relevance
        """
        if self.store is None:
            return []
        
        namespace = ("learned_solutions", category)
        memories = await self.store.asearch(namespace, query=query, limit=limit)
        
        # Convert to dict format
        results = []
        for memory in memories:
            result = memory.value.copy()
            result['distance'] = memory.distance  # Similarity score
            result['key'] = memory.key
            results.append(result)
        
        return results
    
    async def update_solution_statistics(
        self,
        category: str,
        memory_id: str,
        success: bool
    ) -> None:
        """Update statistics for a learned solution.
        
        Args:
            category: Solution category
            memory_id: ID of memory to update
            success: Whether the solution was successful this time
        """
        if self.store is None:
            return
        
        namespace = ("learned_solutions", category)
        memory = await self.store.aget(namespace, memory_id)
        
        if memory:
            memory['occurrences'] += 1
            if success:
                memory['success_count'] = memory.get('success_count', 0) + 1
            
            memory['success_rate'] = memory['success_count'] / memory['occurrences']
            memory['last_updated'] = datetime.utcnow().isoformat()
            
            await self.store.aput(namespace, memory_id, memory)
    
    async def get_top_solutions(
        self,
        category: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get top solutions by success rate.
        
        Returns:
            List of solutions sorted by effectiveness
        """
        if self.store is None:
            return []
        
        # Search all memories in category
        namespace = ("learned_solutions", category)
        memories = await self.store.asearch(namespace, query="", limit=limit * 2)
        
        # Sort by success rate
        solutions = [
            {
                **m.value,
                "key": m.key,
                "distance": m.distance
            }
            for m in memories
        ]
        solutions.sort(key=lambda x: x['success_rate'], reverse=True)
        
        return solutions[:limit]
    
    async def add_agent_context(
        self,
        agent_id: str,
        context: Dict[str, Any]
    ) -> str:
        """Add context about an agent's behavior.
        
        Useful for tracking what each agent learns.
        """
        if self.store is None:
            return ""
        
        namespace = ("agent_context", agent_id)
        memory_id = str(uuid.uuid4())
        
        context_value = {
            "context": context,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await self.store.aput(namespace, memory_id, context_value)
        return memory_id
    
    async def get_agent_context(
        self,
        agent_id: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Get recent context for an agent."""
        if self.store is None:
            return []
        
        namespace = ("agent_context", agent_id)
        memories = await self.store.asearch(namespace, query="", limit=limit)
        
        return [m.value for m in memories]


class LearningTracker:
    """Track what the system learns over time."""
    
    def __init__(self, learning_memory: LearningMemory):
        self.memory = learning_memory
        self.stats = {
            "total_patterns": 0,
            "patterns_used": 0,
            "successful_fixes": 0,
            "failed_fixes": 0
        }
    
    async def record_learning_event(
        self,
        category: str,
        error: str,
        solution: str,
        context: Dict[str, Any],
        success: bool
    ) -> str:
        """Record a learning event and update statistics."""
        memory_id = await self.memory.learn_from_success(
            category, error, solution, context, success
        )
        
        # Update stats
        self.stats["total_patterns"] += 1
        if success:
            self.stats["successful_fixes"] += 1
        else:
            self.stats["failed_fixes"] += 1
        
        return memory_id
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get learning statistics."""
        total_attempts = self.stats["successful_fixes"] + self.stats["failed_fixes"]
        success_rate = (
            self.stats["successful_fixes"] / total_attempts
            if total_attempts > 0
            else 0.0
        )
        
        return {
            **self.stats,
            "success_rate": success_rate,
            "total_attempts": total_attempts
        }


# Global instance (can be overridden)
_global_memory = None

def get_learning_memory() -> LearningMemory:
    """Get or create global learning memory instance."""
    global _global_memory
    if _global_memory is None:
        _global_memory = LearningMemory()
    return _global_memory


def set_learning_memory(memory: LearningMemory) -> None:
    """Set global learning memory instance."""
    global _global_memory
    _global_memory = memory

