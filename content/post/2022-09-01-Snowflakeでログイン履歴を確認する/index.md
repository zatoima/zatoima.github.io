---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Snowflakeでログイン履歴を確認する"
subtitle: ""
summary: " "
tags: ["snowflake"]
categories: ["snowflake"]
url: snowflake-login-history
date: 2022-09-01
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

`LOGIN_HISTORY`ビューを使用する

`過去365日間（1年間）`以内のSnowflakeユーザーによるログイン試行をクエリが可能。

```
SELECT
  EVENT_ID,
  CONVERT_TIMEZONE('Asia/Tokyo',EVENT_TIMESTAMP)  AS JST_EVENT_TIMESTAMP,
  EVENT_TYPE,
  USER_NAME,
  CLIENT_IP,
  REPORTED_CLIENT_TYPE,
  REPORTED_CLIENT_VERSION,
  FIRST_AUTHENTICATION_FACTOR,
  SECOND_AUTHENTICATION_FACTOR,
  IS_SUCCESS,
  ERROR_CODE,
  ERROR_MESSAGE,
  RELATED_EVENT_ID,
  CONNECTION 
FROM
  SNOWFLAKE.ACCOUNT_USAGE.LOGIN_HISTORY
ORDER BY
  EVENT_TIMESTAMP DESC
;
```

- [LOGIN\_HISTORY ビュー — Snowflake Documentation](https://docs.snowflake.com/ja/sql-reference/account-usage/login_history.html#login-history-view)
