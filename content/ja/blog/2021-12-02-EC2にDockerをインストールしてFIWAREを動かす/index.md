---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "EC2にDockerをインストールしてFIWAREを動かす"
subtitle: ""
summary: " "
tags: ["AWS","Docker","Fiware"]
categories: ["AWS","Docker","Fiware"]
url: aws-ec2-docker-fiware-install
date: 2021-12-02
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

## 事前準備編

### Dockerインストール

```sh
sudo yum install -y docker
sudo systemctl start docker
sudo usermod -a -G docker ec2-user
```

### 自動起動を有効にする

```sh
sudo systemctl enable docker
```

## FIWAREのインストール

FIWAREの手順は下記の公式のgithubを参照

> [tutorials\.Getting\-Started/README\.ja\.md at master · FIWARE/tutorials\.Getting\-Started · GitHub](https://github.com/FIWARE/tutorials.Getting-Started/blob/master/README.ja.md)

### Docker バージョン 18.03 以降を使用していることを確認 

```sh
[ec2-user@bastin ~]$ docker version
Client:
 Version:           20.10.7
 API version:       1.41
 Go version:        go1.15.14
 Git commit:        f0df350
 Built:             Tue Sep 28 19:55:50 2021
 OS/Arch:           linux/amd64
 Context:           default
 Experimental:      true
[ec2-user@bastin ~]$ 
```

### コンテナの起動

```sh
docker pull mongo:4.4
docker pull fiware/orion
docker network create fiware_default
```

MongoDB データベースを実行している Docker コンテナを 起動し、ネットワークに接続する

```sh
docker run -d --name=mongo-db --network=fiware_default --expose=27017 mongo:4.4 --bind_ip_all
```

fiware-orionのネットワーク接続

```sh
docker run -d --name fiware-orion  --network=fiware_default -p 1026:1026  fiware/orion -dbhost mongo-db
```

設定のクリーンアップ（※必要な場合に実施する）

```sh
docker stop fiware-orion
docker rm fiware-orion
docker stop mongo-db
docker rm mongo-db
docker network rm fiware_default
```

### httpリクエストの実施

バージョンの取得

```sh
curl -X GET 'http://localhost:1026/version'
```

```sh
[ec2-user@bastin ~]$ curl -X GET 'http://localhost:1026/version'
{
"orion" : {
  "version" : "3.1.0-next",
  "uptime" : "0 d, 0 h, 1 m, 19 s",
  "git_hash" : "7bd1e43514539bd65caeb30d4e3319202e0f115b",
  "compile_time" : "Mon Jul 26 08:19:44 UTC 2021",
  "compiled_by" : "root",
  "compiled_in" : "dae1c5e3a7d9",
  "release_date" : "Mon Jul 26 08:19:44 UTC 2021",
  "machine" : "x86_64",
  "doc" : "https://fiware-orion.rtfd.io/",
  "libversions": {
     "boost": "1_66",
     "libcurl": "libcurl/7.61.1 OpenSSL/1.1.1g zlib/1.2.11 nghttp2/1.33.0",
     "libmicrohttpd": "0.9.70",
     "openssl": "1.1",
     "rapidjson": "1.1.0",
     "mongoc": "1.17.4",
     "bson": "1.17.4"
  }
}
}
```

#### エンティティの作成

```sh
curl -sS http://localhost:1026/v2/entities \
     -H 'Content-Type: application/json' \
     -d @- <<EOF
{
  "id": "living",
  "type": "Room",
  "temperature": {"value": 23, "type": "Float"}
}
EOF
```

#### エンティティの確認

```sh
[ec2-user@bastin ~]$ curl -sS http://localhost:1026/v2/entities/living?type=Room -H 'Accept: application/json' | jq .
{
  "id": "living",
  "type": "Room",
  "temperature": {
    "type": "Float",
    "value": 23,
    "metadata": {}
  }
}
```

エンティティの更新

```sh
curl -sS http://localhost:1026/v2/entities/living/attrs \
     -H 'Content-Type: application/json' \
     -X PATCH \
     -d @- <<EOF
{
  "temperature": {
    "value": 26.5,
    "type": "Float"
  }
}
EOF
```

エンティティの確認

```sh
[ec2-user@bastin ~]$ curl -sS http://localhost:1026/v2/entities/living?type=Room -H 'Accept: application/json' | jq .
{
  "id": "living",
  "type": "Room",
  "temperature": {
    "type": "Float",
    "value": 26.5,
    "metadata": {}
  }
}
[ec2-user@bastin ~]$ 
```

アトリビュートの更新

```sh
curl -sS http://localhost:1026/v2/entities/living/attrs/temperature/value \
       -H 'Content-Type: text/plain' \
       -X PUT \
       -d 28.5
```

