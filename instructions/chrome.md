# chrome

The chrome web browser for linux.

## Installation

1. FireFox comes with Ubuntu.  Using FireFox from within the Ubuntu VM, visit: [https://www.google.com/chrome/](https://www.google.com/chrome/)

2. Click the `Download Chrome` button and select the version for *64 bit .deb (For Debian/Ubuntu)*

3. Click on `Accept and Install`

4. When the dialog box comes up, choose to Save the file (rather than open it).  This will place the Chrome installer in your Downloads folder.

5. Install Chrome with these commands:

```Shell
cd ~/Downloads
sudo apt install ./google-chrome-stable_current_amd64.deb
rm google-chrome-stable_current_amd64.deb
```

## Usage

Enter:

```Shell
google-chrome-stable &
```

then pin the icon to your favorites.

## Additional Help

[http://google.com/chrome](http://google.com/chrome)

---
*Last update: 02/05/20*
