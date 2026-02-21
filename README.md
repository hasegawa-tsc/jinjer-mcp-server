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

- **`list_employee_ids`**: 従業員に紐づく社員番号を取得します。
- **`list_employees`**: 従業員情報を詳細に取得します。
- **`list_labor_hour_settings`**: 従業員に紐づく勤怠設定情報を取得します。
- **`list_attendances`**: 従業員に紐づく打刻データ（出退勤時刻など）を取得します。
- **`list_salary_statements`**: 従業員に紐づく給与計算結果（明細情報）を取得します。
- **`list_requested_day_offs`**: 従業員に紐づく休日休暇申請データを取得します。

各ツールの詳細な引数については、MCPクライアントのツール説明、または `server.py` 内の docstring を参照してください。

## ライセンス
MIT License
