#!/usr/bin/env bash
set -euo pipefail

# Usage: ./scripts/worktrees.sh create <branch> [path]
#        ./scripts/worktrees.sh remove <branch>

cmd=${1:-}
branch=${2:-}
path=${3:-"worktrees/${branch}"}

if [[ -z "$cmd" || -z "$branch" ]]; then
  echo "Usage: $0 <create|remove> <branch> [path]" >&2
  exit 1
fi

if [[ "$cmd" == "create" ]]; then
  git fetch origin || true
  git worktree add -B "$branch" "$path" origin/$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo main)
  echo "Worktree created at $path for branch $branch"
elif [[ "$cmd" == "remove" ]]; then
  git worktree remove "$path" --force || true
  git branch -D "$branch" || true
  echo "Worktree removed for branch $branch"
else
  echo "Unknown command: $cmd" >&2
  exit 1
fi

