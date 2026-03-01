---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Snowflake Access Control and Permission Management"
subtitle: ""
summary: " "
tags: ["snowflake"]
categories: ["snowflake"]
url: snowflake-security-access-control
date: 2022-08-30
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

### Access Control Framework

- **Discretionary Access Control (DAC):** Each object has an owner who can grant access to that object.
- **Role-Based Access Control (RBAC):** Access privileges are assigned to roles, and roles are assigned to users.

![image-20220826105850407](image-20220826105850407.png)

### About ACCOUNTADMIN

I had a misconception: ACCOUNTADMIN is the most powerful role in the system, but I thought it was equivalent to SYSDBA in Oracle or the root user in PostgreSQL. In fact, it is not a superuser role.

> https://docs.snowflake.com/en/user-guide/security-access-control-considerations.html#using-the-accountadmin-role
>
> Note that ACCOUNTADMIN is **not** a superuser role. This role only allows viewing and managing objects in the account when this role, or roles lower in the [role hierarchy](https://docs.snowflake.com/en/user-guide/security-access-control-overview.html#label-role-hierarchy-and-privilege-inheritance), have sufficient privileges on those objects.
>
> https://docs.snowflake.com/en/user-guide/security-access-control-considerations.html#managing-custom-roles
>
> When a custom role is first created, it exists in an orphaned state. It must be assigned to users who will use the object privileges associated with the role. The custom role must also be granted to a role that manages objects created by the custom role.
>
> By default, even the ACCOUNTADMIN role cannot modify or drop objects created by a custom role. The custom role must be granted directly to the ACCOUNTADMIN role or, preferably, to another role in the hierarchy that has SYSADMIN as a parent. The SYSADMIN role is managed by the ACCOUNTADMIN role.

#### Securable Objects

- Under account
  - Users
  - Roles
  - Databases
  - Warehouses
  - Schemas
    - Tables
    - Views
    - Stages
    - Stored Procedures
    - UDFs, etc.

#### Privilege Hierarchy Inheritance

- [Overview of Access Control — Snowflake Documentation](https://docs.snowflake.com/en/user-guide/security-access-control-overview.html#role-hierarchy-and-privilege-inheritance)

![image-20220826105403835](image-20220826105403835.png)

### Trying It Out

Working with `accountadmin`. Ideally, `USERADMIN` should be used...

```sql
use role accountadmin;
```

Create user:

```sql
CREATE USER IF NOT EXISTS WORKUSER
  PASSWORD = 'workusertest'
  DEFAULT_ROLE = 'PUBLIC';
```

Create role:

```sql
CREATE ROLE IF NOT EXISTS WORKROLE;
```

Grant role to user:

```sql
GRANT ROLE WORKROLE TO USER WORKUSER;
SHOW USER LIKE 'WORKUSER';
```

Create database:

```sql
USE ROLE SYSADMIN;
CREATE DATABASE WORKDB;
```

Grant database permissions:

```sql
USE ROLE SECURITYADMIN;
GRANT OWNERSHIP ON DATABASE WORKDB TO ROLE WORKROLE;
GRANT OWNERSHIP ON SCHEMA WORKDB.PUBLIC TO ROLE WORKROLE;
```

Grant warehouse permissions:

```sql
USE ROLE SYSADMIN;
CREATE WAREHOUSE WH_X_SMALL;

USE ROLE SECURITYADMIN;
GRANT USAGE ON WAREHOUSE WH_X_SMALL TO ROLE WORKROLE;
GRANT OPERATE ON WAREHOUSE WH_X_SMALL TO ROLE WORKROLE;
```

Switch to the created user and role:

```sql
USE ROLE WORKROLE;
USE DATABASE WORKDB;
USE WAREHOUSE WH_X_SMALL;
```

Create schema:

```sql
CREATE SCHEMA WORKSCHEMA;
```

Create table:

OWNER and other settings look fine.

```sql
workuser#WH_X_SMALL@WORKDB.WORKSCHEMA>CREATE TABLE t1(a number,b VARCHAR,c VARCHAR,d number,e varchar) AS
                                      SELECT SEQ8()
                                            ,randstr(200, random())
                                            ,randstr(300, random())
                                            ,row_number() over (order by seq4())
                                            ,current_timestamp
                                      FROM   table(generator(rowcount => 1000))
                                      ;
+--------------------------------+
| status                         |
|--------------------------------|
| Table T1 successfully created. |
+--------------------------------+
1 Row(s) produced. Time Elapsed: 1.784s
workuser#WH_X_SMALL@WORKDB.WORKSCHEMA>
workuser#WH_X_SMALL@WORKDB.WORKSCHEMA>show tables;
+-------------------------------+------+---------------+-------------+-------+---------+------------+------+--------+----------+----------------+----------------------+-----------------+-------------+
| created_on                    | name | database_name | schema_name | kind  | comment | cluster_by | rows |  bytes | owner    | retention_time | automatic_clustering | change_tracking | is_external |
|-------------------------------+------+---------------+-------------+-------+---------+------------+------+--------+----------+----------------+----------------------+-----------------+-------------|
| 2022-08-25 18:18:01.195 -0700 | T1   | WORKDB        | WORKSCHEMA  | TABLE |         |            | 1000 | 505344 | WORKROLE | 1              | OFF                  | OFF             | N           |
+-------------------------------+------+---------------+-------------+-------+---------+------------+------+--------+----------+----------------+----------------------+-----------------+-------------+
1 Row(s) produced. Time Elapsed: 0.110s
workuser#WH_X_SMALL@WORKDB.WORKSCHEMA>
```

### Verifying Role Hierarchy

The manual states that when creating a custom role, you should consider creating a role hierarchy that is ultimately assigned to a high-level admin role.

- [Configuring Access Control — Snowflake Documentation](https://docs.snowflake.com/en/user-guide/security-access-control-configure.html#creating-a-role-hierarchy)

![image-20220826103612735](image-20220826103612735.png)

In the current state, even with SYSADMIN or ACCOUNTADMIN, the T1 table in WORKSCHEMA in WORKDB cannot be accessed.

```sql
zatoima#COMPUTE_WH@(no database).(no schema)>select current_user(),current_database(), current_role(), current_warehouse();
+----------------+--------------------+----------------+---------------------+
| CURRENT_USER() | CURRENT_DATABASE() | CURRENT_ROLE() | CURRENT_WAREHOUSE() |
|----------------+--------------------+----------------+---------------------|
| ZATOIMA        | NULL               | ACCOUNTADMIN   | COMPUTE_WH          |
+----------------+--------------------+----------------+---------------------+
zatoima#COMPUTE_WH@(no database).(no schema)>use database WORKDB;
003001 (42501): SQL access control error:
Insufficient privileges to operate on database 'WORKDB'
zatoima#COMPUTE_WH@(no database).(no schema)>use role WORKROLE;
003013 (42501): SQL access control error:
Requested role 'WORKROLE' is not assigned to the executing user.  Specify another role to activate.
zatoima#COMPUTE_WH@(no database).(no schema)>
```

Grant role to sysadmin to create hierarchy:

```sql
grant role WORKROLE to role sysadmin;
```

```sql
zatoima#COMPUTE_WH@(no database).(no schema)>grant role WORKROLE to role sysadmin;
+----------------------------------+
| status                           |
|----------------------------------|
| Statement executed successfully. |
+----------------------------------+
1 Row(s) produced. Time Elapsed: 0.108s
zatoima#COMPUTE_WH@(no database).(no schema)>
zatoima#COMPUTE_WH@(no database).(no schema)>use database WORKDB;

+----------------------------------+
| status                           |
|----------------------------------|
| Statement executed successfully. |
+----------------------------------+
1 Row(s) produced. Time Elapsed: 0.148s
zatoima#COMPUTE_WH@WORKDB.PUBLIC>select current_user(),current_database(), current_role(), current_warehouse();
+----------------+--------------------+----------------+---------------------+
| CURRENT_USER() | CURRENT_DATABASE() | CURRENT_ROLE() | CURRENT_WAREHOUSE() |
|----------------+--------------------+----------------+---------------------|
| ZATOIMA        | WORKDB             | ACCOUNTADMIN   | COMPUTE_WH          |
+----------------+--------------------+----------------+---------------------+

```

#### Checking Permissions

```sql
zatoima#(no warehouse)@WORKDB.PUBLIC>show grants on schema WORKSCHEMA;
+-------------------------------+-----------+------------+-------------------+------------+--------------+--------------+------------+
| created_on                    | privilege | granted_on | name              | granted_to | grantee_name | grant_option | granted_by |
|-------------------------------+-----------+------------+-------------------+------------+--------------+--------------+------------|
| 2022-08-25 18:17:01.660 -0700 | OWNERSHIP | SCHEMA     | WORKDB.WORKSCHEMA | ROLE       | WORKROLE     | true         | WORKROLE   |
+-------------------------------+-----------+------------+-------------------+------------+--------------+--------------+------------+
1 Row(s) produced. Time Elapsed: 0.084s
zatoima#(no warehouse)@WORKDB.PUBLIC>
zatoima#(no warehouse)@WORKDB.PUBLIC>show grants to user workuser;
+-------------------------------+----------+------------+--------------+--------------+
| created_on                    | role     | granted_to | grantee_name | granted_by   |
|-------------------------------+----------+------------+--------------+--------------|
| 2022-08-25 18:06:33.349 -0700 | WORKROLE | USER       | WORKUSER     | ACCOUNTADMIN |
+-------------------------------+----------+------------+--------------+--------------+
1 Row(s) produced. Time Elapsed: 0.088s
zatoima#(no warehouse)@WORKDB.PUBLIC>
zatoima#(no warehouse)@WORKDB.PUBLIC>
zatoima#(no warehouse)@WORKDB.PUBLIC>show grants to role WORKROLE;
+-------------------------------+-----------+------------+----------------------+------------+--------------+--------------+------------+
| created_on                    | privilege | granted_on | name                 | granted_to | grantee_name | grant_option | granted_by |
|-------------------------------+-----------+------------+----------------------+------------+--------------+--------------+------------|
| 2022-08-25 18:11:16.801 -0700 | OWNERSHIP | DATABASE   | WORKDB               | ROLE       | WORKROLE     | true         | WORKROLE   |
| 2022-08-25 18:11:57.027 -0700 | OWNERSHIP | SCHEMA     | WORKDB.PUBLIC        | ROLE       | WORKROLE     | true         | WORKROLE   |
| 2022-08-25 18:17:01.660 -0700 | OWNERSHIP | SCHEMA     | WORKDB.WORKSCHEMA    | ROLE       | WORKROLE     | true         | WORKROLE   |
| 2022-08-25 18:18:01.317 -0700 | OWNERSHIP | TABLE      | WORKDB.WORKSCHEMA.T1 | ROLE       | WORKROLE     | true         | WORKROLE   |
| 2022-08-25 18:13:55.955 -0700 | OPERATE   | WAREHOUSE  | WH_X_SMALL           | ROLE       | WORKROLE     | false        | SYSADMIN   |
| 2022-08-25 18:13:42.713 -0700 | USAGE     | WAREHOUSE  | WH_X_SMALL           | ROLE       | WORKROLE     | false        | SYSADMIN   |
+-------------------------------+-----------+------------+----------------------+------------+--------------+--------------+------------+
6 Row(s) produced. Time Elapsed: 0.089s
zatoima#(no warehouse)@WORKDB.PUBLIC>

```

| Column Name  | Meaning                                                       |
| ------------ | ----------------------------------------------- |
| created_on   | Date/time when a new record was created by a privilege operation |
| privilege    | Type of privilege granted |
| granted_on   | Type of target object for privilege grant |
| name         | Name of target object for privilege grant |
| granted_to   | Type of non-privilege grant target |
| grantee_name | Type of non-privilege grant target |
| grant_option | Whether the privilege has admin option |
| granted_by   | Role that performed the privilege grant |

#### Displaying Roles and Users Granted a Role

```sql
zatoima#COMPUTE_WH@WORKDB.WORKSCHEMA>show grants of role WORKROLE;
+-------------------------------+----------+------------+--------------+--------------+
| created_on                    | role     | granted_to | grantee_name | granted_by   |
|-------------------------------+----------+------------+--------------+--------------|
| 2022-08-25 18:37:02.342 -0700 | WORKROLE | ROLE       | SYSADMIN     | ACCOUNTADMIN |
| 2022-08-25 18:06:33.349 -0700 | WORKROLE | USER       | WORKUSER     | ACCOUNTADMIN |
+-------------------------------+----------+------------+--------------+--------------+
2 Row(s) produced. Time Elapsed: 0.411s

```
