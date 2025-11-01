# Cursor Rules

## Coding Standards
- Prefer clear, maintainable code with descriptive names.
- Add tests for new features; keep coverage meaningful.
- Avoid deep nesting; use early returns and explicit types where applicable.

## Review Gates
- All PRs must pass CI (lint, tests, build) before merge.
- Large changes require an architectural note in `docs/`.

## Agent Guidelines
- Agents must propose atomic edits and reference related tasks.
- Agents should include brief rationale and affected files in PR descriptions.

## Security
- Never commit secrets. Use environment variables and secrets managers.
- Restrict tool access to the project workspace.

## RAG Policy (High-Level)
- Prefer branch-local context first, then main.
- Cite sources (file paths, PRs, commit hashes) in outputs.
