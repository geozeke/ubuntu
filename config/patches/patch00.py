#!/usr/bin/env python3

# Author: Peter Nardi
# Date: 08/17/20
# License: (see MIT License at the end of this file)

# Title: VM Patch 00 (patch00)

# This patch fixes issue 45 -- for details, visit:
# https://github.com/geozeke/ubuntu/issues/45

# Imports
import subprocess as sp
import os, argparse
import textwrap
from datetime import datetime

# Constants
PATCHLOG = '/.patchlog'
PATCHID = 'patch00'
# Expand '~' into the absolute path for the user's home directory.
HOME = os.path.expanduser('~')
# Save required patch dependencies as a list of strings indicating the missing
# PATCHIDs, e.g:
# DEPENDS = ['patch01','patch02']
DEPENDS = []

# ------------------------------------------------------------------

# This encapsulates the portion of the script that does the actual patching.

def patchCode():
   
   # Patch /etc/fuse.conf to un-comment 'user_allow_other'
   cmd  = ['sudo','sed','-i']
   cmd += ['s+\#user_allow_other+user_allow_other+']
   cmd += ['/etc/fuse.conf']
   sp.run(cmd,capture_output=True)

   # Check to see if .profile is already patched.
   f = open(HOME + '/.profile','r')
   contents = f.read()
   f.close()
   goodProfile = '-o nonempty -o allow_other' in contents

   # If .profile is not patched, then patch it.
   if not goodProfile:
      cmd  = ['sudo','sed','-i']
      cmd += ['s+-o nonempty+-o nonempty -o allow_other+']
      cmd += [HOME + '/.profile']
      sp.run(cmd,capture_output=True)
   
   # Log this patch as having been applied for future reference
   f = open(HOME + PATCHLOG,'a+')
   f.write(PATCHID + ';')
   f.write(datetime.now().strftime("%B-%d-%Y") + '\n')
   f.close()
   
   msg  = 'Patch successfully applied. You must reboot your VM for the '
   msg += 'changes to take effect.'
   print('\n' + textwrap.fill(msg) + '\n')

   return

# ------------------------------------------------------------------

def patchScan():
   
   patchNeeded = True
   patchD = {}
   
   # Check .patchlog to see if this patch has already been applied by building a
   # dictionary of installed patches. This will also allow for checking
   # dependencies of future patches.
   if os.path.exists(HOME + PATCHLOG):
      with open(HOME + PATCHLOG,'r') as f:
         for line in f:
            (key,val) = line.split(';')
            patchD[key] = val.strip()
            
      f.close()
      
      if PATCHID in patchD:
         patchNeeded = False
         patchDate = patchD[PATCHID]
   
   # Patch needed
   if patchNeeded:
      # Check dependencies
      missingDepends = ''
      for d in DEPENDS:
         if d not in patchD:
            missingDepends += d + ', '
      
      if missingDepends != '':
         msg  = 'The following dependencies are missing: '
         msg += missingDepends.strip(', ') + '. '
         msg += 'Please install patch dependencies first, then return to '
         msg += 'install ' + PATCHID + '.'
         print('\n' + textwrap.fill(msg) + '\n')
         
      else:
         patchCode()
   
   # Patch already applied.
   else:
      msg  = 'This patch was previously applied on ' + patchDate.strip() + '. '
      msg += 'Applying it again is not necessary.'
      print('\n' + textwrap.fill(msg) + '\n')
      
   return

# ------------------------------------------------------------------

def main():
   
   # Build a python argument parser
   
   msg  = "Fixes issue #45 -- for more information, visit: "
   msg += "https://github.com/geozeke/ubuntu/issues/45"
   
   epi = "Latest update: 10 Aug 2020"
   
   parser = argparse.ArgumentParser(description=msg,epilog=epi)
   
   args = parser.parse_args()
   
   patchScan()
   
   return
   
# ------------------------------------------------------------------

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