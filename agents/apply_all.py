"""Batch edit proposal and application for Cursor Apply All integration.

This module provides utilities to group compatible edits from multiple subagents
and format them for Cursor's batch application feature.
"""
from typing import Any, Dict, List, Set


class EditProposal:
    """Represents a proposed atomic edit from a subagent."""

    def __init__(
        self,
        file_path: str,
        old_string: str,
        new_string: str,
        agent_id: str,
        rationale: str = "",
    ):
        self.file_path = file_path
        self.old_string = old_string
        self.new_string = new_string
        self.agent_id = agent_id
        self.rationale = rationale


class EditGrouper:
    """Groups compatible edits and prepares batch apply."""

    def __init__(self):
        self._proposals: List[EditProposal] = []

    def add(self, proposal: EditProposal) -> None:
        """Add a proposal to the group."""
        self._proposals.append(proposal)

    def group_by_file(self) -> Dict[str, List[EditProposal]]:
        """Group proposals by target file."""
        by_file: Dict[str, List[EditProposal]] = {}
        for prop in self._proposals:
            by_file.setdefault(prop.file_path, []).append(prop)
        return by_file

    def check_conflicts(self) -> Dict[str, List[str]]:
        """Detect overlapping edits to the same file.

        Returns a dict mapping file paths to lists of conflicting agent IDs.
        """
        conflicts: Dict[str, List[str]] = {}
        by_file = self.group_by_file()
        for path, props in by_file.items():
            if len(props) > 1:
                # Simplified: multiple edits to same file may conflict
                conflicts[path] = [p.agent_id for p in props]
        return conflicts

    def to_cursor_format(self) -> List[Dict[str, Any]]:
        """Convert proposals to Cursor's apply-all format.

        This is a placeholder; actual format depends on Cursor's API.
        """
        grouped = self.group_by_file()
        cursor_edits = []
        for file_path, props in grouped.items():
            # For now, just document the structure
            cursor_edits.append({
                "file": file_path,
                "edits": [
                    {
                        "old": p.old_string,
                        "new": p.new_string,
                        "agent": p.agent_id,
                        "rationale": p.rationale,
                    }
                    for p in props
                ],
            })
        return cursor_edits


def propose_from_agent(
    agent_id: str,
    outputs: Dict[str, Any],
    worktree_path: str = ".",
) -> List[EditProposal]:
    """Convert agent outputs to edit proposals.

    This is a stub; real implementation would parse agent outputs.
    """
    proposals = []
    # Example: if agent outputs contain file edits
    if "edits" in outputs:
        for edit in outputs.get("edits", []):
            proposals.append(
                EditProposal(
                    file_path=edit.get("path", ""),
                    old_string=edit.get("old", ""),
                    new_string=edit.get("new", ""),
                    agent_id=agent_id,
                    rationale=edit.get("rationale", ""),
                )
            )
    return proposals

