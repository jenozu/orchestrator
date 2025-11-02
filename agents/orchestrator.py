from typing import Any, Dict, List, Optional, Tuple

try:
    from langgraph.graph import END, StateGraph
except Exception:  # pragma: no cover
    END = "END"  # type: ignore
    StateGraph = object  # type: ignore

# Import subagents
try:
    from agents.subagents.intent_parser import run_task as run_intent_parser
except ImportError:
    run_intent_parser = None


class Orchestrator:
    """Coordinates task DAG execution and subagent dispatch.

    This is a minimal skeleton; subagent nodes and retrieval policies will be
    added in subsequent tasks.
    """

    def __init__(self) -> None:
        self._graph: Optional[StateGraph] = None
        
        # Initialize learning memory
        try:
            from agents.learning_memory import get_learning_memory
            self.learning_memory = get_learning_memory()
        except ImportError:
            self.learning_memory = None

    def build_graph(self) -> None:
        """Construct a graph with IntentParser as the entry point.

        The IntentParser node translates raw user requests into structured JSON,
        then transitions to other subagents for further processing.
        """
        if StateGraph is object:
            # LangGraph not installed; keep skeleton valid
            self._graph = None
            return
        graph = StateGraph(dict)

        # Add the IntentParser as the entry point
        if run_intent_parser:
            graph.add_node("intent_parser", run_intent_parser)
            graph.set_entry_point("intent_parser")
            # For now, IntentParser transitions to END
            # Later we'll add edges to other subagents (PRD, Diagrammer, etc.)
            graph.add_edge("intent_parser", END)
        else:
            # Fallback if IntentParser not available
            def start_node(state: Dict[str, Any]) -> Dict[str, Any]:
                state = dict(state or {})
                state["status"] = "started"
                return state
            graph.add_node("start", start_node)
            graph.set_entry_point("start")
            graph.add_edge("start", END)
        
        self._graph = graph

    def run_once(self, initial_state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if self._graph is None:
            self.build_graph()
        if self._graph is None:
            # Fallback if LangGraph unavailable
            return {"status": "started"}
        app = self._graph.compile()
        result = app.invoke(initial_state or {})
        return result

    def plan_to_dag(self, tasks: List[Dict[str, Any]]) -> List[Tuple[str, List[str]]]:
        """Convert a list of task specs to a simple dependency list.

        Returns list of (task_id, dependencies).
        """
        dag: List[Tuple[str, List[str]]] = []
        for spec in tasks:
            dag.append((spec.get("id", "task"), list(spec.get("deps", []))))
        return dag

