#!/usr/bin/env python3

"""Patch files and run scripts to support network connections at USNA.

Raises
------
RuntimeError
    If Python is not at the minimum required version.
"""

# Author: Peter Nardi
# Date: 06/17/22
# License: (see MIT License at the end of this file)

# Title: USNA Patching Script

# This script installs a patched openssl configuration file and runs the
# necessary scripts to support networking on the USNA mission network.

# Imports

import argparse
import tempfile
import textwrap

from library import Environment
from library import clear
from library import minPythonVersion
from library import runOneCommand

# -------------------------------------------------------------------


def runScript(args, e):
    """Patch openssl configuration and run certificate scripts.

    Parameters
    ----------
    e : Environment
        All the environment variables, saved as attributes in an
        Environment object.
    """
    clear()

    # ------------------------------------------

    # Setup status labels

    labels = []
    labels.append('System initialization')
    labels.append('Patching openssl configuration')
    labels.append('Updating system certificates')
    labels.append('Updating browser certificates')
    pad = len(max(labels, key=len)) + 3

    # ------------------------------------------

    # Step 0: Capture sudo permissions

    msg = "Please enter your password if prompted."
    print(f'\n{textwrap.fill(msg)}\n')
    # Push a dummy sudo command just to force password entry before first
    # command. This will avoid having the password prompt come in the middle of
    # a label when providing status
    runOneCommand(e, 'sudo ls'.split())

    # ------------------------------------------

    # Step 1: System initialization. Right now, it's just a placeholder for
    # future capability.

    print(f'{labels.pop(0):.<{pad}}', end='', flush=True)
    print(e.PASS)

    # ------------------------------------------

    # Step 2: Patch openssl

    if args.mode == 'system':
        print(f'{labels.pop(0):.<{pad}}', end='', flush=True)
        target = '/usr/lib/ssl/openssl.cnf'
        command = f'sudo cp -f {e.SYSTEM}/openssl.cnf {target}'
        print(runOneCommand(e, command.split()))
    else:
        labels.pop(0)

    # ------------------------------------------

    # Step 3: Update certificates

    fname = f'{tempfile.NamedTemporaryFile().name}.sh'

    if args.mode == 'system':
        url = 'apt.cs.usna.edu/ssl/install-ssl-system.sh'
        labels.pop(1)
    else:
        url = 'apt.cs.usna.edu/ssl/install-ssl-browsers.sh'
        labels.pop(0)

    commands = []
    commands.append(f'curl -o {fname} {url}')
    commands.append(f'chmod 754 {fname}')
    commands.append(f'{fname}')

    print(f'{labels.pop(0):.<{pad}}', end='', flush=True)

    success = True
    for command in commands:
        if runOneCommand(e, command.split()) != e.PASS:
            success = False
            break

    # Step 4: Cleanup tmp file and report status

    if success:
        command = f'rm -f {fname}'
        print(runOneCommand(e, command.split()))
    else:
        print(e.FAIL)
    print()

    # ------------------------------------------

    return

# -------------------------------------------------------------------


def main():  # noqa

    # Get a new Environment variable with all the necessary properties
    # initialized.

    e = Environment()
    if (result := minPythonVersion(e)) is not None:
        raise RuntimeError(result)

    msg = """This script installs a patched openssl configuration file
    and runs the necessary certificate scripts to support networking
    on the USNA mission network. You will be prompted for your password
    during installation."""

    epi = "Latest update: 06/17/22"

    parser = argparse.ArgumentParser(description=msg, epilog=epi)

    msg = 'Include one of the following options indicating where '
    msg += 'to apply patches: system, browser'
    parser.add_argument('mode',
                        choices=['system', 'browser'],
                        type=str,
                        help=msg)

    args = parser.parse_args()
    runScript(args, e)

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
