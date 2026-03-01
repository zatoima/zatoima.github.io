---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Using Alexa Routines to Handle Voice Input Errors in the Piyolog Skill"
subtitle: ""
summary: " "
tags: ["Alexa"]
categories: ["Alexa"]
url: alexa-change-word-voice-control-piyolog
date: 2021-08-18
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




Recently, I've been struggling with first-time parenting. I'm using Piyolog via Alexa to keep childcare records, and it has been very well received by both my wife and me. Before using it, we had to unlock our phones and record things manually, which was tedious. On top of that, we frequently forgot to record things, causing arguments. So I started using Piyolog via Alexa. (I was amazed when I found it!)

> https://www.amazon.co.jp/PiyoLog-Inc-%E3%81%B4%E3%82%88%E3%83%AD%E3%82%B0/dp/B08KFD3FWF

![image-20210818211209614](image-20210818211209614.png)

However, there was one issue. It's a wonderful skill, but as noted in the reviews, voice input sometimes fails for certain operations. It doesn't happen frequently, but it occurs about once every five times. Specifically, it's the issue described in reviews:

> Even when saying the template phrase "Alexa, record pee in Piyolog," recording often fails. In most cases, it responds with "This is Piyolog. You can record and check milking, sleep, excretion, and more. What would you like to record?" and you have to say "pee" again, doubling the effort.

Being misheard in the middle of the night at 4 AM doubles the stress, so I wanted to fix this. I decided to set up synonyms (alternative phrases) using Routines. Using Alexa Routines is the easiest way to change the wording for voice commands.

- ##### Select "More" at the bottom right

![image-20210818210258263](image-20210818210258263.png)

- ##### Select "Routines"

![image-20210818210342551](image-20210818210342551.png)

- ##### Click the "+" button at the top right

![image-20210818210434628](image-20210818210434628.png)

- ##### Specify "Routine Name", "When this happens", and "Add action". "Routine Name" is optional and can be skipped.

![image-20210818210458294](image-20210818210458294.png)

- ##### For "When this happens", select "Voice". On the next screen, enter the phrase that will trigger the routine.

![image-20210818210643103](image-20210818210643103.png)

![image-20210818210806622](image-20210818210806622.png)

- ##### For "Add action", enter the phrase that Alexa will speak

![image-20210818210852358](image-20210818210852358.png)



![image-20210818210906936](image-20210818210906936.png)

With this setup, just saying "pee" to Alexa will trigger the same effect as "Record pee in Piyolog." Since the phrase is short, Alexa won't mishear it, which is very convenient. After that, I created more routines with the same approach for other phrases like "poop," "bath," etc., so I can now log entries in Piyolog with short phrases.

![image-20210818211744208](image-20210818211744208.png)

### Thank you Alexa and Piyolog!
