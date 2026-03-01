---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Githubの.gitignoreとgit-secrets設定"
subtitle: ""
summary: " "
tags: ["Github"]
categories: ["Github"]
url: github-gitignore-git-secrets-setting
date: 2022-12-28
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


### AWSアクセスキーを誤ってコミットしないための設定
https://kakakakakku.hatenablog.com/entry/2017/02/06/100706

```sh
cd /Users/jimazato/work/hugo/zatoima.github.io
brew install git-secrets
git secrets --install
git secrets --register-aws
git config -l | grep secrets
```

### AWSのアカウント番号等も追加

アカウント番号は一意となってしまうので誤ってPushしないように設定する。

```sh
git secrets --add 'XXXXXXXX'
git config -l | grep secrets
```

### .gitignoreへの追加
 - [ぼくのかんがえたさいきょうの \.gitignore \- Qiita](https://qiita.com/wnoguchi/items/18f407ff566dc136fef9)

```sh
cat << EOF > .gitignore

# Project Specific rules here

# Temporary Files
#---------------------------
# vim
[._]*.s[a-w][a-z]
[._]s[a-w][a-z]
*.un~
Session.vim
.netrwhist
# Emacs
.\#*
# Backup files
#---------------------------
*~
*.orig
*.bak
# yyyyMMdd
*.[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]
# yyyyMMddHHmm
*.[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]
# yyyyMMddHHmmss
*.[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]
# OS dependent files
#---------------------------
.DS_Store
Thumbs.db
# Bundler specific
#---------------------------
/vendor/bundle/
/.bundle/
# Office specific
~$*
*.tmp
# Vagrant specific
.vagrant/

EOF

```


