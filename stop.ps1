# Stop local development environment
Write-Host "Stopping Loan Insight Assistant..." -ForegroundColor Yellow

# Kill uvicorn (backend) processes
Write-Host "Stopping Backend..." -ForegroundColor Cyan
Get-Process -Name "uvicorn" -ErrorAction SilentlyContinue | Stop-Process -Force
Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*uvicorn*" } | Stop-Process -Force

# Kill node (frontend) processes
Write-Host "Stopping Frontend..." -ForegroundColor Cyan
Get-Process -Name "node" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*vite*" } | Stop-Process -Force

# Clean up any remaining processes on ports 8000 and 5173
Write-Host "Freeing ports..." -ForegroundColor Cyan
$port8000 = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
if ($port8000) {
    Stop-Process -Id $port8000.OwningProcess -Force -ErrorAction SilentlyContinue
}

$port5173 = Get-NetTCPConnection -LocalPort 5173 -ErrorAction SilentlyContinue
if ($port5173) {
    Stop-Process -Id $port5173.OwningProcess -Force -ErrorAction SilentlyContinue
}

Write-Host "Application stopped." -ForegroundColor Green
Write-Host "Ports 8000 and 5173 are now free." -ForegroundColor Green
