---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Pythonista 3を使ってiPhone上でpython実行環境を構築する"
subtitle: ""
summary: " "
tags: ["python","Pythonista 3"]
categories: ["python","Pythonista 3"]
url: python-pythonista-3-insatll-setting.html
date: 2020-01-25
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





定期的に動作させたいわけではないけど、空いている時間にたまーに動かしてみたいpythonのコードがあった。動かしたいときにPCを使える環境であれば良いが常にそういう環境ではないので、出来れば常に持ち歩いているiPhone or iPadから実行できないかと思いPythonista 3を試してみた。

Pythonista 3はiOS上でpythonを実行するための有料アプリ。2020年1月時点では1,200円。

> ‎Pythonista 3 https://apps.apple.com/jp/app/pythonista-3/id1085978097

公式ページはこちら。

> Pythonista for iOS http://omz-software.com/pythonista/

numpy、matplotlib、requestsなどの人気のあるサードパーティモジュールから、iOS用にカスタマイズされたモジュールが使用可能。iPhoneのモーションセンサーデータ、写真ライブラリ、連絡先、アラーム、iOSクリップボードなどの情報にアクセスすることが出来る。

心配な点は継続アップデートがあるかどうか。（最終アップデートが2018年だった）

とはいえ、iOS上で3rd partyモジュールをインストールしてptyhonコードを実行出来る環境は他には見つからなかったので選択肢はこれしかないのかな、という印象。

今回はStaSHをインストールしてpipインストール出来る環境を整え、tweepyを使ってTwitter API操作を行う。

### StaSh インストール

StaSh（Pythoni**<u>sta Sh</u>**ell）はPythonista 3上でpipなどのコマンド操作が出来るようになる拡張機能。Pythonを使う上でpipは必須機能とも言えるのでStaShも入れておくべき。

インストールはまずはコンソールを開き下記コマンドを実行する。このコマンドでは `https://raw.githubusercontent.com/ywangd/stash/master/getstash.py`から**getstash.py**をダウンロードする。

```python
import requests as r; exec(r.get('http://bit.ly/get-stash').text)
```

​	

![image-20200121152807032](image-20200121152807032.png)

githubから**launch_stash.py**がダウンロードされる。"Home directory to Start StaSh"とのこと。

<img src="image-20200121152714804.png" alt="image-20200121152714804" style="zoom:80%;" />

アプリを再起動する。「Script Library」- 「This iPhone」に移動

<img src="image-20200121152920677.png" alt="image-20200121152920677" style="zoom:80%;" />

**launch_stash.py**が配置されているのでこのpythonファイルを実行する。

<img src="image-20200121153023599.png" alt="image-20200121153023599" style="zoom:80%;" />

<img src="image-20200121153053252.png" alt="image-20200121153053252" style="zoom:80%;" />

コンソール画面が起動。この画面でpipコマンドを実行。ここではTwitterAPIのラッパーであるtweepyをインストール。

<img src="image-20200121153128176.png" alt="image-20200121153128176" />

![image-20200121153244289](image-20200121153244289.png)



### pythonコードを実行する

pipで必要なモジュールをインストール出来たので実行するpythonコードをコピペで作って実行してみる。なお、Google DriveやDropboxなどのストレージクラウドから読み込むことは出来ず、ローカルのファイルかiCloudのドライブとなる。

##### ソースコード



![image-20200121153350430](image-20200121153350430.png)

##### 実行結果

![image-20200121153439502](image-20200121153439502.png)

無事に実行できた。これでスマホしか使えないタイミングでもpythonを実行できるのでQOLが向上すると思う。~~ゲームの自動化とかも出来るのかな？~~

更に詳細を知りたい場合はこちらからどうぞ。

> Pythonista for iOS http://omz-software.com/pythonista/