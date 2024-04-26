---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "RDS Oracleで拡張Varchar型の設定を行う"
subtitle: ""
summary: " "
tags: ["Oracle","RDS"]
categories: ["Oracle","RDS"]
url: oracle-rds-for-oracle-extended-varchar2-setting.html
date: 2021-05-06
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



拡張データ型で、ユーザーは VARCHAR2、NVARCHAR2、RAW コラムを最大 32767 バイトのサイズ（デフォルト：4000バイト）に拡大できるという機能があり、その機能をRDS Oracleで設定する方法をメモ。

1. データベースのスナップショットを作成

2. パラメータグループ内の `MAX_STRING_SIZE` パラメータを `EXTENDED` に設定

   ![image-20210427133115351](image-20210427133115351.png)

3. DB インスタンスを修正して `MAX_STRING_SIZE` を `EXTENDED` に設定したパラメータグループと関連付け

4. DB再起動

5. パラメータ確認

```
SQL> show parameters max_string_size

NAME				     TYPE
------------------------------------ ---------------------------------
VALUE
------------------------------
max_string_size 		     string
EXTENDED
SQL> 
```

データベースをupgradeモードにしたり、`utl32k.sql`の実行がないので、オンプレミスよりも手順が簡略化されている。

> Oracle 19cで拡張VARCHAR2型を導入 | my opinion is my own https://zatoima.github.io/oracle-19c-extended-varchar2.html

### 参照

> Oracle DB インスタンスのその他のタスクの実行 - Amazon Relational Database Service https://docs.aws.amazon.com/ja_jp/AmazonRDS/latest/UserGuide/Appendix.Oracle.CommonDBATasks.Misc.html#Oracle.Concepts.ExtendedDataTypes
>
> 拡張データ型を有効にする