---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "gogcli：GoogleサービスをターミナルからCLIで操作するツールのセットアップ手順"
subtitle: ""
summary: " "
tags: ["Google","CLI","Go","OAuth"]
categories: ["CLI"]
url: gogcli-setup-google-cli-terminal
date: 2026-02-25
featured: false
draft: false

# Featured image
image:
  caption: ""
  focal_point: ""
  preview_only: fals
---

## はじめに

gogcliは、Gmail・Calendar・Drive・Sheets・Tasks・Contacts など Google の主要サービスをターミナルから操作できる CLI ツールである。JSON出力に対応しておりスクリプトやパイプラインとの親和性が高い。複数アカウントの管理や最小権限認証もサポートしている。

本記事では、gogcli のインストールから Google Cloud プロジェクトの設定、OAuth 認証、基本的な使い方までをまとめる。

### 対応サービス一覧

| サービス | 主な機能 |
|---|---|
| Gmail | メール検索・送信・ラベル管理・フィルタ・下書き・Watch (Pub/Sub) |
| Calendar | 予定の一覧・作成・更新・削除・空き時間確認・チームカレンダー |
| Drive | ファイル検索・アップロード・ダウンロード・共有権限設定 |
| Sheets | スプレッドシートの読み書き・行列挿入・書式設定・エクスポート |
| Docs | ドキュメント作成・Markdownインポート・PDF/DOCXエクスポート |
| Slides | プレゼン作成・スライド追加・PDF/PPTXエクスポート |
| Contacts | 連絡先の検索・作成・更新・ディレクトリ検索 |
| Tasks | タスクリスト管理・タスク追加・完了・繰り返し設定 |
| Chat | スペース一覧・メッセージ送信・DM（Workspace のみ） |
| Forms | フォーム作成・取得・回答確認 |
| Apps Script | プロジェクト管理・関数実行 |
| Keep | ノート一覧・検索（Workspace + サービスアカウント限定） |
| Groups | グループ一覧・メンバー表示（Workspace のみ） |

## インストール

### Homebrew（推奨）

```bash
brew install steipete/tap/gogcli
```

### ソースからビルド

Go 1.24 以上が必要である。

```bash
git clone https://github.com/steipete/gogcli.git
cd gogcli
make
```

ビルドが成功すると `./bin/gog` にバイナリが生成される。

```bash
./bin/gog --version
# v0.11.0 (xxxxxxxxxxxx 2026-02-25T...)
```

{{< figure src="github-repo.png" caption="gogcli GitHubリポジトリ（[github.com/steipete/gogcli](https://github.com/steipete/gogcli)）" >}}

### コマンド体系

`gog` コマンドは各サービスをサブコマンドとして提供している。

{{< figure src="gog-help.png" caption="gog --help の出力。サブコマンドで各Googleサービスを操作する" >}}

## Google Cloud プロジェクトの設定

gogcli を使うには、Google Cloud プロジェクトで OAuth クライアントを作成し、必要な API を有効化する必要がある。

### API の有効化

`gcloud` コマンドで一括有効化できる。

```bash
gcloud services enable \
  gmail.googleapis.com \
  calendar-json.googleapis.com \
  drive.googleapis.com \
  sheets.googleapis.com \
  tasks.googleapis.com \
  people.googleapis.com \
  chat.googleapis.com \
  classroom.googleapis.com \
  forms.googleapis.com \
  script.googleapis.com \
  cloudidentity.googleapis.com \
  docs.googleapis.com \
  --project=<PROJECT_ID>
```

### OAuth 同意画面の設定

1. [Google Cloud Console の OAuth 同意画面](https://console.cloud.google.com/auth/branding) にアクセス
2. アプリ名やサポートメールなどを設定
3. アプリが「Testing」状態の場合、[テストユーザー設定画面](https://console.cloud.google.com/auth/audience) で自分のメールアドレスを追加

テストモードでは、テストユーザーに登録されたアカウントのみが認証可能である。登録していない場合、以下のような「403: access_denied」エラーが発生する。

{{< figure src="auth-error-403.png" caption="Google OAuth 認証時の 403 access_denied エラー画面。テストユーザー未登録時に表示される（[OAuth同意画面のテストユーザー設定](https://console.cloud.google.com/auth/audience)）" >}}

{{< callout "warning" >}}
このエラーが表示された場合は、Google Cloud Console の OAuth 同意画面設定でテストユーザーに自分のメールアドレスを追加する必要がある。
{{< /callout >}}

### OAuth クライアント JSON の取得

1. [Google Cloud Console の認証情報画面](https://console.cloud.google.com/auth/clients) にアクセス
2. 「Create Client」をクリック
3. アプリケーションの種類に「Desktop app」を選択
4. JSON ファイルをダウンロード（`client_secret_....apps.googleusercontent.com.json`）

## 認証

### クレデンシャルの登録

ダウンロードした OAuth クライアント JSON を gogcli に登録する。

```bash
gog auth credentials ~/Downloads/client_secret_XXXX.json
```

### アカウント認証

```bash
gog auth add you@gmail.com
```

ブラウザが開き、Google の OAuth 認証画面が表示される。「このアプリは確認されていません」という警告が出るが、「詳細」→「gogcli（安全でない）に移動」で進める。

認証が完了すると以下の画面が表示される。

{{< figure src="auth-success.png" caption="gog auth add 完了後の認証成功画面。ブラウザに「You're connected」と表示される" >}}

### 認証の確認

```bash
gog auth list
gog auth status
```

`auth list` で登録済みアカウントの一覧、`auth status` で現在のアカウントの認証状態とサービス一覧が確認できる。

### キーリングバックエンド

macOS ではデフォルトで Keychain が使用される。Keychain のパスワード入力プロンプトが頻繁に出る場合は、ファイルバックエンドに切り替えることもできる。

```bash
# ファイルバックエンドに切り替え
gog auth keyring file

# パスワード入力を省略（CI/自動化用途）
export GOG_KEYRING_PASSWORD='任意のパスワード'
```

## 使い方

### 環境変数によるアカウント設定

毎回 `--account` を指定するのは手間なので、環境変数にデフォルトアカウントを設定しておくと便利である。

```bash
# .zshrc に追加
export GOG_ACCOUNT=you@gmail.com
```

### 各サービスの操作例

{{< figure src="command-example.png" caption="Gmail・Calendar・Drive・Tasks・Sheets の各コマンド実行例" >}}

#### Gmail

```bash
# 直近3日間のメール検索
gog gmail search 'newer_than:3d' --max 10

# 未読メール検索
gog gmail search 'is:unread' --max 5

# ラベル一覧
gog gmail labels list

# メール送信
gog gmail send --to user@example.com --subject "件名" --body "本文"
```

#### Calendar

```bash
# カレンダー一覧
gog calendar calendars

# 今日の予定
gog calendar events primary --today

# 今週の予定
gog calendar events primary --week

# 予定作成
gog calendar create primary \
  --summary "Meeting" \
  --from 2026-03-01T10:00:00+09:00 \
  --to 2026-03-01T11:00:00+09:00
```

#### Drive

```bash
# ファイル一覧
gog drive ls --max 10

# ファイル検索
gog drive search "keyword" --max 10

# ダウンロード
gog drive download <fileId> --out ./file.pdf
```

#### Sheets

```bash
# スプレッドシート読み取り
gog sheets get <spreadsheetId> 'Sheet1!A1:B10'

# データ書き込み
gog sheets update <spreadsheetId> 'A1' --values-json '[["Name","Score"],["Alice","95"]]'

# 新規作成
gog sheets create "シート名" --sheets "Sheet1,Sheet2"
```

#### Tasks

```bash
# タスクリスト一覧
gog tasks lists

# タスク追加
gog tasks add <tasklistId> --title "タスク名"

# タスク完了
gog tasks done <tasklistId> <taskId>
```

#### Contacts

```bash
# 連絡先一覧
gog contacts list --max 50

# 連絡先検索
gog contacts search "名前" --max 10
```

### JSON 出力

`--json` フラグを付けると JSON 形式で出力される。`jq` と組み合わせたスクリプティングに適している。

```bash
# PDF ファイルのみ抽出
gog --json drive ls --max 50 | jq '.files[] | select(.mimeType=="application/pdf")'

# 未読メールのスレッドIDを取得
gog --json gmail search 'is:unread' --max 100 | jq -r '.threads[].id'
```

### 複数アカウント

```bash
# アカウント切り替え
gog gmail search 'is:unread' --account personal@gmail.com
gog gmail search 'is:unread' --account work@company.com

# エイリアス設定
gog auth alias set work work@company.com
gog gmail search 'is:unread' --account work
```

## まとめ

gogcli は Google の 13 以上のサービスを単一の CLI ツールでカバーしており、JSON 出力・複数アカウント対応・最小権限認証といった実用的な機能が揃っている。セットアップには Google Cloud プロジェクトの設定と OAuth 認証が必要だが、一度設定すればトークンが自動更新されるため、継続的に利用できる。

ターミナルから Google サービスを操作したい場合や、シェルスクリプトで自動化を行いたい場合に有用なツールである。

## 参考資料

{{< linkcard "https://github.com/steipete/gogcli" >}}
