#!/usr/bin/env python3

# Author: Peter Nardi
# Date: 01/17/22
# License: (see MIT License at the end of this file)

# Title: Common utilities for Ubuntu VM Scripts

# Imports

import os
import shutil
import subprocess as sp
import sys

# -------------------------------------------------------------------


def clear():
    """Clear the screen

    This is an os-agnostic version, which will work with both Windows
    and Linux.
    """
    return os.system('clear' if os.name == 'posix' else 'cls')

# -------------------------------------------------------------------

# Performs the utf-8 conversion of a byte stream and strips any trailing
# white space or newline characters


def cleanStr(bytes):
    return bytes.decode('utf-8').rstrip()

# -------------------------------------------------------------------

# Run a single command


def runOneCommand(e, cmd, capture=True, std_in=None, std_out=None):
    if e.DEBUG:
        print(f'\nRunning: {cmd}')
        return e.PASS
    else:
        e.RESULT = sp.run(cmd, capture_output=capture, stdin=std_in,
                          stdout=std_out)
        if e.RESULT.returncode != 0:
            return e.FAIL
    return e.PASS

# -------------------------------------------------------------------

# Run a single command, multiple times, with different arguments.


def runManyArguments(e, cmd, targets):
    for target in targets:
        result = runOneCommand(e,
                               cmd.replace('TARGET', target).split())
        if result == e.FAIL:
            return result
    return result

# -------------------------------------------------------------------


def copyFiles(e, targets):
    for target in targets:
        copy_from, copy_to = target[0], target[1]
        if e.DEBUG:
            print(f'\nCopying: {str(copy_from)}\nTo: {str(copy_to)}')
        else:
            if '*' in copy_from.name:
                for file in copy_from.parent.resolve().glob(copy_from.name):
                    shutil.copy(file, copy_to)
            else:
                shutil.copy(copy_from, copy_to)
    return

# -------------------------------------------------------------------


def minPythonVersion(e):
    msg = f'Minimum required Python version is {e.MAJOR}.{e.MINOR}'
    if ((sys.version_info.major < e.MAJOR) or
       (sys.version_info.minor < e.MINOR)):
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

# Copyright 2019-2022 Peter Nardi

# Terms of use for source code:

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
