import tkinter as tk
from tkinter import scrolledtext
import subprocess
import os
import sys
import threading

class DevForgeTerminal:
    def __init__(self, root):
        self.root = root
        self.root.title("DevForge Bash")
        self.root.geometry("900x600")
        self.root.configure(bg="#1a1a2e") # Dark Purple Background

        # Color Scheme
        self.bg_color = "#1a1a2e" # Premium Dark Purple
        self.fg_color = "#ffffff"
        self.accent_color = "#9b59b6"  # Vibrant Purple
        self.prompt_color = "#3FB950"  # Green
        
        # Text Area (Terminal Display)
        self.text_area = scrolledtext.ScrolledText(
            root, 
            bg=self.bg_color, 
            fg=self.fg_color, 
            insertbackground="#ffffff",
            font=("Consolas", 12),
            borderwidth=0,
            highlightthickness=0,
            padx=10,
            pady=10,
            undo=True
        )
        self.text_area.pack(fill="both", expand=True)
        
        # Custom Tags
        self.text_area.tag_config("prompt", foreground=self.prompt_color, font=("Consolas", 12, "bold"))
        self.text_area.tag_config("accent", foreground=self.accent_color, font=("Consolas", 12, "bold"))
        self.text_area.tag_config("error", foreground="#F85149")
        self.text_area.tag_config("output", foreground="#A8FFD8") # Light green/cyan for output

        # Command History
        self.history = []
        self.history_index = -1
        
        # Initial Welcome
        self.write("DEVFORGE BASH [Version 1.0.0]\n", "accent")
        self.write("(c) 2026 DevForge Corporation. All rights reserved.\n\n")
        
        self.show_prompt()

        # Key Bindings
        self.text_area.bind("<Return>", self.handle_enter)
        self.text_area.bind("<Up>", self.handle_up)
        self.text_area.bind("<Down>", self.handle_down)
        self.text_area.bind("<BackSpace>", self.handle_backspace)
        self.text_area.bind("<Control-c>", self.handle_ctrl_c)
        
        # Track the prompt start index
        self.prompt_start = "1.0"

    def write(self, text, tag="output"):
        self.text_area.insert(tk.END, text, tag)
        self.text_area.see(tk.END)

    def show_prompt(self):
        user = os.getlogin()
        path = os.getcwd().replace(os.path.expanduser("~"), "~")
        self.write(f"{user}@DevForge ", "prompt")
        self.write("MINGW64 ", "accent")
        self.write(f"{path}\n$ ", "prompt")
        self.prompt_start = self.text_area.index("insert")
        self.text_area.mark_set("insert", tk.END)

    def handle_backspace(self, event):
        if self.text_area.index("insert") <= self.prompt_start:
            return "break"

    def handle_up(self, event):
        if not self.history: return "break"
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.replace_current_command(self.history[self.history_index])
        return "break"

    def handle_down(self, event):
        if self.history_index > 0:
            self.history_index -= 1
            self.replace_current_command(self.history[self.history_index])
        elif self.history_index == 0:
            self.history_index = -1
            self.replace_current_command("")
        return "break"

    def replace_current_command(self, cmd):
        self.text_area.delete(self.prompt_start, tk.END)
        self.text_area.insert(self.prompt_start, cmd)

    def handle_ctrl_c(self, event):
        self.write("\n^C\n", "error")
        self.show_prompt()
        return "break"

    def handle_enter(self, event):
        cmd_line = self.text_area.get(self.prompt_start, tk.END).strip()
        self.text_area.insert(tk.END, "\n")
        
        if cmd_line:
            if not self.history or self.history[0] != cmd_line:
                self.history.insert(0, cmd_line)
            self.history_index = -1
            self.execute_command(cmd_line)
        else:
            self.show_prompt()
            
        return "break"

    def execute_command(self, cmd_line):
        cmd_parts = cmd_line.split()
        main_cmd = cmd_parts[0].lower()

        if main_cmd == "clear":
            self.text_area.delete("1.0", tk.END)
            self.show_prompt()
            return
        
        if main_cmd == "exit":
            self.root.quit()
            return

        # Execute in background thread
        threading.Thread(target=self.run_process, args=(cmd_line,)).start()

    def run_process(self, cmd_line):
        try:
            devforge_cmds = ["login", "whoami", "reputation", "tickets", "projects", "snippets", "config", "push-snippet"]
            first_word = cmd_line.split()[0]
            
            # Point to the bundled devforge.exe or bin/cli.py
            cli_path = os.path.join(os.path.dirname(__file__), "bin", "cli.py")
            
            if first_word in devforge_cmds:
                process = subprocess.Popen(
                    f'python "{cli_path}" {cmd_line}', 
                    shell=True, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    text=True
                )
            else:
                process = subprocess.Popen(
                    cmd_line, 
                    shell=True, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    text=True
                )
            
            stdout, stderr = process.communicate()
            
            if stdout: self.write(stdout)
            if stderr: self.write(stderr, "error")
            
        except Exception as e:
            self.write(f"Error: {str(e)}\n", "error")
        
        self.root.after(0, self.show_prompt)

if __name__ == "__main__":
    root = tk.Tk()
    # Add icon if possible, or just style
    app = DevForgeTerminal(root)
    root.mainloop()
