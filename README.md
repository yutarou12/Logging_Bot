# Logging_Bot

## データベース構造

|カラム名|意味|フィールド|
|:-----:|:----:|:----:|
|guild_id|サーバーID|TEXT, PRIMARY KEY|
|channel_id|ログチャンネルID|TEXT|
|guild_m_add|メンバー参加時|TEXT (true,false)|
|guild_m_remove|メンバー退出時|TEXT (true,false)|
|message_delete|メッセージ削除時|TEXT (true,false)|
|message_edit|メッセージ編集時|TEXT (true,false)|
|role_cre|役職作成時|TEXT (true,false)|
|role_del|役職削除時|TEXT (true,false)|
|channel_cre|チャンネル作成時|TEXT (true,false)|
|channel_del|チャンネル削除時|TEXT (true,false)|
|function|機能 true/false|TEXT (true,false)|