---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Converting English Text to MP3 with Azure Text to Speech and Python"
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

I was looking for a feature that reads text aloud while studying English. Among the Text to Speech services from AWS, Azure, and GCP, I find Azure to be the most fluent for English.

- Azure
  - [Text to Speech – Realistic AI Voice Generator | Microsoft Azure](https://azure.microsoft.com/en-us/services/cognitive-services/text-to-speech/#features)

- AWS
  - [Amazon Polly (Text-to-Speech Service Using Deep Learning) | AWS](https://aws.amazon.com/polly/)
- Google Cloud
  - [Text-to-Speech: Natural Speech Synthesis | Google Cloud](https://cloud.google.com/text-to-speech)

### Reference Article

- [Creating Synthetic Speech with Azure Text to Speech in Python - Qiita](https://qiita.com/567000/items/f82b8da3ee087c604d8c)

### Changes from the Above

- Changed from Japan region to East US region
- Changed from Japanese Text to Speech to English Text to Speech
- Set up to specify the text to read at runtime.

```python
text = input('Enter English Text : ')
subscription_key = 'xxxxxxxxxx' # Please enter your API key

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
