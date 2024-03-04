#!/usr/bin/env python3
"""Configure Ubuntu VM server instances.

Raises
------
RuntimeError
    If Python is not at the minimum required version.
"""

import argparse
import pwd
from pathlib import Path
from typing import Any

from library.classes import Labels
from library.environment import DEBUG
from library.environment import FAIL
from library.environment import HOME
from library.environment import PASS
from library.environment import SHELL
from library.environment import VIM
from library.utilities import clear
from library.utilities import copy_files
from library.utilities import min_python_version
from library.utilities import run_one_command
from library.utilities import run_shell_script
from library.utilities import wrap_tight


def task_runner(args) -> None:
    """Perform VM configuration and setup."""
    clear()

    # ------------------------------------------

    # Setup status labels

    labels = Labels(
        """
        System initialization
        Creating new directories
        Setting up vim
        Installing OhMyZsh
        Installing OhMyZsh Full-autoupdate
        Installing powerlevel10k theme
        Copying dot files
        Deleting default user account (ubuntu)
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
            print(f"\nMaking: {target}")
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

    # Step 4: Install OhMyZsh

    labels.next()
    src = "https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/"
    cmd = f"{src}install.sh"
    print(run_shell_script(shell="sh", script=cmd, options='"" --unattended'))

    # ------------------------------------------

    # Step 5: Install OhMyZsh Full-autoupdate

    zsh_home = HOME / ".oh-my-zsh/custom"

    labels.next()
    src = "https://github.com/Pilaton/OhMyZsh-full-autoupdate.git"
    dest = f"{zsh_home}/plugins/ohmyzsh-full-autoupdate"
    cmd = f"git clone --depth=1 {src} {dest}"
    print(run_one_command(cmd))

    # ------------------------------------------

    # Step 6: Install powerlevel10k theme

    labels.next()
    src = "https://github.com/romkatv/powerlevel10k.git"
    dest = f"{zsh_home}/themes/powerlevel10k"
    cmd = f"git clone --depth=1 {src} {dest}"
    print(run_one_command(cmd))

    # ------------------------------------------

    # Step 7: Copying dot files

    labels.next()
    file_targets = [
        (SHELL / "zshrc.txt", HOME / ".zshrc"),
        (SHELL / "p10k.txt", HOME / ".p10k.zsh"),
    ]
    copy_files(file_targets)
    print(PASS)

    # ------------------------------------------

    # Step 8: Delete default user account (if that option is selected).

    if args.delete:
        labels.next()
        try:
            pwd.getpwnam("ubuntu")
            cmd = "sudo deluser ubuntu"
            run_one_command(cmd)
            cmd = "sudo rm -rf /home/ubuntu"
            print(run_one_command(cmd))
        except KeyError:
            print(FAIL)
    else:
        labels.dump(1)

    # ------------------------------------------

    # Done

    msg = """Setup script is complete. If all steps above are marked
    with green checkmarks, the Ubuntu instance is ready to go.
    Change your shell \"/bin/zsh\" using the \"chsh\" command. Logout
    and log back in and you should be all set. If any steps above show a
    red \"X\", there was an error during installation."""
    print(f"\n{wrap_tight(msg)}\n")

    return


def main():  # noqa
    if result := min_python_version():
        raise RuntimeError(result)

    msg = """This script will configure a Ubuntu server instance. It
    will setup OhMyZsh & vim, and configure the VM with standardized
    settings. NOTE: Make sure to run the server_initialize.py script
    before running this one."""

    epi = "Latest update: 03/02/24"
    parser = argparse.ArgumentParser(description=msg, epilog=epi)

    msg = """use this option to delete the default user (ubuntu) that
    gets created when a new VM is instantiated."""
    parser.add_argument("-d", "--delete", help=msg, action="store_true")

    args = parser.parse_args()
    task_runner(args)

    return


if __name__ == "__main__":
    main()
