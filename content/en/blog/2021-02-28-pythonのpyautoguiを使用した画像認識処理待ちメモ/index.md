---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Notes on Waiting for Image Recognition Processing with Python pyautogui"
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



Notes on how to wait for processing when using pyautogui for image recognition. Initially I used a primitive method of sleeping for a fixed period, but when the time for the target image to appear is unknown, it's necessary to sleep with extra margin, resulting in a lot of wasted time overall.

```python
time.sleep(15)
pos_check=pyautogui.locateOnScreen('path/to/target/image', confidence=0.6)
pyautogui.click(pos_check)
```

I revised it to loop and sleep until the target image appears. When the image is not found, an `ImageNotFoundException` is raised, which is caught to sleep and continue.

```python
import pyscreeze
from pyscreeze import ImageNotFoundException

～omitted～

def click_from_imagename(imagename,confidence,message):
    for tryCount in range(30):
        # Processing when the target image exists on screen
        try:
            if pyautogui.locateOnScreen(imagename, confidence=confidence):
                print('Execute: {0}'.format(message))
                pos_check=pyautogui.locateOnScreen(imagename, confidence=confidence)
                pyautogui.click(pos_check)
                time.sleep(1)
                print('Done: {0}'.format(message))
                break
        # Processing when the target image does not exist on screen
        except pyautogui.ImageNotFoundException:
            print('Waiting: {0}'.format(message))
            time.sleep(1)
            continue
～omitted～
```

When calling:

```python
click_from_imagename("path/to/target/image", 0.6, "execution name")
```
