---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Fiware/Orionで使うMongoDBへの接続先を変更する"
subtitle: ""
summary: " "
tags: ["Docker","Fiware"]
categories: ["Docker","Fiware"]
url: fireware-orion-mongodb-connection-change
date: 2022-01-15
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, Bott
---

マニュアルの参照先はここになる。Firewareの公式マニュアルがGoogleで引っかかりにくいのは何故。

- Docker - FIWARE-Orion https://fiware-orion.letsfiware.jp/user/docker/

> ### 2A. MongoDB はローカルホスト上にある場合
>
> これを実行するには、このコマンドを実行します。
>
> ```
>  sudo docker run -d --name orion1 -p 1026:1026 fiware/orion
> ```
>
> すべてが動作することを確認します。
>
> ```
>  curl localhost:1026/version
> ```
>
> ### 2B. MongoDB が別の Docker コンテナで動作している場合
>
> 他のコンテナで MongoDB を実行したい場合は、次のように起動することができます
>
> ```
>  sudo docker run --name mongodb -d mongo:4.4
> ```
>
> そして、このコマンドで Orion を実行します
>
> ```
>  sudo docker run -d --name orion1 --link mongodb:mongodb -p 1026:1026 fiware/orion -dbhost mongodb
> ```
>
> すべてが動作することを確認します。
>
> ```
>  curl localhost:1026/version
> ```
>
> このメソッドは、セクション1で説明したものと機能的に同等ですが、docker-compose ファイルではなく手動でステップを実行します。 MongoDB コンテナを無効にするとすぐにデータが失われます。
>
> ### 2C. MongoDB が異なるホスト上で動作している場合
>
> 別の MongoDB インスタンスに接続する場合は、前のコマンドの**代わりに**、次のコマンドを実行します
>
> ```
>  sudo docker run -d --name orion1 -p 1026:1026 fiware/orion -dbhost <MongoDB Host>
> ```
>
> すべてが動作することを確認します。
>
> ```
>  curl localhost:1026/version
> ```
