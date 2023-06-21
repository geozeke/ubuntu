#!/usr/bin/env python3
"""Installs docker.

Raises
------
RuntimeError
    If Python is not at the minimum required version.
"""

import argparse
import getpass

from library.classes import Environment
from library.classes import Labels
from library.utilities import clear
from library.utilities import min_python_version
from library.utilities import run_one_command
from library.utilities import run_shell_script
from library.utilities import wrap_tight


def task_runner(e: Environment) -> None:
    """Install docker engine.

    Parameters
    ----------
    e : Environment
        All the environment variables saved as attributes in an
        Environment object.
    """
    clear()

    # ------------------------------------------

    # Setup status labels

    labels = Labels(
        """
        System initialization
        Installing docker components
        Adding user to Docker group"""
    )

    # ------------------------------------------

    # Step 0: Capture sudo permissions

    print("\nPlease enter your password if prompted.\n")
    # Push a dummy sudo command just to force password entry before first
    # command. This will avoid having the password prompt come in the middle of
    # a label when providing status

    run_one_command(e, "sudo ls")

    # ------------------------------------------

    # Step 1: System initialization.

    labels.next()
    print(e.PASS)

    # ------------------------------------------

    # Step 2: Install docker components

    labels.next()
    print(
        run_shell_script(e, script="https://get.docker.com", shell="sh", as_sudo=True)
    )

    # Step 3: Add user to docker group.

    labels.next()
    cmd = f"sudo usermod -aG docker {getpass.getuser()}"
    print(run_one_command(e, cmd))

    msg = """Setup script is complete. You must reboot your VM now for
    the changes to take effect."""
    print(f"\n{wrap_tight(msg)}\n")

    return


def main():  # noqa
    # Get a new Environment variable with all the necessary properties
    # initialized.
    e = Environment()
    if result := min_python_version(e):
        raise RuntimeError(result)

    msg = """This script will install Docker Engine, which is the
    underlying client-server technology that builds and runs containers
    using Docker\'s components and services. It will also install Docker
    Compose which is a tool to help define and share multi-container
    applications. With Compose, you can create a YAML file to define the
    services and with a single command, can spin everything up or tear
    it all down."""

    epi = "Latest update: 06/16/23"

    parser = argparse.ArgumentParser(description=msg, epilog=epi)
    parser.parse_args()
    task_runner(e)

    return


if __name__ == "__main__":
    main()
