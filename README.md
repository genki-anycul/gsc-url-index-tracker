# URLインデックスステータスチェックツール

このツールは、Google Search Console APIとGoogle Sheets APIを使用して、指定したURLのインデックスステータスをGoogleスプレッドシートに記録します。

## 初期設定:APIの有効化とサービスアカウント作成 (5分)

### GCPプロジェクトの作成

1. Google Cloud Platform (GCP)コンソールにアクセスし、新しいプロジェクトを作成します。

### Google Search Console APIの有効化

1. [Google APIコンソール](https://console.developers.google.com/)にアクセスします。
2. 作成したプロジェクトを選択します。
3. ナビゲーションメニューから「APIとサービス」 > 「ライブラリ」を選択します。
4. 「Google Search Console API」を検索し、有効化します。

### Google Sheets APIの有効化

1. [Google APIコンソール](https://console.developers.google.com/)にアクセスします。
2. 作成したプロジェクトを選択します。
3. ナビゲーションメニューから「APIとサービス」 > 「ライブラリ」を選択します。
4. 「Google Sheets API」を検索し、有効化します。

### サービスアカウントの作成

1. [Google APIコンソール](https://console.developers.google.com/)にアクセスします。
2. ナビゲーションメニューから「IAMと管理」 > 「サービスアカウント」を選択します。
3. 「サービスアカウントを作成」をクリックし、必要な情報を入力してサービスアカウントを作成します。
4. サービスアカウントの「鍵」タブに移動し、「鍵を追加」 > 「新しい鍵を作成」をクリックします。
5. 「JSON」を選択して「作成」をクリックすると、秘密鍵がダウンロードされます。このファイルを安全な場所に保存しておきます。

## 権限付与

### 対象スプレッドシートでサービスアカウントへの権限付与

1. Googleスプレッドシートを開きます。
2. 右上の「共有」ボタンをクリックします。
3. サービスアカウントのメールアドレスを入力し、「編集者」権限で共有します。

### Google Search Console側で、サービスアカウントへの権限付与

1. Google Search Consoleにアクセスします。
2. 対象のプロパティを選択します。
3. 「設定」 > 「ユーザーと権限」を選択します。
4. 「ユーザーを追加」をクリックし、サービスアカウントのメールアドレスを入力して「フル」権限を付与します。

## ファイル設置・編集 (5分)

### JSONファイルの設置

- /json直下にダウンロードしたサービスアカウントのJSONファイルを設置します。

### config.pyに必要情報を追加

- `SERVICE_ACCOUNT_FILE`：JSONファイルのパス (例: `json/{ファイル名.json}`)
- `SPREADSHEET_ID`：スプレッドシートのID (例: https://docs.google.com/spreadsheets/d/○○○○○○○○/ の「○○○○○○○○」部分)
- `URL_SHEET_NAME`：URLを記載するシート名
- `DIRECTORY_SHEET_NAME`：ディレクトリ情報を記載するシート名
- `PROPERTY_URL`：プロパティの対象プレフィックスまたはドメイン名を追加
  - 例: 「https://anycul.jp」のURLプレフィックスの場合：「https://anycul.jp」

### 依存ライブラリのインストール

Pythonの推奨環境は、Python 3.6以上です。以下のコマンドを実行して必要な依存ライブラリをインストールします。

```sh
pip install pandas google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

## 実行方法

1. 必要な設定を行ったら、以下のコマンドを実行してスクリプトを起動します。

```sh
python main.py