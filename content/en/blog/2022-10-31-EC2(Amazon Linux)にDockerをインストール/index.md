---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Installing Docker on EC2 (Amazon Linux)"
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

Place this in user data when creating the EC2, or run it manually after launch.

```sh
#!/bin/bash
sudo yum update -y
sudo amazon-linux-extras install docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -a -G docker ec2-user
```

For verification:

```
docker -v
docker run hello-world
```
