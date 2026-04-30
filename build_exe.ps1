# Build script for DevForge Git-Bash Style CLI
pip install -r requirements.txt
pip install pyinstaller

# Build the Terminal Emulator
pyinstaller --onefile --windowed devforge-terminal.py --name git-bash

# Build the Core CLI (no console for background use)
pyinstaller --onefile --console bin/cli.py --name devforge

# Organize into Git Bash structure
if (!(Test-Path "dist\bin")) { New-Item -ItemType Directory -Path "dist\bin" }
if (!(Test-Path "dist\cmd")) { New-Item -ItemType Directory -Path "dist\cmd" }
if (!(Test-Path "dist\etc")) { New-Item -ItemType Directory -Path "dist\etc" }
if (!(Test-Path "dist\usr")) { New-Item -ItemType Directory -Path "dist\usr" }
if (!(Test-Path "dist\tmp")) { New-Item -ItemType Directory -Path "dist\tmp" }

# Move core cli to bin
Move-Item -Path "dist\devforge.exe" -Destination "dist\bin\devforge.exe" -Force

# Create a simple LICENSE file
"MIT License`nCopyright (c) 2026 DevForge" | Out-File -FilePath "dist\LICENSE"

Write-Host "Build complete. Look in the 'dist' folder for the Git-Bash structure."
