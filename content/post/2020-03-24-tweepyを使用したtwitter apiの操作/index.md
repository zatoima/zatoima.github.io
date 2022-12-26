---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "tweepyを使用したtwitter apiの操作"
subtitle: ""
summary: " "
tags: ["python","tweepy","Twitter API"]
categories: ["python","tweepy","Twitter API"]
url: twitter-api-tweepy-python-operation.html
date: 2020-03-24
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



### 前提条件

Twitter APIの使用申請を行い下記のkeyやtokenを取得していること

- Consumer_key
- Consumer_secret
- Access_token
- Access_secret

> 参考：Twitter API 登録 (アカウント申請方法) から承認されるまでの手順まとめ　※2019年8月時点の情報 - Qiita https://qiita.com/kngsym2018/items/2524d21455aac111cdee

### サンプル

実際に試してみる。tweepyはtwitter apiを簡単に使うためのwrapperなので短いコードでtwitterの基本的操作をすることが出来る。

#### tweepyのimportと接続認証

取得したkeyとtokenの設定、及びtwitterオブジェクトの生成、認証周りを行う。

```python
import tweepy

Consumer_key = 'xxxxxxxxxxxxxxx'
Consumer_secret = 'xxxxxxxxxxxxxxxxxxx'
Access_token = 'xxxxxxxxxxxxxxxxxxxxxxxx'
Access_secret = 'xxxxxxxxxxxxxxxxxxx'

# Twitterオブジェクトの生成
auth=tweepy.OAuthHandler(Consumer_key,Consumer_secret)
auth.set_access_token(Access_token,Access_secret)
api=tweepy.API(auth)
```

#### 特定ユーザのタイムラインを表示する

```
status=api.user_timeline(id='zatoima1')[0]
print(status.user.name)
print(status.text)
```

#### 結果

```
zato
RT @motikiro2: パソコンの排気口を塞ぐツボツボとネコネコ https://t.co/fbfq7GDLbK
```

statusオブジェクトには下記の情報が格納されるためこちらを参照することで各種操作を自動化することが可能。

| オブジェクト                 | 格納情報                      |
| ---------------------------- | ----------------------------- |
| status.text                  | ツイート                      |
| status.id                    | ツイート固有のID              |
| status.in_reply_to_status_id | リプライ先のツイートID        |
| status.retweet_count         | リツイート数                  |
| status.favorite_count        | いいねの数                    |
| status.user.name             | ユーザー名                    |
| status.user.screen_name      | スクリーンネーム（@zatoima1） |
| status.user.friends_count    | フォロー数                    |
| status.user.followers_count  | フォロワー数                  |
| status.user.description      | 自己紹介                      |

その他の格納情報についてはこちらも参照。

> tweepyのstatusオブジェクトに格納される情報一覧 | my opinion is my own https://zatoima.github.io/twitter-api-tweepy-status-list.html

#### 特定ツイートの自動いいね、自動リツイート、自動フォロー

次にこのオブジェクトを使用してbot作成に役に立ちそうな例を記載する。例えば下記のpythonのコードではAWSという文言を含むツイートを20件検索している。検索に引っかかったツイートからユーザ情報やツイート情報を取得して"status"オブジェクトに格納。statusオブジェクトに格納されているツイートやユーザに対して、「①いいね」、「②リツイート」、「③フォロー」を実施している。

この例では検索して引っかかったキーワードに対しての操作だが、Twitterに関わる操作であればほとんど出来るみたいなので、Twitter botや特定キーワードに対して瞬時にいいねをするアカウントはこの辺を自動化しているためなんだな、と実感。

```python
q_list=["#AWS"]
count=20
for q in q_list:
    print("Now:QUERY-->>{}".format(q))
    search_results=api.search(q=q,count=count)
    for status in search_results:
        tweet_id=status.id
        user_id=status.user.name
        try:
            api.create_favorite(tweet_id)
            api.retweet(tweet_id)
            api.create_friendship(user_id)           
        except:
            pass
    print("Done:QUERY-->>{}".format(q))
```

※いいね、リツイート、フォローには回数制限があるので注意が必要。凍結リスクがあります。ご注意ください。

> 開発者契約およびポリシー ‒ Twitter開発者 https://developer.twitter.com/ja/developer-terms/agreement-and-policy



