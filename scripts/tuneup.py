#!/usr/bin/env python3
"""Tuneup the Ubuntu Virtual Machine.

Raises
------
RuntimeError
    If Python is not at the minimum required version.
"""

import argparse

from library.classes import Environment
from library.classes import Labels
from library.utilities import min_python_version
from library.utilities import run_one_command
from library.utilities import wrap_tight


def run_updates(args: argparse.Namespace, e: Environment) -> None:
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
        Scanning for updates to pip
        Scanning for updates to jupyter
        Scanning for updates to jupyter lab
        Scanning for updates to pytest
        Synchronizing jupyter notebooks""")

    # Ubuntu updates (verbose)

    commands = []
    commands.append('sudo apt update')
    commands.append('sudo apt upgrade -y')
    commands.append('sudo apt autoclean -y')
    commands.append('sudo apt autoremove -y')
    commands.append('sudo snap refresh')

    for cmd in commands:
        run_one_command(e, cmd, capture=False)

    # Perform additional updates if -a is selected

    if args.all:

        print('\nPerforming additional updates\n')

        # Pull updates to the ubuntu git repo. This facilitates installing
        # custom patches later.
        labels.next()
        cmd = f'git -C {e.HOME}/ubuntu pull'
        print(run_one_command(e, cmd))

        # Update selected Python packages. Start with pip itself to ensure
        # we've got the lastest version of the Python package installer.
        pips = ['pip', 'jupyter', 'jupyterlab', 'pytest']
        for pip in pips:
            pip_test = f'pip3 show {pip}'
            if run_one_command(e, pip_test) == e.PASS:
                labels.next()
                cmd = f'pip3 install --upgrade {pip}'
                print(run_one_command(e, cmd))
            else:  # Dump the label if the package is not installed
                labels.pop_first()

        # Sync jupyter notebooks
        labels.next()
        cmd = f'git -C {e.HOME}/.notebooksrepo pull'
        result = run_one_command(e, cmd)

        # Sync repo with local notebooks. Use the --delete option so the
        # destination directory always exactly mirrors the source directory.
        # Also use the --delete-excluded option in case a stray file from the
        # source, which should be included, makes its way to the destination.
        # Per the man page, leaving a trailing slash ('/') on the source
        # directory allows you to have a destination directory with a different
        # name.
        if result == e.PASS:
            src = f'{e.HOME}/.notebooksrepo/'
            dest = f'{e.HOME}/notebooks'
            exclude = f'{e.SYSTEM}/rsync_exclude.txt'
            cmd = f'rsync -rc --exclude-from={exclude} {src} {dest} --delete '
            cmd += '--delete-excluded'
            result = run_one_command(e, cmd)

        print(result)

    # Done

    msg = """All updates and upgrades are complete. A reboot is
    recommended to ensure that the changes take effect."""
    print(f'\n{wrap_tight(msg)}\n')

    return


def main():  # noqa

    # Get a new Environment variable with all the necessary properties
    # initialized.
    e = Environment()
    if (result := min_python_version(e)):
        raise RuntimeError(result)

    msg = """This script will perform updates of system files and
    software installed through Ubuntu Personal Package Archives (ppa).
    You will be prompted for your password during updating."""

    epi = "Latest update: 11/15/22"

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
    run_updates(args, e)

    return


if __name__ == '__main__':
    main()
