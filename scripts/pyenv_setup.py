#!/usr/bin/env python3
"""Install support for pyenv.

Raises
------
RuntimeError
    If Python is not at the minimum required version.
"""

import argparse

from library.classes import Environment
from library.classes import Labels
from library.utilities import clear
from library.utilities import lean_text
from library.utilities import min_python_version
from library.utilities import run_many_arguments
from library.utilities import run_one_command
from library.utilities import run_script
from library.utilities import wrap_tight


def task_runner(e: Environment) -> None:
    """Perform pyenv setup steps.

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
        Updating package index
        Checking python build dependencies
        Installing pyenv and tools
        Adjusting shell environments"""
    )

    # Step 0

    msg = """Please enter your password if prompted."""
    print(f"\n{wrap_tight(msg)}\n")

    # Push a dummy sudo command just to force password entry before first ppa
    # pull. This will avoid having the password prompt come in the middle of a
    # label when providing status

    run_one_command(e, "sudo ls")

    # ------------------------------------------

    # Step 1: System initialization.

    labels.next()
    print(e.PASS)

    # ------------------------------------------

    # Step 2: Update package index

    labels.next()
    cmd = "sudo apt update"
    print(run_one_command(e, cmd))

    # ------------------------------------------

    # Step 3: Check dependencies

    labels.next()
    cmd = "sudo apt install TARGET -y"
    targets: list[str] = []
    targets.append("make")
    targets.append("build-essential")
    targets.append("libssl-dev")
    targets.append("zlib1g-dev")
    targets.append("libbz2-dev")
    targets.append("libreadline-dev")
    targets.append("libsqlite3-dev")
    targets.append("wget")
    targets.append("curl")
    targets.append("libncursesw5-dev")
    targets.append("xz-utils")
    targets.append("tk-dev")
    targets.append("libxml2-dev")
    targets.append("libxmlsec1-dev")
    targets.append("libffi-dev")
    targets.append("liblzma-dev")
    print(run_many_arguments(e, cmd, targets))

    # ------------------------------------------

    # Step 4: Install pyenv

    labels.next()
    print(run_script(e, "https://pyenv.run"))

    # ------------------------------------------

    # Step 5: Adjust shell environments

    labels.next()

    # Setup variables with file locations
    support = f"{e.SHELL}/pyenvsupport.txt"
    bash = f"{e.HOME}/.bashrc"
    zsh = f"{e.HOME}/.zshrc"

    # Check to see if the adjustments have already been made, then proceed if
    # not.
    with open(zsh, "r") as f1, open(support, "r") as f2:
        rc_str = f1.read()
        sup_str = lean_text(f2.read())
    if sup_str not in rc_str:
        with open(support, "r") as f1, open(bash, "a") as f2, open(zsh, "a") as f3:
            f2.write(f1.read())
            f1.seek(0)
            f3.write(f1.read())
    print(e.PASS)

    # ------------------------------------------

    # Done

    msg = """Setup script is complete. If all steps above are marked
    with green checkmarks, pyenv is ready to go. You must reboot your
    VM now for the changes to take effect. If any steps above show a
    red \"X\", there was an error during installation."""
    print(f"\n{wrap_tight(msg)}\n")

    return


def main():  # noqa
    # Get a new Environment variable with all the necessary properties
    # initialized.
    e = Environment()
    if result := min_python_version(e):
        raise RuntimeError(result)

    msg = """This script will setup and install the dependencies to use
    pyenv. Pyenv is a powerfull tool that allows you to cleanly run
    multiple, independent python versions without interference or
    breaking the system default python installation. You will be
    prompted for your password during the setup."""

    epi = "Latest update: 06/16/23"

    parser = argparse.ArgumentParser(description=msg, epilog=epi)
    parser.parse_args()
    task_runner(e)

    return


if __name__ == "__main__":
    main()
