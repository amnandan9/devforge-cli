import os
import subprocess
import sys

def main():
    # Launch the terminal emulator
    # If running as script
    cmd = [sys.executable, "devforge-terminal.py"]
    # If running as bundled EXE, it might be different, but for now:
    subprocess.Popen(cmd)

if __name__ == "__main__":
    main()
