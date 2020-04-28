# ubuntu

## VM Setup Guides (Start Here)

*NOTE: When accessing the links below, or accessing any of the links in the guides, please right-click and open the link in a new Tab or Window. That makes it easier to navigate back to this page.*

- [Part-1: Installing Workstation Player and Downloading the Ubuntu VM Image](setupguides/vmguide-p1.md)
- [Part-2: Installation and Setup of The Ubuntu Virtual Machine](setupguides/vmguide-p2.md)
- [Part-3: Setup Instructions for Folder Sharing and Repo Cloning](setupguides/vmguide-p3.md)
- [Part-4: Setup Instructions for Public Key Encryption in Ubuntu Linux](setupguides/vmguide-p4.md)

---

## Technical Details

This repo manages a series of setup and maintenance scripts for Ubuntu VMs. I started these for Cyber Operations classes at USNA, but they've broadened and become very useful for setting up Ubuntu VMs for any purpose.

*Note: The following aliases are used:*

```Shell
HOME    = os.path.expanduser('~')
CWD     = os.getcwd()
REPO    = HOME + '/ubuntu/config'
ATOM    = REPO + '/atom'
GEDIT   = REPO + '/gedit'
JUPYTER = REPO + '/jupyter'
OHMYZSH = HOME + '/.oh-my-zsh'
SCRIPTS = REPO + '/scripts'
SHELL   = REPO + '/shell'
SYSTEM  = REPO + '/system'
VIM     = REPO + '/vim'
VENVPIP = HOME + '/env/bin/pip3'
```
 
The scripts perform the following functions:

### `setup.py`

This script sets up a newly-created Ubuntu VM with the desired software and settings.

Step 1: This is a placeholder step for future initialization, if required.

Step 2: Create the following directories:

```Shell
~/.config/gedit/tools
~/.config/gedit/snippets
~/.vim/colors
~/shares
~/.atom
```

Step 3: Copy the following files using: `cp -f --backup=numbered`

```Shell
target = '~/.jupyter/lab/user-settings/@jupyterlab/notebook-extension/'

cp ATOM/* ~/.atom
cp GEDIT/flexiwrap ~/.config/gedit/tools
cp GEDIT/python.xml ~/.config/gedit/snippets
cp GEDIT/python3.xml ~/.config/gedit/snippets
cp SCRIPTS/tuneup.py ~/.tuneup.py
cp SHELL/bashrc.txt ~/.bashrc
cp SHELL/zshrc.txt ~/.zshrc
cp SHELL/profile.txt ~/.profile
cp SHELL/dircolors.txt ~/.dircolors
cp VIM/vimrc.txt ~/.vimrc
cp VIM/vimcolors/* ~/.vim/colors
cp JUPYTER/tracker.jupyterlab-settings target
```

Step 4: Adjust file permissions:

```Shell
chmod 744 ~/.tuneup.py
chmod 744 ~/.config/gedit/tools/flexiwrap
```

Step 5: Initialize the terminal profile with:

```Shell
dconf reset -f /org/gnome/terminal/
dconf load /org/gnome/terminal/ < SYSTEM/terminalSettings.txt
```

Step 6: Initialize the gedit profile with:

```Shell
dconf reset -f /org/gnome/gedit/
dconf load /org/gnome/gedit/ < GEDIT/geditSettings.txt
```

Step 7: Install the following packages from the ppa and GitHub repos:

```Shell
vim
build-essential
seahorse-nautilus
gedit-plugins
gedit-plugin-text-size
zsh
powerline fonts-powerline
git clone https://github.com/robbyrussell/oh-my-zsh.git ~/.oh-my-zsh
python3-pip
python3-venv
```

Step 8: Set up jupyter.

```Shell
pip3 install --upgrade jupyter
pip3 install --upgrade jupyterlab
```

Step 9: Setup atom

```Shell
sudo snap install atom --classic
apm install markdown-scroll-sync
```

Step 10: Configure favorites

```Shell
'firefox.desktop'
'org.gnome.Calculator.desktop'
'atom_atom.desktop'
'org.gnome.gedit.desktop'
'org.gnome.Nautilus.desktop'
'org.gnome.Terminal.desktop'
'gnome-control-center.desktop'
'snap-store_ubuntu-software.desktop'
'org.gnome.seahorse.Application.desktop'
```

Step 11: Tune system settings:

```Shell
# Disable auto screen lock
gsettings set org.gnome.desktop.screensaver lock-enabled false

# Set idle timeout to 'never'
gsettings set org.gnome.desktop.session idle-delay 'uint32 0'

# Disable auto system updates
sudo cp -f SYSTEM/20auto-upgrades /etc/apt/apt.conf.d/
```

Step 12: Delete unused files

```Shell
rm -f ~/examples.desktop
```

### `tuneup.py`

This script is used to keep the newly-created Ubuntu VM patched. It performs the following updates:

```Shell
sudo apt -y update
sudo apt -y upgrade
sudo apt -y autoremove

sudo snap refresh atom

# Upgrade ohMyZsh. Check first to see if zsh is the current shell
# and oh-my-zsh is installed. 
~/.oh-my-zsh/tools/upgrade.sh

pip3 install --upgrade jupyter
pip3 install --upgrade jupyterlab
```

### `swiftInstall.py`

*Note: This does not yet work in Ubuntu 20.04. The folks at swift.org have not yet released an update. It will be interesting to see how this evolves, given that support for python2 is being dropped in Ubuntu 20.04*

In addition to the Swift programming environment, this script also installs the following dependencies:

```Shell
sudo apt install -y clang
sudo apt install -y libcurl4
sudo apt install -y libpython2.7
sudo apt install -y libpython2.7-dev
```

### `swiftUpdate.py`

This script will be tuned to update the swift distribution to the latest version.

### `vimsetup.py`

This is a standalone script that allows you to  install the necessary files and settings to create a pleasant visual experience in vi. It's useful if you're got a user account on a Linux server and you just want to tune-up the look-and-feel of vi.

Step 1: This is a placeholder step for future initialization, if required.

Step 2: Create the following directory:

```Shell
~/.vim/colors
```

Step 3: Copy the following files using: `cp -f --backup=numbered`

```Shell
cp VIM/vimrc.txt ~/.vimrc
cp VIM/vimcolors/* ~/.vim/colors
```
