---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Commands and Options for Data Pump (expdp/impdp)"
subtitle: ""
summary: " "
tags: ["Oracle"]
categories: ["Oracle"]
url: oracle-datapump-command.html
date: 2019-03-04
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


When using Data Pump, TABLE-level or SCHEMA-level operations are most common, so I summarized the other modes and options for quick reference.

## **expdp**

```bash
-- database level
expdp iko/oracle DIRECTORY=homedir dumpfile=db.dmp REUSE_DUMPFILES=YES full=y

-- tablespace level
expdp iko/oracle DIRECTORY=homedir dumpfile=ts.dmp REUSE_DUMPFILES=YES tablespaces=TSDATA

-- schema level
expdp iko/oracle DIRECTORY=homedir dumpfile=schema.dmp REUSE_DUMPFILES=YES schemas=iko

-- table level
expdp iko/oracle DIRECTORY=homedir dumpfile=table.dmp  REUSE_DUMPFILES=YES tables=iko.t1

```

> https://docs.oracle.com/cd/E57425_01/121/SUTIL/toc.htm
>
> [Parameters Available in Export Utility Command-Line Mode](https://docs.oracle.com/cd/E57425_01/121/SUTIL/GUID-33880357-06B1-4CA2-8665-9D41347C6705.htm)

| Parameter            | Description                                                         |
| -------------------- | -------------------------------------------------------------------- |
| directory            | Specifies the directory where the dump file will be created, using a DIRECTORY object name |
| dumpfile             | Specifies the dump file name                                         |
| logfile              | Specifies the log file name for the export                          |
| content              | Specifies what to export: data_only (table data only), metadata_only (object definitions only), all (definitions and data, default) |
| estimate             | Calculates job estimates. Specifies the method to use for estimation |
| estimate_only        | Estimates disk space without actually running the export             |
| exclude              | Specifies objects to exclude from the export                        |
| reuse_dumpfiles      | Overwrite option for dump files. Overwrites if file already exists  |
| filesize             | Specifies the size of each dump file in bytes                       |
| remap_data           | Specifies a data transformation function                            |
| compression          | Compresses the dump file. ALL, DATA_ONLY, METADATA_ONLY, NONE      |
| encryption           | Encrypts part or all of the dump file. ALL, DATA_ONLY, ENCRYPTED_COLUMNS_ONLY, METADATA_ONLY, NONE |
| encryption_algorithm | Specifies the encryption method (AES128, AES192, AES256)           |
| encryption_mode      | Specifies how the encryption key is generated. DUAL, PASSWORD, TRANSPARENT |
| encryption_password  | Password to create encrypted data in the dump file                  |
| flashback_scn        | Specifies the export point-in-time by SCN. UNDO data must remain    |




## **impdp**

```bash
-- database level
impdp iko/oracle DIRECTORY=homedir dumpfile=db.dmp TABLE_EXISTS_ACTION=REPLACE full=y

-- tablespace level
impdp iko/oracle DIRECTORY=homedir dumpfile=ts.dmp TABLE_EXISTS_ACTION=REPLACE tablespaces=JRADATA

-- schemas level
impdp iko/oracle DIRECTORY=homedir dumpfile=schema.dmp schemas=iko

-- table level
impdp iko/oracle DIRECTORY=homedir dumpfile=table.dmp tables=iko.insert_t1

```

> https://docs.oracle.com/cd/E57425_01/121/SUTIL/toc.htm
>
> Parameters Available in Import Utility Command-Line Mode

| Parameter           | Description                                                         | Notes                          |
| ------------------- | -------------------------------------------------------------------- | ------------------------------ |
| remap_schema        | Specified when importing to a different schema                       |                                |
| remap_tablespace    | Specified when importing to a different tablespace                   |                                |
| directory           | Specifies the directory where import files are located, using a DIRECTORY object name | Same as expdp                  |
| dumpfile            | Specifies the import file name                                       | Same as expdp                  |
| logfile             | Specifies the log file name for the import                          | Same as expdp                  |
| content             | Specifies what to import: data_only (table data only), metadata_only (object definitions only), all (definitions and data, default) | Same as expdp                  |
| exclude             | Specifies objects to exclude from the import                        | Same as expdp                  |
| table_exists_action | Specifies behavior when definitions or data already exist at the import destination. SKIP \| APPEND \| TRUNCATE \| REPLACE | Applies only to table objects  |
| encryption_password | Used when a password was set during expdp                           |                                |
