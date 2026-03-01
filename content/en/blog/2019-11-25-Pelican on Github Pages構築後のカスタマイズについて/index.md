---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Customizing Pelican After Building on Github Pages"
subtitle: ""
summary: " "
tags: ["Blog","Pelican"]
categories: ["Blog","Pelican"]
url: pelican-customize-setting.html
date: 2019-11-25
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

#### **Introduction**

***

After setting up Pelican, I did these 5 things, so I'm organizing them here as a reference.

1. Configuring pelican-bootstrap3

2. Setting up Google Analytics

3. Setting the site favicon

4. Customizing pelicanconf.py

5. Search engine optimization

   <br/>

#### **1. Configuring pelican-bootstrap3**

***

pelican-bootstrap3 is a theme with this kind of design.

<img src="screenshot-article.png" alt="screenshot-article.png" style="zoom: 33%;" />

Clone all official Pelican themes:

```bash
git clone --recursive https://github.com/getpelican/pelican-themes ~/pelican-themes
```

Modify the THEME variable in `pelicanconf.py`:

```sh
THEME = 'pelican-themes\\pelican-bootstrap3'
```

For pelican-bootstrap3, the following setting is also required. It was not needed for other themes.

```python
JINJA_ENVIRONMENT = {
    'extensions': ['jinja2.ext.i18n'],
}
```

<br/>

#### **2. Setting Up Google Analytics**

***

There are many resources online about how to configure Google Analytics itself, so I'll skip that here.

Setting up Google Analytics in Pelican is very easy. The production configuration file `publishconf.py` already has a variable for Google Analytics, so simply set your "UA-XXXXXX" there and you're done.

```
GOOGLE_ANALYTICS = "UA-********-*"
GOOGLE_ANALYTICS_SITEID = "auto"
```

<br/>

#### **3. Setting Up the Favicon**

***

When using pelican-bootstrap3, simply place your ico file in advance and add the following setting to the configuration file (`pelicanconf.py`).

```
# for favicon setting
FAVICON = 'images/favicon.ico'
```

Since this is often theme-dependent, the following articles may be helpful for other cases:

> Tips n Tricks · getpelican/pelican Wiki [https://github.com/getpelican/pelican/wiki/Tips-n-Tricks](https://github.com/getpelican/pelican/wiki/Tips-n-Tricks)
>
> [Python] Setting a favicon for a Pelican site - dackdive's blog [https://dackdive.hateblo.jp/entry/2016/01/12/101200](https://dackdive.hateblo.jp/entry/2016/01/12/101200)

<br/>

#### **4. Customizing pelicanconf.py**

***

#### Customizations for pelican-bootstrap3

These depend on the pelican-bootstrap3 theme, so they won't work with other themes.

Reference URL: [https://github.com/getpelican/pelican-themes/tree/master/pelican-bootstrap3](https://github.com/getpelican/pelican-themes/tree/master/pelican-bootstrap3)

```python
# customize for pelican-bootstrap3 2019.11.17
# Whether to show category in articles
SHOW_ARTICLE_CATEGORY=True

# breadcrumbs - whether to show breadcrumb navigation
DISPLAY_BREADCRUMBS=True
DISPLAY_CATEGORY_IN_BREADCRUMBS=True

# Whether to show Date, Category, and Tags in article list
DISPLAY_ARTICLE_INFO_ON_INDEX=True

# Customizations for banner image
#BANNER = 'images/banner.jpg'
#BANNER_ALL_PAGES = True

# Category
DISPLAY_CATEGORIES_ON_SIDEBAR=True

# Tags
DISPLAY_TAGS_ON_SIDEBAR=True

# Recent posts display (default shows 5 articles)
DISPLAY_RECENT_POSTS_ON_SIDEBAR=True
```

#### Other Global Settings

```python
# cjk_spacing: Inserts spaces between Chinese/Japanese/Korean and English words in Markdown documents
# markdown_cjk_spacing/README-ja.md at master · EloiseSeverin/markdown_cjk_spacing https://github.com/EloiseSeverin/markdown_cjk_spacing/blob/master/README-ja.md
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
        'markdown.extensions.nl2br': {},
        'markdown_cjk_spacing.cjk_spacing': {},
    },
    'output_format': 'html5',
}

# add for date format 2019.11.17
DATE_FORMATS = {
    'en': '%a, %d %b %Y',
    'ja': '%Y-%m-%d(%a)',
}

DEFAULT_LANG = 'Ja'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DEFAULT_PAGINATION = 5

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

```

<br/>

#### **5. Search Engine Optimization**

***

Unlike Hatena Blog, Github Pages cannot be expected to perform well with SEO on its own, so you need to submit your URL or domain directly to the search engines. Register the URL you just created with both Google and Bing using the links below:

- [Google Search Console](https://search.google.com/search-console)
- [Bing Webmaster Tools](https://www.bing.com/toolbox/webmaster/)

<br/>
