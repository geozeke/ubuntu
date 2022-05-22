#!/usr/bin/env python3

"""Tuneup the Ubuntu Virtual Machine.

Raises
------
RuntimeError
    If Python is not at the minimum required version.
"""

# Author: Peter Nardi
# Date: 05/22/22
# License: (see MIT License at the end of this file)

# Title: VM Tuneup Script

# This script will perform system updates to an Ubuntu VM.

# Imports

import argparse
import textwrap

from library import Environment
from library import minPythonVersion
from library import runOneCommand

# -------------------------------------------------------------------


def updatePIP(e, pip, labels, pad):
    """Update a single installed Python package.

    Parameters
    ----------
    e : Environment
        All the environment variables, saved as attributes in an
        Environment object.
    pip : str
        The Python packged to be updated.
    labels : [str]
        A list of strings. Strings are popped during execution and shown
        to the user to provide status on progress.
    pad : int
        A number to be used for padding output labels to keep consistent
        justification.
    """
    # Update pip package only if it's already installed
    piptest = f'pip3 show {pip}'
    if runOneCommand(e, piptest.split()) == e.PASS:
        print(f'{labels.pop(0):.<{pad}}', end='', flush=True)
        cmd = f'pip3 install --upgrade {pip}'
        print(runOneCommand(e, cmd.split()))

    # Dump the label if the package is not installed
    else:
        labels.pop(0)

    return

# -------------------------------------------------------------------


def runUpdates(args, e):
    """Perform system updates.

    Parameters
    ----------
    args : argparse
        If `args.all` is set, then update Python packages, in addition
        to performing system updates.
    e : Environment
        All the environment variables, saved as attributes in an
        Environment object.
    """
    labels = []
    labels.append('Pulling updates to git repo')
    labels.append('Scanning for updates to jupyter')
    labels.append('Scanning for updates to jupyter lab')
    labels.append('Scanning for updates to pytest')
    labels.append('Synchronizing jupyter notebooks')
    pad = len(max(labels, key=len)) + 3

    # Ubuntu updates (verbose)

    commands = []
    commands.append('sudo apt -y update')
    commands.append('sudo apt -y upgrade')
    commands.append('sudo apt -y autoremove')
    commands.append('sudo snap refresh')

    for cmd in commands:
        runOneCommand(e, cmd.split(), capture=False)

    # Perform additional updates if -a is selected

    if args.all:

        print('\nPerforming additional updates\n')

        # Pull updates to the ubuntu git repo. This facilitates installing
        # custom patches later.
        print(f'{labels.pop(0):.<{pad}}', end='', flush=True)
        cmd = f'git -C {e.HOME}/ubuntu pull'
        print(runOneCommand(e, cmd.split()))

        # Update jupyter, jupyterlab & pytest (if installed)
        pips = ['jupyter', 'jupyterlab', 'pytest']
        for pip in pips:
            updatePIP(e, pip, labels, pad)

        # Sync jupyter notebooks
        print(f'{labels.pop(0):.<{pad}}', end='', flush=True)
        cmd = f'git -C {e.HOME}/.notebooksrepo pull'
        result = runOneCommand(e, cmd.split())

        # Sync repo with local notebooks. Use the --delete option so the
        # destination directory always exactly mirrors the source directory.
        # Also skip syncing any git-related files. Per the man page, leaving a
        # trailing slash ('/') on the source directory allows you to have a
        # destination directory with a different name.
        if result == e.PASS:
            cmd = 'rsync -rc '
            cmd += '--exclude .git* --exclude LICENSE* --exclude README* '
            cmd += f'{e.HOME}/.notebooksrepo/ {e.HOME}/notebooks --delete'
            result = runOneCommand(e, cmd.split())

        print(result)

    # Done

    msg = 'All updates and upgrades are complete. A reboot is '
    msg += 'recommended to ensure that the changes take effect.'
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

    msg = """This script will perform updates of system files and
    software installed through Ubuntu Personal Package Archives (ppa).
    You will be prompted for your password during updating."""

    epi = "Latest update: 05/22/22"

    parser = argparse.ArgumentParser(description=msg,
                                     epilog=epi,
                                     prog='tuneup')

    msg = """In addition to updating Ubuntu system, ppa and snap files,
    also update preinstalled pip3 packages in Python and synchronize
    installed jupyter notebooks."""
    parser.add_argument('-a', '--all',
                        help=msg,
                        action='store_true')

    args = parser.parse_args()
    runUpdates(args, e)

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
