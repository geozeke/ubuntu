#!/usr/bin/env python3

# Author: Peter Nardi
# Date: 12/30/21
# License: (see MIT License at the end of this file)

# Title: Environment

# Implementation of a class that defines environment variables for the Ubuntu
# scripting runtime environment. This allows for maintenance of these variables
# in one place, to be used with any Ubuntu VM script.

# Imports

from pathlib import Path

# -------------------------------------------------------------------


class Environment:

    def __init__(self):

        # Minimum required python version for Ubuntu VM scripts.

        self.MAJOR = 3
        self.MINOR = 8

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
        self.JUPYTER = self.UBUNTU/'jupyter'
        self.OHMYZSH = self.HOME/'.oh-my-zsh'
        self.SCRIPTS = self.UBUNTU/'scripts'
        self.SHELL = self.UBUNTU/'shell'
        self.SYSTEM = self.UBUNTU/'system'
        self.VIM = self.UBUNTU/'vim'

# -------------------------------------------------------------------


if __name__ == '__main__':
    pass

# ========================================================================

# MIT License

# Copyright 2019-2022 Peter Nardi

# Terms of use for source code:

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
