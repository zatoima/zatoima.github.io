---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "パワーポイント(pptx)ファイルをPythonでPDF化"
subtitle: ""
summary: " "
tags: ["python","その他"]
categories: ["python","その他"]
url: python-pptx-to-pdf.html
date: 2021-05-01
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

### 手順

Windowsで実施。

1. 必要なライブラリをインストール

   ```python
   pip install comtypes
   ```

2. git clone

   ```python
   git clone https://github.com/matthewrenze/powerpoint-to-pdf.git
   ```

3. pdf化したいpptxファイルを`powerpoint-to-pdf`フォルダ配下に配置する

4. python 実行

   ```python
   python ConvertHere.py
   ```

### 補足

- ファイル指定：`Convert.py`
- フォルダ指定：`ConvertAll.py`
- カレントディレクトリ一式：`ConvertHere.py` （今回使用したスクリプト）

### 参考

from https://github.com/matthewrenze/powerpoint-to-pdf