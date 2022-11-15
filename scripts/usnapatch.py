#!/usr/bin/env python3
"""Patch files and run scripts to support network connections at USNA.

Raises
------
RuntimeError
    If Python is not at the minimum required version.
"""

import argparse
import tempfile

from library.classes import Environment
from library.classes import Labels
from library.utilities import clear
from library.utilities import min_python_version
from library.utilities import run_one_command


def run_script(args: argparse.Namespace, e: Environment) -> None:
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
        System initialization
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

    # Step 1: System initialization. Right now it's just a placeholder for
    # future capability.

    labels.next()
    print(e.PASS)

    # ------------------------------------------

    # Step 2: Patch openssl

    if args.mode == 'system':
        labels.next()
        target = '/usr/lib/ssl/openssl.cnf'
        cmd = f'sudo cp -f {e.SYSTEM}/openssl.cnf {target}'
        print(run_one_command(e, cmd))
    else:
        labels.pop_first()

    # ------------------------------------------

    # Step 3: Update certificates

    fname = f'{tempfile.NamedTemporaryFile().name}.sh'

    if args.mode == 'system':
        url = 'apt.cs.usna.edu/ssl/install-ssl-system.sh'
        labels.pop_last()  # Discard the trailing label
    else:
        url = 'apt.cs.usna.edu/ssl/install-ssl-browsers.sh'
        labels.pop_first()  # Discard the leading label

    commands = []
    commands.append(f'curl -o {fname} {url}')
    commands.append(f'chmod 754 {fname}')
    commands.append(f'{fname}')

    labels.next()
    success = True

    for command in commands:
        if run_one_command(e, command) != e.PASS:
            success = False
            break

    # Step 4: Cleanup tmp file and report status

    if success:
        command = f'rm -f {fname}'
        print(run_one_command(e, command))
    else:
        print(e.FAIL)

    print()

    # ------------------------------------------

    return


def main():  # noqa

    # Get a new Environment variable with all the necessary properties
    # initialized.
    e = Environment()
    if (result := min_python_version(e)):
        raise RuntimeError(result)

    msg = """This script installs a patched openssl configuration file
    and runs the necessary certificate scripts to support networking
    on the USNA mission network. You will be prompted for your password
    during installation."""

    epi = "Latest update: 11/06/22"

    parser = argparse.ArgumentParser(description=msg, epilog=epi)

    msg = """Include one of the following options indicating where
    to apply patches: system, browser"""
    parser.add_argument('mode',
                        choices=['system', 'browser'],
                        type=str,
                        help=msg)

    args = parser.parse_args()
    run_script(args, e)

    return


if __name__ == '__main__':
    main()


# """Find databases in path."""
# import subprocess as sp
# import tempfile
# from pathlib import Path
# from shlex import split


# CERTFILE = 'http://apt.cs.usna.edu/ssl/system-certs-5.6-pa.tgz'


# def find_db_files(starting: Path) -> list[Path]:
#     """Find certificate db files.

#     In this case, a certificate db file is any file that starts with
#     'cert*' and has a '.db' extension.

#     Parameters
#     ----------
#     starting : Path
#         The directory to start a recursive search for db files.

#     Returns
#     -------
#     list[Path]
#         A list of fully-expressed pathlib objects for all db instances
#         found.
#     """
#     L: list[Path] = []
#     for p in starting.rglob('*'):
#         if p.name.startswith('cert') and p.suffix == '.db':
#             L.append(p)
#     return L


# # This will be a list of pathlib objects pointing to certifcate database files.
# cert_databases: list[Path] = []

# # Load certificates from USNA server.
# certdir = Path(tempfile.NamedTemporaryFile().name)
# certdir.mkdir(parents=True)
# commands = []
# commands.append(f'curl -o {certdir}/certs.tgz {CERTFILE}')
# commands.append(f'tar -xpf {certdir}/certs.tgz -C {certdir}')
# for command in commands:
#     sp.run(split(command))


# # From the user's home directory, look for certificate database files inside
# # any hidden directory (starting with '.')
# for p in Path.home().iterdir():
#     if p.is_dir and p.name.startswith('.'):
#         cert_databases += find_db_files(p)

# # Once any / all certificate databases are found, update them with the certutil
# # utility using the certificates taken from the USNA server.
# for db in cert_databases:
#     cmd_root = f'certutil -d sql:{db.parent} -A -t \\"TC\\"'
#     for cert in certdir.iterdir():
#         if cert.suffix == '.crt':
#             cmd = f'{cmd_root} -n {cert.stem} -i {cert}'
#             print(split(cmd))

# # Cleanup downloaded certificates.
# cmd = f'rm -rf {certdir}'
# sp.run(split(cmd))
