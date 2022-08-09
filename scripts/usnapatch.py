#!/usr/bin/env python3
"""Patch files and run scripts to support network connections at USNA.

Raises
------
RuntimeError
    If Python is not at the minimum required version.
"""

import argparse
import tempfile

from library import Environment
from library import Labels
from library import clear
from library import minPythonVersion
from library import runOneCommand


def runScript(args: argparse.Namespace, e: Environment) -> None:
    """Patch openssl configuration and run certificate scripts.

    Parameters
    ----------
    args : argparse.Namespace
        This will contain the argparse object, which allows us to
        extract the mode. The mode determines which operation to
        perform: system, browser.
    e : Environment
        All the environment variables saved as attributes in an
        Environment object.
    """
    clear()

    # ------------------------------------------

    # Setup status labels

    labels = Labels("""
        System initialization
        Patching openssl configuration
        Updating system certificates
        Updating browser certificates""")

    # ------------------------------------------

    # Step 0: Capture sudo permissions

    print("\nPlease enter your password if prompted.\n")
    # Push a dummy sudo command just to force password entry before first
    # command. This will avoid having the password prompt come in the middle of
    # a label when providing status
    runOneCommand(e, 'sudo ls'.split())

    # ------------------------------------------

    # Step 1: System initialization. Right now it's just a placeholder for
    # future capability.

    labels.next()
    print(e.PASS)

    # ------------------------------------------

    # Step 2: Patch openssl

    if args.mode == 'system':
        labels.next()
        target = '/usr/lib/ssl/openssl.cnf'
        command = f'sudo cp -f {e.SYSTEM}/openssl.cnf {target}'
        print(runOneCommand(e, command.split()))
    else:
        labels.popfirst()

    # ------------------------------------------

    # Step 3: Update certificates

    fname = f'{tempfile.NamedTemporaryFile().name}.sh'

    if args.mode == 'system':
        url = 'apt.cs.usna.edu/ssl/install-ssl-system.sh'
        labels.poplast()  # Discard the trailing label
    else:
        url = 'apt.cs.usna.edu/ssl/install-ssl-browsers.sh'
        labels.popfirst()  # Discard the leading label

    commands = []
    commands.append(f'curl -o {fname} {url}')
    commands.append(f'chmod 754 {fname}')
    commands.append(f'{fname}')

    labels.next()

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

    epi = "Latest update: 08/03/22"

    parser = argparse.ArgumentParser(description=msg, epilog=epi)

    msg = """Include one of the following options indicating where
    to apply patches: system, browser"""
    parser.add_argument('mode',
                        choices=['system', 'browser'],
                        type=str,
                        help=msg)

    args = parser.parse_args()
    runScript(args, e)

    return


if __name__ == '__main__':
    main()
