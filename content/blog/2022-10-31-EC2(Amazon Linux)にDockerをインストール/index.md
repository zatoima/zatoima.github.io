---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "EC2(Amazon Linux)にDockerをインストール"
subtitle: ""
summary: " "
tags: ["AWS"]
categories: ["AWS"]
url: aws-ec2-docker-amazon-linux-install
date: 2022-10-31
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

EC2作成時にユーザデータにぶっこむか、もしくは起動後に手動実行

```sh
#!/bin/bash
sudo yum update -y
sudo amazon-linux-extras install docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -a -G docker ec2-user
```

動作確認用

```
docker -v
docker run hello-world
```

