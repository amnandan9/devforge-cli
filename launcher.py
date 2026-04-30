import tkinter as tk
from tkinter import simpledialog
import subprocess
import os
import sys

def run_launcher():
    root = tk.Tk()
    root.title("DevForge CLI Launcher")
    root.geometry("400x500")
    root.configure(bg="#0c0c0c")
    
    # Custom Styles
    bg_color = "#0c0c0c"
    accent_color = "#9b59b6"
    text_color = "#ffffff"
    btn_bg = "#1a1a2e"
    
    # Header
    header = tk.Label(root, text="DEVFORGE", font=("Orbitron", 24, "bold"), bg=bg_color, fg=accent_color, pady=20)
    header.pack()
    
    subtitle = tk.Label(root, text="System Command Center", font=("Inter", 10), bg=bg_color, fg="#888", pady=0)
    subtitle.pack()

    # Buttons Frame
    btn_frame = tk.Frame(root, bg=bg_color, pady=30)
    btn_frame.pack(fill="both", expand=True)

    def execute_cmd(command):
        exe_path = "devforge.exe"
        if not os.path.exists(exe_path):
            exe_path = r"C:\DevForgeCLI\devforge.exe"
            
        if os.path.exists(exe_path):
            subprocess.Popen(f'start cmd /k "{exe_path} {command}"', shell=True)
        else:
            from tkinter import messagebox
            messagebox.showerror("Error", f"Could not find devforge.exe at {exe_path}")

    def custom_cmd():
        cmd = simpledialog.askstring("Custom Command", "Enter DevForge command:")
        if cmd: execute_cmd(cmd)

    # Professional Buttons
    commands = [
        ("👤 User Profile", "whoami"),
        ("💎 Reputation", "reputation"),
        ("🎫 List Tickets", "tickets list"),
        ("🔑 Login System", "login"),
        ("🚀 My Projects", "projects"),
        ("📦 Code Snippets", "snippets"),
    ]

    for text, cmd in commands:
        btn = tk.Button(btn_frame, text=text, font=("Inter", 11, "bold"), 
                        bg=btn_bg, fg=text_color, activebackground=accent_color, 
                        activeforeground="#fff", bd=0, pady=10, width=25,
                        command=lambda c=cmd: execute_cmd(c))
        btn.pack(pady=5)
        btn.bind("<Enter>", lambda e, b=btn: b.configure(bg="#2a2a4e"))
        btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=btn_bg))

    custom_btn = tk.Button(btn_frame, text="⌨️ Custom Command...", font=("Inter", 10, "italic"),
                           bg=bg_color, fg="#888", activebackground=bg_color,
                           activeforeground=accent_color, bd=0, command=custom_cmd)
    custom_btn.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    run_launcher()
