---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Visual Studio Code(VSCode)の設定移行"
subtitle: ""
summary: " "
tags: ["VSCode","Tools"]
categories: ["VSCode","Tools"]
url: vscode-setting-iko.html
date: 2019-04-30
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



社用のPCが調子悪くWindows10のクリーンインストールを行いました。各種ツールの設定を引き継ぐことが出来ずに絶望しています。

毎回調べるVSCodeの設定を引き継ぐ方法を記載します。

Dropbox等を使用した環境設定ファイルの共有方法や拡張機能の「Setting Sync」を使用した共有方法が別途ありますが、今回はファイルのコピーだけで実施可能な方法になります。

> Visual Studio Code の設定を共有・バックアップする - Qiita https://qiita.com/maromaro3721/items/b6d71a5e5d2d6433778a
>
> VSCode(Visual Studio Code)の設定を同期させる拡張機能「Setting Sync」が便利 | カレリエ https://www.karelie.net/vscode-setting-sync/

#### **拡張機能**

下記フォルダに格納されている全サブフォルダを新環境側にコピーして終わりです。

```
C:\Users\ユーザー名\.vscode\extensions

2019/04/06  15:47    <DIR>          .
2019/04/06  15:47    <DIR>          ..
2019/04/06  15:47    <DIR>          davidhouchin.whitespace-plus-0.0.5
2019/04/06  15:47    <DIR>          ms-mssql.mssql-1.5.0
2019/04/06  15:47    <DIR>          ms-vscode.sublime-keybindings-4.0.0
2019/04/06  15:47    <DIR>          sandcastle.whitespace-0.0.5
2019/04/06  15:47    <DIR>          sensourceinc.vscode-sql-beautify-0.0.4
2019/04/06  15:47    <DIR>          shakram02.bash-beautify-0.1.1
2019/04/06  15:47    <DIR>          shuworks.vscode-table-formatter-1.2.1
2019/04/06  15:47    <DIR>          xyz.plsql-language-1.7.0
```

#### **VSCodeの設定関連（キーバインドやその他設定等）**

settings.jsonに設定が記載されているのでこのファイルをコピーして終わりです。

```
C:\Users\ユーザー名\AppData\Roaming\Code\User
・settings.json
```