---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "runinstaller Execution Error on EC2"
subtitle: ""
summary: " "
tags: ["AWS", "EC2", "Oracle"]
categories: ["AWS", "EC2", "Oracle"]
url: aws-oracle-ec2-runinstaller-error.html
date: 2019-10-12
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: ""
  focal_point: ""
  preview_only: fals
---


Even after configuring xclock and xeyes to work, running runinstaller results in an error.

The steps I followed were:

> Setting Up X Window System on AWS EC2 - zato logger [https://www.zatolog.com/entry/aws-ec2-xwindow](https://www.zatolog.com/entry/aws-ec2-xwindow)

```bash
[oracle@db121s-dev-ec2-oracle database]$ ./runInstaller
Starting Oracle Universal Installer...

Checking Temp space: must be greater than 500 MB.   Actual 75212 MB    Passed
Checking swap space: 0 MB available, 150 MB required.    Failed <<<<
Checking monitor: must be configured to display at least 256 colors
    >>> Could not execute auto check for display colors using command /usr/bin/xdpyinfo. Check if the DISPLAY variable is set.    Failed <<<<

Some requirement checks failed. You must fulfill these requirements before

continuing with the installation,

Continue? (y/n) [n] y
```



### Reason 1: Checking swap space: 0 MB available, 150 MB required. Failed <<<<

---

The official Linux AMI's default configuration has no swap partition, so a swap area needs to be configured.

Refer to the following procedures and manual for details.

> Using a Swap File to Allocate Memory as Swap Space for Amazon EC2 Instances [https://aws.amazon.com/jp/premiumsupport/knowledge-center/ec2-memory-swap-file/](https://aws.amazon.com/jp/premiumsupport/knowledge-center/ec2-memory-swap-file/)
> Amazon EC2 (Linux) Swap Area Best Practices | DevelopersIO [https://dev.classmethod.jp/cloud/ec2linux-swap-bestpractice/](https://dev.classmethod.jp/cloud/ec2linux-swap-bestpractice/)
> Instance Store Swap Volumes - Amazon Elastic Compute Cloud [https://docs.aws.amazon.com/ja_jp/AWSEC2/latest/UserGuide/instance-store-swap-volumes.html](https://docs.aws.amazon.com/ja_jp/AWSEC2/latest/UserGuide/instance-store-swap-volumes.html)

### Reason 2: Checking monitor: must be configured to display at least 256 colors >>> Could not execute auto check for display colors using command /usr/bin/xdpyinfo. Check if the DISPLAY variable is set. Failed <<<<

---

In this case, xdpyinfo itself was not installed, so I installed it with yum. When I saw "DISPLAY variable," I assumed it was a problem with Xming or X11 forwarding on the server side... It was simply the straightforward issue that xdpyinfo was not installed.
