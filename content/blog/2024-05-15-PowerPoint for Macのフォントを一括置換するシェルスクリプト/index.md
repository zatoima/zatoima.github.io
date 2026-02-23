---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "PowerPoint for Macのフォントを一括置換するシェルスクリプト"
subtitle: ""
summary: " "
tags: ["Mac"]
categories: ["Mac"]
url: Mac-pptx-font-replace
date: 2024-05-15
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

## はじめに

MacのPPTのフォント置換がGUI上で動作しないケースが多々あるので下記２つの方法で一括置換を行っている。表の中のフォントなどは変わってくれないが、大部分は置き換わるはず。

## シェルスクリプトによるフォント置換

最初の方法は、シェルスクリプトを使用してフォントを置換する方法で、このスクリプトでは、以下の処理を行う。

1. 一時ディレクトリを作成し、.pptxファイルをコピーする
2. .pptxファイルを解凍する
3. ノート部分のテキストを削除する
4. スライドのXMLファイル内のフォント情報を置換する
5. 変更されたファイルを再度.pptxファイルにまとめる
6. 変更された.pptxファイルを元の場所にコピーする

このスクリプトを使用することで、カレントディレクトリ内の全ての.pptxファイルのフォントを一括で置換することができる。

```sh
#!/bin/bash

set -eu

TMP_DIR="$(mktemp -d)"
echo "Created temporary directory: $TMP_DIR"
trap 'rm -rf $TMP_DIR' EXIT

for PPTX_FILE in *.pptx; do
    if [ -e "$PPTX_FILE" ]; then
        echo "Processing $PPTX_FILE..."
        
        cp "$PPTX_FILE" "$TMP_DIR"
        echo "Copied $PPTX_FILE to temporary directory."
        
        pushd "$TMP_DIR"
        echo "Changed directory to temporary directory."
        
        unzip "$PPTX_FILE"
        echo "Unzipped $PPTX_FILE."
        
        rm "$PPTX_FILE"
        echo "Removed original $PPTX_FILE from temporary directory."
        
        # フォント修正
        find "./ppt/slides/"*.xml | xargs -I{} sed -i '' -e 's/typeface="[^"]*"/typeface="M PLUS 1p"/g' "{}"
        echo "Replaced typeface attributes with 'M PLUS 1p' in slide XML files."
        
        zip -0 -r "$PPTX_FILE" ./* # do not compress (-0)
        echo "Zipped modified files into $PPTX_FILE."
        
        popd
        echo "Returned to original directory."
        
        cp "$TMP_DIR/$PPTX_FILE" "$PPTX_FILE"
        echo "Copied modified $PPTX_FILE back to original location."
    else
        echo "File not found: $PPTX_FILE"
    fi
done

echo "Script execution completed."

```

## Pythonスクリプトによるフォント置換

次の方法は、Pythonスクリプトを使用してフォントを置換する方法である。このスクリプトでは、`python-pptx`ライブラリを使用して以下の処理を行う。

1. カレントディレクトリ内の.pptxファイルを検索する
2. 各.pptxファイル内で使用されているフォントを取得し、表示する
3. ユーザが指定した新しいフォントで全てのテキストのフォントを置換する
4. 変更された.pptxファイルを保存する

Pythonスクリプトを使用する場合、`python-pptx`ライブラリをインストールする必要がある。

```python
import os
from pptx import Presentation

def get_used_fonts(ppt_file):
    prs = Presentation(ppt_file)
    used_fonts = set()

    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        used_fonts.add(run.font.name)

            if shape.has_table:
                for row in shape.table.rows:
                    for cell in row.cells:
                        for paragraph in cell.text_frame.paragraphs:
                            for run in paragraph.runs:
                                used_fonts.add(run.font.name)

    return used_fonts

def replace_fonts(ppt_file, new_font):
    prs = Presentation(ppt_file)

    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        run.font.name = new_font

            if shape.has_table:
                table = shape.table

                for row in table.rows:
                    for cell in row.cells:
                        for paragraph in cell.text_frame.paragraphs:
                            for run in paragraph.runs:
                                run.font.name = new_font

    prs.save(ppt_file)

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    ppt_files = [f for f in os.listdir(current_dir) if f.endswith('.pptx')]

    if not ppt_files:
        print("No PowerPoint files found in the current directory.")
        return

    print("Found PowerPoint files:")
    for ppt_file in ppt_files:
        print(ppt_file)

        used_fonts = get_used_fonts(os.path.join(current_dir, ppt_file))
        print(f"Fonts used in {ppt_file}:")
        for font in used_fonts:
            print(f"- {font}")
        print()

    new_font = input("Enter the font name to replace all fonts with (default: 'M PLUS 1p'): ")
    if not new_font:
        new_font = 'M PLUS 1p'

    print(f"\nReplacing all fonts with '{new_font}' in all PowerPoint files...")
    for ppt_file in ppt_files:
        replace_fonts(os.path.join(current_dir, ppt_file), new_font)

    print("\nFont replacement completed.")

if __name__ == '__main__':
    main()

```

## スクリプトの実行方法

### シェルスクリプトの実行

1. スクリプトファイル（`replacefontppt.sh`）をカレントディレクトリに配置する

2. ターミナルを開き、カレントディレクトリに移動する

3. 以下のコマンドを実行してスクリプトを実行する

   ```sh
   ./replacefontppt.sh
   ```

### Pythonスクリプトの実行

ライブラリをインストールする

```sh
pip install python-pptx
```

1. スクリプトファイル（`replacefontppt.py`）をカレントディレクトリに配置する

2. ターミナルを開き、カレントディレクトリに移動する

3. 以下のコマンドを実行してスクリプトを実行する

   ```python
   python replacefontppt.py
   ```
