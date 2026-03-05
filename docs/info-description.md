# Overview

ジンジャーAPIを使うことで、ジンジャーDBの情報の取得や登録を行えます。 <br/>こちらのドキュメントで、APIの使い方をご確認ください。

# クイックスタート

## 概要

ジンジャーAPIでは下記のような HTTP リクエストで各種リソースの操作ができます。

HTTP リクエストの構成は以下の通りです。

```sh
$ curl -X {メソッド} https://api.jinjer.biz/{バージョン}/{リソース} \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer {アクセストークン}'
```

- `{メソッド}`: GET や POST などを指定することで、取得や更新などの操作をおこなえます。
- `{バージョン}`: v1 など公開されている API バージョンを指定します。
- `{リソース}`: 従業員情報などの各種情報を指定します。
- `{アクセストークン}`: API リクエストの認証・認可に利用します。

メソッドとリソースの組み合わせは左メニューの API リファレンスをご確認ください。

アクセストークンの発行は下記の「アクセストークンを発行する」をご確認ください。

## 事前準備

API を利用する前に API キーと API シークレットキーを生成・取得する必要があります。

システム管理者権限でジンジャーにログインし、外部サービス連携 > ジンジャーAPI のメニューを開いてください。

ここで生成・取得された API キーと API シークレットキーが、アクセストークンを発行するために必要となります。

## アクセストークンを発行する

API を利用するには、アクセストークンをリクエストに含める必要があります。

アクセストークンは `GET /v1/token` または `GET /v2/token` にリクエストすることで発行されます。

- `GET /v2/token`: 原則こちらをご利用ください。すべての API キーと API シークレットキーを利用できます。
- `GET /v1/token`: デフォルト (1企業につき必ず1組設定されている) の API キー と API シークレットキー のみが利用でき、任意に追加された API キー と API シークレットキーには非対応です。

## API のリクエスト

`GET /v1/token` と `GET /v2/token` 以外の API のエンドポイントを利用するには、アクセストークンをリクエストに含める必要があります。

発行されたアクセストークンをリクエストヘッダ `Authorization` に Bearer として含めてください。

# リクエスト制限

- アクセストークンの有効期限：4時間
- アクセストークンの最大同時払い出し数：特になし
- 取得リクエスト数上限：1社につき毎分100回まで且つ毎時1,500回まで ※ステータスコードが200の場合のみ
- 打刻データの登録リクエスト数上限：1社につき1秒に1回まで且つ毎分60回まで且つ毎時3,600回まで ※ステータスコードが200の場合のみ
- その他の登録/更新リクエスト数上限：1社につき6秒に1回まで且つ毎分10回まで且つ毎時150回まで ※ステータスコードが200の場合のみ

上記のリクエスト数上限に加えて、1つのリクエストが完了するまで次のリクエストを受け付けることはできません。<br/>
短時間に連続してリクエストをおこなう場合、レスポンスが返却されたことを確認してから次のリクエストをおこなってください。

# ページネーション

リストを返すエンドポイントでは、一度に返せる要素の数に制限があります。

制限以上の数の要素が必要となる場合は、ページ番号を指定する必要があり、ページ番号を表すクエリパラメータ `page` を指定することができます。

また、要素の総数はレスポンスヘッダ `X-Item-Counts` で表されます。

従って、たとえば、一度に返せる要素の数が100件に制限されたエンドポイントにおいて、クエリパラメータに合致する要素の数が160件ある場合、レスポンスヘッダ `X-Item-Counts` の値は 160 と返され、クエリパラメータ `page` を指定しない場合は 0-100 件目、`page=2` と指定する場合は 101-160 件目が返却されます。

# API 利用時の注意点

API の利用には、[ジンジャーAPI利用規約](https://hcm-jinjer.com/terms-api/)が適用され、API を利用するとジンジャーAPI利用規約に同意したものとみなされます。

API の呼び出しや繋ぎ込みの実装に関するお問合せはお受付しておりません。リクエストに必要な情報やご利用可能な項目については左メニューの各 API リファレンスをご参照ください。

API の仕様変更は原則的に API バージョンのインクリメントによっておこなわれますが、以下の変更は同一バージョン内でおこなわれる可能性がありますのであらかじめご了承ください。

- クエリパラメータへの新しいキー（要素）の追加
- レスポンスボディへの新しいキー（要素）の追加
- リクエストボディへの必須以外の新しいキー（要素）の追加

API の機能アップデート及び仕様変更の履歴は、[ジンジャーヘルプセンターのアップデート情報](https://jinjer.zendesk.com/hc/ja/sections/26572311021849-API)をご確認ください。

API への機能要望は、[機能に関するご要望フォーム](https://jinjer.zendesk.com/hc/ja/articles/20800623497625)よりお寄せください。

# リクエストの共通仕様

## 特殊文字のエスケープ

POST や PATCH のリクエストボディにおいて、入力値に以下の特殊文字を文字として含める場合は、JSON形式のルールに従い、バックスラッシュ (`¥`) でエスケープして記述する必要があります。

### ダブルクォーテーション

ダブルクォーテーション (`"`) を文字として含める場合、バックスラッシュとダブルクォーテーション (`¥"`) と記述してください。たとえば "Hello, "World"!" という文字列を入力するためには、リクエストボディにおける記述は "Hello, ¥"World¥"!" としてください。

### バックスラッシュ

バックスラッシュ (`¥`) を文字として含める場合、バックスラッシュ2つ (`¥¥`) と記述してください。たとえば "C:¥Users¥User" という文字列を入力するためには、リクエストボディにおける記述は "C:¥¥Users¥¥User" としてください。
 
従って、N個のバックスラッシュ (`¥`) を入力する場合、2N個のバックスラッシュ (`¥¥...¥¥`) を記述してください。

# レスポンスの共通仕様

## レスポンスステータス

レスポンスステータスの体系は以下の通りです。

各レスポンスステータスごとのレスポンスの内容については左メニューの各 API リファレンスをご参照ください。

| ステータスコード | 説明                               |
| ---------------- | ---------------------------------- |
| 200              | 正常                               |
| 400              | パラメータエラー                   |
| 401              | 認証エラー                         |
| 403              | 権限エラー                         |
| 404              | リソースが存在しないエラー         |
| 405              | メソッドが存在しないエラー         |
| 413              | ペイロード上限エラー               |
| 429              | リクエスト数上限エラー             |
| 500              | 予期しない内部エラー               |
| 503              | メンテナンスによりサービス利用不可 |
| 504              | ゲートウェイタイムアウト           |

## Error code list

ジンジャーAPIが返却するエラーコードの体系は以下の通りです。

リクエストサイズの超過やレート制限など API 基盤で検出されたエラーは、以下の体系にないエラーコードや形式でレスポンスされる場合があります。

### 400 Errors

<table>
    <tr>
        <th>Code</th>
        <th>Reason</th>
        <th>Message</th>
    </tr>
    <tr>
        <td>E400QP0001</td>
        <td>Invalid query parameter.</td>
        <td>Query Parameter: {query_parameter_key} is required.</td>
    </tr>
    <tr>
        <td>E400QP0002</td>
        <td>Invalid query parameter.</td>
        <td>Query Parameter: {query_parameter_key} does not support blanks.</td>
    </tr>
    <tr>
        <td>E400QP0003</td>
        <td>Invalid query parameter.</td>
        <td>Query Parameter: {query_parameter_value} is not supported as a value for {query_parameter_key}.</td>
    </tr>
    <tr>
        <td>E400QP0004</td>
        <td>Invalid query parameter.</td>
        <td>Query Parameter: {query_parameter_key} was an invalid validation. This field must be 10 characters or less.<br>or<br>Query Parameter: {query_parameter_key} was an invalid validation. This field must be at least 10 characters.</td>
    </tr>
    <tr>
        <td>E400QP0005</td>
        <td>Invalid query parameter.</td>
        <td>Query Parameter: {query_parameter_key} was an invalid validation. This field must follow format integer.</td>
    </tr>
    <tr>
        <td>E400QP0006</td>
        <td>Invalid query parameter.</td>
        <td>Query Parameter: {query_parameter_key} was an invalid validation. This field must follow format unsigned integer.</td>
    </tr>
    <tr>
        <td>E400QP0007</td>
        <td>Invalid query parameter.</td>
        <td>Query Parameter: {query_parameter_key} was an invalid validation. This field must follow format string.</td>
    </tr>
    <tr>
        <td>E400QP0008</td>
        <td>Invalid query parameter.</td>
        <td>Query Parameter: {query_parameter_key} was an invalid validation. This field must follow format yyyy-MM-dd.</td>
    </tr>
    <tr>
        <td>E400QP0009</td>
        <td>Invalid query parameter.</td>
        <td>Query Parameter: {query_parameter_key} was an invalid validation. This field must follow format yyyy-MM-dd HH:mm:ss.</td>
    </tr>
    <tr>
        <td>E400QP0010</td>
        <td>Invalid query parameter.</td>
        <td>Query Parameter: {query_parameter_key} was an invalid validation. This field must follow format boolean.</td>
    </tr>
    <tr>
        <td>E400QP0011</td>
        <td>Invalid query parameter.</td>
        <td>Query Parameter: {query_parameter_key} was an invalid validation. This field must follow the regular expression ^[a-zA-Z0-9_-]{1,50}$.</td>
    </tr>
    <tr>
        <td>E400QP0012</td>
        <td>Invalid query parameter.</td>
        <td>Query Parameter: {query_parameter_key} was an invalid validation. This field must follow the regular expression ^[a-zA-Z0-9_-]{1,50}$.</td>
    </tr>
    <tr>
        <td>E400QP0013</td>
        <td>Invalid query parameter.</td>
        <td>Query Parameter: {query_parameter_key} was an invalid validation. This field must follow the regular expression ^(?:[A-Za-z0-9_-]{1,50},){0,99}[A-Za-z0-9_-]{1,50}$.</td>
    </tr>
    <tr>
        <td>E400QP0014</td>
        <td>Invalid query parameter.</td>
        <td>Data periods longer than {period} cannot be retrieved.</td>
    </tr>
    <tr>
        <td>E400QP0015</td>
        <td>Invalid query parameter.</td>
        <td>{end_date_key} must be later than {start_date_key}.</td>
    </tr>
    <tr>
        <td>E400QP0016</td>
        <td>Invalid query parameter.</td>
        <td>The query parameter {query_parameter_key} is duplicated.</td>
    </tr>
    <tr>
        <td>E400QP0017</td>
        <td>Invalid query parameter.</td>
        <td>Query Parameter: {query_parameter_key} was an invalid validation. This field can't be dated in the future.</td>
    </tr>
    <tr>
        <td>E400QP0018</td>
        <td>Invalid query parameter.</td>
        <td>Field: {Field} was an invalid validation. This field must follow format yyyy.</td>
    </tr>
    <tr>
        <td>E400QP0019</td>
        <td>Invalid query parameter.</td>
        <td>Field: {Field} was an invalid validation. This field must follow format MM.</td>
    </tr>
    <tr>
        <td>E400QP0021</td>
        <td>Invalid query parameter.</td>
        <td>Field: {Field} was an invalid validation. This field must follow format yyyy-MM.</td>
    </tr>
    <tr>
        <td>E400QP0023</td>
        <td>Invalid query parameter.</td>
        <td>Query Parameter: {query_parameter_key} is not allowed.</td>
    </tr>
    <tr>
        <td>E400P0001</td>
        <td>Invalid path parameter.</td>
        <td>Path Parameter: {path_parameter} contains an unusable character. Acceptable characters are uppercase and lowercase alphabets, Arabic numerals, hyphens, and underscores.</td>
    </tr>
    <tr>
        <td>E400P0002</td>
        <td>Invalid path parameter.</td>
        <td>Path Parameter: {path_parameter} contains an unusable character. Acceptable characters are uppercase and lowercase alphabets, Arabic numerals.</td>
    </tr>
    <tr>
        <td>E400P0004</td>
        <td>Invalid path parameter.</td>
        <td>Path Parameter: {path_parameter} was an invalid validation. This field must be {limit} characters or less.</td>
    </tr>
    <tr>
        <td>E400P0005</td>
        <td>Invalid path parameter.</td>
        <td>Path Parameter: {{#label}} contains an unusable character. Acceptable characters are Arabic numerals.</td>
    </tr>
    <tr>
        <td>E400P0006</td>
        <td>Invalid path parameter.</td>
        <td>Path Parameter: {{#label}} contains an unusable character. Acceptable characters are lowercase alphabets, Arabic numerals.</td>
    </tr>
    <tr>
        <td>E400P0007</td>
        <td>Invalid path parameter.</td>
        <td>Path Parameter: {{#label}} was an invalid validation. This field must be {{#limit}} characters.</td>
    </tr>
    <tr>
        <td>E400H0001</td>
        <td>Invalid header.</td>
        <td>Header: Content-Type is invalid.</td>
    </tr>
    <tr>
        <td>E400H0002</td>
        <td>Invalid header.</td>
        <td>
            Header: Required header does not exist. {header_item_key} is required.
            <ul>
                <li>Header: Required header does not exist. X-API-KEY is required.</li>
                <li>Header: Required header does not exist. X-SECRET-KEY is required.</li>
            </ul>
        </td>
    </tr>
    <tr>
        <td>E400H0003</td>
        <td>Invalid header.</td>
        <td>Please check the X-API-KEY and X-SECRET-KEY value.</td>
    </tr>
    <tr>
        <td>E400B0001</td>
        <td>Invalid request JSON.</td>
        <td>Field: Required parameter does not exist. {Field} is required.</td>
    </tr>
    <tr>
        <td>E400B0002</td>
        <td>Invalid request JSON.</td>
        <td>Request body was empty.</td>
    </tr>
    <tr>
        <td>E400B0003</td>
        <td>Invalid request JSON.</td>
        <td>Invalid Json format.</td>
    </tr>
    <tr>
        <td>E400B0004</td>
        <td>Invalid request JSON.</td>
        <td>Field: {Field} was an invalid validation. This field must be 10 characters or less.<br><br>Field: {Field} was an invalid validation. This field must be at least 10 characters.</td>
    </tr>
    <tr>
        <td>E400B0005</td>
        <td>Invalid request JSON.</td>
        <td>Field: {Field} was an invalid validation. This field must follow format integer.</td>
    </tr>
    <tr>
        <td>E400B0006</td>
        <td>Invalid request JSON.</td>
        <td>Field: {Field} was an invalid validation. This field must follow format unsigned integer.</td>
    </tr>
    <tr>
        <td>E400B0007</td>
        <td>Invalid request JSON.</td>
        <td>Field: {Field} was an invalid validation. This field must follow format string.</td>
    </tr>
    <tr>
        <td>E400B0008</td>
        <td>Invalid request JSON.</td>
        <td>Field: {Field} was an invalid validation. This field must follow format yyyy-MM-dd.</td>
    </tr>
    <tr>
        <td>E400B0009</td>
        <td>Invalid request JSON.</td>
        <td>Field: {Field} was an invalid validation. This field must follow format yyyy-MM-dd HH:mm:ss.</td>
    </tr>
    <tr>
        <td>E400B0010</td>
        <td>Invalid request JSON.</td>
        <td>Field: {Field} was an invalid validation. This field must follow format boolean.</td>
    </tr>
    <tr>
        <td>E400B0011</td>
        <td>Invalid request JSON.</td>
        <td>Field: The value that exists must be specified for {key}.</td>
    </tr>
    <tr>
        <td>E400B0012</td>
        <td>Invalid request JSON.</td>
        <td>Field: {Field} was an invalid validation. This field must follow format full-width or half-width katakana.
            <br>Field: {Field} was an invalid validation. This field must follow format half-width katakana.
            <br>Field: {Field} was an invalid validation. This field must follow format full-width katakana.
        </td>
    </tr>
    <tr>
        <td>E400B0014</td>
        <td>Invalid request JSON.</td>
        <td>Field: {Field} was an invalid validation. This field can't be dated in the future.</td>
    </tr>
    <tr>
        <td>E400B0015</td>
        <td>Invalid request JSON.</td>
        <td>Field: {field_value} is not supported as a value for {field_key}.</td>
    </tr>
    <tr>
        <td>E400B0016</td>
        <td>Invalid request JSON.</td>
        <td>Field: {Field} was an invalid validation. This field must follow the regular expression ^0\d{1,4}-\d{1,4}-\d{3,5}$ and the maximum number input is 11 characters without hyphens.</td>
    </tr>
    <tr>
        <td>E400B0017</td>
        <td>Invalid request JSON.</td>
        <td>Field: {Field} contains an unusable character. Acceptable characters are uppercase and lowercase alphabets, Arabic numerals, hyphens, and underscores.</td>
    </tr>
    <tr>
        <td>E400B0018</td>
        <td>Invalid request JSON.</td>
        <td>Field: {Field} was an invalid validation. This field must follow the regular expression ^\d{3}-\d{4}$.</td>
    </tr>
    <tr>
        <td>E400B0019</td>
        <td>Invalid request JSON.</td>
        <td>Field: {Field} was an invalid validation. This field must follow format yyyy.</td>
    </tr>
    <tr>
        <td>E400B0020</td>
        <td>Invalid request JSON.</td>
        <td>Field: {Field} was an invalid validation. This field must follow format MM.</td>
    </tr>
    <tr>
        <td>E400B0021</td>
        <td>Invalid request JSON.</td>
        <td>Field: {Field} was an invalid validation. This field must follow format dd.</td>
    </tr>
    <tr>
        <td>E400B0022</td>
        <td>Invalid request JSON.</td>
        <td>Field: {Field} was an invalid validation. This field must follow format yyyy-MM.</td>
    </tr>
    <tr>
        <td>E400B0023</td>
        <td>Invalid request JSON.</td>
        <td>Field: 'employee_id' was an invalid validation. The specified 'employee_id' does not exist.</td>
    </tr>
    <tr>
        <td>E400B0024</td>
        <td>Invalid request JSON.</td>
        <td>Field: {Field} contains an unusable character. Acceptable characters are uppercase and lowercase alphabets, Arabic numerals.</td>
    </tr>
    <tr>
        <td>E400B0025</td>
        <td>Invalid request JSON.</td>
        <td>Field: {Field} does not support blanks.</td>
    </tr>
    <tr>
        <td>E400B0026</td>
        <td>Invalid request JSON.</td>
        <td>Field: {Field} must be an object.</td>
    </tr>
    <tr>
        <td>E400B0027</td>
        <td>Invalid request JSON.</td>
        <td>Field: {Field} must be an array.</td>
    </tr>
    <tr>
        <td>E400B0028</td>
        <td>Invalid request JSON.</td>
        <td>Field: {Field} was an invalid validation. This field must follow decimal format.</td>
    </tr>
    <tr>
        <td>E400B0029</td>
        <td>Invalid request JSON.</td>
        <td>Field: {Field} was an invalid validation. This field must not be registered.</td>
    </tr>
    <tr>
        <td>E400B0030</td>
        <td>Invalid request JSON.</td>
        <td>Field: {Field} was an invalid validation. This field {end_date_key} must be later than {start_date_key}.</td>
    </tr>
    <tr>
        <td>E400B0031</td>
        <td>Invalid request JSON.</td>
        <td>Field: {{#label}} must be a valid year between {{#minYear}} and {{#maxYear}}.</td>
    </tr>
    <tr>
        <td>E400B0033</td>
        <td>Invalid request JSON.</td>
        <td>Field: {Field} is not allowed.</td>
    </tr>
    <tr>
        <td>E400B0034</td>
        <td>Invalid request JSON.</td>
        <td>Field: {Field} was an invalid validation. This field must not be duplicated.</td>
    </tr>
    <tr>
        <td>E400B0035</td>
        <td>Invalid request JSON.</td>
        <td>The maximum number of registrations has been reached. No more registrations will be accepted.</td>
    </tr>
    <tr>
        <td>E400B0036</td>
        <td>Invalid request JSON.</td>
        <td>Field: {Field-B} can not be set to Value: {Field-B-value}, when Field: {Field-A} is Value: {Field-A-value}.</td>
    </tr>
    <tr>
        <td>E400B0037</td>
        <td>Invalid request JSON.</td>
        <td>Field: {Field-B} is required, when Field: {Field-A} is Value: {Field-A-value}.</td>
    </tr>
    <tr>
        <td>E400B0038</td>
        <td>Invalid request JSON.</td>
        <td>Field: {{#label}} was an invalid validation. This field must follow unsigned number format.</td>
    </tr>
    <tr>
        <td>E400B0039</td>
        <td>Invalid request JSON.</td>
        <td>Field: {Field} only supports PNG, JPG, JPEG, PDF.</td>
    </tr>
    <tr>
        <td>E400B0040</td>
        <td>Invalid request JSON.</td>
        <td>Field: {Field} only supports PNG, JPG, JPEG, PDF, XLSX, XLS.</td>
    </tr>
    <tr>
        <td>E400B0041</td>
        <td>Invalid request JSON.</td>
        <td>No resources are registered for this employee. Please register the resource first.</td>
    </tr>
    <tr>
        <td>E400B0042</td>
        <td>Invalid request JSON.</td>
        <td>Field: {Field} must be a valid base64 string.</td>
    </tr>
    <tr>
        <td>E400B0043</td>
        <td>Application logic error.</td>
        <td>You can register only {limit} item(s) at a time.</td>
    </tr>
    <tr>
        <td>E400B0044</td>
        <td>Invalid request JSON.</td>
        <td>Field:{Field} was an invalid validation. This field must follow format HH:mm.</td>
    </tr>
    <tr>
        <td>E400B0045</td>
        <td>Invalid request JSON.</td>
        <td>Field: {Field} was an invalid validation. This field {start_date_key} must be earlier than {end_date_key}.</td>
    </tr>
    <tr>
        <td>E400B0046</td>
        <td>Invalid request JSON.</td>
        <td>Field: {Field} must contain at least 1 item.</td>
    </tr>
    <tr>
        <td>E400B0047</td>
        <td>Invalid request JSON.</td>
        <td>Field: {Field} was an invalid validation. This field {to_key} must be after than {from_key}.</td>
    </tr>
    <tr>
        <td>E400D0001</td>
        <td>Conflict data.</td>
        <td>A data inconsistency error is occurring. Please contact the administrator.</td>
    </tr>
    <tr>
        <td>E400D0003</td>
        <td>Conflict data.</td>
        <td>An error occurred. Please try again later.</td>
    </tr>
</table>

### 401 Unauthorized

<table>
    <tr>
        <th>Code</th>
        <th>Reason</th>
        <th>Message</th>
    </tr>
    <tr>
        <td>E401AT0001</td>
        <td>Invalid access token.</td>
        <td>Access token is required.</td>
    </tr>
</table>

### 403 Forbidden

<table>
    <tr>
        <th>Code</th>
        <th>Reason</th>
        <th>Message</th>
    </tr>
    <tr>
        <td>E403AT0001</td>
        <td>Invalid access token.</td>
        <td>Request to this endpoint or method is not allowed.</td>
    </tr>
    <tr>
        <td>E403AT0002</td>
        <td>Invalid access token.</td>
        <td>Access token has expired. Reacquire the access token.</td>
    </tr>
    <tr>
        <td>E403AT0003</td>
        <td>Invalid access token.</td>
        <td>Access token verification failed. Reacquire the access token.</td>
    </tr>
    <tr>
        <td>E403W0001</td>
        <td>Invalid request.</td>
        <td>Request to this endpoint or method is not allowed.</td>
    </tr>
</table>

### 404 Not Found

<table>
    <tr>
        <th>Code</th>
        <th>Reason</th>
        <th>Message</th>
    </tr>
    <tr>
        <td>E404C0001</td>
        <td>Resource not found.</td>
        <td>Please make your request after registering your resource.</td>
    </tr>
</table>

### 405 Method Not Allowed

<table>
    <tr>
        <th>Code</th>
        <th>Reason</th>
        <th>Message</th>
    </tr>
    <tr>
        <td>E405C0001</td>
        <td>The requested method does not exist.</td>
        <td>Please check the API-documentation.</td>
    </tr>
</table>

### 413 Payload Too Large

<table>
    <tr>
        <th>Code</th>
        <th>Reason</th>
    </tr>
    <tr>
        <td>E413PL0001</td>
        <td>Payload Too Large.</td>
    </tr>
</table>

### 429 Too Many Requests

<table>
    <tr>
        <th>Code</th>
        <th>Reason</th>
        <th>Message</th>
    </tr>
    <tr>
        <td>E429C0001</td>
        <td>Too Many Requests.</td>
        <td>Please check the documentation for limit values.</td>
    </tr>
</table>

### 500 Internal Server Error

<table>
    <tr>
        <th>Code</th>
        <th>Reason</th>
    </tr>
    <tr>
        <td>E500ISE0001</td>
        <td>Internal Server Error.</td>
    </tr>
    <tr>
        <td>E500ISE0002</td>
        <td>Internal Server Error.</td>
    </tr>
    <tr>
        <td>E500ISE0003</td>
        <td>Internal Server Error.</td>
    </tr>
    <tr>
        <td>E500ISE0004</td>
        <td>Internal Server Error.</td>
    </tr>
    <tr>
        <td>E500ISE0005</td>
        <td>Internal Server Error.</td>
    </tr>
    <tr>
        <td>E500ISE0006</td>
        <td>Internal Server Error.</td>
    </tr>
    <tr>
        <td>E500ISE0007</td>
        <td>Internal Server Error.</td>
    </tr>
    <tr>
        <td>E500ISE0008</td>
        <td>Internal Server Error.</td>
    </tr>
    <tr>
        <td>E500ISE0009</td>
        <td>Internal Server Error.</td>
    </tr>
    <tr>
        <td>E500ISE0010</td>
        <td>Internal Server Error.</td>
    </tr>
    <tr>
        <td>E500ISE0011</td>
        <td>Internal Server Error.</td>
    </tr>
    <tr>
        <td>E500ISE0012</td>
        <td>Internal Server Error.</td>
    </tr>
    <tr>
        <td>E500ISE0013</td>
        <td>Internal Server Error.</td>
    </tr>
    <tr>
        <td>E500ISE0014</td>
        <td>Internal Server Error.</td>
    </tr>
    <tr>
        <td>E500ISE0015</td>
        <td>Internal Server Error.</td>
    </tr>
</table>

### 503 Service Temporarily Unavailable

<table>
    <tr>
        <th>Code</th>
        <th>Reason</th>
        <th>Message</th>
    </tr>
    <tr>
        <td>E503UTM0001</td>
        <td>Service Temporarily Unavailable.</td>
        <td>Under the maintenance.</td>
    </tr>
</table>

### 504 Gateway Timeout

<table>
    <tr>
        <th>Code</th>
        <th>Reason</th>
    </tr>
    <tr>
        <td>E504TO0001</td>
        <td>Gateway Timeout.</td>
    </tr>
</table>

## ファイルのレスポンス

レスポンスに PDF 文書や画像などのファイルが含まれる場合、署名付き URL としてレスポンスされます。

署名付き URL からファイルを取得してください。

署名付き URL の有効期限は1時間です。
