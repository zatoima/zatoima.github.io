---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "How to Get Neptune Instance Audit Logs"
subtitle: ""
summary: " "
tags: ["AWS","Neptune"]
categories: ["AWS","Neptune"]
url: aws-neptune-audit-log.html
date: 2020-04-07
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

Even though I had checked `Enable Audit Logging` during instance creation, audit logs were not being output. It turned out that parameter configuration was also required, as indicated by the message: `Audit logging must be enabled for logs to be published in CloudWatch Logs. Please set the neptune_enable_audit_log parameter to enable (1) in the parameter group that is used in this database cluster.`

<img src="image-20200321134807338.png" alt="image-20200321134807338" style="zoom:67%;" />

When audit logs were not being output, I needed to change `neptune_enable_audit_log` from "0" to "1". Since the apply type is static, a restart is required when making this change.

<img src="image-20200321134242850.png" alt="image-20200321134242850" style="zoom:67%;" />

#### Log Sample

The first entry is a query executed from Neptune Workbench, and the second is a query POSTed via curl.

```sh
1584766979615, 10.0.1.18:34266, 10.0.3.215:8182, HTTP_POST, [unknown], [unknown], "HttpObjectAggregator$AggregatedFullHttpRequest(decodeResult: success, version: HTTP/1.1, content: CompositeByteBuf(ridx: 0, widx: 79, cap: 79, components=1)) POST /sparql HTTP/1.1 Host: neptestdb-cluster.cluster-xxxxxx.ap-northeast-1.neptune.amazonaws.com:8182 User-Agent: python-requests/2.20.0 Accept-Encoding: gzip, deflate Accept: */* Connection: keep-alive Content-Length: 79 Content-Type: application/x-www-form-urlencoded", query=SELECT+%2A%0AWHERE+%7B%0A++%3Fs+%3Fp+%3Fo+.%0A%7D%0ALIMIT+100%0AOFFSET+0+

1584767048270, 10.0.1.123:56336, 10.0.3.215:8182, HTTP_POST, [unknown], [unknown], "HttpObjectAggregator$AggregatedFullHttpRequest(decodeResult: success, version: HTTP/1.1, content: CompositeByteBuf(ridx: 0, widx: 47, cap: 47, components=1)) POST /sparql HTTP/1.1 Host: neptestdb.xxxxxxx.ap-northeast-1.neptune.amazonaws.com:8182 User-Agent: curl/7.61.1 Accept: */* Content-Length: 47 Content-Type: application/x-www-form-urlencoded", query=select ?s ?p ?o where {?s ?p ?o} limit 10

```

### References

> Using Audit Logs with an Amazon Neptune Cluster - Amazon Neptune https://docs.aws.amazon.com/ja_jp/neptune/latest/userguide/auditing.html
