#!/usr/bin/env python3
"""Installs docker.

Raises
------
RuntimeError
    If Python is not at the minimum required version.
"""

import argparse
import subprocess as sp
import getpass
import tempfile

from library.classes import Environment
from library.classes import Labels
from library.utilities import clear, run_many_arguments, clean_str, wrap_tight
from library.utilities import min_python_version
from library.utilities import run_one_command
from shlex import split


def run_script(e: Environment) -> None:
    """Install docker.

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
        Installing dependencies
        Installing Docker public key
        Mapping the Docker repository
        Installing Docker
        Adding user to Docker group""")

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

    # Step 2: Update package index

    labels.next()
    commands = []
    commands.append('sudo apt update')
    commands.append('sudo apt upgrade -y')
    for command in commands:
        run_one_command(e, command)
    print(e.PASS)

    # ------------------------------------------

    # Step 3: Install dependencies

    labels.next()
    cmd = 'sudo apt install TARGET -y'
    targets = []
    targets.append('apt-transport-https')
    targets.append('ca-certificates')
    targets.append('curl')
    targets.append('gnupg-agent')
    targets.append('make')
    targets.append('software-properties-common')
    print(run_many_arguments(e, cmd, targets))

    # Step 4: Install Docker public key. Requires custom handling with the
    # subprocess module since we're using pipes.

    labels.next()
    cmd = 'curl -fsSL https://download.docker.com/linux/ubuntu/gpg'
    p1 = sp.Popen(split(cmd), stdout=sp.PIPE)
    tempdest = f'{tempfile.NamedTemporaryFile().name}.gpg'
    dest = '/usr/share/keyrings/docker-archive-keyring.gpg'
    # dest = e.HOME/'Desktop/junk.gpg'
    with open(tempdest, 'wb') as f:
        cmd = 'gpg --dearmor'
        sp.run(split(cmd), stdin=p1.stdout, stdout=f)
    cmd = f'sudo mv {tempdest} {dest} -f'
    run_one_command(e, cmd)
    cmd = f'rm {tempdest} -f'
    run_one_command(e, cmd)
    print(e.PASS)

    # ------------------------------------------

    # Step 5: Map to the Docker repository. Again, special handling with
    # subprocess because we're using pipes.

    labels.next()
    run_one_command(e, 'dpkg --print-architecture')
    deb = f'deb [arch={clean_str(e.RESULT.stdout)} '
    deb += 'signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] '
    deb += 'https://download.docker.com/linux/ubuntu '
    run_one_command(e, 'lsb_release -cs')
    deb += f'{clean_str(e.RESULT.stdout)} stable\"'
    tempdest = f'{tempfile.NamedTemporaryFile().name}.list'
    with open(tempdest, 'w') as f:
        f.write(deb)
    # dest = e.HOME/'Desktop/junk.list'
    dest = '/etc/apt/sources.list.d/docker.list'
    cmd = f'sudo mv {tempdest} {dest} -f'
    run_one_command(e, cmd)
    cmd = f'rm {tempdest} -f'
    run_one_command(e, cmd)
    print(e.PASS)

    # labels.next()
    # run_one_command(e, 'dpkg --print-architecture')
    # cmd = f'echo \"deb [arch={clean_str(e.RESULT.stdout)} '
    # cmd += 'signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] '
    # cmd += 'https://download.docker.com/linux/ubuntu '
    # run_one_command(e, 'lsb_release -cs')
    # cmd += f'{clean_str(e.RESULT.stdout)} stable\"'
    # p1 = sp.Popen(split(cmd), stdout=sp.PIPE)
    # tempdest = f'{tempfile.NamedTemporaryFile().name}.list'
    # # dest = e.HOME/'Desktop/junk.list'
    # dest = '/etc/apt/sources.list.d/docker.list'
    # with open(tempdest, 'wb') as f:
    #     cmd = 'sudo tee - > /dev/null'
    #     sp.run(split(cmd), stdin=p1.stdout, stdout=f)
    # cmd = f'sudo mv {tempdest} {dest} -f'
    # run_one_command(e, cmd)
    # cmd = f'rm {tempdest} -f'
    # run_one_command(e, cmd)
    # print(e.PASS)

    # ------------------------------------------

    # Step 6: Install Docker.

    labels.next()
    cmd = 'sudo apt update'
    result = run_one_command(e, cmd)
    if result == e.PASS:
        cmd = 'sudo apt install TARGET -y'
        targets = []
        targets.append('docker-ce')
        targets.append('docker-ce-cli')
        targets.append('containerd.io')
        result = run_many_arguments(e, cmd, targets)
    print(result)

    # Step 7: Add user to docker group.

    labels.next()
    cmd = f'sudo usermod -aG docker {getpass.getuser()}'
    print(run_one_command(e, cmd))

    msg = """docker installation and setup is complete. You must reboot
    your VM now for the changes to take effect."""
    print(f'\n{wrap_tight(msg)}\n')

    return


def main():  # noqa

    # Get a new Environment variable with all the necessary properties
    # initialized.
    e = Environment()
    if (result := min_python_version(e)):
        raise RuntimeError(result)

    msg = """This script will install docker."""

    epi = "Latest update: 08/16/22"

    parser = argparse.ArgumentParser(description=msg, epilog=epi)
    parser.parse_args()
    run_script(e)

    return


if __name__ == '__main__':
    main()
