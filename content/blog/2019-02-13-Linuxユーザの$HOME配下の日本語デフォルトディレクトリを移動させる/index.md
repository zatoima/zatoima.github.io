---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Linuxユーザの$HOME配下の日本語デフォルトディレクトリを移動させる"
subtitle: ""
summary: " "
tags: ["Linux"]
categories: ["Linux"]
url: linux-home-directory-move.html
date: 2019-02-13
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



Oracle LinuxやCentOS、Red Hat OSを日本語環境でインストールした場合、ユーザの＄HOME配下に日本語ディレクトリが存在するが、使用しないディレクトリのため他ディレクトリに退避する。あと日本語表記から英語表記に変更する

・作業前のディレクトリ構成

```bash
[oracle]$ pwd
/home/oracle
[oracle]$ ls -l
合計 36
drwxr-xr-x. 2 oracle oinstall 4096  1月 24 11:34 2019 tmp
drwxr-xr-x. 2 oracle oinstall 4096  1月 24 11:33 2019 ダウンロード
drwxr-xr-x. 2 oracle oinstall 4096  1月 24 11:33 2019 テンプレート
drwxr-xr-x. 2 oracle oinstall 4096  1月 24 11:33 2019 デスクトップ
drwxr-xr-x. 2 oracle oinstall 4096  1月 24 11:33 2019 ドキュメント
drwxr-xr-x. 2 oracle oinstall 4096  1月 24 11:33 2019 ビデオ
drwxr-xr-x. 2 oracle oinstall 4096  1月 24 11:33 2019 音楽
drwxr-xr-x. 2 oracle oinstall 4096  1月 24 11:33 2019 画像
drwxr-xr-x. 2 oracle oinstall 4096  1月 24 11:33 2019 公開
[oracle]$

```

次に/.config/user-dirs.dirs の ファイルを修正。

```bash
vi/.config/user-dirs.dirs
```

・修正前

```
XDG_DESKTOP_DIR="$HOME/デスクトップ"
XDG_DOWNLOAD_DIR="$HOME/ダウンロード"
XDG_TEMPLATES_DIR="$HOME/テンプレート"
XDG_PUBLICSHARE_DIR="$HOME/公開"
XDG_DOCUMENTS_DIR="$HOME/ドキュメント"
XDG_MUSIC_DIR="$HOME/音楽"
XDG_PICTURES_DIR="$HOME/画像"
XDG_VIDEOS_DIR="$HOME/ビデオ"
```

・修正後

.Desktop配下に移動。このタイミングでディレクトリ名を日本語から英語に変更。

```
XDG_DESKTOP_DIR="$HOME/.Desktop"
XDG_DOWNLOAD_DIR="$HOME/.Desktop/Download"
XDG_TEMPLATES_DIR="$HOME/.Desktop/Templates"
XDG_PUBLICSHARE_DIR="$HOME/.Desktop/Publicshare"
XDG_DOCUMENTS_DIR="$HOME/.Desktop/Documents"
XDG_MUSIC_DIR="$HOME/.Desktop/Music"
XDG_PICTURES_DIR="$HOME/.Desktop/Pictures"
XDG_VIDEOS_DIR="$HOME/.Desktop/Videos"
```

新しい配置場所のディレクトリを作成。

```
mkdir -p $HOME/.Desktop
mkdir -p $HOME/.Desktop/Documents
mkdir -p $HOME/.Desktop/Download
mkdir -p $HOME/.Desktop/Templates
mkdir -p $HOME/.Desktop/Publicshare
mkdir -p $HOME/.Desktop/Music
mkdir -p $HOME/.Desktop/Pictures
mkdir -p $HOME/.Desktop/Videos
```

不要になったディレクトリを削除。

```
rm -rf "ダウンロード" "テンプレート" "デスクトップ" "ドキュメント" "ビデオ" "音楽" "画像" "公開"
```

ユーザでログアウトして再度ログインして完了。