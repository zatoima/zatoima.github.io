---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "metabase起動時のInitialization FAILEDエラー対応"
subtitle: ""
summary: " "
tags: ["metabase"]
categories: ["metabase"]
url: docker-metabase-initialization-failed-error
date: 2022-09-19
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

### エラーメッセージ

```sql
2022-09-17 15:51:59,306 INFO driver.impl :: Registered driver :presto-jdbc (parents: [:presto-common]) 🚚
2022-09-17 15:51:59,309 DEBUG plugins.lazy-loaded-driver :: Registering lazy loading driver :presto...
2022-09-17 15:51:59,317 INFO driver.impl :: Registered driver :presto (parents: [:presto-common]) 🚚
2022-09-17 15:51:59,320 INFO metabase.core :: Setting up and migrating Metabase DB. Please sit tight, this may take a minute...
2022-09-17 15:51:59,323 INFO db.setup :: Verifying h2 Database Connection ...
2022-09-17 15:51:59,891 INFO db.setup :: Successfully verified H2 1.4.197 (2018-03-18) application database connection. ✅
2022-09-17 15:51:59,893 INFO db.setup :: Running Database Migrations...
2022-09-17 15:51:59,894 INFO db.setup :: Setting up Liquibase...
2022-09-17 15:52:00,474 ERROR metabase.core :: Metabase Initialization FAILED
org.h2.jdbc.JdbcBatchUpdateException: The database is read only; SQL statement:
UPDATE DATABASECHANGELOG SET FILENAME = ? [90097-197]
	at org.h2.jdbc.JdbcPreparedStatement.executeBatch(JdbcPreparedStatement.java:1295)
	at com.mchange.v2.c3p0.impl.NewProxyPreparedStatement.executeBatch(NewProxyPreparedStatement.java:2544)
```

H2データベースではなく、ローカルに構築しているPostgreSQLを使用するように環境変数を設定する。

> [Migrating to a production application database](https://www.metabase.com/docs/latest/installation-and-operation/migrating-from-h2)

```sql
export MB_DB_TYPE=postgres
export MB_DB_CONNECTION_URI="jdbc:postgresql://localhost:5432/metabase?user=postgres&password=postgres"
java -jar metabase.jar
```

正常に起動した。

```
2022-09-17 15:54:30,330 INFO metabase.core :: Metabase Initialization COMPLETE
```

> https://discourse.metabase.com/t/error-the-database-is-read-only-unable-to-connect-me-12780/10651/3
>
> https://www.metabase.com/docs/latest/installation-and-operation/migrating-from-h2
