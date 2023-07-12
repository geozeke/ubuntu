#!/usr/bin/env python3
"""Install Python development tools."""

import argparse

from library.classes import Labels
from library.environment import PASS
from library.utilities import clear
from library.utilities import min_python_version
from library.utilities import run_one_command
from library.utilities import wrap_tight


def task_runner() -> None:
    """Install Python development tools."""
    clear()

    labels = Labels(
        """
        System initialization
        Installing jupyter
        Installing jupyter lab
        Installing pytest"""
    )

    # Step 1. System initialization. Right now it's just a placeholder for
    # future capability.

    labels.next()
    print(PASS)

    # Step 2, 3, 4 Install jupyter, jupyterlab & pytest

    base = "pip3 install --upgrade TARGET"
    commands: list[str] = []
    commands.append(base.replace("TARGET", "jupyter"))
    commands.append(base.replace("TARGET", "jupyterlab"))
    commands.append(base.replace("TARGET", "pytest"))
    for cmd in commands:
        labels.next()
        print(run_one_command(cmd))

    # Done

    msg = """Python tools installation complete. Install additional
    tools if desired. No reboot is necessary."""
    print(f"\n{wrap_tight(msg)}\n")

    return


def main():  # noqa
    if result := min_python_version():
        raise RuntimeError(result)

    msg = """This script will install several Python tools.
    Specifically: jupyter, jupyterlab, and pytest. It\'s recommend that
    you create and activate a Python virtual environment before running
    this script, or skip this script and install the tools in a Python
    virtual environment manually."""

    epi = "Latest update: 06/16/23"

    parser = argparse.ArgumentParser(description=msg, epilog=epi)
    parser.parse_args()
    task_runner()

    return


if __name__ == "__main__":
    main()
