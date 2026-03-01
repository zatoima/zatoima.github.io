---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Setting Up X Window System on AWS EC2"
subtitle: ""
summary: " "
tags: ["AWS", "EC2", "Oracle"]
categories: ["AWS", "EC2", "Oracle"]
url: aws-ec2-xwindow.html
date: 2019-10-10
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

An X Window System environment was required when installing Oracle Database (DBCA), so I configured X to run on EC2. Getting X Window System running on EC2 seemed like it would be difficult, but it turned out to be possible by just installing a few packages with yum.

### Prerequisite Version

```sh
[ec2-user@bastin ~]$ cat /etc/os-release
NAME="Amazon Linux"
VERSION="2"
ID="amzn"
ID_LIKE="centos rhel fedora"
VERSION_ID="2"
PRETTY_NAME="Amazon Linux 2"
ANSI_COLOR="0;33"
CPE_NAME="cpe:2.3:o:amazon:amazon_linux:2"
HOME_URL="https://amazonlinux.com/"
[ec2-user@bastin ~]$ cat /etc/image-id
image_name="amzn2-ami-hvm"
image_version="2"
image_arch="x86_64"
image_file="INCOMPLETE-amzn2-ami-hvm-2.0.20191116.0-x86_64.xfs.gpt"
image_stamp="ec6f-62ed"
image_date="20191118225945"
recipe_name="amzn2 ami"
recipe_id="cd573903-ca89-ecf8-cb7f-1320-48ba-1a6d-730da3c5"
[ec2-user@bastin ~]$
```

### Install Xming on the Client Side (Windows)

> File Downloads - Xming X Server for Windows - OSDN https://ja.osdn.net/projects/sfnet_xming/releases/

### Install xorg-related Packages

- xorg-x11-xauth.x86_64
- xorg-x11-server-utils.x86_64

```sh
sudo yum -y install xorg-x11-xauth.x86_64 xorg-x11-server-utils.x86_64
```

### Verify with xeyes

```sh
sudo yum -y install xeyes
xeyes
```

### Notes

#### Configuration File

Check that "X11Forwarding" is set to yes in /etc/ssh/sshd_config

### SSH Terminal Settings

#### For Teraterm

In Teraterm's [Settings]-[SSH Forwarding], a window called "SSH Port Forwarding" appears. Check "Forward X11 client applications" in that window.

#### For [Xshell](https://www.netsarang.com/en/xshell/)

Configure the X11Forwarding destination.

#### User

Be careful about the executing user (Note: behavior was different for users switched via su or su -, but I'm not 100% sure about this.)
