---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "ブログにGithubのcontributions（通称：草）を表示する"
subtitle: ""
summary: " "
tags: ["blog","Github"]
categories: ["blog","Github"]
url: blog-github-contributions-list.html
date: 2020-01-19
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



トップページにgithubのcontributionsが表示するようにした。github pagesでこのブログを運用しているのでブログを書いた場合に、この草が生えてくるという仕組み。

モチベーションと単純なかっこよさからトップページにgithubのcontributionsが表示するようにした。github pagesでこのブログを運用しているのでブログを書いた場合に、草が生えてくるという仕組み。

こちらのツールを使いました。

> GitHub の草状況を PNG 画像で返す heroku app をつくってみた - えいのうにっき https://blog.a-know.me/entry/2016/01/09/222210

##### 1.) アクセス

下記にアクセスする

> Grass-Graph / Imaging your GitHub Contributions Graph https://grass-graph.appspot.com/

<img src="image-20200109182025073.png" alt="image-20200109182025073" style="zoom:50%;" />

##### 2.) githubのidを入力する

![image-20200109182101559](image-20200109182101559.png)

##### 3.) メタタグが生成されるのでメモする

![image-20200109182132991](image-20200109182132991.png)

##### 4.) 画像をクリックした場合にgithubの自分のページに飛ぶようにタグを追加する。

```html
<a href="https://github.com/zatoima" target="_blank">
  <img src="https://grass-graph.appspot.com/images/zatoima.png">
</a>
```

##### 5.) このタグをブログサービスの指定の箇所に貼り付ける。

トップページに貼り付けてみた。

<img src="image-20200109181737393.png" alt="image-20200109181737393" style="zoom:50%;" />

