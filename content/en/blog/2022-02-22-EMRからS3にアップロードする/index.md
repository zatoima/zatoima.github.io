---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Uploading Files from EMR to S3"
subtitle: ""
summary: " "
tags: ["AWS","EMR"]
categories: ["AWS","EMR"]
url: aws-emr-s3-upload
date: 2022-02-22
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

There are broadly two methods for uploading files from HDFS to S3. Let me try both with some quick commands.

- hadoop fs -cp: File operations on HDFS. Appears to use multipart upload to S3.
- hadoop distcp/s3-dist-cp: Distributed processing using MapReduce. Note that s3-dist-cp is specialized for S3 with more features.

### Preparation

Create test files (1 GB each)

```sh
head -c 1000m /dev/urandom > test1.txt
head -c 1000m /dev/urandom > test2.txt
head -c 1000m /dev/urandom > test3.txt

hadoop fs -rm /user/hadoop/test*.txt
hadoop fs -put test1.txt /user/hadoop/
hadoop fs -put test2.txt /user/hadoop/
hadoop fs -put test3.txt /user/hadoop/

hadoop fs -ls /user/hadoop/
```

Confirm files on HDFS

```sh
[hadoop@ip-192-168-0-33 ~]$ hadoop fs -ls /user/hadoop/
SLF4J: Class path contains multiple SLF4J bindings.
SLF4J: Found binding in [jar:file:/usr/lib/hadoop/lib/slf4j-log4j12-1.7.25.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: Found binding in [jar:file:/usr/share/aws/emr/emrfs/lib/slf4j-log4j12-1.7.12.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: See http://www.slf4j.org/codes.html#multiple_bindings for an explanation.
SLF4J: Actual binding is of type [org.slf4j.impl.Log4jLoggerFactory]
Found 3 items
-rw-r--r--   1 hadoop hdfsadmingroup 1048576000 2022-02-03 07:05 /user/hadoop/test1.txt
-rw-r--r--   1 hadoop hdfsadmingroup 1048576000 2022-02-03 07:05 /user/hadoop/test2.txt
-rw-r--r--   1 hadoop hdfsadmingroup 1048576000 2022-02-03 07:05 /user/hadoop/test3.txt
```

### hadoop fs -cp

```sh
[hadoop@ip-192-168-0-33 ~]$ hadoop fs -cp -f /user/hadoop/test1.txt s3://<S3 bucket>/
SLF4J: Class path contains multiple SLF4J bindings.
SLF4J: Found binding in [jar:file:/usr/lib/hadoop/lib/slf4j-log4j12-1.7.25.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: Found binding in [jar:file:/usr/share/aws/emr/emrfs/lib/slf4j-log4j12-1.7.12.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: See http://www.slf4j.org/codes.html#multiple_bindings for an explanation.
SLF4J: Actual binding is of type [org.slf4j.impl.Log4jLoggerFactory]
22/02/03 07:06:12 INFO s3n.MultipartUploadOutputStream: uploadPart: partNum 1 of 's3://<S3 bucket>/test1.txt' from local file '/mnt1/s3/emrfs-5827993998494060058/0000000000', 134217728 bytes in 1498 ms, md5: uq4Pfvy+zC+aWVf01fhRtQ== md5hex: baae0f7efcbecc2f9a5957f4d5f851b5
22/02/03 07:06:12 INFO s3n.MultipartUploadOutputStream: uploadPart: partNum 2 of 's3://<S3 bucket>/test1.txt' from local file '/mnt/s3/emrfs-9215835204334260739/0000000001', 134217728 bytes in 1321 ms, md5: GGb7qT4wl52ltofQ0SSMnQ== md5hex: 1866fba93e30979da5b687d0d1248c9d
22/02/03 07:06:13 INFO s3n.MultipartUploadOutputStream: uploadPart: partNum 3 of 's3://<S3 bucket>/test1.txt' from local file '/mnt1/s3/emrfs-5827993998494060058/0000000002', 134217728 bytes in 1200 ms, md5: FAVMVJoyETUk9XHXYSTUew== md5hex: 14054c549a32113524f571d76124d47b
22/02/03 07:06:13 INFO s3n.MultipartUploadOutputStream: uploadPart: partNum 4 of 's3://<S3 bucket>/test1.txt' from local file '/mnt/s3/emrfs-9215835204334260739/0000000003', 134217728 bytes in 1009 ms, md5: AVAEWiZHnQB7l8QhiwWhIg== md5hex: 0150045a26479d007b97c4218b05a122
22/02/03 07:06:14 INFO s3n.MultipartUploadOutputStream: uploadPart: partNum 5 of 's3://<S3 bucket>/test1.txt' from local file '/mnt1/s3/emrfs-5827993998494060058/0000000004', 134217728 bytes in 1074 ms, md5: d4erSVSapJ8tfT/KPMm0ag== md5hex: 7787ab49549aa49f2d7d3fca3cc9b46a
22/02/03 07:06:15 INFO s3n.MultipartUploadOutputStream: uploadPart: partNum 6 of 's3://<S3 bucket>/test1.txt' from local file '/mnt/s3/emrfs-9215835204334260739/0000000005', 134217728 bytes in 1079 ms, md5: mQElzOq2L+D6NgaM5io9wg== md5hex: 990125cceab62fe0fa36068ce62a3dc2
22/02/03 07:06:15 INFO s3n.MultipartUploadOutputStream: close closed:false s3://<S3 bucket>/test1.txt
22/02/03 07:06:15 INFO s3n.MultipartUploadOutputStream: uploadPart: partNum 7 of 's3://<S3 bucket>/test1.txt' from local file '/mnt1/s3/emrfs-5827993998494060058/0000000006', 134217728 bytes in 985 ms, md5: NpCzzQUQia4lZlXx4TtBxA== md5hex: 3690b3cd051089ae256655f1e13b41c4
22/02/03 07:06:16 INFO s3n.MultipartUploadOutputStream: uploadPart: partNum 8 of 's3://<S3 bucket>/test1.txt' from local file '/mnt/s3/emrfs-9215835204334260739/0000000007', 109051904 bytes in 850 ms, md5: 4yBV8LAdE5MVZcTAjvl+/w== md5hex: e32055f0b01d13931565c4c08ef97eff
22/02/03 07:06:16 INFO dispatch.DefaultMultipartUploadDispatcher: Completed multipart upload of 8 parts 1048576000 bytes
22/02/03 07:06:16 INFO s3n.MultipartUploadOutputStream: close closed:true s3://<S3 bucket>/test1.txt
```

### hadoop distcp

```sh
[hadoop@ip-192-168-0-33 ~]$ time hadoop distcp /user/hadoop/test2.txt s3://<S3 bucket>/
(... output omitted ...)

real	0m18.727s
user	0m9.132s
sys	0m0.356s
[hadoop@ip-192-168-0-33 ~]$
```

### s3-dist-cp

```sh
[hadoop@ip-192-168-0-33 ~]$ time s3-dist-cp --src /user/hadoop/test3.txt --dest s3://<S3 bucket>/
(... output omitted ...)

real	0m31.031s
user	0m11.129s
sys	0m0.432s
[hadoop@ip-192-168-0-33 ~]$
```

Since s3-dist-cp and hadoop distcp use MapReduce distributed processing, they can be checked in the application history. They run on YARN consuming memory, so the number of jobs needs to be considered carefully.

![image-20220203161048359](image-20220203161048359.png)
