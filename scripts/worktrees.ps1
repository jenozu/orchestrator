param(
  [Parameter(Mandatory=$true)][ValidateSet('create','remove')] [string]$Cmd,
  [Parameter(Mandatory=$true)] [string]$Branch,
  [string]$Path
)

if (-not $Path) { $Path = "worktrees/$Branch" }

if ($Cmd -eq 'create') {
  git fetch origin | Out-Null
  $current = git rev-parse --abbrev-ref HEAD 2>$null
  if (-not $current) { $current = 'main' }
  git worktree add -B $Branch $Path "origin/$current"
  Write-Host "Worktree created at $Path for branch $Branch"
}
elseif ($Cmd -eq 'remove') {
  git worktree remove $Path --force | Out-Null
  git branch -D $Branch | Out-Null
  Write-Host "Worktree removed for branch $Branch"
}
else {
  throw "Unknown command: $Cmd"
}

