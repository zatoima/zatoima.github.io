---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Connecting to Aurora PostgreSQL from pgAdmin4 via Bastion Server Port Forwarding"
subtitle: ""
summary: " "
tags: ["AWS","Aurora"]
categories: ["AWS","Aurora"]
url: aws-aurora-postgres-pgadmin4-bastin-connect
date: 2022-05-09
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

### SSH Client Configuration

I use an SSH client called XShell, but similar settings can be configured in Tera Term as well.

![image-20220508211201115](image-20220508211201115.png)

### pgAdmin4 Configuration

Add any name you like under General.

![image-20220508211553430](image-20220508211553430.png)

Specify the localhost and port number that you configured in the SSH client.

![image-20220508211627533](image-20220508211627533.png)

### Dashboard After Successful Login

![image-20220508211511001](image-20220508211511001.png)
