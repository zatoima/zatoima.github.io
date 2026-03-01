---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Installing Elasticsearch + Kibana on EC2"
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

A note just for the satisfaction of installing Elasticsearch on EC2.

### Install Java

```sh
sudo -s
sudo yum install java-1.8.0-openjdk.x86_64
java -version
```

### Install Elasticsearch

##### Configure Repository for yum Installation

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

##### Install Elasticsearch

```
yum -y install elasticsearch
```

##### Start Elasticsearch

```
systemctl start elasticsearch
systemctl status elasticsearch
```

##### Persist on Boot

```
systemctl enable elasticsearch
```

##### Verify Installation

Elasticsearch 7.6.1 is installed.

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

##### Install kuromoji

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

### Install Kibana

```
yum -y install kibana
```

##### Change Configuration

Change `server.host` to `0.0.0.0`.

```
vi /etc/kibana/kibana.yml
```

##### Start Kibana

```
systemctl start kibana
systemctl status kibana
```

It started successfully.

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

##### Persist Kibana on Boot

Configure Kibana to start automatically after reboot, just like Elasticsearch.

```
systemctl enable kibana
```

Done!
