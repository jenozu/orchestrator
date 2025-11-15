# PowerShell script to run tests with proper UTF-8 encoding
# This prevents emoji encoding errors on Windows

Write-Host "Setting UTF-8 encoding..." -ForegroundColor Cyan
$env:PYTHONIOENCODING = "utf-8"

Write-Host "Running Rules Generator Test..." -ForegroundColor Green
Write-Host ""

python test_rules_generator.py

Write-Host ""
Write-Host "Test completed!" -ForegroundColor Green

