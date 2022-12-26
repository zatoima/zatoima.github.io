---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Oracle Databaseのv_$表とv$表の関係"
subtitle: ""
summary: " "
tags: ["Oracle"]
categories: ["Oracle"]
url: oracle-dynamic-performance-view.html
date: 2019-07-13
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



### はじめに

**動的パフォーマンス・ビュー（v$表）**は、データベースが稼働している間にデータベース・サーバーが継続して更新している特別なビューです。他DBと比較してもOracleDatabaseの動的パフォーマンス・ビューの多彩さは郡を抜いています。

アクセスする際は `v$表` に対してselect文を投げますが、たまに各種ドキュメントを見ると「v_$表」という表記が出てきます。例えば下記はたまたま見つけた例ですが、AWSのDMSのマニュアルにはこのような記載があります。

> https://docs.aws.amazon.com/ja_jp/dms/latest/userguide/CHAP_Source.Oracle.html
>
> 権限を付与する場合、オブジェクトのシノニムではなく、オブジェクトの実際の名前を使用します。たとえば、V_$OBJECT を下線を含めて使用し、下線のない V$OBJECT は使用しません。

またディクショナリビューを参照する権限を与える場合には、 `V_$LICENSE` と**<u>アンダーバー</u>**を指定をする必要がありますよね。

```sql
SQL> GRANT SELECT ON SYS.V_$LICENSE TO rivus;
 
権限付与が成功しました。
```

### V_$表とは

下記のマニュアルにもある通り、正確にはv$表は**<u>PUBLIC シノニム</u>**です。V$ARCHIVEの場合、V_$ARCHIVEが `実表` でV$ARCHIVEは `シノニム` です。権限を付与する際はシノニムではなく実表に対しての権限を付与する必要があるため、上記の通りアンダーバーを付与する必要があるということです。

> https://docs.oracle.com/cd/E16338_01/server.112/b56311/dynviews_1001.htm
>
> 実際の動的パフォーマンス・ビューは、接頭辞`V_$`によって識別されます。これらのビューのパブリック・シノニムには、接頭辞`V$`が付いています。データベース管理者および他のユーザーは、`V_$`オブジェクトではなく、`V$`オブジェクトのみにアクセスしてください。

実際の確認した結果は下記の通りです。

```sql
SQL> set pages 2000 lin 2000
col OWNER for a10
col SYNONYM_NAME for a15
col TABLE_OWNER for a15
col TABLE_NAME for a15

select OWNER,SYNONYM_NAME,TABLE_OWNER,TABLE_NAME from ALL_SYNONYMS where TABLE_NAME like 'V_$ARCHIVE';
SQL> SQL> SQL> SQL> SQL> SQL>
OWNER      SYNONYM_NAME    TABLE_OWNER     TABLE_NAME
---------- --------------- --------------- ---------------
PUBLIC     V$ARCHIVE       SYS             V_$ARCHIVE
```