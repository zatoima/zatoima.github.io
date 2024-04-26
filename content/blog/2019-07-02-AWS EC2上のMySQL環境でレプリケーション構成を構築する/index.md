---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "AWS EC2上のMySQL環境でレプリケーション構成を構築する"
subtitle: ""
summary: " "
tags: ["MySQL","AWS", "EC2"]
categories: ["MySQL","AWS", "EC2"]
url: mysql-aws-ec2-replication.html
date: 2019-07-02
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



### はじめに

MySQLのレプリケーション環境をAWSのEC2を使って構築します。マスター側、及びスレーブ側どちらもEC2上に作成したMySQLになります。

### 前提事項

・MySQLのマスター側、スレーブ側は構築済

・データの中身は既にマスター側、スレーブ側にて同一

### EC2のセキュリティリストの編集

マスターとスレーブで通信をするのでインバウントを編集する必要があります。ここではプライベートIPを限定して許可しています。

![image-20191121172723567](images/image-20191121172723567.png)

### スレーブ側のauto.cnfの削除

```sql
cd /var/lib/mysql
rm -rf auto.cnf
systemctl restart mysqld

【実行結果】
[root@awsstg-db002 mysql]# pwd
/var/lib/mysql
[root@awsstg-db002 mysql]# ls -l auto.cnf
-rw-r----- 1 mysql mysql 56 Jun 24 13:25 auto.cnf
[root@awsstg-db002 mysql]#
[root@awsstg-db002 mysql]# rm -rf auto.cnf
[root@awsstg-db002 mysql]#
[root@awsstg-db002 mysql]# systemctl restart mysqld
```

### マスター側のmy.cnfの編集

下記項目をmy.cnfに追加

```sql
#バイナリログの有効化
log-bin
#サーバIDの設定
server_id=1
# GTID有効
gtid_mode=on
# GTID利用時に必須となる設定（GTIDの一貫性を担保できないSQLの実行を禁止）
enforce_gtid_consistency=on
```

### スレーブ側のmy.cnfの編集

下記項目をmy.cnfに追加

```sql
#バイナリログの有効化 ※スレーブ側として可動する場合は必須ではない
log-bin
#サーバIDの設定
server_id=2
# GTID有効
gtid_mode=on
# GTID利用時に必須となる設定（GTIDの一貫性を担保できないSQLの実行を禁止）
enforce_gtid_consistency=on
```

### マスター側にてレプリケーションスレーブ用のユーザを作成

```sql
grant replication slave on *.* to 'repl'@'10.0.0.11' identified by 'mysql';
select Host, User from mysql.user;

【出力結果】
mysql> grant replication slave on *.* to 'repl'@'10.0.0.11' identified by 'mysql'
    -> ;
Query OK, 0 rows affected, 1 warning (0.01 sec)
mysql> select Host, User from mysql.user;
+-----------+---------------+
| Host      | User          |
+-----------+---------------+
| 10.0.0.11 | repl          |
| localhost | mysql.session |
| localhost | mysql.sys     |
| localhost | myuser        |
| localhost | repl          |
| localhost | root          |
+-----------+---------------+
6 rows in set (0.00 sec)

mysql>
```

### マスター側にてステータス確認

```sql
show master status;

【出力結果】
mysql> show master status\G
*************************** 1. row ***************************
             File: awsstg-db001-bin.000007
         Position: 485
     Binlog_Do_DB:
 Binlog_Ignore_DB:
Executed_Gtid_Set: 86a2b2da-9683-11e9-9dd6-067b425ce144:1-42
1 row in set (0.00 sec)

mysql>
```



### スレーブ側にてレプリケーションスレーブの設定と開始

```sql
change master to master_host = '10.0.0.13',master_user = 'repl',master_password = 'mysql',master_log_file = 'awsstg-db001-bin.000007',master_log_pos = 485;

#レプリケーションの開始
start slave;

show slave status\G

【出力結果】

mysql> change master to master_host = '10.0.0.13',master_user = 'repl',master_password = 'mysql',master_log_file = 'awsstg-db001-bin.000007',master_log_pos = 485;
Query OK, 0 rows affected, 2 warnings (0.01 sec)

mysql>

mysql> show warnings\G
*************************** 1. row ***************************
  Level: Note
   Code: 1759
Message: Sending passwords in plain text without SSL/TLS is extremely insecure.
*************************** 2. row ***************************
  Level: Note
   Code: 1760
Message: Storing MySQL user name or password information in the master info repository is not secure and is therefore not recommended. Please consider using the USER and PASSWORD connection options for START SLAVE; see the 'START SLAVE Syntax' in the MySQL Manualfor more information.
2 rows in set (0.00 sec)
mysql> 
mysql> 
mysql> start slave;
Query OK, 0 rows affected (0.00 sec)
mysql> show slave status\G
*************************** 1. row ***************************
               Slave_IO_State: Waiting for master to send event
                  Master_Host: 10.0.0.13
                  Master_User: repl
                  Master_Port: 3306
                Connect_Retry: 60
              Master_Log_File: awsstg-db001-bin.000007
          Read_Master_Log_Pos: 84251854
               Relay_Log_File: awsstg-db002-relay-bin.000004
                Relay_Log_Pos: 84251325
        Relay_Master_Log_File: awsstg-db001-bin.000007
             Slave_IO_Running: Yes
            Slave_SQL_Running: Yes
              Replicate_Do_DB:
          Replicate_Ignore_DB:
           Replicate_Do_Table:
       Replicate_Ignore_Table:
      Replicate_Wild_Do_Table:
  Replicate_Wild_Ignore_Table:
                   Last_Errno: 0
                   Last_Error:
                 Skip_Counter: 0
          Exec_Master_Log_Pos: 84251854
              Relay_Log_Space: 84252123
              Until_Condition: None
               Until_Log_File:
                Until_Log_Pos: 0
           Master_SSL_Allowed: No
           Master_SSL_CA_File:
           Master_SSL_CA_Path:
              Master_SSL_Cert:
            Master_SSL_Cipher:
               Master_SSL_Key:
        Seconds_Behind_Master: 0
Master_SSL_Verify_Server_Cert: No
                Last_IO_Errno: 0
                Last_IO_Error:
               Last_SQL_Errno: 0
               Last_SQL_Error:
  Replicate_Ignore_Server_Ids:
             Master_Server_Id: 1
                  Master_UUID: 86a2b2da-9683-11e9-9dd6-067b425ce144
             Master_Info_File: /var/lib/mysql/master.info
                    SQL_Delay: 0
          SQL_Remaining_Delay: NULL
      Slave_SQL_Running_State: Slave has read all relay log; waiting for more updates
           Master_Retry_Count: 86400
                  Master_Bind:
      Last_IO_Error_Timestamp:
     Last_SQL_Error_Timestamp:
               Master_SSL_Crl:
           Master_SSL_Crlpath:
           Retrieved_Gtid_Set: 86a2b2da-9683-11e9-9dd6-067b425ce144:43-68
            Executed_Gtid_Set: 86a2b2da-9683-11e9-9dd6-067b425ce144:1-27:43-68
                Auto_Position: 0
         Replicate_Rewrite_DB:
                 Channel_Name:
           Master_TLS_Version:
1 row in set (0.00 sec)


```

