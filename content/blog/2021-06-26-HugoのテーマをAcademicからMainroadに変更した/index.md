---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "HugoのテーマをAcademicからMainroadに変更した"
subtitle: ""
summary: " "
tags: ["Hugo"]
categories: ["Hugo"]
url: hugo-academic-to-hugo-change
date: 2021-06-26
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

Academicの後継バージョンがよくわからなくなっていたので、[Mainroad](https://themes.gohugo.io/mainroad/)というテーマに変更した。

### 参考サイト

> - HUGOのテーマ「Mainroad」の設定方法を紹介 https://itsys-tech.com/list/hugo/007/
> - Hugo によるブログ作成と mainroad テーマのカスタマイズ - terashim.com https://terashim.com/posts/create-hugo-blog-and-customize-mainroad-theme/

また、今までは`Public`配下のみをGithubにpushしていたが、hugo配下を全てpushするようにした。GitHub Pagesの設定にもどこのディレクトリを公開するかを選べる。

![image-20210626203205785](image-20210626203205785.png)

### 今後やりたいこと

- 全文検索機能
  - メモとして使っているので、、。できればURLにキーワードを渡すことで検索結果が出るようにしたい
    - [Hugo + Lunrによる日本語全文検索](https://www.google.com/search?q=lunr+search+hugo&sxsrf=ALeKk03UBxgF3ejnSmCTTnu3OvNksm2R9g%3A1624707275802&ei=yxDXYM_IMM-ymAX4xYbYDQ&oq=lunr+search+hugo&gs_lcp=Cgdnd3Mtd2l6EAMyBAgAEB46CQgAELADEAcQHjoLCAAQsAMQBxAKEB46CAgAELADEMsBOgUIABDLAUoECEEYAVDeFFi1HWCQH2gBcAB4AIABxAGIAfIGkgEDMC42mAEAoAEBqgEHZ3dzLXdpesgBCMABAQ&sclient=gws-wiz&ved=0ahUKEwiP2qagmrXxAhVPGaYKHfiiAdsQ4dUDCA4&uact=5) が良さそう
- ブログ名が全部大文字になっているのをどうにかしたい
- Socialリンクを貼る
