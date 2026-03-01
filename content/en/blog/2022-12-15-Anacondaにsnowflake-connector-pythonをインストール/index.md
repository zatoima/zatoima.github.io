---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Installing snowflake-connector-python in Anaconda Environment"
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

### Reference URLs:

- [Snowflake Connector Python :: Anaconda\.org](https://anaconda.org/conda-forge/snowflake-connector-python)
- [conda\-forge/snowflake\-connector\-python\-feedstock: A conda\-smithy repository for snowflake\-connector\-python\.](https://github.com/conda-forge/snowflake-connector-python-feedstock)

### Installation

With pip, you can simply use `pip install snowflake-connector-python`, but since snowflake-connector-python is not in the Anaconda repository, you need to specify conda-forge.
```sh
conda install -c conda-forge snowflake-connector-python
```

### Trouble Encountered
Got an error where `Solving environment` would not proceed, so I updated the conda environment as described in the article below.

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

> [Solution for "Solving environment: failed" with conda update - Qiita](https://qiita.com/jordi/items/cd974b668e7ecf312543)

```sh
conda install anaconda
conda update --all
```
