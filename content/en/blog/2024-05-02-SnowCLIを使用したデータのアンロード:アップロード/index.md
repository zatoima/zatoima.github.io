---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Data Unload and Upload Using SnowCLI"
subtitle: ""
summary: " "
tags: ["Snowflake"]
categories: ["Snowflake"]
url: snowflake-snowcli-data-unload-upload
date: 2024-05-02
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

## Prerequisites

1. CLI Tool Installation:

   - Install SnowSQL
   - Install SnowCLI
2. Enable sample database

   - Using the sample database

     - https://docs.snowflake.com/ja/user-guide/sample-data-using

## Steps

### Delete and recreate working directory

```sql
#rm -rf ~/work/temp/upload
mkdir -p ~/work/temp/upload
```

### Create a new database using SnowSQL

```sql
snow sql -q 'create or replace database sandbox';
```

### Create a new stage

```sql
snow object stage create sandbox.public.my_stage;
```

### Unload data to the stage in the specified format

```sql
snow sql -q 'copy into @sandbox.public.my_stage/data.csv from (select * from SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.LINEITEM limit 1000) file_format = (format_name = CSV_FORMAT compression = NONE) SINGLE=TRUE HEADER=TRUE OVERWRITE = TRUE';
```

### Display the list of files in the stage

```sql
snow object stage list @sandbox.public.my_stage
```

### Copy files from stage to local directory

```sql
cd ~/work/temp/upload
snow object stage copy @sandbox.public.my_stage .
```

### Upload files from local to stage (using SnowCLI)

```sql
snow object stage copy data.csv @sandbox.public.my_stage
```

### Upload local files to stage (using SnowSQL)

*Login omitted*

```sql
use database sandbox;
put file://~/work/temp/upload/* @my_stage;
```

## References

> [Snowflake CLI \| Snowflake Documentation](https://docs.snowflake.com/en/developer-guide/snowflake-cli-v2/index)
>
> [snowflakedb/snowflake\-cli: Snowflake CLI is an open\-source command\-line tool explicitly designed for developer\-centric workloads in addition to SQL operations\.](https://github.com/snowflakedb/snowflake-cli)
