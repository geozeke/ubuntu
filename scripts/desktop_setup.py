#!/usr/bin/env python3
"""Install Ubuntu tools, programs, and settings.

Raises
------
RuntimeError
    If Python is not at the minimum required version.
"""

import argparse
import textwrap
from pathlib import Path
from typing import Any

from library.classes import Labels
from library.environment import DEBUG
from library.environment import FAIL
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
from library.utilities import run_shell_script


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
        Installing zsh
        Installing OhMyZsh
        Installing OhMyZsh Full-autoupdate
        Installing powerlevel10k theme
        Installing Nerd Fonts
        Setting Text Editor profile
        Refreshing snaps (please be patient)
        Configuring favorites
        Disabling auto screen lock
        Setting idle timeout to \"never\"
        Disabling auto updates
        Patching fuse.conf
        Tidying icons
        Cleaning up
        """
    )

    # ------------------------------------------

    # Step 1: Initialize lists for running many arguments. When running
    # commands with generic string targets, the "targets" array will be
    # used. Commands with special target-types are shown below.

    labels.next()
    dir_targets: list[Path] = []
    file_targets: list[tuple[Any, Any]] = []
    targets: list[str] = []
    src: str | Path = ""
    dest: str | Path = ""
    print(PASS)

    # ------------------------------------------

    # Step 2: Create new directories

    labels.next()
    dir_targets = [
        HOME / ".fonts",
        HOME / ".vim/colors",
        HOME / "shares",
    ]
    for target in dir_targets:
        if DEBUG:
            print(f"\nMaking: {target}")
        else:
            target.mkdir(parents=True, exist_ok=True)
    print(PASS)

    # ------------------------------------------

    # Step 3: Copy files

    labels.next()
    file_targets = [
        (SHELL / "bashrc.conf", HOME / ".bashrc"),
        (SHELL / "dircolors.conf", HOME / ".dircolors"),
        (SHELL / "p10k.conf", HOME / ".p10k.zsh"),
        (SHELL / "profile.conf", HOME / ".profile"),
        (SHELL / "profile.conf", HOME / ".zprofile"),
        (VIM / "vimcolors/*", HOME / ".vim/colors"),
        (VIM / "vimrc.conf", HOME / ".vimrc"),
    ]
    copy_files(targets=file_targets)
    print(PASS)

    # ------------------------------------------

    # Step 4: Adjust file permissions on scripts just to make sure
    # they're correct. It may not be absolutely necessary, but it won't
    # hurt.

    labels.next()
    cmd = f"find {SCRIPTS} -name *.py -exec chmod 754 {{}} ;"
    print(run_one_command(cmd=cmd))

    # ------------------------------------------

    # Step 5: Setting terminal profile. Need a little special handling
    # here, because we're redirecting stdin.

    labels.next()
    cmd = "dconf reset -f /org/gnome/terminal/legacy"
    result = run_one_command(cmd=cmd)
    if result == PASS:
        cmd = "dconf load /org/gnome/terminal/legacy/profiles:/"
        path = SYSTEM / "terminal_settings.txt"
        if DEBUG:
            print(f"Opening: {path}")
        with open(path, "r") as f:
            result = run_one_command(cmd=cmd, std_in=f)
    print(result)

    # ------------------------------------------

    msg = """
    Installing additional software. Please enter your password if
    prompted.
    """
    print(f"\n{textwrap.fill(text=" ".join(msg.split()))}\n")

    # Push a dummy sudo command just to force password entry before
    # first ppa pull. This will avoid having the password prompt come in
    # the middle of a label when providing status

    run_one_command(cmd="sudo ls")

    # ------------------------------------------

    # Step 6: Some baseline packages from the ppa.

    labels.next()
    cmd = "sudo apt -y install TARGET"
    targets = [
        "build-essential",
        "ccache",
        "gnome-text-editor",
        "open-vm-tools-desktop",
        "seahorse",
        "tree",
        "vim",
    ]
    print(run_many_arguments(cmd=cmd, targets=targets))

    # ------------------------------------------

    # Step 7: Install zsh.

    labels.next()
    targets = ["zsh"]
    print(run_many_arguments(cmd=cmd, targets=targets))

    # ------------------------------------------

    # Step 8: Install OhMyZsh.

    labels.next()
    src = "https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/"
    cmd = f"{src}install.sh"
    result = run_shell_script(shell="sh", script=cmd, options='"" --unattended')
    # After zsh installation, copy over new .zshrc file
    if result == PASS:
        file_targets = [(SHELL / "zshrc.conf", HOME / ".zshrc")]
        copy_files(targets=file_targets)
    print(result)

    # ------------------------------------------

    # Step 9: Install OhMyZsh Full-autoupdate

    labels.next()
    zsh_home = HOME / ".oh-my-zsh/custom"
    src = "https://github.com/Pilaton/OhMyZsh-full-autoupdate.git"
    dest = f"{zsh_home}/plugins/ohmyzsh-full-autoupdate"
    cmd = f"git clone --depth=1 {src} {dest}"
    print(run_one_command(cmd=cmd))

    # ------------------------------------------

    # Step 10: Install powerlevel10k theme

    labels.next()
    src = "https://github.com/romkatv/powerlevel10k.git"
    dest = f"{zsh_home}/themes/powerlevel10k"
    cmd = f"git clone --depth=1 {src} {dest}"
    print(run_one_command(cmd=cmd))

    # ------------------------------------------

    # Step 11: Install Nerd Fonts

    labels.next()
    base = "https://github.com/romkatv/powerlevel10k-media/raw/master/"
    fonts: list[str] = [
        "MesloLGS%20NF%20Bold.ttf",
        "MesloLGS%20NF%20Bold%20Italic.ttf",
        "MesloLGS%20NF%20Italic.ttf",
        "MesloLGS%20NF%20Regular.ttf",
    ]
    for font in fonts:
        f_name = "\\ ".join(font.split("%20"))
        cmd = f"curl -sL {base}{font} -o {HOME}/.fonts/{f_name}"
        if (result := run_one_command(cmd=cmd)) == FAIL:
            break
    if result == PASS:
        cmd = "fc-cache -vf"
        result = run_one_command(cmd=cmd)
    print(result)

    # ------------------------------------------

    # Step 12: Setting Text Editor profile. Again, need special handling
    # here, because we're redirecting stdin.

    labels.next()
    cmd = "dconf reset -f /org/gnome/TextEditor/"
    if (result := run_one_command(cmd=cmd)) == PASS:
        cmd = "dconf load /org/gnome/TextEditor/"
        path = SYSTEM / "text_editor_settings.txt"
        if DEBUG:
            print(f"Opening: {path}")
        with open(path, "r") as f:
            result = run_one_command(cmd=cmd, std_in=f)
    print(result)

    # ------------------------------------------

    # Step 13: Refresh snaps

    labels.next()
    cmd = "sudo snap refresh"
    print(run_one_command(cmd=cmd))

    # ------------------------------------------

    # Step 14: Configure favorites. NOTE: To get the information needed
    # for the code below, setup desired favorites, then run this
    # command: gsettings get org.gnome.shell favorite-apps

    labels.next()
    cmd = "gsettings set org.gnome.shell favorite-apps \"['"
    targets = [
        "firefox_firefox.desktop",
        "org.gnome.TextEditor.desktop",
        "org.gnome.Terminal.desktop",
        "org.gnome.Nautilus.desktop",
        "org.gnome.Calculator.desktop",
        "snap-store_snap-store.desktop",
        "org.gnome.Settings.desktop",
        "org.gnome.seahorse.Application.desktop",
    ]
    cmd += "','".join(targets) + "']\""
    print(run_one_command(cmd=cmd))

    # ------------------------------------------

    # Step 15: Disable auto screen lock

    labels.next()
    cmd = "gsettings set org.gnome.desktop.screensaver lock-enabled false"
    print(run_one_command(cmd=cmd))

    # ------------------------------------------

    # Step 16: Set idle timeout to 'never'.

    labels.next()
    cmd = "gsettings set org.gnome.desktop.session idle-delay 0"
    print(run_one_command(cmd=cmd))

    # ------------------------------------------

    # Step 17: Disable auto updates.

    labels.next()
    dest = "/etc/apt/apt.conf.d/20auto-upgrades"
    argument = r"s+Update-Package-Lists\ \"1\"+Update-Package-Lists\ \"0\"+"
    cmd = f"sudo sed -i {argument} {dest}"
    result = run_one_command(cmd=cmd)
    if result == PASS:
        argument = r"s+Unattended-Upgrade\ \"1\"+Unattended-Upgrade\ \"0\"+"
        cmd = f"sudo sed -i {argument} {dest}"
        result = run_one_command(cmd=cmd)
    print(result)

    # ------------------------------------------

    # Step 18: Patch /etc/fuse.conf to un-comment 'user_allow_other'.
    # This allows users to start programs from the command line when
    # their current working directory is inside the share.

    labels.next()
    argument = r"s+\#user_allow_other+user_allow_other+"
    dest = "/etc/fuse.conf"
    cmd = f"sudo sed -i {argument} {dest}"
    print(run_one_command(cmd=cmd))

    # ------------------------------------------

    # Step 19: Arrange icons.

    labels.next()
    base = "org.gnome.shell.extensions."
    targets = [
        f"{base}dash-to-dock show-trash false",
        f"{base}dash-to-dock show-mounts false",
        f"{base}ding start-corner bottom-left",
        f"{base}ding show-trash true",
        f"{base}ding show-home false",
    ]
    cmd = "gsettings set TARGET"
    print(run_many_arguments(cmd=cmd, targets=targets))

    # ------------------------------------------

    # Step 20: Cleanup any unused files.

    labels.next()
    print(PASS)

    # ------------------------------------------

    # Done

    msg = """
    Setup script is complete. If all steps above are marked with green
    checkmarks, Ubuntu is ready to go. You must reboot your VM now for
    the changes to take effect. If any steps above show a red \"X\",
    there was an error during installation.
    """
    print(f"\n{textwrap.fill(text=" ".join(msg.split()))}\n")

    return


def main():
    if result := min_python_version():
        raise RuntimeError(result)

    msg = """
    This script will configure a desktop installation of an Ubuntu
    24.04.x Virtual Machine. This should only be used on a single user
    Virtual Machine installation for a user account with sudo
    privileges. Do not attempt to run this script on a standalone Linux
    machine or dual-boot machine. You will be prompted for your password
    during installation.
    """

    epi = "Latest update: 11/27/24"

    parser = argparse.ArgumentParser(description=msg, epilog=epi)
    parser.parse_args()
    task_runner()

    return


if __name__ == "__main__":
    main()
