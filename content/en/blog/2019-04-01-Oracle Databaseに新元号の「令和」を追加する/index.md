---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Adding the New Japanese Era Name 'Reiwa' to Oracle Database"
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


The new era name was announced. Being born in the first year of Heisei, I feel a bit nostalgic thinking that the end of Heisei is approaching.

## Check Era Settings

### When Using the Western Calendar

```sql
SQL> SHOW PARAMETER nls_calendar

NAME                                 TYPE        VALUE
------------------------------------ ----------- ------------------------------
nls_calendar                         string      GREGORIAN <-★Using Western calendar
```

### When Using the Japanese Imperial Calendar

```sql
SQL> SHOW PARAMETER nls_calendar

NAME                                 TYPE        VALUE
------------------------------------ ----------- ------------------------------
nls_calendar                         string      Japanese Imperial <-★Using Japanese calendar
```

## Display Era Before Changes

As shown below, on the day of the era change "May 1, 2019", the Heisei era is still displayed.

```sql
show parameter NLS_CALENDAR
ALTER SESSION SET NLS_CALENDAR="Japanese Imperial";

select sysdate+30 from dual;

SQL> show parameter NLS_CALENDAR

NAME                                 TYPE        VALUE
------------------------------------ ----------- ------------------------------
nls_calendar                         string      GREGORIAN
SQL> ALTER SESSION SET NLS_CALENDAR="Japanese Imperial";

Session altered.

SQL>
SQL> select sysdate+30 from dual;

SYSDATE+30
---------------------------------------------
Heisei 31 year 05 month 01 day
```

## Add Era Settings

Check the EUC hexadecimal code of the new era name. It will be used in hexadecimal form in subsequent steps.

```sql
SELECT DUMP(CONVERT('令和','JA16EUC'),16) AS "Era Name" FROM DUAL;

SQL> SELECT DUMP(CONVERT('令和','JA16EUC'),16) AS "Era Name" FROM DUAL;

Era Name
------------------------
Typ=1 Len=4: ce,e1,cf,c2
```

```sql
select dump('R',16) as "Alphabet" from dual;

SQL> select dump('R',16) as "Alphabet" from dual;

Alphabet
----------------
Typ=96 Len=1: 52
```

Create the lxecal.nlt configuration file in $ORACLE_HOME/nls.

```bash
DEFINE calendar
calendar_name = "Japanese Imperial"
DEFINE calendar_era
era_full_name = "cee1cfc2" ★★Reiwa <====Enter the EUC hexadecimal code of "Era Name" confirmed above
era_abbr_name = "52" ★★Reiwa <=====Enter the EUC hexadecimal code of "Alphabet" confirmed above
start_date = "MAY-01-2019 AD"
end_date = "DEC-31-2099 AD"
ENDDEFINE calendar_era
ENDDEFINE calendar
```

```sh
[oracle@dbvgg ~]$ cd $ORACLE_HOME/nls
[oracle@dbvgg nls]$
[oracle@dbvgg nls]$ ll
Total 32
drwxr-xr-x 3 oracle oinstall  4096  Mar 22 02:09 2019 csscan
drwxr-xr-x 3 oracle oinstall 20480  Mar 22 02:09 2019 data
drwxr-xr-x 3 oracle oinstall  4096  Mar 22 02:10 2019 lbuilder
drwxr-xr-x 2 oracle oinstall  4096  Mar 22 02:09 2019 mesg
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

After stopping the database, run lxegen and confirm that lxecalji.nlb has been created.

```sh
[oracle@dbvgg nls]$ sqlplus / as sysdba

SQL*Plus: Release 11.2.0.4.0 Production on Mon Apr  1 11:58:10 2019

Copyright (c) 1982, 2013, Oracle.  All rights reserved.

Connected to:
Oracle Database 11g Enterprise Edition Release 11.2.0.4.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options
SQL> shutdown immediate
Database closed.
Database dismounted.
ORACLE instance shut down.
SQL>
SQL> Disconnected from Oracle Database 11g Enterprise Edition Release 11.2.0.4.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options
[oracle@dbvgg nls]$
[oracle@dbvgg nls]$ lxegen

NLS Calendar Utility: Version 11.2.0.4.0 - Production

Copyright (c) Oracle 1994, 2004.  All rights reserved.

CORE    11.2.0.4.0      Production

[oracle@dbvgg nls]$
```

## Display Era After Changes

After restarting, "May 1, 2019" is now displayed with the new era name "Reiwa".

```sql
show parameter NLS_CALENDAR
ALTER SESSION SET NLS_CALENDAR="Japanese Imperial";

select sysdate+30 from dual;

SQL> show parameter NLS_CALENDAR

NAME                                 TYPE        VALUE
------------------------------------ ----------- ------------------------------
nls_calendar                         string      GREGORIAN

SQL> ALTER SESSION SET NLS_CALENDAR="Japanese Imperial";

Session altered.

SQL>
SQL> select sysdate+30 from dual;

SYSDATE+30
---------------------------------------------
Reiwa 01 year 05 month 01 day
```

## Notes

Since a system shutdown is required, it is not something that can easily be changed on a running production system.

Does anyone even use this feature?

## Reference URLs

I fully referenced the following:

> Impact of the Era Change on Oracle Products | NTT DATA INTELLILINK http://www.intellilink.co.jp/article/column/ora-report20180604.html

> Oracle Database Response to the New Era | Ashisuto https://www.ashisuto.co.jp/support/gengo/product/oracle-database.html

> https://qiita.com/ora_gonsuke777/items/dc21ee3f2abf718098b9
>
> Adding a New Japanese Era Name (Kanji) to Oracle Database (NLS Calendar Utility lxegen)
