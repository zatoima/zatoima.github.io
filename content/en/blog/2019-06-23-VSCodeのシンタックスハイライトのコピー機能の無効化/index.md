---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Disabling the Copy with Syntax Highlighting Feature in VSCode"
subtitle: ""
summary: " "
tags: ["VSCode","Tools"]
categories: ["VSCode","Tools"]
url: vscore-syntax-highlighting-disabled.html
date: 2019-06-23
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



## Introduction

------

I finally found the method to disable the copy with syntax highlighting feature, which I had asked about on teratail a few years ago and received no answers.

```
Visual Studio Code February 2017 | Unofficial - Visual Studio Code Docs https://vscode-doc-jp.github.io/updates/v1_10.html

Copy with syntax highlighting
Selected text is now copied to the clipboard with syntax highlighting applied.
This is very convenient when pasting content into another application (e.g., Outlook).
The content pasted into the application retains proper formatting and coloring.
```

> Visual Studio Code - How to disable the copy with syntax highlighting feature in VSCode | teratail https://teratail.com/questions/119990

```html
I'm using Visual Studio Code (Windows version).
Is there a way or setting to disable the following feature?

https://vscode-doc-jp.github.io/updates/v1_10.html
> Copy with syntax highlighting

When I copy and paste, the formatting information is also copied and it's causing problems.
I can work around it by pasting into Notepad first or using Ctrl+Shift+V, but
I'd like to know how to disable it in settings if possible.
```

## How to Configure

------

Select "File" - "Preferences" - "Settings", then uncheck `Editor: Copy With Syntax Highlighting`.

<img src="images/image-20191121172147714.png" alt="image-20191121172147714"  />

*If VSCode is an older version (e.g., 1.22), the above method may not work. If you cannot find the above setting, consider updating to the latest version first. This was tested with version 1.35.1. The reason teratail received no answers when I asked may be that the feature to disable syntax highlighting copying had not been implemented yet at that time.

## Reference

------

> Making plain text the default when copying in VSCode - Qiita https://qiita.com/kaityo256/articles/d39884c36bd5b35e6427
