---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "PostgreSQL上のバッファキャッシュをクリアする方法"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgresql-buffercache-clear.html
date: 2020-04-24
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



PostgreSQLにはOracleのようにバッファキャッシュをクリアにする方法は用意されていないので、OS上のファイルシステムをクリアにするしかない。なので件名のPostgreSQL上のバッファキャッシュをクリアにするという表現は正しくなく、OS上のキャッシュをクリアにする方法となる。

```sql
pg_ctl stop
sudo su - -c "echo 3 > /proc/sys/vm/drop_caches"
pg_ctl start
```

### 参考：

[pgsql-jp: 40643] Re: PostgreSQLキャッシュクリア方法についてご質問 https://ml.postgresql.jp/pipermail/pgsql-jp/2010-December/015599.html