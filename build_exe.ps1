# Build script for DevForge CLI
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --onefile cli.py --name devforge
Write-Host "Build complete. The executable is in the 'dist' folder."
