---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Python(pyautogui)とLINE Notifyを利用してWeb画面変化をキャッチしてLINE通知する"
subtitle: ""
summary: " "
tags: ["Python","LINE Notify"]
categories: ["Python","LINE Notify"]
url: python-line-notify-web-screan.html
date: 2020-10-01
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



表題の通り、Web画面変化を定期的にチェックして期待する画面になった場合にLINE Notifyを利用してチェックする簡単なスクリプト。

LINE Notifyの設定自体は大変簡単です。

> [超簡単]LINE notify を使ってみる - Qiita https://qiita.com/iitenkida7/items/576a8226ba6584864d95

当初はRequestsやSeleniumを使用を想定していましたが、アクセスしたいサイトに対してuser-agentを偽装しても`access denied`でどうしようも無かったのでpyautoguiを利用して期待する画像がWeb画面に表示されたら通知が飛ぶようにしました。pyautoguiはUWSCよりも簡単…！

こちらのスクリプト上、URLはダミーのものを入れております。

```python
import webbrowser
import datetime
import pyautogui
import time
import sys
import requests

def main():
    while True:
        time.sleep(300)
        check_web()
        if pos is not None:
            send_line_notify(sent_message)
            send_gazo()
        else:
            continue
    
def send_line_notify(notification_message):
    line_notify_token = 'xxxxxxxxxxxxxxxxxxxxxxxxxx'
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_notify_token}'}
    data = {'message': f'message: {notification_message}'}
    requests.post(line_notify_api, headers = headers, data = data)

def send_gazo():
    line_notify_token = 'xxxxxxxxxxxxxxxxxxxxxxxx'
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_notify_token}'}

    message = 'Screanshot for python script！'
    payload = {"message" :  message}
    files = {"imageFile":open('D:\\tool\\py\\screanshot.jpg','rb')}
    post = requests.post(line_notify_api ,headers = headers ,params=payload,files=files)
    
def check_web():

    #ブラウザでURLを開く
    webbrowser.open('https://www.google.com/')
    
    #完全に表示されるまで待機
    time.sleep(20)
        
    #エラー画面が表示されていないか"pyautogui.locateOnScreen"で判定
    pos_check
    pos_check=pyautogui.locateOnScreen('D:\\tool\\py\\access_denied.jpg', confidence=0.6)
    #print(pos_check)

    if pos_check is not None:
        print("エラーのためスリープ")
        #エラーのスクリーンショットを記録
        pyautogui.screenshot('D:\\tool\\py\\error.jpg')
        time.sleep(3600)

    #confidenceを微調整
    #表示された画面に画像がどこの座標にあるかチェックする
    pos=pyautogui.locateOnScreen('D:\\tool\\py\\google.jpg', confidence=0.6)
    #print(pos)

    #期待する画面が表示されている場合にLINEで飛ばすメッセージをセットする
    if pos is not None:
        global sent_message
        sent_message='LINE Notify Message xxxxxxxxxxxxxxxxxx'
        pyautogui.screenshot('D:\\tool\\py\\screanshot.jpg')

    else:
        print("該当無し")
        #sys.exit()

if __name__ == "__main__":
    main()
```

