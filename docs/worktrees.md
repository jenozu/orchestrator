# Git Worktrees

Use worktrees to isolate agent tasks into parallel branches and directories.

## Create a worktree

```bash
./scripts/worktrees.sh create feature/my-task
# or on Windows
powershell -File scripts/worktrees.ps1 create feature/my-task
```

This creates `worktrees/feature/my-task` checked out to branch `feature/my-task`.

## Remove a worktree

```bash
./scripts/worktrees.sh remove feature/my-task
# or on Windows
powershell -File scripts/worktrees.ps1 remove feature/my-task
```

Refer to Cursor worktrees docs for background: [worktrees](https://cursor.com/docs/configuration/worktrees).

