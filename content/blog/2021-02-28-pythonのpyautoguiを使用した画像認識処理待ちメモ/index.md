---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "pythonのpyautoguiを使用した画像認識処理待ちメモ"
subtitle: ""
summary: " "
tags: ["python"]
categories: ["python"]
url: python-pyautogui-waiting-memo.html
date: 2021-02-28
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





画像認識をpyautoguiで実行させる場合で、どのように処理待ちをするかというメモ。当初は一定期間sleepさせる原始的な方法にしていたが、該当の画像がどのくらいで表示されるかが不明な場合、余裕を持ってsleepさせる必要があり、結果的に多くの時間が掛かっていた。

```python
time.sleep(15)
pos_check=pyautogui.locateOnScreen('対象の画像のパス', confidence=0.6)
pyautogui.click(pos_check)   
```

該当の画像が表示されるまで、ループを回しながらsleepさせるようにした。画像が見当たらない場合は、`ImageNotFoundException`が発生するので、そちらでスリープしてcontinueするように調整。

```python
import pyscreeze
from pyscreeze import ImageNotFoundException

～中略～

def click_from_imagename(imagename,confidence,message):
    for tryCount in range(30):
        #該当の画像が画面上に存在する場合の処理
        try:  
            if pyautogui.locateOnScreen(imagename, confidence=confidence):
                print('Execute：{0}'.format(message))
                pos_check=pyautogui.locateOnScreen(imagename, confidence=confidence)
                pyautogui.click(pos_check)
                time.sleep(1)
                print('Done：{0}'.format(message))
                break
        #該当の画像が画面上に存在しない場合の処理
        except pyautogui.ImageNotFoundException: 
            print('Waiting：{0}'.format(message))
            time.sleep(1)
            continue
～中略～
```

呼び出し時

```python
click_from_imagename("対象の画像のパス",0.6,"実行名")
```



