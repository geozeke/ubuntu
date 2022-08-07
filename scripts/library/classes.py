#!/usr/bin/env python3
"""Support classes for ubuntu setup scripts."""

from pathlib import Path


class Environment:
    """Class for holding environment variables.

    This class sets up the environment for the ubuntu scripts. All the
    paths, debugging flags, and pass/fail glyphs are created and
    initialized here.
    """

    def __init__(self):

        # Minimum required python version for Ubuntu VM scripts.

        self.MAJOR = 3
        self.MINOR = 10

        # PASS and FAIL markers; flag for enabling debug mode; and an
        # environment variable to hold the result from running commands using
        # sub-process. These results may be needed in future use cases.

        self.PASS = '\033[0;32;49m' + u'\u2714' + '\x1b[0m'
        self.FAIL = '\033[0;31;49m' + u'\u2718' + '\x1b[0m'
        self.DEBUG = False
        self.RESULT = None

        # Paths in the repo for installation files.

        self.HOME = Path.home()
        # Ubuntu is resolved in relation to this file (classes.py) to
        # facilitate debugging. The repo should still be cloned in ~ per the
        # setup instructions..
        self.UBUNTU = Path(__file__).resolve().parents[2]
        self.ATOM = self.UBUNTU/'atom'
        self.GEDIT = self.UBUNTU/'gedit'
        self.OHMYZSH = self.HOME/'.oh-my-zsh'
        self.SCRIPTS = self.UBUNTU/'scripts'
        self.SHELL = self.UBUNTU/'shell'
        self.SYSTEM = self.UBUNTU/'system'
        self.VIM = self.UBUNTU/'vim'


if __name__ == '__main__':
    pass
