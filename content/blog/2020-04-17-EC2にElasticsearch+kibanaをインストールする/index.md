---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "EC2にElasticsearch + kibanaをインストールする"
subtitle: ""
summary: " "
tags: ["AWS"]
categories: ["AWS"]
url: aws-ec2-elasticsearch-install.html
date: 2020-04-17
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

EC2にElasticsearchをインストールして満足するだけのメモ。

### javaのインストール

```sh
sudo -s
sudo yum install java-1.8.0-openjdk.x86_64
java -version
```

### Elasicsearchのインストール

##### yum でインストールするためにリポジトリの設定

```sh
cat > /etc/yum.repos.d/elasticsearch.repo <<EOF
[elasticsearch-7.x]
name=Elasticsearch repository for 7.x packages
baseurl=https://artifacts.elastic.co/packages/7.x/yum
gpgcheck=1
gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
enabled=1
autorefresh=1
type=rpm-md
EOF
```

##### Elasitcserchのインストール

```
yum -y install elasticsearch
```

##### Elasticsearchの起動

```
systemctl start elasticsearch
systemctl status elasticsearch
```

##### 永続設定

```
systemctl enable elasticsearch
```

##### インストール確認

Elasicsearchの7.6.1がインストールされています。

```
[root@elastic ec2-user]# curl http://127.0.0.1:9200
{
  "name" : "elastic",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "YWsoyak7S9SOTOXJp92_QQ",
  "version" : {
    "number" : "7.6.1",
    "build_flavor" : "default",
    "build_type" : "rpm",
    "build_hash" : "aa751e09be0a5072e8570670309b1f12348f023b",
    "build_date" : "2020-02-29T00:15:25.529771Z",
    "build_snapshot" : false,
    "lucene_version" : "8.4.0",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}
```

##### kuromojiのインストール

```
[root@elastic ec2-user]# /usr/share/elasticsearch/bin/elasticsearch-plugin install analysis-kuromoji
-> Installing analysis-kuromoji
-> Downloading analysis-kuromoji from elastic
[=================================================] 100%   
-> Installed analysis-kuromoji
[root@elastic ec2-user]# /usr/share/elasticsearch/bin/elasticsearch-plugin list
analysis-kuromoji
[root@elastic ec2-user]# 
```

### kibanaのインストール

```
yum -y install kibana
```

##### 設定変更

`server.host`を`0.0.0.0`に変更

```
vi /etc/kibana/kibana.yml
```

##### kibana起動

```
systemctl start kibana
systemctl status kibana
```

起動しました。

```
[root@elastic ec2-user]# systemctl status kibana
● kibana.service - Kibana
   Loaded: loaded (/etc/systemd/system/kibana.service; disabled; vendor preset: disabled)
   Active: active (running) since Sun 2020-03-22 11:33:46 UTC; 40s ago
 Main PID: 3471 (node)
   CGroup: /system.slice/kibana.service
           └─3471 /usr/share/kibana/bin/../node/bin/node /usr/share/kibana/bin/../src/cli -c /etc/kibana/kibana.yml

Mar 22 11:34:15 elastic kibana[3471]: {"type":"log","@timestamp":"2020-03-22T11:34:15Z","tags":["status","plugin:ui_metric@7.6.1","info"],"pid":3471,"state":"green","message...nitialized"}
Mar 22 11:34:15 elastic kibana[3471]: {"type":"log","@timestamp":"2020-03-22T11:34:15Z","tags":["status","plugin:markdown_vis@7.6.1","info"],"pid":3471,"state":"green","mess...nitialized"}
Mar 22 11:34:15 elastic kibana[3471]: {"type":"log","@timestamp":"2020-03-22T11:34:15Z","tags":["status","plugin:metric_vis@7.6.1","info"],"pid":3471,"state":"green","messag...nitialized"}
Mar 22 11:34:15 elastic kibana[3471]: {"type":"log","@timestamp":"2020-03-22T11:34:15Z","tags":["status","plugin:table_vis@7.6.1","info"],"pid":3471,"state":"green","message...nitialized"}
Mar 22 11:34:15 elastic kibana[3471]: {"type":"log","@timestamp":"2020-03-22T11:34:15Z","tags":["status","plugin:tagcloud@7.6.1","info"],"pid":3471,"state":"green","message"...nitialized"}
Mar 22 11:34:15 elastic kibana[3471]: {"type":"log","@timestamp":"2020-03-22T11:34:15Z","tags":["status","plugin:vega@7.6.1","info"],"pid":3471,"state":"green","message":"St...nitialized"}
Mar 22 11:34:17 elastic kibana[3471]: {"type":"log","@timestamp":"2020-03-22T11:34:17Z","tags":["reporting","warning"],"pid":3471,"message":"Generating a random key for xpac...kibana.yml"}
Mar 22 11:34:17 elastic kibana[3471]: {"type":"log","@timestamp":"2020-03-22T11:34:17Z","tags":["status","plugin:reporting@7.6.1","info"],"pid":3471,"state":"green","message...nitialized"}
Mar 22 11:34:17 elastic kibana[3471]: {"type":"log","@timestamp":"2020-03-22T11:34:17Z","tags":["listening","info"],"pid":3471,"message":"Server running at http://0.0.0.0:5601"}
Mar 22 11:34:18 elastic kibana[3471]: {"type":"log","@timestamp":"2020-03-22T11:34:18Z","tags":["info","http","server","Kibana"],"pid":3471,"message":"http server running at...0.0.0:5601"}
Hint: Some lines were ellipsized, use -l to show in full.
```

##### kibanaの起動永続設定

Elasticsearchと同様に再起動後に自動でkibanaが起動されるように設定を行います。

```
systemctl enable kibana
```

以上！