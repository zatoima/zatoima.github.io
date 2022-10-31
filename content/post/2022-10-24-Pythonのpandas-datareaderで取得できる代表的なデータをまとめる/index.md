---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Pythonのpandas-datareaderで取得できる代表的なデータをまとめる"
subtitle: ""
summary: " "
tags: ["Python"]
categories: ["Python"]
url: python-pandas-datareader-data-from-fred
date: 2022-10-24
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

各種経済指標はここから取得ができる。代表的なものを抜き出す。

- [Categories of Economic Data \| FRED \| St\. Louis Fed](https://fred.stlouisfed.org/categories)

![image-20221024160438477](./image-20221024160438477.png)

```python
import pandas as pd
import datetime as dt
import pandas_datareader.data as pdr

start = dt.date(2006,1,1)
stop = dt.date(2022,1,1)

SYMBOLS=['DJIA','SP500','NIKKEI225','NASDAQ100','DGS10','GS10','T10Y3M','T10Y2Y','DFEDTARU','DFEDTARL','DFF','IRLTLT01JPM156N','PAYEMS','UNRATE','LRUN64TTJPM156S','A191RL1Q225SBEA','GDP','GDPC1','CPALTT01USM659N','ICSA','IPUTIL','JPNNGDP','EXPJP','IMPJP','XTEXVA01JPM667S','XTIMVA01JPM667S','DEXJPUS','DEXCHUS','DEXUSEU','DEXINUS']
df = pdr.DataReader(SYMBOLS, 'fred', start, stop)
```

![image-20221024160945278](./image-20221024160945278.png)

```python
import matplotlib.pyplot as plt
%matplotlib inline

plt.plot(df.index, df['EXPJP'],label='EXPJP')
plt.plot(df.index, df['IMPJP'],label='IMPJP')
plt.legend()
plt.show()
```

![image-20221024161118627](./image-20221024161118627.png)
