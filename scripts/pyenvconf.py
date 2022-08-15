#!/usr/bin/env python3
"""Install support for pyenv.

Raises
------
RuntimeError
    If Python is not at the minimum required version.
"""

import argparse

from library import Environment
from library import Labels
from library import clear
from library import min_python_version
from library import run_many_arguments
from library import run_one_command
from library import wrap_tight


def run_script(e: Environment) -> None:
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

    labels = Labels("""
        System initialization
        Updating package index
        Validating dependencies
        Cloning git repository
        Adjusting shell environments""")

    # Step 0

    msg = """Please enter your password if prompted."""
    print(f'\n{wrap_tight(msg)}\n')

    # Push a dummy sudo command just to force password entry before first ppa
    # pull. This will avoid having the password prompt come in the middle of a
    # label when providing status

    run_one_command(e, 'sudo ls'.split())

    # ------------------------------------------

    # Step 1: System initialization. Right now it's just a placeholder for
    # future capability.

    labels.next()
    print(e.PASS)

    # ------------------------------------------

    # Step 2: Updating package index

    labels.next()
    cmd = 'sudo apt update'
    print(run_one_command(e, 'sudo ls'.split()))

    # ------------------------------------------

    # Step 3: Validating dependencies

    labels.next()
    cmd = 'sudo apt install TARGET -y'
    targets = []
    targets.append('make')
    targets.append('build-essential')
    targets.append('libssl-dev zlib1g-dev')
    targets.append('libbz2-dev')
    targets.append('libreadline-dev')
    targets.append('libsqlite3-dev')
    targets.append('wget')
    targets.append('curl')
    targets.append('llvm')
    targets.append('libncurses5-dev')
    targets.append('libncursesw5-dev')
    targets.append('xz-utils')
    targets.append('tk-dev')
    targets.append('libffi-dev')
    targets.append('liblzma-dev')
    targets.append('python3-openssl')
    targets.append('git')
    print(run_many_arguments(e, cmd, targets))

    # ------------------------------------------

    # Step 4: Cloning git repository

    labels.next()
    cmd = "git clone https://github.com/pyenv/pyenv.git ~/.pyenv"
    print(run_one_command(e, cmd.split()))

    # ------------------------------------------

    # Step 5: Adjusting shell environments

    labels.next()
    cmd = f"cat {e.SHELL/'pyenvsupport.txt'} >> ~/.bashrc"
    result = run_one_command(e, cmd.split())
    if result == e.PASS:
        cmd = f"cat {e.SHELL/'pyenvsupport.txt'} >> ~/.zshrc"
        print(run_one_command(e, cmd.split()))

    # ------------------------------------------

    # Done

    msg = """pyenv setup complete. Reboot your VM now for the changes to
    take effect."""
    print(f'\n{wrap_tight(msg)}\n')

    return


def main():  # noqa

    # Get a new Environment variable with all the necessary properties
    # initialized.
    e = Environment()
    if (result := min_python_version(e)):
        raise RuntimeError(result)

    msg = """This script will setup and install the dependencies to use
    pyenv. Pyenv program is a powerfull tool that allows you to cleanly
    run multiple, independent python versions without interference or
    breaking the system default python installation. You will be
    prompted for your password during the setup."""

    epi = "Latest update: 08/10/22"

    parser = argparse.ArgumentParser(description=msg, epilog=epi)
    parser.parse_args()
    run_script(e)

    return


if __name__ == '__main__':
    main()
