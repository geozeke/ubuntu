#!/usr/bin/env python3
"""Installs docker compose.

Raises
------
RuntimeError
    If Python is not at the minimum required version.
"""

import argparse
import os

from library.classes import Environment
from library.classes import Labels
from library.utilities import clear
from library.utilities import min_python_version
from library.utilities import run_one_command
from library.utilities import wrap_tight


def run_script(e: Environment) -> None:
    """Install docker compose.

    Parameters
    ----------
    e : Environment
        All the environment variables saved as attributes in an
        Environment object.
    """
    clear()

    # ------------------------------------------

    # Setup status labels

    labels = Labels("""
        System initialization
        Cloning compose repository
        Making docker compose binary (please be patient)
        Moving files into final position""")

    # ------------------------------------------

    # Step 0: Capture sudo permissions

    print("\nPlease enter your password if prompted.\n")
    # Push a dummy sudo command just to force password entry before first
    # command. This will avoid having the password prompt come in the middle of
    # a label when providing status

    run_one_command(e, 'sudo ls')

    # ------------------------------------------

    # Step 1: System initialization. Right now it's just a placeholder for
    # future capability.

    labels.next()
    print(e.PASS)

    # ------------------------------------------

    # Step 2: Cloning docker compose repo.

    labels.next()
    src = 'https://github.com/docker/compose.git'
    dest = e.HOME/'.compose'
    cmd = f'git clone {src} {dest} --depth 1'
    print(run_one_command(e, cmd))

    # Step 3: Make the compose binary.

    labels.next()
    os.chdir(e.HOME/'.compose')
    cmd = 'make binary'
    print(run_one_command(e, cmd))

    # Step 4: Move the binary into location and adjust permissions.

    labels.next()
    src = e.HOME/'.compose/bin/build/docker-compose'
    dest = '/usr/libexec/docker/cli-plugins/'
    cmd = f'sudo mv {src} {dest}'
    result = run_one_command(e, cmd)
    if result == e.PASS:
        dest = '/usr/libexec/docker/cli-plugins/docker-compose'
        cmd = f'sudo chmod 755 {dest}'
        result = run_one_command(e, cmd)
    print(result)

    msg = """Setup script is complete. If all steps above are marked
    with green checkmarks, Docker Compose is ready to go. There is no
    need for a reboot. If any steps above show a red \"X\", there was an
    error during installation."""
    print(f'\n{wrap_tight(msg)}\n')

    return


def main():  # noqa

    # Get a new Environment variable with all the necessary properties
    # initialized.
    e = Environment()
    if (result := min_python_version(e)):
        raise RuntimeError(result)

    msg = """This script will install docker compose."""

    epi = "Latest update: 11/06/22"

    parser = argparse.ArgumentParser(description=msg, epilog=epi)
    parser.parse_args()
    run_script(e)

    return


if __name__ == '__main__':
    main()