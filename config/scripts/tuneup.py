#!/usr/bin/env python3

# Author: Peter Nardi
# Date: 12/10/20
# License: (see MIT License at the end of this file)

# Title: VM Tuneup Script

# This script will perform system updates to an Ubuntu VM.

# Imports

import os, argparse, sys, textwrap

# Need to adjust the python environment path to import local modules

sys.path.append(os.path.expanduser('~') + '/ubuntu/config/scripts')
from configinit import *
from configutils import *

# -------------------------------------------------------------------

def runUpdates(args,se):

   # Ubuntu updates (verbose)
   
   sp.run(globify('sudo apt -y update'))
   sp.run(globify('sudo apt -y upgrade'))
   
   # Snap updates (verbose)
   
   sp.run(globify('sudo snap refresh'))
   
   # Cleaning up
   
   sp.run(globify('sudo apt -y autoremove'))
         
   # Perform additional updates if -a is selected
   
   if args.updateAll:
      
      print('\nPerforming additional updates\n')

      # Pull updates to the ubuntu git repo. This facilitates installing custom
      # patches later.
      os.chdir(se.HOME + '/ubuntu')
      cmd = 'git pull'
      packages = [(se.nextLabel(),cmd)]
      batchCommands(packages,se.FMTSTR)

      # Update jupyter and jupyterlab
      cmd = 'pip3 install --upgrade '
      packages = [(se.nextLabel(),cmd + 'jupyter')]
      batchCommands(packages,se.FMTSTR)
      packages = [(se.nextLabel(),cmd + 'jupyterlab')]
      batchCommands(packages,se.FMTSTR)

      # Sync jupyter notebooks
      print(se.FMTSTR.format(se.nextLabel()),end='',flush=True)

      # Pull updates to notebooks repo
      os.chdir(se.HOME + '/.notebooksrepo')
      sp.run(globify('git pull'),capture_output=True)
      
      # Sync repo with local notebooks. Use the --delete option so the
      # destination directory always exactly mirrors the source directory. Also
      # skip syncing any git-related files. Per the man page, leaving a trailing
      # slash ('/') on the source directory allows you to have a destination
      # directory with a different name.
      cmd  = globify('rsync -rc')
      cmd += ['--exclude','.git*']
      cmd += ['--exclude','LICENSE*']
      cmd += ['--exclude','README*']
      cmd += globify('~/.notebooksrepo/ ~/notebooks --delete')
      sp.run(cmd,capture_output=True)
      
      # Reset cwd
      os.chdir(se.CWD)
      
      print('Complete')
      
   # For completeness, restore the python environment path
   
   del sys.path[-1]

   # Done
   
   msg  = "All updates and upgrades are complete. A reboot is recommended "
   msg += "to ensure that the changes take effect."
   print('\n' + textwrap.fill(msg) + '\n')

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
   
   msg  = 'This script will perform updates of system files and software '
   msg += 'installed through Ubuntu Personal Package Archives (ppa). You will '
   msg += 'be prompted for your password during updating.'
   
   epi = "Latest update: 10 Dec 2020"
   
   parser = argparse.ArgumentParser(description=msg,epilog=epi,prog='tuneup')
   
   msg  = 'In addition to updating Ubuntu system, ppa and snap files, also '
   msg += 'update preinstalled pip3 packages in Python and synchronize '
   msg += 'installed jupyter notebooks.'
   parser.add_argument('-a',
      help=msg,
      required=False,
      action='store_true',
      dest='updateAll')

   args = parser.parse_args()
   
   runUpdates(args,se)
   
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
