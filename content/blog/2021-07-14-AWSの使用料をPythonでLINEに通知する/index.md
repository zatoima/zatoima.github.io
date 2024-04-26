---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "AWSの使用料をPythonでLINEに通知する"
subtitle: ""
summary: " "
tags: ["AWS","python"]
categories: ["AWS","python"]
url: aws-python-amount-to-use-cost-line-notify
date: 2021-07-14
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

### 前提

- Line Notifyの設定が完了していること（https://notify-bot.line.me/ja/）
- CloudWatchの権限が付与されていて、AWS CLIの実行が可能なこと

### コード

ほぼ他で作ったスクリプトの使いまわし…

```python
import os,sys,datetime
import boto3
import requests
import datetime

def main():
    get_aws_cost()
    send_line_notify(LINE_TEXT)

def send_line_notify(notification_message):

    line_notify_token = 'xxxxxxxxxxxxxxxxxxxxxxx'
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_notify_token}'}
    data = {'message': f'message: {notification_message}'}
    requests.post(line_notify_api, headers = headers, data = data)

def get_aws_cost():

    AWS_REGION = "us-east-1"
    response = boto3.client('cloudwatch', region_name='us-east-1')
    today_date = datetime.date.today().strftime('%Y/%m/%d')

    def get_value():
        get_demesion = [{'Name': 'Currency', 'Value': 'USD'}]

        data = response.get_metric_statistics(
               Namespace='AWS/Billing',
               MetricName='EstimatedCharges',
               Period=86400,
               StartTime=today_date + " 00:00:00",
               EndTime=today_date + " 23:59:59",
               Statistics=['Maximum'],
               Dimensions=get_demesion
               )
        for info in data['Datapoints']:
            return info['Maximum']

    total_value = get_value()

    global LINE_TEXT
    LINE_TEXT='本日までのAWSの利用料金は$' + str(total_value) + 'になります'

if __name__ == "__main__":
    main()

```



