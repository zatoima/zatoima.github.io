---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Connecting to Snowflake from M1 Mac via Excel ODBC"
subtitle: ""
summary: " "
tags: ["Snowflake"]
categories: ["Snowflake"]
url: snowflake-m1-mac-excel-connect
date: 2022-12-26
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

### Overview

Steps to connect from Excel on M1 Mac to Snowflake via ODBC.

### Environment

- MacBook Pro (M1 chip, macOS Ventura 13.0)
- Microsoft Excel for Mac (Version 16.68)

### Prerequisites

Install iODBC and ODBC Manager.

```sh
brew install libiodbc
```

Download and install ODBC Manager from:
http://www.odbcmanager.net/

### Install Snowflake ODBC Driver

Download the Snowflake ODBC driver for macOS from the Snowflake documentation page and install it.

After installation, the driver files will be located at:
```
/opt/snowflake/snowflakeodbc/lib/universal/libSnowflake.dylib
```

### Configure simba.snowflake.ini

Edit `/opt/snowflake/snowflakeodbc/lib/universal/simba.snowflake.ini`:

```ini
[Driver]
DriverManagerEncoding=UTF-16
ICULib=/opt/snowflake/snowflakeodbc/lib/universal/icu/lib/libicuuc.dylib
ICUi18n=/opt/snowflake/snowflakeodbc/lib/universal/icu/lib/libicui18n.dylib
LogLevel=0
LogPath=/tmp
ODBCInstLib=/usr/local/iODBC/lib/libiodbcinst.dylib
SwapFilePath=/tmp
```

### Configure odbc.ini

Edit `/Library/ODBC/odbc.ini`:

```ini
[ODBC Data Sources]
snowflake_dsn=SnowflakeDSIIDriver

[snowflake_dsn]
Driver=/opt/snowflake/snowflakeodbc/lib/universal/libSnowflake.dylib
Description=
uid=YOUR_USERNAME
pwd=YOUR_PASSWORD
server=YOUR_ACCOUNT.snowflakecomputing.com
database=YOUR_DATABASE
schema=YOUR_SCHEMA
warehouse=YOUR_WAREHOUSE
role=YOUR_ROLE
```

### Register in ODBC Manager

Launch ODBC Manager and register the DSN configured in `odbc.ini`.

### Connect from Excel

In Excel, use **Data > Get External Data > New Database Query** to connect via ODBC.

Select the DSN registered above and enter credentials to connect to Snowflake.

### Troubleshooting

If the connection fails, check the following:
- Verify the iODBC library path in `simba.snowflake.ini` is correct
- Check that the `ODBCInstLib` path points to the correct `libiodbcinst.dylib`
- Ensure ODBC Manager shows the DSN as properly configured
