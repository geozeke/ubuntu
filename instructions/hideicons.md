# Hiding Home and Trash Icons in Ubuntu

When you load Ubuntu, you may see both *Trash* and *Home* icons on your desktop.  If you'd prefer to have either of those icons hidden, you can achieve that with a few shell commands.

## Implementation (Ubuntu 20.04)

```Shell
# To hide the home icon:
gsettings set org.gnome.shell.extensions.desktop-icons show-home false

# To hide the trash icon:
gsettings set org.gnome.shell.extensions.desktop-icons show-trash false

# To display the icons again, change 'false' to 'true' in the commands above
```

## Usage

```Shell
N/A
```

## Additional Help

[How do I remove home folder from the desktop?](https://askubuntu.com/questions/479546/how-do-i-remove-home-folder-from-the-desktop)

---
*Last update: 04/12/20*
