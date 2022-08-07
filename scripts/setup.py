#!/usr/bin/env python3
"""Install Ubuntu tools, programs, and settings.

Raises
------
RuntimeError
    If Python is not at the minimum required version.
"""

import argparse
import textwrap

from library import Environment
from library import clear
from library import copyFiles
from library import minPythonVersion
from library import printlabel
from library import runManyArguments
from library import runOneCommand


def runScript(e: Environment) -> None:
    """Perform tool installation and setup.

    Parameters
    ----------
    e : Environment
        All the environment variables saved as attributes in an
        Environment object.
    """
    clear()

    # ------------------------------------------

    # Setup status labels

    labels = []
    labels.append('System initialization')
    labels.append('Creating new directories')
    labels.append('Copying files')
    labels.append('Adjusting file permissions')
    labels.append('Setting terminal profile')
    labels.append('Setting gedit profile')
    labels.append('Installing developer tools')
    labels.append('Installing seahorse nautilus')
    labels.append('Installing gedit support')
    labels.append('Installing zsh')
    labels.append('Installing python pip3')
    labels.append('Installing python venv')
    labels.append('Creating virtual environment (env)')
    labels.append('Installing Google Chrome')
    labels.append('Setting up jupyter notebooks')
    labels.append('Refreshing snaps (please be patient)')
    labels.append('Installing atom')
    labels.append('Configuring favorites')
    labels.append('Disabling auto screen lock')
    labels.append('Setting idle timeout to \'never\'')
    labels.append('Disabling auto updates')
    labels.append('Patching fuse.conf')
    labels.append('Arranging icons')
    labels.append('Cleaning up')
    pad = len(max(labels, key=len)) + 3

    # ------------------------------------------

    # Step 1: System initialization. Right now it's just a placeholder for
    # future capability.

    printlabel(labels.pop(0), pad)
    print(e.PASS)

    # ------------------------------------------

    # Step 2: Create new directories

    printlabel(labels.pop(0), pad)

    targets = []
    targets.append(e.HOME/'.config/gedit/tools')
    targets.append(e.HOME/'.config/gedit/snippets')
    targets.append(e.HOME/'.vim/colors')
    targets.append(e.HOME/'shares')
    targets.append(e.HOME/'notebooks')
    targets.append(e.HOME/'.notebooksrepo')
    targets.append(e.HOME/'.atom')
    targets.append(e.HOME/'.venv')

    for target in targets:
        if e.DEBUG:
            print(f'\nMaking: {str(target)}')
        else:
            target.mkdir(parents=True, exist_ok=True)

    print(e.PASS)

    # ------------------------------------------

    # Step 3: Copy files

    printlabel(labels.pop(0), pad)

    targets = []
    targets.append((e.ATOM/'*', e.HOME/'.atom'))
    targets.append((e.GEDIT/'flexiwrap', e.HOME/'.config/gedit/tools'))
    targets.append((e.GEDIT/'*.xml', e.HOME/'.config/gedit/snippets'))
    targets.append((e.SHELL/'bashrc.txt', e.HOME/'.bashrc'))
    targets.append((e.SHELL/'zshrc.txt', e.HOME/'.zshrc'))
    targets.append((e.SHELL/'profile.txt', e.HOME/'.profile'))
    targets.append((e.SHELL/'profile.txt', e.HOME/'.zprofile'))
    targets.append((e.SHELL/'dircolors.txt', e.HOME/'.dircolors'))
    targets.append((e.VIM/'vimrc.txt', e.HOME/'.vimrc'))
    targets.append((e.VIM/'vimcolors/*', e.HOME/'.vim/colors'))

    copyFiles(e, targets)

    print(e.PASS)

    # ------------------------------------------

    # Step 4: Adjust these file permissions, just to make sure they're correct.
    # It may not be absolutely necessary, but it won't hurt.

    printlabel(labels.pop(0), pad)

    targets = []
    targets.append(str(e.SCRIPTS/'tuneup.py'))
    targets.append(str(e.SCRIPTS/'cacheburn.py'))
    targets.append(str(e.SCRIPTS/'usnapatch.py'))
    targets.append(str(e.HOME/'.config/gedit/tools/flexiwrap'))

    cmd = 'chmod 754 TARGET'

    print(runManyArguments(e, cmd, targets))

    # ------------------------------------------

    # Step 5: Setting terminal profile. Need a little special handling here,
    # because we're redirecting stdin.

    printlabel(labels.pop(0), pad)

    cmd = 'dconf reset -f /org/gnome/terminal/'
    result = runOneCommand(e, cmd.split())
    if result == e.PASS:
        cmd = 'dconf load /org/gnome/terminal/'
        path = e.SYSTEM/'terminalSettings.txt'
        if e.DEBUG:
            print(f'Opening: {path}')
        with open(path, 'r') as f:
            result = runOneCommand(e, cmd.split(), std_in=f)

    print(result)

    # ------------------------------------------

    # Step 6: Setting gedit profile. Again, need special handling here, because
    # we're redirecting stdin.

    printlabel(labels.pop(0), pad)

    cmd = 'dconf reset -f /org/gnome/gedit/'
    result = runOneCommand(e, cmd.split())
    if result == e.PASS:
        cmd = 'dconf load /org/gnome/gedit/'
        path = e.GEDIT/'geditSettings.txt'
        if e.DEBUG:
            print(f'Opening: {path}')
        with open(path, 'r') as f:
            result = runOneCommand(e, cmd.split(), std_in=f)

    print(result)

    # ------------------------------------------

    msg = "Installing additional software. Please enter your password if "
    msg += "prompted."
    print(f'\n{textwrap.fill(msg)}\n')

    # Push a dummy sudo command just to force password entry before first ppa
    # pull. This will avoid having the password prompt come in the middle of a
    # label when providing status

    runOneCommand(e, 'sudo ls'.split())

    # ------------------------------------------

    # Step 7: Packages from the ppa.

    # NOTE: libnss3-tools, libpcsclite1, pcscd, and pcsc-tools are needed for
    # certificate fixes at USNA. These can be deleted for future non-USNA
    # installations.

    # Build tools

    printlabel(labels.pop(0), pad)

    cmd = 'sudo apt -y install TARGET'

    targets = []
    targets.append('build-essential')
    targets.append('libnss3-tools')
    targets.append('pcscd')
    targets.append('pcsc-tools')
    targets.append('ccache')
    targets.append('vim')
    targets.append('tree')

    print(runManyArguments(e, cmd, targets))

    # ------------------------------------------

    # Step-8: seahorse nautilus

    printlabel(labels.pop(0), pad)
    doThis = cmd.replace('TARGET', 'seahorse-nautilus')
    print(runOneCommand(e, doThis.split()))

    # ------------------------------------------

    # Step-9: Gedit support

    printlabel(labels.pop(0), pad)
    doThis = cmd.replace('TARGET', 'gedit-plugins')
    print(runOneCommand(e, doThis.split()))

    # ------------------------------------------

    # Step-10: zsh. Also copy over the peter zsh theme.

    printlabel(labels.pop(0), pad)

    targets = []
    targets.append('zsh')
    targets.append('powerline')

    result = runManyArguments(e, cmd, targets)

    if result == e.PASS:
        src = 'https://github.com/robbyrussell/oh-my-zsh.git'
        dest = e.HOME/'.oh-my-zsh'
        cmd = f'git clone {src} {dest} --depth 1'
        result = runOneCommand(e, cmd.split())

    if result == e.PASS:
        src = e.SHELL/'peter.zsh-theme'
        dest = e.HOME/'.oh-my-zsh/custom/themes'
        targets = [(src, dest)]
        copyFiles(e, targets)

    print(result)

    # ------------------------------------------

    # Step-11: pip3

    printlabel(labels.pop(0), pad)
    cmd = 'sudo apt install -y python3-pip'
    print(runOneCommand(e, cmd.split()))

    # ------------------------------------------

    # Step-12: python3 venv

    printlabel(labels.pop(0), pad)
    cmd = 'sudo apt install -y python3-venv'
    print(runOneCommand(e, cmd.split()))

    # ------------------------------------------

    # Step-13: Create Python virtual environment

    printlabel(labels.pop(0), pad)
    cmd = f'python3 -m venv {e.HOME}/.venv/env'
    print(runOneCommand(e, cmd.split()))

    # ------------------------------------------

    # Step-14: Google Chrome

    printlabel(labels.pop(0), pad)

    googledeb = 'google-chrome-stable_current_amd64.deb'
    src = f'https://dl.google.com/linux/direct/{googledeb}'
    cmd = f'wget -O /tmp/{googledeb} {src}'
    result = runOneCommand(e, cmd.split())

    if result == e.PASS:
        cmd = f'sudo dpkg -i /tmp/{googledeb}'
        result = runOneCommand(e, cmd.split())

    print(result)

    # ------------------------------------------

    # Step-15: Set up jupyter notebooks

    printlabel(labels.pop(0), pad)

    # Clone the notebook repo (single branch, depth 1)
    src = 'https://github.com/geozeke/notebooks.git'
    dest = e.HOME/'.notebooksrepo'
    cmd = f'git clone {src} {dest} --single-branch --depth 1'
    result = runOneCommand(e, cmd.split())

    # Sync repo with local notebooks. Use the --delete option so the
    # destination directory always exactly mirrors the source directory. Also
    # skip syncing any git-related files. Per the man page, leaving a trailing
    # slash ('/') on the source directory allows you to have a destination
    # directory with a different name.
    if result == e.PASS:
        cmd = 'rsync -rc '
        cmd += '--exclude .git* --exclude LICENSE* --exclude README* '
        cmd += f'{e.HOME}/.notebooksrepo/ {e.HOME}/notebooks --delete'
        result = runOneCommand(e, cmd.split())

    print(result)

    # ------------------------------------------

    # Step-16: Refresh snaps

    printlabel(labels.pop(0), pad)
    cmd = 'sudo snap refresh'
    print(runOneCommand(e, cmd.split()))

    # ------------------------------------------

    # Step-17: Install atom

    printlabel(labels.pop(0), pad)
    cmd = 'sudo snap install atom --classic'
    print(runOneCommand(e, cmd.split()))

    # ------------------------------------------

    # Step-18: Configure favorites. NOTE: To get the information needed for the
    # code below, setup desired favorites, then run this command: gsettings get
    # org.gnome.shell favorite-apps

    printlabel(labels.pop(0), pad)

    cmd = 'gsettings set org.gnome.shell favorite-apps [\''
    parts = []
    parts.append('google-chrome.desktop')
    parts.append('atom_atom.desktop')
    parts.append('org.gnome.gedit.desktop')
    parts.append('org.gnome.Terminal.desktop')
    parts.append('org.gnome.Nautilus.desktop')
    parts.append('org.gnome.Calculator.desktop')
    parts.append('gnome-control-center.desktop')
    parts.append('snap-store_ubuntu-software.desktop')
    parts.append('org.gnome.seahorse.Application.desktop')
    cmd += '\',\''.join(parts) + '\']'

    print(runOneCommand(e, cmd.split()))

    # ------------------------------------------

    # Step-19: Disable auto screen lock

    printlabel(labels.pop(0), pad)
    cmd = 'gsettings set org.gnome.desktop.screensaver lock-enabled false'
    print(runOneCommand(e, cmd.split()))

    # ------------------------------------------

    # Step-20: Set idle timeout to 'never'.

    printlabel(labels.pop(0), pad)
    cmd = 'gsettings set org.gnome.desktop.session idle-delay 0'
    print(runOneCommand(e, cmd.split()))

    # ------------------------------------------

    # Step-21: Disable auto updates.

    printlabel(labels.pop(0), pad)

    dest = '/etc/apt/apt.conf.d/20auto-upgrades'
    argument = 's+Update-Package-Lists "1"+Update-Package-Lists "0"+'
    cmd = f'sudo*sed*-i*{argument}*{dest}'
    result = runOneCommand(e, cmd.split('*'))

    if result == e.PASS:
        argument = 's+Unattended-Upgrade "1"+Unattended-Upgrade "0"+'
        cmd = f'sudo*sed*-i*{argument}*{dest}'
        result = runOneCommand(e, cmd.split('*'))

    print(result)

    # ------------------------------------------

    # Step-22: Patch /etc/fuse.conf to un-comment 'user_allow_other'. This
    # allows users to start programs from the command line when their current
    # working directory is inside the share.

    printlabel(labels.pop(0), pad)

    argument = r's+\#user_allow_other+user_allow_other+'
    dest = '/etc/fuse.conf'
    cmd = f'sudo*sed*-i*{argument}*{dest}'

    print(runOneCommand(e, cmd.split('*')))

    # ------------------------------------------

    # Step 23: Arrange icons.

    printlabel(labels.pop(0), pad)

    targets = []
    base = 'org.gnome.shell.extensions.'
    targets.append(f'{base}dash-to-dock show-trash false')
    targets.append(f'{base}dash-to-dock show-mounts false')
    targets.append(f'{base}ding start-corner bottom-left')
    targets.append(f'{base}ding show-trash true')
    cmd = 'gsettings set TARGET'
    print(runManyArguments(e, cmd, targets))

    # ------------------------------------------

    # Step 24: Silently delete unused files. This includes the Firefox browser.

    printlabel(labels.pop(0), pad)

    targets = []
    targets.append(f'/tmp/{googledeb}')
    cmd = 'rm -f TARGET'
    result = runManyArguments(e, cmd, targets)

    if result == e.PASS:
        result = runOneCommand(e, 'sudo snap remove firefox'.split())
    print(result)

    # ------------------------------------------

    # Done

    msg = 'Ubuntu setup complete. Install additional tools or reboot '
    msg += 'your VM now for the changes to take effect.'
    print(f'\n{textwrap.fill(msg)}\n')

    return


def main():  # noqa

    # Get a new Environment variable with all the necessary properties
    # initialized.
    e = Environment()
    if (result := minPythonVersion(e)) is not None:
        raise RuntimeError(result)

    msg = """This script will install the necessary programs and
    settings files on an Ubuntu 22.04.x Virtual Machine for USNA course
    work in Computing Sciences or Cyber Operations. This should only be
    used on a single user Virtual Machine installation for a user
    account with sudo privileges. Do not attempt to run this script on a
    standalone Linux machine or dual-boot machine (including lab
    machines). You will be prompted for your password during
    installation."""

    epi = "Latest update: 08/03/22"

    parser = argparse.ArgumentParser(description=msg, epilog=epi)
    parser.parse_args()
    runScript(e)

    return


if __name__ == '__main__':
    main()
