---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Displaying GitHub Contributions (Grass) on the Blog"
subtitle: ""
summary: " "
tags: ["blog","Github"]
categories: ["blog","Github"]
url: blog-github-contributions-list.html
date: 2020-01-19
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



I added GitHub contributions to the top page of the blog. Since I run this blog on GitHub Pages, every time I write a post, the "grass" grows. The motivation was both the visual appeal and a desire to track my activity.

The tool I used:

> GitHub の草状況を PNG 画像で返す heroku app をつくってみた - えいのうにっき https://blog.a-know.me/entry/2016/01/09/222210

##### 1.) Visit the Site

Go to the following URL:

> Grass-Graph / Imaging your GitHub Contributions Graph https://grass-graph.appspot.com/

<img src="image-20200109182025073.png" alt="image-20200109182025073" style="zoom:50%;" />

##### 2.) Enter Your GitHub ID

![image-20200109182101559](image-20200109182101559.png)

##### 3.) A Meta Tag Is Generated — Take Note of It

![image-20200109182132991](image-20200109182132991.png)

##### 4.) Add a Tag So That Clicking the Image Links to Your GitHub Profile

```html
<a href="https://github.com/zatoima" target="_blank">
  <img src="https://grass-graph.appspot.com/images/zatoima.png">
</a>
```

##### 5.) Paste This Tag into the Designated Area of Your Blog Service

I added it to the top page of the blog.

<img src="image-20200109181737393.png" alt="image-20200109181737393" style="zoom:50%;" />
