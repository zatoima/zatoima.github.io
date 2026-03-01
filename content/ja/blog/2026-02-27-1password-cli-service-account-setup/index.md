---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "1Password CLI を Service Account で非対話認証する設定手順"
subtitle: ""
summary: "1Password CLI（op コマンド）をスクリプトや自動化環境で非対話的に利用するための Service Account の設定手順を記録する。専用 Vault の作成からトークンの取得・環境変数への設定、op read / op inject / op run による動作確認までの一連の流れを扱う。"
tags: ["1Password"]
categories: ["その他"]
url: 1password-cli-service-account-setup
date: 2026-02-27
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

## はじめに

1Password CLI（`op` コマンド）は、ターミナルから 1Password のアイテムを操作できるツールである。具体的には以下のようなことが可能となる。

- **シークレットの取得**: API キーや DB パスワードをスクリプト内で安全に参照する
- **環境変数の注入**: `.env` ファイルに Secret Reference を書いておき、実行時に実際の値へ置換する
- **テンプレートの展開**: 設定ファイルのテンプレートに 1Password の値を埋め込んで出力する
- **アイテムの管理**: ログイン情報やセキュアノートの作成・更新・削除を CLI から実行する

通常は実行のたびに Touch ID やマスターパスワードの入力が求められるが、自動化スクリプトや CI/CD パイプラインなど非対話的な環境ではこれが障壁となる。

[1Password Service Accounts](https://developer.1password.com/docs/service-accounts/) を利用すると、トークンベースの認証により対話的な操作なしで `op` コマンドを実行できる。本記事では Service Account の作成から CLI との連携設定までの手順を記載する。

## 認証方式の比較

1Password CLI には主に3つの認証方式がある。

| 方式 | 対話操作 | 用途 | Private Vault |
|------|---------|------|---------------|
| `op signin`（パスワード） | 毎回必要 | 手動操作 | アクセス可 |
| Touch ID 連携 | Touch ID が必要 | デスクトップ環境 | アクセス可 |
| Service Account | 不要 | スクリプト・自動化 | アクセス不可 |

Service Account はトークンを環境変数に設定するだけで認証が完了するため、スクリプトからの利用に適している。一方で Private Vault（個人用保管庫）にはアクセスできないという制約がある。CLI のバージョンは 2.18.0 以上が必要となる。

## Service Account の作成手順

### 前提: 専用 Vault の作成

Service Account は Private Vault にアクセスできないため、CLI 用の Vault を事前に作成する。

1. [my.1password.com](https://my.1password.com) にサインイン
2. 左サイドバーの「保管庫」をクリック
3. 「+ 新規保管庫」で任意の名前（例: `Vault`）を作成

### Service Account の作成

1. 左サイドバーの「開発者」をクリック
2. 「Infrastructure Secrets」→「Service Accounts」を選択
3. 「Create a Service Account」をクリック
4. サービスアカウント名を入力する（例: `cli-automation`）
5. 「保管庫を選択」で先ほど作成した Vault を選択し、権限（読み取り / 読み書き）を設定する
6. 「Environment access」を設定する（デフォルトのままでよい）
7. トークンが表示されるので、即座にコピーして安全な場所に保存する

トークンは作成時に一度だけ表示される。画面を閉じると再表示できないため注意が必要である。

## トークンの設定

取得したトークンを環境変数 `OP_SERVICE_ACCOUNT_TOKEN` として設定する。

```bash
# .zshrc に追記
echo 'export OP_SERVICE_ACCOUNT_TOKEN="ops_xxxxxxxxxxxxxxxxx"' >> ~/.zshrc

# 現在のシェルに反映
source ~/.zshrc
```

`OP_CONNECT_HOST` と `OP_CONNECT_TOKEN` が設定されている場合、これらが `OP_SERVICE_ACCOUNT_TOKEN` より優先されるため、不要であれば削除またはコメントアウトする。

## 動作確認

設定が正しいかを確認する。

```bash
# アクセス可能な Vault の一覧
op vault list
```

出力例:

```
ID                            NAME
xxxxxxxxxxxxxxxxxxxxxxxx      Vault
```

アイテムの操作も確認する。

```bash
# アイテム一覧の確認
op item list --vault "Vault"

# テスト用ログインアイテムの作成
op item create --category login \
  --title "Test Item" \
  --vault "Vault" \
  --url "https://example.com" \
  --generate-password

# 特定アイテムの詳細表示
op item get "Test Item" --vault "Vault"

# アイテムのパスワードフィールドだけ取得
op item get "Test Item" --vault "Vault" --fields password

# セキュアノートの作成
op item create --category "Secure Note" \
  --title "API Config Note" \
  --vault "Vault"

# アイテムの削除
op item delete "Test Item" --vault "Vault"
```

`op read` を使うと、Secret Reference 形式でアイテムのフィールドを直接取得できる。シェルスクリプトでの利用に便利である。

```bash
# Secret Reference 形式でパスワードを取得
op read "op://Vault/Test Item/password"

# 環境変数に代入する例
export DB_PASSWORD=$(op read "op://Vault/db-credentials/password")
```

`op inject` を使うと、テンプレートファイル内のプレースホルダーを 1Password の値で置換できる。

```bash
# テンプレート例（config.tpl）
# DATABASE_URL=postgres://user:{{ op://Vault/db-credentials/password }}@localhost/mydb

op inject -i config.tpl -o config.env
```

`op run` を使うと、環境変数を 1Password から注入してコマンドを実行できる。

```bash
# .env ファイル内の Secret Reference を解決して実行
# .env の内容: API_KEY=op://Vault/api-key/credential
op run --env-file=.env -- python app.py
```

いずれのコマンドもパスワード入力や Touch ID のプロンプトが表示されず完了すれば、設定は成功である。

## まとめ

- 1Password CLI の Service Account を使うと、トークンベースの非対話認証が可能になる
- Private Vault にはアクセスできないため、専用の Vault を作成する必要がある
- `OP_SERVICE_ACCOUNT_TOKEN` 環境変数にトークンを設定するだけで利用開始できる

## 参考資料

{{< linkcard "https://developer.1password.com/docs/service-accounts/" >}}

{{< linkcard "https://developer.1password.com/docs/service-accounts/get-started/" >}}

{{< linkcard "https://developer.1password.com/docs/service-accounts/use-with-1password-cli/" >}}
