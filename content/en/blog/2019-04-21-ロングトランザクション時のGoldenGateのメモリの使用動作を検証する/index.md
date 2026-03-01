---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Verifying GoldenGate Memory Usage During Long Transactions"
subtitle: ""
summary: " "
tags: ["GoldenGate"]
categories: ["GoldenGate"]
url: goldengate-longtransaction-memoryuse.html
date: 2019-04-21
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



#### **Introduction**

In a previous article, I summarized how GoldenGate uses memory:

> Understanding Virtual Memory Usage in Oracle GoldenGate - zato logger https://www.zatolog.com/entry/goldengate-vmemory-use

I wanted to actually run a long transaction and visualize how memory is used.

#### **Prerequisites**

#### **About CACHESIZE**

The CACHESIZE configured for the Capture process on the source side is set to "1GB".

#### **Data Collection Targets**

A simple script is set up to collect the following information every minute.

The information collected is as follows:

| Source/Command                                | Information Collected          |
| --------------------------------------------- | ------------------------------ |
| v$sysstat                                     | REDO generation volume         |
| SEND EXTRACT <Capture Name>, CACHEMGR CACHESTATS | Cache manager statistics    |
| info exttrail ./dirdat/c11/lt                 | Trail file information         |

#### **Data Collection Script**

This was only used once so it's rough.

```sh
#!/bin/bash

. "/home/oracle/.oraenv_db112s"

while :
do
    date
    sqlplus / as sysdba << EOF
        set pages 2000 lin 2000
        col name for a20
        select * from v\$sysstat where name = 'redo size';
    exit

    EOF

    /gg/gg1/ggsci << EOF
    info exttrail ./dirdat/c11/lt
    SEND EXTRACT c11, CACHEMGR CACHESTATS
    exit
    EOF

    ls -lth /gg/gg1/BR/C11/stale
    ls -lth /gg/gg1/dirtmp

    sleep 60
done
```

#### **Transaction to Run on the Source Side**

Without committing once, we perform "20,000,000 (20 million)" inserts continuously. Since this is a low-spec environment, there is a possibility of running out of UNDO tablespace, archive log space, or data file space, but let's try.

```sql
create table memtest(a number primary key,b varchar2(30));

declare
v_c1 number;
v_c2 varchar2(30);
begin
dbms_random.seed(uid);
for i in 1..20000000
loop
v_c1 := i;
v_c2 := dbms_random.string('x', 16);
insert into reptest (a, b) values (v_c1, v_c2);
end loop;
commit;
end;
/
```



#### **Execution Results**

A graph was created showing `REDO generation volume`, `vm current (MB)`, and `bytes to disk (MB)`.

<img src="images/image-20191121164246512.png" alt="image-20191121164246512" style="zoom:50%;" />

1. "vm current" remained at the upper limit of CACHESIZE (1GB).

   In the previously summarized documentation, I noted that the `CACHESIZE` upper limit is a soft limit, and some transactions may use up to `CACHESIZEMAX`. In this case, since the transaction pattern was consistent, it did not use virtual memory beyond this soft limit.

2. Approximately 70-80% of REDO generation was swapped to the dirtmp directory on disk.

   Updates continued for about 30 minutes, and `REDO generation volume (MB)` increased steadily. Correspondingly, `bytes to disk (MB)` also increased in tandem.

   In this case, it was a long transaction generating about 10GB of REDO, but in real business environments, large batch updates may occur, and significant REDO generation can be expected. I think it is necessary to reconsider how much swap directory space should be allocated.

3. "vm current" decreased to 0 after the update completed.

   After the long transaction completed and a commit was issued, the `vm current (MB)` value dropped to 0. This shows that the reserved virtual memory was released. If you want to know the maximum virtual memory used in the past, you can check "vm used max".
