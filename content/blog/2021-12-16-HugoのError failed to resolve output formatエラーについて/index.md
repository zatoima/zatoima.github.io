---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Hugo AcademicのError failed to resolve output formatエラーについて"
subtitle: ""
summary: " "
tags: ["Hugo"]
categories: ["Hugo"]
url: hugo-error-build-output-format
date: 2021-12-16
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, Bot
---

Hugo Academicのエラーと対応の備忘。

### エラー

下記のエラーが出てビルド出来ない状態。

```sh
C:\hugo\zatoima.github.io>start http://localhost:1313/
C:\hugo\zatoima.github.io>hugo server
hugo: collected modules in 1055 ms
Error: from config: failed to resolve output format "headers" from site config
```

## 対応

`AppData\Local\Temp`配下に`hugo_cache`ディレクトリがあるのでそれを削除したら問題無くビルド出来るように。

### 参照先

https://wowchemy.com/docs/hugo-tutorials/troubleshooting/#error-file-not-found-or-failed-to-extract

> Error: failed to resolve output format
>
> Users report a commonly occurring [Hugo issue with the integrity of the modules cache](https://github.com/gohugoio/hugo/issues/8883#issuecomment-897832769). **Consider upvoting and commenting on the issue** to show the Hugo team that you are also affected.
>
> To resolve this Hugo issue, either:
>
> (A) Manually **delete Hugo’s default cache folder** and re-run Hugo. Hugo’s cache folder defaults to `$TMPDIR/hugo_cache/` on Mac/Linux and `%TMP%\hugo_cache\` on Windows.
>
> Or, (B) **Set a custom Hugo cache folder when you run Hugo**, for example: `hugo server --cacheDir ./cache/` where `./cache/` is the path of a temporary folder to create. Then you can easily locate and delete Hugo’s cache folder should you experience this issue.
>
> Note: usually `hugo mod clean --all` should delete Hugo’s cache, however, users report a Hugo bug running the command in this situation. You can provide your feedback on the [Hugo issues](https://github.com/gohugoio/hugo/issues/new?assignees=&labels=bug&template=bug_report.md).

日本語訳 by DeepL

> モジュールキャッシュの整合性に関して、Hugoでよく発生する問題がユーザーから報告されています。Hugo チームに自分も影響を受けていることを示すために、この問題に upvoting や commenting することを検討してください。
>
> この Hugo の問題を解決するには、以下のいずれかを行ってください。
>
> (A) Hugo のデフォルトのキャッシュフォルダを手動で削除し、Hugo を再実行します。Hugoのキャッシュフォルダのデフォルトは、Mac/Linuxでは$TMPDIR/hugo_cache/、Windowsでは%TMP%hugo_cacheです。
>
> あるいは、(B) Hugo を実行するときに、カスタム Hugo キャッシュフォルダを設定します。例えば、 hugo server --cacheDir ./cache/ ここで ./cache/ は作成する一時フォルダのパスとなります。そうすれば、この問題が発生したときに、Hugoのキャッシュフォルダを簡単に見つけて削除することができます。
