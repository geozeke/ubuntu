#!/usr/bin/env python3

# Author: Peter Nardi
# Date: 02/01/20
# License: (see MIT License at the end of this file)

# Title: VM Setup script

# This script will install the necessary programs and settings files on an
# Ubuntu 18.04.x Virtual Machine for USNA course work in Computer Science or
# Cyber Operations. This should only be used on a single user Virtual Machine
# installation for a user account with sudo privileges. Do not attempt to run
# this script on a standalone Linux machine or dual-boot machine (including lab
# machines). You will be prompted for your password during installation.

# NOTE to self:
# As of python 3.7, there is a new parameter to the subprocess.run() module
# called "capture_output".  If set to true, then stdout and stderr are given
# PIPEs, otherwise they're set to None.

# Imports

import os, argparse, sys

# Need to adjust the python environment path to import local modules

sys.path.append(os.path.expanduser('~') + '/ubuntu/config/scripts')
from configinit import *
from configutils import *

# -------------------------------------------------------------------

def runScript(se):

   os.system('clear')
   
   # Step 1. System initialization.  Right now, it's just a placeholder for
   # future capability.
   
   print(se.FMTSTR.format(se.nextLabel()),end='')
   print('Complete')

   # Step 2. Creating new directories
   
   cmd = 'mkdir -p '
   target = '~/.jupyter/lab/user-settings/@jupyterlab/notebook-extension/'
   packages = [
      (se.nextLabel(),
         cmd + '~/notebooks',
         cmd + '~/.config/gedit/tools',
         cmd + '~/.config/gedit/snippets',
         cmd + '~/.vim/colors',
         cmd + '~/shares',
         cmd + '~/.atom',
         cmd + target)]
   batchCommands(packages,se.FMTSTR)
   
   # Step 3. Copying files
   
   cmd = 'cp -f --backup=numbered '
   packages = [
      (se.nextLabel(),
         cmd + se.ATOM    + '/* ~/.atom',
         cmd + se.GEDIT   + '/flexiwrap ~/.config/gedit/tools',
         cmd + se.GEDIT   + '/python.xml ~/.config/gedit/snippets',
         cmd + se.GEDIT   + '/python3.xml ~/.config/gedit/snippets',
         cmd + se.SCRIPTS + '/tuneup.py ~/.tuneup.py',
         cmd + se.SHELL   + '/bashrc.txt ~/.bashrc',
         cmd + se.SHELL   + '/zshrc.txt ~/.zshrc',
         cmd + se.SHELL   + '/profile.txt ~/.profile',
         cmd + se.SHELL   + '/dircolors.txt ~/.dircolors',
         cmd + se.VIM     + '/vimrc.txt ~/.vimrc',
         cmd + se.VIM     + '/vimcolors/* ~/.vim/colors',
         cmd + se.JUPYTER + '/tracker.jupyterlab-settings ' + target,
         cmd + se.JUPYTER + '/notebooks/* ~/notebooks')]
   batchCommands(packages,se.FMTSTR)
         
   # Step 4. Adjust file permissions
   
   packages = [
      (se.nextLabel(),
         'chmod 744 ~/.tuneup.py',
         'chmod 744 ~/.config/gedit/tools/flexiwrap')]
   batchCommands(packages,se.FMTSTR)
   
   # Step 5. Setting terminal profile.  Need a little special handling here,
   # because we're redirecting stdin.
   
   print(se.FMTSTR.format(se.nextLabel()),end='',flush=True)
   cmd = 'dconf reset -f /org/gnome/terminal/'
   sp.run(globify(cmd),stdout=sp.PIPE,stderr=sp.PIPE)
   f = open(se.SYSTEM + '/terminalSettings.txt')
   cmd = 'dconf load /org/gnome/terminal/'
   sp.run(globify(cmd),stdout=sp.PIPE,stderr=sp.PIPE,stdin=f)
   f.close()
   print('Complete')

   # Step 6. Setting gedit profile.  Again, need special handling here,
   # because we're redirecting stdin.
   
   print(se.FMTSTR.format(se.nextLabel()),end='',flush=True)
   cmd = 'dconf reset -f /org/gnome/gedit/'
   sp.run(globify(cmd),stdout=sp.PIPE,stderr=sp.PIPE)
   f = open(se.GEDIT + '/geditSettings.txt')
   cmd = 'dconf load /org/gnome/gedit/'
   sp.run(globify(cmd),stdout=sp.PIPE,stderr=sp.PIPE,stdin=f)
   f.close()
   print('Complete')

   msg = "\nInstalling additional software. Please enter password if "
   msg += "prompted.\n"
   sp.run(globify('fmt -w 70'),input=msg,encoding='ascii')
   
   # Push a dummy sudo command just to force password entry before first ppa
   # pull. This will avoid having the password prompt come in the middle of a
   # label when providing status
   
   sp.run(globify('sudo ls'),stdout=sp.PIPE,stderr=sp.PIPE)
   
   # Steps 7. Packages from the ppa and zsh
   
   cmd = 'sudo apt -y install '
   packages = [
      (se.nextLabel(),cmd + 'vim'),
      (se.nextLabel(),cmd + 'build-essential'),
      (se.nextLabel(),cmd + 'seahorse-nautilus'),
      (se.nextLabel(),
         cmd + 'gedit-plugins',
         cmd + 'gedit-plugin-text-size'),
      (se.nextLabel(),
         cmd + 'zsh',
         cmd + 'powerline fonts-powerline',
         'git clone https://github.com/robbyrussell/oh-my-zsh.git ~/.oh-my-zsh'),
      (se.nextLabel(),cmd + 'python3-pip'),
      (se.nextLabel(),cmd + 'python3-venv')]
   batchCommands(packages,se.FMTSTR)
   
   # Step 8 Install jupyter
   
   cmd = 'pip3 install --upgrade '
   packages = [
      (se.nextLabel(),cmd + 'jupyter'),
      (se.nextLabel(),cmd + 'jupyterlab')]
   batchCommands(packages,se.FMTSTR)
   
   # Step 9 Install atom
   
   packages = [
      (se.nextLabel(),
         'sudo snap install atom --classic',
         'apm install markdown-scroll-sync')]
   batchCommands(packages,se.FMTSTR)
      
   # Cleanup: Silently delete unused files
   
   packages = [
      (se.nextLabel(),
         'rm -f ~/examples.desktop')]
   batchCommands(packages,se.FMTSTR)
   
   # For completeness, restore the python environment path   
   
   del sys.path[-1]

   # Done
   
   msg  = "\nUbuntu setup complete. Please reboot your VM for the changes to "
   msg += "take effect.\n\n"
   sp.run(globify('fmt -w 70'),input=msg,encoding='ascii')

   return

# -------------------------------------------------------------------

def main():
   
   # Get a new ScriptEnvironment variable with all the necessary properties
   # initialized.
   
   se = ScriptEnvironment(sys.argv[0])

   # Verify that python is at the minimum version
   
   if se.checkPythonVersion() != None:
      raise Exception(se.checkPythonVersion())
      
   # Build a python argument parser
   
   msg  = "This script will install the necessary programs and settings files "
   msg += "on an Ubuntu 18.04.x Virtual Machine for USNA course work in "
   msg += "Computing Sciences or Cyber Operations. This should only be used on "
   msg += "a single user Virtual Machine installation for a user account with "
   msg += "sudo privileges. Do not attempt to run this script on a standalone "
   msg += "Linux machine or dual-boot machine (including lab machines).  You "
   msg += "will be prompted for your password during installation."
   
   epi = "Latest update: 01 Feb 2020"
   
   parser = argparse.ArgumentParser(description=msg,epilog=epi)
   
   args = parser.parse_args()
   
   runScript(se)
   
   return
   
# -------------------------------------------------------------------

if __name__ == '__main__':
   main()

# ========================================================================

# MIT License

# Copyright 2019-2020 Peter Nardi

# Terms of use for source code:

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
