#!/usr/bin/env python3
"""Clean up cache files and directories."""

import argparse

from library import Environment
from library import minPythonVersion
from library import printlabel
from library import runOneCommand


def burnitup(e: Environment) -> None:
    """Perform cached file cleaning operation.

    Parameters
    ----------
    e : Environment
        All the environment variables saved as attributes in an
        Environment object.
    """
    labels = []
    labels.append('Deleting __pycache__ directories')
    labels.append('Deleting .pytest_cache directories')
    labels.append('Deleting .ipynb_checkpoints directories')
    labels.append('Zapping pesky Icon files')
    labels.append('Crunching annoying desktop.ini files')
    pad = len(max(labels, key=len)) + 3

    # Start with cache directories:

    # NOTE: If this command were being run on the command line, you'd need to
    # escape the semicolon (\;)
    home = e.HOME/'shares'
    base = f'find {home} -name DIR -type d -exec rm -rvf {{}} ; -prune'

    commands = []
    commands.append(base.replace('DIR', '__pycache__'))
    commands.append(base.replace('DIR', '.pytest_cache'))
    commands.append(base.replace('DIR', '.ipynb_checkpoints'))

    for cmd in commands:
        printlabel(labels.pop(0), pad)
        print(runOneCommand(e, cmd.split()))

    # Tee up files for deletion. You can sneak some other options in for the
    # find command if necessary.

    base = f'find {home} -name FILE -type f -delete'

    commands = []
    commands.append(base.replace('FILE', 'Icon? -size 0'))
    commands.append(base.replace('FILE', 'desktop.ini'))

    for cmd in commands:
        printlabel(labels.pop(0), pad)
        print(runOneCommand(e, cmd.split()))

    return


def main():  # noqa

    # Get a new Environment variable with all the necessary properties
    # initialized.
    e = Environment()
    if (result := minPythonVersion(e)) is not None:
        raise RuntimeError(result)

    msg = """This script will scan the ~/shares directory to wipe caches
    and delete other temporary files."""

    epi = "Latest update: 08/03/22"

    parser = argparse.ArgumentParser(description=msg,
                                     epilog=epi,
                                     prog='cacheburn')

    parser.parse_args()
    print()
    burnitup(e)
    print()

    return


if __name__ == '__main__':
    main()
