---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "When FLUSH PRIVILEGES Is Required in MySQL"
subtitle: ""
summary: " "
tags: ["MySQL"]
categories: ["MySQL"]
url: mysql-flush-privileges.html
date: 2019-07-01
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



### Introduction

When performing privilege-related operations in MySQL, there are cases where `FLUSH PRIVILEGES` is executed reflexively without thinking.

### Overview of Privilege Management

Privilege information is stored in tables such as `user`, `db`, `tables_priv`, `columns_priv`, and `procs_priv`, and it appears to be kept in an in-memory cache for faster access.

> https://dev.mysql.com/doc/refman/5.6/ja/privileges-provided.html
>
> 6.2.1 Privileges Provided by MySQL
>
> Information about account privileges is stored in the `user`, `db`, `tables_priv`, `columns_priv`, and `procs_priv` tables in the `mysql` database (see [Section 6.2.2, "Grant Tables"](https://dev.mysql.com/doc/refman/5.6/ja/grant-tables.html)). The MySQL server reads the contents of these tables into memory at startup and reloads them under the conditions indicated in [Section 6.2.6, "When Privilege Changes Take Effect"](https://dev.mysql.com/doc/refman/5.6/ja/privilege-changes.html).

It is explicitly stated that `FLUSH PRIVILEGES` is not required when using `GRANT`, `REVOKE`, `SET PASSWORD`, or `RENAME USER`.

> https://dev.mysql.com/doc/refman/5.6/ja/privilege-changes.html
>
> ### 6.2.6 When Privilege Changes Take Effect
>
> When a user uses account management statements such as `GRANT`, `REVOKE`, `SET PASSWORD`, or `RENAME USER` to indirectly modify the grant tables, the server recognizes those changes and loads the grant tables into memory again immediately.
>
> If you modify the grant tables directly using statements such as `INSERT`, `UPDATE`, or `DELETE`, your changes have no effect on privilege checking until you either restart the server or tell it to reload the tables. If you modify the grant tables directly but forget to reload them, your changes have *no effect* until you restart the server. You might wonder why your changes don't make a difference.

### Cases Where FLUSH PRIVILEGES Is NOT Required

#### Creating a User

```sql
CREATE USER 'mytest'@'localhost' IDENTIFIED BY 'Oracle2019%';
```

#### Displaying the User List

```sql
SELECT host, user FROM mysql.user;
```

#### Granting Privileges

```sql
grant all on *.* to 'mytest'@'localhost' IDENTIFIED BY 'Oracle2019%';
```

#### Checking Privileges

```sql
show grants for mytest@localhost;
```

#### Revoking Privileges

```sql
revoke all on *.* from 'mytest'@'localhost';
```

### Cases Where FLUSH PRIVILEGES IS Required

#### Deleting a User

On the other hand, when using statements such as `INSERT`, `UPDATE`, or `DELETE` to directly modify the grant tables, the changes have no effect on privilege checking until you restart the server or tell it to reload the tables. Let me verify the behavior when directly maintaining mysql.user with a delete statement versus using DROP USER.

##### 1.) Using drop user

```sql
DROP USER mytest@'localhost';
```

In the case of drop user, it is an account management statement, so the user-related information in memory is also synchronously flushed. (FLUSH PRIVILEGES is not required)

```sql
[Command Result]
mysql> DROP USER mytest@'localhost';
Query OK, 0 rows affected (0.00 sec)
mysql> show grants for mytest@localhost;
ERROR 1141 (42000): There is no such grant defined for user 'mytest' on host 'localhost'
```

##### 2.) Deleting from mysql.user with a DELETE statement

```sql
delete from mysql.user where user like 'mytest' and host like 'localhost';
```

Unlike drop user, this method of user deletion leaves privilege-related information in memory, so `FLUSH PRIVILEGES` is required.

```sql
mysql> delete from mysql.user where user like 'mytest' and host like 'localhost';
Query OK, 1 row affected (0.00 sec)

mysql> show grants for mytest@localhost; # mytest user information remains.
+--------------------------------------------+
| Grants for mytest@localhost                |
+--------------------------------------------+
| GRANT USAGE ON *.* TO 'mytest'@'localhost' |
+--------------------------------------------+
1 row in set (0.00 sec)

mysql> FLUSH PRIVILEGES; # Reflect changes with flush privileges command
Query OK, 0 rows affected (0.01 sec)

mysql> show grants for mytest@localhost;
ERROR 1141 (42000): There is no such grant defined for user 'mytest' on host 'localhost'
mysql>
```

### Summary

This example used user deletion, but when performing operations that directly maintain the user table, `FLUSH PRIVILEGES` should be required.
