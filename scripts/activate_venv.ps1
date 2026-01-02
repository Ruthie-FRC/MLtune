# Auto-activation script for MLtune virtual environment (PowerShell)
# Add this to your PowerShell profile to automatically activate
# the virtual environment when you cd into this directory.
#
# To find your profile location, run in PowerShell:
#   echo $PROFILE
#
# Then add this line to your profile:
#   . C:\path\to\MLtune\activate_venv.ps1
#
# Or add the entire function to your profile directly.

function Invoke-MLtuneVenvActivation {
    $currentDir = Get-Location
    $mltuneRoot = $null

    # Try to find the MLtune directory by looking for mltune/ and START_TUNER.bat
    $searchDir = $currentDir
    while ($searchDir) {
        if ((Test-Path "$searchDir\mltune") -and (Test-Path "$searchDir\START_TUNER.bat")) {
            $mltuneRoot = $searchDir
            break
        }
        $parent = Split-Path -Parent $searchDir
        if ($parent -eq $searchDir) { break }
        $searchDir = $parent
    }

    # If we found the MLtune directory and not already in the venv
    if ($mltuneRoot -and $env:VIRTUAL_ENV -ne "$mltuneRoot\.venv") {
        # Create venv if it doesn't exist
        if (-not (Test-Path "$mltuneRoot\.venv")) {
            Write-Host "Creating virtual environment..."
            python -m venv "$mltuneRoot\.venv"

            # Install dependencies
            & "$mltuneRoot\.venv\Scripts\Activate.ps1"
            Write-Host "Installing dependencies..."
            python -m pip install --quiet --upgrade pip
            python -m pip install --quiet -r "$mltuneRoot\mltune\tuner\requirements.txt"
            python -m pip install --quiet -r "$mltuneRoot\dashboard\requirements.txt"
            Write-Host "✓ Virtual environment created and dependencies installed" -ForegroundColor Green
        } else {
            & "$mltuneRoot\.venv\Scripts\Activate.ps1"
            Write-Host "✓ Virtual environment activated (.venv)" -ForegroundColor Green
        }
    }

    # Deactivate if we've left the MLtune directory
    if (-not $mltuneRoot -and $env:VIRTUAL_ENV -and $env:VIRTUAL_ENV -like "*\.venv") {
        # Only deactivate if the venv is in a parent directory we've left
        $venvParent = Split-Path -Parent $env:VIRTUAL_ENV
        if (-not $currentDir.Path.StartsWith($venvParent)) {
            deactivate
            Write-Host "✓ Virtual environment deactivated" -ForegroundColor Green
        }
    }
}

# Hook into directory change
$ExecutionContext.InvokeCommand.LocationChangedAction = {
    Invoke-MLtuneVenvActivation
}

# Activate on shell startup if we're already in the directory
Invoke-MLtuneVenvActivation
