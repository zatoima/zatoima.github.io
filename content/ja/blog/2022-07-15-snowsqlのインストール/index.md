---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "snowsqlのインストール"
subtitle: ""
summary: " "
tags: ["Snowflake"]
categories: ["Snowflake"]
url: snowflake-snowsql-install-howto
date: 2022-07-15
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





> リポジトリ
>
> https://sfc-repo.snowflakecomputing.com/snowsql/bootstrap/1.2/linux_x86_64/index.html

### rpmのダウンロード

-----

```
[ec2-user@bastin ~]$ wget https://sfc-repo.snowflakecomputing.com/snowsql/bootstrap/1.2/linux_x86_64/snowflake-snowsql-1.2.9-1.x86_64.rpm
--2022-07-11 21:25:48--  https://sfc-repo.snowflakecomputing.com/snowsql/bootstrap/1.2/linux_x86_64/snowflake-snowsql-1.2.9-1.x86_64.rpm
Resolving sfc-repo.snowflakecomputing.com (sfc-repo.snowflakecomputing.com)... 65.9.42.106, 65.9.42.8, 65.9.42.36, ...
Connecting to sfc-repo.snowflakecomputing.com (sfc-repo.snowflakecomputing.com)|65.9.42.106|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 25164112 (24M) [binary/octet-stream]
Saving to: ‘snowflake-snowsql-1.2.9-1.x86_64.rpm’

100%[==================================================================================================================================================================================================>] 25,164,112  20.0MB/s   in 1.2s   

2022-07-11 21:25:50 (20.0 MB/s) - ‘snowflake-snowsql-1.2.9-1.x86_64.rpm’ saved [25164112/25164112]

[ec2-user@bastin ~]$ ls -l snowflake-snowsql-1.2.9-1.x86_64.rpm 
-rw-rw-r-- 1 ec2-user ec2-user 25164112 Aug  7  2020 snowflake-snowsql-1.2.9-1.x86_64.rpm
```

### rpmからインストール

-----

```
[ec2-user@bastin ~]$ sudo rpm -ivh snowflake-snowsql-1.2.9-1.x86_64.rpm
Preparing...                          ################################# [100%]
Updating / installing...
   1:snowflake-snowsql-1.2.9-1        ################################# [100%]
[ec2-user@bastin ~]$ snowsql -v
Version: 1.2.9
```

ヘルプ

-----

```
[ec2-user@bastin ~]$ snowsql --help
Usage: snowsql [OPTIONS]

Options:
  -a, --accountname TEXT          Name assigned to your Snowflake account. If
                                  you are not on us-west-2 or AWS deployement,
                                  append the region and platform to the end,
                                  e.g., <account>.<region> or
                                  <account>.<region>.<platform>Honors
                                  $SNOWSQL_ACCOUNT.
  -u, --username TEXT             Username to connect to Snowflake. Honors
                                  $SNOWSQL_USER.
  -d, --dbname TEXT               Database to use. Honors $SNOWSQL_DATABASE.
  -s, --schemaname TEXT           Schema in the database to use. Honors
                                  $SNOWSQL_SCHEMA.
  -r, --rolename TEXT             Role name to use. Honors $SNOWSQL_ROLE.
  -w, --warehouse TEXT            Warehouse to use. Honors $SNOWSQL_WAREHOUSE.
  -h, --host TEXT                 Host address for the connection. Honors
                                  $SNOWSQL_HOST.
  -p, --port INTEGER              Port number for the connection. Honors
                                  $SNOWSQL_PORT.
  --region TEXT                   (DEPRECATED) Append the region or any sub
                                  domains before snowflakecomputing.com to the
                                  end of accountname parameter after a dot.
                                  e.g., accountname=<account>.<region>
  -m, --mfa-passcode TEXT         Token to use for multi-factor authentication
                                  (MFA)
  --mfa-passcode-in-password      Appends the MFA passcode to the end of the
                                  password.
  --abort-detached-query          Aborts a query if the connection between the
                                  client and server is lost. By default, it
                                  won't abort even if the connection is lost.
  --probe-connection              Test connectivity to Snowflake. This option
                                  is mainly used to print out the TLS/SSL
                                  certificate chain.
  --proxy-host TEXT               (DEPRECATED. Use HTTPS_PROXY and HTTP_PROXY
                                  environment variables.) Proxy server
                                  hostname. Honors $SNOWSQL_PROXY_HOST.
  --proxy-port INTEGER            (DEPRECATED. Use HTTPS_PROXY and HTTP_PROXY
                                  environment variables.) Proxy server port
                                  number. Honors $SNOWSQL_PROXY_PORT.
  --proxy-user TEXT               (DEPRECATED. Use HTTPS_PROXY and HTTP_PROXY
                                  environment variables.) Proxy server
                                  username. Honors $SNOWSQL_PROXY_USER. Set
                                  $SNOWSQL_PROXY_PWD for the proxy server
                                  password.
  --authenticator TEXT            Authenticator: 'snowflake',
                                  'externalbrowser' (to use any IdP and a web
                                  browser), 'oauth', or
                                  https://<your_okta_account_name>.okta.com
                                  (to use Okta natively).
  -v, --version                   Shows the current SnowSQL version, or uses a
                                  specific version if provided as a value.
  --noup                          Disables auto-upgrade for this run. If no
                                  version is specified for -v, the latest
                                  version in ~/.snowsql/ is used.
  -D, --variable TEXT             Sets a variable to be referred by &<var>. -D
                                  tablename=CENUSTRACKONE or --variable
                                  db_key=$DB_KEY
  -o, --option TEXT               Set SnowSQL options. See the options
                                  reference in the Snowflake documentation.
  -f, --filename PATH             File to execute.
  -q, --query TEXT                Query to execute.
  --config PATH                   Path and name of the SnowSQL configuration
                                  file. By default, ~/.snowsql/config.
  -P, --prompt                    Forces a password prompt. By default,
                                  $SNOWSQL_PWD is used to set the password.
  -M, --mfa-prompt                Forces a prompt for the second token for
                                  MFA.
  -c, --connection TEXT           Named set of connection parameters to use.
  --single-transaction            Connects with autocommit disabled. Wraps
                                  BEGIN/COMMIT around statements to execute
                                  them as a single transaction, ensuring all
                                  commands complete successfully or no change
                                  is applied.
  --private-key-path PATH         Path to private key file in PEM format used
                                  for key pair authentication. Private key
                                  file is required to be encrypted and
                                  passphrase is required to be specified in
                                  environment variable
                                  $SNOWSQL_PRIVATE_KEY_PASSPHRASE
  -U, --upgrade                   Force upgrade of SnowSQL to the latest
                                  version.
  -K, --client-session-keep-alive
                                  Keep the session active indefinitely, even
                                  if there is no activity from the user..
  --disable-request-pooling       Disable request pooling. This can help speed
                                  up connection failover
  --token TEXT                    The token to be used with oauth
                                  authentication method
  -?, --help                      Show this message and exit.

```



#### 参考

-----

> SnowSQL のインストール — Snowflake Documentation https://docs.snowflake.com/ja/user-guide/snowsql-install-config.html





