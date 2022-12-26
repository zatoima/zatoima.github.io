---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "RedshiftのLambda UDFの設定"
subtitle: ""
summary: " "
tags: ["AWS","Redshift"]
categories: ["AWS","Redshift"]
url: aws-redshift-lamdba-udf-setting
date: 2022-02-24
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

### Lamdba側の関数作成

小文字に変換する関数

```python
import json

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    print(json.dumps(event))
    res = [x[0].lower() for x in event['arguments']]
    ret_json = json.dumps({"results": res})
    return ret_json
```

![image-20220224232758552](image-20220224232758552.png)

### IAMロールの作成

IAMロールを用意してRedshiftクラスタにアタッチする

> https://docs.aws.amazon.com/ja_jp/redshift/latest/dg/udf-creating-a-lambda-sql-udf.html#udf-lambda-authorization
>
> Lambda 用に IAM ロールを作成する

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Invoke",
            "Effect": "Allow",
            "Action": [
                "lambda:InvokeFunction"
            ],
            "Resource": "arn:aws:lambda:us-west-2:123456789012:function:my-function"
        }
    ]
}
```

### Redshift側でLamdba udfの作成

```sql
CREATE OR REPLACE EXTERNAL FUNCTION f_lower_python(varchar)
RETURNS varchar IMMUTABLE
LAMBDA 'f_lower_python'
IAM_ROLE 'arn:aws:iam::xxxxx:role/redshiftlf1';
```

### 実行

```sql
mydb=# select f_lower_python(a) from test1 limit 10;
 f_lower_python 
----------------
 aaaa
 uidus
 aaaa
 uidus
 uidus
 aaaa
 uidus
 aaaa
 aaaa
 uidus
(10 rows)
```

