---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Anaconda環境にsnowflake-connector-pythonをインストール"
subtitle: ""
summary: " "
tags: ["Snowflake"]
categories: ["Snowflake"]
url: snowflake-anaconda-snowflake-conector-python-install
date: 2022-12-15
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


### 参考URL：

- [Snowflake Connector Python :: Anaconda\.org](https://anaconda.org/conda-forge/snowflake-connector-python)
- [conda\-forge/snowflake\-connector\-python\-feedstock: A conda\-smithy repository for snowflake\-connector\-python\.](https://github.com/conda-forge/snowflake-connector-python-feedstock)

### インストール

pipであれば素直に`pip install snowflake-connector-python`で良いが、snowflake-connector-pythonがAnacondaのリポジトリにないのでconda-forgeを指定する必要あり。
```sh
conda install -c conda-forge snowflake-connector-python
```

### ハマったこと
このときエラーで`Solving environment`で先に進まなかったので下記記事を見てconda環境をアップデートした。

```sh
(base) jimazato@xxxxxxx AWS-Tokyo % conda install snowflake-connector-python
Collecting package metadata (current_repodata.json): done
Solving environment: failed with initial frozen solve. Retrying with flexible solve.
Solving environment: failed with repodata from current_repodata.json, will retry with next repodata source.
Collecting package metadata (repodata.json): /
\
|
\
```

> [conda updateで「Solving environment: failed」となった時の解決法 \- Qiita](https://qiita.com/jordi/items/cd974b668e7ecf312543)

```sh
conda install anaconda
conda update --all
```
