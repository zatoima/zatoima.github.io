---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Inserting Binary Data Files into BLOB Using Oracle PL/SQL"
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

#### Create Directory

```sh
mkdir -p /home/oracle/lobdir
```

#### Create Test File

Not exactly binary data, but create an appropriate file.

```sh
dd if=/dev/zero of=/home/oracle/oradir/10M.dummy bs=1M count=10
```

#### Create Directory Object

```sql
drop directory oradir;
CREATE DIRECTORY ORADIR AS '/home/oracle/oradir';
```

#### Create Sequence (for Primary Key)

Create a sequence to use as the primary key.

```sql
drop sequence oraseq1;
create sequence oraseq1 start with 1 increment by 1 cache 20;
```

#### Create Table

The table consists of: id (primary key), name (stores file name), lobsize (stores BLOB size), and blobdata (stores the BLOB data).

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

#### Create Procedure

Store the BLOB size in a column so that the size of each file can be identified.

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

#### Procedure Test

```sql
EXEC LOAD_BLOB_TBL('10M.dummy');
```

#### Verify Results

```sql
set pages 2000 lin 2000
col name for a20
col lobsize for a20
select * from blob_tbl;
```

#### Reference

> Loading a File into a Table as BLOB - A SIer's Melancholy https://incarose86.hatenadiary.org/entry/20140720/1405875714
