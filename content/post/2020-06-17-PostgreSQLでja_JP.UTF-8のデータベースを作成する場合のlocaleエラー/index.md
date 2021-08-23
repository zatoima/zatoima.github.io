---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "PostgreSQLでja_JP.UTF-8のデータベース作成時のlocaleエラー"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgresql-create-database-locale-error.html
date: 2020-06-17
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



PostgreSQL上で`ja_JP.UTF-8` を指定してデータベースを指定した場合にエラー発生

```sh
postgres=# CREATE DATABASE locale_jp_utf8
postgres-#   TEMPLATE template0 ENCODING 'UTF-8'
postgres-#   LC_COLLATE 'ja_JP.UTF-8' LC_CTYPE 'ja_JP.UTF-8';
ERROR:  invalid locale name: "ja_JP.UTF-8"
```

OS上のlocaleを確認してみたら`ja_JP.UTF-8`がない。

```sh
[postgres@pgsql ~]$ locale -a
C
C.utf8
en_AG
en_AU
en_AU.utf8
en_BW
en_BW.utf8
en_CA
en_CA.utf8
en_DK
en_DK.utf8
en_GB
en_GB.iso885915
en_GB.utf8
en_HK
en_HK.utf8
en_IE
en_IE@euro
en_IE.utf8
en_IL
en_IN
en_NG
en_NZ
en_NZ.utf8
en_PH
en_PH.utf8
en_SC.utf8
en_SG
en_SG.utf8
en_US
en_US.iso885915
en_US.utf8
en_ZA
en_ZA.utf8
en_ZM
en_ZW
en_ZW.utf8
POSIX
```

ja_JP.UTF-8をセットアップしようとすると`character map file`が見つからないというエラーが発生。

```sh
[postgres@pgsql ~]$ sudo localedef -i ja_JP -c -f UTF-8 -A /usr/share/locale/locale.alias ja_JP.UTF-8
[error] character map file `UTF-8' not found: No such file or directory
[error] default character map file `ANSI_X3.4-1968' not found: No such file or directory
[postgres@pgsql ~]$ 
```

`glibc-locale-source`と`glibc-langpack-en` をインストール後に再実行

```sh
[postgres@pgsql ~]$ sudo yum -y install glibc-locale-source glibc-langpack-en
[postgres@pgsql ~]$ sudo localedef -i ja_JP -c -f UTF-8 -A /usr/share/locale/locale.alias ja_JP.UTF-8
[error] character map file `UTF-8' not found: No such file or directory
[error] default character map file `ANSI_X3.4-1968' not found: No such file or directory
```

`locale -a`で確認

```sh
[postgres@pgsql ~]$ locale -a
C
C.utf8
en_AG
en_AU
en_AU.utf8
en_BW
en_BW.utf8
en_CA
en_CA.utf8
en_DK
en_DK.utf8
en_GB
en_GB.iso885915
en_GB.utf8
en_HK
en_HK.utf8
en_IE
en_IE@euro
en_IE.utf8
en_IL
en_IN
en_NG
en_NZ
en_NZ.utf8
en_PH
en_PH.utf8
en_SC.utf8
en_SG
en_SG.utf8
en_US
en_US.iso885915
en_US.utf8
en_ZA
en_ZA.utf8
en_ZM
en_ZW
en_ZW.utf8
ja_JP.utf8
POSIX
```

この状態であればPostgreSQL上でのデータベース作成が成功する。※PostgreSQLの再起動必要

```sql
postgres=# CREATE DATABASE locale_us_utf8
postgres-#   TEMPLATE template0 ENCODING 'UTF-8'
postgres-#   LC_COLLATE 'en_US.UTF-8' LC_CTYPE 'en_US.UTF-8';
CREATE DATABASE
postgres=# 
```

