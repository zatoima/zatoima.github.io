---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "改行コードの確認方法"
subtitle: ""
summary: " "
tags: ["Tips"]
categories: ["Tips"]
url: tips-mac-newline-character-confirm
date: 2022-12-09
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

#### 環境
```
xxxx@xxxx % sw_vers
ProductName:		macOS
ProductVersion:		13.0.1
BuildVersion:		22A400
```

不要なBOM（byte order mark）や改行コードの確認のために使用出来る。


#### 実行
```
xxxx@xxxx % od -c tpcds.sql
0000000    -   -       T   P   C   -   D   S       0   1  \n   w   i   t
0000020    h       c   u   s   t   o   m   e   r   _   t   o   t   a   l
0000040    _   r   e   t   u   r   n       a   s  \n   (   s   e   l   e
0000060    c   t       s   r   _   c   u   s   t   o   m   e   r   _   s
0000100    k       a   s       c   t   r   _   c   u   s   t   o   m   e
0000120    r   _   s   k  \n   ,   s   r   _   s   t   o   r   e   _   s
0000140    k       a   s       c   t   r   _   s   t   o   r   e   _   s
0000160    k  \n   ,   s   u   m   (   S   R   _   F   E   E   )       a
0000200    s       c   t   r   _   t   o   t   a   l   _   r   e   t   u
0000220    r   n  \n   f   r   o   m       s   t   o   r   e   _   r   e
0000240    t   u   r   n   s  \n   ,   d   a   t   e   _   d   i   m  \n
0000260    w   h   e   r   e       s   r   _   r   e   t   u   r   n   e
0000300    d   _   d   a   t   e   _   s   k       =       d   _   d   a
0000320    t   e   _   s   k  \n   a   n   d       d   _   y   e   a   r
0000340        =   2   0   0   0  \n   g   r   o   u   p       b   y
0000360    s   r   _   c   u   s   t   o   m   e   r   _   s   k  \n   ,
0000400    s   r   _   s   t   o   r   e   _   s   k   )  \n       s   e
0000420    l   e   c   t           c   _   c   u   s   t   o   m   e   r
0000440    _   i   d  \n   f   r   o   m       c   u   s   t   o   m   e
0000460    r   _   t   o   t   a   l   _   r   e   t   u   r   n       c
0000500    t   r   1  \n   ,   s   t   o   r   e  \n   ,   c   u   s   t
0000520    o   m   e   r  \n   w   h   e   r   e       c   t   r   1   .
0000540    c   t   r   _   t   o   t   a   l   _   r   e   t   u   r   n
0000560        >       (   s   e   l   e   c   t       a   v   g   (   c
0000600    t   r   _   t   o   t   a   l   _   r   e   t   u   r   n   )
0000620    *   1   .   2  \n   f   r   o   m       c   u   s   t   o   m
0000640    e   r   _   t   o   t   a   l   _   r   e   t   u   r   n
0000660    c   t   r   2  \n   w   h   e   r   e       c   t   r   1   .
0000700    c   t   r   _   s   t   o   r   e   _   s   k       =       c
0000720    t   r   2   .   c   t   r   _   s   t   o   r   e   _   s   k
0000740    )  \n   a   n   d       s   _   s   t   o   r   e   _   s   k
0000760        =       c   t   r   1   .   c   t   r   _   s   t   o   r
0001000    e   _   s   k  \n   a   n   d       s   _   s   t   a   t   e
0001020        =       '   N   M   '  \n   a   n   d       c   t   r   1
0001040    .   c   t   r   _   c   u   s   t   o   m   e   r   _   s   k
0001060        =       c   _   c   u   s   t   o   m   e   r   _   s   k
0001100   \n   o   r   d   e   r       b   y       c   _   c   u   s   t
0001120    o   m   e   r   _   i   d  \n   l   i   m   i   t       1   0
0001140    0   ;  \n  \n
0001144
```

