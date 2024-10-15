#!/usr/bin/env python3
"""Configure Ubuntu VM server instances.

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
        Verifying zsh installation
        Installing OhMyZsh
        Installing OhMyZsh Full-autoupdate
        Installing powerlevel10k theme
        Copying dot files
        """
    )

    # ------------------------------------------

    # Step 1: Initialize lists for running many arguments. When running
    # commands with generic string targets, the "targets" array will be
    # used. Commands with special target-types are shown below.

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
        (VIM / "vimrc.conf", HOME / ".vimrc"),
        (VIM / "vimcolors/*", HOME / ".vim/colors"),
    ]
    copy_files(targets=file_targets)
    print(PASS)

    # ------------------------------------------

    # Step 4: Verify zsh

    labels.next()
    cmd = "sudo apt install zsh -y"
    print(run_one_command(cmd=cmd))

    # ------------------------------------------

    # Step 5: Install OhMyZsh

    labels.next()
    src = "https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/"
    cmd = f"{src}install.sh"
    print(run_shell_script(shell="sh", script=cmd, options='"" --unattended'))

    # ------------------------------------------

    # Step 6: Install OhMyZsh Full-autoupdate

    labels.next()
    custom_zsh_home = HOME / ".oh-my-zsh/custom"
    src = "https://github.com/Pilaton/OhMyZsh-full-autoupdate.git"
    dest = f"{custom_zsh_home}/plugins/ohmyzsh-full-autoupdate"
    cmd = f"git clone --depth=1 {src} {dest}"
    print(run_one_command(cmd=cmd))

    # ------------------------------------------

    # Step 7: Install powerlevel10k theme

    labels.next()
    src = "https://github.com/romkatv/powerlevel10k.git"
    dest = f"{custom_zsh_home}/themes/powerlevel10k"
    cmd = f"git clone --depth=1 {src} {dest}"
    print(run_one_command(cmd=cmd))

    # ------------------------------------------

    # Step 8: Copying dot files

    labels.next()
    file_targets = [
        (SHELL / "zshrc.conf", HOME / ".zshrc"),
        (SHELL / "p10k.conf", HOME / ".p10k.zsh"),
    ]
    copy_files(targets=file_targets)
    print(PASS)

    # ------------------------------------------

    # Done

    msg = """
    Setup script is complete. If all steps above are marked with green
    checkmarks, the Ubuntu instance is ready to go. Change your shell
    \"/bin/zsh\" using the \"chsh\" command. Logout and log back in and
    you should be all set. If any steps above show a red \"X\", there
    was an error during installation.
    """
    print(f"\n{wrap_tight(msg)}\n")

    return


def main():
    if result := min_python_version():
        raise RuntimeError(result)

    msg = """
    This script will configure a Ubuntu server instance. It will setup
    OhMyZsh & vim, and configure the VM with standardized settings.
    NOTE: Make sure to run the server_initialize.py script before
    running this one.
    """

    epi = "Latest update: 11/27/24"
    parser = argparse.ArgumentParser(description=msg, epilog=epi)

    args = parser.parse_args()
    task_runner(args)

    return


if __name__ == "__main__":
    main()
