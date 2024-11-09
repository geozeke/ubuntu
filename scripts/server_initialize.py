#!/usr/bin/env python3
"""Initialize a new server instance.

Raises
------
RuntimeError
    If Python is not at the minimum required version.
"""

import argparse
import tempfile
import textwrap
from pathlib import Path

from library.classes import Labels
from library.environment import PASS
from library.environment import SHELL
from library.utilities import clear
from library.utilities import min_python_version
from library.utilities import run_one_command


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
        Turn off password for {args.user} when using sudo
        Installing zsh
        Enabling remote login with ssh
        """
    )

    # ------------------------------------------

    # Step 1: Initialize lists for running many arguments. When running
    # commands with generic string targets, the "targets" array will be
    # used. Commands with special target-types are shown below.

    labels.next()
    dest: str | Path = ""
    target: str | Path = ""
    print(PASS)

    # ------------------------------------------

    # Step 2: Create new user

    labels.next()
    cmd = f"openssl passwd -1 {args.passwd}"
    with tempfile.TemporaryFile(mode="w+") as f:
        run_one_command(cmd=cmd, std_out=f, capture=False)
        f.seek(0)
        crypt_passwd = f.read()
    cmd = f"sudo useradd -s /bin/bash -m -p {crypt_passwd} {args.user}"
    print(run_one_command(cmd=cmd))

    # ------------------------------------------

    # Step 3: Add new user to sudoers

    labels.next()
    cmd = f"sudo usermod -aG sudo {args.user}"
    print(run_one_command(cmd=cmd))

    # ------------------------------------------

    # Step 4: Turn off password requirement when using sudo

    labels.next()
    patch = f"{args.user} ALL=(ALL) NOPASSWD:ALL"
    target = "/etc/sudoers.d/90-cloud-init-users"
    cmd = f"sudo sh -c 'echo \"{patch}\" >> {target}'"
    print(run_one_command(cmd=cmd))

    # ------------------------------------------

    # Step 5: Install zsh

    labels.next()
    cmd = "sudo apt install zsh -y"
    print(run_one_command(cmd=cmd))

    # ------------------------------------------

    # Step 6: Enable remote login with ssh

    # Right now, this is setup to only patch config files on VMs created
    # with Multipass. For Raspberry Pi installations, ssh password
    # authentication is enabled when the Micro USB is flashed, so no
    # patching is required. Additional research is required for bare
    # metal installations on other hardware (e.g. Ubuntu Server on a
    # Dell Micro).

    labels.next()
    target = "60-cloudimg-settings.conf"
    src = SHELL / target
    dest = Path(f"/etc/ssh/sshd_config.d/{target}")
    if dest.exists():
        cmd = f"sudo cp {src} {dest}"
        print(run_one_command(cmd=cmd))
    else:
        print(PASS)

    # ------------------------------------------

    # Done

    msg = f"""
    Initialization script is complete. If all steps above are marked
    with green checkmarks, the Ubuntu server instance is ready to go.
    You must reboot now for the changes to take effect. Log back in as
    {args.user} and run ~/.ubuntu/scripts/server_configure.py. If any
    steps above show a red \"X\", there was an error during
    installation.
    """
    print(f"\n{textwrap.fill(text=" ".join(msg.split()))}\n")

    return


def main():
    if result := min_python_version():
        raise RuntimeError(result)

    msg = """
    This script will initialize a Ubuntu VM server instance. It will
    create a new (non-root) user, defined on the command line with
    user/password, and add that user to the sudoers group. The VM
    instance will also be configured to allow for remote login using
    ssh.
    """

    epi = "Latest update: 11/27/24"

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
