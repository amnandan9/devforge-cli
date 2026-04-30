# DevForge CLI Installer
$InstallDir = "C:\DevForgeCLI"
$ExeSource = "dist\devforge.exe"

# Create Install Directory
if (!(Test-Path $InstallDir)) {
    New-Item -ItemType Directory -Path $InstallDir
}

# Copy Executable
Copy-Item -Path $ExeSource -Destination "$InstallDir\devforge.exe" -Force

# Create Desktop Shortcut
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\DevForge CLI.lnk")
$Shortcut.TargetPath = "$InstallDir\devforge.exe"
$Shortcut.IconLocation = "$InstallDir\devforge.exe,0"
$Shortcut.Description = "DevForge CLI - Terminal Access"
$Shortcut.Save()

Write-Host "DevForge CLI installed successfully!"
Write-Host "Executable copied to: $InstallDir"
Write-Host "Shortcut created on Desktop."
Write-Host "You can now open DevForge CLI from your Desktop."
