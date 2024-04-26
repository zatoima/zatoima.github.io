---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "VSCodeでデフォルトのシンタックスハイライトを設定する"
subtitle: ""
summary: " "
tags: ["VSCode"]
categories: ["VSCode"]
url: other-vscode-syntax-default
date: 2021-11-22
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, Bott
---



下の画像のようなプレーンテキストとか拡張子がついていないファイルに対してシンタックスを自動で設定したい。（下記の記事の通り、言語の自動検出機能が実装されていたりするので必要性は少なくなってきたけども。）

- [VS Code に言語の自動検出機能が追加されました \| DevelopersIO](https://dev.classmethod.jp/articles/vscode-automatic-language-detection/)

![image-20211109115640510](image-20211109115640510.png)

「ユーザ設定」 - 「設定」でDefalut Languageを検索。ここで言語モードを設定する

![image-20211109115655252](image-20211109115655252.png)

これで新規ファイルを作ったときに自動的に選択した言語がハイライトされる。

![image-20211109115708976](image-20211109115708976.png)