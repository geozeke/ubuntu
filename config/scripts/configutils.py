#!/usr/bin/env python3

# Author: Peter Nardi
# Date: 06/08/20
# License: (see MIT License at the end of this file)

# Title: Common utilities for Ubuntu VM Scripts

# Imports

import subprocess as sp, os, sys
from glob import glob

# -------------------------------------------------------------------

# Many functions in the “subprocess” module have a “shell” parameter whose
# default value is False. If it is set to True, then a Unix shell is invoked
# between Python and the command. This means the command should be passed as a
# string to subprocess and wildcard characters will get expanded. There are
# actually injection vulnerabilities with doing it that way, so globify uses
# python's glob.glob library to expand the wildcard characters into a list of
# separate strings which can be passed to subprocess() without using a separate
# shell.
# Note: To expand ~, use: os.path.expanduser('~').

def globify(cmd):

   parts = cmd.split()
   result = []

   for i in range(len(parts)):
      if '~' in parts[i]:
         parts[i] = parts[i].replace('~',os.path.expanduser('~'))
      if '*' in parts[i]:
         result += glob(parts[i])
         continue
      result.append(parts[i])
   
   return result

# -------------------------------------------------------------------

# Takes a list of tuples (packages). The first item in each tuple is a label,
# the remaining item(s) in each tuple are commands to execute. The fmrStr
# (format string) creates a right margin for each label, with leading dots
# ('.'). This creates a pleasing presentation, with all the results ('Complete'
# or 'Failure') aligned to the same column. If any of the commands in a batch
# fails (return code != 0), then the entire batch will have been considered a
# fail. This is just a high-level warning, like a "Check Engine" light.
# 
# The optional parameter "msg" allows for tuning of the message that's printed
# when the commands are finished running.

def batchCommands(packages, fmtStr, msg='Complete'):

   success = True
   
   for package in packages:
      
      print(fmtStr.format(package[0]),end='',flush=True)
      
      for i in range(1,len(package)):
         result = sp.run(globify(package[i]),capture_output=True)
         if result.returncode != 0:
            success = False
      
      print(msg) if success else print('Failure')
   
   return
 
# -------------------------------------------------------------------

# Performs the utf-8 conversion of a byte stream and strips any trailing
# white space or newline characters

def cleanStr(bytes):
   return bytes.decode('utf-8').rstrip()

# -------------------------------------------------------------------

# Checks that the installed python version is at the minimum required. If it is,
# then None is returned. If it's not, then an error message is returned.

def checkPythonVersion(se):
   
   if sys.version_info.major < se.MAJOR or sys.version_info.minor < se.MINOR:
      msg  = "Script requires Python "
      msg += str(se.MAJOR) + "." + str(se.MINOR)
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
