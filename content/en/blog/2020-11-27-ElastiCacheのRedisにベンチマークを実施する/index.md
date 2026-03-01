---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Running Benchmarks Against ElastiCache Redis"
subtitle: ""
summary: " "
tags: ["AWS","ElastiCache","Redis"]
categories: ["AWS","ElastiCache","Redis"]
url: aws-elasticache-redis-benchmark.html
date: 2020-11-27
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

Using the built-in `redis-benchmark` to run benchmarks against ElastiCache Redis.

#### Manual

> How fast is Redis? – Redis https://redis.io/topics/benchmarks

#### Option Descriptions

| Option | Supplement | Default | Description |
| ---------- | -------------- | ------------ | ------------------------------------------------------------ |
| -h | <hostname> | 127.0.0.1 | Specify server hostname |
| -p | <port> | 6379 | Specify server port |
| -s | <socket> | | Specify server socket |
| -c | <clients> | 50 | Specify number of parallel connections |
| -n | <requests> | 100000 | Specify number of requests |
| -d | <size> | 2 | Specify SET/GET value size in bytes |
| -r | <keyspacelen> | | Issue random commands to simulate real operations and induce cache misses<br />Example: Run 1 million SET operations using random keys from 100k possible keys<br />redis-benchmark -t set -r 100000 -n 1000000 |
| -k | | 1 | 1=keep alive 0=reconnect |
| -P | | 1 | Enable pipelining<br />https://redis.io/topics/pipelining |
| -q | | | Show only queries/second value |
| -csv | | | Output in CSV format. Note: no headers are included |
| -l | | | Loop forever |
| -t | <tests> | | Run only the comma-separated list of tests. Example: -t get,set → run only get and set commands |
| -I | | | Idle mode |

#### Pattern 1

Run with default settings. 100,000 requests, 50 concurrent connections, 2-byte data size, etc.

```
redis-benchmark -h redistest.xxxxx.0001.apne1.cache.amazonaws.com
```

Output

Shows latency distribution and how many seconds requests took to complete

```
[ec2-user@bastin ~]$ redis-benchmark -h redistest.xxxxx.0001.apne1.cache.amazonaws.com
====== PING_INLINE ======
  100000 requests completed in 2.62 seconds
  50 parallel clients
  3 bytes payload
  keep alive: 1

12.45% <= 1 milliseconds
98.95% <= 2 milliseconds
99.54% <= 3 milliseconds
99.75% <= 4 milliseconds
99.90% <= 5 milliseconds
99.97% <= 6 milliseconds
100.00% <= 6 milliseconds
38138.82 requests per second

～(omitted)～
```

#### Pattern 2

Run in silent mode. Show only queries/second value.

```
redis-benchmark -h redistest.xxxxx.0001.apne1.cache.amazonaws.com -q
```

Output

```
[ec2-user@bastin ~]$ redis-benchmark -h redistest.xxxxx.0001.apne1.cache.amazonaws.com -q
PING_INLINE: 43840.42 requests per second
PING_BULK: 35958.29 requests per second
SET: 37907.50 requests per second
GET: 34293.55 requests per second
INCR: 41288.19 requests per second
LPUSH: 43327.55 requests per second
RPUSH: 43725.41 requests per second
LPOP: 46403.71 requests per second
RPOP: 44943.82 requests per second
SADD: 45085.66 requests per second
HSET: 27563.40 requests per second
SPOP: 34258.31 requests per second
LPUSH (needed to benchmark LRANGE): 31279.32 requests per second
LRANGE_100 (first 100 elements): 30902.35 requests per second
LRANGE_300 (first 300 elements): 15941.34 requests per second
LRANGE_500 (first 450 elements): 12241.40 requests per second
LRANGE_600 (first 600 elements): 9856.10 requests per second
MSET (10 keys): 25766.55 requests per second
```

#### Pattern 3

Increase client count to 100 and run only `set` and `get` commands (silent mode).

```
redis-benchmark -h redistest.xxxxx.0001.apne1.cache.amazonaws.com -p 6379 -c 100 -n 100000 -q -t set,get
```

Output

```
[ec2-user@bastin ~]$ redis-benchmark -h redistest.xxxxx.0001.apne1.cache.amazonaws.com -p 6379 -c 100 -n 100000 -q -t set,get
SET: 45766.59 requests per second
GET: 42789.90 requests per second
```

#### Pattern 4

Run in CSV mode

```
redis-benchmark -h redistest.xxxxx.0001.apne1.cache.amazonaws.com -p 6379 -c 100 -n 100000 -t set,get --csv
```

Output

```
[ec2-user@bastin ~]$ redis-benchmark -h redistest.xxxxx.0001.apne1.cache.amazonaws.com -p 6379 -c 100 -n 100000 -t set,get --csv
"SET","41562.76"
"GET","38491.14"
```

#### Other

Adding `--latency` to `redis-cli` measures latency using PING. It continuously takes samples, so stop with Ctrl+C.

```
[ec2-user@bastin ~]$ redis-cli -h redistest.xxxx.0001.apne1.cache.amazonaws.com -p 6379 --latency
min: 0, max: 18, avg: 0.40 (4591 samples)
```
