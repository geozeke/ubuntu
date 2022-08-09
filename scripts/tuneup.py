#!/usr/bin/env python3
"""Tuneup the Ubuntu Virtual Machine.

Raises
------
RuntimeError
    If Python is not at the minimum required version.
"""

import argparse
import textwrap

from library import Environment
from library import Labels
from library import minPythonVersion
from library import runOneCommand


def runUpdates(args: argparse.Namespace, e: Environment) -> None:
    """Perform system updates.

    Parameters
    ----------
    args : argparse.Namespace
        If `args.all` is set then update Python packages in addition
        to performing system updates.
    e : Environment
        All the environment variables saved as attributes in an
        Environment object.
    """
    labels = Labels("""
        Pulling updates to git repo
        Scanning for updates to jupyter
        Scanning for updates to jupyter lab
        Scanning for updates to pytest
        Synchronizing jupyter notebooks""")

    # Ubuntu updates (verbose)

    commands = []
    commands.append('sudo apt -y update')
    commands.append('sudo apt -y upgrade')
    commands.append('sudo apt -y autoclean')
    commands.append('sudo apt -y autoremove')
    commands.append('sudo snap refresh')

    for cmd in commands:
        runOneCommand(e, cmd.split(), capture=False)

    # Perform additional updates if -a is selected

    if args.all:

        print('\nPerforming additional updates\n')

        # Pull updates to the ubuntu git repo. This facilitates installing
        # custom patches later.
        labels.next()
        cmd = f'git -C {e.HOME}/ubuntu pull'
        print(runOneCommand(e, cmd.split()))

        # Update jupyter, jupyterlab & pytest (if installed)
        pips = ['jupyter', 'jupyterlab', 'pytest']
        for pip in pips:
            piptest = f'pip3 show {pip}'
            if runOneCommand(e, piptest.split()) == e.PASS:
                labels.next()
                cmd = f'pip3 install --upgrade {pip}'
                print(runOneCommand(e, cmd.split()))
            # Dump the label if the package is not installed
            else:
                labels.popfirst()

        # Sync jupyter notebooks
        labels.next()
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

    msg = """All updates and upgrades are complete. A reboot is
    recommended to ensure that the changes take effect."""
    print(f'\n{textwrap.fill(msg)}\n')

    return


def main():  # noqa

    # Get a new Environment variable with all the necessary properties
    # initialized.
    e = Environment()
    if (result := minPythonVersion(e)) is not None:
        raise RuntimeError(result)

    msg = """This script will perform updates of system files and
    software installed through Ubuntu Personal Package Archives (ppa).
    You will be prompted for your password during updating."""

    epi = "Latest update: 08/03/22"

    parser = argparse.ArgumentParser(description=msg,
                                     epilog=epi,
                                     prog='tuneup')

    msg = """In addition to updating Ubuntu system, ppa, and snap files,
    also update preinstalled pip3 packages in Python and synchronize
    installed jupyter notebooks."""
    parser.add_argument('-a', '--all',
                        help=msg,
                        action='store_true')

    args = parser.parse_args()
    runUpdates(args, e)

    return


if __name__ == '__main__':
    main()
