#!/usr/bin/env python3

"""Configure vim settings in Ubuntu."""

# Author: Peter Nardi
# Date: 06/25/22
# License: (see MIT License at the end of this file)

# Title: vim Setup script

# This script installs the necessary settings files and color schemes for a
# pleasant experience in vi.

# Imports

import argparse
import textwrap

from library import Environment
from library import clear
from library import copyFiles
from library import minPythonVersion

# -------------------------------------------------------------------


def runScript(e):
    """Configure vim.

    Parameters
    ----------
    e : Environment
        All the environment variables, saved as attributes in an
        Environment object.
    """
    clear()

    labels = []
    labels.append('System initialization')
    labels.append('Creating new directories')
    labels.append('Copying files')
    pad = len(max(labels, key=len)) + 3
    poplabel = (
        lambda x: print(f'{labels.pop(x):.<{pad}}', end='', flush=True))

    # Step 1. System initialization. Right now it's just a placeholder for
    # future capability.

    poplabel(0)
    print(e.PASS)

    # Step 2. Creating new directory

    poplabel(0)

    p = e.HOME/'.vim/colors'
    if e.DEBUG:
        print(p)
    else:
        p.mkdir(parents=True, exist_ok=True)

    print(e.PASS)

    # Step 3. Copying files

    poplabel(0)

    targets = []

    targets.append((e.VIM/'vimrc.txt', e.HOME/'.vimrc'))
    targets.append((e.VIM/'vimcolors/*', e.HOME/'.vim/colors'))

    copyFiles(e, targets)

    print(e.PASS)

    # Done

    msg = 'vim setup complete. You are now ready to use vi or vim and '
    msg += 'enjoy a pleasing visual experience.'
    print(f'\n{textwrap.fill(msg)}\n')

    return

# -------------------------------------------------------------------


def main():  # noqa

    # Get a new Environment variable with all the necessary properties
    # initialized.

    e = Environment()
    if (result := minPythonVersion(e)) is not None:
        raise RuntimeError(result)

    # Build a python argument parser

    msg = """This script installs the necessary settings files and
    color schemes for a pleasant visual experience in vi. NOTE: If
    you\'ve already run the ubuntu setup script, there's no need to run
    this script."""

    epi = "Latest update: 06/25/22"

    parser = argparse.ArgumentParser(description=msg, epilog=epi)
    parser.parse_args()
    runScript(e)

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
