---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Building a Static Site with Pelican on Github Pages"
subtitle: ""
summary: " "
tags: ["Blog","Pelican"]
categories: ["Blog","Pelican"]
url: pelican-blog-implement.html
date: 2019-11-23
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


#### **What Is a Static Site?**

***

A mechanism for placing static files on Github Pages or S3 and making them publicly accessible. There are many static site generators, but I used Pelican for this. I chose Pelican because it's a framework built with Python. The setup itself was easy. (Since changes are made basically through the CUI or by modifying configuration files, it takes some time to get used to.)

Static site generators commonly seen on Japanese websites include Hugo and Hexo. There are various types, so check this link too.

<br/>

[StaticGen | Top Open Source Static Site Generators](https://www.staticgen.com/)

<br/>

#### **Prerequisites**

***

- git installed

- Python installed

- Windows10

  <br/>

#### **Installing Pelican**

***

Create a Python virtual environment with virtualenv to avoid polluting the environment.

```bash
cd C:\
virtualenv pelican
cd pelican
Scripts\activate
```

Install pelican and markdown with pip.

```python
pip install pelican
pip install Markdown
```

Pelican 4.2 is installed.

```
(pelican) C:\pelican>pelican --version
4.2.0
```

<br/>

#### Create Blog Template

***

Running the pelican-quickstart command asks various questions interactively.

```sh
pelican-quickstart

> Where do you want to create your new web site? [.]
> What will be the title of this web site? zatolog
> Who will be the author of this web site? zato
> What will be the default language of this web site? [en] ja
> Do you want to specify a URL prefix? e.g., http://example.com   (Y/n) Y
> What is your URL prefix? (see above example; no trailing slash) http://zatoima.github.io
> Do you want to enable article pagination? (Y/n) Y
> How many articles per page do you want? [10] 5
> What is your time zone? [Europe/Paris] Asia/Tokyo
> Do you want to generate a Fabfile/Makefile to automate generation and publishing? (Y/n) Y
> Do you want an auto-reload & simpleHTTP script to assist with theme and site development? (Y/n) Y
> Do you want to upload your website using FTP? (y/N) N
> Do you want to upload your website using SSH? (y/N) N
> Do you want to upload your website using Dropbox? (y/N) N
> Do you want to upload your website using S3? (y/N) N
> Do you want to upload your website using Rackspace Cloud Files? (y/N) N
> Do you want to upload your website using GitHub Pages? (y/N) y
> Is this your personal page (username.github.io)? (y/N) y
Done.
```

#### Create Articles in Markdown Format

***

Create an appropriate file and save it under the `content` folder.

```markdown
Title: My First Review
Date: 2010-12-03 10:20
Category: Review
Slug: pelican-my-first-review

Following is a review of my favorite mechanical keyboard.
```

"Title", "Date", "Category", and "Slug" are the article metadata. Slug becomes the URL name (HTML name) of the page.


#### Additional Steps for Windows

***

Normally static pages can be easily generated with the `make` command, but this doesn't work on Windows, so use batch files. Download the bat file from below and place it directly under the folder where Pelican is installed. (`C:\pelican`)

>  [https://gist.github.com/traeblain/4252511](https://gist.github.com/traeblain/4252511)

Some modifications are needed.


##### Before Modification

```
set _PELICAN=$pelican
set _PELICANOPTS=$pelicanopts
.
.
cd %_OUTPUTDIR% && python -m SimpleHTTPServer
```


##### After Modification

```
set _PELICAN=pelican
set _PELICANOPTS=
.
.
cd %_OUTPUTDIR% && python -m http.server
```

*By default, "http.server" uses port 8000. If another service is using port 8000, it will error, so change it to use another port as needed.*


```
cd %_OUTPUTDIR% && python -m http.server 8080
```


#### Creating HTML Files

Run the pmake html command to create HTML files from markdown, and run the pmake serve command to start a server on localhost where you can check the created articles locally.

```
pmake html
pmake serve
```


##### Access URL

>  [http://localhost:8000](http://localhost:8000)


#### Publishing to Github

***

You can upload all files under the Pelican folder to Github Pages, but there are many unnecessary files. Using ghp-import makes the specified directory into a gh-pages branch. In the following, the "output" folder becomes the gh-pages branch, and only the contents of the "output" folder are pushed.

<br/>

```sh
cd C:\pelican
Scripts\Activate
pip install ghp-import

pmake html
pmake publish
ghp-import output
git commit -m "Update Post"
git push https://github.com/zatoima/zatoima.github.io.git gh-pages:master
```

<br/>

After git push, wait a few minutes and access your own GitHub Pages. *Note: the page below is after theme change.*

<img src="images/image-20191121232046244.png" alt="image-20191121232046244" style="zoom:50%;" />


#### Changing Pelican Themes

***

Changing themes is very easy. However, since configurable settings differ by theme, once you advance customization, switching to another theme becomes difficult. (Probably the same for any blog service.)

Clone all official Pelican themes:

```bash
git clone --recursive https://github.com/getpelican/pelican-themes ~/pelican-themes
```

Modify the THEME variable in `pelicanconf.py`:

```sh
THEME = 'pelican-themes\\pelican-bootstrap3'
```


#### How to Install Plugins

***

Clone all official Pelican plugins:

```bash
git clone --recursive https://github.com/getpelican/pelican-plugins.git pelican-plugins
```

Modify the PLUGIN_PATHS and PLUGINS variables in `pelicanconf.py`. Specify the directory cloned above for PLUGIN_PATHS:

```sh
PLUGIN_PATHS = ['pelican-plugins']

PLUGINS = ['i18n_subsites','tag_cloud','sitemap','series']
```

#### Appendix

***

I checked the web page display performance with WebPageTest. Seems like it could even beat Hiroshi Abe's site.

> WebPageTest - Website Performance and Optimization Test [https://www.webpagetest.org/](https://www.webpagetest.org/)

<img src="image-20191123195128918.png" alt="image-20191123195128918" style="zoom: 50%;" />

<img src="image-20191123195145038.png" alt="image-20191123195145038" style="zoom:50%;" />
