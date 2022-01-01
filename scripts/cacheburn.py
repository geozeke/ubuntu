#!/usr/bin/env python3

# Author: Peter Nardi
# Date: 12/30/21
# License: (see MIT License at the end of this file)

# Title: cacheburn

# This script sweeps ~/shares to clear out cache directories, as well as delete
# selected files.

# Imports

import argparse
import textwrap

from library import Environment
from library import minPythonVersion
from library import runOneCommand

# -------------------------------------------------------------------


def burnitup(e):

    labels = []
    labels.append('Deleting __pycache__ directories')
    labels.append('Deleting .pytest_cache directories')
    labels.append('Deleting .ipynb_checkpoints directories')
    labels.append('Zapping pesky Icon files')
    labels.append('Crunching annoying desktop.ini files')
    pad = len(max(labels, key=len)) + 3

    # Start with cache directories:

    # NOTE: If this command were being run on the command line, you'd need to
    # escape the semicolon (\;)
    home = e.HOME/'shares'
    base = f'find {home} -name DIR -type d -exec rm -rvf {{}} ; -prune'

    commands = []
    commands.append(base.replace('DIR', '__pycache__'))
    commands.append(base.replace('DIR', '.pytest_cache'))
    commands.append(base.replace('DIR', '.ipynb_checkpoints'))

    for cmd in commands:
        print(f'{labels.pop(0):.<{pad}}', end='', flush=True)
        print(runOneCommand(e, cmd.split()))

    # Tee up files for deletion. You can sneak some other options in for the
    # find command if necessary.

    base = f'find {home} -name FILE -type f -delete'

    commands = []
    commands.append(base.replace('FILE', 'Icon? -size 0'))
    commands.append(base.replace('FILE', 'desktop.ini'))

    for cmd in commands:
        print(f'{labels.pop(0):.<{pad}}', end='', flush=True)
        print(runOneCommand(e, cmd.split()))

    return

# -------------------------------------------------------------------


def main():

    # Get a new Environment variable with all the necessary properties
    # initialized.

    e = Environment()
    if (result := minPythonVersion(e)) is not None:
        raise RuntimeError(result)

    # Build a python argument parser

    msg = """This script will scan the ~/shares directory to wipe
    caches, and delete other temporary files."""

    epi = "Latest update: 12/30/21"

    parser = argparse.ArgumentParser(
        description=msg, epilog=epi, prog='cacheburn')
    args = parser.parse_args()
    print()
    burnitup(e)
    print()

    return

# -------------------------------------------------------------------


if __name__ == '__main__':
    main()

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
