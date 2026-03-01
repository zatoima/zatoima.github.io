---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Python Script to Combine Multiple Image Files into a Single PDF"
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

### Install Library

```python
pip install img2pdf
```

### Script

The extension is specified as `png`, but it will work if changed to jpg.

```python
import os
import img2pdf
from PIL import Image

if __name__ == '__main__':
    print('Enter the target directory containing images to combine')
    img_Folder = input('>> ')

    # Check for trailing slash and add if missing
    if(img_Folder[-1:]!="\\"):
      img_Folder=img_Folder + '\\'
      print(img_Folder)

    pdf_FileName = img_Folder + 'output.pdf' # Name of the output PDF
    extension  = ".png"

    with open(pdf_FileName,"wb") as f:
        f.write(img2pdf.convert([Image.open(img_Folder+j).filename for j in os.listdir(img_Folder)if j.endswith(extension)]))
```
