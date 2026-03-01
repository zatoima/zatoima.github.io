---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "\"The number of cursors is limited to 10000\" When Making Column Selections of More Than 10000 Lines in VSCode"
subtitle: ""
summary: " "
tags: ["VSCode"]
categories: ["VSCode"]
url: vscode-eectangular-selection-cursol-error.html
date: 2019-04-14
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



### Introduction

VSCode is very handy, isn't it? I had been using Sublime Text 3 for a long time, but the "IMESupport" behavior on Windows 10 was causing various issues I couldn't tolerate, so I switched to VSCode.

I use VSCode not just for drafting emails and occasionally writing code, but also for viewing CSV files and various logs. When formatting logs or CSV files, I sometimes need to make column selections of more than 10,000 rows, and in VSCode, the following error message appears:

![image-20191121163717894](images/image-20191121163717894.png)

### Cause

As shown in the code below, "MAX_CURSOR_COUNT" is hardcoded, so column selections of more than 10,000 rows are not possible.

[[GitHub] Microsoft/vscode: Visual Studio Code](https://github.com/Microsoft/vscode/blob/17454d4e88886404af130639b979498b227a9167/src/vs/editor/common/controller/cursor.ts#L89)

```c
public static MAX_CURSOR_COUNT = 10000;
```

### Workaround

Based on my research online, there is no workaround. Use a different editor instead.

### Notes

I learned about this issue from an answer when I asked on teratail:

> Visual Studio Code - "The number of cursors is limited to 10000" appears when making column selections in VSCode | teratail https://teratail.com/questions/161064
