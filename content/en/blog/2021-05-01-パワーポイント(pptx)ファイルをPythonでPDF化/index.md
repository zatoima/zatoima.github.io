---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Converting PowerPoint (pptx) Files to PDF with Python"
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

### Procedure

Performed on Windows.

1. Install required libraries

   ```python
   pip install comtypes
   ```

2. git clone

   ```python
   git clone https://github.com/matthewrenze/powerpoint-to-pdf.git
   ```

3. Place the pptx file you want to convert to PDF under the `powerpoint-to-pdf` folder

4. Run Python

   ```python
   python ConvertHere.py
   ```

### Notes

- Specify file: `Convert.py`
- Specify folder: `ConvertAll.py`
- All files in current directory: `ConvertHere.py` (the script used this time)

### Reference

from https://github.com/matthewrenze/powerpoint-to-pdf
