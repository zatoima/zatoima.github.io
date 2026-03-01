---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Moving Japanese Default Directories Under Linux User's $HOME"
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



When installing Oracle Linux, CentOS, or Red Hat OS in a Japanese environment, Japanese-named directories exist under the user's $HOME. Since these directories are not used, we will relocate them to another directory and also rename them from Japanese to English.

- Directory structure before changes:

```bash
[oracle]$ pwd
/home/oracle
[oracle]$ ls -l
Total 36
drwxr-xr-x. 2 oracle oinstall 4096  Jan 24 11:34 2019 tmp
drwxr-xr-x. 2 oracle oinstall 4096  Jan 24 11:33 2019 Downloads
drwxr-xr-x. 2 oracle oinstall 4096  Jan 24 11:33 2019 Templates
drwxr-xr-x. 2 oracle oinstall 4096  Jan 24 11:33 2019 Desktop
drwxr-xr-x. 2 oracle oinstall 4096  Jan 24 11:33 2019 Documents
drwxr-xr-x. 2 oracle oinstall 4096  Jan 24 11:33 2019 Videos
drwxr-xr-x. 2 oracle oinstall 4096  Jan 24 11:33 2019 Music
drwxr-xr-x. 2 oracle oinstall 4096  Jan 24 11:33 2019 Pictures
drwxr-xr-x. 2 oracle oinstall 4096  Jan 24 11:33 2019 Public
[oracle]$

```

Next, edit the `~/.config/user-dirs.dirs` file.

```bash
vi/.config/user-dirs.dirs
```

- Before modification:

```
XDG_DESKTOP_DIR="$HOME/Desktop"
XDG_DOWNLOAD_DIR="$HOME/Downloads"
XDG_TEMPLATES_DIR="$HOME/Templates"
XDG_PUBLICSHARE_DIR="$HOME/Public"
XDG_DOCUMENTS_DIR="$HOME/Documents"
XDG_MUSIC_DIR="$HOME/Music"
XDG_PICTURES_DIR="$HOME/Pictures"
XDG_VIDEOS_DIR="$HOME/Videos"
```

- After modification:

Move to under .Desktop. At this point, also rename the directories from Japanese to English.

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

Create the new destination directories.

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

Delete the unnecessary directories.

```
rm -rf "ダウンロード" "テンプレート" "デスクトップ" "ドキュメント" "ビデオ" "音楽" "画像" "公開"
```

Log out of the user and log back in to complete.
