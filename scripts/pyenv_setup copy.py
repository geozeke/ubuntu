#!/usr/bin/env python3
"""Install support for pyenv.

Raises
------
RuntimeError
    If Python is not at the minimum required version.
"""

import argparse
import tempfile

from library.classes import Environment
from library.classes import Labels
from library.utilities import clean_str
from library.utilities import clear
from library.utilities import min_python_version
from library.utilities import run_many_arguments
from library.utilities import run_one_command
from library.utilities import wrap_tight


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
        Checking python build dependencies
        Installing pyenv and tools
        Adjusting shell environments
        Cleaning up""")

    # Step 0

    msg = """Please enter your password if prompted."""
    print(f'\n{wrap_tight(msg)}\n')

    # Push a dummy sudo command just to force password entry before first ppa
    # pull. This will avoid having the password prompt come in the middle of a
    # label when providing status

    run_one_command(e, 'sudo ls')

    # ------------------------------------------

    # Step 1: System initialization. Initialize a variable to keep track of
    # temp files.

    labels.next()
    temp_files: list[str] = []
    print(e.PASS)

    # ------------------------------------------

    # Step 2: Updating package index

    labels.next()
    cmd = 'sudo apt update'
    print(run_one_command(e, cmd))

    # ------------------------------------------

    # Step 3: Checking dependencies

    labels.next()
    cmd = 'sudo apt install TARGET -y'
    targets: list[str] = []
    targets.append('make')
    targets.append('build-essential')
    targets.append('libssl-dev')
    targets.append('zlib1g-dev')
    targets.append('libbz2-dev')
    targets.append('libreadline-dev')
    targets.append('libsqlite3-dev')
    targets.append('wget')
    targets.append('curl')
    targets.append('libncursesw5-dev')
    targets.append('xz-utils')
    targets.append('tk-dev')
    targets.append('libxml2-dev')
    targets.append('libxmlsec1-dev')
    targets.append('libffi-dev')
    targets.append('liblzma-dev')
    print(run_many_arguments(e, cmd, targets))

    # ------------------------------------------

    # Step 4: Install pyenv

    labels.next()
    remote_script = 'https://pyenv.run'
    local_script = f'{tempfile.NamedTemporaryFile().name}.sh'
    temp_files.append(local_script)
    cmd = f'curl -o {local_script} -L {remote_script}'
    result = run_one_command(e, cmd)
    if result == e.PASS:
        cmd = f'chmod 754 {local_script}'
        run_one_command(e, cmd)
        cmd = f'{local_script}'
        result = run_one_command(e, cmd)
    print(result)

    # ------------------------------------------

    # Step 5: Adjusting shell environments

    labels.next()

    # Setup variables with file locations
    support = f"{e.SHELL}/pyenvsupport.txt"
    bash = f"{e.HOME}/.bashrc"
    zsh = f"{e.HOME}/.zshrc"

    # Use the linux 'comm' command to check if the adjustments have already
    # been made, then proceed if not.
    rc_file = f'{tempfile.NamedTemporaryFile().name}'
    temp_files.append(rc_file)
    mods_file = f'{tempfile.NamedTemporaryFile().name}'
    temp_files.append(mods_file)
    with open(rc_file, 'w') as f:
        cmd = f'sort -u {zsh}'
        run_one_command(e, cmd, std_out=f, capture=False)
    with open(mods_file, 'w') as f:
        cmd = f'sort -u {support}'
        run_one_command(e, cmd, std_out=f, capture=False)
    cmd = f'comm -13 {rc_file} {mods_file}'
    run_one_command(e, cmd)
    if len(clean_str(e.RESULT.stdout).strip()) != 0:
        try:
            with open(support, 'r') as f1:
                with open(bash, 'a') as f2:
                    f2.write(f1.read())
                f1.seek(0)
                with open(zsh, 'a') as f2:
                    f2.write(f1.read())
            print(e.PASS)
        except Exception:
            print(e.FAIL)
    else:
        print(e.PASS)

    # Step 6. Cleanup temp files.
    labels.next()
    cmd = 'rm -f TARGET'
    print(run_many_arguments(e, cmd, temp_files))

    # ------------------------------------------

    # Done

    msg = """Setup script is complete. If all steps above are marked
    with green checkmarks, pyenv is ready to go. You must reboot your
    VM now for the changes to take effect. If any steps above show a
    red \"X\", there was an error during installation."""
    print(f'\n{wrap_tight(msg)}\n')

    return


def main():  # noqa

    # Get a new Environment variable with all the necessary properties
    # initialized.
    e = Environment()
    if (result := min_python_version(e)):
        raise RuntimeError(result)

    msg = """This script will setup and install the dependencies to use
    pyenv. Pyenv is a powerfull tool that allows you to cleanly run
    multiple, independent python versions without interference or
    breaking the system default python installation. You will be
    prompted for your password during the setup."""

    epi = "Latest update: 06/14/23"

    parser = argparse.ArgumentParser(description=msg, epilog=epi)
    parser.parse_args()
    run_script(e)

    return


if __name__ == '__main__':
    main()