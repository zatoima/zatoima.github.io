---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "How to Check Session Information for GoldenGate-Related Processes"
subtitle: ""
summary: " "
tags: ["GoldenGate","Oracle"]
categories: ["GoldenGate","Oracle"]
url: goldengate-check-session-info.html
date: 2019-02-16
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



### **Filter Target Processes by Module**

In the case of Integrated Capture/Replicat, since GoldenGate processes are also DB processes, you can filter and output them using the module column.

```sql
SELECT
    s.inst_id,
    s.con_id,
    s.logon_time,
    s.sid,
    s.serial#,
    s.module,
    p.spid,
    p.pid,
    s.action,
    s.process,
    s.program,
    s.status,
    s.action,
    DECODE(s.server,'DEDICATED','DED','SHR') SVR,
    s.STATE,
    s.event
FROM
    gv$session s,
    v$process p
WHERE
    (s.module = 'GoldenGate' OR
        s.module LIKE '%tream%' OR
        s.module LIKE 'OGG%') AND
    p.addr=s.paddr
ORDER BY
    s.con_id,
    s.inst_id,
    s.module,
    s.action;
```

### **Sample Output**

Since this was run on the target side, only Integrated Replicat processes are shown.
The ACTION column allows you to distinguish "Coordinator", "Receiver", "Reader", and "Apply Server".

| INST_ID | CON_ID | LOGON_TIME | SID  | SERIAL# | MODULE     | SPID  | PID  | ACTION                      | PROCESS | PROGRAM                                      | STATUS   | ACTION                      | SVR  | STATE   | EVENT                                                    |
| ------- | ------ | ---------- | ---- | ------- | ---------- | ----- | ---- | --------------------------- | ------- | -------------------------------------------- | -------- | --------------------------- | ---- | ------- | -------------------------------------------------------- |
| 1       | 0      | 2019/3/3   | 339  | 34151   | Streams    | 28703 | 59   | AQ LB Coordinator           | 28703   | oracle@xxxxxxx1t.jp.oracle.com (QM03)        | ACTIVE   | AQ LB Coordinator           | DED  | WAITING | Streams AQ: load balancer idle                           |
| 1       | 0      | 2019/3/3   | 23   | 462     | Streams    | 27781 | 57   | QMON Coordinator            | 27781   | oracle@xxxxxxx1t.jp.oracle.com (QM02)        | ACTIVE   | QMON Coordinator            | DED  | WAITING | Streams AQ: qmn coordinator idle wait                    |
| 1       | 0      | 2019/3/3   | 25   | 58083   | Streams    | 27787 | 60   | QMON Slave                  | 27787   | oracle@xxxxxxx1t.jp.oracle.com (Q003)        | ACTIVE   | QMON Slave                  | DED  | WAITING | Streams AQ: waiting for time management or cleanup tasks |
| 1       | 0      | 2019/3/3   | 177  | 6407    | Streams    | 27789 | 61   | QMON Slave                  | 27789   | oracle@xxxxxxx1t.jp.oracle.com (Q004)        | ACTIVE   | QMON Slave                  | DED  | WAITING | Streams AQ: qmn slave idle wait                          |
| 1       | 0      | 2019/3/3   | 182  | 19018   | Streams    | 27829 | 67   | QMON Slave                  | 27829   | oracle@xxxxxxx1t.jp.oracle.com (Q006)        | ACTIVE   | QMON Slave                  | DED  | WAITING | Streams AQ: qmn slave idle wait                          |
| 1       | 3      | 2019/3/3   | 33   | 20930   | GoldenGate | 28053 | 75   | OGG$R11 - Apply Coordinator | 28053   | oracle@xxxxxxx1t.jp.oracle.com (AP01)        | ACTIVE   | OGG$R11 - Apply Coordinator | DED  | WAITING | rdbms ipc message                                        |
| 1       | 3      | 2019/3/3   | 176  | 19252   | GoldenGate | 28055 | 76   | OGG$R11 - Apply Reader      | 28055   | oracle@xxxxxxx1t.jp.oracle.com (AS01)        | ACTIVE   | OGG$R11 - Apply Reader      | DED  | WAITING | REPL Capture/Apply: messages                             |
| 1       | 3      | 2019/3/3   | 350  | 51690   | GoldenGate | 28051 | 74   | OGG$R11 - Apply Receiver    | 28047   | replicat@xxxxxxx1t.jp.oracle.com (TNS V1-V3) | INACTIVE | OGG$R11 - Apply Receiver    | DED  | WAITING | SQL*Net message from client                              |
| 1       | 3      | 2019/3/3   | 349  | 48410   | GoldenGate | 28057 | 77   | OGG$R11 - Apply Server      | 28057   | oracle@xxxxxxx1t.jp.oracle.com (AS02)        | ACTIVE   | OGG$R11 - Apply Server      | DED  | WAITING | rdbms ipc message                                        |
| 1       | 3      | 2019/3/3   | 35   | 16249   | GoldenGate | 28059 | 78   | OGG$R11 - Apply Server      | 28059   | oracle@xxxxxxx1t.jp.oracle.com (AS03)        | ACTIVE   | OGG$R11 - Apply Server      | DED  | WAITING | rdbms ipc message                                        |
| 1       | 3      | 2019/3/3   | 184  | 29507   | GoldenGate | 28061 | 79   | OGG$R11 - Apply Server      | 28061   | oracle@xxxxxxx1t.jp.oracle.com (AS04)        | ACTIVE   | OGG$R11 - Apply Server      | DED  | WAITING | rdbms ipc message                                        |
| 1       | 3      | 2019/3/3   | 352  | 60489   | GoldenGate | 28063 | 80   | OGG$R11 - Apply Server      | 28063   | oracle@xxxxxxx1t.jp.oracle.com (AS05)        | ACTIVE   | OGG$R11 - Apply Server      | DED  | WAITING | rdbms ipc message                                        |

```sh

```
