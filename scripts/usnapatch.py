#!/usr/bin/env python3
"""Patch files and run scripts to support network connections at USNA.

Raises
------
RuntimeError
    If Python is not at the minimum required version.
"""

import argparse
import tempfile as tf
from typing import Text

from library.classes import Environment
from library.classes import Labels
from library.utilities import clear
from library.utilities import min_python_version
from library.utilities import run_one_command
from library.utilities import wrap_tight

SYSTEM = 'http://apt.cs.usna.edu/ssl/install-ssl-system.sh'
BROWSER = 'http://apt.cs.usna.edu/ssl/install-ssl.sh'


def run_script(e: Environment, script: str) -> Text:
    """Run a remote shell script.

    Parameters
    ----------
    e : Environment
        All the environment variables saved as attributes in an
        Environment object.
    script : str
        URL of the remote script to run.

    Returns
    -------
    Text
        A green check red X indicating success or failure.
    """
    with tf.TemporaryFile(mode='w') as f:
        cmd = f'curl -sL {script}'
        result = run_one_command(e, cmd, capture=False, std_out=f)
        if result == e.PASS:
            f.seek(0)
            result = run_one_command(e, 'bash', std_in=f)
    return result


def run_patches(args: argparse.Namespace, e: Environment) -> None:
    """Patch openssl configuration and run certificate scripts.

    Parameters
    ----------
    args : argparse.Namespace
        This will contain the argparse object, which allows us to
        extract the mode. The mode determines which operation to
        perform: system, browser.
    e : Environment
        All the environment variables saved as attributes in an
        Environment object.
    """
    clear()

    # ------------------------------------------

    # Setup status labels

    labels = Labels("""
        Patching openssl configuration
        Updating system certificates
        Updating browser certificates""")

    # ------------------------------------------

    # Step 0: Capture sudo permissions

    print("\nPlease enter your password if prompted.\n")
    # Push a dummy sudo command just to force password entry before first
    # command. This will avoid having the password prompt come in the middle of
    # a label when providing status
    run_one_command(e, 'sudo ls')

    # ------------------------------------------

    # Step 2: Take action based on selected option.

    match args.mode:

        case 'system':
            # Patch openssl
            labels.next()
            target = '/usr/lib/ssl/openssl.cnf'
            cmd = f'sudo cp -f {e.SYSTEM}/openssl.cnf {target}'
            print(run_one_command(e, cmd))

            # Run certificate script
            labels.next()
            print(run_script(e, SYSTEM))
            labels.dump(1)

        case 'browser':
            # Run browser script.
            labels.dump(2)
            labels.next()
            print(run_script(e, BROWSER))

        case _:
            pass

    # ------------------------------------------

    msg = """Patch script is complete. If all steps above are marked
    with green checkmarks, the certificate patching was successful. If
    any steps above show a red \"X\", there was an error during
    certificate modification."""
    print(f'\n{wrap_tight(msg)}\n')

    return


def main():  # noqa

    # Get a new Environment variable with all the necessary properties
    # initialized.
    e = Environment()
    if (result := min_python_version(e)):
        raise RuntimeError(result)

    msg = """This script installs a patched openssl configuration file
    and runs the necessary certificate patching utilities to support
    networking on the USNA mission network. You will be prompted for
    your password during installation."""

    epi = "Latest update: 06/15/23"

    parser = argparse.ArgumentParser(description=msg, epilog=epi)

    msg = """Include one of the following options indicating where
    to apply patches: system, browser"""
    parser.add_argument('mode',
                        choices=['system', 'browser'],
                        type=str,
                        help=msg)

    args = parser.parse_args()
    run_patches(args, e)

    return


if __name__ == '__main__':
    main()
