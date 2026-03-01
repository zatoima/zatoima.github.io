---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "T2 Instance Type Cannot Be Used When Using EC2 Instance Store"
subtitle: ""
summary: " "
tags: ["AWS","EC2"]
categories: ["AWS","EC2"]
url: aws-ec2-instancestore-setting.html
date: 2019-10-19
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



### Introduction

Instance store is suitable for temporary storage of frequently changing data (such as buffers, caches, scratch data, temporary logs, dump data, and other temporary content). There is no additional charge. Since it is a volatile disk, data is lost when the instance is stopped and started. (Data is not lost on reboot.)

### What I Misunderstood

As the title says, the instance type I commonly used (t2 series) does not support instance store. The types that support it are listed in the manual below.

> The number and size of instance store volumes available to your instance varies by instance type. Some instance types do not support instance store volumes.
>
> Adding Instance Store Volumes to an EC2 Instance - Amazon Elastic Compute Cloud https://docs.aws.amazon.com/ja_jp/AWSEC2/latest/UserGuide/add-instance-store-volumes.html

> Your instance type determines the amount of instance store available to your instance and the type of hardware used for the instance store volumes.
>
> Amazon EC2 Instance Store - Amazon Elastic Compute Cloud https://docs.aws.amazon.com/ja_jp/AWSEC2/latest/UserGuide/InstanceStorage.html

As shown below, for storage-optimized instance types, `ephemeral0` appears as a volume type during instance creation. This is the instance store.

#### t2.large (General Purpose)

<img src="image-20191121220922386.png" alt="image-20191121220922386" style="zoom: 80%;" />

#### i3.large (Storage Optimized)

<img src="image-20191121220940319.png" alt="image-20191121220940319" style="zoom: 80%;" />

### Configuring/Verifying Instance Store

After launching the instance, instance store volumes are available to the instance, but cannot be accessed until the volume is mounted. For Linux instances, the instance type determines which instance store volumes are mounted and which ones you can mount yourself.

#### Initial State

```sh
[ec2-user@ip-10-0-0-16 ~]$ df -h
Filesystem      Size  Used Avail Use% Mounted on
devtmpfs        7.5G     0  7.5G   0% /dev
tmpfs           7.5G     0  7.5G   0% /dev/shm
tmpfs           7.5G  464K  7.5G   1% /run
tmpfs           7.5G     0  7.5G   0% /sys/fs/cgroup
/dev/xvda1      8.0G  1.3G  6.8G  16% /
tmpfs           1.5G     0  1.5G   0% /run/user/0
tmpfs           1.5G     0  1.5G   0% /run/user/1000
[ec2-user@ip-10-0-0-16 ~]$
```

#### Create File System and Mount

```sh
# Commands
mkfs.ext4 -E nodiscard /dev/nvme0n1
mkdir /mnt/ssd
mount -o discard /dev/nvme0n1 /mnt/ssd

# Execution log
[root@ip-10-0-0-16 ec2-user]# mkfs.ext4 -E nodiscard /dev/nvme0n1
mke2fs 1.42.9 (28-Dec-2013)
Filesystem label=
OS type: Linux
Block size=4096 (log=2)
Fragment size=4096 (log=2)
Stride=0 blocks, Stripe width=0 blocks
28999680 inodes, 115966796 blocks
5798339 blocks (5.00%) reserved for the super user
First data block=0
Maximum filesystem blocks=2264924160
3540 block groups
32768 blocks per group, 32768 fragments per group
8192 inodes per group
Superblock backups stored on blocks:
	32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632, 2654208,
	4096000, 7962624, 11239424, 20480000, 23887872, 71663616, 78675968,
	102400000

Allocating group tables: done
Writing inode tables: done
Creating journal (32768 blocks): done
Writing superblocks and filesystem accounting information: done

[root@ip-10-0-0-16 ec2-user]# echo $?
0
[root@ip-10-0-0-16 ec2-user]#
[root@ip-10-0-0-16 ec2-user]#
[root@ip-10-0-0-16 ec2-user]#
[root@ip-10-0-0-16 ec2-user]# mkdir /mnt/ssd
[root@ip-10-0-0-16 ec2-user]#
[root@ip-10-0-0-16 ec2-user]#
[root@ip-10-0-0-16 ec2-user]# mount -o discard /dev/nvme0n1 /mnt/ssd
[root@ip-10-0-0-16 ec2-user]#
```

#### Add to fstab (to mount after reboot)

```sh
vi /etc/fstab
 /dev/nvme0n1                                    /mnt/ssd       ext4   defaults,nofail   0   2
```

#### Verify

```sh
[root@ip-10-0-0-16 ec2-user]# df -h
Filesystem      Size  Used Avail Use% Mounted on
devtmpfs        7.5G     0  7.5G   0% /dev
tmpfs           7.5G     0  7.5G   0% /dev/shm
tmpfs           7.5G  464K  7.5G   1% /run
tmpfs           7.5G     0  7.5G   0% /sys/fs/cgroup
/dev/xvda1      8.0G  1.3G  6.8G  16% /
tmpfs           1.5G     0  1.5G   0% /run/user/0
tmpfs           1.5G     0  1.5G   0% /run/user/1000
/dev/nvme0n1    436G   73M  414G   1% /mnt/ssd   ★← Instance Store
[root@ip-10-0-0-16 ec2-user]#
```

#### Performance Comparison

```sh
# Instance Store
dd if=/dev/zero of=/mnt/ssd/write.tmp count=5 bs=1024M

→ 5368709120 bytes (5.4 GB) copied, 14.8873 s, 361 MB/s

# EBS
dd if=/dev/zero of=/home/ec2-user/write.tmp count=5 bs=1024M

→ 5368709120 bytes (5.4 GB) copied, 53.8642 s, 99.7 MB/s

```

- Performance values vary significantly depending on the instance type being used.

  > Checking Whether SSD Performance Changes by Instance Type https://blog.manabusakai.com/2015/06/instance-store-benchmark/

### Other Notes

- Instance store volumes can only be specified at instance launch time. You cannot attach instance store volumes to an instance after launch.

- When you change the instance type, instance store is not attached to the new instance type.
