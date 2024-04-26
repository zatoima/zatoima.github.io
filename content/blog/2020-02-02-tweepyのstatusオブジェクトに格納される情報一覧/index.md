---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "tweepyのstatusオブジェクトに格納される情報一覧"
subtitle: ""
summary: " "
tags: ["Twitter","Python","Tweepy"]
categories: ["Twitter","Python","Tweepy"]
url: twitter-api-tweepy-status-list.html
date: 2020-02-02
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



Twitter APIとPythonを使って自動化して遊んでいます。毎回ググるのもtweepyのstatusの中身を出力して確認するのも面倒なのでメモ。

### 前提条件

Twitter APIの使用申請を行い下記のkeyやtokenを取得していること

- Consumer_key
- Consumer_secret
- Access_token
- Access_secret

> 参考：Twitter API 登録 (アカウント申請方法) から承認されるまでの手順まとめ　※2019年8月時点の情報 - Qiita https://qiita.com/kngsym2018/items/2524d21455aac111cdee

### テスト

```python
import tweepy

Consumer_key = 'xxxx'
Consumer_secret = 'xxxxxx'
Access_token = 'xxx-xxx'
Access_secret = 'xxxxxx'
auth=tweepy.OAuthHandler(Consumer_key,Consumer_secret)
auth.set_access_token(Access_token,Access_secret)
api=tweepy.API(auth)

status = api.user_timeline(id='zatoima1')[0]
print(status)
```

### 結果

代表的な情報はこちら。

| status.text                  | ツイート                      |
| ---------------------------- | ----------------------------- |
| status.id                    | ツイート固有のID              |
| status.in_reply_to_status_id | リプライ先のツイートID        |
| status.retweet_count         | リツイート数                  |
| status.favorite_count        | いいねの数                    |
| status.user.name             | ユーザー名                    |
| status.user.screen_name      | スクリーンネーム（@zatoima1） |
| status.user.friends_count    | フォロー数                    |
| status.user.followers_count  | フォロワー数                  |
| status.user.description      | 自己紹介                      |

他にも色々あるので全量の出力を貼り付け。

```text
Status(_api=<tweepy.api.API object at 0x00000240734C1E48>,
 _json={'created_at': 'Thu Jan 30 12:08:18 +0000 2020',
 'id': 1222854043690647552,
 'id_str': '1222854043690647552',
 'text': '海外出張時に休日に移動して月曜日から現地みたいなことやるけど、法律的というか判例的には「移動の時なんて何してもええんやから休日移動には代休あげんくてもええよ」となってるんよな。中々のトラップ。ほとんどの会社は代休くれるやろうけど。',
 'truncated': False,
 'entities': {'hashtags': [],
 'symbols': [],
 'user_mentions': [],
 'urls': []},
 'source': '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>',
 'in_reply_to_status_id': None,
 'in_reply_to_status_id_str': None,
 'in_reply_to_user_id': None,
 'in_reply_to_user_id_str': None,
 'in_reply_to_screen_name': None,
 'user': {'id': 1080276052721553408,
 'id_str': '1080276052721553408',
 'name': 'zato',
 'screen_name': 'zatoima1',
 'location': '日本 東京',
 'description': '都内で働くインフラフラフラエンジニア/Oracle Database/MySQL/PostgreSQL/AWSが主戦場、もしくは興味があります。英語頑張りたい。どうでもいい呟きが多いです。家系ラーメン。Worked at Oracle. Working at AWS。my opinion is my own',
 'url': None,
 'entities': {'description': {'urls': []}},
 'protected': False,
 'followers_count': 86,
 'friends_count': 149,
 'listed_count': 1,
 'created_at': 'Wed Jan 02 01:34:16 +0000 2019',
 'favourites_count': 960,
 'utc_offset': None,
 'time_zone': None,
 'geo_enabled': True,
 'verified': False,
 'statuses_count': 388,
 'lang': None,
 'contributors_enabled': False,
 'is_translator': False,
 'is_translation_enabled': False,
 'profile_background_color': 'F5F8FA',
 'profile_background_image_url': None,
 'profile_background_image_url_https': None,
 'profile_background_tile': False,
 'profile_image_url': 'http://pbs.twimg.com/profile_images/1147139264112517120/Z6NuA_Dn_normal.jpg',
 'profile_image_url_https': 'https://pbs.twimg.com/profile_images/1147139264112517120/Z6NuA_Dn_normal.jpg',
 'profile_link_color': '1DA1F2',
 'profile_sidebar_border_color': 'C0DEED',
 'profile_sidebar_fill_color': 'DDEEF6',
 'profile_text_color': '333333',
 'profile_use_background_image': True,
 'has_extended_profile': True,
 'default_profile': True,
 'default_profile_image': False,
 'can_media_tag': False,
 'followed_by': False,
 'following': False,
 'follow_request_sent': False,
 'notifications': False,
 'translator_type': 'none'},
 'geo': None,
 'coordinates': None,
 'place': None,
 'contributors': None,
 'is_quote_status': False,
 'retweet_count': 0,
 'favorite_count': 0,
 'favorited': False,
 'retweeted': False,
 'lang': 'ja'},
 created_at=datetime.datetime(2020, 1, 30, 12, 8, 18),
 id=1222854043690647552,
 id_str='1222854043690647552',
 text='海外出張時に休日に移動して月曜日から現地みたいなことやるけど、法律的というか判例的には「移動の時なんて何してもええんやから休日移動には代休あげんくてもええよ」となってるんよな。中々のトラップ。ほとんどの会社は代休くれるやろうけど。',
 truncated=False,
 entities={'hashtags': [],
 'symbols': [],
 'user_mentions': [],
 'urls': []},
 source='Twitter for iPhone',
 source_url='http://twitter.com/download/iphone',
 in_reply_to_status_id=None,
 in_reply_to_status_id_str=None,
 in_reply_to_user_id=None,
 in_reply_to_user_id_str=None,
 in_reply_to_screen_name=None,
 author=User(_api=<tweepy.api.API object at 0x00000240734C1E48>,
 _json={'id': 1080276052721553408,
 'id_str': '1080276052721553408',
 'name': 'zato',
 'screen_name': 'zatoima1',
 'location': '日本 東京',
 'description': '都内で働くインフラフラフラエンジニア/Oracle Database/MySQL/PostgreSQL/AWSが主戦場、もしくは興味があります。英語頑張りたい。どうでもいい呟きが多いです。家系ラーメン。Worked at Oracle. Working at AWS。my opinion is my own',
 'url': None,
 'entities': {'description': {'urls': []}},
 'protected': False,
 'followers_count': 86,
 'friends_count': 149,
 'listed_count': 1,
 'created_at': 'Wed Jan 02 01:34:16 +0000 2019',
 'favourites_count': 960,
 'utc_offset': None,
 'time_zone': None,
 'geo_enabled': True,
 'verified': False,
 'statuses_count': 388,
 'lang': None,
 'contributors_enabled': False,
 'is_translator': False,
 'is_translation_enabled': False,
 'profile_background_color': 'F5F8FA',
 'profile_background_image_url': None,
 'profile_background_image_url_https': None,
 'profile_background_tile': False,
 'profile_image_url': 'http://pbs.twimg.com/profile_images/1147139264112517120/Z6NuA_Dn_normal.jpg',
 'profile_image_url_https': 'https://pbs.twimg.com/profile_images/1147139264112517120/Z6NuA_Dn_normal.jpg',
 'profile_link_color': '1DA1F2',
 'profile_sidebar_border_color': 'C0DEED',
 'profile_sidebar_fill_color': 'DDEEF6',
 'profile_text_color': '333333',
 'profile_use_background_image': True,
 'has_extended_profile': True,
 'default_profile': True,
 'default_profile_image': False,
 'can_media_tag': False,
 'followed_by': False,
 'following': False,
 'follow_request_sent': False,
 'notifications': False,
 'translator_type': 'none'},
 id=1080276052721553408,
 id_str='1080276052721553408',
 name='zato',
 screen_name='zatoima1',
 location='日本 東京',
 description='都内で働くインフラフラフラエンジニア/Oracle Database/MySQL/PostgreSQL/AWSが主戦場、もしくは興味があります。英語頑張りたい。どうでもいい呟きが多いです。家系ラーメン。Worked at Oracle. Working at AWS。my opinion is my own',
 url=None,
 entities={'description': {'urls': []}},
 protected=False,
 followers_count=86,
 friends_count=149,
 listed_count=1,
 created_at=datetime.datetime(2019, 1, 2, 1, 34, 16),
 favourites_count=960,
 utc_offset=None,
 time_zone=None,
 geo_enabled=True,
 verified=False,
 statuses_count=388,
 lang=None,
 contributors_enabled=False,
 is_translator=False,
 is_translation_enabled=False,
 profile_background_color='F5F8FA',
 profile_background_image_url=None,
 profile_background_image_url_https=None,
 profile_background_tile=False,
 profile_image_url='http://pbs.twimg.com/profile_images/1147139264112517120/Z6NuA_Dn_normal.jpg',
 profile_image_url_https='https://pbs.twimg.com/profile_images/1147139264112517120/Z6NuA_Dn_normal.jpg',
 profile_link_color='1DA1F2',
 profile_sidebar_border_color='C0DEED',
 profile_sidebar_fill_color='DDEEF6',
 profile_text_color='333333',
 profile_use_background_image=True,
 has_extended_profile=True,
 default_profile=True,
 default_profile_image=False,
 can_media_tag=False,
 followed_by=False,
 following=False,
 follow_request_sent=False,
 notifications=False,
 translator_type='none'),
 user=User(_api=<tweepy.api.API object at 0x00000240734C1E48>,
 _json={'id': 1080276052721553408,
 'id_str': '1080276052721553408',
 'name': 'zato',
 'screen_name': 'zatoima1',
 'location': '日本 東京',
 'description': '都内で働くインフラフラフラエンジニア/Oracle Database/MySQL/PostgreSQL/AWSが主戦場、もしくは興味があります。英語頑張りたい。どうでもいい呟きが多いです。家系ラーメン。Worked at Oracle. Working at AWS。my opinion is my own',
 'url': None,
 'entities': {'description': {'urls': []}},
 'protected': False,
 'followers_count': 86,
 'friends_count': 149,
 'listed_count': 1,
 'created_at': 'Wed Jan 02 01:34:16 +0000 2019',
 'favourites_count': 960,
 'utc_offset': None,
 'time_zone': None,
 'geo_enabled': True,
 'verified': False,
 'statuses_count': 388,
 'lang': None,
 'contributors_enabled': False,
 'is_translator': False,
 'is_translation_enabled': False,
 'profile_background_color': 'F5F8FA',
 'profile_background_image_url': None,
 'profile_background_image_url_https': None,
 'profile_background_tile': False,
 'profile_image_url': 'http://pbs.twimg.com/profile_images/1147139264112517120/Z6NuA_Dn_normal.jpg',
 'profile_image_url_https': 'https://pbs.twimg.com/profile_images/1147139264112517120/Z6NuA_Dn_normal.jpg',
 'profile_link_color': '1DA1F2',
 'profile_sidebar_border_color': 'C0DEED',
 'profile_sidebar_fill_color': 'DDEEF6',
 'profile_text_color': '333333',
 'profile_use_background_image': True,
 'has_extended_profile': True,
 'default_profile': True,
 'default_profile_image': False,
 'can_media_tag': False,
 'followed_by': False,
 'following': False,
 'follow_request_sent': False,
 'notifications': False,
 'translator_type': 'none'},
 id=1080276052721553408,
 id_str='1080276052721553408',
 name='zato',
 screen_name='zatoima1',
 location='日本 東京',
 description='都内で働くインフラフラフラエンジニア/Oracle Database/MySQL/PostgreSQL/AWSが主戦場、もしくは興味があります。英語頑張りたい。どうでもいい呟きが多いです。家系ラーメン。Worked at Oracle. Working at AWS。my opinion is my own',
 url=None,
 entities={'description': {'urls': []}},
 protected=False,
 followers_count=86,
 friends_count=149,
 listed_count=1,
 created_at=datetime.datetime(2019, 1, 2, 1, 34, 16),
 favourites_count=960,
 utc_offset=None,
 time_zone=None,
 geo_enabled=True,
 verified=False,
 statuses_count=388,
 lang=None,
 contributors_enabled=False,
 is_translator=False,
 is_translation_enabled=False,
 profile_background_color='F5F8FA',
 profile_background_image_url=None,
 profile_background_image_url_https=None,
 profile_background_tile=False,
 profile_image_url='http://pbs.twimg.com/profile_images/1147139264112517120/Z6NuA_Dn_normal.jpg',
 profile_image_url_https='https://pbs.twimg.com/profile_images/1147139264112517120/Z6NuA_Dn_normal.jpg',
 profile_link_color='1DA1F2',
 profile_sidebar_border_color='C0DEED',
 profile_sidebar_fill_color='DDEEF6',
 profile_text_color='333333',
 profile_use_background_image=True,
 has_extended_profile=True,
 default_profile=True,
 default_profile_image=False,
 can_media_tag=False,
 followed_by=False,
 following=False,
 follow_request_sent=False,
 notifications=False,
 translator_type='none'),
 geo=None,
 coordinates=None,
 place=None,
 contributors=None,
 is_quote_status=False,
 retweet_count=0,
 favorite_count=0,
 favorited=False,
 retweeted=False,
 lang='ja')

```



