#!/usr/bin/env python3
"""Configure vim settings in Ubuntu."""

import argparse
import textwrap

from library import Environment
from library import clear
from library import copyFiles
from library import minPythonVersion
from library import printlabel


def runScript(e: Environment) -> None:
    """Configure vim.

    Parameters
    ----------
    e : Environment
        All the environment variables saved as attributes in an
        Environment object.
    """
    clear()

    labels = []
    labels.append('System initialization')
    labels.append('Creating new directories')
    labels.append('Copying files')
    pad = len(max(labels, key=len)) + 3

    # Step 1. System initialization. Right now it's just a placeholder for
    # future capability.

    printlabel(labels.pop(0), pad)
    print(e.PASS)

    # Step 2. Creating new directory

    printlabel(labels.pop(0), pad)

    p = e.HOME/'.vim/colors'
    if e.DEBUG:
        print(p)
    else:
        p.mkdir(parents=True, exist_ok=True)

    print(e.PASS)

    # Step 3. Copying files

    printlabel(labels.pop(0), pad)

    targets = []
    targets.append((e.VIM/'vimrc.txt', e.HOME/'.vimrc'))
    targets.append((e.VIM/'vimcolors/*', e.HOME/'.vim/colors'))

    copyFiles(e, targets)

    print(e.PASS)

    # Done

    msg = 'vim setup complete. You are now ready to use vi or vim and '
    msg += 'enjoy a pleasing visual experience.'
    print(f'\n{textwrap.fill(msg)}\n')

    return


def main():  # noqa

    # Get a new Environment variable with all the necessary properties
    # initialized.
    e = Environment()
    if (result := minPythonVersion(e)) is not None:
        raise RuntimeError(result)

    msg = """This script installs the necessary settings files and
    color schemes for a pleasant visual experience in vi. NOTE: If
    you\'ve already run the ubuntu setup script there's no need to run
    this script."""

    epi = "Latest update: 08/03/22"

    parser = argparse.ArgumentParser(description=msg, epilog=epi)
    parser.parse_args()
    runScript(e)

    return


if __name__ == '__main__':
    main()
