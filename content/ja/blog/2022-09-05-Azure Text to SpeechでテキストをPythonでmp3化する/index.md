---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Azure Text to Speechで英語テキストをPythonでmp3化する"
subtitle: ""
summary: " "
tags: ["Python","Azure","英語"]
categories: ["Python","Azure","英語"]
url: python-azure-english-text-to-speech
date: 2022-09-05
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



英語勉強時に文章を読み上げてくれる機能が欲しくて調べてみた。英語に関してはAWS、Azure、GCPのText to Speechサービスの中では一番Azureが流暢に感じる。

- Azure
  - [[テキスト読み上げ – リアルな AI 音声ジェネレーター \| Microsoft Azure]](https://azure.microsoft.com/ja-jp/services/cognitive-services/text-to-speech/#features)

- AWS
  - [Amazon Polly（深層学習を使用したテキスト読み上げサービス）\| AWS](https://aws.amazon.com/jp/polly/)
- Google Cloud
  - [Text\-to\-Speech: 自然な音声合成  \|  Google Cloud](https://cloud.google.com/text-to-speech?hl=ja)

### 参考にした記事

- [PythonでAzure Text to Speechで合成音声の作成 \- Qiita](https://qiita.com/567000/items/f82b8da3ee087c604d8c)

### 上記からの変更点

- 日本リージョンからEast USリージョンに変更
- 日本語のText to Speechではなく、英語でのText to Speechに変更
- 実行時に読み込ませるテキスト文を指定する形に。

```python
text = input('Enter English Text : ')
subscription_key = 'xxxxxxxxxx' # APIキーをいれてください

import requests
import xml.etree.ElementTree as ElementTree
import datetime

dt = datetime.datetime.now()
dt = dt.strftime('%Y%m%d%H%M%S')
output="azure-text-to-speech_"+dt+".mp3"

fetch_token_url = 'https://eastus.api.cognitive.microsoft.com/sts/v1.0/issuetoken'
headers = {
    'Ocp-Apim-Subscription-Key': subscription_key
}
response = requests.post(fetch_token_url, headers=headers)
access_token = str(response.text)
print(access_token)

constructed_url = 'https://eastus.tts.speech.microsoft.com/cognitiveservices/v1'

headers = {
    'Authorization': 'Bearer ' + access_token,
    'Content-Type': 'application/ssml+xml',
    'X-Microsoft-OutputFormat': 'audio-16khz-128kbitrate-mono-mp3',
}

xml_body = ElementTree.Element('speak', version='1.0')
xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
voice = ElementTree.SubElement(xml_body, 'voice')
voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
voice.set('name', 'Microsoft Server Speech Text to Speech Voice (en-US, JennyNeural)')
prosody = ElementTree.SubElement(voice, 'prosody')
prosody.set('pitch','medium') # high
prosody.set('rate','medium') # fast
prosody.text = text
body = ElementTree.tostring(xml_body)

response = requests.post(constructed_url, headers=headers, data=body)
if response.status_code == 200:
    with open(output, 'wb') as audio:
        audio.write(response.content)
        print("\nStatus code: " + str(response.status_code) + "\nYour TTS is ready for playback.\n")
else:
    print("\nStatus code: " + str(response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")

```

