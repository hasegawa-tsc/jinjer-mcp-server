# Jinjer MCP Server

Jinjer API (勤怠・人事・給与) と接続するための Model Context Protocol (MCP) サーバー実装です。
Claude などの MCP クライアントから、従業員情報の取得、打刻データの確認、給与明細の照会などを行うことができます。

## セットアップ

### 1. Pythonのインストール
Python 3.12以上が必要です。

### 2. 依存関係のインストール
[uv](https://github.com/astral-sh/uv) を使用してセットアップします：

```bash
uv sync
```

### 3. 環境変数の設定
`.env` ファイルを作成し、以下の情報を設定してください：

```env
JINJER_API_KEY=your_api_key
JINJER_SECRET_KEY=your_secret_key
```

## 使い方

### サーバーの実行
`uv` を使用してサーバーを直接実行できます：

```bash
uv run server.py
```

### MCP クライアント（Claude Desktopなど）での設定

```json
{
  "mcpServers": {
    "jinjer": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/jinjer-mcp-server",
        "run",
        "server.py"
      ]
    }
  }
}
```

## 利用可能なツール

### 従業員・人事情報
- **`list_employee_ids`**: 従業員に紐づく社員番号を取得します。
- **`list_employees`**: 従業員情報を詳細に取得します。
- **`list_employee_addresses`**: 従業員の住所情報を取得します。
- **`list_employee_bank_accounts`**: 従業員の銀行口座情報を取得します。
- **`list_employee_affiliations`**: 従業員の主務（所属・役職など）を取得します。
- **`list_employee_dependents`**: 従業員の被扶養者情報を取得します。

### 勤怠・ワークフロー
- **`list_labor_hour_settings`**: 従業員に紐づく勤怠設定情報を取得します。
- **`list_attendances`**: 従業員に紐づく打刻データ（出退勤時刻など）を取得します。
- **`list_daily_work_data`**: 従業員の日次勤務データ（日締め）を取得します。
- **`list_monthly_work_data`**: 従業員の月次勤務データ（月締め）を取得します。
- **`list_requested_day_offs`**: 従業員に紐づく休日休暇申請データを取得します。

### 給与
- **`list_salary_statements`**: 従業員に紐づく給与計算結果（明細情報）を取得します。

### マスタデータ
- **`list_departments`**: 所属グループ（組織）情報を取得します。
- **`list_employment_classifications`**: 雇用区分マスタを取得します。
- **`list_employee_posts`**: 役職マスタを取得します。

各ツールの詳細な引数については、MCPクライアントのツール説明、または `server.py` 内の docstring を参照してください。

## トラブルシューティング

### 日本語の文字化けについて
Windows環境や特定のターミナルで実行した際、APIレスポンスの日本語が文字化けして表示されることがあります。
これは表示上の問題であり、データ自体は正しく取得されています。

正確な内容を確認したい場合は、以下のように `json.dumps` を使用してエンコーディングを明示的に指定して実行してください：

```bash
uv run python -c "import json; from server import get_client; client = get_client(); res = client.request('GET', '/v1/employees', params={'employee-last-name': '長谷川'}); print(json.dumps(res, ensure_ascii=False))"
```

### 動作確認済みデータ
開発時のテストに使用できる確認済みのデータ例です：
- **社員番号**: 30
- **氏名**: 〇〇 〇〇 (〇〇〇〇 〇〇〇)
- **所属**: 株式会社テック・エス・シー

## ライセンス
MIT License
