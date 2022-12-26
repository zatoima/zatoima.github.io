---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "LambdaをVPCで使用する際のENI数"
subtitle: ""
summary: " "
tags: ["AWS","Lambda"]
categories: ["AWS","Lambda"]
url: aws-lamdba-vpc-eni-number-use
date: 2022-07-24
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





> [発表] Lambda 関数が VPC 環境で改善されます | Amazon Web Services ブログ https://aws.amazon.com/jp/blogs/news/announcing-improved-vpc-networking-for-aws-lambda-functions/



以前：

![img](https://d2908q01vomqb2.cloudfront.net/b3f0c7f6bb763af1be91d9e74eabfeb199dc1f1f/2019/09/04/many-enis-1024x616.png)

今：

![img](https://d2908q01vomqb2.cloudfront.net/b3f0c7f6bb763af1be91d9e74eabfeb199dc1f1f/2019/09/04/v2n-architecture-1024x613.png)



> https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/foundation-networking.html?utm_source=pocket_mylist
>
> ### ENI の管理
>
> Lambda は、関数実行ロールのアクセス許可を使用して、ネットワークインターフェイスを作成および管理します。アカウントで VPC 対応関数に一意のサブネットとセキュリティグループの組み合わせを定義すると、Lambda は Hyperplane ENI を作成します。Lambda は、同じサブネットとセキュリティグループの組み合わせを使用するアカウントの他の VPC 対応関数に Hyperplane ENI を再利用します。
>
> 同じ Hyperplane ENI を使用できる Lambda 関数の数にクォータはありません。ただし、各 Hyperplane ENI は最大 65,000 個の接続/ポートをサポートします。接続数が 65,000 を超えると、Lambda は新しい Hyperplane ENI を作成して、追加の接続を提供します。
>
> 関数設定を更新して別の VPC にアクセスすると、Lambda は以前の VPC の Hyperplane ENI への接続を終了します。新しい VPC への接続を更新するプロセスには、数分かかる場合があります。この間、関数への呼び出しは以前の VPC を使用し続けます。更新が完了すると、新しい VPC で Hyperplane ENI を使用して新しい呼び出しが開始されます。この時点で、Lambda 関数は以前の VPC に接続されなくなります。
