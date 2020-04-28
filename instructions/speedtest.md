# speedtest

You may be familiar with a free tool for testing internet connection speeds called *speedtest*. It's available via a website ([speedtest.net](https://speedtest.net)) as well as an application for desktop and mobile devices. Here's what the maker of *speedtest* has to say:

*Speedtest® by Ookla® is the definitive way to test the speed and performance of your internet connection. Every day, over ten million unique tests are actively initiated by our users in the locations and at the times when their connectivity matters to them. Since our founding in 2006, an unparalleled total of more than 25 billion tests have been taken with Speedtest.*

In addition to accessing *speedtest* via their website or their applications, you can also install a command line interface (cli) version on your Ubuntu VM. 

## Installation

```Shell
pip3 install speedtest-cli 
```

## Usage

```Shell
speedtest-cli
```

Here's a sample run of *speedtest-cli*

```Shell
ubuntu:~$ speedtest-cli
Retrieving speedtest.net configuration...
Testing from University of Maryland (136.160.90.6)...
Retrieving speedtest.net server list...
Selecting best server based on ping...
Hosted by AT&T (Washington, DC) [37.27 km]: 6.7 ms
Testing download speed........................................
Download: 648.74 Mbit/s
Testing upload speed..........................................
Upload: 365.63 Mbit/s
```


## Additional Help

[speedtest.net](https://www.speedtest.net)

---
*Last update: 02/13/20*
. 