---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Notes on PostgreSQL pg_hba.conf"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgresql-about-pg-hba-conf.html
date: 2019-08-27
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


### Format of the "pg_hba.conf" File

```
Pattern 1 : local database_name user_name authentication_method
Pattern 2 : host database_name user_name ip_address subnet_mask authentication_method
Pattern 3 : host database_name user_name cidr_address authentication_method
```

##### Connection Method

Specifies the connection method the client uses for authentication

| Connection Method | Description             |
| ----------------- | ----------------------- |
| host              | TCP/IP connection       |
| local             | UNIX domain connection  |

##### DB Name

Specifies the database name to connect to. Use comma-separated values for multiple databases. "all" targets all databases.

##### User Name

Specifies the user name to connect with. Use comma-separated values for multiple users. "all" targets all users.

##### IP Address and Subnet

Only when the connection method is "host". Specifies the range of client IP addresses.

##### Client Authentication Settings

| Authentication Method | Description                                             |
| --------------------- | ------------------------------------------------------- |
| trust                 | Always allow                                            |
| reject                | Always deny                                             |
| md5                   | Perform password authentication encrypted with MD5      |
| password              | Perform password authentication in unencrypted plaintext|

### Other Notes

Client authentication decisions are made from the top of the records in order. If there is a match, authentication is performed using the method specified in that line. If authentication succeeds, the connection is allowed; if it fails, the connection is rejected. Once authentication succeeds or fails, subsequent records are not checked.
