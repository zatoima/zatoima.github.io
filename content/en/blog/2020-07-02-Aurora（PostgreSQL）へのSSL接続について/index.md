---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "SSL Connections to Aurora (PostgreSQL)"
subtitle: ""
summary: " "
tags: ["AWS","Aurora","PostgreSQL"]
categories: ["AWS","Aurora","PostgreSQL"]
url: aws-aurora-postgresql-ssl-connect.html
date: 2020-07-02
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

### Prerequisites

> https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.Security.html
>
> Checking SSL connection status

##### Install the Extension

```sql
create extension sslinfo;
```

##### Check Whether SSL Is Being Used

```sql
select ssl_is_used();
select ssl_cipher();
```

### Connect Without SSL

```sh
[ec2-user@bastin ~]$ export PGSSLMODE=disable
[ec2-user@bastin ~]$ psql -h aurorapgsqlv1.cluster-xxxxxx.ap-northeast-1.rds.amazonaws.com -U postgres -d postgres
psql (11.5, server 11.7)
Type "help" for help.

postgres=> select ssl_is_used();
 ssl_is_used
-------------
 f
(1 row)
```

### Connect With SSL

When RDS is created, an SSL certificate is automatically provisioned, and connections to RDS generally have SSL enabled. SSL usage can also be confirmed at the login prompt.

```sh
[ec2-user@bastin ~]$ psql -h aurorapgsqlv1.cluster-xxxxxx.ap-northeast-1.rds.amazonaws.com -U postgres -d postgres
psql (11.5, server 11.7)
SSL connection (protocol: TLSv1.2, cipher: ECDHE-RSA-AES256-GCM-SHA384, bits: 256, compression: off)
Type "help" for help.

postgres=> select ssl_is_used();
 ssl_is_used
-------------
 t
(1 row)

postgres=> select ssl_cipher();
         ssl_cipher
-----------------------------
 ECDHE-RSA-AES256-GCM-SHA384
(1 row)
```

To enforce SSL connections, change `rds.force_ssl` from "0" to "1".

### Validating the Certificate for Anti-Spoofing and Tamper Prevention

It is necessary to obtain the root certificate and perform validation to prevent spoofing and tampering. Refer to the following for the significance of this validation.

> What is SSL? An easy-to-understand explanation of its meaning and mechanism | Sakura's SSL https://ssl.sakura.ad.jp/column/ssl/
>
> For tamper prevention and anti-spoofing, the "Certificate Authority (CA)" in an SSL server certificate plays an important role. Encryption itself is possible without a CA, but CAs are third-party organizations (not servers or PCs) that guarantee "this site claiming to be ○○.jp really is ○○.jp."
>
> The "root certificate" issued by the CA is stored on PCs and smartphones, and is used to verify that the SSL server certificate and intermediate CA certificate sent from the server are genuinely associated with the root certificate (i.e., issued by the CA). Since root certificates are stored on the device itself and are difficult for malicious third parties to alter, this structure provides security.

##### Obtain the Root Certificate

```sh
wget https://s3.amazonaws.com/rds-downloads/rds-combined-ca-bundle.pem
psql "host=aurorapgsqlv1.cluster-xxxxxx.ap-northeast-1.rds.amazonaws.com sslmode=verify-full sslrootcert=rds-combined-ca-bundle.pem user=postgres dbname=postgres"
```

##### On Successful Validation

Specify `sslrootcert` and `sslmode` as arguments to `psql`.

```sh
[ec2-user@bastin ~]$ psql "host=aurorapgsqlv1.cluster-xxxxxx.ap-northeast-1.rds.amazonaws.com sslmode=verify-full sslrootcert=rds-combined-ca-bundle.pem user=postgres dbname=postgres"
psql (11.5, server 11.7)
SSL connection (protocol: TLSv1.2, cipher: ECDHE-RSA-AES256-GCM-SHA384, bits: 256, compression: off)
Type "help" for help.
```

Setting them as environment variables also works:

```sh
export PGSSLMODE=verify-full
export PGSSLROOTCERT=rds-combined-ca-bundle.pem
psql -h aurorapgsqlv1.cluster-xxxxxx.ap-northeast-1.rds.amazonaws.com -U postgres -d postgres
```

##### On Validation Failure

```sh
[ec2-user@bastin ~]$ psql "host=aurorapgsqlv1.cluster-xxxxxx.ap-northeast-1.rds.amazonaws.com sslmode=verify-full sslrootcert=dummy.pem user=postgres dbname=postgres"
psql: could not read root certificate file "dummy.pem": no SSL error reported
[ec2-user@bastin ~]$
```

### References

> Security with Amazon Aurora PostgreSQL - Amazon Aurora https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.Security.html
>
> Rotating Your SSL/TLS Certificate - Amazon Aurora https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/UsingWithRDS.SSL-certificate-rotation.html
