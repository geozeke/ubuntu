#!/usr/bin/env python3
"""Utilities for ubuntu scripts."""

import os
import pathlib
import re
import shlex
import shutil
import subprocess as sp
import sys
import tempfile as tf
import textwrap
from typing import Any
from typing import Text

from .classes import Environment


def clear() -> None:
    """Clear the screen.

    This is an os-agnostic version, which will work with both Windows
    and Linux.
    """
    os.system("clear" if os.name == "posix" else "cls")


def clean_str(bstr: bytes) -> Text:
    """Convert a bytestring.

    Performs the utf-8 conversion of a byte stream and strips any
    trailing white space or newline characters

    Parameters
    ----------
    bstr : bytes
        A byte string to be converted.

    Returns
    -------
    Text
        A utf-8 string.
    """
    return bstr.decode("utf-8").rstrip()


def wrap_tight(msg: str, columns=70) -> str:
    """Clean up a multi-line docstring.

    Take a multi-line docstring and wrap it cleanly as a paragraph to a
    specified column width.

    Parameters
    ----------
    msg : str
        The docstring to be wrapped.
    columns : int, optional
        Column width for wrapping, by default 70.

    Returns
    -------
    str
        A wrapped paragraph.
    """
    clean = " ".join([t for token in msg.split("\n") if (t := token.strip())])
    return textwrap.fill(clean, width=columns)


def lean_text(str_in: str) -> str:
    """Strip blank lines and comments from a text file.

    Take the contents of a text file, contained in a string variable,
    and strip lines that are either blank (no printable characters), or
    lines that represent comments (start with '#')

    Note: If the file contains a environment line (e.g. #!/bin/bash),
    that line will be stripped as well.

    Parameters
    ----------
    str_in : str
        A text file saved in a string variable.

    Returns
    -------
    str
        The input string, with blank lines and comment lines removed.
    """
    clean_lines: list[str] = []
    input_lines: list[str] = str_in.split("\n")
    for line in input_lines:
        if re.search(r"^\s*$", line):  # Skip whitespace/blank lines
            continue
        if re.match(r"^\s*#", line):  # Skip lines starting with '#'
            continue
        clean_lines.append(line)
    return "\n".join(clean_lines)


def run_one_command(
    e: Environment,
    cmd: str,
    capture: bool = True,
    std_in: Any | None = None,
    std_out: Any | None = None,
) -> Text:
    """Run a single command in the shell.

    Parameters
    ----------
    e : Environment
        All the environment variables saved as attributes in an
        Environment object.
    cmd : str
        A shell command (with potentially options) saved as a Python
        string.
    capture : bool, optional
        Determine if stdout should be suppressed (True) or displayed
        (False), by default True.
    std_in : Any | None
        If stdin needs to be redirected on the command line you can
        pass an open file descriptor here for that purpose. It can be
        any kind of file object (Text/Binary), by default None.
    std_out : Any | None
        If stdout needs to be redirected on the command line you can
        pass an open file descriptor here for that purpose. It can be
        any kind of file object (Text/Binary), by default None.

    Returns
    -------
    Text
        Returns a unicode string representing either a green checkmark
        (PASS) or a red X (FAIL).
    """
    if e.DEBUG:
        print(f"\nRunning: {shlex.split(cmd)}")
        return e.PASS
    else:
        e.RESULT = sp.run(
            shlex.split(cmd), capture_output=capture, stdin=std_in, stdout=std_out
        )
        if e.RESULT.returncode != 0:
            return e.FAIL
    return e.PASS


def run_many_arguments(
    e: Environment, cmd: str, targets: list[str], marker: str = "TARGET"
) -> Text:
    """Run the same command with multiple arguments.

    Parameters
    ----------
    e : Environment
        All the environment variables saved as attributes in an
        Environment object.
    cmd : str
        A shell command (with potentially options) saved as a Python
        string.
    targets : list[str]
        A Python list of strings representing the different arguments
        to be used on multiple runs of the command.
    marker : str, optional
        A string representing the replacement marker in the command
        string. Every time the command is run, a new target will be put
        in place of the marker. By default 'TARGET'.

    Returns
    -------
    Text
        Returns a unicode string representing either a green checkmark
        (PASS) or a red X (FAIL).
    """
    for target in targets:
        result = run_one_command(e, cmd.replace(marker, target))
        if result == e.FAIL:
            return result
    return result


def run_script(
    e: Environment,
    script: str,
    shell: str = "bash",
    as_sudo: bool = False,
    capture: bool = True,
) -> Text:
    """Run a remote shell script.

    Parameters
    ----------
    e : Environment
        All the environment variables saved as attributes in an
        Environment object.
    script : str
        URL of the remote script.
    shell : str, optional
        Shell to run (e.g. bash, sh, etc.), by default 'bash'.
    as_sudo : bool, optional
        Run the script as sudo, by default False.
    capture : bool, optional
        Capture stdout or not, by default True.

    Returns
    -------
    Text
        Returns a unicode string representing either a green checkmark
        (PASS) or a red X (FAIL).
    """
    with tf.TemporaryFile(mode="w") as f:
        cmd = f"curl -sL {script}"
        result = run_one_command(e, cmd, capture=False, std_out=f)
        if result == e.PASS:
            f.seek(0)
            if as_sudo:
                cmd = f"sudo {shell}"
            else:
                cmd = shell
            result = run_one_command(e, cmd, capture=capture, std_in=f)
    return result


def copy_files(
    e: Environment, targets: list[tuple[pathlib.Path, pathlib.Path]]
) -> None:
    """Copy files from source to destination.

    Parameters
    ----------
    e : Environment
        All the environment variables saved as attributes in an
        Environment object.
    targets : list[tuple[pathlib.Path, pathlib.Path]]
        A list of tuples. Files will be copied from source [0] to
        destination [1].
    """
    for target in targets:
        copy_from, copy_to = target[0], target[1]
        if e.DEBUG:
            print(f"\nCopying: {str(copy_from)}\nTo: {str(copy_to)}")
        else:
            if "*" in copy_from.name:
                for file in copy_from.parent.resolve().glob(copy_from.name):
                    shutil.copy(file, copy_to)
            else:
                shutil.copy(copy_from, copy_to)
    return


def sync_notebooks(e: Environment) -> Text:
    """Synchronize jupyter notebooks.

    Sync the hidden repository with the local notebooks directory. Use
    the --delete option so the destination directory always exactly
    mirrors the source directory. Also use the --delete-excluded option
    in case a stray file from the source, which should be excluded,
    makes its way to the destination. Per the man page, leaving a
    trailing slash ('/') on the source directory allows you to sync the
    contents of the source directory to a destination directory with a
    different name.

    Parameters
    ----------
    e : Environment
        All the environment variables saved as attributes in an
        Environment object.

    Returns
    -------
    Text
        Returns a unicode string representing either a green checkmark
        (PASS) or a red X (FAIL).
    """
    src = f"{e.HOME}/.notebooksrepo/"
    dest = f"{e.HOME}/notebooks"
    exclude = f"{e.SYSTEM}/rsync_exclude.txt"
    options = f"-rc --exclude-from={exclude} --delete --delete-excluded"
    cmd = f"rsync {src} {dest} {options}"
    return run_one_command(e, cmd)


def min_python_version(e: Environment) -> Text | None:
    """Determine if Python is at required min version.

    Parameters
    ----------
    e : Environment
        All the environment variables saved as attributes in an
        Environment object.

    Returns
    -------
    str | None
        If Python is at the minimum version return None. If not,
        return a string error message.
    """
    msg = f"Minimum required Python version is {e.MAJOR}.{e.MINOR}"
    if (sys.version_info.major < e.MAJOR) or (sys.version_info.minor < e.MINOR):
        return msg
    return None


if __name__ == "__main__":
    pass
