"""Environment for the ubuntu scripts.

All the paths, debugging flags, and pass/fail glyphs are created and
initialized here.
"""

from pathlib import Path

# Minimum required python version for Ubuntu VM scripts.
MAJOR = 3
MINOR = 10

# PASS and FAIL markers and flag for enabling debug mode.
GREEN = "\033[0;32;49m"
RED = "\033[0;31;49m"
COLOR_END = "\x1b[0m"

PASS = f"{GREEN}\u2714{COLOR_END}"
FAIL = f"{RED}\u2718{COLOR_END}"
DEBUG = False

# Paths in the repo for installation files. Note: Ubuntu is resolved in
# relation to this file (classes.py) to facilitate debugging. The repo
# should still be cloned in ~ per the setup instructions..
HOME = Path.home()
UBUNTU = Path(__file__).resolve().parents[2]
OHMYZSH = HOME / ".oh-my-zsh"
SCRIPTS = UBUNTU / "scripts"
SHELL = UBUNTU / "shell"
SYSTEM = UBUNTU / "system"
VIM = UBUNTU / "vim"
