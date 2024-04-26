---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "DynamoDBからkinesis firehose経由でS3に出力"
subtitle: ""
summary: " "
tags: ["AWS"]
categories: ["AWS"]
url: aws-dynamodb-to-s3-by-kinesis
date: 2022-05-04
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

### Kinesis Data Streamsの作成

![image-20220502211530378](image-20220502211530378.png)

![image-20220502211543696](image-20220502211543696.png)

![image-20220502211630241](image-20220502211630241.png)

### Kinesis Data Firehoseの設定

![image-20220502211723573](image-20220502211723573.png)

![image-20220502211812110](image-20220502211812110.png)

![image-20220502211957305](image-20220502211957305.png)

### DynamoDB側の設定

```
aws dynamodb create-table --table-name 'cities' \
--attribute-definitions '[{"AttributeName":"key","AttributeType": "S"}]' \
--key-schema '[{"AttributeName":"key","KeyType": "HASH"}]' \
--provisioned-throughput '{"ReadCapacityUnits": 5,"WriteCapacityUnits": 5}'
```

![image-20220502212422288](image-20220502212422288.png)

![image-20220502212438252](image-20220502212438252.png)

![image-20220502212641300](image-20220502212641300.png)

### DynamoDB側でデータ生成

```
aws dynamodb put-item --table-name cities --item '{ "population": { "N": "38164" }, "date_mod": { "S": "1950-6-22" }, "key": { "S": "t0924" }, "name": { "S": "足利" } }'
aws dynamodb put-item --table-name cities --item '{ "population": { "N": "72391" }, "date_mod": { "S": "1950-8-30" }, "key": { "S": "t0925" }, "name": { "S": "日光" } }'
aws dynamodb put-item --table-name cities --item '{ "population": { "N": "56148" }, "date_mod": { "S": "1950-9-7" }, "key": { "S": "t0926" }, "name": { "S": "下野" } }'
```

![image-20220502212815311](image-20220502212815311.png)

### S3側の出力（※一部抜粋）

![image-20220502215201611](image-20220502215201611.png)

```json
{"awsRegion":"ap-northeast-1","eventID":"1e84f1ca-438d-4837-a6bd-aa4592be6f8a","eventName":"MODIFY","userIdentity":null,"recordFormat":"application/json","tableName":"cities","dynamodb":{"ApproximateCreationDateTime":1651495525900,"Keys":{"key":{"S":"t0926"}},"NewImage":{"population":{"N":"54148"},"key":{"S":"t0926"},"name":{"S":"下野"},"date_mod":{"S":"1950-9-7"}},"OldImage":{"population":{"N":"56148"},"key":{"S":"t0926"},"name":{"S":"下野"},"date_mod":{"S":"1950-9-7"}},"SizeBytes":104},"eventSource":"aws:dynamodb"}
```

