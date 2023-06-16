#!/usr/bin/env python3
"""Installs docker.

Raises
------
RuntimeError
    If Python is not at the minimum required version.
"""

import argparse
import getpass
import tempfile as tf

from library.classes import Environment
from library.classes import Labels
from library.utilities import clean_str
from library.utilities import clear
from library.utilities import min_python_version
from library.utilities import run_many_arguments
from library.utilities import run_one_command
from library.utilities import wrap_tight


def run_script(e: Environment) -> None:
    """Install docker engine.

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
        Installing Docker Engine
        Installing Docker Compose
        Adding user to Docker group""")

    # ------------------------------------------

    # Step 0: Capture sudo permissions

    print("\nPlease enter your password if prompted.\n")
    # Push a dummy sudo command just to force password entry before first
    # command. This will avoid having the password prompt come in the middle of
    # a label when providing status

    run_one_command(e, 'sudo ls')

    # ------------------------------------------

    # Step 1: System initialization.

    labels.next()
    targets: list[str] = []
    print(e.PASS)

    # ------------------------------------------

    # Step 2: Update package index

    labels.next()
    commands: list[str] = []
    commands.append('sudo apt update')
    commands.append('sudo apt upgrade -y')
    for command in commands:
        run_one_command(e, command)
    print(e.PASS)

    # ------------------------------------------

    # Step 3: Install dependencies

    labels.next()
    cmd = 'sudo apt install TARGET -y'
    targets.append('apt-transport-https')
    targets.append('ca-certificates')
    targets.append('curl')
    targets.append('gnupg-agent')
    targets.append('make')
    targets.append('software-properties-common')
    print(run_many_arguments(e, cmd, targets))

    # Step 4: Install Docker public key.

    labels.next()
    keyloc = 'https://download.docker.com/linux/ubuntu/gpg'
    dest = '/etc/apt/keyrings/docker.gpg'
    cmd = 'sudo install -m 0755 -d /etc/apt/keyrings'
    run_one_command(e, cmd)

    with tf.NamedTemporaryFile(mode='w', delete=False) as f1:
        with tf.NamedTemporaryFile(delete=False) as f2:
            f1_name = f1.name
            f2_name = f2.name
            cmd = f'curl -fsSL {keyloc}'
            result = run_one_command(e, cmd, capture=False, std_out=f1)
            if result == e.PASS:
                f1.seek(0)
                cmd = 'gpg -o - --dearmor'
                result = run_one_command(e,
                                         cmd,
                                         capture=False,
                                         std_in=f1,
                                         std_out=f2)

    if result == e.PASS:
        cmd = f'sudo mv -f {f2_name} {dest}'
        result = run_one_command(e, cmd)
        cmd = f'rm -f {f1_name}'
        run_one_command(e, cmd)

    print(result)

    # ------------------------------------------

    # Step 5: Map to the Docker repository.

    labels.next()
    run_one_command(e, 'dpkg --print-architecture')
    deb = f'deb [arch={clean_str(e.RESULT.stdout)} '
    deb += 'signed-by=/etc/apt/keyrings/docker.gpg] '
    deb += 'https://download.docker.com/linux/ubuntu '
    run_one_command(e, 'lsb_release -cs')
    deb += f'{clean_str(e.RESULT.stdout)} stable'
    with tf.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(f'{deb}\n')
        f_name = f.name
    dest = '/etc/apt/sources.list.d/docker.list'
    cmd = f'sudo mv {f_name} {dest} -f'
    print(run_one_command(e, cmd))

    # ------------------------------------------

    # Step 6: Install Docker Engine

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

    # Step 7: Install Docker Compose

    labels.next()
    cmd = 'sudo apt install docker-compose-plugin -y'
    print(run_one_command(e, cmd))

    # Step 8: Add user to docker group.

    labels.next()
    cmd = f'sudo usermod -aG docker {getpass.getuser()}'
    print(run_one_command(e, cmd))

    msg = """Setup script is complete. If all steps above are marked
    with green checkmarks, Docker Engine is ready to go. You must reboot
    your VM now for the changes to take effect. If any steps above show
    a red \"X\", there was an error during installation."""
    print(f'\n{wrap_tight(msg)}\n')

    return


def main():  # noqa

    # Get a new Environment variable with all the necessary properties
    # initialized.
    e = Environment()
    if (result := min_python_version(e)):
        raise RuntimeError(result)

    msg = """This script will install Docker Engine, which is the
    underlying client-server technology that builds and runs containers
    using Docker\'s components and services. It will also install Docker
    Compose which is a tool to help define and share multi-container
    applications. With Compose, you can create a YAML file to define the
    services and with a single command, can spin everything up or tear
    it all down."""

    epi = "Latest update: 06/15/23"

    parser = argparse.ArgumentParser(description=msg, epilog=epi)
    parser.parse_args()
    run_script(e)

    return


if __name__ == '__main__':
    main()
