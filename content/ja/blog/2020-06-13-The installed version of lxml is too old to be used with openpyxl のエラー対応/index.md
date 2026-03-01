---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "The installed version of lxml is too old to be used with openpyxl のエラー対応"
subtitle: ""
summary: " "
tags: ["python"]
categories: ["python"]
url: python-lxml-old-error.html
date: 2020-02-13
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



#### lxmlが古いとエラー

おそらくin2csvで内部的に使っていると推測

```sh
[ec2-user@bastin ~]$ aws dms describe-table-statistics --replication-task-arn $(aws dms describe-replication-tasks | jq -r '.ReplicationTasks[].ReplicationTaskArn') | jq '.TableStatistics' | in2csv -f json
/home/ec2-user/.local/lib/python2.7/site-packages/openpyxl/xml/__init__.py:15: UserWarning: The installed version of lxml is too old to be used with openpyxl
```

#### lxmlをアップグレードする

```sh
[ec2-user@bastin ~]$ sudo pip install --upgrade lxml
DEPRECATION: Python 2.7 reached the end of its life on January 1st, 2020. Please upgrade your Python as Python 2.7 is no longer maintained. A future version of pip will drop support for Python 2.7. More details about Python 2 support in pip, can be found at https://pip.pypa.io/en/latest/development/release-process/#python-2-support
Collecting lxml
  Downloading lxml-4.5.1-cp27-cp27mu-manylinux1_x86_64.whl (5.5 MB)
     |████████████████████████████████| 5.5 MB 10.0 MB/s 
Installing collected packages: lxml
  Attempting uninstall: lxml
    Found existing installation: lxml 3.2.1
    Uninstalling lxml-3.2.1:
      Successfully uninstalled lxml-3.2.1
Successfully installed lxml-4.5.1
```

