---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Oracle Databaseに新元号の「令和」を追加する"
subtitle: ""
summary: " "
tags: ["Oracle"]
categories: ["Oracle"]
url: oracle-era-gengou-add.html
date: 2019-04-01
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


新元号が発表されました。平成元年生まれなので平成の終わりがもうすぐ訪れると思うと色々と寂しいです。

## 元号使用の設定確認

### 西暦を使用している場合

```sql
SQL> SHOW PARAMETER nls_calendar

NAME                                 TYPE        VALUE
------------------------------------ ----------- ------------------------------
nls_calendar                         string      GREGORIAN ←★西暦を使用
```

### 和暦を使用している場合

```sql
SQL> SHOW PARAMETER nls_calendar

NAME                                 TYPE        VALUE
------------------------------------ ----------- ------------------------------
nls_calendar                         string      Japanese Imperial ←★和暦を使用
```

## 変更前の環境で元号を表示

下記の通り、「2019年5月1日」の改元時においても当然平成表示のままです。

```sql
show parameter NLS_CALENDAR
ALTER SESSION SET NLS_CALENDAR="Japanese Imperial";

select sysdate+30 from dual;

SQL> show parameter NLS_CALENDAR

NAME                                 TYPE        VALUE
------------------------------------ ----------- ------------------------------
nls_calendar                         string      GREGORIAN
SQL> ALTER SESSION SET NLS_CALENDAR="Japanese Imperial";

セッションが変更されました。

SQL>
SQL> select sysdate+30 from dual;

SYSDATE+30
---------------------------------------------
平成31年05月01日
```

## 元号の設定追加

新元号名のEUCの16進コードを確認します。後続の手順で16進数で使用します。

```sql
SELECT DUMP(CONVERT('令和','JA16EUC'),16) AS "元号" FROM DUAL;

SQL> SELECT DUMP(CONVERT('令和','JA16EUC'),16) AS "元号" FROM DUAL;

元号
------------------------
Typ=1 Len=4: ce,e1,cf,c2
```

```sql
select dump('R',16) as "アルファベット" from dual;

SQL> select dump('R',16) as "アルファベット" from dual;

アルファベット
----------------
Typ=96 Len=1: 52
```

$ORACLE_HOME/nls に lxecal.nlt 設定ファイルを作成します。

```bash
DEFINE calendar
calendar_name = "Japanese Imperial"
DEFINE calendar_era
era_full_name = "cee1cfc2" ★★令和 <====上記で確認した「元号」のEUC の16進コードをここに記述します
era_abbr_name = "52" ★★令和 <=====上記で確認した「アルファベット」の EUC の16進コードをここに記述します
start_date = "MAY-01-2019 AD"
end_date = "DEC-31-2099 AD"
ENDDEFINE calendar_era
ENDDEFINE calendar
```

```sh
[oracle@dbvgg ~]$ cd $ORACLE_HOME/nls
[oracle@dbvgg nls]$
[oracle@dbvgg nls]$ ll
合計 32
drwxr-xr-x 3 oracle oinstall  4096  3月 22 02:09 2019 csscan
drwxr-xr-x 3 oracle oinstall 20480  3月 22 02:09 2019 data
drwxr-xr-x 3 oracle oinstall  4096  3月 22 02:10 2019 lbuilder
drwxr-xr-x 2 oracle oinstall  4096  3月 22 02:09 2019 mesg
[oracle@dbvgg nls]$
[oracle@dbvgg nls]$ vi lxecal.nlt
[oracle@dbvgg nls]$ cat lxecal.nlt
DEFINE calendar
calendar_name = "Japanese Imperial"
DEFINE calendar_era
era_full_name = "cee1cfc2"
era_abbr_name = "52"
start_date = "MAY-01-2019 AD"
end_date = "DEC-31-2099 AD"
ENDDEFINE calendar_era
ENDDEFINE calendar

[oracle@dbvgg nls]$

```

データベースを停止後にlxegen を実行して lxecalji.nlb が作成されていることを確認します

```sh
[oracle@dbvgg nls]$ sqlplus / as sysdba

SQL*Plus: Release 11.2.0.4.0 Production on 月 4月 1 11:58:10 2019

Copyright (c) 1982, 2013, Oracle.  All rights reserved.

Oracle Database 11g Enterprise Edition Release 11.2.0.4.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options
に接続されました。
SQL> shutdown immediate
データベースがクローズされました。
データベースがディスマウントされました。
ORACLEインスタンスがシャットダウンされました。
SQL>
SQL> Oracle Database 11g Enterprise Edition Release 11.2.0.4.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing optionsとの接続が切断されました。
[oracle@dbvgg nls]$
[oracle@dbvgg nls]$ lxegen

NLS Calendar Utility: Version 11.2.0.4.0 - Production

Copyright (c) Oracle 1994, 2004.  All rights reserved.

CORE    11.2.0.4.0      Production

[oracle@dbvgg nls]$
```

## 変更後の環境で元号を表示

再起動後は、「2019年5月1日」が新元号の「令和」表記になりました。

```sql
show parameter NLS_CALENDAR
ALTER SESSION SET NLS_CALENDAR="Japanese Imperial";

select sysdate+30 from dual;

SQL> show parameter NLS_CALENDAR

NAME                                 TYPE        VALUE
------------------------------------ ----------- ------------------------------
nls_calendar                         string      GREGORIAN

SQL> ALTER SESSION SET NLS_CALENDAR="Japanese Imperial";

セッションが変更されました。

SQL>
SQL> select sysdate+30 from dual;

SYSDATE+30
---------------------------------------------
令和01年05月01日
```

## 備考

システム停止が必要のため、運用中のシステムは気軽に変更出来るものではないですね。

そもそも使っているところあるの？

## 参考URL

こちらを全面的に参考にさせて頂きました。

> Oracle 製品における改元の影響について | NTTデータ先端技術株式会社 http://www.intellilink.co.jp/article/column/ora-report20180604.html

> Oracle Databaseの新元号への対応について | アシスト https://www.ashisuto.co.jp/support/gengo/product/oracle-database.html

> https://qiita.com/ora_gonsuke777/items/dc21ee3f2abf718098b9
>
> Oracle Database に 新しい元号(年号)「野球」を追加してみる。(NLSカレンダ・ユーティリティlxegen)
