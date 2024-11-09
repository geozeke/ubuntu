#!/usr/bin/env python3
"""Install support for pyenv.

Raises
------
RuntimeError
    If Python is not at the minimum required version.
"""

import argparse
import textwrap

from library.classes import Labels
from library.environment import HOME
from library.environment import PASS
from library.environment import SHELL
from library.utilities import clear
from library.utilities import lean_text
from library.utilities import min_python_version
from library.utilities import run_many_arguments
from library.utilities import run_one_command
from library.utilities import run_shell_script


def task_runner() -> None:
    """Perform pyenv setup steps."""
    clear()

    # ------------------------------------------

    # Setup status labels

    labels = Labels(
        """
        System initialization
        Updating package index
        Checking python build dependencies
        Installing pyenv and tools
        Adjusting shell environments
        """
    )

    # Step 0

    msg = """Please enter your password if prompted."""
    print(msg)

    # Push a dummy sudo command just to force password entry before
    # first ppa pull. This will avoid having the password prompt come in
    # the middle of a label when providing status

    run_one_command("sudo ls")

    # ------------------------------------------

    # Step 1: System initialization.

    labels.next()
    print(PASS)

    # ------------------------------------------

    # Step 2: Update package index

    labels.next()
    cmd = "sudo apt update"
    print(run_one_command(cmd=cmd))

    # ------------------------------------------

    # Step 3: Check dependencies

    labels.next()
    cmd = "sudo apt install TARGET -y"
    targets: list[str] = [
        "make",
        "build-essential",
        "libssl-dev",
        "zlib1g-dev",
        "libbz2-dev",
        "libreadline-dev",
        "libsqlite3-dev",
        "wget",
        "curl",
        "libncursesw5-dev",
        "xz-utils",
        "tk-dev",
        "libxml2-dev",
        "libxmlsec1-dev",
        "libffi-dev",
        "liblzma-dev",
    ]
    print(run_many_arguments(cmd=cmd, targets=targets))

    # ------------------------------------------

    # Step 4: Install pyenv

    labels.next()
    print(run_shell_script("https://pyenv.run"))

    # ------------------------------------------

    # Step 5: Adjust shell environments

    labels.next()

    # Setup variables with file locations
    support = SHELL / "pyenvsupport.conf"
    bash = HOME / ".bashrc"
    zsh = HOME / ".zshrc"
    # Check to see if the adjustments have already been made, then
    # proceed if not.
    with open(zsh, "r") as f1, open(support, "r") as f2:
        rc_str = f1.read()
        sup_str = lean_text(f2.read())
    if sup_str not in rc_str:
        with open(support, "r") as f1, open(bash, "a") as f2, open(zsh, "a") as f3:
            f2.write(f1.read())
            f1.seek(0)
            f3.write(f1.read())
    print(PASS)

    # ------------------------------------------

    # Done

    msg = """
    Setup script is complete. If all steps above are marked with green
    checkmarks, pyenv is ready to go. You must reboot your VM now for
    the changes to take effect. If any steps above show a red \"X\",
    there was an error during installation.
    """
    print(f"\n{textwrap.fill(text=" ".join(msg.split()))}\n")

    return


def main():
    if result := min_python_version():
        raise RuntimeError(result)

    msg = """
    This script will setup and install the dependencies to use pyenv.
    Pyenv is a powerfull tool that allows you to cleanly run multiple,
    independent python versions without interference or breaking the
    system default python installation. You will be prompted for your
    password during the setup.
    """

    epi = "Latest update: 11/27/24"

    parser = argparse.ArgumentParser(description=msg, epilog=epi)
    parser.parse_args()
    task_runner()

    return


if __name__ == "__main__":
    main()
