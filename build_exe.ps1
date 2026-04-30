# Build script for DevForge CLI
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --onefile cli.py --name devforge
pyinstaller --onefile --windowed launcher.py --name DevForge_Launcher
Write-Host "Build complete. Executables are in the 'dist' folder."
