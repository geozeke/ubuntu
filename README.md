# <a id="top"></a> ubuntu

<br>

<img
src="https://drive.google.com/uc?export=view&id=1H04KVAA3ohH_dLXIrC0bXuJXDn3VutKc"
alt = "Dinobox logo" width="120"/>

## NOTE

This repository has many dependencies that are pinned to Ubuntu 24.04.x.
It will not work with older versions of Ubuntu.

## VM Setup (Start Here)

These tools work with Ubuntu. You'll create either a Desktop (GNOME)
installation, or a Server (no GUI) installation. Setup a basic Ubuntu
machine using your preferred tools and techniques. Then use these tools
to configure your installation with a standard look-and-feel, tools, and
settings that I use in my workflows.

## Included Tools

* [desktop_setup.py](#desktop_setup)
* [server_initialize.py](#server) and [server_configure.py](#server)
* [docker_setup.py](#docker_setup)
* [vim_setup.py](#vim_setup)

### <a id="desktop_setup"></a> `desktop_setup.py`

This script sets up a new Ubuntu Desktop VM with the following software
and settings:

* Setup and configure zsh and vim
* Initialize the terminal profile and GNOME text editor with a nicer
  color scheme.
* Install the following packages from the ppa:
  * build-essential
  * ccache
  * gnome-text-editor
  * nala
  * python3-pip
  * python3-venv
  * seahorse-nautilus
  * tree
  * zsh
* Install [pipx][def6].
* Install and configure [OhMyZsh][def] and the [powerlevel10K
  theme][def2].
* Configure the GNOME favorites in the application launcher.
* Tune system settings:
  * Disable auto screen lock.
  * Set idle timeout to 'never'.
  * Disable Ubuntu auto-updates.
  * Patch `/etc/fuse.conf` to un-comment `user_allow_other`. This
    permits running programs from the command line when you're inside a
    directory in the share point.

#### usage

Once you complete the initial setup of your desktop installation, open a
terminal and run these commands:

```shell
cd
sudo apt install git curl -y # just to be sure
git clone https://github.com/geozeke/ubuntu.git
./ubuntu/scripts/desktop_setup.py
```

From there, follow the on-screen instructions.

[top](#top)

### <a id="server"></a> `server_initialize.py` and `server_configure.py`

These two scripts work together to initialize and configure a Server
version of Ubuntu (one without a desktop environment). An easy and
elegant way to create a server VM like this is by using
[Multipass](https://multipass.run).

`server_initialize.py`

After creating and logging-in to the new VM, run these commands:

```shell
cd
sudo apt install git curl -y # just to be sure
git clone https://github.com/geozeke/ubuntu.git
./ubuntu/scripts/server_initialize.py -h
```

Follow the directions provided in the on-screen help.

`server_configure.py`

After initializing the server, login with the new user credentials you
created when you ran `server_initialize.py`. Then run the commands
below. The script will setup vim and [OhMyZsh](<[def3]>). NOTE: For all
new Ubuntu instances, a default account is created called `ubuntu`. When
you run this script you also have the option to delete the default
account.

#### usage

```shell
cd
git clone https://github.com/geozeke/ubuntu.git # yes, do it again.
./ubuntu/scripts/server_configure.py -h
```

Follow the directions provided in the on-screen help.

Once the configuration script is complete, do this:

1. Reboot the VM.
2. Login with your new credentials.
3. Change your login shell to zsh by running: `chsh` and entering
   `/bin/zsh` when prompted.
4. Logout and log back in.
5. You should be all set.

[top](#top)

### <a id="pyenv_setup"></a> `pyenv_setup.py`

This script sets up and installs the incredibly helpful utility
[pyenv][def3]. This utility allows you to install and manage multiple
versions of python, without breaking the system default installation.

#### usage

```shell
~/ubuntu/scripts/pyenv_setup.py
```

[top](#top)

### <a id="docker_setup"></a> `docker_setup.py`

This standalone script will install [Docker Engine][def4], which is the
underlying client-server technology that builds and runs containers
using Docker's components and services. It also installs [Docker
Compose][def5], and sets up the appropriate user permissions to run
docker without having to enter `sudo` first.

#### usage

```shell
~/ubuntu/scripts/docker_setup.py
```

[top](#top)

### <a id="vim_setup"></a> `vim_setup.py`

This is a standalone script that allows you to install the necessary
files and settings to create a pleasant visual experience in vi. It's
useful if you've got a user account (with no sudo access) on a Linux
server and you just want a better look-and-feel for vi.

#### usage

```shell
~/ubuntu/scripts/vim_setup.py
```

[top](#top)

[def]: https://ohmyz.sh
[def2]: https://github.com/romkatv/powerlevel10k
[def3]: https://github.com/pyenv/pyenv
[def4]: https://docs.docker.com/engine/
[def5]: https://docs.docker.com/get-started/08_using_compose/
[def6]: https://pipx.pypa.io/stable/
