---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Apache Bench（abコマンド）で簡易的なアクセスをCloudFrontに実行"
subtitle: ""
summary: " "
tags: ["AWS","CloudFront"]
categories: ["AWS","CloudFront"]
url: aws-cloudfront-apache-bench-ab-access
date: 2022-01-24
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, Bott
---


### Apacheをインストール

```sh
[ec2-user@bastin ~]$ sudo yum -y install apache
Loaded plugins: langpacks, priorities, update-motd
amzn2-core                                                                                                         ～省略～                                                                          6/6 

Installed:
  httpd.x86_64 0:2.4.51-1.amzn2                                                                                                                                                                                 

Dependency Installed:
  generic-logos-httpd.noarch 0:18.0.0-4.amzn2    httpd-filesystem.noarch 0:2.4.51-1.amzn2    httpd-tools.x86_64 0:2.4.51-1.amzn2    mailcap.noarch 0:2.1.41-2.amzn2    mod_http2.x86_64 0:1.15.19-1.amzn2.0.1   

Complete!
```

### abコマンドのオプション

よく使うのは`-n`、`-c`あたりか。

```sh
[ec2-user@bastin ~]$ ab
ab: wrong number of arguments
Usage: ab [options] [http[s]://]hostname[:port]/path
Options are:
    -n requests     Number of requests to perform
    -c concurrency  Number of multiple requests to make at a time
    -t timelimit    Seconds to max. to spend on benchmarking
                    This implies -n 50000
    -s timeout      Seconds to max. wait for each response
                    Default is 30 seconds
    -b windowsize   Size of TCP send/receive buffer, in bytes
    -B address      Address to bind to when making outgoing connections
    -p postfile     File containing data to POST. Remember also to set -T
    -u putfile      File containing data to PUT. Remember also to set -T
    -T content-type Content-type header to use for POST/PUT data, eg.
                    'application/x-www-form-urlencoded'
                    Default is 'text/plain'
    -v verbosity    How much troubleshooting info to print
    -w              Print out results in HTML tables
    -i              Use HEAD instead of GET
    -x attributes   String to insert as table attributes
    -y attributes   String to insert as tr attributes
    -z attributes   String to insert as td or th attributes
    -C attribute    Add cookie, eg. 'Apache=1234'. (repeatable)
    -H attribute    Add Arbitrary header line, eg. 'Accept-Encoding: gzip'
                    Inserted after all normal header lines. (repeatable)
    -A attribute    Add Basic WWW Authentication, the attributes
                    are a colon separated username and password.
    -P attribute    Add Basic Proxy Authentication, the attributes
                    are a colon separated username and password.
    -X proxy:port   Proxyserver and port number to use
    -V              Print version number and exit
    -k              Use HTTP KeepAlive feature
    -d              Do not show percentiles served table.
    -S              Do not show confidence estimators and warnings.
    -q              Do not show progress when doing more than 150 requests
    -l              Accept variable document length (use this for dynamic pages)
    -g filename     Output collected data to gnuplot format file.
    -e filename     Output CSV file with percentages served
    -r              Don't exit on socket receive errors.
    -m method       Method name
    -h              Display usage information (this message)
    -I              Disable TLS Server Name Indication (SNI) extension
    -Z ciphersuite  Specify SSL/TLS cipher suite (See openssl ciphers)
    -f protocol     Specify SSL/TLS protocol
                    (SSL3, TLS1, TLS1.1, TLS1.2 or ALL)
    -E certfile     Specify optional client certificate chain and private key
```

### CloudFrontのディストリビューションに簡易的なアクセスを実施

```sh
[ec2-user@bastin ~]$ ab -n 10000 -c 10 https://d35onj12it5a8t.cloudfront.net/date.html
This is ApacheBench, Version 2.3 <$Revision: 1879490 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking d35onj12it5a8t.cloudfront.net (be patient)
Completed 1000 requests
Completed 2000 requests
Completed 3000 requests
Completed 4000 requests
Completed 5000 requests
Completed 6000 requests
Completed 7000 requests
Completed 8000 requests
Completed 9000 requests
Completed 10000 requests
Finished 10000 requests


Server Software:        AmazonS3
Server Hostname:        d35onj12it5a8t.cloudfront.net
Server Port:            443
SSL/TLS Protocol:       TLSv1.2,ECDHE-RSA-AES128-GCM-SHA256,2048,128
Server Temp Key:        ECDH P-256 256 bits
TLS Server Name:        d35onj12it5a8t.cloudfront.net

Document Path:          /date.html
Document Length:        469 bytes

Concurrency Level:      10
Time taken for tests:   12.832 seconds
Complete requests:      10000
Failed requests:        0
Total transferred:      9240000 bytes
HTML transferred:       4690000 bytes
Requests per second:    779.33 [#/sec] (mean)
Time per request:       12.832 [ms] (mean)
Time per request:       1.283 [ms] (mean, across all concurrent requests)
Transfer rate:          703.22 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        5   10   2.8     10      67
Processing:     1    3   1.0      3      10
Waiting:        1    3   1.0      3      10
Total:          6   13   3.7     13      72

Percentage of the requests served within a certain time (ms)
  50%     13
  66%     13
  75%     16
  80%     17
  90%     18
  95%     18
  98%     19
  99%     20
 100%     72 (longest request)
```

### 結果から主に見るポイント

| No.  | 項目                 | 説明                      | 結果サンプル                 |
| ---- | -------------------- | ------------------------- | ---------------------------- |
| 1    | Concurrency Level    | 同時実行数                | 10                           |
| 2    | Time taken for tests | テスト時間                | 12.832 seconds               |
| 3    | Complete requests    | 総リクエスト数            | 10000                        |
| 4    | Failed requests      | 失敗したリクエスト        | 0                            |
| 5    | Total transferred    | 転送量（全体）            | 9240000 bytes                |
| 6    | HTML transferred     | 転送量（HTML）            | 4690000 bytes                |
| 7    | Requests per second  | 1秒間あたりのリクエスト数 | 779.33 [#/sec] (mean)        |
| 8    | Transfer rate        | 転送レート                | 703.22 [Kbytes/sec] received |

### 参考

> Apache Benchでサクッと性能テスト - Qiita https://qiita.com/flexfirm/items/ac5a2f53cfa933a37192
>
> Apache Benchの結果の見方 - Qiita https://qiita.com/nnmr/items/2be82691e19da261c4e4

