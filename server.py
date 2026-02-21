from mcp.server.fastmcp import FastMCP
import httpx
import os
import time
from typing import Optional, Any, Dict
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# 環境変数からAPIキーを取得
JINJER_API_KEY = os.environ.get("JINJER_API_KEY")
JINJER_SECRET_KEY = os.environ.get("JINJER_SECRET_KEY")

if not JINJER_API_KEY or not JINJER_SECRET_KEY:
    print("Warning: JINJER_API_KEY and JINJER_SECRET_KEY environment variables are required.")

mcp = FastMCP("jinjer")

class JinjerClient:
    BASE_URL = "https://api.jinjer.biz"

    def __init__(self, api_key: str, secret_key: str):
        self.api_key = api_key
        self.secret_key = secret_key
        self.access_token: Optional[str] = None
        self.token_expiry: float = 0
        self.client = httpx.Client(base_url=self.BASE_URL, timeout=30.0)

    def _get_token(self) -> str:
        """アクセストークンを取得または更新して返す"""
        current_time = time.time()
        # トークンがあり、有効期限切れまでまだ余裕がある(例えば5分以上)場合は既存のトークンを使用
        if self.access_token and current_time < self.token_expiry - 300:
            return self.access_token

        # 新しいトークンを取得 (v2/tokenを使用)
        response = self.client.get(
            "/v2/token",
            headers={
                "X-API-KEY": self.api_key,
                "X-SECRET-KEY": self.secret_key
            }
        )
        response.raise_for_status()
        data = response.json()

        if data.get("results") != "success":
            raise Exception(f"Failed to get token: {data}")

        self.access_token = data["data"]["access_token"]
        # 有効期限は4時間
        self.token_expiry = current_time + (4 * 3600)
        return self.access_token

    def request(self, method: str, path: str, params: Optional[dict] = None, json_data: Optional[dict] = None) -> Dict[str, Any]:
        """認証付きでAPIリクエストを行う"""
        token = self._get_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        response = self.client.request(
            method,
            path,
            headers=headers,
            params=params,
            json=json_data
        )

        # 429 Too Many Requests のハンドリング
        if response.status_code == 429:
            raise Exception("Rate limit exceeded (100 requests/min, 1500 requests/hour)")

        response.raise_for_status()

        # ページネーション情報の取得 (X-Item-Counts)
        item_count = response.headers.get("X-Item-Counts")
        result = response.json()
        if item_count:
            result["_total_count"] = int(item_count)

        return result

# クライアントのインスタンス化
client = None

def get_client() -> JinjerClient:
    global client
    if client is None:
        if not JINJER_API_KEY or not JINJER_SECRET_KEY:
            raise ValueError("JINJER_API_KEY and JINJER_SECRET_KEY environment variables are not set")
        client = JinjerClient(JINJER_API_KEY, JINJER_SECRET_KEY)
    return client

@mcp.tool()
def list_employee_ids(
    page: int = 1,
    employee_id: Optional[str] = None,
    enrollment_classification_id: Optional[str] = None,
    employment_classification_id: Optional[str] = None,
    has_since_changed_at: Optional[str] = None
) -> str:
    """
    従業員に紐づく社員番号を取得します。

    Args:
        page: ページ番号。クエリパラメータが無い場合、100件返却します。101-200件目を取得したい場合、page=2 を指定してください。
        employee_id: 指定された値に社員番号が部分一致するデータを返却します。
        enrollment_classification_id: 在籍区分 (0:在籍, 1:退職, 2:休職)。
        employment_classification_id: 雇用区分ID。
        has_since_changed_at: 指定された年月日以降に新規登録または更新されたデータを返却します (yyyy-MM-dd)。
    """
    try:
        jinjer = get_client()
        params = {"page": page}
        if employee_id:
            params["employee-id"] = employee_id
        if enrollment_classification_id:
            params["enrollment-classification-id"] = enrollment_classification_id
        if employment_classification_id:
            params["employment-classification-id"] = employment_classification_id
        if has_since_changed_at:
            params["has-since-changed-at"] = has_since_changed_at

        result = jinjer.request("GET", "/v1/employees/employee-ids", params=params)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def list_employees(
    page: int = 1,
    employee_ids: Optional[str] = None,
    has_since_changed_at: Optional[str] = None,
    employee_last_name: Optional[str] = None,
    employee_first_name: Optional[str] = None,
    joined_on_period_start_date: Optional[str] = None,
    joined_on_period_end_date: Optional[str] = None,
    retirement_period_start_date: Optional[str] = None,
    retirement_period_end_date: Optional[str] = None,
    enrollment_classification_id: Optional[str] = None,
    employment_classification_id: Optional[str] = None,
) -> str:
    """
    従業員情報を取得します。

    Args:
        page: ページ番号。クエリパラメータが無い場合、100件返却します。101-200件目を取得したい場合、page=2 を指定してください。
        employee_ids: 複数の社員番号をカンマ区切りで指定できます（最大100件）。
        has_since_changed_at: 指定された年月日以降に新規登録または更新されたデータを返却します (yyyy-MM-dd)。
        employee_last_name: 職場氏名（氏）を指定します。
        employee_first_name: 職場氏名（名）を指定します。
        joined_on_period_start_date: 入社年月日の期間指定の開始日 (yyyy-MM-dd)。
        joined_on_period_end_date: 入社年月日の期間指定の終了日 (yyyy-MM-dd)。
        retirement_period_start_date: 退職年月日の期間指定の開始日 (yyyy-MM-dd)。
        retirement_period_end_date: 退職年月日の期間指定の終了日 (yyyy-MM-dd)。
        enrollment_classification_id: 在籍区分 (0:在籍, 1:退職, 2:休職)。
        employment_classification_id: 雇用区分ID。
    """
    try:
        jinjer = get_client()
        params = {"page": page}
        if employee_ids:
            params["employee-ids"] = employee_ids
        if has_since_changed_at:
            params["has-since-changed-at"] = has_since_changed_at
        if employee_last_name:
            params["employee-last-name"] = employee_last_name
        if employee_first_name:
            params["employee-first-name"] = employee_first_name
        if joined_on_period_start_date:
            params["joined-on-period-start-date"] = joined_on_period_start_date
        if joined_on_period_end_date:
            params["joined-on-period-end-date"] = joined_on_period_end_date
        if retirement_period_start_date:
            params["retirement-period-start-date"] = retirement_period_start_date
        if retirement_period_end_date:
            params["retirement-period-end-date"] = retirement_period_end_date
        if enrollment_classification_id:
            params["enrollment-classification-id"] = enrollment_classification_id
        if employment_classification_id:
            params["employment-classification-id"] = employment_classification_id

        result = jinjer.request("GET", "/v1/employees", params=params)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def list_labor_hour_settings(
    page: int = 1,
    employee_ids: Optional[str] = None,
    has_since_changed_at: Optional[str] = None,
    year: Optional[str] = None
) -> str:
    """
    従業員に紐づく勤怠情報を取得します。

    Args:
        page: ページ番号。クエリパラメータが無い場合、100件返却します。101-200件目を取得したい場合、page=2 を指定してください。
        employee_ids: 複数の社員番号をカンマ区切りで指定できます（最大100件）。
        has_since_changed_at: 指定された年月日以降に新規登録または更新されたデータを返却します (yyyy-MM-dd)。
        year: 指定した年のデータ (yyyy)。
    """
    try:
        jinjer = get_client()
        params = {"page": page}
        if employee_ids:
            params["employee-ids"] = employee_ids
        if has_since_changed_at:
            params["has-since-changed-at"] = has_since_changed_at
        if year:
            params["year"] = year

        result = jinjer.request("GET", "/v1/employees/labor-hour-settings", params=params)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def list_attendances(
    month: str,
    page: int = 1,
    employee_ids: Optional[str] = None
) -> str:
    """
    従業員に紐づく打刻データを取得します。

    Args:
        month: 取得する打刻データの年月 (yyyy-MM)。必須。
        page: ページ番号。クエリパラメータが無い場合、20件返却します。21-40件目を取得したい場合、page=2 を指定してください。
        employee_ids: 複数の社員番号をカンマ区切りで指定できます（最大20件）。
    """
    try:
        jinjer = get_client()
        params = {"month": month, "page": page}
        if employee_ids:
            params["employee-ids"] = employee_ids

        result = jinjer.request("GET", "/v2/employees/attendances", params=params)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def list_salary_statements(
    executed_on: str,
    page: int = 1,
    employee_ids: Optional[str] = None,
    has_since_changed_at: Optional[str] = None
) -> str:
    """
    従業員に紐づく給与計算結果を取得します。

    Args:
        executed_on: 指定された処理月のデータを返却します (yyyy-MM)。必須。
        page: ページ番号。クエリパラメータが無い場合、10件返却します。11-20件目を取得したい場合、page=2 を指定してください。
        employee_ids: 複数の社員番号をカンマ区切りで指定できます（最大100件）。
        has_since_changed_at: 指定された年月日以降に新規登録または更新されたデータを返却します (yyyy-MM-dd)。
    """
    try:
        jinjer = get_client()
        params = {"executed-on": executed_on, "page": page}
        if employee_ids:
            params["employee-ids"] = employee_ids
        if has_since_changed_at:
            params["has-since-changed-at"] = has_since_changed_at

        result = jinjer.request("GET", "/v1/employees/salary-statements", params=params)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def list_requested_day_offs(
    month: str,
    page: int = 1,
    employee_ids: Optional[str] = None
) -> str:
    """
    従業員に紐づく休日休暇データを取得します。

    Args:
        month: 取得する休日休暇データの年月 (yyyy-MM)。暦月で指定します。必須。
        page: ページ番号。クエリパラメータが無い場合、20件返却します。21-40件目を取得したい場合、page=2 を指定してください。
        employee_ids: 複数の社員番号をカンマ区切りで指定できます（最大20件）。
    """
    try:
        jinjer = get_client()
        params = {"month": month, "page": page}
        if employee_ids:
            params["employee-ids"] = employee_ids

        result = jinjer.request("GET", "/v2/employees/requested-day-offs", params=params)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()
