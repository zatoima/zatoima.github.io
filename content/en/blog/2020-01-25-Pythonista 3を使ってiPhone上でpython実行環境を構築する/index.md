---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Building a Python Execution Environment on iPhone Using Pythonista 3"
subtitle: ""
summary: " "
tags: ["python","Pythonista 3"]
categories: ["python","Pythonista 3"]
url: python-pythonista-3-insatll-setting.html
date: 2020-01-25
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




I had some Python code that I didn't need to run continuously but wanted to run occasionally during downtime. While it's fine if I always have access to a PC, that's not always the case. So I tried Pythonista 3 to see if I could run it from my iPhone or iPad, which I always carry with me.

Pythonista 3 is a paid app for running Python on iOS. As of January 2020, it costs 1,200 yen.

> ‎Pythonista 3 https://apps.apple.com/jp/app/pythonista-3/id1085978097

The official page is here:

> Pythonista for iOS http://omz-software.com/pythonista/

Popular third-party modules such as numpy, matplotlib, and requests are available, as well as modules customized for iOS. You can access iPhone motion sensor data, photo library, contacts, alarms, iOS clipboard, and more.

One concern is whether it continues to receive updates (the last update was in 2018).

That said, I couldn't find any other option that allows installing 3rd-party modules and running Python code on iOS, so this seems to be the only choice.

In this post, I'll install StaSH to set up a pip-capable environment, then use tweepy to operate the Twitter API.

### Installing StaSH

StaSH (Pythoni**<u>sta Sh</u>**ell) is an extension that enables command operations like pip within Pythonista 3. Since pip is essentially a required feature for using Python, StaSH should also be installed.

To install, first open the console and run the following command. This downloads **getstash.py** from `https://raw.githubusercontent.com/ywangd/stash/master/getstash.py`.

```python
import requests as r; exec(r.get('http://bit.ly/get-stash').text)
```

​

![image-20200121152807032](image-20200121152807032.png)

**launch_stash.py** is downloaded from GitHub. The message says "Home directory to Start StaSh."

<img src="image-20200121152714804.png" alt="image-20200121152714804" style="zoom:80%;" />

Restart the app and navigate to "Script Library" - "This iPhone."

<img src="image-20200121152920677.png" alt="image-20200121152920677" style="zoom:80%;" />

**launch_stash.py** has been placed there. Execute this Python file.

<img src="image-20200121153023599.png" alt="image-20200121153023599" style="zoom:80%;" />

<img src="image-20200121153053252.png" alt="image-20200121153053252" style="zoom:80%;" />

The console screen launches. Run pip commands from this screen. Here, I'll install tweepy, a Twitter API wrapper.

<img src="image-20200121153128176.png" alt="image-20200121153128176" />

![image-20200121153244289](image-20200121153244289.png)



### Running Python Code

Now that I can install required modules via pip, I'll create a Python script by copy-pasting and try running it. Note that loading from cloud storage like Google Drive or Dropbox is not possible — only local files or iCloud Drive are supported.

##### Source Code



![image-20200121153350430](image-20200121153350430.png)

##### Execution Result

![image-20200121153439502](image-20200121153439502.png)

It ran successfully. Now I can run Python even in situations where I only have my smartphone, which should improve quality of life. ~~I wonder if game automation is also possible?~~

For more details:

> Pythonista for iOS http://omz-software.com/pythonista/
