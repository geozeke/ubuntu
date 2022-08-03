#!/usr/bin/env python3
"""Install Python development tools."""

import argparse
import textwrap

from library import Environment
from library import clear
from library import minPythonVersion
from library import runOneCommand


def runScript(e: Environment) -> None:
    """Install development tools.

    Parameters
    ----------
    e : Environment
        All the environment variables, saved as attributes in an
        Environment object.
    """
    clear()

    labels = []
    labels.append('System initialization')
    labels.append('Installing jupyter')
    labels.append('Installing jupyter lab')
    labels.append('Installing pytest')
    pad = len(max(labels, key=len)) + 3
    poplabel = (
        lambda x: print(f'{labels.pop(x):.<{pad}}', end='', flush=True))

    # Step 1. System initialization. Right now it's just a placeholder for
    # future capability.

    poplabel(0)
    print(e.PASS)

    # Step 2, 3, 4 Install jupyter, jupyterlab & pytest

    base = 'pip3 install --upgrade TARGET'

    commands = []
    commands.append(base.replace('TARGET', 'jupyter'))
    commands.append(base.replace('TARGET', 'jupyterlab'))
    commands.append(base.replace('TARGET', 'pytest'))

    for cmd in commands:
        poplabel(0)
        print(runOneCommand(e, cmd.split()))

    # Done

    msg = 'Python tools installation complete. Install additional '
    msg += 'tools or reboot your VM now for the changes to take effect.'
    print(f'\n{textwrap.fill(msg)}\n')

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

    epi = "Latest update: 08/03/22"

    parser = argparse.ArgumentParser(description=msg, epilog=epi)
    parser.parse_args()
    runScript(e)

    return


if __name__ == '__main__':
    main()
