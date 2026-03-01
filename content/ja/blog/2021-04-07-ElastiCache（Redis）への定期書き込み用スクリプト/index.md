---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "ElastiCache（Redis）への定期書き込み用スクリプト"
subtitle: ""
summary: " "
tags: ["AWS","ElastiCache","Redis","Bash"]
categories: ["AWS","ElastiCache","Redis","Bash"]
url: aws-elasticache-redis-bash-write-monitoring.html
date: 2021-04-07
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



ElastiCache Redisのフェイルオーバーやメンテナンス時にどのくらい影響があるかを調査する時に適当に準備したスクリプト

- タイムアウトを0.1秒に設定
  - 接続不可の場合に、タイムアウトさせて次の処理に進むため
- redis-cliの戻り値で処理成功か否かでsleep時間を微調整

```sh
#!/bin/bash
for a in {1..100000}
  do
    dt_now=`date "+%Y%m%d%H%M%S"`
    echo "==================="
    timeout -sKILL 0.1 redis-cli -c -h redis-test11.xxxxx.ng.0001.apne1.cache.amazonaws.com -p 6379 set $dt_now $a
      if [ $? != 0 ]; then 
        # タイムアウトしたときの処理
        echo "異常終了orタイムアウト"
      else
        # 正常終了したときの処理
        echo "正常終了"
        sleep 1
      fi
    echo $dt_now
    echo "==================="
  done
```







