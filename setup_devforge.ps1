# DevForge CLI Installer
$InstallDir = "C:\DevForgeCLI"
$ExeSource = "dist\devforge.exe"

# Create Install Directory
if (!(Test-Path $InstallDir)) {
    New-Item -ItemType Directory -Path $InstallDir
}

# Copy Executables
Copy-Item -Path "dist\devforge.exe" -Destination "$InstallDir\devforge.exe" -Force
Copy-Item -Path "dist\DevForge_Launcher.exe" -Destination "$InstallDir\DevForge_Launcher.exe" -Force

# Create Desktop Shortcut for Launcher
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\DevForge Launcher.lnk")
$Shortcut.TargetPath = "$InstallDir\DevForge_Launcher.exe"
$Shortcut.IconLocation = "$InstallDir\DevForge_Launcher.exe,0"
$Shortcut.Description = "DevForge CLI - Quick Launcher"
$Shortcut.Save()

Write-Host "DevForge CLI installed successfully!"
Write-Host "Executable copied to: $InstallDir"
Write-Host "Shortcut created on Desktop."
Write-Host "You can now open DevForge CLI from your Desktop."
