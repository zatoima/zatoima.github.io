---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Amazon LinuxにMongoDB(5.x系)をインストールする"
subtitle: ""
summary: " "
tags: ["AWS","MongoDB"]
categories: ["AWS","MongoDB"]
url: aws-mongodb-install
date: 2021-12-30
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, Bott
---

### Linuxのディストリビューションの確認

```sh
grep ^NAME  /etc/*release
```

```sh
[ec2-user@bastin ~]$ grep ^NAME  /etc/*release
/etc/os-release:NAME="Amazon Linux"
```

### インストール準備

`mongodb-org-5.0.repo`を作成

```sh
sudo vi /etc/yum.repos.d/mongodb-org-5.0.repo
```

```sh
[mongodb-org-5.0]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/amazon/2/mongodb-org/5.0/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-5.0.asc
```

### yumでインストール

最新のmongodbがインストールされる

```sh
sudo yum install -y mongodb-org
```

```sh
mongo -version
```

### MongoDBの起動

```sh
sudo systemctl start mongod
```

### MongoDBの起動確認

```sh
sudo systemctl status mongod
```

### MongoDBの再起動

```sh
sudo systemctl restart mongod
```

### OS起動と同時にプロセスを起動したい場合

```sh
sudo systemctl enable mongod
```

### バージョン確認

```sh
[ec2-user@bastin ~]$ mongo
MongoDB shell version v3.6.23
connecting to: mongodb://127.0.0.1:27017/?gssapiServiceName=mongodb
Implicit session: session { "id" : UUID("c2030c87-8f92-4fdd-8b93-6265be9fdc28") }
MongoDB server version: 5.0.5
WARNING: shell and server versions do not match
Server has startup warnings: 
{"t":{"$date":"2021-12-30T21:38:38.651+09:00"},"s":"W",  "c":"CONTROL",  "id":22120,   "ctx":"initandlisten","msg":"Access control is not enabled for the database. Read and write access to data and configuration is unrestricted","tags":["startupWarnings"]}
> db.version()
5.0.5
```

### データ挿入と確認

```sh
> db.stats()
{
	"db" : "test",
	"collections" : 0,
	"views" : 0,
	"objects" : 0,
	"avgObjSize" : 0,
	"dataSize" : 0,
	"storageSize" : 0,
	"totalSize" : 0,
	"indexes" : 0,
	"indexSize" : 0,
	"scaleFactor" : 1,
	"fileSize" : 0,
	"fsUsedSize" : 0,
	"fsTotalSize" : 0,
	"ok" : 1
}
> 
> db.user.insert({name:'mr.a', age:10, gender:'m', hobbies:['programming']});
WriteResult({ "nInserted" : 1 })
> db.user.insert({name:'mr.b', age:20, gender:'m', hobbies:['vi']});
WriteResult({ "nInserted" : 1 })
> db.user.insert({name:'ms.c', age:30, gender:'f', hobbies:['programming', 'vi']});
WriteResult({ "nInserted" : 1 })
> db.user.insert({name:'ms.d', age:40, gender:'f', hobbies:['cooking']});
WriteResult({ "nInserted" : 1 })
> 
> db.user.find()
{ "_id" : ObjectId("61cda8e0f9bdc7753af20459"), "name" : "mr.a", "age" : 10, "gender" : "m", "hobbies" : [ "programming" ] }
{ "_id" : ObjectId("61cda8e0f9bdc7753af2045a"), "name" : "mr.b", "age" : 20, "gender" : "m", "hobbies" : [ "vi" ] }
{ "_id" : ObjectId("61cda8e0f9bdc7753af2045b"), "name" : "ms.c", "age" : 30, "gender" : "f", "hobbies" : [ "programming", "vi" ] }
{ "_id" : ObjectId("61cda8e0f9bdc7753af2045c"), "name" : "ms.d", "age" : 40, "gender" : "f", "hobbies" : [ "cooking" ] }
> db.stats()
{
	"db" : "test",
	"collections" : 1,
	"views" : 0,
	"objects" : 4,
	"avgObjSize" : 96.25,
	"dataSize" : 385,
	"storageSize" : 20480,
	"freeStorageSize" : 0,
	"indexes" : 1,
	"indexSize" : 20480,
	"indexFreeStorageSize" : 0,
	"totalSize" : 40960,
	"totalFreeStorageSize" : 0,
	"scaleFactor" : 1,
	"fsUsedSize" : 206759358464,
	"fsTotalSize" : 214735761408,
	"ok" : 1
}
```

### 参考

> Install MongoDB Community Edition on Amazon Linux — MongoDB Manual https://docs.mongodb.com/manual/tutorial/install-mongodb-on-amazon/
