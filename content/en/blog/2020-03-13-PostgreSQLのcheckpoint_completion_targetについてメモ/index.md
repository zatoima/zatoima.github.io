---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Notes on PostgreSQL's checkpoint_completion_target"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgresql-about-checkpoint_completion_target.html
date: 2020-03-13
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



Notes on PostgreSQL's `checkpoint_completion_target`.

> 19.5. Write Ahead Log https://www.postgresql.jp/document/10/html/runtime-config-wal.html#GUC-CHECKPOINT-TIMEOUT
>
> checkpoint_completion_target
>
> Specifies the target of checkpoint completion, as a fraction of total time between checkpoints. The default is 0.5. This parameter can only be set in the postgresql.conf file or on the server command line.

```sh
postgres=# show checkpoint_completion_target;
 checkpoint_completion_target
------------------------------
 0.5
(1 row)
```

On the other hand, there is a parameter called `checkpoint_timeout`, which is set to 5 minutes by default. This parameter allows you to specify the maximum interval between automatic WAL checkpoints in seconds.

`checkpoint_completion_target` works to distribute the load by spreading the checkpoint work over a "fraction" of the time set by `checkpoint_timeout`. It appears to be more of a guideline than a strict target.

```sh
postgres=# show checkpoint_timeout;
 checkpoint_timeout
--------------------
 5min
(1 row)
```

As per the defaults, when `checkpoint_timeout` is 5 minutes and `checkpoint_completion_target` is 0.5, it takes approximately 2.5 minutes (as a guideline) to write dirty pages to disk during a checkpoint.

In other words, lowering checkpoint_completion_target is expected to increase the load when writing dirty pages to disk during a checkpoint, while raising checkpoint_completion_target (= taking more time) increases the number of WAL files that need to be processed during crash recovery.

If there are many updates and checkpoint load is a concern, consider raising checkpoint_completion_target from the default 0.5 to a value between "0.6 and 0.9".
