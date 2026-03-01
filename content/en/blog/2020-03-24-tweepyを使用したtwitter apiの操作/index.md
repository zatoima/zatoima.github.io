---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Using the Twitter API with tweepy"
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



### Prerequisites

You must have applied for the Twitter API and obtained the following keys and tokens:

- Consumer_key
- Consumer_secret
- Access_token
- Access_secret

> Reference: Step-by-step guide from Twitter API registration (account application process) to approval - as of August 2019 - Qiita https://qiita.com/kngsym2018/items/2524d21455aac111cdee

### Sample

Let's try it out. tweepy is a wrapper that makes it easy to use the Twitter API, allowing basic Twitter operations with short code.

#### Importing tweepy and Connection Authentication

Set the obtained keys and tokens, create the Twitter object, and handle authentication.

```python
import tweepy

Consumer_key = 'xxxxxxxxxxxxxxx'
Consumer_secret = 'xxxxxxxxxxxxxxxxxxx'
Access_token = 'xxxxxxxxxxxxxxxxxxxxxxxx'
Access_secret = 'xxxxxxxxxxxxxxxxxxx'

# Create Twitter object
auth=tweepy.OAuthHandler(Consumer_key,Consumer_secret)
auth.set_access_token(Access_token,Access_secret)
api=tweepy.API(auth)
```

#### Display a Specific User's Timeline

```
status=api.user_timeline(id='zatoima1')[0]
print(status.user.name)
print(status.text)
```

#### Result

```
zato
RT @motikiro2: パソコンの排気口を塞ぐツボツボとネコネコ https://t.co/fbfq7GDLbK
```

The status object stores the following information, which can be referenced to automate various operations.

| Object                       | Stored Information                    |
| ---------------------------- | ------------------------------------- |
| status.text                  | Tweet                                 |
| status.id                    | Tweet's unique ID                     |
| status.in_reply_to_status_id | Tweet ID of the reply target          |
| status.retweet_count         | Number of retweets                    |
| status.favorite_count        | Number of likes                       |
| status.user.name             | Username                              |
| status.user.screen_name      | Screen name (@zatoima1)               |
| status.user.friends_count    | Following count                       |
| status.user.followers_count  | Follower count                        |
| status.user.description      | Bio                                   |

For other stored information, please also refer to:

> List of Information Stored in the tweepy Status Object | my opinion is my own https://zatoima.github.io/twitter-api-tweepy-status-list.html

#### Auto-Like, Auto-Retweet, and Auto-Follow for Specific Tweets

Next, let me show an example that might be useful for bot creation using this object. For example, the Python code below searches for 20 tweets containing the word "AWS." User information and tweet information retrieved from matching tweets are stored in the "status" object. The code then performs "1. Like", "2. Retweet", and "3. Follow" on the tweets and users stored in the status object.

In this example, we operate on keywords found through search, but it appears that almost any Twitter-related operation is possible. This shows how Twitter bots and accounts that instantly like tweets for specific keywords automate this kind of thing.

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

*Note: There are rate limits for likes, retweets, and follows. There is a risk of account suspension. Please be careful.*

> Developer Agreement and Policy - Twitter Developer https://developer.twitter.com/ja/developer-terms/agreement-and-policy
