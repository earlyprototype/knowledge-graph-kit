# Knowledge Graph Kit - PowerShell Setup Launcher
# Run with: .\setup.ps1

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Knowledge Graph Kit - Setup Wizard" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ ERROR: Python not found!" -ForegroundColor Red
    Write-Host "  Please install Python 3.7+ from python.org" -ForegroundColor Yellow
    exit 1
}

# Check/Install dependencies
Write-Host ""
Write-Host "Checking dependencies..." -ForegroundColor Yellow

try {
    python -c "import yaml" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Installing dependencies..." -ForegroundColor Yellow
        pip install -r requirements.txt
        if ($LASTEXITCODE -ne 0) {
            Write-Host "✗ ERROR: Failed to install dependencies" -ForegroundColor Red
            exit 1
        }
    }
    Write-Host "✓ Dependencies OK" -ForegroundColor Green
} catch {
    Write-Host "✗ ERROR: Could not verify dependencies" -ForegroundColor Red
    exit 1
}

# Run wizard
Write-Host ""
Write-Host "Starting setup wizard..." -ForegroundColor Green
Write-Host ""

python setup_wizard.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "✗ Setup failed or was cancelled" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✓ Setup complete!" -ForegroundColor Green

