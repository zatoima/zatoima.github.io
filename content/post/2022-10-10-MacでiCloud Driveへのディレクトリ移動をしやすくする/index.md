---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "MacでiCloud Driveへのディレクトリ移動をしやすくする"
subtitle: ""
summary: " "
tags: ["Mac"]
categories: ["Mac"]
url: Mac-icloud-drive-ln-create
date: 2022-10-10
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

iCloudの場所がややこしくて一発で移動しにくいのでシンボリックリンクを作成。

```sh
ln -s $HOME/Library/Mobile\ Documents/com~apple~CloudDocs/ $HOME/iCloud
```

$HOME配下に設定。これで移動しやすくなったはず。

```sh
(base) zatoima@M1MBA ~ % ls -l $HOME/iCloud
lrwxr-xr-x  1 zatoima  staff  60 10 10 10:59 /Users/zatoima/iCloud -> /Users/zatoima/Library/Mobile Docu
```

