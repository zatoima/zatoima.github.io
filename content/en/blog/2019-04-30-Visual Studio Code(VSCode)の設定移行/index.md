---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Migrating Visual Studio Code (VSCode) Settings"
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



My work PC was having trouble and I did a clean install of Windows 10. I was devastated that I couldn't carry over the settings for various tools.

Here I will document how to migrate VSCode settings, which I look up every time.

There are other methods such as sharing configuration files via Dropbox or using the "Setting Sync" extension, but this method can be done with just file copying.

> Visual Studio Code の設定を共有・バックアップする - Qiita https://qiita.com/maromaro3721/items/b6d71a5e5d2d6433778a
>
> VSCode(Visual Studio Code)の設定を同期させる拡張機能「Setting Sync」が便利 | カレリエ https://www.karelie.net/vscode-setting-sync/

#### **Extensions**

Simply copy all subfolders stored in the following folder to the new environment.

```
C:\Users\username\.vscode\extensions

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

#### **VSCode Settings (Key Bindings and Other Settings)**

The settings are stored in settings.json, so just copy this file.

```
C:\Users\username\AppData\Roaming\Code\User
・settings.json
```
