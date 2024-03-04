# <a id="top"></a> ubuntu

<br>

<img
src="https://drive.google.com/uc?export=view&id=1H04KVAA3ohH_dLXIrC0bXuJXDn3VutKc"
alt = "Dinobox logo" width="120"/>

## VM Setup Guides (Start Here)

To install a new Ubuntu Virtual Machine (desktop version) using the tools in
this repository, follow the setup guide available here: [Ubuntu
Setup](https://sites.google.com/view/ubuntuvm). This repository also includes
tools to initialize and configure a server version of Ubuntu.

## Included Tools

This repo manages a series of setup and maintenance scripts for Ubuntu VMs. I
originally started this repo for Cyber Operations classes at USNA, but it's
broadened and become useful for setting up Ubuntu VMs for any purpose.

* [desktop_setup.py](#desktop_setup)
* [server_initialize.py](#server) and [server_configure.py](#server)
* [tuneup.py](#tuneup)
* [docker_setup.py](#docker_setup)
* [vim_setup.py](#vim_setup)

### <a id="desktop_setup"></a> `desktop_setup.py`

This script sets up a new Ubuntu VM with the following software and settings:

* Setup and configure zsh and vim
* Initialize the terminal profile with a nicer color scheme.
* Install the following packages from the ppa:
  * gnome-text-editor
  * build-essential
  * ccache
  * nala
  * tree
  * seahorse-nautilus
* Configure the gnome favorites in the application launcher.
* Tune system settings:
  * Disable auto screen lock.
  * Set idle timeout to 'never'.
  * Disable Ubuntu auto-updates.
  * Patch `/etc/fuse.conf` to un-comment `user_allow_other`. This permits
    running programs from the command line when you're inside a directory in
    the share point.

#### usage

Follow the [VM Setup Guides](#top).

[top](#top)

### <a id="server"></a> `server_initialize.py` and `server_configure.py`

These two scripts work together to initialize and configure a server version of
Ubuntu (one without a desktop environment). An easy and elegant way to create a
server VM like this is by using [Multipass](https://multipass.run).

`server_initialize.py`

After creating and logging-in to the new VM, clone this repo and run this
script. It will install some basic tools and create a new user account, which
you can specify on the command line.

`server_configure.py`

After initializing the server, login with the new user credentials you created,
clone this repo again, and run this script. It will setup vim and [Oh My
Zsh](https://ohmyz.sh). Note, for all new Ubuntu instances, a default account is
created called `ubuntu`. When you run this script you also have the option to
delete the default account.

#### usage

Learn about each script by getting help on the command line:

`~/ubuntu/scripts/server_initialize.py -h`

`~/ubuntu/scripts/server_configure.py -h`

[top](#top)

### <a id="pyenv_setup"></a> `pyenv_setup.py`

This script sets up and installs the incredibly helpful utility
[pyenv](https://github.com/pyenv/pyenv). This utility allows you to install and
manage multiple versions of python, without breaking the system default
installation.

#### usage

`~/ubuntu/scripts/pyenv_setup.py`

[top](#top)

### <a id="tuneup"></a> `tuneup.py`

This script is used to keep the newly-created Ubuntu VM patched. It performs
the following updates:

* `sudo apt update && sudo apt upgrade`
* `sudo apt -y autoremove`
* `sudo apt -y autoclean`
* `sudo snap refresh`
* Pull updates to this repo to support patching if necessary.
* Synchronize jupyter notebooks to catch updates.

#### usage

An alias for this script is created when the VM is setup. To run the tuneup
script and get help, just enter: `tuneup -h`.

### <a id="docker_setup"></a> `docker_setup.py`

This standalone script will install [Docker
Engine](https://docs.docker.com/engine/), which is the underlying client-server
technology that builds and runs containers using Docker's components and
services. It also installs [Docker
Compose](https://docs.docker.com/get-started/08_using_compose/), and sets up
the appropriate user permissions to run docker without having to enter `sudo`
first.

#### usage

`~/ubuntu/scripts/docker_setup.py`

[top](#top)

### <a id="vim_setup"></a> `vim_setup.py`

This is a standalone script that allows you to install the necessary files and
settings to create a pleasant visual experience in vi. It's useful if you've
got a user account (with no sudo access) on a Linux server and you just want a
better look-and-feel for vi.

#### usage

`~/ubuntu/scripts/vim_setup.py`

[top](#top)
