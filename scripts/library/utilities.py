#!/usr/bin/env python3

"""Utilities for ubuntu scripts."""

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
    """Clear the screen.

    This is an os-agnostic version, which will work with both Windows
    and Linux.
    """
    os.system('clear' if os.name == 'posix' else 'cls')

# -------------------------------------------------------------------


def cleanStr(bytes):
    """Convert a bytestring.

    Performs the utf-8 conversion of a byte stream and strips any
    trailing white space or newline characters

    Parameters
    ----------
    bytes : bytes
        A byte string to be converted.

    Returns
    -------
    str
        A utf-8 string.
    """
    return bytes.decode('utf-8').rstrip()

# -------------------------------------------------------------------


def runOneCommand(e, cmd, capture=True, std_in=None, std_out=None):
    """Run a single command in the shell.

    Parameters
    ----------
    e : Environment
        All the environment variables, saved as attributes in an
        Environment object.
    cmd : [str]
        A shell command (with potentially options) saved as a Python
        list of strings.
    capture : bool, optional
        Determine if stdout should be suppressed (True) or displayed
        (False), by default True.
    std_in : _io.TextIOWrapper, optional
        If stdin needs to be redirected on the command line, you can
        pass an open file descriptor here for that purpose, by default
        None.
    std_out : _io.TextIOWrapper, optional
        If stdin needs to be redirected on the command line, you can
        pass an open file descriptor here for that purpose, by default
        None.

    Returns
    -------
    unicode
        Returns a unicode string, represeting either a green checkmark
        (PASS) or a red X (FAIL).
    """
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


def runManyArguments(e, cmd, targets):
    """Run the same command with multiple arguments.

    Parameters
    ----------
    e : Environment
        All the environment variables, saved as attributes in an
        Environment object.
    cmd : [str]
        A shell command (with potentially options) saved as a Python
        list of strings.
    targets : [str]
        A Python list of strings, representing the different arguments
        to be used on multiple runs of the command.

    Returns
    -------
    unicode
        Returns a unicode string, represeting either a green checkmark
        (PASS) or a red X (FAIL).
    """
    for target in targets:
        result = runOneCommand(e,
                               cmd.replace('TARGET', target).split())
        if result == e.FAIL:
            return result
    return result

# -------------------------------------------------------------------


def copyFiles(e, targets):
    """Copy files from source to destination.

    Parameters
    ----------
    e : Environment
        All the environment variables, saved as attributes in an
        Environment object.
    targets : [(str, str)]
        A list of tuples. Files will be copied from source [0] to
        destination [1].
    """
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
    """Determine if Python is at required min version.

    Parameters
    ----------
    e : Environment
        All the environment variables, saved as attributes in an
        Environment object.

    Returns
    -------
    str | None
        If Python is at the minimum version, return None. If not,
        return a string error message.
    """
    msg = f'Minimum required Python version is {e.MAJOR}.{e.MINOR}'
    if ((sys.version_info.major < e.MAJOR) or
       (sys.version_info.minor < e.MINOR)):
        return msg
    return None

# -------------------------------------------------------------------


def main():  # noqa
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
