#!/usr/bin/env python3
"""Install Python development tools."""

import argparse

from library import Environment
from library import Labels
from library import clear
from library import minPythonVersion
from library import runOneCommand
from library import wrapTight


def runScript(e: Environment) -> None:
    """Install Python development tools.

    Parameters
    ----------
    e : Environment
        All the environment variables saved as attributes in an
        Environment object.
    """
    clear()

    labels = Labels("""
        System initialization
        Installing jupyter
        Installing jupyter lab
        Installing pytest""")

    # Step 1. System initialization. Right now it's just a placeholder for
    # future capability.

    labels.next()
    print(e.PASS)

    # Step 2, 3, 4 Install jupyter, jupyterlab & pytest

    base = 'pip3 install --upgrade TARGET'
    commands = []
    commands.append(base.replace('TARGET', 'jupyter'))
    commands.append(base.replace('TARGET', 'jupyterlab'))
    commands.append(base.replace('TARGET', 'pytest'))

    for cmd in commands:
        labels.next()
        print(runOneCommand(e, cmd.split()))

    # Done

    msg = """Python tools installation complete. Install additional
    tools if desired. No reboot is necessary."""
    print(f'\n{wrapTight(msg)}\n')

    return


def main():  # noqa

    # Get a new Environment variable with all the necessary properties
    # initialized.
    e = Environment()
    if (result := minPythonVersion(e)) is not None:
        raise RuntimeError(result)

    msg = """This script will install several Python tools.
    Specifically: jupyter, jupyterlab, and pytest. It\'s recommend that
    you create and activate a Python virtual environment before running
    this script, or skip this script and install the tools in a Python
    virtual environment manually."""

    epi = "Latest update: 08/09/22"

    parser = argparse.ArgumentParser(description=msg, epilog=epi)
    parser.parse_args()
    runScript(e)

    return


if __name__ == '__main__':
    main()
