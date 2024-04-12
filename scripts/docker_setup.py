#!/usr/bin/env python3
"""Installs docker.

Raises
------
RuntimeError
    If Python is not at the minimum required version.
"""

import argparse
import getpass

from library.classes import Labels
from library.environment import PASS
from library.utilities import clear
from library.utilities import min_python_version
from library.utilities import run_one_command
from library.utilities import run_shell_script
from library.utilities import wrap_tight


def task_runner() -> None:
    """Install docker engine."""
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

    run_one_command("sudo ls")

    # ------------------------------------------

    # Step 1: System initialization.

    labels.next()
    print(PASS)

    # ------------------------------------------

    # Step 2: Install docker components

    labels.next()
    print(
        run_shell_script(
            script="https://get.docker.com",
            shell="sh",
            as_sudo=True,
        )
    )

    # Step 3: Add user to docker group.

    labels.next()
    cmd = f"sudo usermod -aG docker {getpass.getuser()}"
    print(run_one_command(cmd))

    msg = """Setup script is complete. You must reboot your VM now for
    the changes to take effect."""
    print(f"\n{wrap_tight(msg)}\n")

    return


def main():  # noqa
    if result := min_python_version():
        raise RuntimeError(result)

    msg = """This script will install Docker Engine, which is the
    underlying client-server technology that builds and runs containers
    using Docker\'s components and services. It will also install Docker
    Compose which is a tool to help define and share multi-container
    applications. With Compose, you can create a YAML file to define the
    services and with a single command, can spin everything up or tear
    it all down."""

    epi = "Latest update: 04/12/24"

    parser = argparse.ArgumentParser(description=msg, epilog=epi)
    parser.parse_args()
    task_runner()

    return


if __name__ == "__main__":
    main()
