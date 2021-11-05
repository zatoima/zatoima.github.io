---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Windows端末の処分前のディスク初期化、及び初期化の確認方法"
subtitle: ""
summary: " "
tags: ["その他"]
categories: ["その他"]
url: windows-delete-disk-confirm
date: 2021-11-05
featured: false
draft: false

---



自宅に3台くらいあったPC端末を処分及び売却する際にこの方法で初期化を行った、というまたいずれやってくる将来に向けたメモ。LinuxであればコマンドベースでできるけどもWindowsだと手っ取り早い方法を見つけきれなかったのでフリーソフトで実施した。

### ディスク消去

- [ディスク消去ユーティリティの詳細情報 : Vector ソフトを探す！](https://www.vector.co.jp/soft/winnt/util/se500811.html?utm_source=pocket_mylist)

米国家安全保障局(NSA)推奨方式をメディア全体に対して実施する。『乱数1→乱数2→ゼロ』の順に3回書き込みで削除

この方法に加えて、一応`cipher`コマンドでも削除しておいた

### ディスクの消去確認

- [EaseUS®製Windows用のデータ復元フリーソフト \- EaseUS Data Recovery Wizard Free](https://jp.easeus.com/data-recovery-software/drw-free.html?utm_source=pocket_mylist)

これは誤って消したファイルの復元ソフトで復元は有料だが、どのファイルを復元できるかについては無料でできるのでこちらで消去確認を行った。見事に何もファイルが表示されなくなったことを確認して売却及び処分！
