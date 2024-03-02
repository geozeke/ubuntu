#!/usr/bin/env python3
"""Patch files and run scripts to support network connections at USNA.

Raises
------
RuntimeError
    If Python is not at the minimum required version.
"""

import argparse

from library.classes import Labels
from library.environment import SYSTEM
from library.utilities import clear
from library.utilities import min_python_version
from library.utilities import run_one_command
from library.utilities import run_shell_script
from library.utilities import wrap_tight

SYSTEM_SH = "http://apt.cs.usna.edu/ssl/install-ssl-system.sh"
BROWSER_SH = "http://apt.cs.usna.edu/ssl/install-ssl.sh"


def task_runner(args: argparse.Namespace) -> None:
    """Patch openssl configuration and run certificate scripts.

    Parameters
    ----------
    args : argparse.Namespace
        This will contain the argparse object, which allows us to
        extract the mode. The mode determines which operation to
        perform: system, browser.
    """
    clear()

    # ------------------------------------------

    # Setup status labels

    labels = Labels(
        """
        Patching openssl configuration
        Updating system certificates
        Updating browser certificates"""
    )

    # ------------------------------------------

    # Step 0: Capture sudo permissions

    print("\nPlease enter your password if prompted.\n")
    # Push a dummy sudo command just to force password entry before first
    # command. This will avoid having the password prompt come in the middle of
    # a label when providing status
    run_one_command("sudo ls")

    # ------------------------------------------

    # Step 2: Take action based on selected option.

    match args.mode:
        case "system":
            # Patch openssl
            labels.next()
            target = "/usr/lib/ssl/openssl.cnf"
            cmd = f"sudo cp -f {SYSTEM}/openssl.cnf {target}"
            print(run_one_command(cmd))

            # Run system script
            labels.next()
            print(run_shell_script(script=SYSTEM_SH))
            labels.dump(1)

        case "browser":
            # Run browser script.
            labels.dump(2)
            labels.next()
            print(run_shell_script(script=BROWSER_SH))

        case _:
            pass

    # ------------------------------------------

    msg = """Patch script is complete. If all steps above are marked
    with green checkmarks, the certificate patching was successful. If
    any steps above show a red \"X\", there was an error during
    certificate modification."""
    print(f"\n{wrap_tight(msg)}\n")

    return


def main():  # noqa
    if result := min_python_version():
        raise RuntimeError(result)

    msg = """This script installs a patched openssl configuration file
    and runs the necessary certificate patching utilities to support
    networking on the USNA mission network. You will be prompted for
    your password during installation."""

    epi = "Latest update: 07/12/23"

    parser = argparse.ArgumentParser(description=msg, epilog=epi)

    msg = """Include one of the following options indicating where
    to apply patches: system, browser"""
    parser.add_argument(
        "mode",
        choices=["system", "browser"],
        type=str,
        help=msg,
    )

    args = parser.parse_args()
    task_runner(args)

    return


if __name__ == "__main__":
    main()
