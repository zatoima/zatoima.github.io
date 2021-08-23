---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Data Pump(expdp/impdp)使用時のコマンドとオプション"
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


Data Pumpを使うときはTABLE単位かSCHEMA単位が多いのでそのほかのモードとオプション含めて簡単に整理した。

## **expdp**

```bash
-- database単位
expdp iko/oracle DIRECTORY=homedir dumpfile=db.dmp REUSE_DUMPFILES=YES full=y

-- tablespace単位
expdp iko/oracle DIRECTORY=homedir dumpfile=ts.dmp REUSE_DUMPFILES=YES tablespaces=TSDATA

-- schema単位
expdp iko/oracle DIRECTORY=homedir dumpfile=schema.dmp REUSE_DUMPFILES=YES schemas=iko

-- table単位
expdp iko/oracle DIRECTORY=homedir dumpfile=table.dmp  REUSE_DUMPFILES=YES tables=iko.t1

```

> https://docs.oracle.com/cd/E57425_01/121/SUTIL/toc.htm
>
> [エクスポート・ユーティリティのコマンドライン・モードで使用可能なパラメータ](https://docs.oracle.com/cd/E57425_01/121/SUTIL/GUID-33880357-06B1-4CA2-8665-9D41347C6705.htm)

| パラメータ           | 説明                                                         |
| -------------------- | ------------------------------------------------------------ |
| directory            | dmpファイルを作成するディレクトリを、DIRECTORYオブジェクト名で指定する |
| dumpfile             | dmpファイル名を指定する                                      |
| logfile              | dmp時のログファイル名を指定する                              |
| content              | expdp対象を指定する      data_only：表のデータのみ      metadata_only：オブジェクト定義のみ      all：定義とデータ（デフォルト） |
| estimate             | ジョブ見積りを算出します。見積もりに使用するメソッドを指定   |
| estimate_only        | expdpを実行せず、ディスク容量の見積りだけ行う                |
| exclude              | expdpから除外したいオブジェクトを指定する                    |
| reuse_dumpfiles      | dmpファイルの上書きオプション。expdp先にファイルが存在する場合は上書きする |
| filesize             | 各dmpファイルのサイズをバイト単位で指定                      |
| remap_data           | データ変換ファンクションを指定                               |
| compression          | dmpファイルを圧縮する。ALL, DATA_ONLY, METADATA_ONLY, NONE   |
| encryption           | dmpファイルの一部またはすべてを暗号化      ALL, DATA_ONLY, ENCRYPTED_COLUMNS_ONLY, METADATA_ONLY, NONE |
| encryption_algorithm | 暗号化の方法を指定（AES128, AES192, AES256）                 |
| encryption_mode      | 暗号化キーの生成方法。      DUAL, PASSWORD, TRANSPARENT      |
| encryption_password  | dmpファイル内に暗号化データを作成するためのパスワード        |
| flashback_scn        | expdp時点をSCNで指定するUNDOにデータが残っている必要がある   |





## **impdp**

```bash
-- database単位
impdp iko/oracle DIRECTORY=homedir dumpfile=db.dmp TABLE_EXISTS_ACTION=REPLACE full=y

-- tablespace単位
impdp iko/oracle DIRECTORY=homedir dumpfile=ts.dmp TABLE_EXISTS_ACTION=REPLACE tablespaces=JRADATA

-- schemas単位
impdp iko/oracle DIRECTORY=homedir dumpfile=schema.dmp schemas=iko

-- table単位
impdp iko/oracle DIRECTORY=homedir dumpfile=table.dmp tables=iko.insert_t1

```

> https://docs.oracle.com/cd/E57425_01/121/SUTIL/toc.htm
>
> インポート・ユーティリティのコマンドライン・モードで使用可能なパラメータ

| パラメータ          | 説明                                                         | 備考                           |
| ------------------- | ------------------------------------------------------------ | ------------------------------ |
| remap_schema        | 異なるスキーマへimpdpする場合に指定する                      |                                |
| remap_tablespace    | 異なる表領域へimpdpする場合に指定する                        |                                |
| directory           | impdpファイルが置いてあるディレクトリを、DIRECTORYオブジェクト名で指定する | expdpと同様                    |
| dumpfile            | impdpファイルのファイル名を指定する                          | expdpと同様                    |
| logfile             | impdp時のログファイル名を指定する                            | expdpと同様                    |
| content             | impdp対象を指定する       data_only：表のデータのみ       metadata_only：オブジェクト定義のみ       all：定義とデータ（デフォルト） | expdpと同様                    |
| exclude             | impdpから除外したいのオブジェクトを指定する                  | expdpと同様                    |
| table_exists_action | impdp先に既に定義やデータが存在した場合の動きを指定する      SKIP \| APPEND \| TRUNCATE \| REPLACE | 表オブジェクトだけを対象とする |
| encryption_password | expdp時にパスワードセットした場合に使用する                  |                                |