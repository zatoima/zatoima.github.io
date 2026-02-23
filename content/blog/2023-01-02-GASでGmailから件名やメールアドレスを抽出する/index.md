---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "GASでGmailから件名やメールアドレスを抽出する"
subtitle: ""
summary: " "
tags: ["GAS"]
categories: ["GAS"]
url: gas-mail-address-list
date: 2023-01-02
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

プライベートのメールでほぼ見ないメールはArchiveラベルをつけて受信トレイをSkipする運用にしている。これをやるためにはフィルタリングを行う必要があるのだが、メールアドレスの抽出時にOutlookのエクスポート -> メールアドレス抽出という手順を踏んでいた。これを簡略化したくて、抽出したいメールをスターをつけておいて、必要なときにこのGASを実行して、メールアドレスを一覧化したのでメモしておく。

### コード

こちらのサイトのスクリプトにメールアドレス"だけ"を抽出するファンクションを追加したり検索条件を変えただけ。

> - [Gmailの検索と内容取得をするGAS – TD シネックスブログ](https://jp.tdsynnex.com/blog/google/gmail-gas/)

```js
function searchMails() {

  const query = 'is:starred'
  const threads = GmailApp.search(query);

  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName('メールリスト');

  // 削除の開始行と削除する行数を取得（詳細後述）
  const rowPosition = 2;
  const howMany = sheet.getLastRow() - 1;

  // データの行がある場合、行削除を実行（詳細後述）
  if(howMany > 0){
    sheet.deleteRows(rowPosition, howMany);
  }

  // 送信元からメールアドレスを抽出するための正規表現定義
  const emailRe = new RegExp("[a-zA-Z0-9_.+-]+@([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*.)+[a-zA-Z]{2,}");

  // 送信元からメールアドレスを抽出するためのファンクション
  function emailOf(s) {
      const m = s.match(emailRe);
      if (m) {  // m != null
          return m[0];
      }
      return "";
  }

  threads.forEach(thread => {

    const messages = thread.getMessages();

    messages.forEach(message => {

      let fromData = message.getFrom(); // 送信元
      let subject = message.getSubject(); // 件名
      //let body = message.getPlainBody(); // 本文
      let attachments = message.getAttachments(); // 添付ファイル群（配列）

      let fromAdress= emailOf(fromData); //メールアドレス

      let attachmentList = []; // 添付ファイルのファイル名格納用の配列

      if(attachments.length > 0){
        attachments.forEach(attachment => {

          let name = attachment.getName();

          attachmentList.push(name);
        });
      }

      attachmentList = attachmentList.join(',');

      let data = [fromData, fromAdress, subject, attachmentList]; //本文が必要な場合はbodyの変数を追加

      sheet.appendRow(data);

    });
  });
}

```

### スプレッドシート側

事前にやることとして、`メールリスト`というシート名とヘッダーを用意する。

![image-20230102214603127](./image-20230102214603127.png)
