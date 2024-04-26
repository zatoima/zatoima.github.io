---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "複数の画像ファイルを一つのPDFにするPythonスクリプト"
subtitle: ""
summary: " "
tags: ["python"]
categories: ["python"]
url: python-multiple-img-to-pdf
date: 2021-07-09
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

### ライブラリのインストール

```python
pip install img2pdf
```

### スクリプト

拡張子を`png`で指定しているが、jpgに変えれば動く。

```python
import os
import img2pdf
from PIL import Image

if __name__ == '__main__':
    print('画像を結合したい対象ディレクトリを入力してください')
    img_Folder = input('>> ')

    #末尾のスラッシュ有無を確認し、スラッシュを付与
    if(img_Folder[-1:]!="\\"):
      img_Folder=img_Folder + '\\'
      print(img_Folder)

    pdf_FileName = img_Folder + 'output.pdf' # 出力するPDFの名前
    extension  = ".png"

    with open(pdf_FileName,"wb") as f:
        f.write(img2pdf.convert([Image.open(img_Folder+j).filename for j in os.listdir(img_Folder)if j.endswith(extension)]))
```



