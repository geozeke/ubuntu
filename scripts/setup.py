#!/usr/bin/env python3
"""Install Ubuntu tools, programs, and settings.

Raises
------
RuntimeError
    If Python is not at the minimum required version.
"""

import argparse
from pathlib import Path
from typing import Any

from library.classes import Labels
from library.environment import DEBUG
from library.environment import HOME
from library.environment import PASS
from library.environment import SCRIPTS
from library.environment import SHELL
from library.environment import SYSTEM
from library.environment import VIM
from library.utilities import clear
from library.utilities import copy_files
from library.utilities import min_python_version
from library.utilities import run_many_arguments
from library.utilities import run_one_command
from library.utilities import sync_notebooks
from library.utilities import wrap_tight


def task_runner() -> None:
    """Perform tool installation and setup."""
    clear()

    # ------------------------------------------

    # Setup status labels

    labels = Labels(
        """
        System initialization
        Creating new directories
        Copying files
        Adjusting file permissions
        Setting terminal profile
        Installing developer tools
        Installing seahorse nautilus
        Installing zsh
        Setting Text Editor profile
        Installing python pip3
        Installing python venv
        Creating virtual environment (env)
        Installing Google Chrome
        Setting up jupyter notebooks
        Refreshing snaps (please be patient)
        Configuring favorites
        Disabling auto screen lock
        Setting idle timeout to \"never\"
        Disabling auto updates
        Patching fuse.conf
        Tidying icons
        Cleaning up"""
    )

    # ------------------------------------------

    # Step 1: Initialize lists for running many arguments. When running
    # commands with generic string targets, the "targets" array will be used.
    # Commands with special target-types are shown below.

    labels.next()
    dir_targets: list[Path] = []
    file_targets: list[tuple[Any, Any]] = []
    targets: list[str] = []
    print(PASS)

    # ------------------------------------------

    # Step 2: Create new directories

    labels.next()
    dir_targets.append(HOME / ".vim/colors")
    dir_targets.append(HOME / "shares")
    dir_targets.append(HOME / "notebooks")
    dir_targets.append(HOME / ".notebooksrepo")
    for target in dir_targets:
        if DEBUG:
            print(f"\nMaking: {str(target)}")
        else:
            target.mkdir(parents=True, exist_ok=True)
    print(PASS)

    # ------------------------------------------

    # Step 3: Copy files

    labels.next()
    file_targets.append((SHELL / "bashrc.txt", HOME / ".bashrc"))
    file_targets.append((SHELL / "zshrc.txt", HOME / ".zshrc"))
    file_targets.append((SHELL / "profile.txt", HOME / ".profile"))
    file_targets.append((SHELL / "profile.txt", HOME / ".zprofile"))
    file_targets.append((SHELL / "dircolors.txt", HOME / ".dircolors"))
    file_targets.append((VIM / "vimrc.txt", HOME / ".vimrc"))
    file_targets.append((VIM / "vimcolors/*", HOME / ".vim/colors"))
    copy_files(file_targets)
    print(PASS)

    # ------------------------------------------

    # Step 4: Adjust file permissions on scripts just to make sure they're
    # correct. It may not be absolutely necessary, but it won't hurt.

    labels.next()
    cmd = f"find {SCRIPTS} -name *.py -exec chmod 754 {{}} ;"
    print(run_one_command(cmd))

    # ------------------------------------------

    # Step 5: Setting terminal profile. Need a little special handling here,
    # because we're redirecting stdin.

    labels.next()
    cmd = "dconf reset -f /org/gnome/terminal/"
    result = run_one_command(cmd)
    if result == PASS:
        cmd = "dconf load /org/gnome/terminal/"
        path = SYSTEM / "terminalSettings.txt"
        if DEBUG:
            print(f"Opening: {path}")
        with open(path, "r") as f:
            result = run_one_command(cmd, std_in=f)
    print(result)

    # ------------------------------------------

    msg = """Installing additional software. Please enter your password
    if prompted."""
    print(f"\n{wrap_tight(msg)}\n")

    # Push a dummy sudo command just to force password entry before first ppa
    # pull. This will avoid having the password prompt come in the middle of a
    # label when providing status

    run_one_command("sudo ls")

    # ------------------------------------------

    # Step 6: Packages from the ppa.

    # NOTE: libnss3-tools, libpcsclite1, pcscd, and pcsc-tools are needed for
    # certificate fixes at USNA. These can be deleted for future non-USNA
    # installations.

    # Build tools

    labels.next()
    cmd = "sudo apt -y install TARGET"
    targets = []
    targets.append("gnome-text-editor")
    targets.append("build-essential")
    targets.append("ccache")
    targets.append("vim")
    targets.append("tree")
    print(run_many_arguments(cmd, targets))

    # ------------------------------------------

    # Step-7: seahorse nautilus

    labels.next()
    seahorse = cmd.replace("TARGET", "seahorse-nautilus")
    print(run_one_command(seahorse))

    # ------------------------------------------

    # Step-8: zsh. Also copy over the peter zsh theme.

    labels.next()
    targets = []
    targets.append("zsh")
    targets.append("powerline")
    result = run_many_arguments(cmd, targets)
    if result == PASS:
        src: str | Path = "https://github.com/robbyrussell/oh-my-zsh.git"
        dest: str | Path = HOME / ".oh-my-zsh"
        cmd = f"git clone {src} {dest} --depth 1"
        result = run_one_command(cmd)
    if result == PASS:
        src = SHELL / "peter.zsh-theme"
        dest = HOME / ".oh-my-zsh/custom/themes"
        file_targets = [(src, dest)]
        copy_files(file_targets)
    print(result)

    # ------------------------------------------

    # Step 9: Setting Text Editor profile. Again, need special handling here,
    # because we're redirecting stdin.

    labels.next()
    cmd = "dconf reset -f /org/gnome/TextEditor/"
    result = run_one_command(cmd)
    if result == PASS:
        cmd = "dconf load /org/gnome/TextEditor/"
        path = SYSTEM / "text_editor_settings.txt"
        if DEBUG:
            print(f"Opening: {path}")
        with open(path, "r") as f:
            result = run_one_command(cmd, std_in=f)
    print(result)

    # ------------------------------------------

    # Step-10: pip3

    labels.next()
    cmd = "sudo apt install -y python3-pip"
    print(run_one_command(cmd))

    # ------------------------------------------

    # Step-11: python3 venv

    labels.next()
    cmd = "sudo apt install -y python3-venv"
    print(run_one_command(cmd))

    # ------------------------------------------

    # Step-12: Create Python virtual environment

    labels.next()
    cmd = f"python3 -m venv {HOME}/.venv"
    print(run_one_command(cmd))

    # ------------------------------------------

    # Step-13: Google Chrome

    labels.next()
    google_deb = "google-chrome-stable_current_amd64.deb"
    src = f"https://dl.google.com/linux/direct/{google_deb}"
    cmd = f"wget -O /tmp/{google_deb} {src}"
    result = run_one_command(cmd)
    if result == PASS:
        cmd = f"sudo dpkg -i /tmp/{google_deb}"
        result = run_one_command(cmd)
    print(result)

    # ------------------------------------------

    # Step-14: Set up jupyter notebooks

    labels.next()
    # Clone the notebook repo (single branch, depth 1)
    src = "https://github.com/geozeke/notebooks.git"
    dest = HOME / ".notebooksrepo"
    cmd = f"git clone {src} {dest} --single-branch --depth 1"
    result = run_one_command(cmd)
    if result == PASS:
        result = sync_notebooks()
    print(result)

    # ------------------------------------------

    # Step-15: Refresh snaps

    labels.next()
    cmd = "sudo snap refresh"
    print(run_one_command(cmd))

    # ------------------------------------------

    # Step-16: Configure favorites. NOTE: To get the information needed for the
    # code below, setup desired favorites, then run this command: gsettings get
    # org.gnome.shell favorite-apps

    labels.next()
    cmd = "gsettings set org.gnome.shell favorite-apps \"['"
    targets = []
    targets.append("google-chrome.desktop")
    targets.append("org.gnome.TextEditor.desktop")
    targets.append("org.gnome.Terminal.desktop")
    targets.append("org.gnome.Nautilus.desktop")
    targets.append("org.gnome.Calculator.desktop")
    targets.append("gnome-control-center.desktop")
    targets.append("snap-store_ubuntu-software.desktop")
    targets.append("org.gnome.seahorse.Application.desktop")
    cmd += "','".join(targets) + "']\""
    print(run_one_command(cmd))

    # ------------------------------------------

    # Step-17: Disable auto screen lock

    labels.next()
    cmd = "gsettings set org.gnome.desktop.screensaver lock-enabled false"
    print(run_one_command(cmd))

    # ------------------------------------------

    # Step-18: Set idle timeout to 'never'.

    labels.next()
    cmd = "gsettings set org.gnome.desktop.session idle-delay 0"
    print(run_one_command(cmd))

    # ------------------------------------------

    # Step-19: Disable auto updates.

    labels.next()
    dest = "/etc/apt/apt.conf.d/20auto-upgrades"
    argument = r"s+Update-Package-Lists\ \"1\"+Update-Package-Lists\ \"0\"+"
    cmd = f"sudo sed -i {argument} {dest}"
    result = run_one_command(cmd)
    if result == PASS:
        argument = r"s+Unattended-Upgrade\ \"1\"+Unattended-Upgrade\ \"0\"+"
        cmd = f"sudo sed -i {argument} {dest}"
        result = run_one_command(cmd)
    print(result)

    # ------------------------------------------

    # Step-20: Patch /etc/fuse.conf to un-comment 'user_allow_other'. This
    # allows users to start programs from the command line when their current
    # working directory is inside the share.

    labels.next()
    argument = r"s+\#user_allow_other+user_allow_other+"
    dest = "/etc/fuse.conf"
    cmd = f"sudo sed -i {argument} {dest}"
    print(run_one_command(cmd))

    # ------------------------------------------

    # Step 21: Arrange icons.

    labels.next()
    base = "org.gnome.shell.extensions."
    targets = []
    targets.append(f"{base}dash-to-dock show-trash false")
    targets.append(f"{base}dash-to-dock show-mounts false")
    targets.append(f"{base}ding start-corner bottom-left")
    targets.append(f"{base}ding show-trash true")
    cmd = "gsettings set TARGET"
    print(run_many_arguments(cmd, targets))

    # ------------------------------------------

    # Step 22: Silently delete unused files. This includes the Firefox browser.

    labels.next()
    targets = []
    targets.append(f"/tmp/{google_deb}")
    cmd = "rm -f TARGET"
    result = run_many_arguments(cmd, targets)
    if result == PASS:
        result = run_one_command("sudo snap remove firefox")
    print(result)

    # ------------------------------------------

    # Done

    msg = """Setup script is complete. If all steps above are marked
    with green checkmarks, Ubuntu is ready to go. You must reboot your
    VM now for the changes to take effect. If any steps above show a red
    \"X\", there was an error during installation."""
    print(f"\n{wrap_tight(msg)}\n")

    return


def main():  # noqa
    if result := min_python_version():
        raise RuntimeError(result)

    msg = """This script will install the necessary programs and
    settings files on an Ubuntu 22.04.x Virtual Machine for USNA course
    work in Computing Sciences or Cyber Operations. This should only be
    used on a single user Virtual Machine installation for a user
    account with sudo privileges. Do not attempt to run this script on a
    standalone Linux machine or dual-boot machine (including lab
    machines). You will be prompted for your password during
    installation."""

    epi = "Latest update: 06/16/23"

    parser = argparse.ArgumentParser(description=msg, epilog=epi)
    parser.parse_args()
    task_runner()

    return


if __name__ == "__main__":
    main()
