---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Oracle PL/SQLでバイナリデータ・ファイルをBLOBに挿入する"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: oracle-plsql-blob-insert.html
date: 2020-06-13
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

#### ディレクトリ作成

```sh
mkdir -p /home/oracle/lobdir
```

#### テスト用のファイル作成

バイナリデータというわけではないが、適当なファイルを作成する。

```sh
dd if=/dev/zero of=/home/oracle/oradir/10M.dummy bs=1M count=10
```

#### ディレクトリオブジェクトの作成

```sql
drop directory oradir;
CREATE DIRECTORY ORADIR AS '/home/oracle/oradir';
```

#### シーケンス作成(Primary key用)

primary keyとして使用するため、シーケンスを作成。

```sql
drop sequence oraseq1;
create sequence oraseq1 start with 1 increment by 1 cache 20;
```

#### テーブル作成

primary keyであるid、ファイル名を挿入するname、BLOBのサイズを格納するlobsize、blobデータを格納するblobdataで構成。

```sql
drop table BLOB_TBL;
CREATE TABLE BLOB_TBL (
    id number,
    name VARCHAR2(100),
    lobsize VARCHAR2(100),
    blobdata BLOB,
    CONSTRAINT BLOB_TBL_PK PRIMARY KEY (id)
)
LOB (blobdata) STORE AS BASICFILE;
```

#### プロシージャ作成

BLOBのサイズをカラムに挿入することで各ファイルのサイズがわかるようにした。

```sql
drop PROCEDURE LOAD_BLOB_TBL;
CREATE PROCEDURE LOAD_BLOB_TBL(filename VARCHAR2) AS
    bfileloc BFILE;
    blobloc BLOB;
BEGIN
    bfileloc := BFILENAME('ORADIR', filename);

    INSERT INTO BLOB_TBL VALUES(oraseq1.nextval,filename, DBMS_LOB.GETLENGTH(bfileloc), EMPTY_BLOB())
        RETURN blobdata INTO blobloc;

    DBMS_LOB.FILEOPEN(bfileloc, DBMS_LOB.FILE_READONLY);
    DBMS_LOB.LOADFROMFILE(blobloc, bfileloc, DBMS_LOB.GETLENGTH(bfileloc));
    DBMS_LOB.FILECLOSE(bfileloc);
    COMMIT;

    dbms_output.put_line ( 'Blob Size : ' || DBMS_LOB.GETLENGTH(bfileloc) || ' Bytes' );
END;
/
```

#### プロシージャテスト

```sql
EXEC LOAD_BLOB_TBL('10M.dummy');
```

#### 結果確認

```sql
set pages 2000 lin 2000
col name for a20
col lobsize for a20
select * from blob_tbl;
```

#### 参考

> ファイルをBLOBとしてテーブルに読み込む - とあるSIerの憂鬱 https://incarose86.hatenadiary.org/entry/20140720/1405875714