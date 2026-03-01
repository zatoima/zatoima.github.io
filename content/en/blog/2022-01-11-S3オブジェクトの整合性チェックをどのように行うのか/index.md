---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "How to Perform Integrity Checks on S3 Objects"
subtitle: ""
summary: " "
tags: ["AWS","S3"]
categories: ["AWS","S3"]
url: aws-s3-object-checksum-how-to
date: 2022-01-11
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom
---

As noted in the article below, when files are uploaded to S3 via multipart upload, there is a discrepancy between the MD5 and ETag values.

> Organizing the Relationship Between MD5 and ETag for S3 Objects | my opinion is my own https://zatoima.github.io/aws-s3-object-md5-etag/

### At Upload Time

As described below, the AWS CLI performs checksum validation for both standard and multipart uploads.

> https://docs.aws.amazon.com/cli/latest/topic/s3-faq.html
>
> ### Q: Does the AWS CLI validate checksums?
>
> The AWS CLI will perform checksum validation for uploading and downloading files in specific scenarios.
>
> #### Upload
>
> The AWS CLI will calculate and auto-populate the `Content-MD5` header for both standard and multipart uploads. If the checksum that S3 calculates does not match the `Content-MD5` provided, S3 will not store the object and instead will return an error message back the AWS CLI. The AWS CLI will retry this error up to 5 times before giving up. On the case that any files fail to transfer successfully to S3, the AWS CLI will exit with a non zero RC. See `aws help return-codes` for more information.

### At Download Time

As noted below, checksum verification cannot be performed under certain conditions.

- When the object was uploaded via multipart upload
- When the object was uploaded using server-side encryption with KMS
- When the object was uploaded using a customer-provided encryption key

> #### Download
>
> The AWS CLI will attempt to verify the checksum of downloads when possible, based on the `ETag` header returned from a `GetObject` request that's performed whenever the AWS CLI downloads objects from S3. If the calculated MD5 checksum does not match the expected checksum, the file is deleted and the download is retried. This process is retried up to 3 times. If a downloads fails, the AWS CLI will exit with a non zero RC. See `aws help return-codes` for more information.
>
> There are several conditions where the CLI is *not* able to verify checksums on downloads:
>
> - If the object was uploaded via multipart uploads
> - If the object was uploaded using server side encryption with KMS
> - If the object was uploaded using a customer provided encryption key
> - If the object is downloaded using range `GetObject` requests

So what should you do when integrity checking is not possible under certain conditions (such as multipart uploads or KMS encryption)? As stated: "Before uploading a file, you can use the file's MD5 checksum value as a reference for integrity checking after upload." This means attaching the md5 value as metadata and checking it after download. (In practice, this likely involves building an integrity-checking tool of some kind.)

> [Using the AWS CLI for Multipart Uploads to Amazon S3](https://aws.amazon.com/jp/premiumsupport/knowledge-center/s3-multipart-upload-cli/)
>
> Before uploading a file, you can use the file's MD5 checksum value as a reference for integrity checking after upload.
>
> ```
> aws s3 cp large_test_file s3://DOC-EXAMPLE-BUCKET/ --metadata md5="examplemd5value1234/4Q"
> ```
