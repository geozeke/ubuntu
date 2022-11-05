#!/usr/bin/env python3
"""Installs docker and docker compose.

Raises
------
RuntimeError
    If Python is not at the minimum required version.
"""

import argparse
import subprocess as sp
import getpass
import os

from library.classes import Environment
from library.classes import Labels
from library.utilities import clear, run_many_arguments, clean_str
from library.utilities import min_python_version
from library.utilities import run_one_command
from shlex import split


def run_script(e: Environment) -> None:
    """Patch openssl configuration and run certificate scripts.

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
        Adding user to Docker group
        Cloning compose repository
        Making docker compose binary
        Moving files into final position""")

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
    cmd = 'sudo apt update && sudo apt upgrade -y'
    print(run_one_command(e, cmd))

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
    dest = '/usr/share/keyrings/docker-archive-keyring.gpg'
    # dest = e.HOME/'Desktop/junk.gpg'
    with open(dest, 'wb') as f:
        cmd = 'sudo gpg --dearmor'
        sp.run(split(cmd), stdin=p1.stdout, stdout=f)
    print(e.PASS)

    # ------------------------------------------

    # Step 5: Map to the Docker repository. Again, special handling with
    # subprocess because we're using pipes.

    labels.next()
    run_one_command(e, 'dpkg --print-architecture')
    cmd = f'echo \"deb [arch={clean_str(e.RESULT.stdout)} '
    cmd += 'signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] '
    cmd += 'https://download.docker.com/linux/ubuntu '
    run_one_command(e, 'lsb_release -cs')
    cmd += f'{clean_str(e.RESULT.stdout)} stable\"'
    p1 = sp.Popen(split(cmd), stdout=sp.PIPE)
    # dest = e.HOME/'Desktop/junk.list'
    dest = '/etc/apt/sources.list.d/docker.list'
    with open(dest, 'wb') as f:
        cmd = 'sudo tee - > /dev/null'
        sp.run(split(cmd), stdin=p1.stdout, stdout=f)
    print(e.PASS)

    # ------------------------------------------

    # Step 6: Install Docker.

    labels.next()
    cmd = 'sudo apt update'
    result = run_one_command(e, cmd)
    if result == e.PASS:
        cmd = 'sudo apt install docker-ce docker-ce-cli containerd.io -y'
        result = run_one_command(e, cmd)
    print(result)

    # Step 7: Add user to docker group.

    labels.next()
    cmd = f'sudo usermod -aG docker {getpass.getuser()}'
    print(run_one_command(e, cmd))

    # Step 8: Cloning docker compose repo.

    labels.next()
    src = 'https://github.com/docker/compose.git'
    dest = e.HOME/'.compose'
    cmd = f'git clone {src} {dest} --depth 1'
    print(run_one_command(e, cmd))

    # Step 9: Make the compose binary.

    labels.next()
    os.chdir(e.HOME/'.compose')
    cmd = 'make binary'
    print(run_one_command(e, cmd))

    # Step 10: Move the binary into location and adjust permissions.

    labels.next()
    src = e.HOME/'.compose/bin/build/docker-compose'
    dest = '/usr/libexec/docker/cli-plugins/'
    cmd = f'sudo mv {src} {dest}'
    result = run_one_command(e, cmd)
    if result == e.PASS:
        dest = '/usr/libexec/docker/cli-plugins/docker-compose'
        cmd = f'sudo chmod 755 {dest}'
        result = run_one_command(e, cmd)
    print(result)

    return


def main():  # noqa

    # Get a new Environment variable with all the necessary properties
    # initialized.
    e = Environment()
    if (result := min_python_version(e)):
        raise RuntimeError(result)

    msg = """This script will install docker and docker compose."""

    epi = "Latest update: 08/16/22"

    parser = argparse.ArgumentParser(description=msg, epilog=epi)
    parser.parse_args()
    run_script(e)

    return


if __name__ == '__main__':
    main()
