# Part-4: Setup Instructions for Public Key Encryption in Ubuntu Linux

Public Key encryption works by creating a set of mathematically related keys (long strings of characters) that permit encryption and decryption of files. A file encrypted with a public key can only be decrypted with the associated private key. In this way we can share our public keys with anyone without being concerned about compromise, as long as we always keep our private keys secure.

![](images/image36.png)

In this course, each of us will generate a key pair (public and private) and share our public keys. We can then post encrypted files in a common shared folder and only the intended recipients will be able to decrypt the files and access the contents

## Step - 1:

If you have not completed Parts 1, 2 and 3 of the installation instructions, please do so before proceeding.

- [Part-1: Installing Workstation Player and Downloading the Ubuntu VM Image](vmguide-p1.md)
- [Part-2: Installation and Setup of The Ubuntu Virtual Machine](vmguide-p2.md)
- [Part-3: Setup Instructions for Folder Sharing and Repo Cloning](vmguide-p3.md)

## Step - 2:

Click on the *`Passwords and Keys`* icon.

![](images/image37.png)

## Step - 3:

If you see the screen below, click on the arrow in the top left corner of the window.

![](images/image39a.png)

Now click on the plus sign (+) in the top left corner of the *`Passwords and Keys`* window. In the pop-up window that follows click on *`GPG Key`*.

![](images/image39.png)

## Step - 4:

In the next window, enter your full name and USNA e-mail address. Leave all the defaults as-is. When you're ready, click *`Create`*

![](images/image40.png)

## Step - 5:

Enter the same password you used for your VM login and enter it again to confirm it. When you're ready, click on *`OK`*.

![](images/image41.png)

## Step - 6:

Once your key pair is generated (it may take a little while) it will show up in your list of keys. To see your key list, double-click on the *`GnuPG keys`* item in the *Passwords and Keys window*.

![](images/image42.png)

## Step - 7:

Export your public key to allow others to send you encrypted files. To generate and export your public key, open a terminal window and enter the commands below:

Start by changing your directory to the Desktop.

```Shell
cd ~/Desktop
```

Next, enter the command below, replacing my name and email address with your own.

```Shell
gpg --armor --output nardi.asc --export nardi@usna.edu
```

## Step - 8:

As a final step, click on the three dots shown below and select the *`Show Any`* option.

![](images/image45.png)

## Step - 9:

You're all set!  Your instructor will guide you through posting your public keys and encrypting / decrypting files.
