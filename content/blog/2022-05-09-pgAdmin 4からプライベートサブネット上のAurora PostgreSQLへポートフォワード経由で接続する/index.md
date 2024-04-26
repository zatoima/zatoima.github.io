---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "pgAdmin4からAurora PostgreSQLへ踏み台サーバのポートフォワード経由で接続する"
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

### SSHクライアント側の設定

XShellというSSHクライアント使っていますが、Teratermでも同じような設定が可能。

![image-20220508211201115](image-20220508211201115.png)

### pgAdmin4の設定

Generalで任意の名前を追加

![image-20220508211553430](image-20220508211553430.png)

SSHクライアントで指定したlocalhostとポート番号を指定する

![image-20220508211627533](image-20220508211627533.png)

### 正常ログイン後のダッシュボード

![image-20220508211511001](image-20220508211511001.png)
