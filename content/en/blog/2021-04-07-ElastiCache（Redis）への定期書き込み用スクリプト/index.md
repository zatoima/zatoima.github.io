---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Script for Periodic Writes to ElastiCache (Redis)"
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



A script I prepared for investigating impact during ElastiCache Redis failover or maintenance:

- Set timeout to 0.1 seconds
  - So that if connection fails, it times out and moves to the next iteration
- Adjust sleep time based on the return value of redis-cli (success or failure)

```sh
#!/bin/bash
for a in {1..100000}
  do
    dt_now=`date "+%Y%m%d%H%M%S"`
    echo "==================="
    timeout -sKILL 0.1 redis-cli -c -h redis-test11.xxxxx.ng.0001.apne1.cache.amazonaws.com -p 6379 set $dt_now $a
      if [ $? != 0 ]; then
        # Processing when timeout occurs
        echo "Abnormal termination or timeout"
      else
        # Processing when normal termination
        echo "Normal termination"
        sleep 1
      fi
    echo $dt_now
    echo "==================="
  done
```
