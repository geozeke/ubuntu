#!/usr/bin/env python3
"""Configure VM instances created with Multipass.

Raises
------
RuntimeError
    If Python is not at the minimum required version.
"""

import argparse
from pathlib import Path
from typing import Any

from library.classes import Labels
from library.environment import DEBUG
from library.environment import HOME
from library.environment import PASS
from library.environment import SHELL
from library.environment import VIM
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
        Creating new directories
        Setting up vim
        Creating new user {args.user}
        Adding {args.user} to sudoers
        Enabling remote login with ssh
        Installing nala
        Installing zsh
        Installing OhMyZsh
        Installing OhMyZsh Full-autoupdate
        Installing powerlevel10k theme
        Copying dot files
        """
    )

    # ------------------------------------------

    # Step 1: Initialize lists for running many arguments. When running
    # commands with generic string targets, the "targets" array will be used.
    # Commands with special target-types are shown below.

    labels.next()
    dir_targets: list[Path] = []
    file_targets: list[tuple[Any, Any]] = []
    src: str | Path = ""
    dest: str | Path = ""
    target: str | Path = ""
    print(PASS)

    # ------------------------------------------

    # Step 2: Create new directories

    labels.next()
    dir_targets = [HOME / ".vim/colors"]
    for target in dir_targets:
        if DEBUG:
            print(f"\nMaking: {str(target)}")
        else:
            target.mkdir(parents=True, exist_ok=True)
    print(PASS)

    # ------------------------------------------

    # Step 3: Configure vim

    labels.next()
    file_targets = [
        (VIM / "vimrc.txt", HOME / ".vimrc"),
        (VIM / "vimcolors/*", HOME / ".vim/colors"),
    ]
    copy_files(file_targets)
    print(PASS)

    # ------------------------------------------

    # Step 4: Create new user

    labels.next()
    cmd = f"sudo useradd -m -p $(openssl passwd -1 {args.passwd}) {args.user}"
    print(run_one_command(cmd))

    # ------------------------------------------

    # Step 5: Add new user to sudoers

    labels.next()
    cmd = f"sudo usermod -aG sudo {args.user}"
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

    # Step 9: Install OhMyZsh

    labels.next()
    src = "https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/"
    cmd = f'$curl -fsSL {src}install.sh "" --unattended'
    print(run_one_command(cmd))

    # ------------------------------------------

    # Step 10: Install OhMyZsh Full-autoupdate

    labels.next()
    src = "https://github.com/Pilaton/OhMyZsh-full-autoupdate.git"
    dest = "${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/ohmyzsh-full-autoupdate"
    cmd = f"git clone --depth=1 {src} {dest}"
    print(run_one_command(cmd))

    # ------------------------------------------

    # Step 11: Install powerlevel10k theme

    labels.next()
    src = "https://github.com/romkatv/powerlevel10k.git"
    dest = "${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/themes/powerlevel10k"
    cmd = f"git clone --depth=1 {src} {dest}"
    print(run_one_command(cmd))

    # ------------------------------------------

    # Step 12: Copying dot files

    labels.next()
    file_targets = [
        (SHELL / "zshrc.txt", HOME / ".zshrc"),
        (SHELL / "p10k.txt", HOME / ".p10k.zsh"),
    ]
    copy_files(file_targets)
    print(PASS)

    # ------------------------------------------

    # Done

    msg = """Setup script is complete. If all steps above are marked
    with green checkmarks, the multipass Ubuntu instance is ready to go.
    You must reboot your VM instance now for the changes to take effect.
    Log back in with the username you created and immediately change the
    shell to zsh using the \"chsh\" command. Logout and log back in and
    you should be all set. If any steps above show a red \"X\", there
    was an error during installation."""
    print(f"\n{wrap_tight(msg)}\n")

    return


def main():  # noqa
    if result := min_python_version():
        raise RuntimeError(result)

    msg = """This script will configure a Ubuntu VM instance created
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
    print(args.user)
    #    task_runner()

    return


if __name__ == "__main__":
    main()
