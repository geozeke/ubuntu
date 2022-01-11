#!/usr/bin/env python3

# Author: Peter Nardi
# Date: 12/30/21
# License: (see MIT License at the end of this file)

# Title: Github Desktop for Linux Installation Script

# This script will install the GitHub Desktop client for Ubuntu Linux.

# Imports

import argparse
import textwrap

from library import clear
from library import Environment
from library import minPythonVersion
from library import runOneCommand

# -------------------------------------------------------------------


def runScript(e):

    clear()

    labels = []
    labels.append('System initialization')
    labels.append('Installing developer\'s public gpg key')
    labels.append('Mapping to developer ppa')
    labels.append('Refreshing')
    labels.append('Installing GitHub Desktop')
    pad = len(max(labels, key=len)) + 3

    # Start with a dummy ls command using sudo so we can prompt for the user's
    # password.

    print('Please enter password if prompted.\n')
    runOneCommand(e, 'sudo ls'.split())

    # Step 1. System initialization. Hold for future use.

    print(f'{labels.pop(0):.<{pad}}', end='', flush=True)
    print(e.PASS)

    # Step 2. Get the shiftkey gpg public key and save it to the appropriate
    # location.

    print(f'{labels.pop(0):.<{pad}}', end='', flush=True)

    keylocation = 'https://packagecloud.io/shiftkey/desktop/gpgkey'
    target = '/etc/apt/trusted.gpg.d/shiftkey-desktop.asc'
    cmd = f'sudo wget -qO {target} {keylocation}'

    print(runOneCommand(e, cmd.split()))

    # Step 3. Setup ppa mapping

    print(f'{labels.pop(0):.<{pad}}', end='', flush=True)

    src = e.SYSTEM/'githubdesktop.txt'
    dest = '/etc/apt/sources.list.d/packagecloud-shiftkey-desktop.list'
    cmd = f'sudo cp -f {src} {dest}'
    print(runOneCommand(e, cmd.split()))

    # Step 4. Refresh ppa

    print(f'{labels.pop(0):.<{pad}}', end='', flush=True)

    cmd = 'sudo apt update'

    print(runOneCommand(e, cmd.split()))

    # Step 4. Install GitHub Desktop

    print(f'{labels.pop(0):.<{pad}}', end='', flush=True)

    cmd = 'sudo apt install github-desktop'

    print(runOneCommand(e, cmd.split()))

    # Done

    msg = 'GitHub Desktop installation complete. Run the command '
    msg += '\'github-desktop\' and pin the icon to favorites.'
    print(f'\n{textwrap.fill(msg)}\n')

    return

# -------------------------------------------------------------------


def main():

    # Get a new Environment variable with all the necessary attributes
    # initialized.

    e = Environment()
    if (result := minPythonVersion(e)) is not None:
        raise RuntimeError(result)

    # Build a python argument parser

    msg = """This script will install the GitHub Desktop client for
    Ubuntu Linux."""

    epi = "Latest update: 12/30/21"

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
