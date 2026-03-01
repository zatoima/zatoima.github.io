---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "How to Clear the Buffer Cache in PostgreSQL"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgresql-buffercache-clear.html
date: 2020-04-24
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



PostgreSQL does not have a built-in method to clear the buffer cache like Oracle does, so the only option is to clear the OS-level filesystem cache. Therefore, the title "clearing the buffer cache in PostgreSQL" is not quite accurate — what this actually does is clear the OS-level cache.

```sql
pg_ctl stop
sudo su - -c "echo 3 > /proc/sys/vm/drop_caches"
pg_ctl start
```

### Reference

[pgsql-jp: 40643] Re: Question about how to clear PostgreSQL cache https://ml.postgresql.jp/pipermail/pgsql-jp/2010-December/015599.html
