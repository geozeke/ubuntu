#!/usr/bin/env python3

"""Install Python development tools."""

# Author: Peter Nardi
# Date: 01/17/22
# License: (see MIT License at the end of this file)

# Title: Python tools installation script

# This script will install several Python tools. The script installs the tools
# globally (not generally a good idea), but having this script allows for an
# "air gap" between these tools and the base Ubuntu installation. It's fine for
# an introductory class, but for more advanced students, either create and
# activate a Python virtual environment before running this script, or skip
# this script and install the tools in a Python virtual environment manually.

# Imports

import argparse
import textwrap

from library import Environment
from library import clear
from library import copyFiles
from library import minPythonVersion
from library import runOneCommand

# -------------------------------------------------------------------


def runScript(e):
    """Install development tools.

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
    labels.append('Installing jupyter')
    labels.append('Installing jupyter lab')
    labels.append('Installing pytest')
    pad = len(max(labels, key=len)) + 3

    # Step 1. System initialization. Right now, it's just a placeholder for
    # future capability.

    print(f'{labels.pop(0):.<{pad}}', end='', flush=True)
    print(e.PASS)

    # Step 2. Creating new directories

    print(f'{labels.pop(0):.<{pad}}', end='', flush=True)

    p = e.HOME/'.jupyter/lab/user-settings/@jupyterlab/notebook-extension/'
    if e.DEBUG:
        print(f'\nMaking: {str(p)}')
    else:
        p.mkdir(parents=True, exist_ok=True)

    print(e.PASS)

    # Step 3. Copying files

    print(f'{labels.pop(0):.<{pad}}', end='', flush=True)

    targets = []
    targets.append((e.JUPYTER/'tracker.jupyterlab-settings', p))

    copyFiles(e, targets)

    print(e.PASS)

    # Step 4, 5, 6 Install jupyter, jupyterlab & pytest

    base = 'pip3 install --upgrade TARGET'

    commands = []
    commands.append(base.replace('TARGET', 'jupyter'))
    commands.append(base.replace('TARGET', 'jupyterlab'))
    commands.append(base.replace('TARGET', 'pytest'))

    for cmd in commands:
        print(f'{labels.pop(0):.<{pad}}', end='', flush=True)
        print(runOneCommand(e, cmd.split()))

    # Done

    msg = 'Python tools installation complete. Install additional '
    msg += 'tools or reboot your VM now for the changes to take effect.'
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

    msg = """This script will install several Python tools.
    Specifically: jupyter, jupyterlab, and pytest. It\'s recommend that
    you create and activate a Python virtual environment before running
    this script, or skip this script and install the tools in a Python
    virtual environment manually."""

    epi = "Latest update: 01/17/22"

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
