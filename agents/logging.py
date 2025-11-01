"""Run logging and task tracking for the orchestrator system."""
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


_logger = logging.getLogger(__name__)


class RunLogger:
    """Logger for orchestrator runs with structured output."""

    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.current_run: Optional[str] = None

    def start_run(self, run_id: str, metadata: Dict[str, Any]) -> None:
        """Begin a new orchestrator run."""
        self.current_run = run_id
        self._write_event("run_start", {"run_id": run_id, "metadata": metadata})

    def log_task(
        self,
        task_id: str,
        agent_id: str,
        status: str,
        outputs: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Log a task execution event."""
        self._write_event(
            "task",
            {
                "task_id": task_id,
                "agent_id": agent_id,
                "status": status,
                "outputs": outputs,
                "timestamp": datetime.utcnow().isoformat(),
            },
        )

    def end_run(self, summary: Dict[str, Any]) -> None:
        """End the current run."""
        self._write_event("run_end", {"summary": summary})
        self.current_run = None

    def _write_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """Write a structured event to the log."""
        if self.current_run:
            log_file = self.log_dir / f"{self.current_run}.log"
            with log_file.open("a") as f:
                f.write(json.dumps({"event": event_type, "data": data}) + "\n")
        _logger.info(f"{event_type}: {data}")


class TaskTracker:
    """Tracks task status and dependencies."""

    def __init__(self):
        self.tasks: Dict[str, Dict[str, Any]] = {}

    def register(self, task_id: str, deps: List[str], metadata: Dict[str, Any]) -> None:
        """Register a task with dependencies."""
        self.tasks[task_id] = {
            "deps": deps,
            "status": "pending",
            "metadata": metadata,
        }

    def mark_started(self, task_id: str) -> None:
        """Mark a task as started."""
        if task_id in self.tasks:
            self.tasks[task_id]["status"] = "started"

    def mark_completed(self, task_id: str, outputs: Dict[str, Any]) -> None:
        """Mark a task as completed."""
        if task_id in self.tasks:
            self.tasks[task_id]["status"] = "completed"
            self.tasks[task_id]["outputs"] = outputs

    def mark_failed(self, task_id: str, error: str) -> None:
        """Mark a task as failed."""
        if task_id in self.tasks:
            self.tasks[task_id]["status"] = "failed"
            self.tasks[task_id]["error"] = error

    def get_ready(self) -> List[str]:
        """Return task IDs with all dependencies satisfied."""
        ready = []
        for task_id, info in self.tasks.items():
            if info["status"] == "pending":
                deps_satisfied = all(
                    self.tasks.get(dep, {}).get("status") == "completed"
                    for dep in info["deps"]
                )
                if deps_satisfied:
                    ready.append(task_id)
        return ready

    def to_dict(self) -> Dict[str, Any]:
        """Export tracker state as dict."""
        return {"tasks": self.tasks}


class MemoryStore:
    """Simple in-memory store for orchestration state.

    In production, this would interface with LangGraph Store or a vector DB.
    """

    def __init__(self):
        self._store: Dict[str, Any] = {}

    def put(self, key: str, value: Any) -> None:
        """Store a value."""
        self._store[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve a value."""
        return self._store.get(key, default)

    def exists(self, key: str) -> bool:
        """Check if a key exists."""
        return key in self._store

    def delete(self, key: str) -> None:
        """Delete a key."""
        del self._store[key]

    def list_keys(self, prefix: str = "") -> List[str]:
        """List all keys, optionally filtered by prefix."""
        if prefix:
            return [k for k in self._store if k.startswith(prefix)]
        return list(self._store.keys())

