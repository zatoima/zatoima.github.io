---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Windows10でssh-keygen"
subtitle: ""
summary: " "
tags: ["Windows"]
categories: ["Windows"]
url: windows10-ssh-keygen-generate
date: 2021-09-23
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



OpenSSHがWindows10に標準搭載されていることでssh-keygenも使えるようになっていることに気づく。Puttyとか入れる必要が無く便利

```
cd /d D:\key
ssh-keygen.exe -q -t rsa -b 4096 -C "" -N "" -f gcp-for-keypair
```

作成される鍵

- gcp-for-keypair.pub：公開鍵
- gcp-for-keypair:秘密鍵

