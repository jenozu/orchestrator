# PowerShell script to run quick test with API key
# Usage: .\run_test_with_key.ps1

param(
    [Parameter(Mandatory=$true)]
    [string]$ApiKey
)

Write-Host "Setting OPENAI_API_KEY..." -ForegroundColor Yellow
$env:OPENAI_API_KEY = $ApiKey

Write-Host "Running quick test..." -ForegroundColor Yellow
python quick_test.py

