---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "PythonのPyArrorwを使用してCSVをParquetに変換、及び確認"
subtitle: ""
summary: " "
tags: ["Python"]
categories: ["Python"]
url: python-pyarrow-convert-csv-to-parquet-pandas
date: 2021-11-03
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



pandasでparquetを扱えることを知った

### テスト用CSVの作成

```
cat << EOF > testdata.csv
1,test1,ゎぶばあちあぬナクバ
2,test2,がマうひバぴじクハぺ
3,test3,スみでてゥあッあけげ
EOF
```

### pyarrowのインストール

```
pip install pyarrow
```

### csvからparquetへの変換

```
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

#csvからparquetへの変換
df = pd.read_csv('./testdata.csv')
table = pa.Table.from_pandas(df)
pq.write_table(table, './testdata.parquet')
```

### parquetの内容確認

```
#parquetの内容確認
load_df_pq = pd.read_parquet("./testdata.parquet")
print(load_df_pq.info())
print(load_df_pq)
```

AWSのs3 selectでもParquetを簡単に見れて便利

![image-20211019134446831](image-20211019134446831.png)

![image-20211019134457434](image-20211019134457434.png)