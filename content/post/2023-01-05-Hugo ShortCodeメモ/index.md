---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Hugo ShortCodeメモ"
subtitle: ""
summary: " "
tags: ["Hugo"]
categories: ["Hugo"]
url: hugo-blog-shortcode-memo
date: 2023-01-05
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



### Amazonの商品ページのshortcake

- [Hugoでわりと楽してわりとかっこよくAmazon商品紹介をする \- ゆーすけべー日記](https://yusukebe.com/posts/2020/amazon-shortcode/)

`.Site.Params.amazonJpAffiliate`となっている場合は`params`を定義した上で記載すれば良い。

```
baseURL = 'http://example.org/'
languageCode = 'en-us'
title = 'My New Hugo Site'
pygmentsUseClasses = true

[params]
  amazonJpAffiliate='zatoima'
```

↓のように使用する。

![image-20230102002952674](image-20230102002952674.png)

### 折りたたみ表示のshortcake

- [Hugo の shortcode で折りたたみ\(details タグ\)を使えるようにする – m1yam0t0\.com](https://m1yam0t0.com/posts/2022/09/use-details-in-hugo/)

↓のように使用する。

![image-20230102003042364](image-20230102003042364.png)

{{< details 具体的な設定例 >}} 

```
baseURL = 'http://example.org/'
languageCode = 'en-us'
title = 'My New Hugo Site'
pygmentsUseClasses = true

[params]
  amazonJpAffiliate='zatoima'
```

 {{< /details >}}

