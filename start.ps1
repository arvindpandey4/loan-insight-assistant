# Start local development environment (No Docker)
Write-Host "Starting Loan Insight Assistant (Local Mode)..." -ForegroundColor Green

# Check if venv exists
if (-not (Test-Path ".\venv")) {
    Write-Host "Virtual environment not found. Creating one..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "Installing dependencies..." -ForegroundColor Cyan
    .\venv\Scripts\Activate.ps1
    pip install -r backend\requirements.txt
    pip install -r frontend\package.json 2>$null
}
else {
    Write-Host "Activating virtual environment..." -ForegroundColor Cyan
    .\venv\Scripts\Activate.ps1
}

# Start backend in background
Write-Host "Starting Backend API..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\backend'; ..\venv\Scripts\Activate.ps1; uvicorn main:app --reload --port 8000" -WindowStyle Normal

# Wait for backend to start
Write-Host "Waiting for backend to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Start frontend in background
Write-Host "Starting Frontend..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\frontend'; npm run dev" -WindowStyle Normal

# Wait for frontend to start
Start-Sleep -Seconds 2

Write-Host "`nApplications are running!" -ForegroundColor Green
Write-Host "Backend API: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "Frontend App: http://localhost:5173" -ForegroundColor Cyan
Write-Host "`nTo stop, run: .\stop.ps1" -ForegroundColor Yellow
Write-Host "Or close the PowerShell windows that opened." -ForegroundColor Yellow
