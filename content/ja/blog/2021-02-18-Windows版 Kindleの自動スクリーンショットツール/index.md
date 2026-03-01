---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Windows版 Kindleの自動スクリーンショットツール"
subtitle: ""
summary: " "
tags: ["Python","その他","メモ"]
categories: ["Python","その他","メモ"]
url: python-kindle-screenshot-get.html
date: 2021-02-15
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



このスクリーンショットは自分用に実施しましょう。

### 参考サイト

こちらのソースをベースに使いやすいように修正。

> 【Python】pyautoguiを使ってKindle書籍を自動でスクショするツールを作ってみた！ | 都会のエレキベア https://elekibear.com/20200225_01

### キャプチャする座標の取得

パソコンごとに座標は異なってくるので座標を取得する

```python
import pyautogui
import time

# 左上座標を取得
print('3秒以内にキャプチャ範囲の左上座標にマウスカーソルを合わせてください')
time.sleep(3)
print('左上座標：' + str(pyautogui.position()))

# １秒待機
time.sleep(1)

# 右下座標を取得
print('3秒以内にキャプチャ範囲の右下座標にマウスカーソルを合わせてください')
time.sleep(3)
print('右下座標：' + str(pyautogui.position()))

```

### Kindleのキャプチャ取得

```python
import pyautogui
import time
import os
import datetime

# ページ数
page = 600   #←変更必要
# スクショ間隔(秒)
span = 0.1
# 出力フォルダ頭文字
h_foldername = "output"
# 出力ファイル頭文字
h_filename = "picture"

# 取得範囲：左上座標
x1, y1 = 825, 105 #"キャプチャする座標の取得"を元に修正する
# 取得範囲：右下座様
x2, y2 = 1781, 989 #"キャプチャする座標の取得"を元に修正する

#5秒の間に、スクショしたいkindleの画面に移動
time.sleep(5)

# 出力フォルダ作成(フォルダ名：頭文字_年月日時分秒)
folder_name = h_foldername + "_" + str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
os.mkdir(folder_name)

# スクショ処理
for p in range(page):
    # 出力ファイル名(頭文字_連番.png)
    out_filename = h_filename + "_" + str(p+1).zfill(4) + '.png'
    # 画面全体のスクリーンショット
    s = pyautogui.screenshot(region=(x1, y1, x2-x1, y2-y1))
    # 出力パス： 出力フォルダ名 / 出力ファイル名
    s.save(folder_name + "/" + out_filename)
    # 次のページ
    pyautogui.keyDown('right')
    pyautogui.keyUp('right')
    # 画面の動作待ち
    time.sleep(span)

```

