---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "VSCodeで10000行以上の矩形選択を行った場合に「カーソルの数は10000個に制限されています」が出力される"
subtitle: ""
summary: " "
tags: ["VSCode"]
categories: ["VSCode"]
url: vscode-eectangular-selection-cursol-error.html
date: 2019-04-14
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



### はじめに

VSCode使いやすいですよね。長らくSublime text3を使用していましたが、Windows10の「IMESupport」の動作が色々と耐えられなかったのでVSCodeに乗り換えました。

VSCodeはメールの下書きを作成するようのテキストエディタ（たまにコードも書く）だけではなくCSVや各種ログを参照するのにも使っています。ログやCSVを整形する時に1万行以上の矩形選択をすることもあるのですが、VSCodeの場合は下記エラーメッセージが出力されます。

![image-20191121163717894](images/image-20191121163717894.png)

### 原因

下記のコードのように"MAX_CURSOR_COUNT"でハードコーディングされているため1万行以上の矩形選択は出来ない模様です。

[[GitHub\]Microsoft/vscode: Visual Studio Code](https://github.com/Microsoft/vscode/blob/17454d4e88886404af130639b979498b227a9167/src/vs/editor/common/controller/cursor.ts#L89)

```c
public static MAX_CURSOR_COUNT = 10000;
```

### 回避策

ネット上で調査する限り回避策はありませんでした。他のエディタを使いましょう。

### 備考

本件はteratailで質問した際の回答で教えて頂きました。

> Visual Studio Code - vscodeの矩形選択で「カーソルの数は 10000 個に制限されています。」が出力される｜teratail https://teratail.com/questions/161064