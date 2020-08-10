# nuitka

Nuitka is a Python compiler written in Python.

## Installation

```
pip3 install nuitka 
```

## Usage

In its simplest form, you use nuitka this way:

```
python3 -m nuitka file.py
```

You can create a shortcut with nuitka's commonly used settings by putting this in your `.bashrc` (or `.zshrc`):

```
alias nb="python3 -m nuitka --recurse-all --remove-output"
```

Now, `nb` (what I think of as *nuitka build*) can be used like this:

```
nb file.py
```

## Additional Help

[http://nuitka.net](http://nuitka.net)

---
*Last update: 02/03/20*
