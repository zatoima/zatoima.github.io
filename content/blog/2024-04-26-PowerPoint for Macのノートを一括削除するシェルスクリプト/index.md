---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "PowerPoint for Macのノートを一括削除するシェルスクリプト"
subtitle: ""
summary: " "
tags: ["Mac"]
categories: ["Mac"]
url: mac-pptx-delete-note
date: 2024-04-26
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

PowerPointのプレゼンテーションファイル(*.pptx)には、各スライドにノートを追加することができる。 ただ、このノートを一括で削除する機能はMac版のPowerPoint本体には備わっていない（はず）。 今回は、シェルスクリプトを用いてこのノート削除を自動化してみる。

### シェルスクリプトの説明

このシェルスクリプト(`delete_note.sh`)は、以下のような処理を行う。

1. 一時ディレクトリを作成し、そのパスを`TMP_DIR`変数に格納する。

2. カレントディレクトリ内の全てのpptxファイルに対して、以下の処理を行う。

   1. `.pptx`ファイルを一時ディレクトリにコピーする。
   2. 一時ディレクトリ内で`.pptx`ファイルを解凍する。
   3. `./ppt/notesSlides/`ディレクトリ内の全ての`.xml`ファイルに対して、`<a:t>タグの内容を空にする。
   4. 解凍したファイルを再度`.pptx`ファイルにまとめる。
   5. 生成された`.pptx`ファイルを元のディレクトリにコピーする。

3. 一時ディレクトリを削除する。

   

### シェルスクリプト

```shell
#!/bin/bash

set -eu

TMP_DIR="$(mktemp -d)"
trap 'rm -rf $TMP_DIR' EXIT

for PPTX_FILE in *.pptx; do
    if [ -e "$PPTX_FILE" ]; then
        echo "Processing $PPTX_FILE..."
        
        cp "$PPTX_FILE" "$TMP_DIR"
        pushd "$TMP_DIR"
        
        unzip "$PPTX_FILE"
        rm "$PPTX_FILE"
        find "./ppt/notesSlides/"*.xml | xargs -I{} sed -i '' -e 's/<a:t>[^<]*<\/a:t>/<a:t><\/a:t>/g' "{}"
        zip -0 -r "$PPTX_FILE" ./* # do not compress (-0)
        
        popd
        
        cp "$TMP_DIR/$PPTX_FILE" "$PPTX_FILE"
    fi
done

```

### 前提：PPTXファイルの構造

PPTXファイルは、実際にはXMLファイルの集合体である。 具体的には、以下のような構造になっている。

- `_rels/`: リレーションシップを定義するXMLファイルを格納するディレクトリ。
- `docProps/`: ドキュメントのプロパティを定義するXMLファイルを格納するディレクトリ。
- `pptx` プレゼンテーションの本体を構成するXMLファイルを格納するディレクトリ。
  - `slides/`: 各スライドの情報を格納するXMLファイルを格納するディレクトリ。
  - `slideMasters/`: スライドマスターの情報を格納するXMLファイルを格納するディレクトリ。
  - `notesMasters/`: ノートマスターの情報を格納するXMLファイルを格納するディレクトリ。
  - `notesSlides/`: 各スライドのノートの情報を格納するXMLファイルを格納するディレクトリ。
  - `theme/`: テーマの情報を格納するXMLファイルを格納するディレクトリ。
- `_rels/`: リレーションシップを定義するXMLファイルを格納するディレクトリ。
- `[Content_Types].xml`: コンテンツタイプを定義するXMLファイル。

これらのXMLファイルが圧縮されたものが、PPTXファイルとなる。 つまり、PPTXファイルを編集するには、一度解凍してXMLファイルを修正し、再度圧縮する必要がある。この構造が知っていないとMac版のPPTを運用していく際は詰む。
