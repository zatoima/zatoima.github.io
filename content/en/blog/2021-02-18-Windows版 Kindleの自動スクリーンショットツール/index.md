---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Automated Screenshot Tool for Kindle on Windows"
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



Use these screenshots for personal use only.

### Reference Sites

Based on the following source, modified for easier use.

> [Python] Creating a tool to automatically take screenshots of Kindle books using pyautogui | Urban ElekiBear https://elekibear.com/20200225_01

### Getting the Capture Coordinates

Coordinates vary by computer, so get them first.

```python
import pyautogui
import time

# Get top-left coordinates
print('Move the mouse cursor to the top-left of the capture area within 3 seconds')
time.sleep(3)
print('Top-left coordinates: ' + str(pyautogui.position()))

# Wait 1 second
time.sleep(1)

# Get bottom-right coordinates
print('Move the mouse cursor to the bottom-right of the capture area within 3 seconds')
time.sleep(3)
print('Bottom-right coordinates: ' + str(pyautogui.position()))

```

### Taking Kindle Screenshots

```python
import pyautogui
import time
import os
import datetime

# Number of pages
page = 600   # <- Change as needed
# Screenshot interval (seconds)
span = 0.1
# Output folder prefix
h_foldername = "output"
# Output file prefix
h_filename = "picture"

# Capture area: top-left coordinates
x1, y1 = 825, 105  # Modify based on "Getting the Capture Coordinates"
# Capture area: bottom-right coordinates
x2, y2 = 1781, 989  # Modify based on "Getting the Capture Coordinates"

# Move to the Kindle screen you want to screenshot within 5 seconds
time.sleep(5)

# Create output folder (folder name: prefix_YYYYMMDDHHmmss)
folder_name = h_foldername + "_" + str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
os.mkdir(folder_name)

# Screenshot process
for p in range(page):
    # Output filename (prefix_sequence.png)
    out_filename = h_filename + "_" + str(p+1).zfill(4) + '.png'
    # Full screen screenshot
    s = pyautogui.screenshot(region=(x1, y1, x2-x1, y2-y1))
    # Output path: output folder / output filename
    s.save(folder_name + "/" + out_filename)
    # Next page
    pyautogui.keyDown('right')
    pyautogui.keyUp('right')
    # Wait for screen action
    time.sleep(span)

```
