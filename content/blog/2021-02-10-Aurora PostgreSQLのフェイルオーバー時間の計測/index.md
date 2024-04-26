---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Aurora PostgreSQLのフェイルオーバー時間の計測"
subtitle: ""
summary: " "
tags: ["AWS","Aurora","RDS","PostgreSQL"]
categories: ["AWS","Aurora","RDS","PostgreSQL"]
url: aws-aurora-failover-time-test
date: 2021-02-10
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



# はじめに

Auroraのよくある質問を見ていたらフェイルオーバーが30秒以内に完了するとあったので、一応確認してみた。

> https://aws.amazon.com/jp/rds/aurora/faqs/
>
> Q: フェイルオーバー中はどのようなことが起き、どのくらいの時間がかかりますか?
>
> フェイルオーバーは Amazon Aurora によって自動的に処理されるため、アプリケーションは管理上の手動介入なしで、可能な限り迅速にデータベースオペレーションを再開することができます。
>
> - Amazon Aurora レプリカを同一の、または異なるアベイラビリティーゾーンに作成しておくと、フェイルオーバーが発生した場合、Aurora は DB インスタンスの正規名レコード (CNAME) を切り替えて正常なレプリカを指定します。指定されたレプリカはこれにより新しいプライマリに昇格します。フェイルオーバーは開始から終了まで通常 30 秒以内に完了します。

# 事前準備

テスト用のテーブル作成

```
create table failovertest(id serial,time timestamp);
```

雑なテスト用スクリプト。接続エラーが発生しても継続するようにexceptでpass。

```python
import psycopg2
import psycopg2.extras
import time
import datetime

for i in range(20000):
  try:
    dt_now = datetime.datetime.now()
    conn = psycopg2.connect("host=xxxxxx.cluster-xxxxx.ap-northeast-1.rds.amazonaws.com port=5432 dbname=xxx user=xxx password=xx")
    cur = conn.cursor()
    cur.execute("insert into failovertest (time) values (current_timestamp)")
    print(dt_now)
    time.sleep(1)
    conn.commit()
    cur.close()
    conn.close()
  except:
    pass
```

# 結果

`平均12秒`という結果に。

|       | Start    | End      | 秒数    |
| ----- | -------- | -------- | ------- |
| 1回目 | 2:20:40  | 2:20:53  | 0:00:13 |
| 2回目 | 2:23:19  | 2:23:30  | 0:00:11 |
| 3回目 | 2:24:37  | 2:24:53  | 0:00:16 |
| 4回目 | 11:29:03 | 11:29:13 | 0:00:10 |
| 5回目 | 11:30:06 | 11:30:18 | 0:00:12 |