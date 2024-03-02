#!/usr/bin/env python3
"""Initialize a new multipass instance.

Raises
------
RuntimeError
    If Python is not at the minimum required version.
"""

import argparse
from pathlib import Path
from typing import Any

from library.classes import Labels
from library.environment import PASS
from library.environment import SHELL
from library.utilities import clear
from library.utilities import copy_files
from library.utilities import min_python_version
from library.utilities import run_one_command
from library.utilities import wrap_tight


def task_runner(args: argparse.Namespace) -> None:
    """Perform VM configuration and setup."""
    clear()

    # ------------------------------------------

    # Setup status labels

    labels = Labels(
        f"""
        System initialization
        Creating user {args.user}
        Adding user {args.user} to sudoers
        Installing nala
        Installing zsh
        Enabling remote login with ssh
        """
    )

    # ------------------------------------------

    # Step 1: Initialize lists for running many arguments. When running
    # commands with generic string targets, the "targets" array will be used.
    # Commands with special target-types are shown below.

    labels.next()
    file_targets: list[tuple[Any, Any]] = []
    dest: str | Path = ""
    target: str | Path = ""
    print(PASS)

    # ------------------------------------------

    # Step 2: Create new user

    labels.next()
    cmd = f"sudo useradd -m -p $(openssl passwd -1 {args.passwd}) {args.user}"
    print(run_one_command(cmd))

    # ------------------------------------------

    # Step 5: Add new user to sudoers

    labels.next()
    cmd = f"sudo usermod -aG sudo {args.user}"
    print(run_one_command(cmd))

    # ------------------------------------------

    # Step 7: Install nala

    labels.next()
    cmd = "sudo apt install nala"
    print(run_one_command(cmd))

    # ------------------------------------------

    # Step 8: Install zsh

    labels.next()
    cmd = "sudo apt install zsh"
    print(run_one_command(cmd))

    # ------------------------------------------

    # Step 6: Enable remote login with ssh

    labels.next()
    target = "60-cloudimg-settings.conf"
    dest = f"/etc/ssh/sshd_config.d/{target}"
    file_targets = [(SHELL / "{target}", dest)]
    copy_files(file_targets)
    print(PASS)

    # ------------------------------------------

    # Done

    msg = f"""Initialization script is complete. If all steps above are
    marked with green checkmarks, the multipass Ubuntu instance is ready
    to go. You must reboot your VM instance now for the changes to take
    effect. Log back in as {args.user} and run
    ~/.ubuntu/scripts/multipass_configure.py. If any steps above show a
    red \"X\", there was an error during installation."""
    print(f"\n{wrap_tight(msg)}\n")

    return


def main():  # noqa
    if result := min_python_version():
        raise RuntimeError(result)

    msg = """This script will initialize a Ubuntu VM instance created
          with Multipass. It will create a new (non-root) user, defined
          on the command line with user/password, and add that user to
          the sudoers group. The VM instance will also be configured to
          allow for remote login using ssh."""

    epi = "Latest update: 03/02/24"

    parser = argparse.ArgumentParser(description=msg, epilog=epi)

    msg = """username for new account."""
    parser.add_argument(
        "-u",
        "--user",
        required=True,
        type=str,
        help=msg,
    )

    msg = """password for new account."""
    parser.add_argument(
        "-p",
        "--passwd",
        required=True,
        type=str,
        help=msg,
    )

    args = parser.parse_args()
    task_runner(args)

    return


if __name__ == "__main__":
    main()
