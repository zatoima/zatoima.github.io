---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "S3オブジェクトの整合性チェックをどのように行うのか"
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

下記の記事でも書いた通り、S3へマルチアップロードを行った際はMD5とEtagに差異が発生する。

> S3オブジェクトのmd5やEtagの関係性について整理する | my opinion is my own https://zatoima.github.io/aws-s3-object-md5-etag/

### アップロード時

下記記載の通り、AWS CLIで実行される。標準アップロードとマルチパートアップロードの両方でチェックサム検証を行うと記載ある

> https://docs.aws.amazon.com/cli/latest/topic/s3-faq.html
>
> ### Q: Does the AWS CLI validate checksums?
>
> The AWS CLI will perform checksum validation for uploading and downloading files in specific scenarios.
>
> #### Upload
>
> The AWS CLI will calculate and auto-populate the `Content-MD5` header for both standard and multipart uploads. If the checksum that S3 calculates does not match the `Content-MD5` provided, S3 will not store the object and instead will return an error message back the AWS CLI. The AWS CLI will retry this error up to 5 times before giving up. On the case that any files fail to transfer successfully to S3, the AWS CLI will exit with a non zero RC. See `aws help return-codes` for more information.
>
> ### Q: AWS CLI はチェックサムの検証を行いますか？
>
> AWS CLIは、特定のシナリオでファイルのアップロードとダウンロードのチェックサム検証を実行します。
>
> #### アップロード
>
> AWS CLI は、標準アップロードとマルチパートアップロードの両方で `Content-MD5` ヘッダを計算し、自動入力することができます。S3が計算したチェックサムが提供された`Content-MD5`と一致しない場合、S3はオブジェクトを保存せず、代わりにAWS CLIにエラーメッセージを返します。AWS CLIはこのエラーを5回までリトライして、あきらめる。S3へのファイル転送に失敗した場合、AWS CLIは0以外のRCで終了します。詳細は`aws help return-codes`を参照してください。

### ダウンロード時

下記の通り、特定条件で整合性チェックが出来ない旨、記載があるので注意が必要。

- オブジェクトがマルチパートアップロードでアップロードされた場合
- オブジェクトがKMSによるサーバーサイドの暗号化を使用してアップロードされた場合
- 顧客が提供した暗号化キーを使用してオブジェクトをアップロードした場合

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
>
> ダウンロード
> AWS CLIがS3からオブジェクトをダウンロードするたびに実行されるGetObjectリクエストから返されるETagヘッダーに基づいて、可能な場合はダウンロードのチェックサムを確認しようとします。計算されたMD5チェックサムが期待されるチェックサムと一致しない場合、ファイルは削除され、ダウンロードが再試行される。この処理は最大3回まで再試行される。ダウンロードに失敗した場合、AWS CLI は 0 以外の RC で終了する。詳細については、aws help return-codesを参照。
>
> CLIがダウンロードのチェックサムを検証できない条件がいくつかある。
>
> オブジェクトがマルチパートアップロードでアップロードされた場合
> オブジェクトがKMSによるサーバーサイドの暗号化を使用してアップロードされた場合
> 顧客が提供した暗号化キーを使用してオブジェクトをアップロードした場合
> オブジェクトが範囲 GetObject リクエストを使用してダウンロードされた場合

では、特定条件（マルチアップロード時やKMS暗号化している場合等）で整合性チェックが出来ない際にどうすれば良いのかというと、「ファイルをアップロードする前に、 ファイルの MD5 チェックサム値をアップロード後の整合性チェックの参照として使用することができます。」と書いてある通り、metadataを付与してダウンロード後にmd5値を確認するということになる。（実質的に整合性チェックツール等を作ることになる模様）

> [Amazon S3 へのマルチパートアップロードに AWS CLI を使用する](https://aws.amazon.com/jp/premiumsupport/knowledge-center/s3-multipart-upload-cli/)
>
> ファイルをアップロードする前に、 ファイルの MD5 チェックサム値をアップロード後の整合性チェックの参照として使用することができます。
>
> ```
> aws s3 cp large_test_file s3://DOC-EXAMPLE-BUCKET/ --metadata md5="examplemd5value1234/4Q"
> ```



