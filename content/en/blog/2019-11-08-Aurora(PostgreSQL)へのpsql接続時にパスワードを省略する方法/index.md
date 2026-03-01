---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "How to Omit the Password When Connecting to Aurora (PostgreSQL) via psql"
subtitle: ""
summary: " "
tags: ["AWS", "Aurora", "PostgreSQL"]
categories: ["AWS", "Aurora", "PostgreSQL"]
url: aws-aurora-postgres-password.html
date: 2019-11-08
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


This is about PostgreSQL, not specifically Aurora (PostgreSQL).

### **Method 1: Write the password in '.pgpass'**

***

Create a '.pgpass' file in the home directory and write the password there.

##### .pgpass Format

```
hostname:port:database:user:password
Example) 192.168.1.**:5432:dbname:dbuser:password
```

##### Creating .pgpass

```sh
vi $HOME/.pgpass
aurorapostdb.xxxxxxxxxx.ap-northeast-1.rds.amazonaws.com:5432:aurorapostdb:master:postgres

chmod 600 $HOME/.pgpass

[ec2-user@donald-dev-ec2-bastin ~]$ psql -h aurorapostdb.xxxxxxx.ap-northeast-1.rds.amazonaws.com -U master -d aurorapostdb
psql (10.4, server 10.7)
SSL connection (protocol: TLSv1.2, cipher: ECDHE-RSA-AES256-GCM-SHA384, bits: 256, compression: off)
Type "help" for help.

aurorapostdb=>
```

If you don't change the permissions, a WARNING will appear.

> WARNING: password file "/home/ec2-user/.pgpass" has group or world access; permissions should be u=rw (0600) or less

### Method 2: Write in environment variable

***

```sh
export PGPASSWORD=postgres
psql -h aurorapostdb.xxxxxxxxxx.ap-northeast-1.rds.amazonaws.com -U master -d aurorapostdb

[ec2-user@donald-dev-ec2-bastin ~]$ export PGPASSWORD=xxxxxxxx
[ec2-user@donald-dev-ec2-bastin ~]$ psql -h aurorapostdb.xxxxxxx.ap-northeast-1.rds.amazonaws.com -U master -d aurorapostdb
psql (10.4, server 10.7)
SSL connection (protocol: TLSv1.2, cipher: ECDHE-RSA-AES256-GCM-SHA384, bits: 256, compression: off)
Type "help" for help.

aurorapostdb=>
```

### References

***

> 33.14. Environment Variables https://www.postgresql.jp/document/10/html/libpq-envars.html

> 33.15. Password File https://www.postgresql.jp/document/10/html/libpq-pgpass.html
