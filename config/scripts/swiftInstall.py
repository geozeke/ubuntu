#!/usr/bin/env python3

# Author: Peter Nardi
# Date: 12/10/20
# License: (see MIT License at the end of this file)

# Title: Swift installation script

# This script will install swift on Ubuntu 20.04.x.

# Imports

import os, argparse, sys, textwrap

# Need to adjust the python environment path to import local modules

sys.path.append(os.path.expanduser('~') + '/ubuntu/config/scripts')
from configinit import *
from configutils import *

# -------------------------------------------------------------------

def runScript(se):

   os.system('clear')
   print('Please enter your password if prompted.\n')

   # Push a dummy sudo command just to force password entry before first ppa
   # pull. This will avoid having the password prompt come in the middle of a
   # label when providing status
   
   sp.run(globify('sudo ls'),capture_output=True)
   
   # Step 1. System initialization - Make Swift temp dir then change to it.
   
   cmd = 'mkdir -p ' + se.TEMPDIR
   packages = [(se.nextLabel(),cmd)]
   batchCommands(packages,se.FMTSTR)
   os.chdir(se.TEMPDIR)

   cmd = 'sudo apt install -y '

   # Step 2. Install clang
   
   packages = [(se.nextLabel(),cmd + 'clang')]
   batchCommands(packages,se.FMTSTR)
   
   # Step 3. Install required dependencies
   
   packages = [
      (se.nextLabel(),
         cmd + 'libpython2.7')]
   batchCommands(packages,se.FMTSTR)
         
   # Step 4. Download Swift to the tmp directory
   
   cmd = 'wget ' + se.SWIFTURL
   packages = [(se.nextLabel(),cmd)]
   batchCommands(packages,se.FMTSTR)
   
   # Step 5. Unpack files.
   
   cmd = 'tar -xzf ' + se.SWIFTPKG
   packages = [(se.nextLabel(),cmd)]
   batchCommands(packages,se.FMTSTR)

   # Step 6. Move files into position. Strip '.tar.gz' from the swift package.
   # That will produce a string that points to the unpacked contents of the
   # se.SWIFTPKG.
   
   cmd = 'sudo mv ' + se.SWIFTPKG.strip('.tar.gz') + ' ' + se.SWIFTDIR
   packages = [(se.nextLabel(),cmd)]
   batchCommands(packages,se.FMTSTR)

   # Step 7. Validate / update PATH as necessary
   
   PATH = os.environ['PATH']
   SHELL = os.environ['SHELL']
   
   if '/usr/share/swift/usr/bin' not in PATH:
   
      if SHELL == '/bin/bash':
         RC = '/.bashrc'
      elif SHELL == '/bin/zsh':
         RC = '/.zshrc'
   
      f = open(se.HOME + RC,'a+')
      f.write('\nPATH=/usr/share/swift/usr/bin:$PATH\n')
      f.close()

   # Step 8. Clean up and restore the original cwd.
   
   os.chdir(se.CWD)
   cmd = 'rm -rf ' + se.TEMPDIR
   packages = [(se.nextLabel(),cmd)]
   batchCommands(packages,se.FMTSTR)

   # For completeness, restore the python environment path   
   
   del sys.path[-1]

   # Done
   
   msg  = 'Swift version ' + se.SWIFTVER + ' installation complete. Please '
   msg += 'reboot your VM for the changes to take effect.'
   print('\n' + textwrap.fill(msg) + '\n\n')
   
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
   
   msg  = "This script will install swift ver " + se.SWIFTVER + " on Ubuntu "
   msg += "20.04.x. You will be prompted for your password during installation."
   
   epi = "Latest update: 10 Dec 2020"
   
   parser = argparse.ArgumentParser(description=msg,epilog=epi)
   
   args = parser.parse_args()
   
   runScript(se)
   
   return
   
# -------------------------------------------------------------------

if __name__ == '__main__':
   main()

# ========================================================================

# MIT License

# Copyright 2020 Peter Nardi

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
