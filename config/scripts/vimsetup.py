#!/usr/bin/env python3

# Author: Peter Nardi
# Date: 02/11/20
# License: (see MIT License at the end of this file)

# Title: vim Setup script

# This script installs the necessary settings files and color schemes for a
# pleasant experience in vi.

# NOTE to self:
# As of python 3.7, there is a new parameter to the subprocess.run() module
# called "capture_output". If set to true, then stdout and stderr are given
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
   
   # Step 1. System initialization. Right now, it's just a placeholder for
   # future capability.
   
   print(se.FMTSTR.format(se.nextLabel()),end='')
   print('Complete')

   # Step 2. Creating new directory
   
   cmd = 'mkdir -p '
   packages = [
      (se.nextLabel(),
         cmd + '~/.vim/colors')]
   batchCommands(packages,se.FMTSTR)
   
   # Step 3. Copying files
   
   cmd = 'cp -f --backup=numbered '
   packages = [
      (se.nextLabel(),
         cmd + se.VIM + '/vimrc.txt ~/.vimrc',
         cmd + se.VIM + '/vimcolors/* ~/.vim/colors')]
   batchCommands(packages,se.FMTSTR)
         
   # For completeness, restore the python environment path   
   
   del sys.path[-1]

   # Done
   
   msg  = "\nvim setup complete. You're now ready to use vi or vim and "
   msg += "enjoy a pleasing visual experience.\n\n"
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
   
   msg  = "This script installs the necessary settings files and color schemes "
   msg += "for a pleasant visual experience in vi. NOTE: If you've already "
   msg += "run the ubuntu setup script, there's no need to run this script."
   
   epi = "Latest update: 11 Feb 2020"
   
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
