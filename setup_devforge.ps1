# DevForge Bash Installer
$InstallDir = "C:\Program Files\DevForgeBash"
if (!(Test-Path $InstallDir)) {
    New-Item -ItemType Directory -Path $InstallDir -Force
}

# Copy all files from dist to InstallDir
Copy-Item -Path "dist\*" -Destination $InstallDir -Recurse -Force

# Create Desktop Shortcut for git-bash.exe
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\DevForge Bash.lnk")
$Shortcut.TargetPath = "$InstallDir\git-bash.exe"
$Shortcut.IconLocation = "$InstallDir\git-bash.exe,0"
$Shortcut.Description = "DevForge Bash - Terminal Shell"
$Shortcut.Save()

Write-Host "DevForge Bash installed successfully!"
Write-Host "Location: $InstallDir"
Write-Host "Shortcut created on Desktop."
