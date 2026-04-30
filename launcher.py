import tkinter as tk
from tkinter import simpledialog
import subprocess
import os
import sys

def run_launcher():
    root = tk.Tk()
    root.withdraw() # Hide the main window

    # Ask for command
    command = simpledialog.askstring("DevForge CLI Launcher", "Enter DevForge command (e.g., tickets list, login, whoami):")
    
    if command:
        # Construct the path to devforge.exe
        # Assuming devforge.exe is in the same directory or in C:\DevForgeCLI
        exe_path = "devforge.exe"
        if not os.path.exists(exe_path):
            exe_path = r"C:\DevForgeCLI\devforge.exe"
            
        if os.path.exists(exe_path):
            # Run in a new terminal window that stays open (/k)
            subprocess.Popen(f'start cmd /k "{exe_path} {command}"', shell=True)
        else:
            tk.messagebox.showerror("Error", f"Could not find devforge.exe at {exe_path}. Please install the CLI first.")
    
    root.destroy()

if __name__ == "__main__":
    run_launcher()
