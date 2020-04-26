#!/usr/bin/env python3

# Author: Peter Nardi
# Date: 04/26/20
# License: (see MIT License at the end of this file)

# Title: Config Init

# Implementation of a class that defines global variables for the Ubuntu
# scripting runtime environment.  This allows for maintenance of these
# variables in one place, to be used with any Ubuntu VM script.

# Imports

import os, sys

class ScriptEnvironment:

   def __init__(self,scriptName):
   
      # The script name passed to the initializer will be sys.argv[0]
      self.script = scriptName.split('/')[-1]
      
      # Minimum required python version for Ubuntu VM scripts.
      self.MAJOR = 3
      self.MINOR = 6

      # Paths in the repo for installation files.
      self.HOME    = os.path.expanduser('~')
      self.CWD     = os.getcwd()
      self.REPO    = self.HOME + '/ubuntu/config'
      self.ATOM    = self.REPO + '/atom'
      self.GEDIT   = self.REPO + '/gedit'
      self.JUPYTER = self.REPO + '/jupyter'
      self.OHMYZSH = self.HOME + '/.oh-my-zsh'
      self.SCRIPTS = self.REPO + '/scripts'
      self.SHELL   = self.REPO + '/shell'
      self.SYSTEM  = self.REPO + '/system'
      self.VIM     = self.REPO + '/vim'
      self.VENVPIP = self.HOME + '/env/bin/pip3'

      # Swift Specific

      # Check the URL on Swift.org to make sure it's correct, but you should
      # only have to change the SWIFTVER variable below to run the script
      # properly.
      self.SWIFTVER  = '5.2.1'
      
      self.SWIFTURL  = 'https://swift.org/builds/swift-' + self.SWIFTVER
      self.SWIFTURL += '-release/ubuntu1804/swift-' + self.SWIFTVER
      self.SWIFTURL += '-RELEASE/swift-' + self.SWIFTVER
      self.SWIFTURL += '-RELEASE-ubuntu18.04.tar.gz'
      
      self.SWIFTPKG  = 'swift-' + self.SWIFTVER + '-RELEASE-ubuntu18.04.tar.gz'
      self.SWIFTDIR  = '/usr/share/swift'
      self.TEMPDIR   = "/tmp/placeholder" + str(os.getpid())
      
      # Labels
      self.LABELS = []
      self.FMTSTR = ""
      
      self.initLabels()
      
      return

# -------------------------------------------------------------------
# Initialize the labels based on the script being run

   def initLabels(self):
      
      if self.script == "setup.py":

         # Step 1
         self.LABELS.append('System initialization')
         # Step 2
         self.LABELS.append('Creating new directories')
         # Step 3
         self.LABELS.append('Copying files')
         # Step 4
         self.LABELS.append('Adjusting file permissions')
         # Step 5
         self.LABELS.append('Setting terminal profile')
         # Step 6
         self.LABELS.append('Setting gedit profile')
         # Step 7
         self.LABELS.append('Installing vim')
         self.LABELS.append('Installing developer tools')
         self.LABELS.append('Installing seahorse nautilus')
         self.LABELS.append('Installing gedit plugins')
         self.LABELS.append('Installing zsh')
         self.LABELS.append('Installing pip3')
         self.LABELS.append('Installing python3 venv')
         # Step 8
         self.LABELS.append('Installing jupyter')
         self.LABELS.append('Installing jupyter lab')
         # Step 9
         self.LABELS.append('Installing atom (please be patient)')
         # Step 10
         self.LABELS.append('Configuring favorites')
         # Step 11
         self.LABELS.append('Tuning System Settings')
         # Step 12
         self.LABELS.append('Cleaning up')         

      elif self.script == ".tuneup.py":
      
         self.LABELS.append('Scanning for updates to jupyter')
         self.LABELS.append('Scanning for updates to jupyter lab')
         
      elif self.script == "swiftInstall.py":
         
         self.LABELS.append('System initialization')
         self.LABELS.append('Installing clang')
         self.LABELS.append('Installing required dependencies')
         
         msg = 'Downloading swift ' + self.SWIFTVER 
         msg += ' (this may take some time)'
         self.LABELS.append(msg)
         
         self.LABELS.append('Unpacking files')
         self.LABELS.append('Moving files into position')
         self.LABELS.append('Validating PATH')
         self.LABELS.append('Cleaning up')
         
      elif self.script == "swiftUpdate.py":
         
         self.LABELS.append('System initialization')
         self.LABELS.append('Removing older version of swift')
         self.LABELS.append('Validating clang is the most-recent version')
         self.LABELS.append('Checking for updated dependencies')
         
         msg = 'Downloading swift ' + self.SWIFTVER
         msg += ' (this may take some time)'
         self.LABELS.append(msg)
         
         self.LABELS.append('Unpacking files')
         self.LABELS.append('Moving files into position')
         self.LABELS.append('Validating PATH')
         self.LABELS.append('Cleaning up')

      elif self.script == "vimsetup.py":
         
         self.LABELS.append('System initialization')
         self.LABELS.append('Creating new directories')
         self.LABELS.append('Copying files')

# -------------------------------------------------------------------

      # Reverse the label list so we can pop items off the end as we go.
      self.LABELS.reverse()

      # Calculate the length of the longest label.  Add 3 to provide some
      # buffer to print at least 3 dots for the longest label
      maxLabel = 0
      for label in self.LABELS:
         if len(label) > maxLabel:
            maxLabel = len(label)
      maxLabel += 3

      # Setup a formatted printing string for the labels
      self.FMTSTR = '{0:.<' + str(maxLabel) + 's}'
      
      return

# -------------------------------------------------------------------

   # Return the next label in the list
   def nextLabel(self):
      return self.LABELS.pop()
      
# -------------------------------------------------------------------

   # Checks that the installed python version is at the minimum required.  If it
   # is, then None is returned.  If it's not, then an error message is returned.

   def checkPythonVersion(self):
      
      if ((sys.version_info.major < self.MAJOR) or
         (sys.version_info.minor < self.MINOR)):
         
         msg  = "Script requires Python "
         msg += str(self.MAJOR) + "." + str(self.MINOR)
         msg += " or greater"
         
         return msg
         
      return None

# -------------------------------------------------------------------

def main():
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
